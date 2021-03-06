# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/redis/connection.py
# Compiled at: 2019-07-06 06:05:05
# Size of source mod 2**32: 37280 bytes
from __future__ import with_statement
from distutils.version import StrictVersion
from itertools import chain
from select import select
import os, socket, sys, threading, warnings
try:
    import ssl
    ssl_available = True
except ImportError:
    ssl_available = False

from redis._compat import b, xrange, imap, byte_to_chr, unicode, bytes, long, BytesIO, nativestr, basestring, iteritems, LifoQueue, Empty, Full, urlparse, parse_qs, unquote
from redis.exceptions import RedisError, ConnectionError, TimeoutError, BusyLoadingError, ResponseError, InvalidResponse, AuthenticationError, NoScriptError, ExecAbortError, ReadOnlyError
from redis.utils import HIREDIS_AVAILABLE
if HIREDIS_AVAILABLE:
    import hiredis
    hiredis_version = StrictVersion(hiredis.__version__)
    HIREDIS_SUPPORTS_CALLABLE_ERRORS = hiredis_version >= StrictVersion('0.1.3')
    HIREDIS_SUPPORTS_BYTE_BUFFER = hiredis_version >= StrictVersion('0.1.4')
    if not HIREDIS_SUPPORTS_BYTE_BUFFER:
        msg = "redis-py works best with hiredis >= 0.1.4. You're running hiredis %s. Please consider upgrading." % hiredis.__version__
        warnings.warn(msg)
else:
    HIREDIS_USE_BYTE_BUFFER = True
    if HIREDIS_SUPPORTS_BYTE_BUFFER:
        if sys.version_info[0] == 2:
            if sys.version_info[1] < 7:
                HIREDIS_USE_BYTE_BUFFER = False
        SYM_STAR = b('*')
        SYM_DOLLAR = b('$')
        SYM_CRLF = b('\r\n')
        SYM_EMPTY = b('')
        SERVER_CLOSED_CONNECTION_ERROR = 'Connection closed by server.'

        class Token(object):
            __doc__ = '\n    Literal strings in Redis commands, such as the command names and any\n    hard-coded arguments are wrapped in this class so we know not to apply\n    and encoding rules on them.\n    '

            def __init__(self, value):
                if isinstance(value, Token):
                    value = value.value
                self.value = value

            def __repr__(self):
                return self.value

            def __str__(self):
                return self.value


        class BaseParser(object):
            EXCEPTION_CLASSES = {'ERR':{'max number of clients reached': ConnectionError}, 
             'EXECABORT':ExecAbortError, 
             'LOADING':BusyLoadingError, 
             'NOSCRIPT':NoScriptError, 
             'READONLY':ReadOnlyError}

            def parse_error(self, response):
                """Parse an error response"""
                error_code = response.split(' ')[0]
                if error_code in self.EXCEPTION_CLASSES:
                    response = response[len(error_code) + 1:]
                    exception_class = self.EXCEPTION_CLASSES[error_code]
                    if isinstance(exception_class, dict):
                        exception_class = exception_class.get(response, ResponseError)
                    return exception_class(response)
                return ResponseError(response)


        class SocketBuffer(object):

            def __init__(self, socket, socket_read_size):
                self._sock = socket
                self.socket_read_size = socket_read_size
                self._buffer = BytesIO()
                self.bytes_written = 0
                self.bytes_read = 0

            @property
            def length(self):
                return self.bytes_written - self.bytes_read

            def _read_from_socket(self, length=None):
                socket_read_size = self.socket_read_size
                buf = self._buffer
                buf.seek(self.bytes_written)
                marker = 0
                try:
                    while True:
                        data = self._sock.recv(socket_read_size)
                        if isinstance(data, bytes):
                            if len(data) == 0:
                                raise socket.error(SERVER_CLOSED_CONNECTION_ERROR)
                        buf.write(data)
                        data_length = len(data)
                        self.bytes_written += data_length
                        marker += data_length
                        if length is not None:
                            if length > marker:
                                continue
                        break

                except socket.timeout:
                    raise TimeoutError('Timeout reading from socket')
                except socket.error:
                    e = sys.exc_info()[1]
                    raise ConnectionError('Error while reading from socket: %s' % (
                     e.args,))

            def read(self, length):
                length = length + 2
                if length > self.length:
                    self._read_from_socket(length - self.length)
                self._buffer.seek(self.bytes_read)
                data = self._buffer.read(length)
                self.bytes_read += len(data)
                if self.bytes_read == self.bytes_written:
                    self.purge()
                return data[:-2]

            def readline(self):
                buf = self._buffer
                buf.seek(self.bytes_read)
                data = buf.readline()
                while not data.endswith(SYM_CRLF):
                    self._read_from_socket()
                    buf.seek(self.bytes_read)
                    data = buf.readline()

                self.bytes_read += len(data)
                if self.bytes_read == self.bytes_written:
                    self.purge()
                return data[:-2]

            def purge(self):
                self._buffer.seek(0)
                self._buffer.truncate()
                self.bytes_written = 0
                self.bytes_read = 0

            def close(self):
                try:
                    self.purge()
                    self._buffer.close()
                except:
                    pass

                self._buffer = None
                self._sock = None


        class PythonParser(BaseParser):
            __doc__ = 'Plain Python parsing class'
            encoding = None

            def __init__(self, socket_read_size):
                self.socket_read_size = socket_read_size
                self._sock = None
                self._buffer = None

            def __del__(self):
                try:
                    self.on_disconnect()
                except Exception:
                    pass

            def on_connect(self, connection):
                """Called when the socket connects"""
                self._sock = connection._sock
                self._buffer = SocketBuffer(self._sock, self.socket_read_size)
                if connection.decode_responses:
                    self.encoding = connection.encoding

            def on_disconnect(self):
                """Called when the socket disconnects"""
                if self._sock is not None:
                    self._sock.close()
                    self._sock = None
                if self._buffer is not None:
                    self._buffer.close()
                    self._buffer = None
                self.encoding = None

            def can_read(self):
                return self._buffer and bool(self._buffer.length)

            def read_response(self):
                response = self._buffer.readline()
                if not response:
                    raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
                byte, response = byte_to_chr(response[0]), response[1:]
                if byte not in ('-', '+', ':', '$', '*'):
                    raise InvalidResponse('Protocol Error: %s, %s' % (
                     str(byte), str(response)))
                if byte == '-':
                    response = nativestr(response)
                    error = self.parse_error(response)
                    if isinstance(error, ConnectionError):
                        raise error
                    return error
                if byte == '+':
                    pass
                elif byte == ':':
                    response = long(response)
                else:
                    if byte == '$':
                        length = int(response)
                        if length == -1:
                            return
                        response = self._buffer.read(length)
                    else:
                        if byte == '*':
                            length = int(response)
                            if length == -1:
                                return
                            response = [self.read_response() for i in xrange(length)]
                        elif isinstance(response, bytes) and self.encoding:
                            response = response.decode(self.encoding)
                        return response


        class HiredisParser(BaseParser):
            __doc__ = 'Parser class for connections using Hiredis'

            def __init__(self, socket_read_size):
                if not HIREDIS_AVAILABLE:
                    raise RedisError('Hiredis is not installed')
                self.socket_read_size = socket_read_size
                if HIREDIS_USE_BYTE_BUFFER:
                    self._buffer = bytearray(socket_read_size)

            def __del__(self):
                try:
                    self.on_disconnect()
                except Exception:
                    pass

            def on_connect(self, connection):
                self._sock = connection._sock
                kwargs = {'protocolError':InvalidResponse, 
                 'replyError':self.parse_error}
                if not HIREDIS_SUPPORTS_CALLABLE_ERRORS:
                    kwargs['replyError'] = ResponseError
                if connection.decode_responses:
                    kwargs['encoding'] = connection.encoding
                self._reader = (hiredis.Reader)(**kwargs)
                self._next_response = False

            def on_disconnect(self):
                self._sock = None
                self._reader = None
                self._next_response = False

            def can_read(self):
                if not self._reader:
                    raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
                if self._next_response is False:
                    self._next_response = self._reader.gets()
                return self._next_response is not False

            def read_response(self):
                if not self._reader:
                    raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
                else:
                    if self._next_response is not False:
                        response = self._next_response
                        self._next_response = False
                        return response
                    response = self._reader.gets()
                    socket_read_size = self.socket_read_size
                    while response is False:
                        try:
                            if HIREDIS_USE_BYTE_BUFFER:
                                bufflen = self._sock.recv_into(self._buffer)
                                if bufflen == 0:
                                    raise socket.error(SERVER_CLOSED_CONNECTION_ERROR)
                            else:
                                buffer = self._sock.recv(socket_read_size)
                                if not isinstance(buffer, bytes) or len(buffer) == 0:
                                    raise socket.error(SERVER_CLOSED_CONNECTION_ERROR)
                        except socket.timeout:
                            raise TimeoutError('Timeout reading from socket')
                        except socket.error:
                            e = sys.exc_info()[1]
                            raise ConnectionError('Error while reading from socket: %s' % (
                             e.args,))

                        if HIREDIS_USE_BYTE_BUFFER:
                            self._reader.feed(self._buffer, 0, bufflen)
                        else:
                            self._reader.feed(buffer)
                        response = self._reader.gets()

                    if (HIREDIS_SUPPORTS_CALLABLE_ERRORS or isinstance)(response, ResponseError):
                        response = self.parse_error(response.args[0])
                    else:
                        if isinstance(response, list):
                            if response:
                                if isinstance(response[0], ResponseError):
                                    response[0] = self.parse_error(response[0].args[0])
                if isinstance(response, ConnectionError):
                    raise response
                else:
                    if isinstance(response, list):
                        if response:
                            if isinstance(response[0], ConnectionError):
                                raise response[0]
                    return response


        if HIREDIS_AVAILABLE:
            DefaultParser = HiredisParser
    else:
        DefaultParser = PythonParser

class Connection(object):
    __doc__ = 'Manages TCP communication to and from a Redis server'
    description_format = 'Connection<host=%(host)s,port=%(port)s,db=%(db)s>'

    def __init__(self, host='localhost', port=6379, db=0, password=None, socket_timeout=None, socket_connect_timeout=None, socket_keepalive=False, socket_keepalive_options=None, retry_on_timeout=False, encoding='utf-8', encoding_errors='strict', decode_responses=False, parser_class=DefaultParser, socket_read_size=65536):
        self.pid = os.getpid()
        self.host = host
        self.port = int(port)
        self.db = db
        self.password = password
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout or socket_timeout
        self.socket_keepalive = socket_keepalive
        self.socket_keepalive_options = socket_keepalive_options or {}
        self.retry_on_timeout = retry_on_timeout
        self.encoding = encoding
        self.encoding_errors = encoding_errors
        self.decode_responses = decode_responses
        self._sock = None
        self._parser = parser_class(socket_read_size=socket_read_size)
        self._description_args = {'host':self.host, 
         'port':self.port, 
         'db':self.db}
        self._connect_callbacks = []

    def __repr__(self):
        return self.description_format % self._description_args

    def __del__(self):
        try:
            self.disconnect()
        except Exception:
            pass

    def register_connect_callback(self, callback):
        self._connect_callbacks.append(callback)

    def clear_connect_callbacks(self):
        self._connect_callbacks = []

    def connect(self):
        """Connects to the Redis server if not already connected"""
        if self._sock:
            return
        try:
            sock = self._connect()
        except socket.error:
            e = sys.exc_info()[1]
            raise ConnectionError(self._error_message(e))

        self._sock = sock
        try:
            self.on_connect()
        except RedisError:
            self.disconnect()
            raise

        for callback in self._connect_callbacks:
            callback(self)

    def _connect(self):
        """Create a TCP socket connection"""
        err = None
        for res in socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM):
            family, socktype, proto, canonname, socket_address = res
            sock = None
            try:
                sock = socket.socket(family, socktype, proto)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                if self.socket_keepalive:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    for k, v in iteritems(self.socket_keepalive_options):
                        sock.setsockopt(socket.SOL_TCP, k, v)

                sock.settimeout(self.socket_connect_timeout)
                sock.connect(socket_address)
                sock.settimeout(self.socket_timeout)
                return sock
            except socket.error as _:
                try:
                    err = _
                    if sock is not None:
                        sock.close()
                finally:
                    _ = None
                    del _

        if err is not None:
            raise err
        raise socket.error('socket.getaddrinfo returned an empty list')

    def _error_message(self, exception):
        if len(exception.args) == 1:
            return 'Error connecting to %s:%s. %s.' % (
             self.host, self.port, exception.args[0])
        return 'Error %s connecting to %s:%s. %s.' % (
         exception.args[0], self.host, self.port, exception.args[1])

    def on_connect(self):
        """Initialize the connection, authenticate and select a database"""
        self._parser.on_connect(self)
        if self.password:
            self.send_command('AUTH', self.password)
            if nativestr(self.read_response()) != 'OK':
                raise AuthenticationError('Invalid Password')
        if self.db:
            self.send_command('SELECT', self.db)
            if nativestr(self.read_response()) != 'OK':
                raise ConnectionError('Invalid Database')

    def disconnect(self):
        """Disconnects from the Redis server"""
        self._parser.on_disconnect()
        if self._sock is None:
            return
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
        except socket.error:
            pass

        self._sock = None

    def send_packed_command(self, command):
        """Send an already packed command to the Redis server"""
        if not self._sock:
            self.connect()
        try:
            if isinstance(command, str):
                command = [
                 command]
            for item in command:
                self._sock.sendall(item)

        except socket.timeout:
            self.disconnect()
            raise TimeoutError('Timeout writing to socket')
        except socket.error:
            e = sys.exc_info()[1]
            self.disconnect()
            if len(e.args) == 1:
                errno, errmsg = 'UNKNOWN', e.args[0]
            else:
                errno = e.args[0]
                errmsg = e.args[1]
            raise ConnectionError('Error %s while writing to socket. %s.' % (
             errno, errmsg))
        except:
            self.disconnect()
            raise

    def send_command(self, *args):
        """Pack and send a command to the Redis server"""
        self.send_packed_command((self.pack_command)(*args))

    def can_read(self, timeout=0):
        """Poll the socket to see if there's data that can be read."""
        sock = self._sock
        if not sock:
            self.connect()
            sock = self._sock
        return self._parser.can_read() or bool(select([sock], [], [], timeout)[0])

    def read_response(self):
        """Read the response from a previously sent command"""
        try:
            response = self._parser.read_response()
        except:
            self.disconnect()
            raise

        if isinstance(response, ResponseError):
            raise response
        return response

    def encode(self, value):
        """Return a bytestring representation of the value"""
        if isinstance(value, Token):
            return b(value.value)
            if isinstance(value, bytes):
                return value
            if isinstance(value, (int, long)):
                value = b(str(value))
        elif isinstance(value, float):
            value = b(repr(value))
        else:
            if not isinstance(value, basestring):
                value = unicode(value)
        if isinstance(value, unicode):
            value = value.encode(self.encoding, self.encoding_errors)
        return value

    def pack_command(self, *args):
        """Pack a series of arguments into the Redis protocol"""
        output = []
        command = args[0]
        if ' ' in command:
            args = tuple([Token(s) for s in command.split(' ')]) + args[1:]
        else:
            args = (
             Token(command),) + args[1:]
        buff = SYM_EMPTY.join((
         SYM_STAR, b(str(len(args))), SYM_CRLF))
        for arg in imap(self.encode, args):
            if len(buff) > 6000 or len(arg) > 6000:
                buff = SYM_EMPTY.join((
                 buff, SYM_DOLLAR, b(str(len(arg))), SYM_CRLF))
                output.append(buff)
                output.append(arg)
                buff = SYM_CRLF
            else:
                buff = SYM_EMPTY.join((buff, SYM_DOLLAR, b(str(len(arg))),
                 SYM_CRLF, arg, SYM_CRLF))

        output.append(buff)
        return output

    def pack_commands(self, commands):
        """Pack multiple commands into the Redis protocol"""
        output = []
        pieces = []
        buffer_length = 0
        for cmd in commands:
            for chunk in (self.pack_command)(*cmd):
                pieces.append(chunk)
                buffer_length += len(chunk)

            if buffer_length > 6000:
                output.append(SYM_EMPTY.join(pieces))
                buffer_length = 0
                pieces = []

        if pieces:
            output.append(SYM_EMPTY.join(pieces))
        return output


class SSLConnection(Connection):
    description_format = 'SSLConnection<host=%(host)s,port=%(port)s,db=%(db)s>'

    def __init__(self, ssl_keyfile=None, ssl_certfile=None, ssl_cert_reqs=None, ssl_ca_certs=None, **kwargs):
        if not ssl_available:
            raise RedisError("Python wasn't built with SSL support")
        else:
            (super(SSLConnection, self).__init__)(**kwargs)
            self.keyfile = ssl_keyfile
            self.certfile = ssl_certfile
            if ssl_cert_reqs is None:
                ssl_cert_reqs = ssl.CERT_NONE
            else:
                if isinstance(ssl_cert_reqs, basestring):
                    CERT_REQS = {'none':ssl.CERT_NONE,  'optional':ssl.CERT_OPTIONAL, 
                     'required':ssl.CERT_REQUIRED}
                    if ssl_cert_reqs not in CERT_REQS:
                        raise RedisError('Invalid SSL Certificate Requirements Flag: %s' % ssl_cert_reqs)
                    ssl_cert_reqs = CERT_REQS[ssl_cert_reqs]
        self.cert_reqs = ssl_cert_reqs
        self.ca_certs = ssl_ca_certs

    def _connect(self):
        sock = super(SSLConnection, self)._connect()
        sock = ssl.wrap_socket(sock, cert_reqs=(self.cert_reqs),
          keyfile=(self.keyfile),
          certfile=(self.certfile),
          ca_certs=(self.ca_certs))
        return sock


class UnixDomainSocketConnection(Connection):
    description_format = 'UnixDomainSocketConnection<path=%(path)s,db=%(db)s>'

    def __init__(self, path='', db=0, password=None, socket_timeout=None, encoding='utf-8', encoding_errors='strict', decode_responses=False, retry_on_timeout=False, parser_class=DefaultParser, socket_read_size=65536):
        self.pid = os.getpid()
        self.path = path
        self.db = db
        self.password = password
        self.socket_timeout = socket_timeout
        self.retry_on_timeout = retry_on_timeout
        self.encoding = encoding
        self.encoding_errors = encoding_errors
        self.decode_responses = decode_responses
        self._sock = None
        self._parser = parser_class(socket_read_size=socket_read_size)
        self._description_args = {'path':self.path, 
         'db':self.db}
        self._connect_callbacks = []

    def _connect(self):
        """Create a Unix domain socket connection"""
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.socket_timeout)
        sock.connect(self.path)
        return sock

    def _error_message(self, exception):
        if len(exception.args) == 1:
            return 'Error connecting to unix socket: %s. %s.' % (
             self.path, exception.args[0])
        return 'Error %s connecting to unix socket: %s. %s.' % (
         exception.args[0], self.path, exception.args[1])


class ConnectionPool(object):
    __doc__ = 'Generic connection pool'

    @classmethod
    def from_url(cls, url, db=None, decode_components=False, **kwargs):
        """
        Return a connection pool configured from the given URL.

        For example::

            redis://[:password]@localhost:6379/0
            rediss://[:password]@localhost:6379/0
            unix://[:password]@/path/to/socket.sock?db=0

        Three URL schemes are supported:
            redis:// creates a normal TCP socket connection
            rediss:// creates a SSL wrapped TCP socket connection
            unix:// creates a Unix Domain Socket connection

        There are several ways to specify a database number. The parse function
        will return the first specified option:
            1. A ``db`` querystring option, e.g. redis://localhost?db=0
            2. If using the redis:// scheme, the path argument of the url, e.g.
               redis://localhost/0
            3. The ``db`` argument to this function.

        If none of these options are specified, db=0 is used.

        The ``decode_components`` argument allows this function to work with
        percent-encoded URLs. If this argument is set to ``True`` all ``%xx``
        escapes will be replaced by their single-character equivalents after
        the URL has been parsed. This only applies to the ``hostname``,
        ``path``, and ``password`` components.

        Any additional querystring arguments and keyword arguments will be
        passed along to the ConnectionPool class's initializer. In the case
        of conflicting arguments, querystring arguments always win.
        """
        url_string = url
        url = urlparse(url)
        qs = ''
        if '?' in url.path:
            qs = url.query or url.path.split('?', 1)[1]
            url = urlparse(url_string[:-(len(qs) + 1)])
        else:
            qs = url.query
        url_options = {}
        for name, value in iteritems(parse_qs(qs)):
            if value and len(value) > 0:
                url_options[name] = value[0]

        if decode_components:
            password = unquote(url.password) if url.password else None
            path = unquote(url.path) if url.path else None
            hostname = unquote(url.hostname) if url.hostname else None
        else:
            password = url.password
            path = url.path
            hostname = url.hostname
        if url.scheme == 'unix':
            url_options.update({'password':password, 
             'path':path, 
             'connection_class':UnixDomainSocketConnection})
        else:
            url_options.update({'host':hostname, 
             'port':int(url.port or 6379), 
             'password':password})
            if 'db' not in url_options:
                if path:
                    try:
                        url_options['db'] = int(path.replace('/', ''))
                    except (AttributeError, ValueError):
                        pass

            if url.scheme == 'rediss':
                url_options['connection_class'] = SSLConnection
            url_options['db'] = int(url_options.get('db', db or 0))
            kwargs.update(url_options)
            if 'charset' in kwargs:
                warnings.warn(DeprecationWarning('"charset" is deprecated. Use "encoding" instead'))
                kwargs['encoding'] = kwargs.pop('charset')
            if 'errors' in kwargs:
                warnings.warn(DeprecationWarning('"errors" is deprecated. Use "encoding_errors" instead'))
                kwargs['encoding_errors'] = kwargs.pop('errors')
            return cls(**kwargs)

    def __init__(self, connection_class=Connection, max_connections=None, **connection_kwargs):
        """
        Create a connection pool. If max_connections is set, then this
        object raises redis.ConnectionError when the pool's limit is reached.

        By default, TCP connections are created connection_class is specified.
        Use redis.UnixDomainSocketConnection for unix sockets.

        Any additional keyword arguments are passed to the constructor of
        connection_class.
        """
        max_connections = max_connections or 2147483648
        if not isinstance(max_connections, (int, long)) or max_connections < 0:
            raise ValueError('"max_connections" must be a positive integer')
        self.connection_class = connection_class
        self.connection_kwargs = connection_kwargs
        self.max_connections = max_connections
        self.reset()

    def __repr__(self):
        return '%s<%s>' % (
         type(self).__name__,
         self.connection_class.description_format % self.connection_kwargs)

    def reset(self):
        self.pid = os.getpid()
        self._created_connections = 0
        self._available_connections = []
        self._in_use_connections = set()
        self._check_lock = threading.Lock()

    def _checkpid(self):
        if self.pid != os.getpid():
            with self._check_lock:
                if self.pid == os.getpid():
                    return
                self.disconnect()
                self.reset()

    def get_connection(self, command_name, *keys, **options):
        """Get a connection from the pool"""
        self._checkpid()
        try:
            connection = self._available_connections.pop()
        except IndexError:
            connection = self.make_connection()

        self._in_use_connections.add(connection)
        return connection

    def make_connection(self):
        """Create a new connection"""
        if self._created_connections >= self.max_connections:
            raise ConnectionError('Too many connections')
        self._created_connections += 1
        return (self.connection_class)(**self.connection_kwargs)

    def release(self, connection):
        """Releases the connection back to the pool"""
        self._checkpid()
        if connection.pid != self.pid:
            return
        self._in_use_connections.remove(connection)
        self._available_connections.append(connection)

    def disconnect(self):
        """Disconnects all connections in the pool"""
        all_conns = chain(self._available_connections, self._in_use_connections)
        for connection in all_conns:
            connection.disconnect()


class BlockingConnectionPool(ConnectionPool):
    __doc__ = '\n    Thread-safe blocking connection pool::\n\n        >>> from redis.client import Redis\n        >>> client = Redis(connection_pool=BlockingConnectionPool())\n\n    It performs the same function as the default\n    ``:py:class: ~redis.connection.ConnectionPool`` implementation, in that,\n    it maintains a pool of reusable connections that can be shared by\n    multiple redis clients (safely across threads if required).\n\n    The difference is that, in the event that a client tries to get a\n    connection from the pool when all of connections are in use, rather than\n    raising a ``:py:class: ~redis.exceptions.ConnectionError`` (as the default\n    ``:py:class: ~redis.connection.ConnectionPool`` implementation does), it\n    makes the client wait ("blocks") for a specified number of seconds until\n    a connection becomes available.\n\n    Use ``max_connections`` to increase / decrease the pool size::\n\n        >>> pool = BlockingConnectionPool(max_connections=10)\n\n    Use ``timeout`` to tell it either how many seconds to wait for a connection\n    to become available, or to block forever:\n\n        # Block forever.\n        >>> pool = BlockingConnectionPool(timeout=None)\n\n        # Raise a ``ConnectionError`` after five seconds if a connection is\n        # not available.\n        >>> pool = BlockingConnectionPool(timeout=5)\n    '

    def __init__(self, max_connections=50, timeout=20, connection_class=Connection, queue_class=LifoQueue, **connection_kwargs):
        self.queue_class = queue_class
        self.timeout = timeout
        (super(BlockingConnectionPool, self).__init__)(connection_class=connection_class, 
         max_connections=max_connections, **connection_kwargs)

    def reset(self):
        self.pid = os.getpid()
        self._check_lock = threading.Lock()
        self.pool = self.queue_class(self.max_connections)
        while True:
            try:
                self.pool.put_nowait(None)
            except Full:
                break

        self._connections = []

    def make_connection(self):
        """Make a fresh connection."""
        connection = (self.connection_class)(**self.connection_kwargs)
        self._connections.append(connection)
        return connection

    def get_connection(self, command_name, *keys, **options):
        """
        Get a connection, blocking for ``self.timeout`` until a connection
        is available from the pool.

        If the connection returned is ``None`` then creates a new connection.
        Because we use a last-in first-out queue, the existing connections
        (having been returned to the pool after the initial ``None`` values
        were added) will be returned before ``None`` values. This means we only
        create new connections when we need to, i.e.: the actual number of
        connections will only increase in response to demand.
        """
        self._checkpid()
        connection = None
        try:
            connection = self.pool.get(block=True, timeout=(self.timeout))
        except Empty:
            raise ConnectionError('No connection available.')

        if connection is None:
            connection = self.make_connection()
        return connection

    def release(self, connection):
        """Releases the connection back to the pool."""
        self._checkpid()
        if connection.pid != self.pid:
            return
        try:
            self.pool.put_nowait(connection)
        except Full:
            pass

    def disconnect(self):
        """Disconnects all connections in the pool."""
        for connection in self._connections:
            connection.disconnect()