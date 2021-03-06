# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\clients\test_Client.py
# Compiled at: 2016-03-08 18:42:10
import operator
from b3.clients import Client, Group
from mock import Mock, patch, ANY
from b3 import TEAM_UNKNOWN, TEAM_RED, TEAM_BLUE
from b3.clients import Alias, IpAlias
import unittest2 as unittest
from tests import B3TestCase

class Test_Client(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        self.client = Client(console=self.console)

    def test_construct(self):
        c = Client(name='Courgette', guid='1234567890')
        self.assertEqual(c.name, 'Courgette')
        self.assertEqual(c.exactName, 'Courgette^7')
        self.assertEqual(c.guid, '1234567890')
        self.assertEqual(c.team, TEAM_UNKNOWN)
        self.assertTrue(c.connected)
        self.assertFalse(c.hide)
        self.assertEqual(c.ip, '')
        self.assertEqual(c.greeting, '')
        self.assertEqual(c.pbid, '')

    def test_team(self):
        m = Mock()
        self.client.team = m
        self.assertEqual(self.client.team, m)

    def test_team_change(self):
        self.client._team = TEAM_RED
        with self.assertRaiseEvent(event_type='EVT_CLIENT_TEAM_CHANGE', event_client=self.client, event_data=TEAM_BLUE):
            self.client.team = TEAM_BLUE
        self.client._team = TEAM_RED
        with self.assertRaiseEvent(event_type='EVT_CLIENT_TEAM_CHANGE2', event_client=self.client, event_data={'previous': TEAM_RED, 'new': TEAM_BLUE}):
            self.client.team = TEAM_BLUE

    def test_name_change(self):
        self.client.authed = True
        with self.assertRaiseEvent(event_type='EVT_CLIENT_NAME_CHANGE', event_client=self.client, event_data='cucurb'):
            self.client.name = 'cucurb'

    def test_makeAlias_new(self):
        self.client.id = 123
        self.console.storage.getClientAlias = Mock(side_effect=KeyError())
        self.client.makeAlias('bar')
        self.assertEquals(self.console.storage.getClientAlias.call_count, 1)
        alias = self.console.storage.getClientAlias.call_args[0][0]
        self.assertIsInstance(alias, Alias)
        self.assertEqual(alias.alias, 'bar')
        self.assertEqual(alias.numUsed, 1)

    def test_makeAlias_existing(self):
        self.client.id = 123
        aliasFoo = Alias()
        aliasFoo.alias = 'foo'
        aliasFoo.clientId = self.client.id
        aliasFoo.numUsed = 48
        self.console.storage.getClientAlias = Mock(side_effect=lambda x: aliasFoo)
        self.client.makeAlias('whatever')
        self.assertEquals(self.console.storage.getClientAlias.call_count, 1)
        self.assertIsInstance(aliasFoo, Alias)
        self.assertEqual(aliasFoo.alias, 'foo')
        self.assertEqual(aliasFoo.numUsed, 49)

    def test_guid_readonly(self):
        self.assertFalse(self.client.authed)
        self.client.guid = 'foo'
        self.assertEqual(self.client.guid, 'foo')
        self.client.auth()
        self.assertTrue(self.client.authed)
        self.client.guid = 'bar'
        self.assertFalse(self.client.authed)
        self.client.guid = 'foo'

    def test_set_ip(self):
        self.client.ip = '1.2.3.4'
        self.assertEqual(self.client._ip, '1.2.3.4')
        self.client.ip = '5.6.7.8:27960'
        self.assertEqual(self.client._ip, '5.6.7.8')

    def test_makeIpAlias_new(self):
        self.client.id = 123
        self.console.storage.getClientIpAddress = Mock(side_effect=KeyError())
        self.client.makeIpAlias('1.4.7.8')
        self.assertEquals(self.console.storage.getClientIpAddress.call_count, 1)
        alias = self.console.storage.getClientIpAddress.call_args[0][0]
        self.assertIsInstance(alias, IpAlias)
        self.assertEqual(alias.ip, '1.4.7.8')
        self.assertEqual(alias.numUsed, 1)

    def test_makeIpAlias_existing(self):
        self.client.id = 123
        aliasFoo = IpAlias()
        aliasFoo.ip = '9.5.4.4'
        aliasFoo.clientId = self.client.id
        aliasFoo.numUsed = 8
        self.console.storage.getClientIpAddress = Mock(side_effect=lambda x: aliasFoo)
        self.client.makeIpAlias('whatever')
        self.assertEquals(self.console.storage.getClientIpAddress.call_count, 1)
        self.assertIsInstance(aliasFoo, IpAlias)
        self.assertEqual(aliasFoo.ip, '9.5.4.4')
        self.assertEqual(aliasFoo.numUsed, 9)


class Test_Client_groups(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        self.client = Client(console=self.console)
        self.group_guest = self.console.storage.getGroup(Group(keyword='guest'))
        self.group_user = self.console.storage.getGroup(Group(keyword='user'))
        self.group_reg = self.console.storage.getGroup(Group(keyword='reg'))
        self.group_mod = self.console.storage.getGroup(Group(keyword='mod'))
        self.group_admin = self.console.storage.getGroup(Group(keyword='admin'))
        self.group_fulladmin = self.console.storage.getGroup(Group(keyword='fulladmin'))
        self.group_senioradmin = self.console.storage.getGroup(Group(keyword='senioradmin'))
        self.group_superadmin = self.console.storage.getGroup(Group(keyword='superadmin'))

    def assertGroups(self, groups):
        keywords = map(operator.attrgetter('keyword'), groups)
        self.assertListEqual(keywords, map(operator.attrgetter('keyword'), self.client.groups))
        self.assertListEqual(keywords, map(operator.attrgetter('keyword'), self.client.getGroups()))

    def test_addGroup(self):
        self.client.addGroup(self.group_mod)
        self.assertGroups([self.group_mod])
        self.client.addGroup(self.group_superadmin)
        self.assertGroups([self.group_mod, self.group_superadmin])

    def test_rmGroup(self):
        self.client.addGroup(self.group_mod)
        self.assertGroups([self.group_mod])
        self.client.addGroup(self.group_superadmin)
        self.client.remGroup(self.group_mod)
        self.assertGroups([self.group_superadmin])

    def test_guest_group_is_the_default_group_when_none(self):
        self.assertGroups([self.group_guest])
        self.client.remGroup(self.group_guest)
        self.assertGroups([self.group_guest])
        self.client.addGroup(self.group_admin)
        self.assertGroups([self.group_admin])

    def test_inGroup(self):
        self.assertFalse(self.client.inGroup(self.group_guest))
        self.assertFalse(self.client.inGroup(self.group_user))
        self.assertFalse(self.client.inGroup(self.group_reg))
        self.assertFalse(self.client.inGroup(self.group_mod))
        self.assertFalse(self.client.inGroup(self.group_admin))
        self.assertFalse(self.client.inGroup(self.group_fulladmin))
        self.assertFalse(self.client.inGroup(self.group_senioradmin))
        self.assertFalse(self.client.inGroup(self.group_superadmin))
        self.client.addGroup(self.group_user)
        self.assertTrue(self.client.inGroup(self.group_user))
        self.client.addGroup(self.group_reg)
        self.assertTrue(self.client.inGroup(self.group_reg))
        self.client.addGroup(self.group_mod)
        self.assertTrue(self.client.inGroup(self.group_mod))
        self.client.addGroup(self.group_admin)
        self.assertTrue(self.client.inGroup(self.group_admin))
        self.client.addGroup(self.group_fulladmin)
        self.assertTrue(self.client.inGroup(self.group_fulladmin))
        self.client.addGroup(self.group_senioradmin)
        self.assertTrue(self.client.inGroup(self.group_senioradmin))
        self.client.addGroup(self.group_superadmin)
        self.assertTrue(self.client.inGroup(self.group_superadmin))


class Test_Client_events(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        self.queueEvent_patcher = patch.object(self.console, 'queueEvent')
        self.queueEvent_mock = self.queueEvent_patcher.start()
        self.admin = Client(console=self.console)
        self.client = Client(console=self.console)
        self.client.save()

    def tearDown(self):
        B3TestCase.tearDown(self)
        self.queueEvent_patcher.stop()

    def test_warn(self):
        with self.assertRaiseEvent(event_type='EVT_CLIENT_WARN', event_client=self.client, event_data={'reason': 'insulting admin', 
           'duration': 300, 
           'data': 'foobar', 
           'admin': self.admin, 
           'timeExpire': ANY}, event_target=None):
            self.client.warn(duration='5h', warning='insulting admin', keyword=None, admin=self.admin, data='foobar')
        return

    def test_notice(self):
        with self.assertRaiseEvent(event_type='EVT_CLIENT_NOTICE', event_client=self.client, event_data={'notice': 'keep a eye on this guy', 
           'admin': self.admin, 
           'timeAdd': ANY}):
            self.client.notice(notice='keep a eye on this guy', spare=None, admin=self.admin)
        return


if __name__ == '__main__':
    unittest.main()