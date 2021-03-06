# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/modules/data_group_type.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 2995 bytes
"""DataGroupType module class"""
from apis.data_group_type_api import DataGroupTypeApi
from common.base import Base
from ..common.config import *
MODULE_NAME = DATA_GROUP_TYPE

class DataGroupType(DataGroupTypeApi):

    def __init__(self, metadata_client, name, identifier, flg_available, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.identifier = identifier
        self.flg_available = flg_available
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_data_group_type_api(self._DataGroupType__get_resource())
        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        if res['success']:
            self.id = res['data']['id']
        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_data_group_type_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_data_group_type_api(self.id, self._DataGroupType__get_resource())
        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, data_group_type_id):
        response = mdc_client.get_data_group_type_by_id_api(data_group_type_id)
        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(mdc_client, name):
        response = mdc_client.get_all_data_group_types_by_name_api(name)
        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all(mdc_client):
        response = mdc_client.get_all_data_group_types_api()
        Base.cal_debug(MODULE_NAME, 'get_all', response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name(mdc_client, name):
        res = DataGroupType.get_all_by_name(mdc_client, name)
        if res['success']:
            res = Base.unique_key_format_result(res=res, module_name=MODULE_NAME,
              unique_id=name)
        return res

    def __get_resource(self):
        data_group_type = {MODULE_NAME: {'name':self.name, 
                       'identifier':self.identifier, 
                       'flg_available':self.flg_available, 
                       'description':self.description}}
        return data_group_type