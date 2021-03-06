# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/xmlclient.py
# Compiled at: 2007-12-02 16:26:58
import xmlrpclib
from salamoia.h2o.logioni import *
from salamoia.h2o.protocols import NO_ADAPTER_NEEDED
from salamoia.h2o.config import Config
from threading import Lock
import traceback, base64, urllib, string, sre, zlib

class ClientCredentialsMetaclass(type):
    __module__ = __name__

    def __init__(cls, name, bases, dict):
        super(ClientCredentialsMetaclass, cls).__init__(name, bases, dict)
        if hasattr(cls, 'methodName'):
            cls.methodMap[cls.methodName] = cls


class ClientCredentials(object):
    __module__ = __name__
    __metaclass__ = ClientCredentialsMetaclass
    methodMap = {}

    def encode(self):
        raise NotImplementedError

    @classmethod
    def authenticateWithMethod(cls, method, base, username, password, headers):
        if method in Config.defaultConfig().getlist('security', 'disabledAuthenticationMethods'):
            return False
        cred = cls.methodMap.get(method)
        if cred:
            return cred.authenticate(base, username, password, headers)
        return False

    @classmethod
    def authenticate(cls, base, username, password, headers):
        credentials = cls.authenticationCredentials(base, username, password, headers)
        proxy = Proxy(base=base, credentials=credentials)
        try:
            proxy.connectionAuthenticationCheck()
            return credentials
        except xmlrpclib.ProtocolError, error:
            pass

        return


class BasicClientCredentials(ClientCredentials):
    __module__ = __name__
    methodName = 'Basic'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def encode(self):
        auth = base64.encodestring(urllib.unquote('%s:%s' % (self.username, self.password)))
        auth = string.join(string.split(auth), '')
        return 'Basic ' + auth

    @classmethod
    def authenticationCredentials(cls, base, username, password, headers):
        return cls(username, password)


class TokenClientCredentials(ClientCredentials):
    __module__ = __name__

    def __init__(self, token):
        self.token = token

    def encode(self):
        auth = self.token
        auth = string.join(string.split(auth), '')
        return 'Token ' + auth


class SSHClientCredentials(TokenClientCredentials):
    __module__ = __name__
    methodName = 'SSH'

    @classmethod
    def authenticationCredentials(cls, base, username, password, headers):
        from Crypto.Util.randpool import RandomPool
        import paramiko, base64, urlparse
        baseRoot = urlparse.urljoin(base, '/')
        ch = headers['challenge']
        key = paramiko.Agent().get_keys()[0]
        sig = base64.encodestring(key.sign_ssh_data(RandomPool(), ch)).replace('\n', '')
        proxy = Proxy(base=baseRoot, credentials=BasicClientCredentials('anonymous', 'unauthenticated'))
        if '@' not in username:
            username = username + '@' + headers['realm']
        proxy.authmanager.ssh.response(username, ch, sig)
        return cls(sig)


class Transport(xmlrpclib.Transport):
    __module__ = __name__
    _use_datetime = False
    user_agent = 'Salamoia xmlrpc'

    def __init__(self, proxy):
        self.proxy = proxy

    def get_host_info(self, host):
        (host, extra_headers, x509) = xmlrpclib.Transport.get_host_info(self, host)
        extra_headers = []
        if Config.defaultConfig().get('transport', 'encoding') == 'deflate':
            extra_headers.append(('Accept-Encoding', 'deflate'))
        if self.proxy._credentials:
            extra_headers.append(('Authorization', self.proxy._credentials.encode()))
        return (host, extra_headers, x509)

    def request(self, host, handler, request_body, verbose=0):
        """
        Replaces original method in order to implement gzip compression

        credits to http://orca.mojam.com/~skip/python/gzip-xmlrpc.txt

        NOTE: confusion!! this is actually the 'deflate' encoding
        see http://www.cherrypy.org/wiki/GzipFilter
        gzip uses some additional control words
        """
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        (errcode, errmsg, headers) = h.getreply()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(host + handler, errcode, errmsg, headers)
        self.verbose = verbose
        try:
            sock = h._conn.sock
        except AttributeError:
            sock = None

        try:
            content_encoding = headers['content-encoding']
            if content_encoding and content_encoding == 'deflate':
                return self.parse_response_gzip(h.getfile())
            elif content_encoding:
                raise xmlrpclib.ProtocolError(host + handler, 500, 'Unknown encoding type: %s' % content_encoding, headers)
            else:
                return self.parse_response(h.getfile())
        except KeyError:
            return self.parse_response(h.getfile())

        return

    def parse_response_gzip(self, f):
        dc = zlib.decompressobj()
        (p, u) = xmlrpclib.getparser()
        resp = []
        append = resp.append
        read = f.read
        while 1:
            response = read(8192)
            if not response:
                break
            append(response)

        response = dc.decompress(string.join(resp, ''))
        p.feed(response)
        rest = dc.flush()
        if rest:
            p.feed(rest)
        f.close()
        p.close()
        return u.close()


class Proxy(object):
    __module__ = __name__

    def __init__(self, name='', base='', parent=None, interfacePair=None, credentials=None):
        self._name = name
        self._base = base
        self._parent = parent
        if parent:
            self._authenticationCheckLock = self._parent._authenticationCheckLock
        else:
            self._authenticationCheckLock = Lock()
        if parent:
            self._interfacePair = parent._interfacePair
            self._credentials = parent._credentials
        else:
            if interfacePair is None:
                interfacePair = (
                 NO_ADAPTER_NEEDED, NO_ADAPTER_NEEDED)
            self._interfacePair = interfacePair
            self._credentials = credentials
        return

    def __getattr__(self, name):
        if name == '_connection':
            self._connection = xmlrpclib.Server(self._base, allow_none=True, transport=Transport(self))
            return self._connection
        if name == '_authenticationCheckLock':
            return self._authenticationCheckLock
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError, 'no such attribute'
        return Proxy(name, self._base + '/' + name, self)

    def __call__(self, *args):
        nativeArgs = self._interfacePair[0](args)
        try:
            res = getattr(self._parent._connection, self._name)(*nativeArgs)
        except xmlrpclib.ProtocolError:
            if self._authenticationCheckLock.locked():
                raise
            self._connect()
            res = getattr(self._parent._connection, self._name)(*nativeArgs)

        if res is None:
            return res
        return self._interfacePair[1](res)

    def _connect(self):
        """
        """
        if self._parent:
            self._parent._connect()


class Client(Proxy):
    """
    Compatibility interface
    """
    __module__ = __name__

    def _connect(self):
        base = self._base
        username = self._username
        password = self._password

        def explode(header):
            (method, args) = header.split(' ')
            args = dict([ sre.match('(.*)="(.*)"', x).groups() for x in args.split(',') ])
            return (
             method, args)

        headers = {}
        proxy = Proxy(base=base)
        try:
            proxy.connectionAuthenticationCheck()
        except xmlrpclib.ProtocolError, error:
            headers = dict([ explode(h) for h in error.headers.getheaders('WWW-Authenticate') ])

        methods = headers.keys()
        orderedMethods = ['SSH', 'GSSAPI', 'Basic']
        methods.sort(lambda x, y: cmp(orderedMethods.index(x), orderedMethods.index(y)))
        for m in methods:
            credentials = ClientCredentials.authenticateWithMethod(m, base, username, password, headers[m])
            if credentials:
                break

        self._credentials = credentials
        if not credentials:
            try:
                self._authenticationCheckLock.acquire()
                self.connectionAuthenticationCheck()
            finally:
                self._authenticationCheckLock.release()

    def __init__(self, host, port, timeout=-1.0, username=None, password=None, base='hostello', interfacePair=None):
        base = 'http://%s:%s/%s' % (host, port, base)
        self._username = username
        self._password = password
        super(Client, self).__init__(base=base, interfacePair=interfacePair, credentials=None)
        self._connect()
        return