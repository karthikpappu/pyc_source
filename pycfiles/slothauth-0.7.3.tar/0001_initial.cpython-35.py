# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/test_mocks/migrations/0001_initial.py
# Compiled at: 2016-03-10 19:05:53
# Size of source mod 2**32: 2749 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone, slothauth.managers, slothauth.utils

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('auth', '0007_alter_validators_add_error_messages')]
    operations = [
     migrations.CreateModel(name='Account', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'password', models.CharField(max_length=128, verbose_name='password')),
      (
       'last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
      (
       'is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
      (
       'first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
      (
       'last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
      (
       'email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
      (
       'is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
      (
       'is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
      (
       'date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
      (
       'passwordless_key', slothauth.utils.RandomField(max_length=32)),
      (
       'one_time_authentication_key', slothauth.utils.RandomField(max_length=32)),
      (
       'password_reset_key', slothauth.utils.RandomField(max_length=32)),
      (
       'groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
      (
       'user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'))], options={'abstract': False}, managers=[
      (
       'objects', slothauth.managers.UserManager())])]