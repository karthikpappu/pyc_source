# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/madjuice/Documents/Python/crosspredict/crosspredict/target_encoder.py
# Compiled at: 2020-01-23 09:41:17
# Size of source mod 2**32: 6234 bytes
from crosspredict.iterator import Iterator
import pandas as pd

class CrossTargetEncoder:

    def __init__(self, iterator, encoder_class, cols, col_encoded, n_splits=10, n_repeats=1, random_state=0, col_target=None, col_client=None, cv_byclient=False, **kwargs):
        self.iterator = iterator
        self._encoder_class = encoder_class
        self._encoder_kwargs = kwargs
        self.cols = cols
        self.col_encoded = col_encoded
        self.n_repeats = n_repeats
        self.n_splits = n_splits
        self.random_state = random_state
        self.col_target = col_target
        self.col_client = col_client
        self.cv_byclient = cv_byclient
        self._targetencoder_list = []
        self._targetencoded_cols = ['encoded_' + col for col in self.cols]

    def fit(self, df):
        self._targetencoder_list = []
        for X_train, X_val in self.iterator.split(df):
            encoder_ = TargetEncoder(encoder_class=self._encoder_class, cols=self.cols, 
             col_encoded=self.col_encoded, 
             n_splits=self.n_splits, 
             n_repeats=self.n_repeats, 
             random_state=self.random_state, 
             col_target=self.col_target, 
             col_client=self.col_client, 
             cv_byclient=self.cv_byclient, **self._encoder_kwargs)
            encoder_.fit(X_train)
            self._targetencoder_list.append(encoder_)

    def transform(self, fold, train=None, test=None):
        encoder_ = self._targetencoder_list[fold]
        if not (train is not None) | (test is not None):
            raise AssertionError
        else:
            transformed_test = None
            transformed_train = None
            if train is None:
                transformed_test = encoder_.predict(test)
            else:
                if test is None:
                    transformed_train = encoder_.transform(train)
                else:
                    transformed_test = encoder_.predict(test)
                    transformed_train = encoder_.transform(train)
        return (
         transformed_train, transformed_test)

    def predict(self, df):
        encoder_count = 0
        result = pd.DataFrame(index=(df.index),
          columns=(self._targetencoded_cols),
          data=0)
        for encoder_ in self._targetencoder_list:
            result += encoder_.predict(df) * encoder_.n_splits * encoder_.n_repeats
            encoder_count += encoder_.n_splits * encoder_.n_repeats

        result = result / encoder_count
        return result


class TargetEncoder:

    def __init__(self, encoder_class, cols, col_encoded, n_splits=10, n_repeats=1, random_state=0, col_target=None, col_client=None, cv_byclient=False, **kwargs):
        self._encoder_class = encoder_class
        self._encoder_kwargs = kwargs
        self.cols = cols
        self.col_encoded = col_encoded
        self.n_repeats = n_repeats
        self.n_splits = n_splits
        self.random_state = random_state
        self.col_target = col_target
        self.col_client = col_client
        self.cv_byclient = cv_byclient
        self._encoder_list = []
        self._encoded_cols = ['encoded_' + col for col in self.cols]
        self.iterator_double = Iterator(n_splits=(self.n_splits), n_repeats=(self.n_repeats),
          random_state=(self.random_state),
          col_target=(self.col_target),
          col_client=(self.col_client),
          cv_byclient=(self.cv_byclient))

    def fit(self, df):
        self._encoder_list = []
        self.iterator_double.fit(df=df)
        for fold, (train, val) in enumerate(self.iterator_double.split(df)):
            X_train, X_val = train, val
            encoder = (self._encoder_class)(cols=self.cols, **self._encoder_kwargs)
            encoder.fit(X_train[self.cols], X_train[self.col_encoded])
            self._encoder_list.append(encoder)

        return self

    def transform(self, df):
        result = pd.DataFrame(index=(df.index),
          columns=(self._encoded_cols),
          data=0)
        for fold, (train, val) in enumerate(self.iterator_double.split(df)):
            X_train, X_val = train, val
            encoder = self._encoder_list[fold]
            result.loc[(X_val.index,
             self._encoded_cols)] += encoder.transform(X_val[self.cols], X_val[self.col_encoded]).values / self.n_repeats

        return result

    def fit_transform(self, df):
        self._encoder_list = []
        result = pd.DataFrame(index=(df.index),
          columns=(self._encoded_cols),
          data=0)
        self.iterator_double.fit(df=df)
        for fold, (train, val) in enumerate(self.iterator_double.split(df)):
            X_train, X_val = train, val
            encoder = self._encoder_class(cols=(self.cols))
            encoder.fit(X_train[self.cols], X_train[self.col_target])
            self._encoder_list.append(encoder)
            result.loc[(X_val.index,
             self._encoded_cols)] += encoder.transform(X_val[self.cols], X_val[self.col_encoded]).values / self.n_repeats

        return result

    def predict(self, df):
        result = pd.DataFrame(index=(df.index),
          columns=(self._encoded_cols),
          data=0)
        for encoder in self._encoder_list:
            result.loc[(df.index,
             self._encoded_cols)] += encoder.transform(df[self.cols], df[self.col_encoded]).values / (self.n_repeats * self.n_splits)

        return result