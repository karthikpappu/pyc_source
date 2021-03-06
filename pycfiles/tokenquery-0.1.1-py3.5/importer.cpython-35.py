# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/nlp/importer.py
# Compiled at: 2017-01-28 21:39:30
# Size of source mod 2**32: 2148 bytes
from conllu.parser import parse, parse_tree
from tokenquery.models.token import Token

class Importer:

    @classmethod
    def load_from_conll_u_file(self, file_path):
        tokens = []
        with open(file_path) as (input_file):
            data = input_file.read()
            paresed_data = parse(data)
            total_counter = 0
            total_span_counter = 0
            for sent_counter, sentence in enumerate(paresed_data):
                for token_counter, token in enumerate(sentence):
                    new_token = Token(total_counter, token['form'], total_span_counter, total_span_counter + len(token['form']))
                    total_span_counter += len(token['form']) + 1
                    if token_counter == 0:
                        new_token.add_a_label('SentenceBegin', str(sent_counter))
                    if token['lemma']:
                        new_token.add_a_label('lemma', token.get('lemma'))
                    if token['upostag']:
                        new_token.add_a_label('upostag', token.get('upostag'))
                    if token['xpostag']:
                        new_token.add_a_label('xpostag', token.get('xpostag'))
                    feats = token['feats']
                    if feats:
                        for feat in feats:
                            new_token.add_a_label('feat-' + feat, feats[feat])

                    if token['head']:
                        new_token.add_a_label('head', str(token.get('head')))
                    if token['deprel']:
                        new_token.add_a_label('deprel', str(token.get('deprel')))
                    if token['deps']:
                        new_token.add_a_label('deps', token.get('deps'))
                    misc = token['misc']
                    if misc:
                        for feat in misc:
                            new_token.add_a_label('misc-' + feat, misc[feat])

                    tokens.append(new_token)
                    total_counter += 1

        return tokens