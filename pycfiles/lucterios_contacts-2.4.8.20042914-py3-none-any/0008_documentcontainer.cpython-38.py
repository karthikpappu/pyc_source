# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-contacts/lucterios/mailing/migrations/0008_documentcontainer.py
# Compiled at: 2020-03-26 06:35:18
# Size of source mod 2**32: 453 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mailing', '0007_message_statistics')]
    operations = [
     migrations.AddField(model_name='message',
       name='attachments',
       field=models.ManyToManyField(blank=True, to='documents.DocumentContainer', verbose_name='documents'))]