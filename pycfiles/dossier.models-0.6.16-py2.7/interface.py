# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/etl/interface.py
# Compiled at: 2015-07-08 07:34:06
"""
.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

Generate feature collections with your data
===========================================
This library ships with a command line program ``dossier.etl`` which
provides a rudimentary pipeline for transforming data from your database
to feature collections managed by :mod:`dossier.store`.

(Currently, ``dossier.etl`` is hard-coded to support a specific HBase
database, but it will be generalized as part of future work.)
"""
from __future__ import absolute_import, division, print_function
import abc
from itertools import chain
import json, logging, time, urllib, gensim, kvlayer
from dossier.store import Store
from streamcorpus import Chunk
from streamcorpus_pipeline.stages import Configured
from streamcorpus_pipeline._clean_visible import cleanse, make_clean_visible
from streamcorpus_pipeline._clean_html import make_clean_html
import yakonfig
from dossier.fc import FeatureCollection, StringCounter
import dossier.models.features as features
logger = logging.getLogger(__name__)

class ETL(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def cids_and_fcs(self):
        raise NotImplementedError


class to_dossier_store(Configured):
    """A :mod:`streamcorpus_pipeline` `writer` stage with one optional parameter:

    .. code-block:: yaml

        tfidf_path: path/to/tfidf.data

    """
    config_name = 'to_dossier_store'
    default_config = {'tfidf_path': None}

    def __init__(self, *args, **kwargs):
        super(to_dossier_store, self).__init__(*args, **kwargs)
        kvl = kvlayer.client()
        feature_indexes = None
        try:
            conf = yakonfig.get_global_config('dossier.store')
            feature_indexes = conf['feature_indexes']
        except KeyError:
            pass

        self.store = Store(kvl, feature_indexes=feature_indexes)
        tfidf_path = self.config.get('tfidf_path')
        self.tfidf = gensim.models.TfidfModel.load(tfidf_path)
        return

    def process(self, t_path, name_info, i_str):
        """converts each :attr:`streamcorpus.StreamItem.body.clean_html` from
        `t_path` into a :class:`~dossier.fc.FeatureCollection` and saves it in
        a :class:`~dossier.store.Store` configured with the global `kvlayer`
        config.

        """

        def cids_and_fcs():
            count = 0
            seen = set()
            for si in Chunk(t_path):
                clean_html = getattr(si.body, 'clean_html', '')
                if clean_html is None or len(clean_html.strip()) == 0:
                    logger.warn('dropping SI lacking clean_html: %r', si.abs_url)
                    continue
                if 'other_features' in si.other_content:
                    other_features = json.loads(si.other_content['other_features'].raw)
                else:
                    other_features = None
                fc = html_to_fc(clean_html=si.body.clean_html.decode('utf-8'), clean_visible=si.body.clean_visible.decode('utf-8'), encoding='utf-8', url=si.abs_url, timestamp=si.stream_time.epoch_ticks, other_features=other_features)
                add_sip_to_fc(fc, self.tfidf)
                content_id = mk_content_id(str(fc.get('meta_url')))
                if content_id in seen:
                    logger.warn('dropping duplicate content_id=%r', content_id)
                else:
                    seen.add(content_id)
                    yield (content_id, fc)
                    count += 1

            logger.info('saved %d FCs from %d SIs', count, len(seen))
            return

        self.store.put(cids_and_fcs())
        return []

    __call__ = process


def mk_content_id(key):
    return 'web|' + urllib.quote(key, safe='~')


def html_to_fc(html=None, clean_html=None, clean_visible=None, encoding=None, url=None, timestamp=None, other_features=None):
    """`html` is expected to be a raw string received over the wire from a
    remote webserver, and `encoding`, if provided, is used to decode
    it.  Typically, encoding comes from the Content-Type header field.
    The :func:`~streamcorpus_pipeline._clean_html.make_clean_html`
    function handles character encodings.

    """

    def add_feature(name, xs):
        if name not in fc:
            fc[name] = StringCounter()
        fc[name] += StringCounter(xs)

    timestamp = timestamp or int(time.time() * 1000)
    other_features = other_features or {}
    if clean_html is None:
        if html is not None:
            clean_html_utf8 = make_clean_html(html, encoding=encoding)
            clean_html = clean_html_utf8.decode('utf-8')
        else:
            clean_html_utf8 = ''
            clean_html = ''
    else:
        clean_html_utf8 = ''
    if clean_visible is None or len(clean_visible) == 0:
        clean_visible = make_clean_visible(clean_html_utf8).decode('utf-8')
    else:
        if isinstance(clean_visible, str):
            clean_visible = clean_visible.decode('utf-8')
        fc = FeatureCollection()
        fc['meta_raw'] = html and uni(html, encoding) or ''
        fc['meta_clean_html'] = clean_html
        fc['meta_clean_visible'] = clean_visible
        fc['meta_timestamp'] = unicode(timestamp)
        url = url or ''
        fc['meta_url'] = uni(url)
        add_feature('phone', features.phones(clean_visible))
        add_feature('email', features.emails(clean_visible))
        bowNP, normalizations = features.noun_phrases(cleanse(clean_visible), included_unnormalized=True)
        add_feature('bowNP', bowNP)
        bowNP_unnorm = chain(*normalizations.values())
        add_feature('bowNP_unnorm', bowNP_unnorm)
        add_feature('image_url', features.image_urls(clean_html))
        add_feature('a_url', features.a_urls(clean_html))
        fc['img_url_path_dirs'] = features.path_dirs(fc['image_url'])
        fc['img_url_hostnames'] = features.host_names(fc['image_url'])
        fc['img_url_usernames'] = features.usernames(fc['image_url'])
        fc['a_url_path_dirs'] = features.path_dirs(fc['a_url'])
        fc['a_url_hostnames'] = features.host_names(fc['a_url'])
        fc['a_url_usernames'] = features.usernames(fc['a_url'])
        xform = features.entity_names()
        fc = xform.process(fc)
        for feat_name, feat_val in other_features.iteritems():
            fc[feat_name] += StringCounter(feat_val)

    return fc


def add_sip_to_fc(fc, tfidf, limit=40):
    """add "bowNP_sip" to `fc` using `tfidf` data
    """
    if 'bowNP' not in fc:
        return
    else:
        if tfidf is None:
            return
        sips = features.sip_noun_phrases(tfidf, fc['bowNP'].keys(), limit=limit)
        fc['bowNP_sip'] = StringCounter(sips)
        return


def uni(s, encoding=None):
    if not isinstance(s, unicode):
        try:
            return unicode(s, encoding)
        except:
            try:
                return unicode(s, 'utf-8')
            except UnicodeDecodeError:
                return unicode(s, 'latin-1')

    return s