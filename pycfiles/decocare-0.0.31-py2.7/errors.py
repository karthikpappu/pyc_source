# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/errors.py
# Compiled at: 2016-03-06 17:04:33


class StickError(Exception):
    pass


class AckError(StickError):
    pass


class BadDeviceCommError(AckError):
    pass


class DataTransferCorruptionError(Exception):
    pass