# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/styo/venv/lib/python2.7/site-packages/direct_render/urls.py
# Compiled at: 2015-05-23 10:14:47
from django.conf.urls import url
from .views import direct_render
urlpatterns = [
 url('^(?P<template_name>.*\\.html)$', direct_render)]