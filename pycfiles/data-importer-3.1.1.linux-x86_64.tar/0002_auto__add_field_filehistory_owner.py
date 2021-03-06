# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/south_migrations/0002_auto__add_field_filehistory_owner.py
# Compiled at: 2020-04-17 10:46:24
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('data_importer_filehistory', 'owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True), keep_default=False)

    def backwards(self, orm):
        db.delete_column('data_importer_filehistory', 'owner_id')

    models = {'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                      'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'auth.permission': {'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'}, 'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'auth.user': {'Meta': {'object_name': 'User'}, 'date_joined': (
                                   'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'email': (
                             'django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}), 
                     'first_name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'groups': (
                              'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}), 
                     'id': (
                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                     'is_active': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                     'is_staff': (
                                'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'is_superuser': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'last_login': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'last_name': (
                                 'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'password': (
                                'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                     'user_permissions': (
                                        'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}), 
                     'username': (
                                'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})}, 
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'data_importer.filehistory': {'Meta': {'object_name': 'FileHistory'}, 'active': (
                                              'django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}), 
                                     'content': (
                                               'django.db.models.fields.files.FileField', [], {'max_length': '100'}), 
                                     'created_at': (
                                                  'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                     'id': (
                                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                     'owner': (
                                             'django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}), 
                                     'updated_at': (
                                                  'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}}
    complete_apps = [
     'data_importer']