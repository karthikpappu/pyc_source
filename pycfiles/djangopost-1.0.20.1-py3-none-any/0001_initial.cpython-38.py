# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangopost\src\djangopost\migrations\0001_initial.py
# Compiled at: 2019-11-22 06:11:33
# Size of source mod 2**32: 3494 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, djangopost.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='CategoryModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'serial', models.IntegerField(blank=True, null=True)),
      (
       'title', models.CharField(max_length=35, unique=True)),
      (
       'slug', models.SlugField(max_length=35, unique=True)),
      (
       'description', models.TextField(blank=True, null=True)),
      (
       'status', models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish'), ('withdraw', 'Withdraw'), ('private', 'Private')], default='draft', max_length=20)),
      (
       'verification', models.BooleanField(default=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'author', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))],
       options={'verbose_name':'Djangopost category', 
      'verbose_name_plural':'Djangopost categories', 
      'ordering':[
       'serial', 'pk']}),
     migrations.CreateModel(name='ArticleModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'serial', models.IntegerField(blank=True, null=True)),
      (
       'cover_image', models.ImageField(blank=True, null=True, upload_to=(djangopost.models.image_upload_destination))),
      (
       'title', models.CharField(max_length=95, unique=True)),
      (
       'slug', models.CharField(max_length=95, unique=True)),
      (
       'description', models.TextField(blank=True, null=True)),
      (
       'shortlines', models.TextField(blank=True, null=True)),
      (
       'content', models.TextField()),
      (
       'verification', models.BooleanField(default=False)),
      (
       'status', models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish'), ('withdraw', 'Withdraw'), ('private', 'Private')], default='draft', max_length=20)),
      (
       'is_promote', models.BooleanField(default=False)),
      (
       'is_trend', models.BooleanField(default=False)),
      (
       'total_views', models.IntegerField(blank=True, default=0, null=True)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'author', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL))),
      (
       'category', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djangopost.CategoryModel'))],
       options={'verbose_name':'Djangopost article', 
      'verbose_name_plural':'Djangopost articles', 
      'ordering':[
       'serial', 'pk']})]