# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/opps/feedcrawler/migrations/0004_auto__add_field_entry_entry_original_id.py
# Compiled at: 2014-07-23 16:20:23
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('feedcrawler_entry', 'entry_original_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_column('feedcrawler_entry', 'entry_original_id')

    models = {'%s.%s' % (User._meta.app_label, User._meta.module_name): {'Meta': {'object_name': User.__name__}}, 'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                      'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'auth.permission': {'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'}, 'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'channels.channel': {'Meta': {'ordering': "['name', 'parent__id', 'published']", 'unique_together': "(('site', 'long_slug', 'slug', 'parent'),)", 'object_name': 'Channel'}, 'date_available': (
                                             'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}), 
                            'date_insert': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                            'date_update': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                            'description': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                            'group': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                            'hat': (
                                  'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                            'homepage': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'include_in_main_rss': (
                                                  'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                            'layout': (
                                     'django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '250', 'db_index': 'True'}), 
                            'level': (
                                    'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                            'lft': (
                                  'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                            'long_slug': (
                                        'django.db.models.fields.SlugField', [], {'max_length': '250'}), 
                            'mirror_site': (
                                          'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'channels_channel_mirror_site'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}), 
                            'name': (
                                   'django.db.models.fields.CharField', [], {'max_length': '60'}), 
                            'order': (
                                    'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                            'paginate_by': (
                                          'django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}), 
                            'parent': (
                                     'mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subchannel'", 'null': 'True', 'to': "orm['channels.Channel']"}), 
                            'published': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}), 
                            'rght': (
                                   'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                            'show_in_menu': (
                                           'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                            'site': (
                                   'django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}), 
                            'site_domain': (
                                          'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                            'site_iid': (
                                       'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}), 
                            'slug': (
                                   'django.db.models.fields.SlugField', [], {'max_length': '150'}), 
                            'tree_id': (
                                      'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                            'user': (
                                   'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})}, 
       'containers.container': {'Meta': {'ordering': "['-date_available']", 'unique_together': "(('site', 'channel_long_slug', 'slug'),)", 'object_name': 'Container'}, 'channel': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['channels.Channel']"}), 
                                'channel_long_slug': (
                                                    'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                                'channel_name': (
                                               'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '140', 'null': 'True', 'blank': 'True'}), 
                                'child_app_label': (
                                                  'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}), 
                                'child_class': (
                                              'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}), 
                                'child_module': (
                                               'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '120', 'null': 'True', 'blank': 'True'}), 
                                'date_available': (
                                                 'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}), 
                                'date_insert': (
                                              'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                'date_update': (
                                              'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                'hat': (
                                      'django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'images': (
                                         'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['images.Image']", 'null': 'True', 'through': "orm['containers.ContainerImage']", 'blank': 'True'}), 
                                'json': (
                                       'opps.db.models.fields.jsonf.JSONField', [], {'null': 'True', 'blank': 'True'}), 
                                'main_image': (
                                             'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'containers_container_mainimage'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['images.Image']"}), 
                                'main_image_caption': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                'mirror_channel': (
                                                 'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'containers_container_mirror_channel'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['channels.Channel']"}), 
                                'mirror_site': (
                                              'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'containers_container_mirror_site'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}), 
                                'polymorphic_ctype': (
                                                    'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_containers.container_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                'published': (
                                            'django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}), 
                                'short_url': (
                                            'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                'show_on_root_channel': (
                                                       'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                'site': (
                                       'django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}), 
                                'site_domain': (
                                              'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                                'site_iid': (
                                           'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}), 
                                'slug': (
                                       'django.db.models.fields.SlugField', [], {'max_length': '150'}), 
                                'source': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                'tags': (
                                       'django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}), 
                                'title': (
                                        'django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}), 
                                'user': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})}, 
       'containers.containerimage': {'Meta': {'ordering': "('order',)", 'object_name': 'ContainerImage'}, 'caption': (
                                               'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                     'container': (
                                                 'django.db.models.fields.related.ForeignKey', [], {'to': "orm['containers.Container']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}), 
                                     'id': (
                                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                     'image': (
                                             'django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}), 
                                     'order': (
                                             'django.db.models.fields.PositiveIntegerField', [], {'default': '0'})}, 
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'feedcrawler.entry': {'Meta': {'ordering': "['-entry_published_time']", 'object_name': 'Entry', '_ormbases': ['containers.Container']}, 'container_ptr': (
                                             'django.db.models.fields.related.OneToOneField', [], {'to': "orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}), 
                             'entry_category': (
                                              'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                             'entry_category_code': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                             'entry_content': (
                                             'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                             'entry_description': (
                                                 'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                             'entry_feed': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedcrawler.Feed']"}), 
                             'entry_json': (
                                          'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                             'entry_link': (
                                          'django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}), 
                             'entry_original_id': (
                                                 'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                             'entry_published_time': (
                                                    'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                             'entry_pulled_time': (
                                                 'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                             'entry_title': (
                                           'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                             'post_created': (
                                            'django.db.models.fields.BooleanField', [], {'default': 'False'})}, 
       'feedcrawler.feed': {'Meta': {'ordering': "['title']", 'object_name': 'Feed'}, 'channel': (
                                      'django.db.models.fields.related.ForeignKey', [], {'to': "orm['channels.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}), 
                            'date_available': (
                                             'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}), 
                            'date_insert': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                            'date_update': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                            'description': (
                                          'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                            'feed_type': (
                                        'django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedcrawler.FeedType']"}), 
                            'group': (
                                    'django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedcrawler.Group']", 'null': 'True', 'blank': 'True'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'interval': (
                                       'django.db.models.fields.PositiveIntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}), 
                            'last_polled_time': (
                                               'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                            'link': (
                                   'django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}), 
                            'main_image': (
                                         'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'feed_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['images.Image']"}), 
                            'max_entries': (
                                          'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                            'mirror_site': (
                                          'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'feedcrawler_feed_mirror_site'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}), 
                            'publish_entries': (
                                              'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                            'published': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}), 
                            'published_time': (
                                             'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                            'site': (
                                   'django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}), 
                            'site_domain': (
                                          'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                            'site_iid': (
                                       'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}), 
                            'slug': (
                                   'django.db.models.fields.SlugField', [], {'max_length': '150'}), 
                            'source_json_params': (
                                                 'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                            'source_password': (
                                              'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                            'source_port': (
                                          'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                            'source_root_folder': (
                                                 'django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '255'}), 
                            'source_url': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                            'source_username': (
                                              'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                            'title': (
                                    'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                            'user': (
                                   'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})}, 
       'feedcrawler.feedtype': {'Meta': {'object_name': 'FeedType'}, 'actions': (
                                          'django.db.models.fields.CharField', [], {'default': "'opps.feedcrawler.actions.rss.RSSActions'", 'max_length': '255'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'name': (
                                       'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}), 
                                'processor': (
                                            'django.db.models.fields.CharField', [], {'default': "'opps.feedcrawler.processors.rss.RSSProcessor'", 'max_length': '255'})}, 
       'feedcrawler.group': {'Meta': {'ordering': "['name']", 'object_name': 'Group'}, 'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'name': (
                                    'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})}, 
       'feedcrawler.processlog': {'Meta': {'object_name': 'ProcessLog'}, 'feed': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedcrawler.Feed']"}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'log_time': (
                                             'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}), 
                                  'text': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                  'type': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}, 
       'images.image': {'Meta': {'object_name': 'Image'}, 'archive': (
                                  'django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'archive_link': (
                                       'django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'crop_example': (
                                       'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'crop_x1': (
                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}), 
                        'crop_x2': (
                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}), 
                        'crop_y1': (
                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}), 
                        'crop_y2': (
                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}), 
                        'date_available': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}), 
                        'date_insert': (
                                      'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                        'date_update': (
                                      'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                        'description': (
                                      'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                        'fit_in': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                        'flip': (
                               'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                        'flop': (
                               'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                        'halign': (
                                 'django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'mirror_site': (
                                      'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'images_image_mirror_site'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}), 
                        'published': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}), 
                        'site': (
                               'django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}), 
                        'site_domain': (
                                      'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                        'site_iid': (
                                   'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}), 
                        'slug': (
                               'django.db.models.fields.SlugField', [], {'max_length': '150'}), 
                        'smart': (
                                'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                        'source': (
                                 'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'tags': (
                               'django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}), 
                        'user': (
                               'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)}), 
                        'valign': (
                                 'django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'})}, 
       'sites.site': {'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}}
    complete_apps = [
     'feedcrawler']