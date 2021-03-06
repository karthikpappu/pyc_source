# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/jira/uninstalled.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.views.decorators.csrf import csrf_exempt
from sentry.api.base import Endpoint
from sentry.constants import ObjectStatus
from sentry.integrations.atlassian_connect import AtlassianConnectValidationError, get_integration_from_jwt

class JiraUninstalledEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(JiraUninstalledEndpoint, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(' ', 1)[1]
        except (KeyError, IndexError):
            return self.respond(status=400)

        try:
            integration = get_integration_from_jwt(token, request.path, 'jira', request.GET, method='POST')
        except AtlassianConnectValidationError:
            return self.respond(status=400)

        integration.update(status=ObjectStatus.DISABLED)
        return self.respond()