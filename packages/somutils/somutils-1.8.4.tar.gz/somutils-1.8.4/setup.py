#!/usr/bin/env python
#-*- coding: utf8 -*-

from setuptools import setup
import sys

readme = open("README.md").read()
py2 = sys.version_info < (3,)

setup(
    name = "somutils",
    version = "1.8.4",
    description = "Tools we use at Somenergia and can be useful",
    author = u"César López Ramírez",
    author_email = "cesar.lopez@somenergia.coop",
    url = 'https://github.com/Som-Energia/somenergia-utils',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    license = 'GNU General Public License v3 or later (GPLv3+)',
    py_modules = [
        "sheetfetcher",
        "dbutils",
        "trace",
        ],
    packages=[
        'somutils',
        ],
    scripts=[
        'venv',
        'activate_wrapper.sh',
        'sql2csv.py',
        'enable_destructive_tests.py',
        ],
    install_requires=[
        'yamlns>=0.7',
        'consolemsg',
        'pytz',
        'python-dateutil',
        'csv342', # Py2/3 compatibility
        ] + ([
        'gspread<4', # Py2 dropped
        'google-auth<=1.34', # Py2 dropped
        'google-auth-oauthlib<0.4.2', # Py2 dropped
        'oauthlib<3', # Py2 dropped
        'requests-oauthlib<1.2', # Py2 dropped
        'setuptools_rust<0.11',
        'psycopg2-binary<2.9',
        'decorator<5',
        'cryptography<3.4', # Py2 dropped
        'rsa<4.6',
        'cachetools<4',
        'httplib2<0.18',
        'pathlib2',
        'pyyaml<6',
        'certifi<2022-05-18', # Py2, indirect of request
        ] if py2 else [
        'google-auth',
        'PyOpenSSL',
        'psycopg2-binary',
        'decorator',
        'gspread>=4',
        ]),
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)

