# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/frame/models.py
# Compiled at: 2017-04-19 09:40:55
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Seen(models.Model):
    user = models.OneToOneField(User)
    seen = models.DateTimeField(auto_now=True)


admin.site.register(Seen, list_display=('user', 'seen'))