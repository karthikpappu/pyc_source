# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/esa_top_n_terms.py
# Compiled at: 2020-05-08 10:16:41
# Size of source mod 2**32: 6483 bytes
import re, math, time, pickle, gensim, argparse, pandas as pd
from collections import Counter
from nltk.stem import WordNetLemmatizer

class Preprocessor:

    def __init__(self, vocab_path):
        self._lemmatizer = WordNetLemmatizer()
        self._vocab = set(pickle.load(open(vocab_path, 'rb')))

    def preprocess(self, input, lemma=False):
        df = pd.read_csv(input)
        preprocessed = {}
        for index, row in df.iterrows():
            preprocessed[row['concept']] = self.to_bow(row['text'], lemma)

        return preprocessed

    def tokenize(self, text, lemma):
        text = text.lower()
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = re.sub('https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+', ' ', text)
        tokens = re.sub('[^A-Za-z]+', ' ', text).replace('  ', ' ')
        if lemma:
            tokens = [self._lemmatizer.lemmatize(word.strip()) for word in tokens.split(' ')]
            tokens = [t for t in tokens if not len(t) < 4]
            tokens = [t for t in tokens if t in self._vocab]
        else:
            tokens = tokens.split('')
            tokens = [t for t in tokens if not len(t) < 4]
        return tokens

    def to_bow(self, text, lemma):
        return dict(Counter(self.tokenize(text, lemma)))


def compute_tf(preprocessed, concepts, bows, terms):
    tf = pd.DataFrame(columns=(list(terms)))
    for concept in concepts:
        bow = preprocessed[concept]
        doc_length = sum(bow.values())
        row = {term:0.0 for term in terms}
        for term in bow:
            row[term] = bow[term] / doc_length

        tf = tf.append(row, ignore_index=True)

    tf.index = list(concepts)
    return tf


def compute_idf(preprocessed, concepts, terms):
    idfs = {}
    N = len(concepts)
    for term in terms:
        count = 0
        for concept in concepts:
            if term in preprocessed[concept].keys():
                count += 1

        idfs[term] = math.log(N / count, 2)

    return idfs


def compute_tfidf(tf, idfs, terms):
    for term in terms:
        tf[term] = tf[term] * idfs[term]

    return tf


def get_top_terms(tfidf, n):
    if n is None:
        return tfidf
    else:
        top_n = pd.DataFrame()
        for index, row in tfidf.iterrows():
            top_n[index] = row.transpose().sort_values(ascending=False)[:n].index

        return top_n


def doc_to_vec(doc_prep):
    document_vec = {}
    document_norm = norm(doc_prep)
    for term in doc_prep:
        document_vec[term] = doc_prep[term] / document_norm

    return document_vec


def get_esa_matrix(top_n, tfidf, concepts):
    esa_matrix = {}
    for concept in concepts:
        esa_matrix[concept] = {term:0.0 for term in list(top_n[concept])}
        for term in list(top_n[concept]):
            esa_matrix[concept][term] = tfidf.loc[(concept, term)]

    return esa_matrix


def norm(vec):
    s = 0.0
    for term in vec:
        s += vec[term] ** 2

    return math.sqrt(s)


def max_sim(model, document_vec, concept_vec):
    similarity = 0.0
    comparisons = 0
    start_time = time.time()
    for term_1 in document_vec:
        max_similarity = -1
        matched_term = None
        for term_2 in concept_vec:
            comparisons += 1
            current_similarity = model.similarity(term_1, term_2)
            if current_similarity < 0:
                print(current_similarity)
                current_similarity = 0
            if current_similarity > max_similarity:
                max_similarity = current_similarity
                matched_term = term_2
            elif max_similarity >= 1.0:
                max_similarity = 1
                break
                print(max_similarity)
            else:
                continue

        if matched_term != None:
            similarity += document_vec[term_1] * concept_vec[matched_term] * max_similarity

    similarity /= norm(document_vec) * norm(concept_vec)
    end_time = time.time()
    return (similarity, comparisons, end_time - start_time)


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', required=True)
    parser.add_argument('--corpus-path', required=True)
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--model-vocab', required=True)
    parser.add_argument('--text', required=True)
    return parser


p = None
esa_matrix = None
model = None
concepts = None

def normalize(esa_matrix):
    for concept in esa_matrix:
        concept_norm = norm(esa_matrix[concept])
        for term in esa_matrix[concept]:
            esa_matrix[concept][term] = esa_matrix[concept][term] / concept_norm


def initialize_model(path_corpus, path_model, path_model_vocab, n):
    global concepts
    global esa_matrix
    global model
    global p
    if esa_matrix == None:
        if concepts == None:
            p = Preprocessor(path_model_vocab)
            preprocessed = p.preprocess(path_corpus, lemma=True)
            concepts = tuple(preprocessed.keys())
            bows = tuple([preprocessed[bow] for bow in preprocessed])
            terms = tuple(set([word for bow in bows for word in bow]))
            tf = compute_tf(preprocessed, concepts, bows, terms)
            idfs = compute_idf(preprocessed, concepts, terms)
            tfidf = compute_tfidf(tf, idfs, terms)
            top_n = get_top_terms(tfidf, n)
            esa_matrix = get_esa_matrix(top_n, tfidf, concepts)
            normalize(esa_matrix)
            model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(path_model, binary=True)
            model.init_sims(replace=True)


def model_topic(path_corpus, path_model, path_model_vocab, text, n):
    if n == -1:
        n = None
    initialize_model(path_corpus, path_model, path_model_vocab, n)
    doc_prep = p.to_bow(text, lemma=True)
    document_vec = doc_to_vec(doc_prep)
    result = {}
    for concept in concepts:
        res = max_sim(model, document_vec, esa_matrix[concept])
        result[concept] = res[0]

    return result


def main():
    parser = create_argparser()
    args = parser.parse_args()
    n = int(vars(args)['n'])
    path_corpus = vars(args)['corpus_path']
    path_model = vars(args)['model_path']
    path_vocab = vars(args)['model_vocab']
    text = vars(args)['text']
    result = model_topic(path_corpus, path_model, path_vocab, text, n)
    print(result)


if __name__ == '__main__':
    main()