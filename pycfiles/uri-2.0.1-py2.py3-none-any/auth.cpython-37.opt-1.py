# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/part/auth.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 264 bytes
from __future__ import unicode_literals
from .base import ProxyPart, GroupPart

class AuthenticationPart(GroupPart):
    attributes = ('user', 'password')
    suffix = '@'


class SafeAuthenticationPart(ProxyPart):
    attribute = 'user'
    suffix = '@'