# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdd/__init__.py
# Compiled at: 2019-06-08 10:30:06
# Size of source mod 2**32: 431 bytes
from __future__ import absolute_import
import os
from .version import __VERSION__ as __version__
from .io import *
from .aliases import *
here = __file__
basedir = os.path.split(here)[0]
example_data = os.path.join(basedir, 'example_data')