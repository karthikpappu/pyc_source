# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyredatam/utils.py
# Compiled at: 2015-09-21 12:56:27
__doc__ = b'\nutils.py\n\nHelper methods.\n'
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os

def get_data_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), b'data'))