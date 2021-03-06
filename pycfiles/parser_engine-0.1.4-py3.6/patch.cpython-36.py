# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/patch.py
# Compiled at: 2019-03-22 03:43:37
# Size of source mod 2**32: 3133 bytes
import six
from scrapy.item import DictItem
from scrapy.utils.misc import load_object
from scrapy_redis import connection, defaults
from .log import debug

def __setitem__(self, key, value):
    if key in self.fields:
        self._values[key] = value
    else:
        debug('%s does not support field: %s, but PE will ignore' % (
         self.__class__.__name__, key))


DictItem.__setitem__ = __setitem__
SETTINGS_PARAMS_MAP = {'REDIS_URL':'url', 
 'REDIS_HOST':'host', 
 'REDIS_PORT':'port', 
 'REDIS_ENCODING':'encoding', 
 'REDIS_SENTINELS':'sentinels'}

def get_redis_from_settings(settings):
    """Returns a redis client instance from given Scrapy settings object.

    This function uses ``get_client`` to instantiate the client and uses
    ``defaults.REDIS_PARAMS`` global as defaults values for the parameters. You
    can override them using the ``REDIS_PARAMS`` setting.

    Parameters
    ----------
    settings : Settings
        A scrapy settings object. See the supported settings below.

    Returns
    -------
    server
        Redis client instance.

    Other Parameters
    ----------------
    REDIS_URL : str, optional
        Server connection URL.
    REDIS_HOST : str, optional
        Server host.
    REDIS_PORT : str, optional
        Server port.
    REDIS_ENCODING : str, optional
        Data encoding.
    REDIS_PARAMS : dict, optional
        Additional client parameters.

    """
    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])
    return get_redis(**params)


def get_redis(**kwargs):
    """Returns a redis client instance.

    Parameters
    ----------
    redis_cls : class, optional
        Defaults to ``redis.StrictRedis``.
    url : str, optional
        If given, ``redis_cls.from_url`` is used to instantiate the class.
    **kwargs
        Extra parameters to be passed to the ``redis_cls`` class.

    Returns
    -------
    server
        Redis client instance.

    """
    sentiels = kwargs.pop('sentinels', None)
    if sentiels:
        from redis.sentinel import Sentinel
        master_name = kwargs.pop('master_name')
        sentiel = Sentinel(sentiels, **kwargs)
        master = sentiel.master_for(master_name)
        return master
    else:
        redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
        url = kwargs.pop('url', None)
        if url:
            return (redis_cls.from_url)(url, **kwargs)
        return redis_cls(**kwargs)


connection.get_redis = get_redis