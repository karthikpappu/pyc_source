#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <pjg.github@ubergrabner.net>
# date: 2015/03/31
# copy: (C) Copyright 2015-EOT Canary Health, Inc., All Rights Reserved.
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
  'pyramid              >= 1.4.2',
  'six                  >= 1.6.1',
  'aadict               >= 0.2.2',
  'morph                >= 0.1.2',
  'FormEncode           >= 1.2.5',
  'SQLAlchemy           >= 0.8.2',
]

extras_dependencies = {
}

entrypoints = {
}

classifiers = [
  'Development Status :: 1 - Planning',
  #'Development Status :: 2 - Pre-Alpha',
  #'Development Status :: 3 - Alpha',
  #'Development Status :: 4 - Beta',
  #'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Operating System :: OS Independent',
  'Natural Language :: English',
  'License :: OSI Approved :: MIT License',
  'License :: Public Domain',
]

setup(
  name                  = 'pyramid_pagination',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'Easy pagination for Pyramid applications',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'Philip J Grabner, Canary Health Inc',
  author_email          = 'pjg.github@ubergrabner.net',
  url                   = 'http://github.com/canaryhealth/pyramid_pagination',
  keywords              = 'pyramid application pagination paging',
  packages              = find_packages(),
  platforms             = ['any'],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  extras_require        = extras_dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'pyramid_pagination',
  entry_points          = entrypoints,
  license               = 'MIT (http://opensource.org/licenses/MIT)',
)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
