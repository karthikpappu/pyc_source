# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0006_auto_20190501_1142.py
# Compiled at: 2019-05-01 03:16:49
from __future__ import unicode_literals
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    File = apps.get_model(b'files', b'File')
    for file in File.objects.all():
        if file.password and file.password != b'':
            file.file_obj.password = file.password
            file.file_obj.iv = file.iv
            file.file_obj.is_encrypt_needed = True
            file.file_obj.save()


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    File = apps.get_model(b'files', b'File')
    for file in File.objects.all():
        if file.file_obj.is_encrypt_needed:
            file.password = file.file_obj.password
            file.iv = file.file_obj.iv
            file.save()


class Migration(migrations.Migration):
    dependencies = [
     ('files', '0005_file_publish_date')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]