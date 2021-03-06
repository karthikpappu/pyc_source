# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/noun/_noun_postprocessing.py
# Compiled at: 2018-10-01 03:38:35
# Size of source mod 2**32: 3048 bytes
import os
from soynlp.utils import check_dirs
filepath = os.path.dirname(os.path.realpath(__file__))
josapath = filepath + '/frequent_enrolled_josa.txt'
suffixpath = filepath + '/frequent_noun_suffix.txt'
with open(josapath, encoding='utf-8') as (f):
    josaset = {word.strip() for word in f if word if word}
with open(suffixpath, encoding='utf-8') as (f):
    suffixset = {word.strip() for word in f if word if word}

def write_log(path, header, words):
    check_dirs(path)
    with open(path, 'a', encoding='utf-8') as (f):
        f.write('\n{}\n'.format(header))
        for word in sorted(words):
            f.write('{}\n'.format(word))


def _select_true_nouns(nouns, removals):
    return {word:score for word, score in nouns.items() if (word in removals) == False}


def detaching_features(nouns, features, logpath=None, logheader=None):
    if not logheader:
        logheader = '## Ignored noun candidates from detaching features'
    removals = set()
    for word in nouns:
        if len(word) <= 2:
            continue
        for e in range(2, len(word)):
            l, r = word[:e], word[e:]
            if len(r) <= 1:
                continue
            if l in nouns and r in features:
                removals.add(word)
                break

    if logpath:
        write_log(logpath, logheader, removals)
    nouns_ = _select_true_nouns(nouns, removals)
    return (nouns_, removals)


def ignore_features(nouns, features, logpath=None, logheader=None):
    if not logheader:
        logheader = '## Ignored noun candidates these are same with features'
    removals = set()
    for word in nouns:
        if word in features:
            removals.add(word)

    if logpath:
        write_log(logpath, logheader, removals)
    nouns_ = _select_true_nouns(nouns, removals)
    return (nouns_, removals)


def check_N_is_NJ(nouns, lrgraph, min_num_of_josa=5, logpath=None, logheader=None):
    if not logheader:
        logheader = '## Ignored true N+J'
    removals = set()
    for word, score in nouns.items():
        n = len(word)
        if n <= 2:
            continue
        for i in range(2, n):
            l, r = word[:i], word[i:]
            if r not in josaset or r in suffixset or l not in nouns or score[0] >= nouns[l][0]:
                continue
            features = lrgraph._lr_origin.get(l, {})
            features = [r for r in features if r in josaset]
            n_josa = len(features)
            if n_josa >= min_num_of_josa:
                removals.add(word)

    if logpath:
        write_log(logpath, logheader, removals)
    nouns_ = _select_true_nouns(nouns, removals)
    return (nouns_, removals)


def ngram_nouns(nouns, sents, min_count=10, min_score=0.7, max_n=2):
    ngram_nouns = {}
    return ngram_nouns