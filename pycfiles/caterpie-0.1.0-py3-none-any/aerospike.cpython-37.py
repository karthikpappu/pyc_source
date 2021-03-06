# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/connectors/aerospike.py
# Compiled at: 2019-08-07 08:55:15
# Size of source mod 2**32: 4749 bytes
import aerospike
from aerospike import exception as aerospike_exceptions
import time, logging

class AerospikeConnector:

    def __init__(self, bootstrap_server, bootstrap_port, default_namespace=None, default_set=None, connect=False):
        self._config = {'hosts':[
          (
           bootstrap_server, bootstrap_port)], 
         'policies':{'timeout': 5000}}
        if default_namespace != None:
            self._default_namespace = default_namespace
        if default_set != None:
            self._default_set = default_set
        self._client = None
        if connect:
            self.open_connection()

    @property
    def client(self):
        return self._client

    def set_defaults(self, namespace, set_=None):
        if namespace == None:
            raise AttributeError('Namespace cannot be None')
        self._default_namespace = namespace
        if set_ != None:
            self._default_set = set_

    def open_connection(self, attempts=10):
        if self._client == None:
            try:
                self._client = aerospike.client(self._config).connect()
            except Exception:
                if attempts == 0:
                    logging.exception('')
                else:
                    time.sleep(1)
                    self.open_connection(attempts - 1)

    def close_connection(self):
        if self._client != None:
            self._client.close()
            self._client = None

    def _connect_get_askey(self, key, namespace, set_):
        self.open_connection()
        namespace, set_ = self._get_namespace_and_set_names(namespace, set_)
        as_key = (namespace, set_, key)
        return as_key

    def _get_namespace_and_set_names(self, namespace, set_):
        if namespace == None:
            if hasattr(self, '_default_namespace'):
                namespace = self._default_namespace
        if set_ == None:
            if hasattr(self, '_default_set'):
                set_ = self._default_set
        return (
         namespace, set_)

    def get_and_close(self, key, namespace=None, set_=None):
        self.open_connection()
        namespace, set_ = self._get_namespace_and_set_names(namespace, set_)
        try:
            bins = self.get(key, namespace, set_)
            self.close_connection()
            return bins
        except Exception:
            return

    def exists(self, key, namespace=None, set_=None):
        self.open_connection()
        namespace, set_ = self._get_namespace_and_set_names(namespace, set_)
        _, meta = self._client.exists((namespace, set_, key))
        if meta == None:
            return False
        return True

    def get(self, key, namespace=None, set_=None):
        as_key = self._connect_get_askey(key, namespace, set_)
        try:
            _, _, bins = self._client.get(as_key)
        except aerospike_exceptions.RecordNotFound:
            return (None, None)
        else:
            if len(bins) == 1:
                if 'value' in bins:
                    return (None, bins['value'])
                if 'key' in bins:
                    return (bins['key'], None)
            elif len(bins) == 2:
                if 'key' in bins:
                    if 'value' in bins:
                        return (
                         bins['key'], bins['value'])
                if 'key' in bins:
                    if key in bins:
                        return (
                         bins['key'], bins[key])
            return (
             None, bins)

    def put(self, key, bins=None, namespace=None, set_=None, store_key=False):
        if store_key:
            if bins == None:
                bins = {'key': key}
            elif type(bins) == dict:
                bins['key'] = key
            else:
                bins = {'key':key, 
                 'value':bins}
        else:
            if bins == None:
                bins = 0
            if type(bins) != dict:
                bins = {'value': bins}
        as_key = self._connect_get_askey(key, namespace, set_)
        self._client.put(as_key, bins)

    def remove(self, key, namespace=None, set_=None):
        as_key = self._connect_get_askey(key, namespace, set_)
        self._client.remove(as_key)

    def create_index(self, bin_, set_=None, type_='string', name=None, namespace=None):
        self.open_connection()
        namespace, set_ = self._get_namespace_and_set_names(namespace, set_)
        if not name:
            name = bin_ + '_index'
        if type_ == 'string':
            self._client.index_string_create(namespace, set_, bin_, name)
        elif type_ == 'integer' or type_ == 'numeric':
            self._client.index_integer_create(namespace, set_, bin_, name)