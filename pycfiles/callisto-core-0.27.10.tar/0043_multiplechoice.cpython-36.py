# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0043_multiplechoice.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 641 bytes
from __future__ import unicode_literals
from django.db import migrations
import callisto_core.wizard_builder.model_helpers

class Migration(migrations.Migration):
    dependencies = [
     ('wizard_builder', '0042_auto_20171101_1410')]
    operations = [
     migrations.CreateModel(name='MultipleChoice',
       fields=[],
       options={'proxy':True, 
      'indexes':[]},
       bases=(
      callisto_core.wizard_builder.model_helpers.ProxyQuestion,
      'wizard_builder.formquestion'))]