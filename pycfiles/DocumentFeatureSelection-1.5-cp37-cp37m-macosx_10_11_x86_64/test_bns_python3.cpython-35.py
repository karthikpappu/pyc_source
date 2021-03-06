# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/tests/test_bns_python3.py
# Compiled at: 2017-11-06 02:37:10
# Size of source mod 2**32: 4355 bytes
import unittest
from DocumentFeatureSelection.common import data_converter
from DocumentFeatureSelection.common.data_converter import DataCsrMatrix
from DocumentFeatureSelection.bns import bns_python3
from DocumentFeatureSelection.models import ScoredResultObject
from scipy.sparse import csr_matrix

class TestBnsPython3(unittest.TestCase):

    def setUp(self):
        self.correct_input = {'label_a': [
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
                      'hero', 'cc', 'bb']]}

    def test_fit_transform(self):
        data_csr_matrix = data_converter.DataConverter().labeledMultiDocs2DocFreqMatrix(labeled_documents=self.correct_input, n_jobs=5)
        assert isinstance(data_csr_matrix, DataCsrMatrix)
        label2id_dict = data_csr_matrix.label2id_dict
        csr_matrix_ = data_csr_matrix.csr_matrix_
        n_docs_distribution = data_csr_matrix.n_docs_distribution
        vocabulary = data_csr_matrix.vocabulary
        bns_score_csr_matrix = bns_python3.BNS().fit_transform(X=csr_matrix_, y=None, unit_distribution=n_docs_distribution, verbose=True)
        assert isinstance(bns_score_csr_matrix, csr_matrix)
        bns_scores_dict = ScoredResultObject(scored_matrix=bns_score_csr_matrix, label2id_dict=label2id_dict, feature2id_dict=vocabulary).ScoreMatrix2ScoreDictionary()
        assert isinstance(bns_scores_dict, list)
        import pprint
        pprint.pprint(bns_scores_dict)

    def test_check_input_error(self):
        incorrect_input_dict = {'label_a': [
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
                      'hero', 'cc', 'bb'],
                     [
                      'cc', 'cc', 'cc'],
                     [
                      'cc', 'cc', 'bb'],
                     [
                      'xx', 'xx', 'cc'],
                     [
                      'aa', 'xx', 'cc']], 
         
         'label_c': [
                     [
                      'aa', 'xx', 'cc']]}
        data_csr_matrix = data_converter.DataConverter().labeledMultiDocs2DocFreqMatrix(labeled_documents=incorrect_input_dict, n_jobs=5)
        assert isinstance(data_csr_matrix, DataCsrMatrix)
        csr_matrix_ = data_csr_matrix.csr_matrix_
        n_docs_distribution = data_csr_matrix.n_docs_distribution
        try:
            bns_python3.BNS().fit_transform(X=csr_matrix_, y=None, unit_distribution=n_docs_distribution)
        except:
            pass

    def test_bns_cython(self):
        incorrect_input_dict = {'label_a': [
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
                      'hero', 'cc', 'bb'],
                     [
                      'cc', 'cc', 'cc'],
                     [
                      'cc', 'cc', 'bb'],
                     [
                      'xx', 'xx', 'cc'],
                     [
                      'aa', 'xx', 'cc']]}
        data_csr_matrix = data_converter.DataConverter().labeledMultiDocs2DocFreqMatrix(labeled_documents=incorrect_input_dict, n_jobs=5)
        assert isinstance(data_csr_matrix, DataCsrMatrix)
        csr_matrix_ = data_csr_matrix.csr_matrix_
        n_docs_distribution = data_csr_matrix.n_docs_distribution
        result_bns = bns_python3.BNS().fit_transform(X=csr_matrix_, y=None, unit_distribution=n_docs_distribution, use_cython=True)
        print(result_bns)


if __name__ == '__main__':
    unittest.main()