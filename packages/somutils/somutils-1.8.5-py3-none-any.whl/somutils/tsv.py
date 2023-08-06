from __future__ import unicode_literals
from yamlns import namespace as ns
from .pathlib import Path
import csv342 as csv # Py2 compatibility, use plain csv when dropped

def tsvread(file):
    """
    Provides ns objects (dict-like) from the rows of a TSV file.
    """
    if not hasattr(file, 'read'):
        with Path(file).open() as of:
            # yield from tsvread(of) # >=Py3.3
            for item in tsvread(of): # <Py3.3
                yield item
            return

    tsv = csv.DictReader(file, delimiter='\t') # Py2 hack, str
    for item in tsv:
        yield ns(item)

def tsvwrite(file, iterable):
    """
    Takes an iterable of dict like objects and dumps it as a TSV file.
    Columns are taken from the keys of the first item.
    """
    if not hasattr(file, 'write'):
        with Path(file).open('w', encoding='utf8') as outputfile:
            return tsvwrite(outputfile, iterable)

    tsv = None
    for item in iterable:
        if not tsv: # first item
            tsv = csv.DictWriter(file,
                fieldnames=item.keys(),
                delimiter='\t',
                lineterminator='\n',
            )
            tsv.writeheader()
        tsv.writerow(item)

