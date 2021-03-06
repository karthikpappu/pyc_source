# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/tests/test_analysis.py
# Compiled at: 2018-11-26 11:04:16
# Size of source mod 2**32: 5412 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest, numpy as np, tempfile, os, shutil
from neurosynth.analysis import cluster
from neurosynth.analysis import reduce
from neurosynth.analysis import decode
from neurosynth.analysis import meta
from neurosynth.analysis import stats
from neurosynth.analysis import network
from neurosynth.tests.utils import get_test_dataset, get_test_data_path
from numpy.testing import assert_array_almost_equal
from glob import glob
import nibabel as nb

class TestAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Create a new Dataset and add features. """
        self.dataset = get_test_dataset()
        self.real_dataset = get_test_dataset(prefix='test_real')

    def test_meta_analysis(self):
        """ Test full meta-analysis stream. """
        ids = [
         'study1', 'study3']
        ma = meta.MetaAnalysis(self.dataset, ids)
        tempdir = tempfile.mkdtemp()
        ma.save_results((tempdir + os.path.sep), prefix='test')
        files = glob(tempdir + os.path.sep + 'test_*.nii.gz')
        self.assertEquals(len(files), 9)
        shutil.rmtree(tempdir)
        tempdir = tempfile.mkdtemp()
        meta.analyze_features((self.dataset),
          output_dir=tempdir, prefix='meep')
        files = glob(tempdir + os.path.sep + 'meep*.nii.gz')
        self.assertEquals(len(files), 45)
        shutil.rmtree(tempdir)

    def test_decoder(self):
        t = tempfile.mktemp()
        test_data_path = get_test_data_path()
        dec = decode.Decoder((self.real_dataset), features=['pain', 'emotion'])
        img = os.path.join(test_data_path, 'sgacc_mask.nii.gz')
        dec.decode(img, save=t)
        self.assertTrue(os.path.exists(t))
        results = dec.decode(img)
        self.assertEqual(results.shape, (2, 1))
        os.unlink(t)

    def test_coactivation(self):
        """ Test seed-based coactivation. """
        tempdir = tempfile.mkdtemp()
        seed_img = get_test_data_path() + 'sgacc_mask.nii.gz'
        network.coactivation((self.dataset), seed_img, output_dir=tempdir, prefix='test',
          r=20)
        filter = os.path.join(tempdir, 'test*.nii.gz')
        files = glob(filter)
        self.assertEquals(len(files), 9)
        shutil.rmtree(tempdir)

    def test_roi_averaging(self):
        """ Test averaging within region labels in a mask. """
        filename = get_test_data_path() + 'sgacc_mask.nii.gz'
        regions = self.dataset.masker.mask(filename, in_global_mask=True)
        avg_vox = reduce.average_within_regions(self.dataset, regions)
        n_studies = self.dataset.image_table.data.shape[1]
        self.assertEqual(n_studies, avg_vox.shape[1])
        self.assertGreater(avg_vox.sum(), 0.05)

    def test_get_random_voxels(self):
        """ Test random voxel retrieval. """
        n_vox = 100
        rand_vox = reduce.get_random_voxels(self.dataset, n_vox)
        n_studies = self.dataset.image_table.data.shape[1]
        self.assertEqual(rand_vox.shape, (n_vox, n_studies))

    def test_apply_grid_to_image(self):
        data, grid = reduce.apply_grid((self.dataset), scale=6)
        self.assertEquals(data.shape, (1435, 5))
        sums = np.sum(data, 0)
        self.assertGreater(sums[2], sums[3])
        self.assertGreater(sums[4], sums[0])

    def test_two_way_chi_sq(self):
        p = stats.two_way(np.array([[42, 32], [60, 81]])[None, :, :])
        assert_array_almost_equal(p, 0.04753082)

    def test_clustering(self):
        roi_mask = os.path.join(get_test_data_path(), 'sgacc_mask.nii.gz')
        clusters = cluster.magic((self.real_dataset), roi_mask=roi_mask, reduce_reference='pca',
          n_components=5,
          min_studies_per_voxel=1,
          n_clusters=3)
        n_unique = len(np.unique(clusters.get_data()))
        self.assertEqual(n_unique, 4)
        d = tempfile.mkdtemp()
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans
        pca = PCA(20, svd_solver='randomized')
        clust = KMeans(3)
        cluster.magic((self.real_dataset),
          method='studies', roi_mask=roi_mask, features=[
         'emotion', 'pain'],
          feature_threshold=0.0,
          reduce_reference=pca,
          clustering_algorithm=clust,
          distance_metric='jaccard',
          output_dir=d,
          filename='test.nii.gz')
        img = nb.load(os.path.join(d, 'test.nii.gz'))
        self.assertEqual(len(np.unique(img.get_data())), 4)
        clusters = cluster.magic((self.real_dataset), method='features', n_clusters=3)
        n_unique = len(np.unique(clusters.get_data()))
        self.assertEqual(n_unique, 4)
        shutil.rmtree(d)

    def test_fdr(self):
        pvals = np.array([0.005, 0.1, 0.2, 0.5])
        fdr_p = stats.fdr(pvals)
        self.assertEqual(fdr_p, pvals[0])


suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalysis)
if __name__ == '__main__':
    unittest.main()