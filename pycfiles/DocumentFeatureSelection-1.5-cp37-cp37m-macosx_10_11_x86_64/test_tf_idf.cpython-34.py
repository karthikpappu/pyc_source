# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/tests/test_tf_idf.py
# Compiled at: 2016-11-29 04:36:51
# Size of source mod 2**32: 2846 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from scipy.sparse import csr_matrix
from DocumentFeatureSelection.common import data_converter
from DocumentFeatureSelection.common.data_converter import DataCsrMatrix
from DocumentFeatureSelection.tf_idf import tf_idf
import logging, unittest, numpy
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
__author__ = 'kensuke-mi'

class TestTfIdf(unittest.TestCase):

    def setUp(self):
        input_dict = {'label_a': [
                     [
                      'I', 'aa', 'aa', 'aa', 'aa', 'aa'],
                     [
                      'bb', 'aa', 'aa', 'aa', 'aa', 'aa'],
                     [
                      'I', 'aa', 'hero', 'some', 'ok', 'aa']], 
         'label_b': [
                     [
                      'bb', 'bb', 'bb'],
                     [
                      'bb', 'bb', 'bb'],
                     [
                      'hero', 'ok', 'bb'],
                     [
                      'hero', 'cc', 'bb']], 
         'label_c': [
                     [
                      'cc', 'cc', 'cc'],
                     [
                      'cc', 'cc', 'bb'],
                     [
                      'xx', 'xx', 'cc'],
                     [
                      'aa', 'xx', 'cc']]}
        tf_matrix = numpy.array([
         [
          2, 12, 1, 0, 1, 1, 1, 0],
         [
          0, 0, 8, 1, 2, 1, 0, 0],
         [
          0, 1, 1, 7, 0, 0, 0, 3]])
        data_csr_matrix = data_converter.DataConverter().labeledMultiDocs2DocFreqMatrix(labeled_documents=input_dict, ngram=1, n_jobs=-1)
        assert isinstance(data_csr_matrix, DataCsrMatrix)
        self.label2id_dict = data_csr_matrix.label2id_dict
        self.csr_matrix_ = data_csr_matrix.csr_matrix_
        self.n_docs_distribution = data_csr_matrix.n_docs_distribution
        self.vocabulary = data_csr_matrix.vocabulary
        numpy.array_equal(data_csr_matrix.csr_matrix_.toarray(), tf_matrix)

    def test_normal_fit_transform(self):
        tf_idf_weighted_matrix = tf_idf.TFIDF().fit_transform(X=self.csr_matrix_)
        assert isinstance(tf_idf_weighted_matrix, csr_matrix)

    def test_output_result_pmi(self):
        import numpy
        tf_idf_weighted_matrix = tf_idf.TFIDF().fit_transform(X=self.csr_matrix_)
        assert isinstance(tf_idf_weighted_matrix, csr_matrix)
        tf_idf_scored_dict = data_converter.ScoreMatrix2ScoreDictionary(scored_matrix=tf_idf_weighted_matrix, label2id_dict=self.label2id_dict, feature2id_dict=self.vocabulary, outformat='items', n_jobs=-1)
        assert isinstance(tf_idf_scored_dict, list)
        import pprint
        pprint.pprint(tf_idf_scored_dict)


if __name__ == '__main__':
    unittest.main()