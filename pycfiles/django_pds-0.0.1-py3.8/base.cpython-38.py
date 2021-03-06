# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/controllers/base.py
# Compiled at: 2020-05-09 00:25:55
# Size of source mod 2**32: 2052 bytes
from rest_framework import status
from rest_framework.response import Response
from django_pds.core.base import BaseDocument, SimpleBaseDocument
from django_pds.core.rest.response import error_response
import django_pds.core.utils as document_provider

class BaseController:

    def common_fields(self, a, b):
        return a.intersection(b)

    def get_document(self, document_name):
        return document_provider(document_name)

    def is_base_instance(self, document_name):
        doc = self.get_document(document_name)
        return issubclass(doc, BaseDocument)

    def is_simple_base_doc_instance(self, document_name):
        doc = self.get_document(document_name)
        return issubclass(doc, SimpleBaseDocument)


class RequiredController:

    def required(self, request, *args):
        if request.META.get('REQUEST_METHOD') == 'GET':
            if len(args) > 0:
                response = error_response('Get method should not have required parameters. Config error.', status=400)
                return (True, Response(response, status=(status.HTTP_400_BAD_REQUEST)))
        params, files = request.data, request.FILES
        required_fields = args
        missing_fields = []
        if len(required_fields) == 0:
            return (False, None)
        ignore_on_files = []
        for field in required_fields:
            if params.get(field) is None:
                missing_fields.append(field)
            else:
                ignore_on_files.append(field)
        else:
            for field in required_fields:
                if files.get(field) is None:
                    if field not in ignore_on_files and field not in missing_fields:
                        missing_fields.append(field)
                    if len(missing_fields) == 0:
                        return (False, None)
                response = {'error':400,  'error_message':'missing required payload fields in this request', 
                 'missing_fields':missing_fields}
                return (
                 True, Response(response, status=(status.HTTP_400_BAD_REQUEST)))