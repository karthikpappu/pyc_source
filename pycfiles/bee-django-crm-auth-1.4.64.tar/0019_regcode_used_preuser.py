# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0019_regcode_used_preuser.py
# Compiled at: 2019-04-22 02:36:45
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0018_regcode_used_at')]
    operations = [
     migrations.AddField(model_name=b'regcode', name=b'used_preuser', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.PreUser', verbose_name=b'被谁使用'))]