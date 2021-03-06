# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_pure_sasl_mechanisms.py
# Compiled at: 2018-03-08 20:03:41
# Size of source mod 2**32: 17349 bytes
import base64, hashlib, hmac, random, struct, sys
from cerebro._pure_sasl import SASLError, SASLProtocolException, QOP
try:
    import kerberos
    _have_kerberos = True
except ImportError:
    _have_kerberos = False

PY3 = sys.version_info[0] == 3
if PY3:

    def _b(s):
        return s.encode('utf-8')


else:

    def _b(s):
        return s


class Mechanism(object):
    """Mechanism"""
    name = None
    score = 0
    complete = False
    has_initial_response = False
    allows_anonymous = True
    uses_plaintext = True
    active_safe = False
    dictionary_safe = False
    qops = [
     QOP.AUTH]
    qop = QOP.AUTH

    def __init__(self, sasl, **props):
        self.sasl = sasl

    def process(self, challenge=None):
        """
        Process a challenge request and return the response.

        :param challenge: A challenge issued by the server that
                          must be answered for authentication.
        """
        raise NotImplementedError()

    def wrap(self, outgoing):
        """
        Wrap an outgoing message intended for the SASL server. Depending
        on the negotiated quality of protection, this may result in the
        message being signed, encrypted, or left unaltered.
        """
        raise NotImplementedError()

    def unwrap(self, incoming):
        """
        Unwrap a message from the SASL server. Depending on the negotiated
        quality of protection, this may check a signature, decrypt the message,
        or leave the message unaltered.
        """
        raise NotImplementedError()

    def dispose(self):
        """
        Clear all sensitive data, such as passwords.
        """
        pass

    def _fetch_properties(self, *properties):
        """
        Ensure this mechanism has the needed properties. If they haven't
        been set yet, the registered callback function will be called for
        each property to retrieve a value.
        """
        needed = [p for p in properties if getattr(self, p, None) is None]
        if needed and not self.sasl.callback:
            raise SASLError('The following properties are required, but a callback has not been set: %s' % ', '.join(needed))
        for prop in needed:
            setattr(self, prop, self.sasl.callback(prop))

    def _pick_qop(self, server_qop_set):
        """
        Choose a quality of protection based on the user's requirements,
        what the server supports, and what the mechanism supports.
        """
        user_qops = set((_b(qop) if isinstance(qop, str) else qop) for qop in self.sasl.qops)
        supported_qops = set(self.qops)
        available_qops = user_qops & supported_qops & server_qop_set
        if not available_qops:
            user = ', '.join(user_qops).decode('ascii')
            supported = ', '.join(supported_qops).decode('ascii')
            offered = ', '.join(server_qop_set).decode('ascii')
            raise SASLProtocolException('Your requested quality of protection is one of (%s), the server is offering (%s), and %s supports (%s)' % (
             user, offered, self.name, supported))
        else:
            for qop in (QOP.AUTH_CONF, QOP.AUTH_INT, QOP.AUTH):
                if qop in available_qops:
                    self.qop = qop
                    break


class AnonymousMechanism(Mechanism):
    """AnonymousMechanism"""
    name = 'ANONYMOUS'
    score = 0
    uses_plaintext = False

    def process(self, challenge=None):
        self.complete = True
        return 'Anonymous, None'


class PlainMechanism(Mechanism):
    """PlainMechanism"""
    name = 'PLAIN'
    score = 1
    allows_anonymous = False

    def wrap(self, outgoing):
        return outgoing

    def unwrap(self, incoming):
        return incoming

    def __init__(self, sasl, username=None, password=None, identity='', **props):
        Mechanism.__init__(self, sasl)
        self.identity = identity
        self.username = username
        self.password = password

    def process(self, challenge=None):
        self._fetch_properties('username', 'password')
        self.complete = True
        auth_id = self.sasl.authorization_id or self.identity
        return ''.join((_b(auth_id), '\x00', _b(self.username), '\x00', _b(self.password)))

    def dispose(self):
        self.password = None


class CramMD5Mechanism(PlainMechanism):
    name = 'CRAM-MD5'
    score = 20
    allows_anonymous = False
    uses_plaintext = False

    def __init__(self, sasl, username=None, password=None, **props):
        Mechanism.__init__(self, sasl)
        self.username = username
        self.password = password

    def process(self, challenge=None):
        if challenge is None:
            return
        self._fetch_properties('username', 'password')
        mac = hmac.HMAC(key=_b(self.password), digestmod=hashlib.md5)
        mac.update(challenge)
        return ''.join((_b(self.username), ' ', _b(mac.hexdigest())))

    def dispose(self):
        self.password = None


def bytes(text):
    """
    Convert Unicode text to UTF-8 encoded bytes.

    Since Python 2.6+ and Python 3+ have similar but incompatible
    signatures, this function unifies the two to keep code sane.

    :param text: Unicode text to convert to bytes
    :rtype: bytes (Python3), str (Python2.6+)
    """
    if sys.version_info < (3, 0):
        import __builtin__
        return __builtin__.bytes(text)
    else:
        import builtins
        if isinstance(text, builtins.bytes):
            return text
        if isinstance(text, list):
            return builtins.bytes(text)
        return builtins.bytes(str(text), encoding='utf-8')


def quote(text):
    """
    Enclose in quotes and escape internal slashes and double quotes.

    :param text: A Unicode or byte string.
    """
    text = bytes(text)
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


class DigestMD5Mechanism(Mechanism):
    name = 'DIGEST-MD5'
    score = 30
    allows_anonymous = False
    uses_plaintext = False

    def __init__(self, sasl, username=None, password=None, **props):
        Mechanism.__init__(self, sasl)
        self.username = username
        self.password = password
        self._rspauth_okay = False
        self._digest_uri = None
        self._a1 = None

    def dispose(self):
        self._rspauth_okay = None
        self._digest_uri = None
        self._a1 = None
        self.password = None
        self.key_hash = None
        self.realm = None
        self.nonce = None
        self.cnonce = None
        self.nc = 0

    def wrap(self, outgoing):
        return outgoing

    def unwrap(self, incoming):
        return incoming

    def response(self):
        required_props = [
         'username']
        if not getattr(self, 'key_hash', None):
            required_props.append('password')
        self._fetch_properties(*required_props)
        resp = {}
        resp['qop'] = self.qop
        if getattr(self, 'realm', None) is not None:
            resp['realm'] = quote(self.realm)
        resp['username'] = quote(bytes(self.username))
        resp['nonce'] = quote(self.nonce)
        if self.nc == 0:
            self.cnonce = bytes('%s' % random.random())[2:]
        resp['cnonce'] = quote(self.cnonce)
        self.nc += 1
        resp['nc'] = bytes('%08x' % self.nc)
        self._digest_uri = bytes(self.sasl.service) + '/' + bytes(self.sasl.host)
        resp['digest-uri'] = quote(self._digest_uri)
        a2 = 'AUTHENTICATE:' + self._digest_uri
        if self.qop != 'auth':
            a2 += ':00000000000000000000000000000000'
            resp['maxbuf'] = '16777215'
        resp['response'] = self.gen_hash(a2)
        return ','.join([bytes(k) + '=' + bytes(v) for k, v in resp.items()])

    @staticmethod
    def parse_challenge(challenge):
        ret = {}
        var = ''
        val = ''
        in_var = True
        in_quotes = False
        new = False
        escaped = False
        for c in challenge.decode('ascii'):
            if in_var:
                if c.isspace():
                    pass
                else:
                    if c == '=':
                        in_var = False
                        new = True
                    else:
                        var += c
            elif new:
                if c == '"':
                    in_quotes = True
                else:
                    val += c
                new = False
            else:
                if in_quotes:
                    if escaped:
                        escaped = False
                        val += c
                    else:
                        if c == '\\':
                            escaped = True
                        else:
                            if c == '"':
                                in_quotes = False
                            else:
                                val += c
                else:
                    if c == ',':
                        if var:
                            ret[var] = bytes(val)
                        var = ''
                        val = ''
                        in_var = True
                    else:
                        val += c

        if var:
            ret[var] = val
        return ret

    def gen_hash(self, a2):
        if not getattr(self, 'key_hash', None):
            key_hash = hashlib.md5()
            user = bytes(self.username)
            password = bytes(self.password)
            realm = bytes(self.realm)
            kh = user + ':' + realm + ':' + password
            key_hash.update(kh)
            self.key_hash = key_hash.digest()
        a1 = hashlib.md5(self.key_hash)
        a1h = ':' + self.nonce + ':' + self.cnonce
        a1.update(a1h)
        response = hashlib.md5()
        self._a1 = a1.digest()
        rv = bytes(a1.hexdigest().lower())
        rv += ':' + self.nonce
        rv += ':' + bytes('%08x' % self.nc)
        rv += ':' + self.cnonce
        rv += ':' + self.qop
        rv += ':' + bytes(hashlib.md5(a2).hexdigest().lower())
        response.update(rv)
        return bytes(response.hexdigest().lower())

    def authenticate_server(self, cmp_hash):
        a2 = ':' + self._digest_uri
        if self.qop != 'auth':
            a2 += ':00000000000000000000000000000000'
        if self.gen_hash(a2) == cmp_hash:
            self._rspauth_okay = True

    def process(self, challenge=None):
        if challenge is None:
            needed = [
             'username', 'realm', 'nonce', 'key_hash',
             'nc', 'cnonce', 'qops']
            if all(getattr(self, p, None) is not None for p in needed):
                return self.response()
            return
        challenge_dict = DigestMD5Mechanism.parse_challenge(challenge)
        if self.sasl.mutual_auth and 'rspauth' in challenge_dict:
            self.authenticate_server(challenge_dict['rspauth'])
        if 'realm' not in challenge_dict:
            self._fetch_properties('realm')
            challenge_dict['realm'] = self.realm
        for key in ('nonce', 'realm'):
            if key in challenge_dict:
                setattr(self, key, challenge_dict[key])

        self.nc = 0
        if 'qop' in challenge_dict:
            server_offered_qops = [x.strip() for x in challenge_dict['qop'].split(',')]
        else:
            server_offered_qops = [
             'auth']
        self._pick_qop(set(server_offered_qops))
        if 'maxbuf' in challenge_dict:
            self.max_buffer = min(self.sasl.max_buffer, int(challenge_dict['maxbuf']))
        return self.response()


class GSSAPIMechanism(Mechanism):
    name = 'GSSAPI'
    score = 100
    qops = QOP.all
    allows_anonymous = False
    uses_plaintext = False
    active_safe = True

    def __init__(self, sasl, principal=None, **props):
        Mechanism.__init__(self, sasl)
        self.user = None
        self._have_negotiated_details = False
        self.host = self.sasl.host
        self.service = self.sasl.service
        self.principal = principal
        self._fetch_properties('host', 'service')
        krb_service = '@'.join((self.service, self.host))
        try:
            _, self.context = kerberos.authGSSClientInit(service=krb_service, principal=self.principal)
        except TypeError:
            if self.principal is not None:
                raise Exception('Error: kerberos library does not support principal.')
            _, self.context = kerberos.authGSSClientInit(service=krb_service)

    def process(self, challenge=None):
        if not self._have_negotiated_details:
            kerberos.authGSSClientStep(self.context, '')
            _negotiated_details = kerberos.authGSSClientResponse(self.context)
            self._have_negotiated_details = True
            return base64.b64decode(_negotiated_details)
        challenge = base64.b64encode(challenge).decode('ascii')
        if self.user is None:
            ret = kerberos.authGSSClientStep(self.context, challenge)
            if ret == kerberos.AUTH_GSS_COMPLETE:
                self.user = kerberos.authGSSClientUserName(self.context)
                return ''
            response = kerberos.authGSSClientResponse(self.context)
            if response:
                response = base64.b64decode(response)
            else:
                response = ''
            return response
        kerberos.authGSSClientUnwrap(self.context, challenge)
        data = kerberos.authGSSClientResponse(self.context)
        plaintext_data = base64.b64decode(data)
        if len(plaintext_data) != 4:
            raise SASLProtocolException('Bad response from server')
        word, = struct.unpack('!I', plaintext_data)
        qop_bits = word >> 24
        max_length = word & 16777215
        server_offered_qops = QOP.names_from_bitmask(qop_bits)
        self._pick_qop(server_offered_qops)
        self.max_buffer = min(self.sasl.max_buffer, max_length)
        auth_id = self.sasl.authorization_id or self.user
        l = len(auth_id)
        fmt = '!I' + str(l) + 's'
        word = QOP.flag_from_name(self.qop) << 24 | self.max_buffer
        out = struct.pack(fmt, word, _b(auth_id))
        encoded = base64.b64encode(out).decode('ascii')
        kerberos.authGSSClientWrap(self.context, encoded)
        response = kerberos.authGSSClientResponse(self.context)
        self.complete = True
        return base64.b64decode(response)

    def wrap(self, outgoing):
        if self.qop != 'auth':
            outgoing = base64.b64encode(outgoing)
            if self.qop == 'auth-conf':
                protect = 1
            else:
                protect = 0
            kerberos.authGSSClientWrap(self.context, outgoing, None, protect)
            return base64.b64decode(kerberos.authGSSClientResponse(self.context))
        else:
            return outgoing

    def unwrap(self, incoming):
        if self.qop != 'auth':
            incoming = base64.b64encode(incoming)
            kerberos.authGSSClientUnwrap(self.context, incoming)
            conf = kerberos.authGSSClientResponseConf(self.context)
            if 0 == conf and self.qop == 'auth-conf':
                raise Exception('Error: confidentiality requested, but not honored by the server.')
            return base64.b64decode(kerberos.authGSSClientResponse(self.context))
        else:
            return incoming

    def dispose(self):
        kerberos.authGSSClientClean(self.context)


mechanisms = dict((m.name, m) for m in (
 AnonymousMechanism,
 PlainMechanism,
 CramMD5Mechanism,
 DigestMD5Mechanism))
if _have_kerberos:
    mechanisms[GSSAPIMechanism.name] = GSSAPIMechanism