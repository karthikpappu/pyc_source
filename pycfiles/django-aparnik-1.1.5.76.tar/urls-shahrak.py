# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/test/testproject/aparnik/contrib/province/api/urls-shahrak.py
# Compiled at: 2018-01-15 07:17:37
from django.conf.urls import url
from aparnik.contrib.province.api.views import ShahrakCreateAPIView, ShahrakDetailAPIView, ShahrakListAPIView
urlpatterns = [
 url('^$', ShahrakListAPIView.as_view(), name='list'),
 url('^create/$', ShahrakCreateAPIView.as_view(), name='create'),
 url('^(?P<id>\\d+)/$', ShahrakDetailAPIView.as_view(), name='detail')]