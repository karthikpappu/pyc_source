# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ultracache/tests/settings/22_no_sites.py
# Compiled at: 2019-12-31 02:49:50
# Size of source mod 2**32: 1157 bytes
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
ROOT_URLCONF = 'ultracache.tests.urls'
INSTALLED_APPS = ('test_without_migrations', 'ultracache', 'ultracache.tests', 'django.contrib.auth',
                  'django.contrib.contenttypes', 'django.contrib.sessions', 'crum',
                  'rest_framework')
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
SECRET_KEY = 'SECRET_KEY'
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[],  'APP_DIRS':False, 
  'OPTIONS':{'context_processors':[
    'django.template.context_processors.request'], 
   'loaders':[
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader']}}]
ULTRACACHE = {'purge':{'method': 'ultracache.tests.utils.dummy_purger'}, 
 'drf':{'viewsets': {'*': {}}}, 
 'consider-headers':[
  'cookie']}