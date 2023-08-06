from __future__ import unicode_literals
import unittest
from yamlns import ns
from .testutils import sandbox_dir, Path
from .dbutils import (
    runsql,
    runsql_cached,
    MissingParameter,
    csvTable,
    nsList,
    fetchNs,
    pgconfig_from_environ,
)
import os
import sys

@unittest.skipIf(not pgconfig_from_environ(),
    "Please specify PGxxx variables to enable those tests"
)
class DBUtils_Test(unittest.TestCase):

    from yamlns.testutils import assertNsEqual

    def write(self, file, content):
        Path(file).write_text(content, encoding='utf8')

    def assertContent(self, file, expected):
        content = Path(file).read_text(encoding='utf8')
        self.assertMultiLineEqual(expected, content)

    def clearPgEnviron(self, prefix='PG'):
        safe = {}
        for var in list(os.environ): # Py2 mutating dict
            if var.startswith(prefix):
                safe[var] = os.environ.pop(var)
        return safe

    def test_pgconfig_from_environ__empty__default(self):
        old_pg_vars = self.clearPgEnviron()
        try:
            self.assertNsEqual(pgconfig_from_environ(), """
                database: postgres
            """)
        finally:
            self.clearPgEnviron()
            os.environ.update(old_pg_vars)

    def test_pgconfig_from_environ__partial_set(self):
        old_pg_vars = self.clearPgEnviron()
        try:
            os.environ.update(
                PGUSER = 'myuser',
                PGHOST = 'myhost',
                PGPASSFILE = 'mypassfile.txt',
            )
            self.assertNsEqual(pgconfig_from_environ(), """
                user: myuser
                host: myhost
                passfile: mypassfile.txt
            """)
        finally:
            self.clearPgEnviron()
            os.environ.update(old_pg_vars)

    def test_pgconfig_from_environ__complete_set(self):
        old_pg_vars = self.clearPgEnviron()
        try:
            os.environ.update(
                PGHOST = 'myhost',
                PGUSER = 'myuser',
                PGPASSWORD = 'mypassword',
                PGPORT = '8034',
                PGDATABASE= 'mydatabase',
                PGPASSFILE = 'mypassfile.txt',
                PGHOSTADDR = '8.8.8.8',
            )
            self.assertNsEqual(pgconfig_from_environ(), """
                database: mydatabase
                user: myuser
                password: mypassword
                host: myhost
                port: '8034'
                passfile: mypassfile.txt
                hostaddr: 8.8.8.8
            """)
        finally:
            self.clearPgEnviron()
            os.environ.update(old_pg_vars)

    def test_pgconfig_from_environ__customPrefix(self):
        old_pg_vars = self.clearPgEnviron()
        try:
            os.environ.update(
                MYDB_HOST = 'myhost',
                MYDB_USER = 'myuser',
                MYDB_PASSWORD = 'mypassword',
                MYDB_PORT = '8034',
                MYDB_DATABASE= 'mydatabase',
                MYDB_PASSFILE = 'mypassfile.txt',
                MYDB_HOSTADDR = '8.8.8.8',
            )
            self.assertNsEqual(pgconfig_from_environ('MYDB_'), """
                database: mydatabase
                user: myuser
                password: mypassword
                host: myhost
                port: '8034'
                passfile: mypassfile.txt
                hostaddr: 8.8.8.8
            """)
        finally:
            self.clearPgEnviron()
            self.clearPgEnviron(prefix='MYDB_')
            os.environ.update(old_pg_vars)

    def test_runsql_helloworld(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()

            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql('hello.sql', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    def test_runsql_custom_configfile(self):
        with sandbox_dir() as sandbox:
            self.write('myconfig.py',
                "psycopg = {!r}".format(pgconfig_from_environ())
            )
            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql('hello.sql', config='myconfig.py')

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    def test_runsql_default_dbconfig(self):
        with sandbox_dir() as sandbox:
            self.write('dbconfig.py',
                "psycopg = {!r}".format(pgconfig_from_environ())
            )
            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql('hello.sql')

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    def test_runsql_parametrized(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT %(name)s as hello"
            )

            result = runsql('hello.sql', config=config, name='Perico')

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: Perico
            """)

    def test_runsql_parametrized_list_asArray(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT %(ids)s as hello"
            )

            result = runsql('hello.sql', config=config, ids=[1,2,3])

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello:
                - 1
                - 2
                - 3
            """)

    def test_runsql_parametrized_tuple_asSet(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT 2 in %(ids)s as hello"
            )
            result = runsql('hello.sql', config=config, ids=(1,2,3))

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: true
            """)

    def test_runsql_missingParameter(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT %(forgottenParameter)s as hello"
            )

            with self.assertRaises(MissingParameter) as ctx:
                result = runsql('hello.sql', config=config)
                list(result) # fetch to force load

            self.assertEquals(format(ctx.exception),
                "forgottenParameter"
            )

    def test_runsql_multirow(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql', """\
                SELECT * FROM (VALUES
                    ('alice', 34),
                    ('bob', 29),
                    ('cynthia', 25))
                AS mytable(name, points)
            """)

            result = runsql('hello.sql', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - name: alice
                points: 34
              - name: bob
                points: 29
              - name: cynthia
                points: 25
            """)


    def test__runsql_cache__firstExecution(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()

            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql_cached('hello.sql', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

            self.assertContent('hello.tsv', (
                "hello\n"
                "world\n"
            ))

    def test__runsql_cache__cacheExists_usesIt(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()

            self.write('hello.sql',
                "SELECT 'world' as hello"
            )
            self.write('hello.tsv', (
                "hello\n"
                "othercontent\n"
            ))

            result = runsql_cached('hello.sql', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: othercontent
            """)


    def test__runsql_cache__force_ignoresCache(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()

            self.write('hello.sql',
                "SELECT 'world' as hello"
            )
            self.write('hello.tsv', (
                "hello\n"
                "othercontent\n"
            ))

            result = runsql_cached('hello.sql', force=True, config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    def test__runsql_cache__force_ignoresCache(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()

            self.write('hello.sql',
                "SELECT 'world' as hello"
            )
            self.write('other.tsv', (
                "hello\n"
                "othercontent\n"
            ))

            result = runsql_cached('hello.sql', cachefile='other.tsv', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: othercontent
            """)


    # csvTable

    def test_csvTable(self):
        with sandbox_dir() as sandbox:
            import psycopg2
            config = pgconfig_from_environ()
            db = psycopg2.connect(**config)
            with db.cursor() as cursor :
                cursor.execute("""\
                    SELECT * FROM (VALUES
                        ('alice', 34),
                        ('bob', 29),
                        ('cynthia', 25))
                    AS mytable(name, points)
                """)

                self.assertMultiLineEqual(csvTable(cursor),
                    "name\tpoints\n"
                    "alice\t34\n"
                    "bob\t29\n"
                    "cynthia\t25"
                )

    # fetchNs

    def test_fetchNs(self):
        with sandbox_dir() as sandbox:
            import psycopg2
            config = pgconfig_from_environ()
            db = psycopg2.connect(**config)
            with db.cursor() as cursor :
                cursor.execute("""\
                    SELECT * FROM (VALUES
                        ('alice', 34),
                        ('bob', 29),
                        ('cynthia', 25))
                    AS mytable(name, points)
                """)
                result = list(fetchNs(cursor))

                self.assertNsEqual(ns(data=result), """\
                  data:
                  - name: alice
                    points: 34
                  - name: bob
                    points: 29
                  - name: cynthia
                    points: 25
                """)

    # nsList

    def test_nsList(self):
        with sandbox_dir() as sandbox:
            import psycopg2
            config = pgconfig_from_environ()
            db = psycopg2.connect(**config)
            with db.cursor() as cursor :
                cursor.execute("""\
                    SELECT * FROM (VALUES
                        ('alice', 34),
                        ('bob', 29),
                        ('cynthia', 25))
                    AS mytable(name, points)
                """)
                result = nsList(cursor)

                self.assertNsEqual(ns(data=result), """\
                  data:
                  - name: alice
                    points: 34
                  - name: bob
                    points: 29
                  - name: cynthia
                    points: 25
                """)

    def test_nsList_resultCanBeUsedOnceTheCursorIsClosed(self):
        with sandbox_dir() as sandbox:
            import psycopg2
            config = pgconfig_from_environ()
            db = psycopg2.connect(**config)
            with db.cursor() as cursor :
                cursor.execute("""\
                    SELECT * FROM (VALUES
                        ('alice', 34),
                        ('bob', 29),
                        ('cynthia', 25))
                    AS mytable(name, points)
                """)
                result = nsList(cursor)

            # outside the "with cursor" block
            self.assertNsEqual(ns(data=result), """\
              data:
              - name: alice
                points: 34
              - name: bob
                points: 29
              - name: cynthia
                points: 25
            """)

