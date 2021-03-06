# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/urls.py
# Compiled at: 2017-12-07 19:41:42
from django.conf.urls import url
from . import feeds
from . import views
app_name = 'cmsplugin_newsplus'
urlpatterns = [
 url('^$', views.ArchiveIndexView.as_view(), name='news_archive_index'),
 url('^(?P<year>\\d{4})/$', views.YearArchiveView.as_view(), name='news_archive_year'),
 url('^(?P<year>\\d{4})/(?P<month>\\d{2})/$', views.MonthArchiveView.as_view(), name='news_archive_month'),
 url('^(?P<year>\\d{4})/(?P<month>\\d{2})/(?P<day>\\d{2})/$', views.DayArchiveView.as_view(), name='news_archive_day'),
 url('^(?P<year>\\d{4})/(?P<month>\\d{2})/(?P<day>\\d{2})/(?P<slug>[-\\w]+)/$', views.DetailView.as_view(), name='news_detail'),
 url('^feed/$', feeds.NewsFeed())]