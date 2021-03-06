# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/urls/api.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2682 bytes
from django.conf.urls import url, include
app_name = 'aparnik'
urlpatterns = [
 url('^audits/', include('aparnik.contrib.audits.api.urls', namespace='audits')),
 url('^users/', include('aparnik.contrib.users.api.urls', namespace='users')),
 url('^addresses/', include('aparnik.contrib.addresses.api.urls', namespace='addresses')),
 url('^bankaccounts/', include('aparnik.contrib.bankaccounts.api.urls', namespace='bankaccounts')),
 url('^aboutus/', include('aparnik.contrib.aboutus.api.urls', namespace='aboutus')),
 url('^contactus/', include('aparnik.contrib.contactus.api.urls', namespace='contactus')),
 url('^invitations/', include('aparnik.contrib.invitation.api.urls', namespace='invitations')),
 url('^filefields/', include('aparnik.contrib.filefields.api.urls', namespace='files')),
 url('^provinces/', include('aparnik.contrib.province.api.urls', namespace='provinces')),
 url('^models/', include('aparnik.contrib.basemodels.api.urls', namespace='models')),
 url('^bookmarks/', include('aparnik.contrib.bookmarks.api.urls', namespace='bookmarks')),
 url('^reviews/', include('aparnik.contrib.reviews.api.urls', namespace='reviews')),
 url('^qa/', include('aparnik.contrib.questionanswers.api.urls', namespace='qa')),
 url('^pages/', include('aparnik.contrib.pages.api.urls', namespace='pages')),
 url('^sliders/', include('aparnik.contrib.sliders.api.urls', namespace='sliders')),
 url('^notifications/', include('aparnik.contrib.notifications.api.urls', namespace='notifications')),
 url('^notifiesme/', include('aparnik.contrib.notifiesme.api.urls', namespace='notifiesme')),
 url('^supports/', include('aparnik.contrib.supports.api.urls', namespace='supports')),
 url('^faq/', include('aparnik.contrib.faq.api.urls', namespace='faq')),
 url('^tickets/', include('aparnik.contrib.tickets.api.urls', namespace='tickets')),
 url('^termsandconditions/', include('aparnik.contrib.termsandconditions.api.urls', namespace='termsandconditions')),
 url('^categories/', include('aparnik.contrib.categories.api.urls', namespace='categories')),
 url('^chats/', include('aparnik.contrib.chats.api.urls', namespace='chats')),
 url('^segments/', include('aparnik.contrib.segments.api.urls', namespace='segments')),
 url('^shops/', include('aparnik.packages.shops.urls.api', namespace='shops')),
 url('^bank-gateways/', include('aparnik.packages.bankgateways.urls.api', namespace='bank_gateways')),
 url('^educations/', include('aparnik.packages.educations.urls.api', namespace='educations')),
 url('^news/', include('aparnik.packages.news.api.urls', namespace='news'))]