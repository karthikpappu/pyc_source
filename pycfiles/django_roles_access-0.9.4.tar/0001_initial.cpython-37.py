# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vicente/Documents/trabajo/desarrollos/roles/django_roles_access/django_roles_access/migrations/0001_initial.py
# Compiled at: 2019-03-19 16:07:20
# Size of source mod 2**32: 2065 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('auth', '0009_alter_user_last_name_max_length')]
    operations = [
     migrations.CreateModel(name='TemplateAccess',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'flag', models.CharField(default=None, help_text='Unique between all applications.Flag is used with template tag check_role to restrict access in templates.', max_length=255, unique=True, verbose_name='Flag')),
      (
       'roles', models.ManyToManyField(help_text='Select the groups (roles) with access with check_role template tag and flag.', related_name='template_access', to='auth.Group', verbose_name='Roles'))],
       options={'verbose_name':'Template access', 
      'verbose_name_plural':'Templates access'}),
     migrations.CreateModel(name='ViewAccess',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'view', models.CharField(default=None, help_text='View name to be secured: <em>namespace:view_name</em>', max_length=255, unique=True, verbose_name='View')),
      (
       'type', models.CharField(choices=[('pu', 'Public'), ('au', 'Authorized'), ('br', 'By role')], default=None, help_text='Type of access for the view. Select from available options.', max_length=2, verbose_name='Type')),
      (
       'roles', models.ManyToManyField(blank=True, help_text='Select the groups (roles) with view access if access type = By role.', related_name='view_access', to='auth.Group', verbose_name='Roles'))],
       options={'verbose_name':'View access', 
      'verbose_name_plural':'Views access'})]