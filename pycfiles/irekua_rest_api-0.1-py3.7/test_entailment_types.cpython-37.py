# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/tests/test_entailment_types.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 1619 bytes
from uuid import uuid4
from random import sample
from rest_framework.test import APITestCase
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import TermType
from irekua_rest_api.serializers import entailment_types
from .utils import BaseTestCase, Users, Actions, create_permission_mapping_from_lists

class EntailmentTypeTestCase(BaseTestCase, APITestCase):
    serializer = entailment_types.CreateSerializer
    permissions = create_permission_mapping_from_lists({Actions.LIST: Users.ALL_AUTHENTICATED_USERS, 
     Actions.CREATE: [
                      Users.ADMIN,
                      Users.DEVELOPER], 
     
     Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS, 
     Actions.UPDATE: [
                      Users.ADMIN,
                      Users.DEVELOPER], 
     
     Actions.PARTIAL_UPDATE: [
                              Users.ADMIN,
                              Users.DEVELOPER], 
     
     Actions.DESTROY: [
                       Users.ADMIN,
                       Users.DEVELOPER]})
    term_type_names = [str(uuid4()) for _ in range(50)]

    def setUp(self):
        super().setUp()
        for term_type_name in self.term_type_names:
            TermType.objects.create(name=term_type_name,
              description='random term type',
              is_categorical=True)

    @staticmethod
    def generate_random_json_data():
        source_type, target_type = sample(EntailmentTypeTestCase.term_type_names, 2)
        data = {'source_type':source_type, 
         'target_type':target_type, 
         'metadata_schema':simple_JSON_schema()}
        return data