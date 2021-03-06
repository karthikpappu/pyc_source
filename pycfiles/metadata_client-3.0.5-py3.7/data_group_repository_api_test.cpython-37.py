# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/data_group_repository_api_test.py
# Compiled at: 2019-03-11 08:28:16
# Size of source mod 2**32: 6365 bytes
"""DataGroupRepositoryApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from common.generators import Generators
from ..common.secrets import *
from ...metadata_client_api import MetadataClientApi

class DataGroupRepositoryApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)

    def test_create_data_group_api(self):
        data_group_repository = {'data_group_repository': {'data_group_id':'-1', 
                                   'repository_id':'11', 
                                   'flg_available':'true'}}
        expect = data_group_repository['data_group_repository']
        received = self._DataGroupRepositoryApiTest__create_entry_api(data_group_repository, expect)
        data_group_repository_id = received['id']
        data_group_id = received['data_group_id']
        repository_id = received['repository_id']
        self._DataGroupRepositoryApiTest__create_error_entry_uk_api(data_group_repository)
        self._DataGroupRepositoryApiTest__get_all_entries_by_data_group_and_repository_ids_api(data_group_id, repository_id, expect)
        self._DataGroupRepositoryApiTest__get_all_entries_by_data_group_id_api(data_group_id, expect)
        self._DataGroupRepositoryApiTest__get_entry_by_id_api(data_group_repository_id, expect)
        self._DataGroupRepositoryApiTest__update_entry_api(data_group_repository_id, data_group_id, repository_id, expect)
        self._DataGroupRepositoryApiTest__delete_entry_by_id_api(data_group_repository_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'data_group_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'repository_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)

    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_data_group_repository_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_data_group_repository_api(entry_info)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {'info': {'data_group_id':['has already been taken'],  'repository_id':[
                   'has already been taken']}}
        self.assertEqual(receive, expect, 'Expected result not received')
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)
        receive_msg = receive['info']['data_group_id'][0]
        expect_msg = expect['info']['data_group_id'][0]
        self.assert_eq_str(receive_msg, expect_msg)
        receive_msg = receive['info']['repository_id'][0]
        expect_msg = expect['info']['repository_id'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, data_group_id, repository_id, expect):
        data_group_repository_upd = {'data_group_repository': {'data_group_id':str(data_group_id), 
                                   'repository_id':str(repository_id), 
                                   'flg_available':'false'}}
        response = self.client_api.update_data_group_repository_api(entry_id, data_group_repository_upd)
        resp_content = self.load_response_content(response)
        receive = resp_content
        expect_upd = data_group_repository_upd['data_group_repository']
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)
        field = 'data_group_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'repository_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_data_group_and_repository_ids_api(self, data_group_id, repository_id, expect):
        response = self.client_api.get_all_by_data_group_id_and_repository_id_api(data_group_id, repository_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_all_entries_by_data_group_id_api(self, data_group_id, expect):
        response = self.client_api.get_all_by_data_group_id_api(data_group_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive[1], expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        resp = self.client_api.get_data_group_repository_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(resp)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_data_group_repository_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()