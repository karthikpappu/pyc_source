# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/datasets/semeval14.py
# Compiled at: 2017-11-28 10:47:30
# Size of source mod 2**32: 1679 bytes
"""
Processing of the Semeval2014 dataset.

URL:
http://alt.qcri.org/semeval2014/task9/

REF:
Rosenthal, S., Ritter, A., Nakov, P., & Stoyanov, V. (2014, August). Semeval-2014 task 9: Sentiment analysis in twitter. 
In Proceedings of the 8th international workshop on semantic evaluation (SemEval 2014) (pp. 73-80)."""
import os, logging, re, pandas as pd
from gsitk.datasets import utils
from gsitk.datasets.datasets import Dataset
from gsitk.preprocess import normalize
logger = logging.getLogger(__name__)

class Semeval14(Dataset):

    def normalize_data(self):
        raw_datapath = os.path.join(self.data_path, self.info['properties']['data_file'])
        data = pd.read_csv(raw_datapath,
          header=None,
          encoding='utf-8',
          sep='\t',
          index_col=False,
          names=[
         'tweet_id',
         'user_id',
         'polarity',
         'text'])
        pol_conv = {'negative':-1, 
         'neutral':0, 
         'positive':1}
        data['polarity'].replace(pol_conv, inplace=True)
        text_data = normalize.normalize_text(data)
        data = pd.concat([data['polarity'], text_data], axis=1)
        data.columns = ['polarity', 'text']
        remove = lambda l: l != ['not', 'available']
        data = data.loc[data['text'].apply(remove)].reset_index(drop=True)
        return data