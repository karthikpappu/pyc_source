# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_extractors.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 5852 bytes
"""Tests the extractor modules in KomiDL"""
import os, sys, unittest
from unittest.mock import patch
from difflib import SequenceMatcher
sys.path.append(os.path.abspath('..'))
from komidl.extractors import get_extractors

class ExtractorTest(unittest.TestCase):
    __doc__ = 'Test the extractor modules in KomiDL'

    def setUp(self):
        self.extractors = get_extractors()

    def _compare_size(self, test, extractor, soup):
        """Compare the expected size from the test dictionary to the actual
        size returned from the extractor implementation.

        If the test set 'series' to True, then the assertion is more lenient,
        wherein the actual size may also be greater than the expected.
        """
        title = test['tags']['Title']
        expected = test.get('size', None)
        if expected is not None:
            actual = extractor.get_size(test['url'], soup, None)
            is_series = test.get('series', None)
            with self.subTest(msg=f"{extractor.name}.get_size({title})", expected=expected,
              actual=actual):
                if is_series:
                    self.assertTrue(expected <= actual)
                else:
                    self.assertEqual(expected, actual)

    def _compare_tags(self, test, extractor, soup):
        """Compare the expected tags from the test dictionary to the actual
        tags returned from the extractor implementation.

        If there exist key-value pairs in the actual implementation not found
        in the expected dictionary for the test, the test will still pass.

        Expected values need only be a subset of actual values.
        """
        title = test['tags']['Title']
        expected_tags = test.get('tags', None)
        if expected_tags is not None:
            actual_tags = extractor.get_tags(test['url'], soup, None)
            for key, value in expected_tags.items():
                with self.subTest(msg=f"{extractor.name} {title} {key}"):
                    if isinstance(actual_tags[key], list):
                        actual = actual_tags[key]
                    else:
                        actual = [
                         actual_tags[key]]
                    if isinstance(value, list):
                        expected = value
                    else:
                        expected = [
                         value]
                    expected_set = set((word.lower() for word in expected))
                    actual_set = set((word.lower() for word in actual))
                    self.assertTrue(expected_set.issubset(actual_set))

    def _compare_urls(self, test, extractor, soup):
        """Compare the expected URLs from the test dictionary to the actual
        URLs returned from the extractor implementation.

        This test does not compare the filenames.

        If there exist image URLs in the actual implementation not found in the
        expected values for the test, the test will still pass.
        """

        class MockArgs:

            def __init__(self, thread_size):
                self.thread_size = thread_size

        mock_args = MockArgs(3)
        title = test['tags']['Title']
        expected_imgs = test.get('img_urls', None)
        if expected_imgs is not None:
            actual_imgs = extractor.get_gallery_urls(test['url'], soup, mock_args)
            for expected, (_, actual) in zip(expected_imgs, actual_imgs):
                if test.get('diff_ratio', None) is None:
                    with self.subTest(msg=f"{extractor.name}.get_gallery_urls({title})", expected=expected,
                      actual=actual):
                        if test.get('diff_ratio', None) is None:
                            self.assertEqual(expected, actual)
                        else:
                            seq = SequenceMatcher(a=expected, b=actual)
                            actual_ratio = seq.ratio()
                            expected_ratio = test['diff_ratio']
                            self.assertTrue(expected_ratio >= actual_ratio)

    def test_extractors(self):
        """Test public methods of all extractors"""
        self.maxDiff = None
        for extractor in self.extractors:
            tests = extractor.get_tests()
            if not tests:
                continue
            for test in tests:
                url = test.get('url', None)
                self.assertTrue(url is not None)
                soup = extractor._get_soup(url)
                with self.subTest(msg=f"{extractor.name}EX testing {url}"):
                    self._compare_size(test, extractor, soup)
                    self._compare_tags(test, extractor, soup)
                    self._compare_urls(test, extractor, soup)
                extractor.reset()

            extractor._session.close()

    def test_is_gallery(self):
        """Test the is_gallery method"""
        for extractor in self.extractors:
            tests = extractor.get_tests()
            if not tests:
                continue
            for test in tests:
                url = test.get('url', None)
                self.assertTrue(extractor.is_gallery(url))