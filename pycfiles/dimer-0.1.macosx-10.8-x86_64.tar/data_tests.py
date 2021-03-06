# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/data_tests.py
# Compiled at: 2013-07-25 01:03:26
import unittest, tempfile
from data import Dataset, AnchorDataset, TrainAnchorDataset
import numpy as np, pandas as pd
rng = np.random.RandomState(10)

class TestDataset(unittest.TestCase):

    def setUp(self):
        self.X = rng.rand(100, 800)

    def test_normalize_feats(self):
        """0-mean and 1-variance features"""

        def check_norm(x, m, v):
            self.assertEqual(m.shape, v.shape)
            self.assertEqual(m.shape, tuple(x.shape[1:]))
            print x.reshape(x.shape[0], -1)
            print m.reshape((-1, ))
            print v.reshape((-1, ))
            for f in range(x.shape[1]):
                self.assertAlmostEqual(x[:, f].mean(), 0)
                if v[f] != 0:
                    self.assertAlmostEqual(x[:, f].std(), 1)
                else:
                    self.assertAlmostEqual(x[:, f].std(), 0)

        X = self.X
        check_norm(*Dataset.normalize_features(X))
        X[:, 0] = 0
        print X[:, 0]
        check_norm(*Dataset.normalize_features(X))

    def test_fit_feats(self):
        """features in [0,1]"""
        print self.X
        fx = Dataset.fit_features(self.X)
        self.assertAlmostEqual(fx.min(), -1)
        self.assertAlmostEqual(fx.max(), 1)
        self.assertEqual(fx.shape, self.X.shape)

    def test_labeled(self):
        x = rng.rand(3, 4)
        self.assertTrue(Dataset(x, rng.rand(3), rng.rand(3)).is_labeled)
        self.assertFalse(Dataset(x, rng.rand(3), None).is_labeled)
        return


class TestAnchorDataset(unittest.TestCase):

    def setUp(self):
        n, tr, w = rng.randint(10, 100), rng.randint(2, 5), rng.randint(200, 500)
        self.bs = rng.randint(2, n / 4)
        self.X = rng.rand(n, tr, w)
        self.Y = rng.rand(n)
        self.T = np.array(map(lambda v: (v > 0 and [1] or [0])[0], self.Y), np.int)
        self.T[0] = 0
        self.T[1] = 1
        self.gnames = map(lambda i: 'gene%d' % i, range(self.X.shape[0]))
        self.tracks = map(lambda i: 'track%d' % i, range(self.X.shape[1]))
        self.width = map(lambda i: 'pos%d' % i, range(self.X.shape[2]))
        self.labels = ('R', 'I')
        self.pX = pd.Panel(self.X, items=self.gnames, major_axis=self.tracks, minor_axis=self.width)
        self.dfT = pd.DataFrame({'label_code': self.T, 'label_name': map(lambda v: self.labels[v], self.T)})
        self.sY = pd.Series(self.Y, index=self.gnames)
        self.labds = AnchorDataset(self.pX, self.sY, self.dfT)
        self.ds = AnchorDataset(self.pX, self.sY, None)
        return

    def test_annotations(self):
        self.assertEqual(set(self.labds.label_names), set(self.labels))
        self.assertEqual(set(self.labds.track_names), set(self.tracks))
        self.assertEqual(self.ds.label_names, None)
        self.assertEqual(self.ds.track_names, self.tracks)
        return

    def test_share(self):
        """dataset on theano shared vars"""
        self.assertTrue(np.all(self.ds.shX.get_value() == self.ds.X))

    def test_batch_allocation(self):
        ds = TrainAnchorDataset(self.pX, self.sY, self.dfT, self.bs)
        self.assertEqual(ds.train_batches + ds.valid_batches, range(ds.n_batches))
        ds = TrainAnchorDataset(self.pX, self.sY, self.dfT, self.bs, rng=rng)
        self.assertNotEqual(ds.train_batches + ds.valid_batches, range(ds.n_batches))
        self.assertEqual(set(ds.train_batches + ds.valid_batches), set(range(ds.n_batches)))

    @unittest.SkipTest
    def test_batch_iter(self):
        ds = AnchorDataset(self.pX, None, None, self.bs)
        self.assertEqual(5 * list(ds.iter_train(1)), 5 * ds.train_batches)
        self.assertEqual(7 * list(ds.iter_valid(1)), 7 * ds.valid_batches)
        self.assertEqual(list(ds.iter_train(5)), 5 * ds.train_batches)
        self.assertEqual(list(ds.iter_valid(7)), 7 * ds.valid_batches)
        return

    def test_io(self):
        from archive import __SPEC_SEP__, __HDF_SUFFIX__
        with tempfile.NamedTemporaryFile(suffix='.' + __HDF_SUFFIX__) as (fd):
            path = __SPEC_SEP__.join((fd.name, 'empty'))
            lds = self.labds
            lds.dump(path)
            ods = AnchorDataset._from_archive(path, True)
            self.assertEqual(ods.label_names, lds.label_names)
            self.assertEqual(ods.track_names, lds.track_names)
            self.assertAlmostEqual(np.max(np.abs(ods.X - lds.X)), 0)
            self.assertTrue(np.all(ods.sY == lds.sY))
            self.assertTrue(np.all(ods.dfT == lds.dfT))
            ods = AnchorDataset._from_archive(path, False)
            ldsX, m, sd = lds.normalize_features(lds.X.reshape(self.X.shape[0], -1))
            self.assertAlmostEqual(np.max(np.abs(ods.X - ldsX.reshape(ods.X.shape))), 0)
        with tempfile.NamedTemporaryFile(suffix='.' + __HDF_SUFFIX__) as (fd):
            path = __SPEC_SEP__.join((fd.name, 'empty'))
            lds = TrainAnchorDataset(self.pX, self.sY, self.dfT, self.bs)
            lds.dump(path)
            ods = TrainAnchorDataset._from_archive(path, False, self.bs)
            self.assertEqual(ods.train_batches, lds.train_batches)
            self.assertEqual(ods.valid_batches, lds.valid_batches)