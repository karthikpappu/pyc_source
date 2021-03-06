# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bas/dev/django-dmarc/dmarc/migrations/0001_initial.py
# Compiled at: 2018-06-18 18:57:52
# Size of source mod 2**32: 5473 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='FBReport',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'date', models.DateTimeField(db_index=True)),
      (
       'source_ip', models.CharField(max_length=39)),
      (
       'domain', models.CharField(max_length=100)),
      (
       'email_from', models.CharField(blank=True, max_length=100)),
      (
       'email_subject', models.CharField(blank=True, max_length=100)),
      (
       'spf_alignment', models.CharField(blank=True, max_length=10)),
      (
       'dkim_alignment', models.CharField(blank=True, max_length=10)),
      (
       'dmarc_result', models.CharField(blank=True, max_length=10)),
      (
       'description', models.TextField(blank=True, verbose_name='human readable feedback')),
      (
       'email_source', models.TextField(blank=True, verbose_name='source email including rfc822 headers')),
      (
       'feedback_report', models.TextField(blank=True)),
      (
       'feedback_source', models.TextField())]),
     migrations.CreateModel(name='FBReporter',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'org_name', models.CharField(max_length=100, unique=True, verbose_name='Organisation')),
      (
       'email', models.EmailField(max_length=254))]),
     migrations.CreateModel(name='Record',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'source_ip', models.CharField(max_length=39)),
      (
       'recordcount', models.IntegerField()),
      (
       'policyevaluated_disposition', models.CharField(max_length=10)),
      (
       'policyevaluated_dkim', models.CharField(max_length=4)),
      (
       'policyevaluated_spf', models.CharField(max_length=4)),
      (
       'policyevaluated_reasontype', models.CharField(blank=True, max_length=75)),
      (
       'policyevaluated_reasoncomment', models.CharField(blank=True, max_length=100)),
      (
       'identifier_headerfrom', models.CharField(max_length=100))]),
     migrations.CreateModel(name='Report',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'report_id', models.CharField(max_length=100)),
      (
       'date_begin', models.DateTimeField(db_index=True)),
      (
       'date_end', models.DateTimeField()),
      (
       'policy_domain', models.CharField(max_length=100)),
      (
       'policy_adkim', models.CharField(max_length=1, verbose_name='DKIM alignment mode')),
      (
       'policy_aspf', models.CharField(max_length=1, verbose_name='SPF alignment mode')),
      (
       'policy_p', models.CharField(max_length=10, verbose_name='Requested handling policy')),
      (
       'policy_sp', models.CharField(max_length=10, verbose_name='Requested handling policy for subdomains')),
      (
       'policy_pct', models.SmallIntegerField(verbose_name='Sampling rate')),
      (
       'report_xml', models.TextField(blank=True))]),
     migrations.CreateModel(name='Reporter',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'org_name', models.CharField(max_length=100, unique=True, verbose_name='Organisation')),
      (
       'email', models.EmailField(max_length=254))]),
     migrations.CreateModel(name='Result',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'record_type', models.CharField(max_length=4)),
      (
       'domain', models.CharField(max_length=100)),
      (
       'result', models.CharField(max_length=9)),
      (
       'record', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='results', to='dmarc.Record'))]),
     migrations.AddField(model_name='report',
       name='reporter',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='dmarc.Reporter')),
     migrations.AddField(model_name='record',
       name='report',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='records', to='dmarc.Report')),
     migrations.AddField(model_name='fbreport',
       name='reporter',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='dmarc.FBReporter')),
     migrations.AlterUniqueTogether(name='report',
       unique_together=(set([('reporter', 'report_id', 'date_begin')])))]