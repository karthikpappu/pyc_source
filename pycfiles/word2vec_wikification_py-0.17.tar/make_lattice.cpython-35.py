# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/word2vec_wikification_py/make_lattice.py
# Compiled at: 2017-03-15 17:26:27
# Size of source mod 2**32: 10687 bytes
try:
    from gensim.models import Word2Vec, KeyedVectors
except ImportError:
    from gensim.models import Word2Vec

from numpy import ndarray
from word2vec_wikification_py import init_logger
from word2vec_wikification_py.models import WikipediaArticleObject, PersistentDict, LatticeObject, IndexDictionaryObject, EdgeObject
from typing import List, Tuple, Union, Any, Dict, Set
from tempfile import mkdtemp
from scipy.sparse import csr_matrix
import os, logging
logger = logging.getLogger(name=init_logger.LOGGER_NAME)

class TransitionEdgeObject(object):
    __slots__ = [
     'row_index', 'column_index', 'transition_score']

    def __init__(self, row_index: int, column_index: int, transition_score: float):
        self.row_index = row_index
        self.column_index = column_index
        self.transition_score = transition_score


def __update_index_dictionary(key: Tuple[(int, str)], index_dictionary: Dict[(Tuple[(int, str)], int)]) -> Dict[(Tuple[(int, str)], int)]:
    """
    """
    if key in index_dictionary:
        raise Exception('The key is already existing in index_dictionary. key={}'.format(key))
    else:
        if len(index_dictionary) == 0:
            index_dictionary[key] = 0
        else:
            latest_index_number = max(index_dictionary.values())
            index_dictionary[key] = latest_index_number + 1
        return index_dictionary


def make_state_transition_edge(state_t_word_tuple, state_t_plus_word_tuple, state2index_obj, entity_vector):
    """* What you can do
    - tの単語xからt+1の単語x'への遷移スコアを計算する

    * Output
    - tuple object whose element is (transition_element, row2index, column2index)
    - transition_element is (row_index, column_index, transition_score)
    """
    if isinstance(entity_vector, Word2Vec):
        if state_t_word_tuple[1] not in entity_vector.wv.vocab:
            raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_word_tuple))
        if state_t_plus_word_tuple[1] not in entity_vector.wv.vocab:
            raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_plus_word_tuple))
    else:
        if isinstance(entity_vector, KeyedVectors):
            if state_t_word_tuple[1] not in entity_vector.vocab:
                raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_word_tuple))
            if state_t_plus_word_tuple[1] not in entity_vector.vocab:
                raise Exception('Element does not exist in entity_voctor model. element={}'.format(state_t_plus_word_tuple))
        else:
            raise Exception()
        transition_score = entity_vector.similarity(state_t_word_tuple[1], state_t_plus_word_tuple[1])
        if state_t_word_tuple in state2index_obj.state2index['row2index']:
            row_index = state2index_obj.state2index['row2index'][state_t_word_tuple]
        else:
            state2index_obj.state2index['row2index'] = __update_index_dictionary(state_t_word_tuple, state2index_obj.state2index['row2index'])
            row_index = state2index_obj.state2index['row2index'][state_t_word_tuple]
        if state_t_plus_word_tuple in state2index_obj.state2index['column2index']:
            column_index = state2index_obj.state2index['column2index'][state_t_plus_word_tuple]
        else:
            state2index_obj.state2index['column2index'] = __update_index_dictionary(state_t_plus_word_tuple, state2index_obj.state2index['column2index'])
            column_index = state2index_obj.state2index['column2index'][state_t_plus_word_tuple]
    transition_edge_obj = TransitionEdgeObject(row_index=row_index, column_index=column_index, transition_score=transition_score)
    return (
     transition_edge_obj, state2index_obj)


def make_state_transition(index: int, seq_wiki_article_name: List[WikipediaArticleObject], state2index_obj: IndexDictionaryObject, entity_vector_model: Word2Vec) -> Tuple[(List[EdgeObject], List[TransitionEdgeObject])]:
    """* What you can do
    - You make all state-information between state_index and state_index_plus_1
    """
    edge_group = []
    seq_transition_element = []
    for candidate_wikipedia_article_name in seq_wiki_article_name[index].candidate_article_name:
        for candiate_wikipedia_article_name_state_plus in seq_wiki_article_name[(index + 1)].candidate_article_name:
            state_t_word_tuple = (
             index, candidate_wikipedia_article_name)
            state_t_plus_word_tuple = (index + 1, candiate_wikipedia_article_name_state_plus)
            transition_element, state2index_obj = make_state_transition_edge(state_t_word_tuple=state_t_word_tuple, state_t_plus_word_tuple=state_t_plus_word_tuple, state2index_obj=state2index_obj, entity_vector=entity_vector_model)
            seq_transition_element.append(transition_element)
            edge_group.append(EdgeObject(state2index_obj.state2index['row2index'][state_t_word_tuple], state2index_obj.state2index['column2index'][state_t_plus_word_tuple]))

    return (edge_group, seq_transition_element)


def make_state_transition_sequence(seq_wiki_article_name: List[WikipediaArticleObject], entity_vector_model: Word2Vec, state2index_obj: IndexDictionaryObject) -> Tuple[(IndexDictionaryObject,
 List[List[EdgeObject]],
 csr_matrix)]:
    """系列での遷移行列を作成する
    """
    seq_transition_element = []
    seq_edge_group = []
    for index in range(0, len(seq_wiki_article_name) - 1):
        edge_group, seq_transition_edge_object = make_state_transition(index=index, seq_wiki_article_name=seq_wiki_article_name, state2index_obj=state2index_obj, entity_vector_model=entity_vector_model)
        seq_edge_group.append(edge_group)
        seq_transition_element += seq_transition_edge_object

    data = [transition_tuple.transition_score for transition_tuple in seq_transition_element]
    row = [transition_tuple.row_index for transition_tuple in seq_transition_element]
    column = [transition_tuple.column_index for transition_tuple in seq_transition_element]
    transition_matrix = csr_matrix((
     data, (row, column)), shape=(
     len(state2index_obj.state2index['row2index']), len(state2index_obj.state2index['column2index'])))
    return (
     state2index_obj, seq_edge_group, transition_matrix)


def filter_out_of_vocabulary_word(wikipedia_article_obj: WikipediaArticleObject, vocabulary_words: Set) -> Union[(bool, WikipediaArticleObject)]:
    """* What you can do
    - You remove out-of-vocabulary word from wikipedia_article_obj.candidate_article_name
    """
    filtered_article_name = []
    for article_name in wikipedia_article_obj.candidate_article_name:
        if article_name in vocabulary_words:
            filtered_article_name.append(article_name)
        else:
            logger.warning(msg='Out of vocabulary word. It removes. word = {}'.format(article_name))

    if len(filtered_article_name) == 0:
        return False
    else:
        wikipedia_article_obj.candidate_article_name = filtered_article_name
        return wikipedia_article_obj


def make_lattice_object(seq_wiki_article_name, entity_vector_model, path_wordking_dir=None, is_use_cache=True):
    """* What you can do

    """
    if path_wordking_dir is None:
        path_wordking_dir = mkdtemp()
    if is_use_cache:
        persistent_state2index = PersistentDict(os.path.join(path_wordking_dir, 'column2index.json'), flag='c', format='json')
        persistent_state2index['row2index'] = {}
        persistent_state2index['column2index'] = {}
    else:
        persistent_state2index = {}
        persistent_state2index['row2index'] = {}
        persistent_state2index['column2index'] = {}
    state2dict_obj = IndexDictionaryObject(state2index=persistent_state2index, index2state={})
    if isinstance(entity_vector_model, Word2Vec):
        vocabulary_words = set(entity_vector_model.wv.vocab.keys())
    else:
        if isinstance(entity_vector_model, KeyedVectors):
            vocabulary_words = set(entity_vector_model.vocab.keys())
        else:
            raise Exception()
        seq_wiki_article_name = [wiki_article_name for wiki_article_name in seq_wiki_article_name if filter_out_of_vocabulary_word(wiki_article_name, vocabulary_words) is not False]
        updated_state2dict_obj, seq_edge_group, transition_matrix = make_state_transition_sequence(seq_wiki_article_name=seq_wiki_article_name, entity_vector_model=entity_vector_model, state2index_obj=state2dict_obj)
        if is_use_cache:
            index2state = PersistentDict(os.path.join(path_wordking_dir, 'index2row.json'), flag='c', format='json')
            updated_state2dict_obj.index2state = index2state
        else:
            updated_state2dict_obj.index2state = {}
    updated_state2dict_obj.index2state['index2row'] = {value:key for key, value in updated_state2dict_obj.state2index['row2index'].items()}
    updated_state2dict_obj.index2state['index2column'] = {value:key for key, value in updated_state2dict_obj.state2index['column2index'].items()}
    return LatticeObject(transition_matrix=transition_matrix, index_dictionary_obj=updated_state2dict_obj, seq_edge_groups=seq_edge_group, seq_wiki_article_name=seq_wiki_article_name)