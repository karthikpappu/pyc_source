#!/usr/bin/env python
# Copyright (c) 2013 Oliver Cope. All rights reserved.
# See LICENSE.txt for terms of redistribution and use.

import os
import re
from setuptools import setup

VERSIONFILE = "tms.py"


def get_version():
    return re.search("^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                     read(VERSIONFILE), re.M).group(1)


def read(*path):
    """\
    Read and return contents of ``path``
    """
    with open(os.path.join(os.path.dirname(__file__), *path),
              'rb') as f:
        return f.read().decode('UTF-8')

setup(
    name='tms',
    version=get_version(),
    url='',

    license='BSD',
    author='Oliver Cope',
    author_email='oliver@redgecko.org',

    description='Test match special: fuzzy value matching for test assertions',
    long_description=read('README.rst') + "\n\n" + read("CHANGELOG.rst"),

    py_modules=['tms'],

    install_requires=[],

    zip_safe=False,
    classifiers=['License :: OSI Approved :: BSD License',
                 'Topic :: Software Development :: Testing',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3'],
)
