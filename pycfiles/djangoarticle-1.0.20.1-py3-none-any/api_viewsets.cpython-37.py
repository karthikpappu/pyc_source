# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoarticle\src\djangoarticle\rest_api\api_viewsets.py
# Compiled at: 2020-03-14 05:57:56
# Size of source mod 2**32: 4241 bytes
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from djangoarticle.models import CategoryModelScheme
from djangoarticle.models import ArticleModelScheme
from djangoarticle.rest_api.api_serializers import CategorySchemeSerializer
from djangoarticle.rest_api.api_serializers import ArticleSchemeSerializer
from djangoarticle.rest_api.api_permissions import IsOwnerOrReadOnly

class CategoryListViewset(ListAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class CategoryListPublishedViewset(ListAPIView):
    queryset = CategoryModelScheme.objects.published()
    serializer_class = CategorySchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class CategoryRetrieveViewset(RetrieveAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    lookup_field = 'slug'


class CategoryUpdateViewset(RetrieveUpdateAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class CategoryDestroyViewset(DestroyAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class CategoryCreateViewset(CreateAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer


class ArticleListViewset(ListAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListPublishedViewset(ListAPIView):
    queryset = ArticleModelScheme.objects.published()
    serializer_class = ArticleSchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListPromotedViewset(ListAPIView):
    queryset = ArticleModelScheme.objects.promoted()
    serializer_class = ArticleSchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListTrendingViewset(ListAPIView):
    queryset = ArticleModelScheme.objects.trending()
    serializer_class = ArticleSchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleListPromoViewset(ListAPIView):
    queryset = ArticleModelScheme.objects.promo()
    serializer_class = ArticleSchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial', )


class ArticleRetrieveViewset(RetrieveAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    lookup_field = 'slug'


class ArticleUpdateViewset(RetrieveUpdateAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ArticleDestroyViewset(DestroyAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ArticleCreateViewset(CreateAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer