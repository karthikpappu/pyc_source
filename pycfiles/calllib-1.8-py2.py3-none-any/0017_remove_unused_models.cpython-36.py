# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0017_remove_unused_models.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 381 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0016_checkboxes')]
    operations = [
     migrations.DeleteModel(name='Date'),
     migrations.DeleteModel(name='SingleLineTextWithMap')]