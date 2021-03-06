# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_title_filter.py
# Compiled at: 2018-08-07 00:31:28
# Size of source mod 2**32: 598 bytes
__doc__ = 'Title filter testcases'
from unittest import TestCase
from purewords.filters import title_filter

class TestTitleFilterClass(TestCase):

    def setUp(self):
        self.filter = title_filter

    def test_title_filter(self):
        sentence = "I'm Mr. Qoo. She's Mrs. M. " + "Hello ma'am. I'd and I'll " + 'like to show you something'
        answer = "I'm Mr Qoo. She's Mrs M. Hello madam. " + "I'd and I'll like to show you something"
        self.assertEqual(answer, self.filter(sentence))