# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/context_var/__init__.py
# Compiled at: 2020-03-15 16:14:17
# Size of source mod 2**32: 405 bytes
from contextlib import contextmanager

class ContextVar:
    __doc__ = '\n    Dynamically-scoped "context" variable.\n\n    See tests/test_all.py for example usage.\n    '

    def __init__(self, default=None):
        self.values = [default]

    @contextmanager
    def set(self, value):
        self.values.append(value)
        yield
        self.values.pop()

    def get(self):
        return self.values[(-1)]