from __future__ import unicode_literals
from yamlns import namespace as ns
from .pathlib import Path
from .tsv import tsvread, tsvwrite
from consolemsg import step, fail
import os

def pgconfig_from_environ(prefix='PG'):
    """
    Constructs a configuration for runsql from psql environment variables.
    https://www.postgresql.org/docs/current/libpq-envars.html
    You can provide a different prefix from the PG standard to enable
    configuration of different databases.
    """
    environs = dict(
        host=prefix+'HOST',
        user=prefix+'USER',
        password=prefix+'PASSWORD',
        port=prefix+'PORT',
        database=prefix+'DATABASE',
        passfile=prefix+'PASSFILE',
        hostaddr=prefix+'HOSTADDR',
    )
    config = dict(
        (param, value)
        for param, value in (
            (param, os.environ.get(var, None))
            for param, var in environs.items()
        )
        if value is not None
    )
    return config or dict(database='postgres')

def fetchNs(cursor):
	"""
		Wraps a database cursor so that instead of providing data
		as arrays, it provides objects with attributes named
		as the query column names.
	"""

	fields = [column.name for column in cursor.description]
	for row in cursor:
		yield ns(zip(fields, row))

def nsList(cursor) :
	"""
		Given a database cursor, returns a list of objects with the fields
		as attributes for every returned row.
		Use fetchNs for a more optimal usage.
	"""
	return [e for e in fetchNs(cursor) ]

def csvTable(cursor) :
	"""
		Returns retrieved rows as a tab separated values csv with proper headers.
	"""
	fields = [column.name for column in cursor.description]
	return '\n'.join('\t'.join(str(x) for x in line) for line in ([fields] + cursor.fetchall()) )

class MissingParameter(Exception): pass

def runsql(sqlfile, config=None, **kwds):
    """
    Returns the result of the posgresql query in sqlfile after subsituting kwds.
    'config' is used as psycopg
    """
    #step(sqlfile)
    #step(kwds)
    import sys
    if not isinstance(config, dict):
        config = config or 'dbconfig.py'
        import imp
        config = imp.load_source('config', config)
        config = config.psycopg

    sql = Path(sqlfile).read_text(encoding='utf8')

    import psycopg2
    db = psycopg2.connect(**config)

    with db.cursor() as cursor :
        try:
            cursor.execute(sql, kwds)
        except KeyError as e:
            key = e.args[0]
            raise MissingParameter(key)
        for item in fetchNs(cursor):
            yield item


def runsql_cached(sqlfile, cachefile=None, force=False, config=None, **kwds):
    """
    Like runsql but the first time is run, a tsv file with the results
    is dumped, and later executions will skip the query and take those results.
    If no 'cachefile' is provided, sqlfile with '.tsv' suffix will be used.
    Setting 'force' will force the query execution and an updated dump.
    """
    if not cachefile:
        cachefile = Path(sqlfile).with_suffix('.tsv')
    cache = Path(cachefile)

    if force or not cache.exists():
        step("Regenerating cache {}", cache)
        tsvwrite(cache, runsql(sqlfile, config, **kwds))

    step("Reading cache {}", cache)
    for item in tsvread(cache):
        yield item



