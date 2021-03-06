# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/lib/authkit_adapter/authenticate/basic.py
# Compiled at: 2007-12-04 08:45:17
"""HTTP basic authentication middleware

This implementation is identical to the `paste.auth.basic
<http://pythonpaste.org/module-paste.auth.basic.html>`_ implemenation.

Note:: If users are prompted to sign in this also seems to have the effect of
    signing them out.

"""
from paste.httpexceptions import HTTPUnauthorized
from paste.httpheaders import *
from authkit.authenticate.multi import MultiHandler, status_checker
from authproxy.lib.authkit_adapter.authenticate import get_template, valid_password, get_authenticate_function, strip_base, RequireEnvironKey, AuthKitUserSetter, AuthKitAuthHandler
from authkit.permissions import AuthKitConfigError

class AuthBasicAuthenticator(object):
    """
    implements ``Basic`` authentication details
    """
    type = 'basic'

    def __init__(self, realm, authfunc):
        self.realm = realm
        self.authfunc = authfunc

    def build_authentication(self):
        head = WWW_AUTHENTICATE.tuples('Basic realm="%s"' % self.realm)
        return HTTPUnauthorized(headers=head)

    def authenticate(self, environ):
        authorization = AUTHORIZATION(environ)
        if not authorization:
            return self.build_authentication()
        (authmeth, auth) = authorization.split(' ', 1)
        if 'basic' != authmeth.lower():
            return self.build_authentication()
        auth = auth.strip().decode('base64')
        (username, password) = auth.split(':', 1)
        if self.authfunc(environ, username, password):
            return username
        return self.build_authentication()

    __call__ = authenticate


class BasicAuthHandler(AuthKitAuthHandler):
    """
    HTTP/1.0 ``Basic`` authentication middleware

    Parameters:

        ``application``

            The application object is called only upon successful
            authentication, and can assume ``environ['REMOTE_USER']``
            is set.  If the ``REMOTE_USER`` is already set, this
            middleware is simply pass-through.

        ``realm``

            This is a identifier for the authority that is requesting
            authorization.  It is shown to the user and should be unique
            within the domain it is being used.

        ``authfunc``

            This is a mandatory user-defined function which takes a
            ``username`` and ``password`` for its first and second
            arguments respectively.  It should return ``True`` if
            the user is authenticated.

    """

    def __init__(self, application, realm, authfunc):
        self.application = application
        self.authenticate = AuthBasicAuthenticator(realm, authfunc)

    def __call__(self, environ, start_response):
        if environ.has_key('authkit.multi'):
            authenitcation = self.authenticate.build_authentication()
            return authenitcation.wsgi_application(environ, start_response)
        else:
            result = self.authenticate(environ)
            return result.wsgi_application(environ, start_response)


class BasicUserSetter(AuthKitUserSetter):

    def __init__(self, application, realm, authfunc, users):
        self.application = application
        self.users = 'WSGI'
        self.authenticate = AuthBasicAuthenticator(realm, authfunc)

    def __call__(self, environ, start_response):
        if not self.users == 'WSGI':
            environ['authkit.users'] = self.users
        result = self.authenticate(environ)
        if isinstance(result, str):
            AUTH_TYPE.update(environ, 'basic')
            REMOTE_USER.update(environ, result)
        return self.application(environ, start_response)


def load_basic_config(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.basic'):
    auth_handler_params = {}
    user_setter_params = {}
    authenticate_conf = strip_base(auth_conf, 'authenticate.')
    (app, authfunc, users) = get_authenticate_function(app, authenticate_conf, prefix=prefix + 'authenticate.', format='basic')
    realm = auth_conf.get('realm', 'AuthKit')
    auth_handler_params['realm'] = realm
    auth_handler_params['authfunc'] = authfunc
    user_setter_params['realm'] = realm
    user_setter_params['authfunc'] = authfunc
    user_setter_params['users'] = users
    return (app, auth_handler_params, user_setter_params)


def make_basic_auth_handler(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.basic'):
    (app, auth_handler_params, user_setter_params) = load_basic_config(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.basic')
    app = MultiHandler(app)
    app.add_method('basic', BasicAuthHandler, auth_handler_params['realm'], auth_handler_params['authfunc'])
    app.add_checker('basic', status_checker)
    app = BasicUserSetter(app, user_setter_params['realm'], user_setter_params['authfunc'], user_setter_params['users'])
    return app


AuthBasicHandler = BasicAuthHandler
middleware = BasicAuthHandler
TryToAddUsername = BasicUserSetter
make_basic_handler = make_basic_auth_handler