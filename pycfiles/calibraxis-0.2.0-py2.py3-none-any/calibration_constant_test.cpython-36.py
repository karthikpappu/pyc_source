# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/modules/calibration_constant_test.py
# Compiled at: 2019-08-05 13:13:33
# Size of source mod 2**32: 9005 bytes
__doc__ = 'CalibrationConstantTest class'
import unittest
from calibration_client.calibration_client import CalibrationClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.calibration_constant import CalibrationConstant
MODULE_NAME = CALIBRATION_CONSTANT

class CalibrationConstantTest(ModuleBase, unittest.TestCase):

    def setUp(self):
        self.cal_client = CalibrationClient(client_id=(CLIENT_OAUTH2_INFO['CLIENT_ID']),
          client_secret=(CLIENT_OAUTH2_INFO['CLIENT_SECRET']),
          token_url=(CLIENT_OAUTH2_INFO['TOKEN_URL']),
          refresh_url=(CLIENT_OAUTH2_INFO['REFRESH_URL']),
          auth_url=(CLIENT_OAUTH2_INFO['AUTH_URL']),
          scope=(CLIENT_OAUTH2_INFO['SCOPE']),
          user_email=(CLIENT_OAUTH2_INFO['EMAIL']),
          base_api_url=BASE_API_URL)
        _CalibrationConstantTest__unique_name1 = Generators.generate_unique_name('CalConst01')
        self.cc_01 = {'name':_CalibrationConstantTest__unique_name1, 
         'calibration_id':'-2', 
         'device_type_id':'-1', 
         'condition_id':'-1', 
         'flg_auto_approve':'true', 
         'flg_available':'true', 
         'description':'desc 01'}
        _CalibrationConstantTest__unique_name_upd = Generators.generate_unique_name('CalConstUpd01')
        self.cc_01_upd = {'name':_CalibrationConstantTest__unique_name_upd, 
         'calibration_id':'-2', 
         'device_type_id':'-1', 
         'condition_id':'-1', 
         'flg_auto_approve':'false', 
         'flg_available':'false', 
         'description':'desc 01 updated!'}

    def test_create_calibration_constant(self):
        cc_01 = CalibrationConstant(calibration_client=(self.cal_client),
          name=(self.cc_01['name']),
          calibration_id=(self.cc_01['calibration_id']),
          device_type_id=(self.cc_01['device_type_id']),
          condition_id=(self.cc_01['condition_id']),
          flg_auto_approve=(self.cc_01['flg_auto_approve']),
          flg_available=(self.cc_01['flg_available']),
          description=(self.cc_01['description']))
        result1 = cc_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.cc_01)
        calibration_constant = result1['data']
        cc_id = calibration_constant['id']
        cc_name = calibration_constant['name']
        cc_calibration_id = calibration_constant['calibration_id']
        cc_device_type_id = calibration_constant['device_type_id']
        cc_condition_id = calibration_constant['condition_id']
        cc_01_dup = cc_01
        result2 = cc_01_dup.create()
        expect_app_info = {'name':['has already been taken'],  'condition':[
          'has already been taken'], 
         'device_type':[
          'has already been taken'], 
         'calibration':[
          'has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)
        result3 = CalibrationConstant.get_by_name(self.cal_client, cc_name)
        self.assert_find_success(MODULE_NAME, result3, self.cc_01)
        result4 = CalibrationConstant.get_by_id(self.cal_client, cc_id)
        self.assert_find_success(MODULE_NAME, result4, self.cc_01)
        cc_id = -666
        result5 = CalibrationConstant.get_by_id(self.cal_client, cc_id)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)
        result_uk = CalibrationConstant.get_by_uk(self.cal_client, cc_calibration_id, cc_device_type_id, cc_condition_id)
        self.assert_find_success(MODULE_NAME, result_uk, self.cc_01)
        calibration_id = -666
        device_type_id = -666
        condition_id = -666
        res_uk_error = CalibrationConstant.get_by_uk(self.cal_client, calibration_id, device_type_id, condition_id)
        self.assert_find_error(MODULE_NAME, res_uk_error, RESOURCE_NOT_FOUND)
        cc_01.name = self.cc_01_upd['name']
        cc_01.flg_auto_approve = self.cc_01_upd['flg_auto_approve']
        cc_01.flg_available = self.cc_01_upd['flg_available']
        cc_01.description = self.cc_01_upd['description']
        result6 = cc_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.cc_01_upd)
        wrong_name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN'
        wrong_name += '_THE_ALLOWED_MAX_NUM__'
        wrong_name += '_(NUM_CHARACTERS_IS_256)_'
        wrong_name += '-->_{0}'.format('Z' * 170)
        cc_01.name = wrong_name
        cc_01.flg_available = self.cc_01_upd['flg_available']
        cc_01.description = self.cc_01_upd['description']
        result7 = cc_01.update()
        expect_app_info = {'name': ['is too long (maximum is 255 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)
        result8 = cc_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)
        result9 = cc_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_calibration_constant_from_dict(self):
        result1 = CalibrationConstant.set_from_dict(self.cal_client, self.cc_01)
        self.assert_create_success(MODULE_NAME, result1, self.cc_01)
        calibration_constant = result1['data']
        cc_id = calibration_constant['id']
        result2 = CalibrationConstant.create_from_dict(self.cal_client, self.cc_01)
        expect_app_info = {'name':['has already been taken'],  'condition':[
          'has already been taken'], 
         'device_type':[
          'has already been taken'], 
         'calibration':[
          'has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)
        result3 = CalibrationConstant.set_from_dict(self.cal_client, self.cc_01)
        self.assert_find_success(MODULE_NAME, result3, self.cc_01)
        result_uk = CalibrationConstant.set_from_dict(self.cal_client, self.cc_01)
        self.assert_find_success(MODULE_NAME, result_uk, self.cc_01)
        result8 = CalibrationConstant.delete_by_id(self.cal_client, cc_id)
        self.assert_delete_success(MODULE_NAME, result8)
        result9 = CalibrationConstant.delete_by_id(self.cal_client, cc_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'device_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'calibration_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'condition_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_auto_approve', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)


if __name__ == '__main__':
    unittest.main()