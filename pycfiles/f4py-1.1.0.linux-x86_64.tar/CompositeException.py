# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/f4py/exception/CompositeException.py
# Compiled at: 2016-03-10 01:40:29


class CompositeException(Exception):

    def __init__(self, e1, e2):
        super().__init__(e1)
        self.__cause__ = e2