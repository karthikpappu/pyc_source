# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0017_remove_report_autosaved.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 338 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0016_report_contact_voicemail')]
    operations = [
     migrations.RemoveField(model_name='report', name='autosaved')]