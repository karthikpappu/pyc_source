# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/apis/data_file_api_test.py
# Compiled at: 2020-02-20 08:00:45
# Size of source mod 2**32: 5180 bytes
"""DataFileApiTest class"""
import unittest
from .api_base import ApiBase
from ..common.config_test import *
from ..common.secrets import *
from ...metadata_client_api import MetadataClientApi

class DataFileApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClientApi(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
      client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
      token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
      refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
      auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
      scope=(CLIENT_OAUTH2_INFO['SCOPE']),
      user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
      base_api_url=BASE_API_URL)

    def test_create_data_file_api(self):
        files_ar = [
         {'filename':'s0000.h5', 
          'sequence':'11', 
          'relative_path':'r0001/', 
          'file_format':'TODO!!!'}]
        data_file = {'data_file': {'data_group_id':'2', 
                       'files':str(files_ar)}}
        expect = data_file['data_file']
        received = self._DataFileApiTest__create_entry_api(data_file, expect)
        data_file_id = received['id']
        data_file_data_group_id = received['data_group_id']
        self._DataFileApiTest__create_successfully_entry_uk_api(data_file, expect)
        self._DataFileApiTest__get_all_entries_by_data_group_id_api(data_file_data_group_id, expect)
        self._DataFileApiTest__get_entry_by_id_api(data_file_id, expect)
        self._DataFileApiTest__update_entry_api(data_file_id, expect)
        self._DataFileApiTest__delete_entry_by_id_api(data_file_id)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'data_group_id', NUMBER)
        rec_files = self.escape_and_load_json_from_str(receive['files'])
        exp_files = self.escape_and_load_json_from_str(expect['files'])
        self.assertEqual(len(rec_files), len(exp_files))
        self.assert_eq_hfield(rec_files[0], exp_files[0], 'filename', STRING)
        self.assert_eq_hfield(rec_files[0], exp_files[0], 'sequence', STRING)
        self.assert_eq_hfield(rec_files[0], exp_files[0], 'relative_path', STRING)
        self.assert_eq_hfield(rec_files[0], exp_files[0], 'file_format', STRING)

    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_data_file_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_successfully_entry_uk_api(self, entry_info, expect):
        received = self._DataFileApiTest__create_entry_api(entry_info, expect)
        self._DataFileApiTest__delete_entry_by_id_api(received['id'])

    def __update_entry_api(self, entry_id, expect):
        files_ar = [
         {'filename':'s0001.h5', 
          'sequence':'12', 
          'relative_path':'r0001/', 
          'file_format':'TODO!!!'}]
        data_file_upd = {'data_file': {'data_group_id':'2', 
                       'files':str(files_ar)}}
        resp = self.client_api.update_data_file_api(entry_id, data_file_upd)
        resp_content = self.load_response_content(resp)
        receive = resp_content
        expect_upd = data_file_upd['data_file']
        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(resp.status_code, OK)
        field = 'data_group_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'files'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_data_group_id_api(self, data_group_id, expect):
        response = self.client_api.get_all_data_files_by_data_group_id_api(data_group_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_data_file_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_data_file_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()