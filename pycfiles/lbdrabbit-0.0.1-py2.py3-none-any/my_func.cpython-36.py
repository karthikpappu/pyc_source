# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/handlers/my_func.py
# Compiled at: 2019-09-26 19:05:14
# Size of source mod 2**32: 173 bytes


def handler(event, context):
    if event.get('name'):
        return 'Hello {}!'.format(event.get('name'))
    else:
        return 'Hello World!'