# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/utils.py
# Compiled at: 2019-06-28 12:46:35
from django.apps import apps
from .settings import DJANGO_SLOOP_SETTINGS

def get_device_model():
    return apps.get_model(*DJANGO_SLOOP_SETTINGS['DEVICE_MODEL'].split('.'))