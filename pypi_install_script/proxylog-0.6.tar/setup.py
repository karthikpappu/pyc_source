#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@uberdev.org>
# date: 2013/12/14
# copy: (C) Copyright 2013-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import os, sys, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kw):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kw.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.5.3',
]

dependencies = [
  'distribute           >= 0.6.24',
  'pxml                 >= 0.2.10',
  'blessings            >= 1.5',
  'six                  >= 1.4.1',
  'aadict               >= 0.2.1',
  'morph                >= 0.1.1',
  'asset                >= 0.6',
  'requests             >= 2.1.0',
  'PyYAML               >= 3.10',
  'Pygments             >= 1.6',
]

entrypoints = {
  'console_scripts': [
    'proxylog           = proxylog.cli:main',
  ],
}

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Operating System :: OS Independent',
  'Natural Language :: English',
  'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
]

setup(
  name                  = 'proxylog',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'A simple, logging, colorizing, pretty-formatting, HTTP proxy.',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'metagriffin',
  author_email          = 'mg.pypi@uberdev.org',
  url                   = 'http://github.com/metagriffin/proxylog',
  keywords              = 'http proxy logging xml colorize prettify',
  packages              = find_packages(),
  platforms             = ['any'],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'proxylog',
  entry_points          = entrypoints,
  license               = 'GPLv3+',
)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
