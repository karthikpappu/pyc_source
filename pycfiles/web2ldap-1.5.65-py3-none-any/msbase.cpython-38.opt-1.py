# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/msbase.py
# Compiled at: 2020-04-26 05:22:07
# Size of source mod 2**32: 2431 bytes
"""
msbase.py - some basic stuff

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
from collections import defaultdict

class DefaultDict(defaultdict):
    __doc__ = '\n    Dictionary which returns a default value for non-existent keys.\n    '

    def __init__(self, data=None, default=None):
        defaultdict.__init__(self, default=default)
        self.__default__ = default
        data = data or {}
        for key, val in data.items():
            self.__setitem__(key, val)

    def __missing__(self, key):
        return self.__default__


class Str1stValueDict(DefaultDict):
    __doc__ = '\n    Dicitionary class which always returns first item of value sequence\n    '

    def __setitem__(self, key, val):
        DefaultDict.__setitem__(self, key, val[0])


class GrabKeys:
    __doc__ = '\n    Class for grabbing the dict keys out of a C-style formatter string\n    '

    def __init__(self, fmt: str):
        self.keys = set()
        _ = fmt % self

    def __call__(self):
        return self.keys

    def __getitem__(self, name):
        self.keys.add(name)
        return ''


class CaseinsensitiveStringKeyDict(DefaultDict):
    __doc__ = '\n    Dictionary class for case-insensitive string-keyed dictionaries\n    '

    def __init__(self, default_dict=None, default=None):
        DefaultDict.__init__(self, default=default)
        self.update(default_dict or {})

    def __setitem__(self, key, value):
        DefaultDict.__setitem__(self, key.lower(), value)

    def __getitem__(self, key):
        return DefaultDict.__getitem__(self, key.lower())


def chunks(l, s):
    """
    generator returns which returns chunks of items in :l:
    of length :s:
    """
    q, r = divmod(len(l), s)
    for i in range(q):
        (yield l[i * s:(i + 1) * s])
    else:
        if r:
            (yield l[q * s:])


def ascii_dump(buf: bytes, repl: str='.') -> str:
    """
    Converts bytes in :buf: to str with non-ASCII chars replaced by :repl:.
    """
    assert isinstance(buf, bytes), ValueError('Expected buf to be bytes, got %r' % (buf,))
    res = []
    for b in buf:
        if ord(' ') <= b <= ord('~'):
            res.append(chr(b))
        else:
            res.append(repl)
    else:
        return ''.join(res)