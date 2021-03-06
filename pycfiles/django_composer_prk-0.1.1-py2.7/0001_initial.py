# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/migrations/0001_initial.py
# Compiled at: 2017-10-20 11:35:08
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('sites', '0002_alter_domain_unique')]
    operations = [
     migrations.CreateModel(name=b'Column', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'position', models.PositiveIntegerField(default=0)),
      (
       b'width', models.PositiveIntegerField(default=8, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
      (
       b'title', models.CharField(blank=True, help_text=b'The title is rendered at the top of a column.', max_length=256, null=True)),
      (
       b'class_name', models.CharField(blank=True, help_text=b'One or more CSS classes that are applied to the column.', max_length=200, null=True))]),
     migrations.CreateModel(name=b'Row', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'position', models.PositiveIntegerField(default=0)),
      (
       b'class_name', models.CharField(blank=True, help_text=b'One or more CSS classes that are applied to the row.', max_length=200, null=True))]),
     migrations.CreateModel(name=b'Slot', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'url', models.CharField(db_index=True, default=b'/', help_text=b"Where on the site this slot will appear. Start and end with a slash. Example: '/about-us/people/'", max_length=100, verbose_name=b'URL')),
      (
       b'slot_name', models.CharField(choices=[('header', 'Header'), ('content', 'Content'), ('footer', 'Footer')], default=b'content', help_text=b'Which base template slot should this be rendered in?', max_length=32)),
      (
       b'title', models.CharField(help_text=b'A title that may appear in the browser window caption.', max_length=200)),
      (
       b'description', models.TextField(blank=True, help_text=b'A short description. More verbose than the title but limited to one or two sentences.', null=True)),
      (
       b'sites', models.ManyToManyField(blank=True, help_text=b'Sites that this slot will appear on.', to=b'sites.Site'))]),
     migrations.CreateModel(name=b'Tile', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'position', models.PositiveIntegerField(default=0)),
      (
       b'target_object_id', models.PositiveIntegerField(blank=True, null=True)),
      (
       b'view_name', models.CharField(blank=True, help_text=b'A view to be rendered in this tile. This view is typically a snippet of a larger page. If you are unsure test and see if it works - you cannot break anything.', max_length=200, null=True)),
      (
       b'style', models.CharField(blank=True, help_text=b'Display style. This corresponds to a listing or object style template.', max_length=200, null=True)),
      (
       b'class_name', models.CharField(blank=True, help_text=b'One or more CSS classes that are applied to the tile.', max_length=200, null=True)),
      (
       b'column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'composer.Column')),
      (
       b'target_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'tile_target_content_type', to=b'contenttypes.ContentType'))]),
     migrations.AddField(model_name=b'row', name=b'slot', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'composer.Slot')),
     migrations.AddField(model_name=b'column', name=b'row', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'composer.Row'))]