# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0012_auto_20190701_0911.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 641 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0011_auto_20190615_1430')]
    operations = [
     migrations.AddField(model_name='filefield',
       name='multi_quality',
       field=models.BooleanField(default=False, verbose_name='Multi Quality')),
     migrations.AddField(model_name='filefield',
       name='multi_quality_processing',
       field=models.IntegerField(default=(-1), verbose_name='Multi Quality Processing'))]