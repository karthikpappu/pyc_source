# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/tests/test_server_commands.py
# Compiled at: 2014-01-08 15:07:06
# Size of source mod 2**32: 4228 bytes
from unittest import TestCase
from ploader.commands import interface_commands

class TestServerCommandAdd(TestCase):

    def setUp(self):
        self.command = interface_commands['add']()

    def test_parse_options(self):
        self.assertTrue(self.command.parse_options('links MyDir'))
        self.assertTrue(self.command.parse_options('links MyDir secretPw42'))
        self.assertTrue(self.command.parse_options('links "MyDir with spaces" secretPw42'))
        self.assertTrue(self.command.parse_options('dlc MyDir'))
        self.assertTrue(self.command.parse_options('dlc MyDir secretPw42'))
        self.assertTrue(self.command.parse_options('dlc "MyDir with spaces" secretPw42'))
        self.assertFalse(self.command.parse_options(''))
        self.assertFalse(self.command.parse_options('links'))
        self.assertFalse(self.command.parse_options('dlc'))
        self.assertFalse(self.command.parse_options('foo'))
        self.assertFalse(self.command.parse_options('foo bar'))
        self.assertFalse(self.command.parse_options('foo links'))
        self.assertFalse(self.command.parse_options('foo dlc'))
        self.assertFalse(self.command.parse_options('links MyDir pw foo'))
        self.assertFalse(self.command.parse_options('dlc MyDir pw foo'))

    def test_add_links(self):
        self.command.type = 'links'
        self.assertFalse(self.command.add_links('www.google.de/'))
        self.assertEqual(self.command.add_links('http://www.google.de/'), 1)
        self.assertEqual(self.command.add_links('http://www.google.de/\nhttp://www.google.de/'), 2)
        self.assertEqual(self.command.add_links('http://www.google.de/ http://www.google.de/'), 2)

    def test_get_obj(self):
        self.command.type = 'links'
        self.command.name = 'Name'
        self.command.passwd = None
        self.command.links = []
        self.assertEqual(self.command.get_obj(), {'type': 'links',  'name': 'Name',  'passwd': '',  'links': []})
        self.command.type = 'links'
        self.command.name = 'Name'
        self.command.passwd = 'secret'
        self.command.links = []
        self.assertEqual(self.command.get_obj(), {'type': 'links',  'name': 'Name',  'passwd': 'secret',  'links': []})
        self.command.type = 'links'
        self.command.name = 'Name'
        self.command.passwd = 'secret'
        self.command.links = ['foo', 'bar', 'baz']
        self.assertEqual(self.command.get_obj(), {'type': 'links',  'name': 'Name',  'passwd': 'secret',  'links': ['foo', 'bar', 'baz']})
        return

    def test_execute(self):
        self._command = interface_commands['add']()
        self.assertEqual(self._command.execute(), ('proceed', 'Enter: "<type:links/dlc> <name> [passwd]"'))
        self.assertEqual(self._command.execute('links MyDir secretPw42'), ('proceed',
                                                                           'Enter one link per line. Terminate with empty line'))
        self.assertEqual(self._command.execute('http://www.google.de google.com'), ('proceed',
                                                                                    1))
        self.assertEqual(self._command.execute('http://www.google.fr'), ('proceed',
                                                                         1))
        self.assertEqual(self._command.execute('just invalid'), ('proceed', 0))
        self.assertEqual(self._command.execute(''), ('return', 'download'))
        self.assertEqual(self._command.execute(), {'type': 'links', 
         'name': 'MyDir', 
         'passwd': 'secretPw42', 
         'links': [
                   'http://www.google.de', 'http://www.google.fr']})
        self._command = interface_commands['add']()
        self.assertEqual(self._command.execute(), ('proceed', 'Enter: "<type:links/dlc> <name> [passwd]"'))
        self.assertEqual(self._command.execute('links MyDir secretPw42 hahaha'), ('error',
                                                                                  'Invalid statement'))
        self._command = interface_commands['add']()
        self.assertEqual(self._command.execute(), ('proceed', 'Enter: "<type:links/dlc> <name> [passwd]"'))
        self.assertEqual(self._command.execute('links MyDir secretPw42'), ('proceed',
                                                                           'Enter one link per line. Terminate with empty line'))
        self.assertEqual(self._command.execute(''), ('return', 'download'))
        self.assertEqual(self._command.execute(), {'type': 'links', 
         'name': 'MyDir', 
         'passwd': 'secretPw42', 
         'links': []})


class TestServerCommandStats(TestCase):

    def setUp(self):
        self.command = interface_commands['stats']()

    def test_execute(self):
        self.assertEqual(self.command.execute('stats'), ('return', 'status'))