# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0003_auto_20181026_1131.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 468 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0002_auto_20181025_1543')]
    operations = [
     migrations.AlterField(model_name='course',
       name='teacher_obj',
       field=models.ManyToManyField(blank=True, to='teachers.Teacher', verbose_name='Teachers'))]