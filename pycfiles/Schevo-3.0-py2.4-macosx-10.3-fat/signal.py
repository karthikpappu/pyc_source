# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/signal.py
# Compiled at: 2007-03-21 14:34:41
"""PyDispatcher signals.

For copyright, license, and warranty, see bottom of file.
"""
from schevo.constant import _GLOBAL

class TransactionExecuted(object):
    """Signal sent using PyDispatcher to indicate that a transaction
    was successfully executed."""
    __module__ = __name__
    __metaclass__ = _GLOBAL