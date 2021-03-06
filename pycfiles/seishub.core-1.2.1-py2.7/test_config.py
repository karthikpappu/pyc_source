# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\tests\test_config.py
# Compiled at: 2010-12-23 17:42:44
from seishub.core.config import Configuration, Option, ConfigurationError, ConfigParser
import os, tempfile, time, unittest

class TestConfiguration(Configuration):

    def __init__(self, filename):
        Configuration.__init__(self, filename)
        self.site_parser = ConfigParser()


class ConfigurationTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(tempfile.gettempdir(), 'seishub-test.ini')
        self._write([])
        self._orig_registry = Option.registry
        Option.registry = {}

    def tearDown(self):
        Option.registry = self._orig_registry
        os.remove(self.filename)

    def _read(self):
        return TestConfiguration(self.filename)

    def _write(self, lines):
        fileobj = open(self.filename, 'w')
        try:
            fileobj.write(('\n').join(lines + ['']))
        finally:
            fileobj.close()

    def test_default(self):
        config = self._read()
        self.assertEquals('', config.get('a', 'option'))
        self.assertEquals('value', config.get('a', 'option', 'value'))

        class Foo(object):
            option_a = Option('a', 'option', 'value')

        self.assertEquals('value', config.get('a', 'option'))

    def test_default_bool(self):
        config = self._read()
        self.assertEquals(False, config.getbool('a', 'option'))
        self.assertEquals(True, config.getbool('a', 'option', 'yes'))
        self.assertEquals(True, config.getbool('a', 'option', 1))

        class Foo(object):
            option_a = Option('a', 'option', 'true')

        self.assertEquals(True, config.getbool('a', 'option'))

    def test_default_int(self):
        config = self._read()
        self.assertRaises(ConfigurationError, config.getint, 'a', 'option', 'b')
        self.assertEquals(None, config.getint('a', 'option'))
        self.assertEquals(1, config.getint('a', 'option', '1'))
        self.assertEquals(1, config.getint('a', 'option', 1))

        class Foo(object):
            option_a = Option('a', 'option', '2')

        self.assertEquals(2, config.getint('a', 'option'))
        return

    def test_read_and_get(self):
        self._write(['[a]', 'option = x'])
        config = self._read()
        self.assertEquals('x', config.get('a', 'option'))
        self.assertEquals('x', config.get('a', 'option', 'y'))

    def test_read_and_getbool(self):
        self._write(['[a]', 'option = yes'])
        config = self._read()
        self.assertEquals(True, config.getbool('a', 'option'))
        self.assertEquals(True, config.getbool('a', 'option', False))

    def test_read_and_getint(self):
        self._write(['[a]', 'option = 42'])
        config = self._read()
        self.assertEquals(42, config.getint('a', 'option'))
        self.assertEquals(42, config.getint('a', 'option', 25))

    def test_read_and_getlist(self):
        self._write(['[a]', 'option = foo, bar, baz'])
        config = self._read()
        self.assertEquals(['foo', 'bar', 'baz'], config.getlist('a', 'option'))

    def test_read_and_getlist_sep(self):
        self._write(['[a]', 'option = foo | bar | baz'])
        config = self._read()
        self.assertEquals(['foo', 'bar', 'baz'], config.getlist('a', 'option', sep='|'))

    def test_read_and_getlist_keep_empty(self):
        self._write(['[a]', 'option = ,bar,baz'])
        config = self._read()
        self.assertEquals(['bar', 'baz'], config.getlist('a', 'option'))
        self.assertEquals(['', 'bar', 'baz'], config.getlist('a', 'option', keep_empty=True))

    def test_set_and_save(self):
        config = self._read()
        config.set('b', 'option0', 'y')
        config.set('a', 'option0', 'x')
        config.set('a', 'option2', "Voilà l'été")
        config.set('a', 'option1', "Voilà l'été")
        self.assertEquals('x', config.get('a', 'option0'))
        self.assertEquals("Voilà l'été", config.get('a', 'option1'))
        self.assertEquals("Voilà l'été", config.get('a', 'option2'))
        config.save()
        configfile = open(self.filename, 'r')
        self.assertEquals(['# -*- coding: utf-8 -*-\n',
         '\n',
         '[a]\n',
         'option0 = x\n',
         "option1 = Voilà l'été\n",
         "option2 = Voilà l'été\n",
         '\n',
         '[b]\n',
         'option0 = y\n',
         '\n'], configfile.readlines())
        configfile.close()
        config2 = Configuration(self.filename)
        self.assertEquals('x', config2.get('a', 'option0'))
        self.assertEquals("Voilà l'été", config2.get('a', 'option1'))
        self.assertEquals("Voilà l'été", config2.get('a', 'option2'))

    def test_sections(self):
        self._write(['[a]', 'option = x', '[b]', 'option = y'])
        config = self._read()
        self.assertEquals(['a', 'b'], config.sections())
        config.parser.add_section('c')
        self.assertEquals(['a', 'b', 'c'], config.sections())

    def test_options(self):
        self._write(['[a]', 'option = x', '[b]', 'option = y'])
        config = self._read()
        self.assertEquals(('option', 'x'), iter(config.options('a')).next())
        self.assertEquals(('option', 'y'), iter(config.options('b')).next())
        self.assertRaises(StopIteration, iter(config.options('c')).next)

    def test_reparse(self):
        self._write(['[a]', 'option = x'])
        config = self._read()
        self.assertEquals('x', config.get('a', 'option'))
        time.sleep(1)
        self._write(['[a]', 'option = y'])
        config.parse_if_needed()
        self.assertEquals('y', config.get('a', 'option'))


def suite():
    return unittest.makeSuite(ConfigurationTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')