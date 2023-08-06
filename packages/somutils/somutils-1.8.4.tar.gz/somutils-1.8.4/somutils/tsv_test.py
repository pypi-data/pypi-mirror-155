from __future__ import unicode_literals

import unittest
from yamlns import ns
from .pathlib import Path
from .testutils import temp_path
from .tsv import tsvwrite, tsvread


class DbUtilsTest(unittest.TestCase):

    def assertContent(self, file, expected):
        path = Path(file)
        self.assertTrue(path.exists())
        content = path.read_text(encoding='utf8')
        self.assertMultiLineEqual(content, expected)

    def write(self, file, content):
        Path(file).write_text(content, encoding='utf8')

    from yamlns.testutils import assertNsEqual

    def test_tsvwrite_empty(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = []
            tsvwrite(tsvfile, data)
            self.assertContent(tsvfile,
                ""
            )

    def test_tsvwrite_singleLine(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value1
                field2: value2
            """)
            tsvwrite(tsvfile, data)
            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value1\tvalue2\n"
            )

    def test_tsvwrite_manyLines(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value11
                field2: value12
              - field1: value21
                field2: value22
            """)
            tsvwrite(tsvfile, data)
            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value11\tvalue12\n"
                "value21\tvalue22\n"
            )

    def test_tsvwrite_generatorData(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value1
                field2: value2
            """)

            tsvwrite(tsvfile, (x for x in data)) # using a generator expression

            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value1\tvalue2\n"
            )

    def test_tsvwrite_openFile(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value1
                field2: value2
            """)
            with tsvfile.open('w', encoding='utf8') as file:
                tsvwrite(file, data) # passing an open file, not a Path

            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value1\tvalue2\n"
            )

    def test_tsvwrite_filename(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value1
                field2: value2
            """)
            tsvwrite(str(tsvfile), data) # passing a string, not a Path
            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value1\tvalue2\n"
            )

    def test_tsvwrite_extraFieldsInLaterLines(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value11
                field2: value12
              - field1: value21
                field2: value22
                field3: value23 # Extra field
            """)

            with self.assertRaises(ValueError) as ctx:
                tsvwrite(tsvfile, data)

            self.assertEqual(format(ctx.exception),
                "dict contains fields not in fieldnames: 'field3'"
            )

    def test_tsvwrite_missingFieldsInLaterLines(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value11
                field2: value12
              - field1: value21
                # missing field2
            """)

            data = tsvwrite(tsvfile, data)

            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value11\tvalue12\n"
                "value21\t\n" # Just empty
            )

    def test_tsvwrite_nonStringsAsStrings(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            data = ns.loads("""
              - field1: value1
                field2: 2  # Number
            """)

            data = tsvwrite(tsvfile, data)

            self.assertContent(tsvfile,
                "field1\tfield2\n"
                "value1\t2\n"
            )

    def test_tsvread_path(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            self.write(tsvfile, 
                "field1\tfield2\n"
                "value11\tvalue12\n"
                "value21\tvalue22\n"
            )

            data = tsvread(tsvfile)

            self.assertNsEqual(list(data), """
              - field1: value11
                field2: value12
              - field1: value21
                field2: value22
            """)

    def test_tsvread_openFile(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            self.write(tsvfile, 
                "field1\tfield2\n"
                "value11\tvalue12\n"
                "value21\tvalue22\n"
            )
            with tsvfile.open('r') as file:
                data = list(tsvread(file))  # using a file object, not a Path

            self.assertNsEqual(data, """
              - field1: value11
                field2: value12
              - field1: value21
                field2: value22
            """)

    def test_tsvread_filename(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            self.write(tsvfile, 
                "field1\tfield2\n"
                "value11\tvalue12\n"
                "value21\tvalue22\n"
            )
            data = tsvread(str(tsvfile))  # using a string, not a Path

            self.assertNsEqual(list(data), """
              - field1: value11
                field2: value12
              - field1: value21
                field2: value22
            """)

    def test_tsvread_intFields_parsedAsStrings(self):
        with temp_path() as tmp:
            tsvfile = tmp/'data.tsv'
            self.write(tsvfile, 
                "field1\tfield2\n"
                "value11\t1\n"
            )
            data = tsvread(tsvfile)

            self.assertNsEqual(list(data), """
              - field1: value11
                field2: '1'  # string not number
            """)


