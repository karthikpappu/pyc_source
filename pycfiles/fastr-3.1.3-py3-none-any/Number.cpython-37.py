# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/Number.py
# Compiled at: 2019-04-10 08:38:03
# Size of source mod 2**32: 877 bytes
from fastr.datatypes import TypeGroup

class Number(TypeGroup):
    description = 'an numeric value'
    _members = ('UnsignedInt', 'Int', 'Float')