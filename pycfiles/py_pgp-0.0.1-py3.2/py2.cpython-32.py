# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/py2.py
# Compiled at: 2015-08-31 08:17:33


def raise_with(new, old):
    setattr(new, '__cause__', old)
    raise new