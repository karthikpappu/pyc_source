# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0004_auto_20190129_1728.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 507 bytes
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('vouchers', '0003_auto_20190129_1620')]
    operations = [
     migrations.AlterField(model_name='voucher',
       name='expire_at',
       field=models.DateTimeField(default=(datetime.datetime(2219, 1, 29, 17, 28, 5, 432761)), verbose_name='Expire at'))]