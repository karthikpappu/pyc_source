# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aio/tcp/clienting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 25645 bytes
"""
tcp async io (nonblocking) client module

"""
from __future__ import absolute_import, division, print_function
import sys, os, socket, errno, platform
from collections import deque
from binascii import hexlify
try:
    import ssl
except ImportError:
    pass

from ...aid.sixing import *
from ...aid.odicting import odict
from ...aid.timing import StoreTimer
from ...aid.consoling import getConsole
from .. import aioing
from ...base import storing
console = getConsole()

class Client(object):
    __doc__ = '\n    Nonblocking TCP Socket Client Class.\n    '
    Timeout = 1.0
    Reconnectable = False

    def __init__(self, name='', uid=0, ha=None, host='127.0.0.1', port=56000, bufsize=8096, wlog=None, store=None, timeout=None, reconnectable=None, txes=None, rxbs=None):
        """
        Initialization method for instance.
        name = user friendly name for connection
        uid = unique identifier for connection
        ha = host address duple (host, port) of remote server
        host = host address or tcp server to connect to
        port = socket port
        bufsize = buffer size
        wlog = WireLog object if any
        store = store reference
        timeout = auto reconnect timeout
        reconnectable = Boolean auto reconnect if timed out
        txes = deque of data to send
        rxbs = bytearray of data received
        """
        self.name = name
        self.uid = uid
        self.reinitHostPort(ha=ha, hostname=host, port=port)
        self.ha = ha or (host, port)
        host, port = self.ha
        self.hostname = host
        host = aioing.normalizeHost(host)
        self.ha = (host, port)
        self.bs = bufsize
        self.wlog = wlog
        self.cs = None
        self.ca = (None, None)
        self._accepted = False
        self.cutoff = False
        self.txes = txes if txes is not None else deque()
        self.rxbs = rxbs if rxbs is not None else bytearray()
        self.store = store or storing.Store(stamp=0.0)
        self.timeout = timeout if timeout is not None else self.Timeout
        self.timer = StoreTimer((self.store), duration=(self.timeout))
        self.reconnectable = reconnectable if reconnectable is not None else self.Reconnectable
        self.opened = False

    @property
    def host(self):
        """
        Property that returns host in .ha duple
        """
        return self.ha[0]

    @host.setter
    def host(self, value):
        """
        setter for host property
        """
        self.ha = (
         value, self.port)

    @property
    def port(self):
        """
        Property that returns port in .ha duple
        """
        return self.ha[1]

    @port.setter
    def port(self, value):
        """
        setter for port property
        """
        self.ha = (
         self.host, value)

    @property
    def accepted(self):
        """
        Property that returns accepted state of TCP socket
        """
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        """
        setter for accepted property
        """
        self._accepted = value

    @property
    def connected(self):
        """
        Property that returns connected state of TCP socket
        Non-tls tcp is connected when accepted
        """
        return self.accepted

    @connected.setter
    def connected(self, value):
        """
        setter for connected property
        """
        self.accepted = value

    def reinitHostPort(self, ha=None, hostname='127.0.0.1', port=56000):
        """
        Reinit self.ha and self.hostname from ha = (host, port) or hostname port
        self.ha is of form (host, port) where host is either dns name or ip
        self.hostname is hostname as dns name
        host eventually is host ip address output from normalizeHost()
        """
        self.ha = ha or (hostname, port)
        hostname, port = self.ha
        self.hostname = hostname
        host = aioing.normalizeHost(hostname)
        self.ha = (host, port)

    def actualBufSizes(self):
        """
        Returns duple of the the actual socket send and receive buffer size
        (send, receive)
        """
        if not self.cs:
            return (0, 0)
        else:
            return (
             self.cs.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF),
             self.cs.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF))

    def open(self):
        """
        Opens connection socket in non blocking mode.

        if socket not closed properly, binding socket gets error
          socket.error: (48, 'Address already in use')
        """
        self.accepted = False
        self.connected = False
        self.cutoff = False
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if sys.platform.startswith('linux'):
            bs = 2 * self.bs
        else:
            bs = self.bs
        if self.cs.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) < bs:
            self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.bs)
        if self.cs.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) < bs:
            self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.bs)
        self.cs.setblocking(0)
        self.opened = True
        return True

    def reopen(self):
        """
        Idempotently opens socket
        """
        self.close()
        return self.open()

    def shutdown(self, how=socket.SHUT_RDWR):
        """
        Shutdown connected socket .cs
        """
        if self.cs:
            try:
                self.cs.shutdown(how)
            except socket.error as ex:
                pass

    def shutdownSend(self):
        """
        Shutdown send on connected socket .cs
        """
        if self.cs:
            try:
                self.shutdown(how=(socket.SHUT_WR))
            except socket.error as ex:
                pass

    def shutdownReceive(self):
        """
        Shutdown receive on connected socket .cs
        """
        if self.cs:
            try:
                self.shutdown(how=(socket.SHUT_RD))
            except socket.error as ex:
                pass

    def shutclose(self):
        """
        Shutdown and close connected socket .cs
        """
        if self.cs:
            self.shutdown()
            self.cs.close()
            self.cs = None
            self.accepted = False
            self.connected = False
            self.opened = False

    close = shutclose

    def refresh(self):
        """
        Restart timer
        """
        self.timer.restart()

    def accept(self):
        """
        Attempt nonblocking acceptance connect to .ha
        Returns True if successful
        Returns False if not so try again later
        """
        if not self.cs:
            self.reopen()
        try:
            result = self.cs.connect_ex(self.ha)
        except socket.error as ex:
            console.terse('socket.error = {0}\n'.format(ex))
            raise

        if result not in [0, errno.EISCONN]:
            if result in (errno.EINVAL, errno.ECONNREFUSED):
                self.reopen()
            return False
        else:
            self.ca = self.cs.getsockname()
            self.ha = self.cs.getpeername()
            self.accepted = True
            self.cutoff = False
            return True

    def connect(self):
        """
        Attempt nonblocking connect to .ha
        Returns True if successful
        Returns False if not so try again later
        For non-TLS tcp connect is done when accepted
        """
        return self.accept()

    def serviceConnect(self):
        """
        Service connection attempt
        If not already connected make a nonblocking attempt
        Returns .connected
        """
        if not self.connected:
            self.connect()
            if not self.connected:
                if self.reconnectable:
                    if self.timeout > 0.0:
                        if self.timer.expired:
                            self.reopen()
                            self.timer.restart()
        return self.connected

    def receive(self):
        """
        Perform non blocking receive from connected socket .cs

        If no data then returns None
        If connection closed then returns empty
        Otherwise returns data
        data is string in python2 and bytes in python3
        """
        try:
            data = self.cs.recv(self.bs)
        except socket.error as ex:
            if ex.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                return
            if ex.args[0] in (errno.ECONNRESET,
             errno.ENETRESET,
             errno.ENETUNREACH,
             errno.EHOSTUNREACH,
             errno.ENETDOWN,
             errno.EHOSTDOWN,
             errno.ETIMEDOUT,
             errno.ECONNREFUSED):
                emsg = 'socket.error = {0}: Outgoer at {1} while receiving from {2}\n'.format(ex, self.ca, self.ha)
                console.profuse(emsg)
                self.cutoff = True
                return bytes()
            emsg = 'socket.error = {0}: Outgoer at {1} while receiving from {2}\n'.format(ex, self.ca, self.ha)
            console.profuse(emsg)
            raise

        if data:
            if console._verbosity >= console.Wordage.profuse:
                try:
                    load = data.decode('UTF-8')
                except UnicodeDecodeError as ex:
                    load = '0x{0}'.format(hexlify(data).decode('ASCII'))

                cmsg = 'Outgoer at {0}, received from {1}:\n------------\n{2}\n\n'.format(self.ca, self.ha, load)
                console.profuse(cmsg)
            if self.wlog:
                self.wlog.writeRx(self.ha, data)
        else:
            self.cutoff = True
        return data

    def serviceReceives(self):
        """
        Service receives until no more
        """
        while self.connected and not self.cutoff:
            data = self.receive()
            if not data:
                break
            self.rxbs.extend(data)

    def serviceReceiveOnce(self):
        """
        Retrieve from server only one reception
        """
        if self.connected:
            if not self.cutoff:
                data = self.receive()
                if data:
                    self.rxbs.extend(data)

    def clearRxbs(self):
        """
        Clear .rxbs
        """
        del self.rxbs[:]

    def catRxbs(self):
        """
        Return copy and clear .rxbs
        """
        rx = self.rxbs[:]
        self.clearRxbs()
        return rx

    def tailRxbs(self, index):
        """
        Returns duple of (bytes(self.rxbs[index:]), len(self.rxbs))
        slices the tail from index to end and converts to bytes
        also the length of .rxbs to be used to update index
        """
        return (
         bytes(self.rxbs[index:]), len(self.rxbs))

    def send(self, data):
        """
        Perform non blocking send on connected socket .cs.
        Return number of bytes sent
        data is string in python2 and bytes in python3
        """
        try:
            result = self.cs.send(data)
        except socket.error as ex:
            if ex.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                result = 0
            else:
                if ex.args[0] in (errno.ECONNRESET,
                 errno.ENETRESET,
                 errno.ENETUNREACH,
                 errno.EHOSTUNREACH,
                 errno.ENETDOWN,
                 errno.EHOSTDOWN,
                 errno.ETIMEDOUT,
                 errno.ECONNREFUSED):
                    emsg = 'socket.error = {0}: Outgoer at {1} while sending to {2} \n'.format(ex, self.ca, self.ha)
                    console.profuse(emsg)
                    self.cutoff = True
                    result = 0
                else:
                    emsg = 'socket.error = {0}: Outgoer at {1} while sending to {2} \n'.format(ex, self.ca, self.ha)
                    console.profuse(emsg)
                    raise

        if result:
            if console._verbosity >= console.Wordage.profuse:
                try:
                    load = data[:result].decode('UTF-8')
                except UnicodeDecodeError as ex:
                    load = '0x{0}'.format(hexlify(data[:result]).decode('ASCII'))

                cmsg = 'Outgoer at {0}, sent {1} bytes to {2}:\n------------\n{3}\n\n'.format(self.ca, result, self.ha, load)
                console.profuse(cmsg)
            if self.wlog:
                self.wlog.writeTx(self.ha, data[:result])
        return result

    def tx(self, data):
        """
        Queue data onto .txes
        """
        self.txes.append(data)

    def serviceTxes(self):
        """
        Service transmits
        For each tx if all bytes sent then keep sending until partial send
        or no more to send
        If partial send reattach and return
        """
        while self.txes and self.connected and not self.cutoff:
            data = self.txes.popleft()
            count = self.send(data)
            if count < len(data):
                self.txes.appendleft(data[count:])
                break


Outgoer = Client

class ClientTls(Client):
    __doc__ = '\n    Outgoer with Nonblocking TLS/SSL support\n    Nonblocking TCP Socket Client Class.\n    '

    def __init__(self, context=None, version=None, certify=None, hostify=None, certedhost='', keypath=None, certpath=None, cafilepath=None, **kwa):
        """
        Initialization method for instance.

        IF no context THEN create one

        IF no version THEN create using library default

        IF certify is not None then use certify else use default

        IF hostify is not none the use hostify else use default

        context = context object for tls/ssl If None use default
        version = ssl version If None use default
        certify = cert requirement If None use default
                  ssl.CERT_NONE = 0
                  ssl.CERT_OPTIONAL = 1
                  ssl.CERT_REQUIRED = 2
        keypath = pathname of local client side PKI private key file path
                  If given apply to context
        certpath = pathname of local client side PKI public cert file path
                  If given apply to context
        cafilepath = Cert Authority file path to use to verify server cert
                  If given apply to context
        hostify = verify server hostName If None use default
        certedhost = server's certificate common name (hostname) to check against
        """
        (super(OutgoerTls, self).__init__)(**kwa)
        self._connected = False
        if context is None:
            if not version:
                context = ssl.create_default_context(purpose=(ssl.Purpose.SERVER_AUTH))
                hostify = hostify if hostify is not None else context.check_hostname
                context.check_hostname = hostify
                certify = certify if certify is not None else context.verify_mode
                context.verify_mode = certify
            else:
                context = ssl.SSLContext(version)
                context.options |= ssl.OP_NO_SSLv2
                context.options |= ssl.OP_NO_SSLv3
                context.options |= getattr(ssl._ssl, 'OP_NO_COMPRESSION', 0)
                context.verify_mode = certify = ssl.CERT_REQUIRED if certify is None else certify
                context.check_hostname = hostify = True if hostify else False
        self.context = context
        self.certedhost = certedhost or self.hostname
        if cafilepath:
            context.load_verify_locations(cafile=cafilepath, capath=None,
              cadata=None)
        else:
            if context.verify_mode != ssl.CERT_NONE:
                context.load_default_certs(purpose=(ssl.Purpose.SERVER_AUTH))
        if keypath or certpath:
            context.load_cert_chain(certfile=certpath, keyfile=keypath)
        if hostify:
            if certify == ssl.CERT_NONE:
                raise ValueError('Check Hostname needs a SSL context with either CERT_OPTIONAL or CERT_REQUIRED')

    @property
    def connected(self):
        """
        Property that returns connected state of TCP socket
        TLS tcp is connected when accepted and handshake completed
        """
        return self._connected

    @connected.setter
    def connected(self, value):
        """
        setter for connected property
        """
        self._connected = value

    def shutclose(self):
        """
        Shutdown and close connected socket .cs
        """
        if self.cs:
            self.shutdown()
            self.cs.close()
            self.cs = None
            self.accepted = False
            self.connected = False
            self.opened = False

    close = shutclose

    def wrap(self):
        """
        Wrap socket .cs in ssl context
        """
        self.cs = self.context.wrap_socket((self.cs), server_side=False,
          do_handshake_on_connect=False,
          server_hostname=(self.certedhost))

    def handshake(self):
        """
        Attempt nonblocking ssl handshake to .ha
        Returns True if successful
        Returns False if not so try again later
        """
        try:
            self.cs.do_handshake()
        except ssl.SSLError as ex:
            if ex.errno in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE):
                return False
            else:
                if ex.errno in (ssl.SSL_ERROR_EOF,):
                    self.shutclose()
                    raise
                else:
                    self.shutclose()
                    raise
        except OSError as ex:
            self.shutclose()
            if ex.errno in (errno.ECONNABORTED,):
                raise
            raise
        except Exception as ex:
            self.shutclose()
            raise

        self.connected = True
        return True

    def connect(self):
        """
        Attempt nonblocking connect to .ha
        Returns True if successful
        Returns False if not so try again later
        Connected when both accepted connection and TLS handshake complete
        """
        if not self.accepted:
            self.accept()
            if self.accepted:
                if not self.certedhost:
                    self.certedhost = self.ha[0]
                self.wrap()
        else:
            if self.accepted:
                if not self.connected:
                    self.handshake()
        return self.connected

    def receive(self):
        """
        Perform non blocking receive from connected socket .cs

        If no data then returns None
        If connection closed then returns ''
        Otherwise returns data
        data is string in python2 and bytes in python3
        """
        try:
            data = self.cs.recv(self.bs)
        except socket.error as ex:
            if ex.args[0] in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE):
                return
            if ex.args[0] in (errno.ECONNRESET,
             errno.ENETRESET,
             errno.ENETUNREACH,
             errno.EHOSTUNREACH,
             errno.ENETDOWN,
             errno.EHOSTDOWN,
             errno.ETIMEDOUT,
             errno.ECONNREFUSED,
             ssl.SSLEOFError):
                emsg = 'socket.error = {0}: OutgoerTLS at {1} receiving from {2}\n'.format(ex, self.ca, self.ha)
                console.profuse(emsg)
                self.cutoff = True
                return bytes()
            emsg = 'socket.error = {0}: OutgoerTLS at {1} receiving from {2}\n'.format(ex, self.ca, self.ha)
            console.profuse(emsg)
            raise

        if data:
            if console._verbosity >= console.Wordage.profuse:
                try:
                    load = data.decode('UTF-8')
                except UnicodeDecodeError as ex:
                    load = '0x{0}'.format(hexlify(data).decode('ASCII'))

                cmsg = 'Outgoer at {0}, received from {1}:\n------------\n{2}\n\n'.format(self.ca, self.ha, load)
                console.profuse(cmsg)
            if self.wlog:
                self.wlog.writeRx(self.ha, data)
        else:
            self.cutoff = True
        return data

    def send(self, data):
        """
        Perform non blocking send on connected socket .cs.
        Return number of bytes sent
        data is string in python2 and bytes in python3
        """
        try:
            result = self.cs.send(data)
        except socket.error as ex:
            if ex.args[0] in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE):
                result = 0
            else:
                if ex.args[0] in (errno.ECONNRESET,
                 errno.ENETRESET,
                 errno.ENETUNREACH,
                 errno.EHOSTUNREACH,
                 errno.ENETDOWN,
                 errno.EHOSTDOWN,
                 errno.ETIMEDOUT,
                 errno.ECONNREFUSED,
                 ssl.SSLEOFError):
                    emsg = 'socket.error = {0}: OutgoerTLS at {1} while sending to {2} \n'.format(ex, self.ca, self.ha)
                    console.profuse(emsg)
                    self.cutoff = True
                    result = 0
                else:
                    emsg = 'socket.error = {0}: OutgoerTLS at {1} while sending to {2} \n'.format(ex, self.ca, self.ha)
                    console.profuse(emsg)
                    raise

        if result:
            if console._verbosity >= console.Wordage.profuse:
                try:
                    load = data[:result].decode('UTF-8')
                except UnicodeDecodeError as ex:
                    load = '0x{0}'.format(hexlify(data[:result]).decode('ASCII'))

                cmsg = 'Outgoer at {0}, sent {1} bytes to {2}:\n------------\n{3}\n\n'.format(self.ca, result, self.ha, load)
                console.profuse(cmsg)
            if self.wlog:
                self.wlog.writeTx(self.ha, data[:result])
        return result


OutgoerTls = ClientTls