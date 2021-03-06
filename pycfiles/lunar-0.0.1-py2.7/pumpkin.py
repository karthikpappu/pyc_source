# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pumpkin/pumpkin.py
# Compiled at: 2014-12-15 19:29:13
"""
Pumpkin. A simple WSGI based webframework for learning.

Pumpkin是一个玩具式的网络框架，基于PEP333和它的进化版PEP3333，它包括一个Router，
一个Template engine，一个简单的WSGI Request和Response的封装，没有任何第三方包的依赖。
项目会不断的演化，在你看到这句话的时候，这个项目还是千疮百孔，下一步会修复很多bug，
重构一些代码，可能会加入基于epoll或者select的异步请求支持。

查看example来看看这是怎么运作的。

Pumpkin is a WSGI based webframework in pure Python, without any third-party dependency.
Pumpkin include a simple router, which provide the request routing, a template engine
for template rendering, a simple wrapper for WSGI request and response.

Happy hacking.

About pumpkin：

洋葱、萝卜和番茄不相信世界上有南瓜这个东西，它们认为那只是空想。南瓜默默不说话，它只是继续成长。
这句话来自《当世界年纪还小的时候》这本书的封底，希望我们都能成长为一只大大的南瓜。

"""
import os, time, sys, traceback, threading, mimetypes
from functools import wraps
if sys.version < '3':
    from Queue import Queue
    from urllib import quote
else:
    from queue import Queue
    from urllib.parse import quote
try:
    import pkg_resources
    pkg_resources.resource_stream
except (ImportError, AttributeError):
    pkg_resources = None

from .server import ServerAdapter
from .server import WSGIRefServer
from .template import Loader, unescape
from .wrappers import Request, Response
from .router import Router, RouterException

class _Stack(threading.local):

    def __init__(self):
        self._Stack = []

    def push(self, app):
        self._Stack.append(app)

    def pop(self):
        try:
            self._Stack.pop()
        except IndexError:
            return

        return

    def top(self):
        try:
            return self._Stack[(-1)]
        except IndexError:
            return

        return

    def __len__(self):
        return len(self._Stack)

    def empty(self):
        if len(self._Stack) == 0:
            return True
        return False

    def __repr__(self):
        return '_app_stack with %s applications' % len(self)


class PumpkinException(Exception):

    def __init__(self, code, response, server_handler, DEBUG=False):
        self._DEBUG = DEBUG
        self._response = response
        self._response.set_status(code)
        self._server_handler = server_handler

    def __call__(self):
        body = self._response.status
        if self._DEBUG:
            body = ('<br>').join([
             self._response.status, traceback.format_exc().replace('\n', '<br>')])
        self._response.set_body(body)
        self._server_handler(self._response.status, self._response.headerlist)
        return [self._response.body]


class Pumpkin(object):
    """Main object of this funny web frameWork
    """

    def __init__(self, pkg_name, template='template', static='static'):
        global app_stack
        self._router = Router()
        self._request = Request()
        self._response = Response(None)
        self.package_name = pkg_name
        self.root_path = self._get_package_path(self.package_name).replace('\\', '\\\\')
        self.loader = Loader(os.sep.join([self.root_path, template]))
        self.static_folder = static
        self.static_url_cache = {}
        self._session = self._request.cookies
        self._req_arg_queue = Queue()
        self._server_handler = None
        self.DEBUG = False
        self.config = {}
        self.config.setdefault('DATABASE_NAME', 'pumpkin.db')
        app_stack.push(self)
        return

    def set_template_engine(self, engine):
        self.loader.update_template_engine(engine)

    def _get_package_path(self, name):
        """Returns the path to a package or cwd if that cannot be found."""
        try:
            return os.path.abspath(os.path.dirname(sys.modules[name].__file__))
        except (KeyError, AttributeError):
            return os.getcwd()

    def route(self, path=None, methods=['GET']):
        if path is None:
            raise RouterException()
        methods = [ m.upper() for m in methods ]

        def wrapper(fn):
            self._router.register(path, fn, methods)
            return fn

        return wrapper

    @property
    def session(self):
        return self._session

    def run(self, server=WSGIRefServer, host='localhost', port=8000, DEBUG=False):
        self.DEBUG = DEBUG
        if isinstance(server, type) and issubclass(server, ServerAdapter):
            server = server(host=host, port=port)
        if not isinstance(server, ServerAdapter):
            raise RuntimeError('Server must be a subclass of ServerAdapter.')
        print 'running on %s:%s' % (host, port)
        try:
            server.run(self)
        except KeyboardInterrupt:
            pass

    def render_template(self, file, **context):
        app_namespace = sys.modules[self.package_name].__dict__
        context.update(globals())
        context.update(app_namespace)
        return self.loader.load(file).render(**context)

    def not_found(self):
        response = Response(body='<h1>404 Not Found</h1>', code=404)
        return response

    def not_modified(self):
        response = Response('', code=304)
        del response.headers['Content-Type']
        return response

    def redirect(self, location, code=302):
        response = Response(body='<p>Redirecting...</p>', code=code)
        response.headers['Location'] = location
        return response

    def url_for(self, fn, filename=None, **kwargs):
        if fn == self.static_folder and filename:
            if filename in self.static_url_cache.keys():
                return self.static_url_cache[filename]
            else:
                url = self.construct_url(filename)
                self.static_url_cache[filename] = url
                return url

        if kwargs:
            return self._router.url_for(fn, **kwargs)
        return self._router.url_for(fn)

    def construct_url(self, filename):
        environ = self._request.headers
        url = environ['wsgi.url_scheme'] + '://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']
            if environ['wsgi.url_scheme'] == 'https':
                if environ['SERVER_PORT'] != '443':
                    url += ':' + environ['SERVER_PORT']
            elif environ['SERVER_PORT'] != '80':
                url += ':' + environ['SERVER_PORT']
        url += quote(environ.get('SCRIPT_NAME', ''))
        if environ.get('QUERY_STRING'):
            url += '?' + environ['QUERY_STRING']
        url += '/' + ('/').join([self.static_folder, filename])
        return url

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response

    def handle_static(self, path):
        response = Response(None)
        path = self.root_path + path
        if not os.path.exists(path) or not os.path.isfile(path):
            return self.not_found()
        else:
            mimetype = 'text/plain'
            guess_type = mimetypes.guess_type(path)[0]
            if guess_type:
                response.set_content_type(guess_type)
            else:
                response.set_content_type(mimetype)
            stats = os.stat(path)
            last_modified_time = time.gmtime(stats.st_mtime)
            last_modified_str = time.strftime('%a, %d %b %Y %H:%M:%S UTC', last_modified_time)
            if_modified_since_str = self._request.if_modified_since
            if if_modified_since_str:
                if_modified_since_time = time.strptime(if_modified_since_str, '%a, %d %b %Y %H:%M:%S %Z')
                if if_modified_since_time >= last_modified_time:
                    return self.not_modified()
            if 'Last-Modified' not in response.headers.keys():
                response.headers['Last-Modified'] = last_modified_str
            with open(path, 'r') as (f):
                response.set_body(body=f.read())
            return response

    def handle_router(self):
        try:
            handler, args = self._router.get(self._request.path, self._request.method)
        except TypeError:
            return self.not_found()

        if args:
            r = handler(**args)
        else:
            r = handler()
        return r

    def __call__(self, environ, start_response):
        self._response = Response(None)
        self._request = Request(None)
        self._server_handler = start_response
        self._request.bind(environ)
        r = None
        if self._request.path is not None and self._request.path.lstrip('/').startswith(self.static_folder):
            r = self.handle_static(self._request.path)
        else:
            try:
                r = self.handle_router()
            except Exception as e:
                return PumpkinException(500, self._response, self._server_handler, self.DEBUG)()

        if isinstance(r, Response):
            self._response = r
            self._server_handler(r.status, r.headerlist)
            return [
             r.body]
        else:
            self._response.set_body(body=r)
            self._response.set_status(200)
            start_response(self._response.status, self._response.headerlist)
            return [self._response.body]


app_stack = _Stack()
default_app = app_stack.top()
if not default_app:
    default_app = Pumpkin('/')
request = app_stack.top().request
response = app_stack.top().response
session = app_stack.top().session