# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/search.py
# Compiled at: 2019-09-05 14:05:50
# Size of source mod 2**32: 6596 bytes
import pandas as pd
from depgrep import depgrep_compile
from nltk.tgrep import tgrep_compile
from .utils import _get_tqdm, _make_tree, _tqdm_close, _tqdm_update, _tree_once

class Searcher(object):
    __doc__ = '\n    An engine for searching corpora\n    '

    def _understand_input_data(self, corpus):
        """
        Searcher understands Corpus, File and Dataset
        """
        from .file import File
        from .corpus import Corpus
        from .dataset import Dataset
        if type(corpus) == Corpus:
            to_search = corpus.files
            reference = None
        else:
            if type(corpus) == File:
                corpus = corpus.load()
                to_search = [corpus]
                reference = corpus.reference
            else:
                if type(corpus) == Dataset:
                    to_search = [
                     corpus]
                    reference = corpus.reference
        return (
         to_search, reference)

    def _tgrep_iteration(self, df):
        """
        Search a DataFrame-like object's parse column using tgrep.
        """
        df['_gram'] = False
        tree_once = _tree_once(df)
        if isinstance(tree_once.values[0], str):
            tree_once = tree_once.apply(_make_tree)
        indices_to_keep = dict()
        t = None
        if isinstance(self.corpus, pd.DataFrame):
            tqdm = _get_tqdm()
            running_count = 0
            t = tqdm(total=(len(tree_once)),
              desc='Searching trees',
              ncols=120,
              unit='tree')
        for n, tree in tree_once.items():
            if not tree:
                continue
            match_count = 0
            root_positions = tree.treepositions(order='leaves')
            positions = tree.treepositions()
            for position in positions:
                if self.query(tree[position]):
                    match_count += 1
                    size = len(tree[position].leaves())
                    first = tree[position].treepositions('leaves')[0]
                    first = position + first
                    pos = root_positions.index(first)
                    form = ','.join([str(x) for x in range(pos + 1, pos + size + 1)])
                    for x in range(pos + 1, pos + size + 1):
                        indices_to_keep[(n[0], n[1], x)] = form

            if isinstance(self.corpus, pd.DataFrame):
                running_count += match_count
                kwa = dict(results=(format(running_count, ',')))
                (t.set_postfix)(**kwa)
                t.update()

        _tqdm_close(t)
        return pd.Series(indices_to_keep)

    def depgrep(self, df, positions):
        """
        Run query over dependencies
        """
        if isinstance(self.corpus, pd.DataFrame):
            tqdm = _get_tqdm()
            prog_bar_info = dict(desc='Searching loaded corpus',
              unit='tokens',
              ncols=120)
            (tqdm.pandas)(**prog_bar_info)
            matches = df.progress_apply((self.query), axis=1, raw=True)
        else:
            matches = df.apply((self.query), axis=1, raw=True)
        try:
            matches = matches.fillna(False)
        except Exception:
            pass

        return [bool(i) for i in matches.values]

    def _depgrep_iteration(self, piece, query):
        """
        depgrep over one piece of data, returning the matching lines
        """
        df = piece.drop(['_n', 'file', 's', 'i'], axis=1, errors='ignore')
        df['_n'] = range(len(df))
        df = df.reset_index(level=(df.index.names))
        positions = {y:x for x, y in enumerate(list(df.columns))}
        values = df.values
        self.query = depgrep_compile(query,
          values=values,
          positions=positions,
          case_sensitive=(self.case_sensitive))
        bool_ix = self.depgrep(df, positions)
        return bool_ix

    def run(self, corpus, target, query, case_sensitive=True, inverse=False):
        """
        Search either trees or dependencies for query

        Return: Dataset of matching indices
        """
        from .file import File
        from .dataset import Dataset
        self.corpus = corpus
        self.to_search, self.reference = self._understand_input_data(corpus)
        self.target = target
        self.query = query
        self.case_sensitive = case_sensitive
        name = getattr(corpus, 'name', None)
        results = list()
        if target == 't':
            self.query = tgrep_compile(query)
        tqdm = _get_tqdm()
        kwa = dict(total=(len(self.to_search)),
          desc='Searching corpus',
          ncols=120,
          unit='document')
        t = tqdm(**kwa) if len(self.to_search) > 1 else None
        n = 0
        for piece in self.to_search:
            if isinstance(piece, File):
                piece = piece.load()
                piece['_n'] = list(range(n, len(piece) + n))
                n += len(piece)
            if self.target == 'd':
                depg = self._depgrep_iteration(piece, query)
                res = piece[depg] if not inverse else piece[(~depg)]
            else:
                if self.target == 't':
                    gram_ser = self._tgrep_iteration(piece)
                    res = piece.loc[gram_ser.index]
                    res['_gram'] = gram_ser
                if not res.empty:
                    results.append(res)
                _tqdm_update(t)

        _tqdm_close(t)
        results = Dataset(pd.concat(results, sort=False), name=name) if results else Dataset((pd.DataFrame()), name=name)
        results.reference = self.reference
        return results