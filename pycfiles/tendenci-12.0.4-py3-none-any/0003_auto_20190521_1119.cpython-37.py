# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/entities/migrations/0003_auto_20190521_1119.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 670 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('entities', '0002_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='entity',
       name='entity_type',
       field=models.CharField(blank=True, choices=[('', 'SELECT ONE'), ('Committee', 'Committee'), ('Reporting', 'Reporting'), ('Study Group', 'Study Group'), ('Technical Interest Group', 'Technical Interest Group'), ('Other', 'Other')], default='Reporting', max_length=200, verbose_name='Type'))]