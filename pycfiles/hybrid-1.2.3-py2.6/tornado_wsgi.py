# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/wsgi_app/tornado_wsgi.py
# Compiled at: 2016-01-09 10:34:11
from tornado.web import RequestHandler
from tornado.wsgi import WSGIApplication
from .base_wsgi import BaseWSGI

class TornadoWSGI(BaseWSGI):

    def __init__(self, *a, **kw):
        BaseWSGI.__init__(self)
        self._wsgi_app = WSGIApplication(*a, **kw)

    def __getattr__(self, attr):
        if hasattr(self._wsgi_app, attr):
            return getattr(self._wsgi_app, attr)
        raise AttributeError("instance of `%s' has no attribute: %s" % (
         self.__class__.__name__, attr))

    def route(self, uri, host_pattern='.*$'):
        if not isinstance(uri, str):
            raise TypeError('expected string or buffer')

        def _inner(handler_class):
            if not issubclass(handler_class, RequestHandler):
                raise RuntimeError('expected subclass of RequestHandler')
            self._wsgi_app.add_handlers(host_pattern, [
             (
              uri, handler_class)])
            handler_class.__register_app__ = self
            return handler_class

        return _inner

    def reflect_uri(self):
        uris = []
        for (_, urlspecs) in self._wsgi_app.handlers:
            for urlspec in urlspecs:
                uris.append(urlspec.regex.pattern)

        return uris