# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/HtmlUtil.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 884 bytes
"""
Created on April 14, 2011

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.
"""
try:
    import regex as re
except ImportError:
    import re

def attrValue(str, name):
    prestuff, matchedName, valuePart = str.lower().partition('charset')
    value = []
    endSep = None
    beforeEquals = True
    for c in valuePart:
        if value:
            if c == endSep or c.isspace() or c in ';':
                break
            value.append(c)
        elif beforeEquals:
            if c == '=':
                beforeEquals = False
            else:
                if c in ('"', "'"):
                    endSep = c
                else:
                    if c == ';':
                        break
                    elif not c.isspace():
                        value.append(c)

    return ''.join(value)