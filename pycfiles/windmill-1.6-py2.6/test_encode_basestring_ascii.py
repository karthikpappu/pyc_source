# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_encode_basestring_ascii.py
# Compiled at: 2011-01-13 01:48:00
from unittest import TestCase
import simplejson.encoder
CASES = [
 ('/\\"쫾몾ꮘﳞ볚\uef4a\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?', '"/\\\\\\"\\ucafe\\ubabe\\uab98\\ufcde\\ubcda\\uef4a\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"'),
 ('ģ䕧覫췯ꯍ\uef4a', '"\\u0123\\u4567\\u89ab\\ucdef\\uabcd\\uef4a"'),
 ('controls', '"controls"'),
 ('\x08\x0c\n\r\t', '"\\b\\f\\n\\r\\t"'),
 ('{"object with 1 member":["array with 1 element"]}', '"{\\"object with 1 member\\":[\\"array with 1 element\\"]}"'),
 (' s p a c e d ', '" s p a c e d "'),
 ('𝄠', '"\\ud834\\udd20"'),
 ('αΩ', '"\\u03b1\\u03a9"'),
 ('αΩ', '"\\u03b1\\u03a9"'),
 ('αΩ', '"\\u03b1\\u03a9"'),
 ('αΩ', '"\\u03b1\\u03a9"'),
 ('αΩ', '"\\u03b1\\u03a9"'),
 ('αΩ', '"\\u03b1\\u03a9"'),
 ("`1~!@#$%^&*()_+-={':[,]}|;.</>?", '"`1~!@#$%^&*()_+-={\':[,]}|;.</>?"'),
 ('\x08\x0c\n\r\t', '"\\b\\f\\n\\r\\t"'),
 ('ģ䕧覫췯ꯍ\uef4a', '"\\u0123\\u4567\\u89ab\\ucdef\\uabcd\\uef4a"')]

class TestEncodeBaseStringAscii(TestCase):

    def test_py_encode_basestring_ascii(self):
        self._test_encode_basestring_ascii(simplejson.encoder.py_encode_basestring_ascii)

    def test_c_encode_basestring_ascii(self):
        if not simplejson.encoder.c_encode_basestring_ascii:
            return
        self._test_encode_basestring_ascii(simplejson.encoder.c_encode_basestring_ascii)

    def _test_encode_basestring_ascii(self, encode_basestring_ascii):
        fname = encode_basestring_ascii.__name__
        for (input_string, expect) in CASES:
            result = encode_basestring_ascii(input_string)
            self.assertEquals(result, expect, '%r != %r for %s(%r)' % (result, expect, fname, input_string))