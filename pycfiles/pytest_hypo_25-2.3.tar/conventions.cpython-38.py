# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\utils\conventions.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1248 bytes


class UniqueIdentifier:

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return self.identifier


class DefaultValueType(UniqueIdentifier):
    pass


class InferType(UniqueIdentifier):
    pass


infer = InferType('infer')
not_set = UniqueIdentifier('not_set')