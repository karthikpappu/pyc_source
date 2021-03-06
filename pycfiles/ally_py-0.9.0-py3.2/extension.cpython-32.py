# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/api/extension.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Aug 2, 2012

@package: ally api
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides standard extended objects.
"""
from ally.api.config import extension
from collections import Iterable

@extension
class IterPart(Iterable):
    """
    Provides a wrapping for iterable objects that represent a part of a bigger collection. Basically beside the actual
    items this class objects also contain a total count of the big item collection that this iterable is part of.
    """
    total = int
    offset = int
    limit = int

    def __init__(self, wrapped, total, offset=None, limit=None):
        """
        Construct the partial iterable.
        
        @param wrapped: Iterable
            The iterable that provides the actual data.
        """
        assert isinstance(wrapped, Iterable), 'Invalid iterable %s' % wrapped
        self.wrapped = wrapped
        self.total = total
        if offset is None:
            self.offset = 0
        else:
            self.offset = offset
        if limit is None:
            self.limit = total
        else:
            if limit > total:
                self.limit = total
            else:
                self.limit = limit
        return

    def __iter__(self):
        return self.wrapped.__iter__()

    def __str__(self):
        return '%s[%s(%s:%s), %s]' % (self.__class__.__name__, self.total, self.offset, self.limit, self.wrapped)