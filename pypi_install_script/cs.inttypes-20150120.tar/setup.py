#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.inttypes',
  description = 'various trite types associated with integers, such as bitmasks, flags and enums',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20150120',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers', 'Development Status :: 4 - Beta', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  keywords = ['python2', 'python3'],
  long_description = 'Various integer relates classes and functions.\n==============================================\n\nThis modules contains various types built on integers, such as bitmasks, flags and enums: BitMask, Flags, Enum.\n\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.inttypes'],
)
