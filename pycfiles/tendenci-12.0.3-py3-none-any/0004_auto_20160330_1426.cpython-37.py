# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/profiles/migrations/0004_auto_20160330_1426.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 418 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('profiles', '0003_auto_20160308_1106')]
    operations = [
     migrations.AlterField(model_name='profile',
       name='allow_anonymous_view',
       field=models.NullBooleanField(default=False, verbose_name='Public can view'))]