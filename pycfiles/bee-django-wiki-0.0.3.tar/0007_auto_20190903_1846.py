# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_wiki/migrations/0007_auto_20190903_1846.py
# Compiled at: 2019-09-03 06:46:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_wiki', '0006_topicimage')]
    operations = [
     migrations.AlterField(model_name=b'topic', name=b'view_group', field=models.ManyToManyField(to=b'auth.Group', verbose_name=b'可观看的用户组（可多选）'))]