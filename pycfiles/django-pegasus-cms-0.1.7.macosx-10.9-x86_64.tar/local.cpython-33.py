# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/settings/local.py
# Compiled at: 2015-02-18 13:07:40
# Size of source mod 2**32: 267 bytes
from __future__ import absolute_import, division
from .base import *
INSTALLED_APPS += ('debug_toolbar', )
PRECOMPRESSED_SETTINGS = {'GZIP_PATTERNS': ()}
try:
    from .local_settings import *
except:
    pass