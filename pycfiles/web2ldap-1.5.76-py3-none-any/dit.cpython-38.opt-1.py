# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/dit.py
# Compiled at: 2020-05-04 07:51:53
# Size of source mod 2**32: 7774 bytes
"""
web2ldap.app.dit: do a tree search and display to the user

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0
from ldap0.dn import DNObj
import web2ldap.app.gui
from web2ldap.app.gui import dn_anchor_hash
DIT_ATTR_LIST = [
 'objectClass',
 'structuralObjectClass',
 'displayName',
 'description',
 'hasSubordinates',
 'subordinateCount',
 'numSubordinates',
 'numAllSubordinates',
 'countImmSubordinates',
 'countTotSubordinates',
 'msDS-Approx-Immed-Subordinates']

def decode_dict(d, charset):
    r = {}
    for k, v in d.items():
        r[k] = [value.decode(charset) for value in v]
    else:
        return r


def dit_html(app, anchor_dn, dit_dict, entry_dict, max_levels):
    """
    Outputs HTML representation of a directory information tree (DIT)
    """

    def meta_results(d):
        """
        Side effect! This removes meta result data from d!
        """
        try:
            size_limit = d['_sizelimit_']
        except KeyError:
            size_limit = False
        else:
            del d['_sizelimit_']
        return size_limit

    assert isinstance(anchor_dn, DNObj), ValueError('Expected anchor_dn to be DNObj, got %r' % (anchor_dn,))
    res = [
     '<dl>']
    for dn, d in dit_dict.items():
        if not isinstance(dn, DNObj):
            raise AssertionError(ValueError('Expected dn to be DNObj, got %r' % (dn,)))
        else:
            size_limit = meta_results(d)
            if dn:
                rdn = dn.rdn()
            else:
                rdn = 'Root DSE'
        try:
            node_entry = entry_dict[dn]
        except KeyError:
            try:
                ldap_res = app.ls.l.read_s((str(dn)), attrlist=DIT_ATTR_LIST)
            except ldap0.LDAPError:
                node_entry = {}
            else:
                node_entry = {} if ldap_res is None else ldap_res.entry_s
        else:
            if size_limit:
                partial_str = '<strong>...</strong>'
            else:
                partial_str = ''
            hasSubordinates = node_entry.get('hasSubordinates', ['TRUE'])[0].upper() == 'TRUE'
        try:
            subordinateCountFlag = int(node_entry.get('subordinateCount', node_entry.get('numAllSubordinates', node_entry.get('msDS-Approx-Immed-Subordinates', ['1'])))[0])
        except ValueError:
            subordinateCountFlag = 1
        else:
            has_subordinates = hasSubordinates and subordinateCountFlag
            try:
                display_name_list = [app.form.utf2display(node_entry['displayName'][0]), partial_str]
            except KeyError:
                display_name_list = [
                 app.form.utf2display(str(rdn)), partial_str]
            else:
                display_name = ''.join(display_name_list)
                title_msg = '\r\n'.join((
                 str(dn) or 'Root DSE', node_entry.get('structuralObjectClass', [''])[0]) + tuple(node_entry.get('description', [])))
                dn_anchor_id = dn_anchor_hash(dn)
                res.append('<dt id="%s">' % app.form.utf2display(dn_anchor_id))
                if has_subordinates:
                    if dn == anchor_dn:
                        link_text = '&lsaquo;&lsaquo;'
                        next_dn = dn.parent()
                    else:
                        link_text = '&rsaquo;&rsaquo;'
                        next_dn = dn
                    res.append(app.anchor('dit',
                      link_text, [
                     (
                      'dn', str(next_dn))],
                      title=('Browse from %s' % (str(next_dn),)),
                      anchor_id=dn_anchor_id))
                else:
                    res.append('&nbsp;&nbsp;&nbsp;&nbsp;')
                res.append('<span title="%s">%s</span>' % (
                 app.form.utf2display(title_msg),
                 display_name))
                res.append(app.anchor('read',
                  '&rsaquo;', [
                 (
                  'dn', str(dn))],
                  title='Read entry'))
                res.append('</dt>')
                res.append('<dd>')
                if max_levels:
                    if d:
                        res.extend(dit_html(app, anchor_dn, d, entry_dict, max_levels - 1))
                res.append('</dd>')
    else:
        res.append('</dl>')
        return res


def w2l_dit(app):
    dit_dict = {}
    entry_dict = {}
    root_dit_dict = dit_dict
    dn_levels = len(app.dn_obj)
    dit_max_levels = app.cfg_param('dit_max_levels', 10)
    cut_off_levels = max(0, dn_levels - dit_max_levels)
    for i in range(1, dn_levels - cut_off_levels + 1):
        search_base = app.dn_obj.slice(dn_levels - cut_off_levels - i, None)
        dit_dict[search_base] = {}
        try:
            msg_id = app.ls.l.search((str(search_base)),
              (ldap0.SCOPE_ONELEVEL),
              '(objectClass=*)',
              attrlist=DIT_ATTR_LIST,
              timeout=(app.cfg_param('dit_search_timelimit', 10)),
              sizelimit=(app.cfg_param('dit_search_sizelimit', 50)))
            for ldap_result in app.ls.l.results(msg_id):
                if ldap_result.rtype == ldap0.RES_SEARCH_REFERENCE:
                    pass
                else:
                    for res in ldap_result.rdata:
                        entry_dict[res.dn_o] = res.entry_s
                        dit_dict[search_base][res.dn_o] = {}

        except (
         ldap0.TIMEOUT,
         ldap0.SIZELIMIT_EXCEEDED,
         ldap0.TIMELIMIT_EXCEEDED,
         ldap0.ADMINLIMIT_EXCEEDED,
         ldap0.NO_SUCH_OBJECT,
         ldap0.INSUFFICIENT_ACCESS,
         ldap0.PARTIAL_RESULTS,
         ldap0.REFERRAL):
            dit_dict[search_base]['_sizelimit_'] = True
        else:
            dit_dict[search_base]['_sizelimit_'] = False
        dit_dict = dit_dict[search_base]

    if root_dit_dict:
        outf_lines = dit_html(app, app.dn_obj, root_dit_dict, entry_dict, dit_max_levels)
    else:
        if app.dn:
            outf_lines = [
             'No results.']
        else:
            outf_lines = [
             '<p>No results for root search.</p>']
            for naming_context in app.ls.namingContexts:
                outf_lines.append('<p>%s %s</p>' % (
                 app.anchor('dit',
                   '&rsaquo;&rsaquo;', (
                  (
                   'dn', str(naming_context)),),
                   title=('Display tree beneath %s' % (naming_context,))),
                 app.form.utf2display(str(naming_context))))
            else:
                app.simple_message('Tree view',
                  ('\n        <h1>Directory Information Tree</h1>\n        <div id="DIT">%s</div>\n        ' % '\n'.join(outf_lines)),
                  main_menu_list=(web2ldap.app.gui.main_menu(app)),
                  context_menu_list=[])