# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/path.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 363 bytes
from __future__ import unicode_literals
from .string import String
from ....schema.compat import unicode, py3
try:
    from pathlib import PurePosixPath as _Path
except ImportError:
    from pathlib2 import PurePosixPath as _Path

class Path(String):

    def to_native(self, obj, name, value):
        return _Path(value)