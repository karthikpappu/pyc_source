# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/data_group_type_api_test.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 5501 bytes
"""DataGroupTypeApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
from ...metadata_client_api import MetadataClientApi

class DataGroupTypeApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)

    def test_create_data_group_type_api(self):
        _DataGroupTypeApiTest__unique_name = Generators.generate_unique_name('DataGroupTypeApi')
        _DataGroupTypeApiTest__unique_identifier = Generators.generate_unique_identifier()
        data_group_type = {'data_group_type': {'name':_DataGroupTypeApiTest__unique_name, 
                             'identifier':_DataGroupTypeApiTest__unique_identifier, 
                             'flg_available':'true', 
                             'description':'desc 01'}}
        expect = data_group_type['data_group_type']
        received = self._DataGroupTypeApiTest__create_entry_api(data_group_type, expect)
        data_group_type_id = received['id']
        data_group_type_name = received['name']
        self._DataGroupTypeApiTest__create_error_entry_uk_api(data_group_type)
        self._DataGroupTypeApiTest__get_all_entries_by_name_api(data_group_type_name, expect)
        self._DataGroupTypeApiTest__get_entry_by_id_api(data_group_type_id, expect)
        self._DataGroupTypeApiTest__update_entry_api(data_group_type_id, expect)
        self._DataGroupTypeApiTest__delete_entry_by_id_api(data_group_type_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_data_group_type_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_data_group_type_api(entry_info)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {'info': {'identifier':['has already been taken'],  'name':[
                   'has already been taken']}}
        self.assertEqual(receive, expect, 'Expected result not received')
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)
        receive_msg = receive['info']['name'][0]
        expect_msg = expect['info']['name'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = Generators.generate_unique_name('ExpTypeApiUpd')
        unique_id_upd = Generators.generate_unique_identifier(1)
        data_group_type_upd = {'data_group_type': {'name':unique_name_upd, 
                             'identifier':unique_id_upd, 
                             'flg_available':'false', 
                             'description':'desc 01 updated!!!'}}
        response = self.client_api.update_data_group_type_api(entry_id, data_group_type_upd)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect_upd = data_group_type_upd['data_group_type']
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)
        field = 'name'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'identifier'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_name_api(self, name, expect):
        response = self.client_api.get_all_data_group_types_by_name_api(name)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_data_group_type_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_data_group_type_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()