# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0013_grade_cert_image.py
# Compiled at: 2018-01-19 02:20:28
from __future__ import unicode_literals
import django.core.files.storage
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0012_remove_grade_cert_image')]
    operations = [
     migrations.AddField(model_name=b'grade', name=b'cert_image', field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'media/exam/cert'), upload_to=b'', verbose_name=b'证书图片'))]