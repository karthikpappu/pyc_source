# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/shaft/shaft/decorators.py
# Compiled at: 2017-01-27 03:22:43
# Size of source mod 2**32: 21167 bytes
import functools, inspect, copy
from flask import Response, jsonify, request, current_app, url_for, make_response
from werkzeug.wrappers import BaseResponse
from jinja2 import Markup
from dicttoxml import dicttoxml
from .core import Shaft, init_app, apply_function_to_members
from . import ext
from . import utils
import blinker, flask_cors
cache = ext.cache.cached
memoize = ext.cache.memoize
exempt_csrf = ext.csrf.exempt

def route(rule=None, **kwargs):
    """
    This decorator defines custom route for both class and methods in the view.
    It behaves the same way as Flask's @app.route

    on class:
        It takes the following args
            - rule: the root route of the endpoint
            - decorators: a list of decorators to run on each method

    on methods:
        along with the rule, it takes kwargs
            - endpoint
            - defaults
            - ...

    :param rule:
    :param kwargs:
    :return:
    """
    _restricted_keys = [
     'extends', 'route', 'decorators']

    def decorator(f):
        if inspect.isclass(f):
            extends = kwargs.pop('extends', None)
            if extends:
                if hasattr(extends, self.view_key):
                    for k, v in getattr(extends, self.view_key).items():
                        kwargs.setdefault(k, v)

            kwargs.setdefault('route', rule)
            kwargs['decorators'] = kwargs.get('decorators', []) + f.decorators
            setattr(f, '_route_extends__', kwargs)
            setattr(f, 'base_route', kwargs.get('route'))
            setattr(f, 'decorators', kwargs.get('decorators', []))
        else:
            if not rule:
                raise ValueError("'rule' is missing in @route ")
            for k in _restricted_keys:
                if k in kwargs:
                    del kwargs[k]

            (Shaft._bind_route_rule_cache)(f, rule=rule, **kwargs)
        return f

    return decorator


def _accept_method(methods, f):
    kw = {'append_method':True, 
     'methods':methods}
    (Shaft._bind_route_rule_cache)(f, rule=None, **kw)
    return f


def accept_get(f):
    """ Accept GET method """
    return _accept_method(['GET'], f)


def accept_post(f):
    """ Accept POST method """
    return _accept_method(['POST'], f)


def accept_post_get(f):
    """ Accept POST & GET method """
    return _accept_method(['POST', 'GET'], f)


def accept_delete(f):
    """ Accept DELETE method """
    return _accept_method(['DELETE'], f)


def accept_options(f):
    """ Accept OPTIONS method """
    return _accept_method(['OPTIONS'], f)


def accept_put(f):
    """ Accept PUT method """
    return _accept_method(['PUT'], f)


def template(page=None, layout=None, markup='html', **kwargs):
    """
    Decorator to change the view template and layout.

    It works on both Shaft class and view methods

    on class
        only $layout and markup are applied, everything else will be passed to the kwargs
        Using as first argument, it will be the layout.

        :first arg or $layout: The layout to use for that view
        :param layout: The layout to use for that view
        :param markup: the markup to use, by default it's html, can switch to jade.
        this will attach it to template_markup
        :param kwargs:
            get pass to the TEMPLATE_CONTEXT

    ** on method that return a dict
        page or layout are optional

        :param page: The html page
        :param layout: The layout to use for that view

        :param kwargs:
            get pass to the view as k/V

    ** on other methods that return other type, it doesn't apply

    :return:
    """
    pkey = '_template_extends__'

    def decorator(f):
        if inspect.isclass(f):
            layout_ = layout or page
            extends = kwargs.pop('extends', None)
            if extends:
                if hasattr(extends, pkey):
                    items = getattr(extends, pkey).items()
                    if 'layout' in items:
                        layout_ = items.pop('layout')
                    for k, v in items:
                        kwargs.setdefault(k, v)

            if not layout_:
                layout_ = 'layout.html'
            kwargs.setdefault('brand_name', '')
            kwargs['layout'] = layout_
            setattr(f, pkey, kwargs)
            setattr(f, 'base_layout', kwargs.get('layout'))
            setattr(f, 'template_markup', markup or 'html')
            f.g(TEMPLATE_CONTEXT=kwargs)
            return f
        else:

            @functools.wraps(f)
            def wrap(*args2, **kwargs2):
                response = f(*args2, **kwargs2)
                if isinstance(response, dict) or response is None:
                    response = response or {}
                    if page:
                        response.setdefault('_template', page)
                    if layout:
                        response.setdefault('_layout', layout)
                    for k, v in kwargs.items():
                        response.setdefault(k, v)

                return response

            return wrap

    return decorator


def _normalize_response_tuple(tuple_):
    """
    Helper function to normalize view return values .
    It always returns (dict, status, headers). Missing values will be None.
    For example in such cases when tuple_ is
      (dict, status), (dict, headers), (dict, status, headers),
      (dict, headers, status)

    It assumes what status is int, so this construction will not work:
    (dict, None, headers) - it doesn't make sense because you just use
    (dict, headers) if you want to skip status.
    """
    v = tuple_ + (None, ) * (3 - len(tuple_))
    if isinstance(v[1], int):
        return v
    else:
        return (v[0], v[2], v[1])


__view_parsers = set()

def view_parser(f):
    """
    A simple decorator to to parse the data that will be rendered
    :param func:
    :return:
    """
    __view_parsers.add(f)
    return f


def _build_response(data, renderer=None):
    """
    Build a response using the renderer from the data
    :return:
    """
    if isinstance(data, Response) or isinstance(data, BaseResponse):
        return data
    else:
        if not renderer:
            raise AttributeError(' Renderer is required')
        else:
            if isinstance(data, dict) or data is None:
                data = {} if data is None else data
                for _ in __view_parsers:
                    data = _(data)

                return (
                 renderer(data), 200)
            if isinstance(data, tuple):
                data, status, headers = _normalize_response_tuple(data)
                for _ in __view_parsers:
                    data = _(data)

                return (
                 renderer(data or {}), status, headers)
        return data


json_renderer = lambda i, data: _build_response(data, jsonify)
xml_renderer = lambda i, data: _build_response(data, dicttoxml)

def render_json(func):
    """
    Decorator to render as JSON
    :param func:
    :return:
    """
    if inspect.isclass(func):
        apply_function_to_members(func, json)
        return func
    else:

        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            data = func(*args, **kwargs)
            return _build_response(data, jsonify)

        return decorated_view


def render_xml(func):
    """
    Decorator to render as XML
    :param func:
    :return:
    """
    if inspect.isclass(func):
        apply_function_to_members(func, xml)
        return func
    else:

        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            data = func(*args, **kwargs)
            return _build_response(data, dicttoxml)

        return decorated_view


def render_jsonp(func):
    """Wraps JSONified output for JSONP requests.
    http://flask.pocoo.org/snippets/79/
    """

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        callback = request.args.get('callback', None)
        if callback:
            data = str(func(*args, **kwargs))
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_view


class MenuNavigation(object):
    __doc__ = "\n    MenuNavigation is class decorator to build page menu while building the enpoints\n\n    Decorator to build navigation menu directly on the methods\n    By default it will build the menu of the module, class an method\n    If the class is also decorated, it will use the menu _name as the top level _name\n\n    :param title: The menu title\n    :param kwargs: extra options to pass into the menu or to move the menu somewhere else\n\n        order int: The order of the menu in the set\n\n        visible (list of bool or callback): To hide and show menu. Accepts bool or\n                    list of callback function the callback function must return\n                    a bool to check if all everything is True to show or will be False\n                    ** When this menu is inside of a menu set, or has parent, if you want\n                    that page to be activated, but don't want to create a menu link,\n                    for example: a blog read page, set show to False. It will know\n                    the menu set is active\n\n        endpoint string: By default the endpoint is built based on the method and class.\n                    When set it will be used instead\n\n        endpoint_kwargs dict: dict of k/v data for enpoint\n\n        group_name str: On class menu, it can be used to filter a menu set to display.\n                    If a class is passed, it will try to inherit the group from that class\n\n        The args below will allow you to change where the menu is placed.\n        By default they are set automatically\n\n        module_: the module _name. Usually if using another module\n        class_: the class _name class _name in the module\n        method_: The method _name, to build endpoint. Changing this will change the url\n\n        extends: class Name. To use the extends of the class\n\n        some other kwargs:\n            url\n            target\n            fa_icon\n            align_right\n            show_profile_avatar\n            show_profile_name\n            css_class\n            css_id\n    :return:\n    "
    _title_map = {}

    def __call__(self, title, **kwargs):

        def wrap(f):
            if title:
                module_ = kwargs.pop('module_', f.__module__)
                class_ = kwargs.pop('class_', inspect.stack()[1][3])
                method_ = kwargs.pop('method_', f.__name__)
                is_class_ = inspect.isclass(f)
                extends = kwargs.pop('extends', None)
                if extends:
                    if is_class_:
                        extendscls = self.get(extends)
                        if extendscls:
                            if 'kwargs' in extendscls:
                                if 'group_name' not in kwargs:
                                    kwargs['group_name'] = extendscls['kwargs']['group_name']
                                if 'visible' not in kwargs:
                                    kwargs['visible'] = extendscls['kwargs']['visible']
                    else:
                        if 'endpoint' not in kwargs:
                            endpoint = '%s:%s' % (class_, f.__name__)
                            kwargs['endpoint'] = endpoint
                    module_ = extends.__module__
                    class_ = extends.__name__
                kwargs.setdefault('key', class_)
                (self._push)(module_=module_, class_=class_, 
                 method_=method_, 
                 title=title, 
                 is_class_=is_class_, **kwargs)
            return f

        return wrap

    def __init__(self):
        self.MENU = {}

    def add(self, title, extends, **kwargs):
        """
        To manually add a extends. Usually, menu by hand which
        may not be attached to any functions
        :param title:
        :param cls:
        :param method_:
        :param is_class_:
        :param kwargs:
        :return:
        """
        f = extends
        (self._push)(title=title, module_=f.__module__, 
         class_=f.__name__, 
         method_=f.__name__, 
         is_class_=False, **kwargs)

    def clear(self):
        self.MENU = {}

    def _push(self, **kwargs):
        module_ = kwargs.pop('module_')
        class_ = kwargs.pop('class_')
        method_ = kwargs.pop('method_')
        is_class_ = kwargs.pop('is_class_')
        _MenuNavigation__cls = method_ if is_class_ else class_
        path = '%s.%s' % (module_, _MenuNavigation__cls)
        if path not in self.MENU:
            self.MENU[path] = {'title':None,  'endpoint':None, 
             'endpoint_kwargs':{},  'order':None, 
             'sub_menu':[],  'kwargs':{}}
        if 'title' not in kwargs:
            raise TypeError("Missing 'title' in menu decorator")
        else:
            _endpoint = '%s:%s' % (_MenuNavigation__cls, 'index' if is_class_ else method_)
            kwargs['endpoint'] = kwargs.pop('endpoint', _endpoint)
            kwargs['endpoint_kwargs'] = kwargs.pop('endpoint_kwargs', {})
            order = kwargs.pop('order', 0)
            title = kwargs.pop('title')
            endpoint = kwargs.pop('endpoint')
            visible = kwargs.pop('visible', [True])
            if not isinstance(visible, list):
                visible = [
                 visible]
            kwargs['visible'] = visible
            kwargs['active'] = None
            kwargs['index'] = None
            kwargs['key'] = _MenuNavigation__cls
            if is_class_:
                kwargs['endpoint'] = endpoint
                kwargs['group_name'] = kwargs.pop('group_name', None)
                kwargs['has_submenu'] = True
                self.MENU[path]['title'] = title
                self.MENU[path]['order'] = order
                self.MENU[path]['kwargs'] = kwargs
            else:
                kwargs['has_submenu'] = False
                menu = (order, title, endpoint, kwargs)
                self.MENU[path]['sub_menu'].append(menu)
        self._title_map[endpoint] = title

    def _test_visibility(self, shows):
        if isinstance(shows, bool):
            return shows
        else:
            if not isinstance(shows, list):
                shows = [
                 shows]
            return all([x() if hasattr(x, '__call__') else x for x in shows])

    def get(self, cls):
        key = self.get_key(cls)
        return self.MENU[key]

    def get_key(self, cls):
        """
        Return the string key of the class
        :param cls: class
        :return: str
        """
        return '%s.%s' % (cls.__module__, cls.__name__)

    def get_extends(self, f):
        return dict(module_=(f.__module__), class_=(f.__name__))

    def render(self):
        menu_list = []
        menu_index = 0
        for _, menu in copy.deepcopy(self.MENU).items():
            menu_index += 1
            sub_menu = []
            menu['kwargs']['index'] = menu_index
            menu['kwargs']['active'] = False
            if 'visible' in menu['kwargs']:
                menu['kwargs']['visible'] = self._test_visibility(menu['kwargs']['visible'])
            for s in menu['sub_menu']:
                if s[2] == request.endpoint:
                    s[3]['active'] = True
                    menu['kwargs']['active'] = True
                s[3]['visible'] = self._test_visibility(s[3]['visible'])
                sub_menu.append(s)

            _kwargs = menu['kwargs']
            if menu['title']:
                menu_list.append((
                 menu['order'],
                 menu['title'],
                 sorted(sub_menu),
                 _kwargs))
            else:
                menu_list += sub_menu

        return sorted(menu_list)

    def init_app(self, app):

        def link_for(endpoint, props={}, **kwargs):
            url = url_for(endpoint, **kwargs)
            title = self._title_map.get(endpoint, '')
            props = ' '.join(["%s='%s'" % (k, v) for k, v in props.items()])
            a = "<a href='{url}' {props}>{title}</a>".format(title=title, url=url,
              props=props)
            return Markup(a)

        @app.context_processor
        def _():
            return dict(link_for=link_for)

        @app.before_request
        def p(*args, **kwargs):
            if request.endpoint not in ('static', None):
                Shaft.g(__NAV_MENU__=(nav_menu.render()))


nav_menu = MenuNavigation()
menu_title = nav_menu
init_app(nav_menu.init_app)

def cors(*args, **kwargs):
    """
    A wrapper around flask-cors cross_origin, to also act on classes

    **An extra note about cors, a response must be available before the
    cors is applied. Dynamic return is applied after the fact, so use the
    decorators, render_json, render_xml, or return self.render() for txt/html
    ie:
    @cors()
    class Index(Shaft):
        def index(self):
            return self.render()

        @render_json
        def json(self):
            return {}

    class Index2(Shaft):
        def index(self):
            return self.render()

        @cors()
        @render_json
        def json(self):
            return {}

    :return:
    """

    def decorator(fn):
        cors_fn = (flask_cors.cross_origin)(args, automatic_options=False, **kwargs)
        if inspect.isclass(fn):
            apply_function_to_members(fn, cors_fn)
        else:
            return cors_fn(fn)
        return fn

    return decorator


def headers(params={}):
    """This decorator adds the headers passed in to the response
    http://flask.pocoo.org/snippets/100/
    """

    def decorator(f):
        if inspect.isclass(f):
            h = headers(params)
            apply_function_to_members(f, h)
            return f
        else:

            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                resp = make_response(f(*args, **kwargs))
                h = resp.headers
                for header, value in params.items():
                    h[header] = value

                return resp

            return decorated_function

    return decorator


def noindex(f):
    """This decorator passes X-Robots-Tag: noindex
    http://flask.pocoo.org/snippets/100/
    """
    return headers({'X-Robots-Tag': 'noindex'})(f)


__signals_namespace = blinker.Namespace()

def emit_signal(sender=None, namespace=None):
    """
    @emit_signal
    A decorator to mark a method or function as a signal emitter
    :param sender: string  to be the sender.
    If empty, it will use the function __module__+__fn_name,
    or method __module__+__class_name__+__fn_name__
    :param namespace: The namespace. If None, it will use the global namespace
    :return:
    """
    if not namespace:
        namespace = __signals_namespace

    def decorator(fn):
        fname = sender
        if not fname:
            fnargs = inspect.getargspec(fn).args
            fname = fn.__module__
            if 'self' in fnargs or 'cls' in fnargs:
                caller = inspect.currentframe().f_back
                fname += '_' + caller.f_code.co_name
            fname += '__' + fn.__name__
        fn.pre = namespace.signal('pre_%s' % fname)
        fn.post = namespace.signal('post_%s' % fname)

        def send(action, *a, **kw):
            sig_name = '%s_%s' % (action, fname)
            result = kw.pop('result', None)
            kw.update((inspect.getcallargs)(fn, *a, **kw))
            sendkw = {k:v for k, v in kw.items() if k in kw.keys()}
            sendkw['emitter'] = sendkw.pop('self', sendkw.pop('cls', kw.get('self', kw.get('cls', fn))))
            if action == 'post':
                sendkw['result'] = result
            (namespace.signal(sig_name).send)(fname, **sendkw)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            send('pre', *args, **kwargs)
            result = fn(*args, **kwargs)
            kwargs['result'] = result
            send('post', *args, **kwargs)
            return result

        return wrapper

    return decorator