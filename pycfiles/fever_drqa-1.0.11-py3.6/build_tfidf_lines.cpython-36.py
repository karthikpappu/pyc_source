# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqascripts/retriever/build_tfidf_lines.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 5048 bytes
"""A script to build the tf-idf document matrices for retrieval."""
import argparse, math, logging
from drqa.retriever import TfidfDocRanker
from drqa import tokenizers
from .build_tfidf import TfIdfBuilder
logger = logging.getLogger('DRQA')

class OnlineTfidfDocRanker(TfidfDocRanker):
    __doc__ = 'Loads a pre-weighted inverted index of token/document terms.\n    Scores new queries by taking sparse dot products.\n    '

    def __init__(self, args, lines, freqs=None, strict=True):
        """
        Args:
            tfidf_path: path to saved model file
            strict: fail on empty queries or continue (and return empty result)
        """
        logging.info('Counting words...')
        tb = TfIdfBuilder(args, 'memory', {'lines': lines})
        count_matrix, doc_dict = tb.get_count_matrix()
        logger.info('Making tfidf vectors...')
        tfidf = tb.get_tfidf_matrix(count_matrix)
        if freqs is None:
            logger.info('Getting word-doc frequencies...')
            freqs = tb.get_doc_freqs(count_matrix)
        metadata = {'doc_freqs':freqs, 
         'tokenizer':args.tokenizer, 
         'hash_size':args.hash_size, 
         'ngram':args.ngram, 
         'doc_dict':doc_dict}
        self.doc_mat = tfidf
        self.ngrams = metadata['ngram']
        self.hash_size = metadata['hash_size']
        self.tokenizer = tokenizers.get_class(metadata['tokenizer'])()
        self.doc_freqs = metadata['doc_freqs'].squeeze()
        self.doc_dict = metadata['doc_dict']
        self.num_docs = len(self.doc_dict[0])
        self.strict = strict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ngram', type=int, default=2, help='Use up to N-size n-grams (e.g. 2 = unigrams + bigrams)')
    parser.add_argument('--hash-size', type=int, default=(int(math.pow(2, 24))), help='Number of buckets to use for hashing ngrams')
    parser.add_argument('--tokenizer', type=str, default='simple', help="String option specifying tokenizer type to use (e.g. 'corenlp')")
    parser.add_argument('--num-workers', type=int, default=None, help='Number of CPU processes (for tokenizing, etc)')
    args = parser.parse_args()
    ranker = OnlineTfidfDocRanker(args, [
     'It said that because the ads had been shared widely on social media , they therefore would have been seen by a large number of people , including some children who did not actively follow the Poundland accounts .',
     'The ads were irresponsible and likely to cause serious or widespread offence , said the ASA , which also revealed it had received 85 complaints about the Poundland campaign .',
     "Thousands of women who work in Tesco stores could receive back pay totalling £20,000 if the legal challenge demanding parity with men who work in the company's warehouses is successful.",
     'Lawyers say hourly-paid female store staff earn less than men even though the value of the work is comparable.',
     'Paula Lee, of Leigh Day solicitors told the BBC it was time for Tesco to tackle the problem of equal pay for work of equal worth.',
     'Her firm has been contacted by more than 1,000 Tesco staff and will this week take the initial legal steps for 100 of them.',
     'The most common rate for women is £8 an hour whereas for men the hourly rate can be as high as £11 an hour, she added.',
     'Since 1984 workers doing jobs that require comparable skills, have similar levels of responsibility and are of comparable worth to the employer, should also be rewarded equally, according to the law.',
     'Thus if you are a cleaner, lugging mops and buckets up and down staircases, you may have a case for being paid the same as co-workers collecting rubbish bins.',
     "It doesn't matter whether the cleaner or the shop floor worker is male or female, they may still have a case to see their pay upped to match colleagues doing other jobs.But in practice many of the poorer paid jobs have been done by women."])
    print(ranker.closest_docs('female met the employer and had the responsibility to collect rubbish bins', k=5))