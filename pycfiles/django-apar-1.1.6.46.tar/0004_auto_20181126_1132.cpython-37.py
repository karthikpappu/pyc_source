# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/contactus/migrations/0004_auto_20181126_1132.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1007 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0004_auto_20181103_2233'),
     ('contactus', '0003_auto_20181126_1132')]
    operations = [
     migrations.RemoveField(model_name='contactus',
       name='created_at'),
     migrations.RemoveField(model_name='contactus',
       name='id'),
     migrations.RemoveField(model_name='contactus',
       name='update_at'),
     migrations.AddField(model_name='contactus',
       name='basemodel_ptr',
       field=models.OneToOneField(auto_created=True, default=1, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='basemodels.BaseModel'),
       preserve_default=False)]