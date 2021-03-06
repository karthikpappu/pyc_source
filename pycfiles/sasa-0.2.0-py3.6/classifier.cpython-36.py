# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sasa/classifier.py
# Compiled at: 2019-04-09 16:41:36
# Size of source mod 2**32: 2287 bytes
"""this class implements the classifier, currently wrapping either
nltk.classify.naivebayes.NaiveBayesClassifier or
nltk.classify.MaxEntClassifier together with feature extraction"""
__author__ = 'Abe Kazemzadeh, Dogan Can, Hao Wang'
__copyright__ = 'Copyright 2013, University of Southern California'
__credits__ = []
__license__ = 'http://www.apache.org/licenses/LICENSE-2.0'
__version__ = '1.0'
__maintainer__ = 'Last modified by Abe Kazemzadeh'
__email__ = "See the authors' website"
import pickle, os
from collections import defaultdict
import nltk
from sasa.normalizer import N1
from sasa.happyfuntokenizing import Tokenizer

class Classifier(nltk.classify.api.ClassifierI):
    __doc__ = ' implements nltk classifier api '
    normalizer = N1()
    tokenizer = Tokenizer()

    def __init__(self, modelfile='model.unigram.nb.bool.politics.unbiased'):
        """ load model """
        modelpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models', modelfile)
        f = open(modelpath, 'rb')
        self.model = pickle.load(f)
        f.close()

    def classify(self, features):
        return self.model.classify(features)

    def prob_classify(self, features):
        return self.model.prob_classify(features)

    def labels(self):
        return self.model.labels()

    def valence(self, features):
        hyp = self.model.classify(features)
        posterior = self.model.prob_classify(features)
        if hyp == 'negative':
            valence = -posterior.prob('negative')
        else:
            if hyp == 'positive':
                valence = posterior.prob('positive')
            else:
                valence = 0
        return valence

    def classifyFromText(self, text):

        def features(text, n=1):
            feats = defaultdict(bool)
            words = ['<s>'] + self.normalizer.normalize(self.tokenizer.tokenize(text)) + ['</s>']
            for i in range(len(words)):
                for j in range(i + 1, i + n + 1):
                    feat = ' '.join(words[i:j])
                    feats[feat] = True

            return feats

        features = features(text)
        label = self.model.classify(features)
        valence = self.valence(features)
        post = self.prob_classify(features)
        return (label, valence, post)