# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangopost\src\djangopost\rest_api\api_permissions.py
# Compiled at: 2020-03-14 00:53:20
# Size of source mod 2**32: 369 bytes
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    message = 'Only the owner of this post can modify it.'

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False