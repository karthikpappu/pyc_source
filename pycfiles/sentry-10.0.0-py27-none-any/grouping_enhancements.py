# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/grouping_enhancements.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.grouping.enhancer import ENHANCEMENT_BASES

class GroupingEnhancementsEndpoint(Endpoint):
    permission_classes = ()

    def get(self, request):
        return Response(serialize([ e.as_dict() for e in sorted(ENHANCEMENT_BASES.values(), key=lambda x: x.id) ]))