# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/tests/test_PMI_python3.py
# Compiled at: 2017-11-06 02:37:10
# Size of source mod 2**32: 2782 bytes
import unittest
from DocumentFeatureSelection.common import data_converter
from DocumentFeatureSelection.common.data_converter import DataCsrMatrix
from DocumentFeatureSelection.models import ScoredResultObject
from DocumentFeatureSelection.pmi import PMI_python3
from scipy.sparse import csr_matrix

class TestPmiPython3(unittest.TestCase):

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
        data_csr_matrix = data_converter.DataConverter().labeledMultiDocs2DocFreqMatrix(labeled_documents=input_dict, n_jobs=5)
        assert isinstance(data_csr_matrix, DataCsrMatrix)
        self.label2id_dict = data_csr_matrix.label2id_dict
        self.csr_matrix_ = data_csr_matrix.csr_matrix_
        self.n_docs_distribution = data_csr_matrix.n_docs_distribution
        self.vocabulary = data_csr_matrix.vocabulary

    def test_normal_fit_transform(self):
        pmi_object = PMI_python3.PMI()
        scored_matrix = pmi_object.fit_transform(X=self.csr_matrix_, n_jobs=1, n_docs_distribution=self.n_docs_distribution)
        assert isinstance(scored_matrix, csr_matrix)

    def test_multi_process_fit_transform(self):
        pmi_object = PMI_python3.PMI()
        scored_matrix = pmi_object.fit_transform(X=self.csr_matrix_, n_jobs=5, n_docs_distribution=self.n_docs_distribution, verbose=True)
        assert isinstance(scored_matrix, csr_matrix)

    def test_output_result_pmi(self):
        pmi_object = PMI_python3.PMI()
        scored_matrix = pmi_object.fit_transform(X=self.csr_matrix_, n_jobs=5, n_docs_distribution=self.n_docs_distribution)
        assert isinstance(scored_matrix, csr_matrix)
        pmi_scored_dict = ScoredResultObject(scored_matrix=scored_matrix, label2id_dict=self.label2id_dict, feature2id_dict=self.vocabulary).ScoreMatrix2ScoreDictionary(outformat='items')
        assert isinstance(pmi_scored_dict, list)
        import pprint
        pprint.pprint(pmi_scored_dict)


if __name__ == '__main__':
    unittest.main()