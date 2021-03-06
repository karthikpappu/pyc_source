# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mbe/cherrypy.py
# Compiled at: 2015-11-03 03:02:45
# Size of source mod 2**32: 5248 bytes
"""
    The CherryPy-module provides a web server plugin for CherryPy.
"""
from http.cookies import SimpleCookie
import cherrypy
from decorator import decorator
from mbe.authentication import check_session, login, AuthenticationError, logout
from mbe.node import Node
__author__ = 'Nicklas Borjesson'

def _check_session_aspect(func, *args, **kwargs):
    """CherryPy-specific check_session aspect code, checks if there is a valid cookie"""
    try:
        _session_id = cherrypy.request.cookie['session_id'].value
    except:
        raise AuthenticationError('Authentication aspect for "' + func.__name__ + '": No session_id cookie')

    kwargs['user'] = check_session(_session_id)
    kwargs['session_id'] = _session_id
    return func(*args, **kwargs)


def aop_check_session(f):
    """
    CherryPy-specific session checking decorator.

    :param f: the function

    """
    print('aop_check_session')
    return decorator(_check_session_aspect, f)


def _login_json_aspect(func, *args, **kwargs):
    """
    CherryPy-specific session login aspect.

    """
    _message = cherrypy.request.json
    if _message is not None and isinstance(_message, dict):
        if 'credentials' not in _message:
            raise AuthenticationError('_login_json_aspect for "' + func.__name__ + '": No credentials in request')
        if 'session_id' in cherrypy.request.cookie:
            if cherrypy.request.cookie['session_id'].value != '':
                print('_login_json_aspect: Logging out old session: ' + cherrypy.request.cookie['session_id'].value)
                logout(cherrypy.request.cookie['session_id'].value)
        _session_id, _user = login(_message['credentials'])
        _session_cookie = cherrypy.response.cookie
        _session_cookie['session_id'] = _session_id
        _session_cookie['session_id']['secure'] = True
        _session_cookie['session_id']['path'] = '/'
        kwargs['message'] = _message
        kwargs['session_id'] = _session_id
        kwargs['user'] = _user
        return func(*args, **kwargs)
    raise AuthenticationError('Authentication aspect for "' + func.__name__ + '": No message structure')


def aop_login_json(f):
    """
    CherryPy-specific session login decorator.

    """
    return decorator(_login_json_aspect, f)


class CherryPyNode(object):
    __doc__ = '\n    The CherryPyNode class is a plugin for CherryPy to expose the MBE node-functionality.\n    Each function maps to counterparts in the node class.\n\n    '
    _node = None

    def __init__(self, _database_access):
        self._node = Node(_database_access)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_login_json
    def login(self, **kwargs):
        return {}

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json')
    def logout(self, **kwargs):
        if 'session_id' in cherrypy.request.cookie:
            logout(cherrypy.request.cookie['session_id'].value)
            cherrypy.response.cookie['session_id'] = SimpleCookie()
            cherrypy.response.cookie['session_id']['expires'] = 0
        return {}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def save(self, **kwargs):
        return self._node.save(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def find(self, **kwargs):
        return self._node.find(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def lookup(self, **kwargs):
        return self._node.lookup(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def remove(self, **kwargs):
        return self._node.remove(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def load_node(self, **kwargs):
        return self._node.load_node(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def load_children(self, **kwargs):
        return self._node.load_children(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def history(self, **kwargs):
        return self._node.history(cherrypy.request.json, kwargs['user'])

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json')
    @aop_check_session
    def get_schemas(self, **kwargs):
        return self._node.get_schemas(kwargs['user'])