# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0052_contract_status.py
# Compiled at: 2020-03-24 16:47:33
# Size of source mod 2**32: 445 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0051_contract')]
    operations = [
     migrations.AddField(model_name='contract',
       name='status',
       field=models.CharField(blank=True, choices=[(0, 'Inactive'), (1, 'Active')], max_length=20, null=True))]