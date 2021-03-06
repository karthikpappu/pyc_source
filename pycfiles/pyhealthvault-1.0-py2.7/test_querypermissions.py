# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_querypermissions.py
# Compiled at: 2015-12-14 14:43:47
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.querypermissions import QueryPermissions

class TestQueryPermissions(TestBase):

    def test_querypermissions(self):
        itemtypes = [
         '822a5e5a-14f1-4d06-b92f-8f3f1b05218f',
         'a5033c9d-08cf-4204-9bd3-cb412ce39fc0',
         '3b3e6b16-eb69-483c-8d7e-dfe116ae6092',
         '40750a6a-89b2-455c-bd8d-b420a4cb500b']
        method = QueryPermissions(itemtypes)
        method.execute(self.connection)
        for i in method.response.permissions:
            self.assertIn(i.thing_type_id, itemtypes)
            self.assertTrue(i.offline_access_permissions is not None or i.online_access_permissions is not None)
            if i.offline_access_permissions is not None:
                self.assertNotEqual(i.offline_access_permissions.permission, 0)
            if i.online_access_permissions is not None:
                self.assertNotEqual(i.online_access_permissions.permission, 0)

        return