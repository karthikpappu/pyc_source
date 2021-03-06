# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/ext/flasik_db.py
# Compiled at: 2019-08-24 12:05:10
"""
Active Alchemy with some custom types

Just like sqlalchemy_utils, this module contains some custom types to
save in the db
"""
import active_alchemy
from sqlalchemy.engine.url import make_url as sa_make_url
import sqlalchemy_utils as sa_utils, flask_cloudy, redis

class FlasikDB(active_alchemy.ActiveAlchemy):
    """
    A custom ActiveAlchemy wrapper which defers the connection
    """

    def __init__(self):
        self.Model = active_alchemy.declarative_base(cls=active_alchemy.Model, name='Model')
        self.BaseModel = active_alchemy.declarative_base(cls=active_alchemy.BaseModel, name='BaseModel')
        self._initialized = False
        self._IS_OK_ = False
        self.redis = {}

    def connect__(self, uri, app):
        self.uri = uri
        self.info = sa_make_url(uri)
        self.options = self._cleanup_options(echo=False, pool_size=None, pool_timeout=None, pool_recycle=None, convert_unicode=True)
        self._initialized = True
        self._IS_OK_ = True
        self.connector = None
        self._engine_lock = active_alchemy.threading.Lock()
        self.session = active_alchemy._create_scoped_session(self, query_cls=active_alchemy.BaseQuery)
        self.Model.db, self.BaseModel.db = self, self
        self.Model._query, self.BaseModel._query = self.session.query, self.session.query
        self.init_app(app)
        active_alchemy._include_sqlalchemy(self)
        self.StorageObjectType = StorageObjectType
        return

    def connect_redis(self, name, url=None, decode_responses=True, **kwargs):
        """
        To connect to a Redis instance and attach it to db.redis 
        Example: 

            # Establish the connection
            db.connect_redis('cache', 'https://u:p@url/db')
            
            # Access it
            db.redis.cache.set('key', 'value')
        """
        connect = redis.from_url(url, decode_responses=decode_responses, **kwargs)
        setattr(self.redis, name, connect)
        return connect


class StorageObjectType(sa_utils.JSONType):
    """
    A type to store flask_cloudy Storage Object Type:
    -> https://github.com/mardix/flask-cloudy

    It provides a convenient way to store object and retrieve it as you would
    in the Flasik's storage.

    By default it will hold basic info such as name and url, size, extension
    Querying object.url, will not query the storage but use the default data
    this way it prevents certain overhead when dealing with multiple items

    Once an object is not found, it will try to connect to the storage and pull
    the file data

    If object is not found, it will return None.

    Example:
        from flasik import db

        class Image(db.Model):
            name = db.Column(db.String(255))
            image = db.Column(db.StorageObjectType)
            ...

        # Setting the object
        file = request.files.get("file")
        if file:
            upload = storage.upload(file)
            if upload is not None:
                new_img = Image.create(name="New Upload", image=upload)

        # Getting the object. By default, most keys are cached,
        # if not found it will load from the storage

        img = Image.get(1234)
        if img.image:
            url = img.image.url
            size = img.image.size
            full_url = img.image.full_url
            download_url = img.image.download_url

        # Force loading of the storage
        img.image.from_storage(my_other_storage)

        img.image.url (will get it from my_other_storage)

    """
    DEFAULT_KEYS = [
     'name', 'size', 'hash', 'url', 'full_url',
     'extension', 'type', 'path', 'provider_name']

    def process_bind_param(self, obj, dialect):
        """Get a flask_cloudy.Object and save it as a dict"""
        value = obj or {}
        if isinstance(obj, flask_cloudy.Object):
            value = {}
            for k in self.DEFAULT_KEYS:
                value[k] = getattr(obj, k)

        return super(self.__class__, self).process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        value = super(self.__class__, self).process_result_value(value, dialect)
        if value:
            return StorageObject(value)
        else:
            return


class StorageObject(dict):
    """
    This object will be loaded when querying the table
    It also extends dict so it can json serialized when being copied
    """

    def __init__(self, data):
        """
        :param data: dict
            name (required)
            ...
        """
        self._storage_obj = None
        self._storage_loaded = False
        self._data = data
        super(self.__class__, self).__init__(data)
        return

    def __getattr__(self, item):
        if item in self._data and not self._storage_loaded:
            return self._data.get(item)
        if not self._storage_loaded:
            from flasik.ext import storage
            self.from_storage(storage)
        return getattr(self._storage_obj, item)

    def from_storage(self, storage):
        """
        To use a different storage
        :param storage: flask_cloudy.Storage instance
        """
        self._storage_obj = storage.get(self._data['name'])
        self._storage_loaded = True