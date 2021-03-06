# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_platform.py
# Compiled at: 2011-04-20 15:31:07
import unittest, os, sys, tempfile
from linkexchange.platform import Platform
from linkexchange.config import file_config
from test_clients import SapeTestServer

class SapeTestServer1(SapeTestServer):
    data = {'/': [
           '<a href="url1">xlink1</a>',
           '<a href="url2">xlink2</a>'], 
       '/path/1': [
                 '<a href="url1">xlink1</a>',
                 '<a href="url2">xlink2</a>',
                 '<a href="url3">xlink3</a>',
                 '<a href="url4">xlink4</a>'], 
       '/path/2': [
                 'Plain text and <a href="url">link text</a>'], 
       '__sape_new_url__': '<!--x12345-->', 
       '__sape_delimiter__': '. '}


class SapeTestServer2(SapeTestServer):
    data = {'/': [
           '<a href="url1">ylink1</a>'], 
       '__sape_new_url__': '<!--y12345-->', 
       '__sape_delimiter__': '. '}


class PlatformTestCase(unittest.TestCase):

    def setUpClass(cls):
        cls.server1 = SapeTestServer1()
        cls.server2 = SapeTestServer2()
        clients = [
         ('sape', [],
          dict(user='user123456789', db_driver=('mem', ), server_list=[
           cls.server1.url.replace('%', '%%')])),
         (
          'sape', [],
          dict(user='user123456789', db_driver=('mem', ), server_list=[
           cls.server2.url.replace('%', '%%')]))]
        cls.platform = Platform(clients=clients)

    setUpClass = classmethod(setUpClass)

    def tearDownClass(cls):
        del cls.platform
        del cls.server1
        del cls.server2

    tearDownClass = classmethod(tearDownClass)

    def testGetRawLinks(self):
        lx = self.platform.get_raw_links('http://example.com/')
        self.assertEqual(unicode(lx[0]), '<a href="url1">xlink1</a>')
        self.assertEqual(unicode(lx[1]), '<a href="url2">xlink2</a>')
        self.assertEqual(unicode(lx[2]), '<a href="url1">ylink1</a>')

    def testGetBlocks(self):
        formatters = [
         (
          'inline', [2],
          dict(class_='links', class_for_empty='empty', suffix='. ')),
         (
          'list', [None], dict(id='links'))]
        bx = self.platform.get_blocks('http://example.com/', formatters)
        self.assertEqual(unicode(bx[0]), '<div class="links"><a href="url1">xlink1</a>. <a href="url2">xlink2</a>. </div>')
        self.assertEqual(unicode(bx[1]), '<ul id="links"><li><a href="url1">ylink1</a></li></ul>')
        bx = self.platform.get_blocks('http://example.com/notexists', formatters)
        self.assertEqual(unicode(bx[0]), '<div class="empty"></div><!--x12345--><!--y12345-->')
        self.assertEqual(unicode(bx[1]), '<span id="links"></span>')
        bx = self.platform.get_blocks('http://example.com/path/1', formatters)
        self.assertEqual(unicode(bx[0]), '<div class="links"><a href="url1">xlink1</a>. <a href="url2">xlink2</a>. </div>')
        self.assertEqual(unicode(bx[1]), '<ul id="links"><li><a href="url3">xlink3</a></li><li><a href="url4">xlink4</a></li></ul><!--y12345-->')
        formatters = [
         (
          'inline', [None], dict()),
         (
          'inline', [None], dict(client=1))]
        bx = self.platform.get_blocks('http://example.com/', formatters)
        self.assertEqual(unicode(bx[0]), '<div><a href="url1">ylink1</a></div>')
        self.assertEqual(unicode(bx[1]), '<div><a href="url1">xlink1</a><a href="url2">xlink2</a></div>')
        return


class PlatformConfigTestCase(PlatformTestCase):
    linkexchange_cfg = '\n[client-1]\ntype = sape\nuser = user123456789\ndb_driver.type = mem\nserver-1 = %(server1)s\n\n[client-2]\ntype = sape\nuser = user123456789\ndb_driver.type = mem\nserver-1 = %(server2)s\n'

    def setUpClass(cls):
        cls.server1 = SapeTestServer1()
        cls.server2 = SapeTestServer2()
        cfgfd, cls.cfgfn = tempfile.mkstemp()
        os.close(cfgfd)
        open(cls.cfgfn, 'w').write(cls.linkexchange_cfg % {'server1': cls.server1.url.replace('%', '%%'), 
           'server2': cls.server2.url.replace('%', '%%')})
        vars = {}
        result = file_config(vars, cls.cfgfn)
        assert result == [cls.cfgfn]
        cls.platform = vars['platform']

    setUpClass = classmethod(setUpClass)

    def tearDownClass(cls):
        del cls.platform
        del cls.server1
        del cls.server2
        os.unlink(cls.cfgfn)

    tearDownClass = classmethod(tearDownClass)

    def testLXRefresh(self):
        from linkexchange.commands import lxrefresh
        retcode = os.spawnl(os.P_WAIT, sys.executable, sys.executable, lxrefresh.__file__, '-c', self.cfgfn, '-r', 'http://example.com')
        self.assertEqual(retcode, 0)