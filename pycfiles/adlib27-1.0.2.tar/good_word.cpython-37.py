# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/adversaries/good_word.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 10757 bytes
from typing import List, Dict
from adlib.adversaries.adversary import Adversary
from data_reader.binary_input import Instance, BinaryFeatureVector
from adlib.learners.learner import Learner
from copy import deepcopy

class GoodWord(Adversary):
    BEST_N = 'best_n'
    FIRST_N = 'first_n'

    def __init__(self, n=100, attack_model_type=BEST_N):
        """
        :param n: number of words needed
        :param attack_model_type: choose the best-n or first-n algorithm
        """
        self.learn_model = None
        self.positive_instance = None
        self.negative_instance = None
        self.n = n
        self.num_queries = 0
        self.attack_model_type = attack_model_type

    def attack(self, instances: List[Instance]) -> List[Instance]:
        word_indices = self.get_n_words()
        transformed_instances = []
        for instance in instances:
            transformed_instance = deepcopy(instance)
            if instance.get_label() == Learner.positive_classification:
                transformed_instances.append(self.add_words_to_instance(transformed_instance, word_indices))
            else:
                transformed_instances.append(transformed_instance)

        print('Number of queries issued:', self.num_queries)
        return transformed_instances

    def get_available_params(self):
        return {'n':self.n, 
         'positive_instance':self.positive_instance, 
         'negative_instance':self.negative_instance}

    def set_params(self, params: Dict):
        if 'n' in params:
            self.n = params['n']
        if 'attack_model_type' in params:
            if not self.is_valid_attack_model_type(params['attack_model_type']):
                raise ValueError('Invalid attack model type')
            self.attack_model_type = params['attack_model_type']

    def is_valid_attack_model_type(self, model_type):
        return model_type in [GoodWord.BEST_N, GoodWord.FIRST_N]

    def set_adversarial_params(self, learner, train_instances):
        self.learn_model = learner
        instances = train_instances
        self.positive_instance = next((x for x in instances if x.get_label() == learner.positive_classification), None)
        self.negative_instance = next((x for x in instances if x.get_label() == learner.negative_classification), None)
        self.feature_space = set()
        for instance in train_instances:
            self.feature_space.update(instance.get_feature_vector())

    def feature_difference(self, y: BinaryFeatureVector, xa: BinaryFeatureVector) -> List:
        y_array = y.get_csr_matrix()
        xa_array = xa.get_csr_matrix()
        C_y = (y_array - xa_array).indices
        return C_y

    def add_words_to_instance(self, instance, word_indices):
        feature_vector = instance.get_feature_vector()
        for index in word_indices:
            if index not in feature_vector:
                feature_vector.flip_bit(index)

        return instance

    def find_witness(self):
        curr_message = deepcopy(self.negative_instance.get_feature_vector())
        curr_message_words = set(curr_message)
        spam_message = self.positive_instance.get_feature_vector()
        spam_message_words = set(spam_message)
        prev_message = None
        while self.predict_and_record(curr_message) != Learner.positive_classification:
            prev_message = deepcopy(curr_message)
            word_removed = False
            for index in curr_message:
                if index not in spam_message_words:
                    curr_message.flip_bit(index)
                    word_removed = True
                    break

            if word_removed:
                continue
            word_added = False
            for index in spam_message:
                if index not in curr_message_words:
                    curr_message.flip_bit(index)
                    curr_message_words.add(index)
                    word_added = True
                    break

            assert word_added, 'Could not find witness'

        return (
         curr_message, prev_message)

    def first_n_words(self, spam_message, legit_message):
        if not self.n:
            raise ValueError('Must specify n')
        negative_weight_word_indices = set()
        spam_message, _ = self.find_witness()
        for feature in self.feature_space:
            if spam_message.get_feature(feature) == 0:
                spam_message.flip_bit(feature)
                prediction_result = self.predict_and_record(spam_message)
                if prediction_result == Learner.negative_classification:
                    negative_weight_word_indices.add(feature)
                if len(negative_weight_word_indices) == self.n:
                    return negative_weight_word_indices
                spam_message.flip_bit(feature)

        return negative_weight_word_indices

    def best_n_words(self, spam_message, legit_message):
        barely_spam_message, barely_legit_message = self.find_witness()
        positive_weight_word_indices = self.build_word_set(barely_legit_message, Learner.positive_classification)
        negative_weight_word_indices = self.build_word_set(barely_spam_message, Learner.negative_classification)
        best_n_word_indices = set()
        iterations_without_change = 0
        max_iterations_without_change = 10
        for spammy_word_index in positive_weight_word_indices:
            is_index_in_spam_msg = barely_spam_message.get_feature(spammy_word_index) == 1
            if not is_index_in_spam_msg:
                barely_spam_message.flip_bit(spammy_word_index)
            if not is_index_in_spam_msg:
                barely_spam_message.flip_bit(spammy_word_index)
            else:
                small_weight_word_indices = self.build_word_set(barely_spam_message, Learner.positive_classification, negative_weight_word_indices)
                large_weight_word_indices = self.build_word_set(barely_spam_message, Learner.negative_classification, negative_weight_word_indices)
                if not is_index_in_spam_msg:
                    barely_spam_message.flip_bit(spammy_word_index)
                elif len(best_n_word_indices) + len(large_weight_word_indices) < self.n:
                    negative_weight_word_indices = negative_weight_word_indices - large_weight_word_indices
                    best_n_word_indices = best_n_word_indices.union(large_weight_word_indices)
                    if len(large_weight_word_indices) == 0:
                        iterations_without_change += 1
                    else:
                        iterations_without_change = 0
                else:
                    negative_weight_word_indices = negative_weight_word_indices - small_weight_word_indices
                    if len(small_weight_word_indices) == 0:
                        iterations_without_change += 1
                    else:
                        iterations_without_change = 0
            if iterations_without_change == max_iterations_without_change:
                for i in range(min(self.n - len(best_n_word_indices), len(negative_weight_word_indices))):
                    best_n_word_indices.add(negative_weight_word_indices.pop())

                return best_n_word_indices

        return best_n_word_indices

    def build_word_set(self, message, intended_classification, indices_to_check=None):
        indices_to_check = indices_to_check if indices_to_check != None else self.feature_space
        result = set()
        for index in indices_to_check:
            if message.get_feature(index) == 0:
                message.flip_bit(index)
                prediction_result = self.predict_and_record(message)
                if prediction_result == intended_classification:
                    result.add(index)
                message.flip_bit(index)

        return result

    def predict_and_record(self, message):
        self.num_queries += 1
        return self.predict(Instance(0, message))

    def predict(self, instance):
        return self.learn_model.predict(instance)

    def get_n_words(self):
        if self.attack_model_type == GoodWord.FIRST_N:
            return self.first_n_words(self.positive_instance.get_feature_vector(), self.negative_instance.get_feature_vector())
        if self.attack_model_type == GoodWord.BEST_N:
            return self.best_n_words(self.positive_instance.get_feature_vector(), self.negative_instance.get_feature_vector())
        raise ValueError('Unknown attack model type')