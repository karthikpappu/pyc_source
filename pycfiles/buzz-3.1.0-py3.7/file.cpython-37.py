# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/file.py
# Compiled at: 2019-09-06 06:11:37
# Size of source mod 2**32: 2791 bytes
import os
from functools import total_ordering
from .corpus import Corpus
from .utils import _get_nlp, _to_df, _order_df_columns, _tree_once, _make_tree

@total_ordering
class File(Corpus):

    def __init__(self, path, **kwargs):
        self.path = path
        self.filename = os.path.basename(path)
        self.name = self.filename.split('.txt')[0]
        self.files = None
        self.subcorpora = None
        self.nlp = None
        self.is_parsed = self.filename.endswith(('.conll', '.conllu'))
        self.in_subcorpus = kwargs.get('in_subcorpus')

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        in_memory = self.load() if self.is_parsed else self.read()
        return in_memory.__iter__()

    def to_spacy(self, language='en'):
        """
        get spaCy model of this file
        """
        self.nlp = _get_nlp(language=language)
        with open(self.path, 'r') as (fo):
            text = fo.read().strip()
        if self.is_parsed:
            pre = '# text = '
            lines = [i.replace(pre, '').strip() for i in text.splitlines() if i.startswith(pre)]
            text = ' '.join((i for i in lines))
            text = text.replace('  ', ' ')
        return self.nlp(text)

    def __len__(self):
        raise NotImplementedError('File has no length')

    def __bool__(self):
        return True

    def table(self, show=[
 'w'], subcorpora=['file'], **kwargs):
        """
        Generate a frequency table for this file
        """
        if isinstance(show, str):
            show = [
             show]
        if isinstance(subcorpora, str):
            subcorpora = [
             subcorpora]
        needed = show + subcorpora
        usecols = kwargs.pop('usecols', needed)
        loaded = self.load(usecols=usecols)
        return (loaded.table)(show=show, subcorpora=subcorpora, **kwargs)

    def load(self, load_trees=False, **kwargs):
        """
        For parsed dataset, get dataframe or spacy object
        """
        if self.is_parsed:
            df = _to_df(self, **kwargs)
            df['_n'] = range(len(df))
            df = _order_df_columns(df)
            df.reference = df
            if load_trees:
                tree_once = _tree_once(df)
                if isinstance(tree_once.values[0], str):
                    df['parse'] = tree_once.apply(_make_tree)
            return df
        raise NotImplementedError('Cannot load DataFame from unparsed file. Use file.read()')

    def read(self):
        """
        Get the file contents as string
        """
        with open(self.path, 'r') as (fo):
            data = fo.read()
        return data