# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0005_delete_encrypted_fields_from_match_report.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 974 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0004_encrypt_existing_matching_entries')]
    operations = [
     migrations.RemoveField(model_name='matchreport', name='contact_name'),
     migrations.RemoveField(model_name='matchreport', name='contact_notes'),
     migrations.RemoveField(model_name='matchreport', name='contact_phone'),
     migrations.RemoveField(model_name='matchreport', name='contact_voicemail'),
     migrations.RemoveField(model_name='matchreport', name='name'),
     migrations.AlterField(model_name='matchreport',
       name='encrypted',
       field=(models.BinaryField())),
     migrations.AlterField(model_name='matchreport',
       name='salt',
       field=models.CharField(max_length=256))]