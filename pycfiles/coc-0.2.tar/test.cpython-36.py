# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cob_arcgis_geocoder/test.py
# Compiled at: 2018-12-06 10:13:34
# Size of source mod 2**32: 5479 bytes
import unittest, pandas as pd
from cob_arcgis_geocoder.geocode import CobArcGISGeocoder

class TestInitiatingGeocoderClass(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1, 2],  'address':['89 Orleans Street Boston MA, 02128', '51 Montebello Road Apt 2 Boston, MA 02130']})
        self.address = 'address'
        self.geocoder = CobArcGISGeocoder(self.df, self.address)

    def test_can_correctly_create_geocoder_class(self):
        self.assertIsInstance(self.geocoder, CobArcGISGeocoder)


class TestAbleToFindAddressCandidates(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':['89 Orleans Street Boston MA, 02128']})
        self.address_to_geocode = self.df['address'][0]
        self.geocoder = CobArcGISGeocoder(self.df, self.address_to_geocode)
        self.candidates = self.geocoder._find_address_candidates(self.address_to_geocode)

    def test_parameters_are_as_expected(self):
        self.assertEqual(len(self.candidates['candidates']), 6)


class TestAbleToCorrectlyPickPointAddressCandidate(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':['89 Orleans Street Boston MA, 02128']})
        self.address_to_geocode = self.df['address'][0]
        self.geocoder = CobArcGISGeocoder(self.df, self.address_to_geocode)
        self.candidates = self.geocoder._find_address_candidates(self.address_to_geocode)
        self.picked_candidate = self.geocoder._pick_address_candidate(self.candidates)

    def test_picks_highest_score_candidate(self):
        self.assertEqual(self.picked_candidate['score'], 94.57)

    def test_picks_expected_candidate(self):
        self.assertEqual(self.picked_candidate['attributes.Ref_ID'], 105967)


class TestReturnsNoneWhenNoCandidates(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':["This isn't an address"]})
        self.address_to_geocode = self.df['address'][0]
        self.geocoder = CobArcGISGeocoder(self.df, self.address_to_geocode)
        self.candidates = self.geocoder._find_address_candidates(self.address_to_geocode)
        self.picked_candidate = self.geocoder._pick_address_candidate(self.candidates)

    def test_returns_none_when_no_candidates(self):
        self.assertEqual(self.picked_candidate, None)


class TestReverseGeocodeFindsPoint(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':['890 Commonwealth Avenue']})
        self.address_to_geocode = self.df['address'][0]
        self.geocoder = CobArcGISGeocoder(self.df, self.address_to_geocode)
        self.candidates = self.geocoder._find_address_candidates(self.address_to_geocode)
        self.picked_candidate = self.geocoder._pick_address_candidate(self.candidates)

    def test_returns_point_address(self):
        self.assertEqual(self.picked_candidate['attributes.Ref_ID'], 41280)

    def test_returns_correct_flag_point_addresses(self):
        self.assertEqual(self.picked_candidate['flag'], 'Able to reverse-geocode to a point address.')


class TestAbleToHandleNullAddresses(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1, 2],  'address':['89 Orleans Street Boston MA, 02128', None]})
        self.address = 'address'
        self.geocoder = CobArcGISGeocoder(self.df, self.address)
        self.geocode_df_with_Nulls = self.geocoder.geocode_df(df=(self.df), address_field=(self.address))

    def test_handle_null_address(self):
        self.assertEqual(self.geocode_df_with_Nulls.loc[:, 'flag'][1], 'No address provided. Unable to geocode.')


class TestAbleToFindPointAddress(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':['1 City Hall Plz, Boston, 02108']})
        self.address = 'address'
        self.geocoder = CobArcGISGeocoder(self.df, self.address)
        self.geocode_df = self.geocoder.geocode_df(df=(self.df), address_field=(self.address))

    def test_returns_expected_address(self):
        print(self.geocode_df['SAM_ID'])
        self.assertEqual(self.geocode_df['SAM_ID'][0], 32856)


class TestAbleToReverseGeocodeToPointAddress(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':['890 Commonwealth Avenue']})
        self.address = 'address'
        self.geocoder = CobArcGISGeocoder(self.df, self.address)
        self.geocode_df = self.geocoder.geocode_df(df=(self.df), address_field=(self.address))

    def test_reverse_geocode_to_point_address(self):
        self.assertEqual(self.geocode_df['SAM_ID'][0], 41280)


class TestHandlesNotFindingAddressAsExpected(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id':[1],  'address':["This isn't an address."]})
        self.address = 'address'
        self.geocoder = CobArcGISGeocoder(self.df, self.address)
        self.geocode_df = self.geocoder.geocode_df(df=(self.df), address_field=(self.address))

    def test_reverse_geocode_to_point_address(self):
        self.assertEqual(self.geocode_df['flag'][0], 'Unable to geocode to any address.')