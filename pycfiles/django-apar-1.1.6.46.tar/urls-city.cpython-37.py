# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/province/api/urls-city.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 490 bytes
from django.conf.urls import include, url
from aparnik.contrib.province.api.views import CityCreateAPIView, CityDetailAPIView, CityListAPIView
app_name = 'province'
urlpatterns = [
 url('^$', (CityListAPIView.as_view()), name='list'),
 url('^create/$', (CityCreateAPIView.as_view()), name='create'),
 url('^(?P<id>\\d+)/$', (CityDetailAPIView.as_view()), name='detail'),
 url('^(?P<city_id>\\d+)/town/', include('aparnik.contrib.province.api.urls-town', namespace='town-api'))]