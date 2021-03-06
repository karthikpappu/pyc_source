# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/trim_learner_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 931 bytes
from adlib.tests.learners.dp_learner_test import TestDataPoisoningLearner
from adlib.utils.common import report
from data_reader.dataset import EmailDataset
import sys

def test_trim_learner():
    if len(sys.argv) == 2 and sys.argv[1] in ('label-flipping', 'k-insertion', 'data-modification',
                                              'dummy'):
        attacker_name = sys.argv[1]
    else:
        attacker_name = 'dummy'
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False,
      raw=True)
    tester = TestDataPoisoningLearner('trim', attacker_name, dataset)
    result = tester.test()
    report(result)


if __name__ == '__main__':
    test_trim_learner()