# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/source/ambition-edc/venv/lib/python3.7/site-packages/edc_selenium/wsgi.py
# Compiled at: 2018-07-21 05:52:01
# Size of source mod 2**32: 401 bytes
"""
WSGI config for edc_selenium project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edc_selenium.settings')
application = get_wsgi_application()