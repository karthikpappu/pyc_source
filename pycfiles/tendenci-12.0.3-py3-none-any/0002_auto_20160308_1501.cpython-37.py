# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/invoices/migrations/0002_auto_20160308_1501.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 563 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('invoices', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='invoice',
       name='bill_to_country',
       field=models.CharField(max_length=255, null=True, blank=True)),
     migrations.AlterField(model_name='invoice',
       name='ship_to_country',
       field=models.CharField(max_length=255, blank=True))]