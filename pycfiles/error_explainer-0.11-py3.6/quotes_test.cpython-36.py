# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/quotes_test.py
# Compiled at: 2020-04-06 02:33:21
# Size of source mod 2**32: 3561 bytes
import unittest
from error_explainer.messages import get_formatted_message
from test.test_utils import run_test_scenario

class QuotesTest(unittest.TestCase):

    def test_simple_missing_single_after(self):
        path = 'quotes_samples/mixed_missing_single_after_error.py'
        expected_message = get_formatted_message('invalid_quotes',
          line_start=1, quote="'", pos=10)
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_double_before(self):
        path = 'quotes_samples/missing_double_before_error.py'
        expected_message = get_formatted_message('invalid_quotes',
          line_start=1, quote='"', pos=5)
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_double_after(self):
        path = 'quotes_samples/missing_double_after_error.py'
        expected_message = get_formatted_message('invalid_quotes',
          line_start=1, quote='"', pos=3)
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_single_before(self):
        path = 'quotes_samples/missing_single_before_error.py'
        expected_message = get_formatted_message('invalid_quotes',
          line_start=1, quote="'", pos=5)
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_single_after(self):
        path = 'quotes_samples/missing_single_after_error.py'
        expected_message = get_formatted_message('invalid_quotes',
          line_start=1, quote="'", pos=3)
        run_test_scenario(self, path, 1, expected_message)

    def test_miss_matched_quotes(self):
        path = 'quotes_samples/miss_matched_quotes_error.py'
        expected_message = get_formatted_message('miss_matched_quotes',
          line_start=1, line_end=3)
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_quotes_docstring_after(self):
        path = 'quotes_samples/missing_quotes_after_docstring_error.py'
        expected_message = get_formatted_message('invalid_quotes_triple',
          line_start=1, quote='"""', pos=0)
        run_test_scenario(self, path, 1, expected_message)

    def test_missing_quotes_docstring_after(self):
        path = 'quotes_samples/missing_quotes_before_docstring_error.py'
        expected_message = get_formatted_message('invalid_quotes_triple',
          line_start=3, quote='"""', pos=0)
        run_test_scenario(self, path, 1, expected_message)

    def test_some_missing_quotes_docstring_after(self):
        path = 'quotes_samples/missing_some_quotes_after_docstring_error.py'
        expected_message = get_formatted_message('missing_docstring_quotes',
          line_start=1)
        run_test_scenario(self, path, 1, expected_message)

    def test_some_missing_quotes_no_colon(self):
        path = 'quotes_samples/missing_quotes_no_colon_error.py'
        expected_message = get_formatted_message('invalid_quotes',
          line_start=1, quote='"', pos=7)
        run_test_scenario(self, path, 1, expected_message)

    def test_some_missing_quote_docstring_before(self):
        pass


if __name__ == '__main__':
    unittest.main()