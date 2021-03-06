# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoarticle\src\djangoarticle\rest_api\api_serializers.py
# Compiled at: 2020-03-14 05:57:24
# Size of source mod 2**32: 2362 bytes
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from djangoarticle.models import CategoryModelScheme
from djangoarticle.models import ArticleModelScheme

class CategorySchemeSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(view_name='djangoarticle:category_retrieve_viewset',
      lookup_field='slug')
    api_update_url = HyperlinkedIdentityField(view_name='djangoarticle:category_update_viewset',
      lookup_field='slug')
    api_delete_url = HyperlinkedIdentityField(view_name='djangoarticle:category_destroy_viewset',
      lookup_field='slug')
    detail_url = HyperlinkedIdentityField(view_name='djangoarticle:category_detail_view',
      lookup_field='slug',
      lookup_url_kwarg='category_slug')

    class Meta:
        model = CategoryModelScheme
        fields = ['serial', 'title', 'slug', 'description', 'author', 'status', 'verification',
         'created_at', 'updated_at', 'api_detail_url', 'api_update_url', 'api_delete_url',
         'detail_url']


class ArticleSchemeSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(view_name='djangoarticle:article_retrieve_viewset',
      lookup_field='slug')
    api_update_url = HyperlinkedIdentityField(view_name='djangoarticle:article_update_viewset',
      lookup_field='slug')
    api_delete_url = HyperlinkedIdentityField(view_name='djangoarticle:article_destroy_viewset',
      lookup_field='slug')
    detail_url = HyperlinkedIdentityField(view_name='djangoarticle:article_detail_view',
      lookup_field='slug',
      lookup_url_kwarg='article_slug')

    class Meta:
        model = ArticleModelScheme
        fields = ['serial', 'cover_image', 'title', 'slug', 'category', 'description', 'shortlines',
         'content', 'author', 'status', 'verification', 'is_promote', 'is_trend',
         'total_views', 'created_at', 'updated_at', 'api_detail_url', 'api_update_url',
         'api_delete_url', 'detail_url']