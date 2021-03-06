# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_service/plugins/password/ldap3/__init__.py
# Compiled at: 2020-02-24 16:25:03
# Size of source mod 2**32: 6369 bytes
"""
ekca_service.plugins.password.ldap3 - Module package for LDAP password checker plugins
"""
import ssl, ldap3
import ldap3.utils.conv as escape_ldapfilter_chars
from ldap3.core.exceptions import LDAPException, LDAPInvalidCredentialsResult, LDAPNoSuchObjectResult
from ekca_service.plugins.password.base import PasswordCheckFailed, PasswordChecker

def escape_rdn(val):
    """
    Escape all DN special characters found in s
    with a back-slash (see RFC 4514, section 2.4)
    """
    if not isinstance(val, str):
        raise AssertionError(TypeError('Expected str (unicode) for val, got %r' % (val,)))
    else:
        return val or val
    val = val.replace('\\', '\\\\')
    val = val.replace(',', '\\,')
    val = val.replace('+', '\\+')
    val = val.replace('"', '\\"')
    val = val.replace('<', '\\<')
    val = val.replace('>', '\\>')
    val = val.replace(';', '\\;')
    val = val.replace('=', '\\=')
    val = val.replace('\x00', '\\\x00')
    if val[-1:] == ' ':
        val = ''.join((val[:-1], '\\ '))
    if val[0:1] == '#' or val[0:1] == ' ':
        val = ''.join(('\\', val))
    return val


def ldap_connect_and_bind(ldap_uri, bind_dn, bind_pw, client_strategy, auto_bind=True, ca_certs=None):
    """
    Connect and bind to LDAP server
    """
    ldap_server = ldap3.Server(ldap_uri,
      get_info=(ldap3.NONE),
      tls=ldap3.Tls(validate=(ssl.CERT_REQUIRED),
      version=(ssl.PROTOCOL_TLSv1_2),
      ca_certs_file=ca_certs))
    if not bind_pw:
        raise ValueError('Empty value for bind_pw disallowed!')
    ldap_conn = ldap3.Connection(ldap_server,
      auto_bind=auto_bind,
      user=bind_dn,
      password=bind_pw,
      raise_exceptions=True,
      authentication=(ldap3.SIMPLE),
      client_strategy=client_strategy,
      auto_referrals=False,
      read_only=True,
      lazy=False,
      check_names=False,
      fast_decoder=True,
      receive_timeout=5,
      auto_escape=False,
      auto_encode=True,
      collect_usage=False)
    return ldap_conn


class LDAPPasswordChecker(PasswordChecker):
    __doc__ = '\n    Password check done by sending a simple bind request to the server\n    '

    def __init__(self, cfg, logger):
        PasswordChecker.__init__(self, cfg, logger)
        self.user_attrs = []
        if self._cfg.get('SSH_FROMIP_METHOD', '').lower().startswith('user:'):
            ipaddr_attr = self._cfg['SSH_FROMIP_METHOD'][5:].strip()
            self.user_attrs.append(ipaddr_attr)
        cert_perms_attr = self._cfg.get('SSH_CERT_PERMISSIONS_ATTR', None)
        if cert_perms_attr:
            self.user_attrs.append(cert_perms_attr)
        self.user_attrs = self.user_attrs or ['1.1']

    def _ldap_conn(self):
        """
        Opens a new service LDAP connection
        """
        ldap_conn = ldap_connect_and_bind((self._cfg['LDAP_URI']),
          (self._cfg.get('LDAP_BIND_DN', '')),
          (self._cfg.get('LDAP_BIND_PW', '')),
          (ldap3.ASYNC),
          ca_certs=(self._cfg['LDAP_CA_CERT']))
        self._log.debug('Connected to %r as %r', self._cfg['LDAP_URI'], ldap_conn.extend.standard.who_am_i())
        return ldap_conn

    def check(self, user_name, password, remote_addr):
        """
        Check password of user
        """
        if not password:
            raise PasswordCheckFailed('Empty password for user name {!r}'.format(user_name))
        user_entry = None
        if self._cfg.get('LDAP_USER_DN', None) is not None:
            bind_dn = self._cfg['LDAP_USER_DN'].format(username=(escape_rdn(user_name)))
        else:
            ldap_conn = self._ldap_conn()
            try:
                msg_id = ldap_conn.search(search_base=(self._cfg['LDAP_SEARCH_BASE']),
                  search_scope=(self._cfg['LDAP_SEARCH_SCOPE']),
                  search_filter=self._cfg['LDAP_SEARCH_FILTER'].format(username=(escape_ldapfilter_chars(user_name)),
                  raddr=(escape_ldapfilter_chars(remote_addr))),
                  attributes=(self.user_attrs),
                  size_limit=2)
                ldap_entries, ldap_result = ldap_conn.get_response(msg_id)
            except LDAPNoSuchObjectResult:
                raise PasswordCheckFailed('No such object searching {!r}'.format(self._cfg['LDAP_SEARCH_BASE']))

            if not len(ldap_entries) != 1:
                if ldap_result['result']:
                    raise PasswordCheckFailed('Invalid LDAP results for user name {!r}: {!r} {!r}'.format(user_name, ldap_result, ldap_entries[:10]))
                user_entry = ldap_entries[0]
                bind_dn = user_entry['dn']
            else:
                try:
                    user_conn = ldap_connect_and_bind((self._cfg['LDAP_URI']),
                      bind_dn,
                      password,
                      (ldap3.ASYNC),
                      auto_bind=False,
                      ca_certs=(self._cfg['LDAP_CA_CERT']))
                    bind_res = user_conn.bind()
                except LDAPInvalidCredentialsResult as ldap_err:
                    try:
                        raise PasswordCheckFailed('Bind as {!r} failed: {!r}'.format(bind_dn, ldap_err))
                    finally:
                        ldap_err = None
                        del ldap_err

            if bind_res != True:
                raise PasswordCheckFailed('Bind as {!r} did not return True'.format(bind_dn))
            if user_entry is None:
                user_entry = {}
            return user_entry.get('attributes', {})