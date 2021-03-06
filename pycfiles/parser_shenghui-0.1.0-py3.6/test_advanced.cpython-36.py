# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_advanced.py
# Compiled at: 2017-09-13 01:56:34
# Size of source mod 2**32: 1128 bytes
from parser import Parser
from .context import TEST_DATA_DIR_PATH
import unittest, os

class AdvancedTestSuite(unittest.TestCase):
    __doc__ = 'Advanced test cases.'

    def setUp(self):
        self.file_path = os.path.join(TEST_DATA_DIR_PATH, 'original_sample.txt')
        self.parser = Parser()
        self.parser.scan_document(self.file_path)

    def test_when_x_is_negative_number(self):
        with self.assertRaises(Exception) as (context):
            self.parser.x_largest(-1)
        self.assertTrue('X invalidly negative.' in str(context.exception))

    def test_when_x_is_larger_than_number_of_records(self):
        with self.assertRaises(Exception) as (context):
            self.parser.x_largest(10)
        self.assertTrue('X is larger than number of records.' in str(context.exception))

    def test_when_x_is_not_a_valid_integer(self):
        with self.assertRaises(Exception) as (context):
            self.parser.x_largest('str')
        self.assertTrue('Your x_largest input is not a valid integer.' in str(context.exception))


if __name__ == '__main__':
    unittest.main()