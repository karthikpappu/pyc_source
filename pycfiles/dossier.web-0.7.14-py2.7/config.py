# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/web/config.py
# Compiled at: 2015-09-05 21:24:22
"""dossier.web.config

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.
"""
import functools, logging, threading, traceback
from dossier.label import LabelStore
from dossier.store import ElasticStore
import kvlayer, yakonfig, yakonfig.factory
logger = logging.getLogger(__name__)

def safe_service(attr, default_value=None):
    """A **method** decorator for creating safe services.

    Given an attribute name, this returns a decorator for creating
    safe services. Namely, if a service that is not yet available is
    requested (like a database connection), then ``safe_service`` will
    log any errors and set the given attribute to ``default_value``.

    :param str attr: attribute name
    :param object default_value: default value to set
    :rtype: decorator
    """

    def _(fun):

        @functools.wraps(fun)
        def run(self):
            try:
                return fun(self)
            except:
                logger.error(traceback.format_exc())
                setattr(self, attr, default_value)

        return run

    return _


def thread_local_property(name):
    """Creates a thread local ``property``."""
    name = '_thread_local_' + name

    def fget(self):
        try:
            return getattr(self, name).value
        except AttributeError:
            return

        return

    def fset(self, value):
        getattr(self, name).value = value

    return property(fget=fget, fset=fset)


class Config(yakonfig.factory.AutoFactory):
    """Configuration for dossier.web.

    .. automethod:: dossier.web.Config.create
    .. autoattribute:: dossier.web.Config.kvlclient
    .. autoattribute:: dossier.web.Config.store
    .. autoattribute:: dossier.web.Config.label_store
    """
    _THREAD_LOCALS = [
     'store', 'label_store', 'kvlclient']
    for n in _THREAD_LOCALS:
        locals()['_' + n] = thread_local_property(n)

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.new_config()
        for n in self._THREAD_LOCALS:
            setattr(self, '_thread_local_' + n, threading.local())

    def new_config(self):
        super(Config, self).new_config()
        self._idx_map = None
        return

    @property
    def config_name(self):
        return 'dossier.web'

    @property
    def web_config(self):
        return self

    @property
    def auto_config(self):
        return [ElasticStore, LabelStore]

    @property
    @safe_service('_store')
    def store(self):
        """Return a thread local :class:`dossier.store.Store` client."""
        if self._store is None:
            config = global_config('dossier.store')
            self._store = self.create(ElasticStore, config=config)
        return self._store

    @property
    @safe_service('_label_store')
    def label_store(self):
        """Return a thread local :class:`dossier.label.LabelStore` client."""
        if self._label_store is None:
            config = global_config('dossier.label')
            if 'kvlayer' in config:
                kvl = kvlayer.client(config=config['kvlayer'])
                self._label_store = LabelStore(kvl)
            else:
                self._label_store = self.create(LabelStore, config=config)
        return self._label_store

    @property
    @safe_service('_kvlclient')
    def kvlclient(self):
        """Return a thread local ``kvlayer`` client."""
        if self._kvlclient is None:
            self._kvlclient = kvlayer.client()
        return self._kvlclient


def global_config(name):
    try:
        return yakonfig.get_global_config(name)
    except KeyError:
        return {}