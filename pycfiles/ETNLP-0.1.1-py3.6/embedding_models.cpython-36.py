# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/embeddings/embedding_models.py
# Compiled at: 2019-03-30 11:11:39
# Size of source mod 2**32: 11661 bytes
from gensim.models import KeyedVectors as Word2Vec
import numpy as np
from embeddings import embedding_utils
from utils import file_utils
import os, re, logging
DEBUG = False

class Model_Constants(object):
    word2vec = 'word2vec'
    char2vec = 'char2vec'
    private_word2vec = 'private_word2vec'
    elmo = 'elmo'


class Embedding_Model(object):

    def __init__(self, name, vector_dim):
        self.name = name
        self.model = None
        self.char_model = None
        self.vocabs_list = None
        self.vector_dim = vector_dim
        self.unknown_word = 'replace_by_character_embedding'

    def load_model(self, model_path):
        if self.name == Model_Constants.word2vec or self.name == Model_Constants.elmo:
            if model_path.endswith('.bin'):
                self.model = Word2Vec.load_word2vec_format(model_path, binary=True)
            else:
                self.model = Word2Vec.load_word2vec_format(model_path, binary=False)
        else:
            if self.name == Model_Constants.char2vec:
                self.model = dict()
                print('Loading model_path = ', model_path)
                file = open(model_path, 'r')
                for line in file:
                    elements = line.split()
                    if len(elements) > 100:
                        self.model[elements[0]] = np.array([float(i) for i in elements[1:]]).tolist()

                return self.model
            if self.name == Model_Constants.private_word2vec:
                self.model, _, self.vocabs_list = embedding_utils.reload_embeddings(model_path)
            else:
                raise Exception('Unknown embedding models!')

    def is_punct(self, word):
        arr_list = ['!',
         '"',
         '%',
         '&',
         "'",
         "''",
         '(',
         '(.',
         ')',
         '*',
         '+',
         ',',
         '-',
         '---',
         '.',
         '..',
         '...',
         '....',
         '/']
        if word in arr_list:
            return True
        else:
            return False

    def is_number(self, word):
        regex = '^[0-9]+'
        matches = re.finditer(regex, word, re.MULTILINE)
        matchNum = 0
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1

        if matchNum > 0:
            return True
        else:
            return False

    def set_char_model(self, char_model):
        self.char_model = char_model

    def load_vocabs_list(self, vocab_file_path):
        """
        Load vocabs list for private w2v model. Has to be pickle file.
        :param vocab_file_path:
        :return:
        """
        if vocab_file_path:
            self.vocabs_list = file_utils.load_obj(vocab_file_path)

    def get_char_vector(self, char_model, word):
        """
        char_model here is an instance of embedding_model
        :param char_model: an instance of embedding_model
        :param word:
        :return:
        """
        if char_model is None:
            raise Exception('Char_model is None! Cannot use character-embedding.')
        else:
            out_char_2_vec = []
            char_vecs = []
            chars = list(word)
            vecs = []
            for c in chars:
                if c in char_model.model:
                    emb_vector = char_model.model[c]
                    vecs.append(emb_vector)
                    if DEBUG:
                        input('>>>>>>')
                        print('Char_emb_vector=', emb_vector)

            if len(vecs) > 0:
                out_char_2_vec = np.mean(vecs, axis=0)
            if DEBUG:
                print('>>> Output of char2vec: %s' % out_char_2_vec)
                input('>>>> outc2v ...')
        return out_char_2_vec

    def is_unknown_word(self, word):
        """Check whether or not a word is unknown"""
        is_unknown_word = False
        if self.vocabs_list is not None:
            if word not in self.vocabs_list:
                is_unknown_word = True
        else:
            if word not in self.model:
                is_unknown_word = True
        return is_unknown_word

    def get_word_vector(self, word):
        """
        Handle unknown word: In case of our private word2vec, we have a vocabs_list to check. With regular models,
        we can check inside the model. Note that by default, we use char-model to handle unknown words.
        :param word:
        :param char_model:
        :return:
        """
        rtn_vector = []
        is_unknown_word = self.is_unknown_word(word)
        if is_unknown_word:
            word = word.lower()
            is_unknown_word = self.is_unknown_word(word)
        if is_unknown_word:
            if self.char_model:
                rtn_vector = self.get_vector_of_unknown(word)
        if self.name == Model_Constants.word2vec:
            rtn_vector = self.model[word]
            if len(rtn_vector) > self.vector_dim:
                print('Warning: auto trim to %s/%s dimensions' % (self.vector_dim, len(rtn_vector)))
                rtn_vector = self.model[word][:self.vector_dim]
        else:
            if self.name == Model_Constants.elmo:
                rtn_vector = self.model[word]
                if self.vector_dim == len(rtn_vector) / 2:
                    vector1 = rtn_vector[:self.vector_dim]
                    vector2 = rtn_vector[self.vector_dim:]
                    print('Notice: auto average to  b[i] = (a[i] + a[i + %s])/2 /%s dimensions' % (self.vector_dim,
                     len(rtn_vector)))
                    rtn_vector = np.mean([vector1, vector2], 0)
                else:
                    if len(rtn_vector) > self.vector_dim:
                        print('Warning: auto trim to %s/%s dimensions' % (self.vector_dim, len(rtn_vector)))
                        rtn_vector = self.model[word][:self.vector_dim]
            else:
                if self.name == Model_Constants.char2vec:
                    rtn_vector = self.get_char_vector(self, word)
                else:
                    if self.name == Model_Constants.private_word2vec:
                        if word not in self.vocabs_list:
                            word = 'UNK'
                        word_idx = self.vocabs_list.index(word)
                        emb_vector = self.model[word_idx]
                        rtn_vector = emb_vector
            if DEBUG:
                print('>>> DEBUG: len(rtn_vector) = %s' % len(rtn_vector))
                input('>>> before returning vector ...')
            if len(rtn_vector) < 1:
                return np.zeros(self.vector_dim)
            else:
                if len(rtn_vector) == self.vector_dim:
                    return rtn_vector
                logging.debug('Model name = %s, Current word = %s, Current size = %s, expected size = %s' % (
                 self.name, word, len(rtn_vector), self.vector_dim))
                return np.append(rtn_vector, np.zeros(self.vector_dim - len(rtn_vector)))

    def get_vector_of_unknown(self, word):
        """
        If word is UNK, use char_vector model instead.
        :param word:
        :return:
        """
        if self.name == Model_Constants.word2vec:
            if self.is_number(word):
                rtn_vector = self.model['<number>']
            else:
                if self.is_punct(word):
                    rtn_vector = self.model['<punct>']
                else:
                    rtn_vector = self.get_char_vector(self.char_model, word)
            if rtn_vector is not None:
                if len(rtn_vector) > self.vector_dim:
                    print('Warning: auto trim to %s/%s dimensions' % (self.vector_dim, len(rtn_vector)))
                    return rtn_vector[:self.vector_dim]
                else:
                    return rtn_vector
        else:
            return self.get_char_vector(self.char_model, word)


class Embedding_Models(object):
    __doc__ = '\n    Using all available embedding models to generate vectors\n    '

    def __init__(self, list_models):
        self.list_models = list_models

    def add_model(self, emb_model, char_model):
        """
        Add new model into the collection of embedding models. Note that, every model has to add char_model to handle
        unknown word.
        :param emb_model:
        :param char_model:
        :return:
        """
        if char_model is None:
            print('Warning: char_model is None -> cannot solve OOV word. Keep going ...')
        else:
            if isinstance(emb_model, Embedding_Model):
                emb_model.set_char_model(char_model)
                self.list_models.append(emb_model)
            else:
                raise Exception('Not an instance of embedding_model class.')

    def get_vector_of_document(self, document):
        """
        Get all embedding vectors for one document
        :param document:
        :return:
        """
        doc_vector = []
        for word in document:
            all_vectors_of_word = []
            for emb_model in self.list_models:
                emb_vector = emb_model.get_word_vector(word)
                all_vectors_of_word.extend(emb_vector)

            doc_vector.append(all_vectors_of_word)

        doc_vector = np.mean(doc_vector, axis=0)
        return doc_vector

    def get_word_vector_of_multi_embeddings(self, word):
        """
        Get all embedding vectors for one document
        :param word:
        :return:
        """
        word_vector = []
        for emb_model in self.list_models:
            emb_vector = emb_model.get_word_vector(word)
            word_vector.extend(emb_vector)

        return word_vector