# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/wheezy/akara_adapter.py
# Compiled at: 2013-05-10 23:47:26
from wheezy.http import CacheProfile
from wheezy.caching.patterns import Cached
from wheezy.http import WSGIApplication
from wheezy.caching.memcache import MemcachedClient
from wheezy.http.cache import etag_md5crc32
from wheezy.http import bootstrap_http_defaults
from wheezy.http import bootstrap_http_defaults
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.http.middleware import environ_cache_adapter_middleware_factory
from wheezy.http.middleware import wsgi_adapter_middleware_factory
from datetime import timedelta

class AkaraCachingWsgiWrapper(object):

    def __init__(self, cache_location='public', static_dependency=None, queries=None, ttl=15, debug=False, max_age=None, memcache_socket='unix:/tmp/memcached.sock'):
        assert cache_location in ('none', 'server', 'client', 'public')
        self.cache = MemcachedClient([memcache_socket])
        self.cache_location = cache_location
        self.debug = debug
        self.cached = Cached(self.cache, time=ttl)
        self.static_dependency = static_dependency
        self.max_age = max_age
        self.cache_profile = CacheProfile(cache_location, vary_query=queries, enabled=True, etag_func=etag_md5crc32, duration=timedelta(seconds=ttl))

    def __call__(self, akara_application):
        """
        Called by Akara to provide the akara application
        as a WSGI application to be 'wrapped'
        """
        self.akara_application = akara_application

        def wsgi_wrapper(environ, start_response):
            if self.cache_location != 'none':
                environ['wheezy.http.cache_profile'] = self.cache_profile

            def InvalidateCacheViaDependency(cacheName):
                if self.debug:
                    print 'invalidating cache: ', cacheName
                self.cached.delete(cacheName)

            environ['akamu.wheezy.invalidate'] = InvalidateCacheViaDependency
            if self.debug:
                print 'Calling akara application from wheezy.http'
            rt = akara_application(environ, start_response)
            if 'wheezy.http.cache_dependency' in environ:
                if not isinstance(environ['wheezy.http.cache_dependency'], list):
                    raise ValueError('wheezy.http.cache_dependency must be set to a list')
                if self.debug:
                    print 'Dependency key(s): ', environ['wheezy.http.cache_dependency']
            elif self.static_dependency:
                environ['wheezy.http.cache_dependency'] = self.static_dependency if isintance(self.static_dependency) else [
                 self.static_dependency]
                if self.debug:
                    print 'Dependency key(s): ', self.static_dependency
            if self.max_age is not None:
                policy = self.cache_profile.cache_policy()
                policy.max_age(self.max_age)
                policy.etag(self.cache_profile.etag_func(rt))
            return rt

        return WSGIApplication([
         bootstrap_http_defaults,
         http_cache_middleware_factory,
         environ_cache_adapter_middleware_factory,
         wsgi_adapter_middleware_factory], {'wsgi_app': wsgi_wrapper, 
           'http_cache': self.cache})