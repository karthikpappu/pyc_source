# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/analytics/events/sentry_app_created.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import
from sentry import analytics

class SentryAppCreatedEvent(analytics.Event):
    type = 'sentry_app.created'
    attributes = (
     analytics.Attribute('user_id'),
     analytics.Attribute('organization_id'),
     analytics.Attribute('sentry_app'))


analytics.register(SentryAppCreatedEvent)