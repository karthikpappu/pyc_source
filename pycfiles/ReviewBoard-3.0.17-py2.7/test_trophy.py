# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_trophy.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.models.Trophy."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from reviewboard.accounts.models import Trophy
from reviewboard.accounts.trophies import TrophyType
from reviewboard.deprecation import RemovedInReviewBoard40Warning
from reviewboard.testing import TestCase

class TrophyTests(TestCase):
    """Unit tests for reviewboard.accounts.models.Trophy."""
    fixtures = [
     b'test_users']

    def test_is_fish_trophy_awarded_for_new_review_request(self):
        """Testing if a fish trophy is awarded for a new review request"""
        user1 = User.objects.get(username=b'doc')
        category = b'fish'
        review_request = self.create_review_request(publish=True, id=3223, submitter=user1)
        trophies = Trophy.objects.get_trophies(review_request)
        self.assertEqual(trophies[0].category, category)
        self.assertTrue(trophies[0].review_request.extra_data[b'calculated_trophies'])

    def test_is_fish_trophy_awarded_for_older_review_request(self):
        """Testing if a fish trophy is awarded for an older review request"""
        user1 = User.objects.get(username=b'doc')
        category = b'fish'
        review_request = self.create_review_request(publish=True, id=1001, submitter=user1)
        del review_request.extra_data[b'calculated_trophies']
        trophies = Trophy.objects.get_trophies(review_request)
        self.assertEqual(trophies[0].category, category)
        self.assertTrue(trophies[0].review_request.extra_data[b'calculated_trophies'])

    def test_is_milestone_trophy_awarded_for_new_review_request(self):
        """Testing if a milestone trophy is awarded for a new review request
        """
        user1 = User.objects.get(username=b'doc')
        category = b'milestone'
        review_request = self.create_review_request(publish=True, id=1000, submitter=user1)
        trophies = Trophy.objects.compute_trophies(review_request)
        self.assertEqual(trophies[0].category, category)
        self.assertTrue(trophies[0].review_request.extra_data[b'calculated_trophies'])

    def test_is_milestone_trophy_awarded_for_older_review_request(self):
        """Testing if a milestone trophy is awarded for an older review
        request
        """
        user1 = User.objects.get(username=b'doc')
        category = b'milestone'
        review_request = self.create_review_request(publish=True, id=10000, submitter=user1)
        del review_request.extra_data[b'calculated_trophies']
        trophies = Trophy.objects.compute_trophies(review_request)
        self.assertEqual(trophies[0].category, category)
        self.assertTrue(trophies[0].review_request.extra_data[b'calculated_trophies'])

    def test_is_no_trophy_awarded(self):
        """Testing if no trophy is awarded"""
        user1 = User.objects.get(username=b'doc')
        review_request = self.create_review_request(publish=True, id=999, submitter=user1)
        trophies = Trophy.objects.compute_trophies(review_request)
        self.assertFalse(trophies)

    def test_get_display_text_deprecated(self):
        """Testing TrophyType.format_display_text for an old-style trophy warns
        that get_display_text it is deprecated
        """

        class OldTrophyType(TrophyType):
            image_width = 1
            image_height = 1
            category = b'old-n-busted'

            def get_display_text(self, trophy):
                return b'A trophy for you.'

        review_request = self.create_review_request()
        trophy = Trophy(category=OldTrophyType.category, review_request=review_request, user=review_request.submitter)
        message = b'TrophyType.get_display_text has been deprecated in favor of TrophyType.format_display_text.'
        with self.assert_warns(RemovedInReviewBoard40Warning, message):
            text = OldTrophyType().format_display_text(trophy, RequestFactory().get(b'/'))
        self.assertEqual(text, b'A trophy for you.')