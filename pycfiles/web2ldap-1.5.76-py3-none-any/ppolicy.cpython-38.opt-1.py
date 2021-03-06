# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/ppolicy.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 8096 bytes
"""
web2ldap plugin classes for attributes defined in draft-behera-ldap-password-policy
"""
import time, datetime
from ldap0 import LDAPError
import web2ldap.app.searchform
from web2ldap.utctime import strptime
from web2ldap.app.schema.syntaxes import SelectList, DynamicDNSelectList, Timespan, GeneralizedTime, syntax_registry
from web2ldap.app.plugins.quirks import UserPassword
from web2ldap import cmp

class PwdCheckQuality(SelectList):
    oid = 'PwdCheckQuality-oid'
    oid: str
    desc = 'Password quality checking enforced'
    desc: str
    attr_value_dict = {'0':'quality checking not be enforced',  '1':'quality checking enforced, accepting un-checkable passwords', 
     '2':'quality checking always enforced'}


syntax_registry.reg_at(PwdCheckQuality.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.5'])

class PwdAttribute(SelectList):
    oid = 'PwdAttribute-oid'
    oid: str
    desc = 'Password attribute'
    desc: str
    attr_value_dict = {'2.5.4.35': 'userPassword'}

    def _validate(self, attrValue: bytes) -> bool:
        return not attrValue or attrValue.lower() in {b'2.5.4.35', b'userpassword'}


syntax_registry.reg_at(PwdAttribute.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.1'])

class PwdPolicySubentry(DynamicDNSelectList):
    oid = 'PwdPolicySubentry-oid'
    oid: str
    desc = 'DN of the pwdPolicy entry to be used for a certain entry'
    desc: str
    ldap_url = 'ldap:///_??sub?(|(objectClass=pwdPolicy)(objectClass=ds-cfg-password-policy))'


syntax_registry.reg_at(PwdPolicySubentry.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.23'])

class PwdMaxAge(Timespan):
    oid = 'PwdMaxAge-oid'
    oid: str
    desc = 'pwdPolicy entry: Maximum age of user password'
    desc: str
    link_text = 'Search expired'
    title_text = 'Search for entries with this password policy and expired password'

    @staticmethod
    def _search_timestamp(diff_secs):
        return time.strftime('%Y%m%d%H%M%SZ', time.gmtime(time.time() - diff_secs))

    def _timespan_search_params(self):
        return (
         ('search_attr', 'pwdChangedTime'),
         (
          'search_option', web2ldap.app.searchform.SEARCH_OPT_LE_THAN),
         (
          'search_string', self._search_timestamp(int(self.av_u.strip()))))

    def display(self, valueindex=0, commandbutton=False) -> str:
        ts_dv = Timespan.display(self, valueindex, commandbutton)
        ocs = self._entry.object_class_oid_set()
        if not commandbutton or 'pwdPolicy' not in ocs:
            return ts_dv
        try:
            ts_search_params = self._timespan_search_params()
        except (ValueError, KeyError):
            return ts_dv
        else:
            search_link = self._app.anchor('searchform',
              (self.link_text), ((
             (
              'dn', self._dn),
             ('searchform_mode', 'adv'),
             ('search_attr', 'pwdPolicySubentry'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             (
              'search_string', self._dn)) + ts_search_params),
              title=(self.title_text))
            return ' '.join((ts_dv, search_link))


syntax_registry.reg_at(PwdMaxAge.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.3'])

class PwdExpireWarning(PwdMaxAge):
    oid = 'PwdExpireWarning-oid'
    oid: str
    desc = 'pwdPolicy entry: Password warning period'
    desc: str
    link_text = 'Search soon to expire'
    title_text = 'Search for entries with this password policy and soon to expire password'

    def _timespan_search_params(self):
        pwd_expire_warning = int(self.av_u.strip())
        pwd_max_age = int(self._entry['pwdMaxAge'][0].decode('ascii').strip())
        warn_timestamp = pwd_max_age - pwd_expire_warning
        return (
         ('search_attr', 'pwdChangedTime'),
         (
          'search_option', web2ldap.app.searchform.SEARCH_OPT_GE_THAN),
         (
          'search_string', self._search_timestamp(pwd_max_age)),
         ('search_attr', 'pwdChangedTime'),
         (
          'search_option', web2ldap.app.searchform.SEARCH_OPT_LE_THAN),
         (
          'search_string', self._search_timestamp(warn_timestamp)))


syntax_registry.reg_at(PwdExpireWarning.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.7'])

class PwdAccountLockedTime(GeneralizedTime):
    oid = 'PwdAccountLockedTime-oid'
    oid: str
    desc = 'user entry: time that the account was locked'
    desc: str
    magic_values = {'000001010000Z': 'permanently locked'}

    def _validate(self, attrValue: bytes) -> bool:
        return attrValue in self.magic_values or GeneralizedTime._validate(self, attrValue)

    def display(self, valueindex=0, commandbutton=False) -> str:
        gt_disp_html = GeneralizedTime.display(self, valueindex, commandbutton)
        if self._av in self.magic_values:
            return '%s (%s)' % (gt_disp_html, self.magic_values[self._av])
        return gt_disp_html


syntax_registry.reg_at(PwdAccountLockedTime.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.17'])

class PwdChangedTime(GeneralizedTime):
    oid = 'PwdChangedTime-oid'
    oid: str
    desc = 'user entry: Last password change time'
    desc: str
    time_divisors = Timespan.time_divisors

    def display(self, valueindex=0, commandbutton=False) -> str:
        gt_disp_html = GeneralizedTime.display(self, valueindex, commandbutton)
        try:
            pwd_changed_dt = strptime(self._av)
        except ValueError:
            return gt_disp_html

        try:
            pwd_policy_subentry_dn = self._entry['pwdPolicySubentry'][0].decode(self._app.ls.charset)
        except KeyError:
            return gt_disp_html

        try:
            pwd_policy = self._app.ls.l.read_s(pwd_policy_subentry_dn,
              filterstr='(objectClass=pwdPolicy)',
              attrlist=[
             'pwdMaxAge', 'pwdExpireWarning'])
        except LDAPError:
            return gt_disp_html

        try:
            pwd_max_age_secs = int(pwd_policy.entry_s['pwdMaxAge'][0])
        except KeyError:
            expire_msg = 'will never expire'
        except ValueError:
            return gt_disp_html
        else:
            if pwd_max_age_secs:
                pwd_max_age = datetime.timedelta(seconds=pwd_max_age_secs)
                current_time = datetime.datetime.utcnow()
                expire_dt = pwd_changed_dt + pwd_max_age
                expired_since = (expire_dt - current_time).total_seconds()
                expire_cmp = cmp(expire_dt, current_time)
                expire_msg = '%s %s (%s %s)' % (
                 {-1:'expired since', 
                  0:'', 
                  1:'will expire'}[expire_cmp],
                 expire_dt.strftime('%c'),
                 self._app.form.utf2display(web2ldap.app.gui.ts2repr(self.time_divisors, ' ', abs(expired_since))),
                 {-1:'ago', 
                  0:'', 
                  1:'ahead'}[expire_cmp])
            else:
                expire_msg = 'will never expire'


syntax_registry.reg_at(PwdChangedTime.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.16'])
syntax_registry.reg_at(UserPassword.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.20'])
syntax_registry.reg_at(Timespan.oid, [
 '1.3.6.1.4.1.42.2.27.8.1.2',
 '1.3.6.1.4.1.42.2.27.8.1.12',
 '1.3.6.1.4.1.42.2.27.8.1.10'])
syntax_registry.reg_syntaxes(__name__)