# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jake/Github/django-jasmine/django_jasmine/settings.py
# Compiled at: 2017-05-08 18:59:13
from django.conf import settings
DEFAULT_JASMINE_TAG = 'v2.6.1'
DEFAULT_JASMINE_VERSION = getattr(settings, 'DEFAULT_JASMINE_VERSION', DEFAULT_JASMINE_TAG)