# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cardberg/__init__.py
# Compiled at: 2019-10-03 03:26:20
from .error import CardbergError, APIConnectionError, APIError
from .resource import Card
api_credentials = None
timeout = 30
CARDBERG_API_ENDPOINT = 'http://loys.cardberg.com/api/'