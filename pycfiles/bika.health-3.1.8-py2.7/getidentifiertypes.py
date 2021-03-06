# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/identifiertype/getidentifiertypes.py
# Compiled at: 2014-12-12 07:13:54
from bika.health import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser import BrowserView
from bika.lims.permissions import *
from operator import itemgetter
import json, plone

class ajaxGetIdentifierTypes(BrowserView):
    """ Identifier types vocabulary source for jquery combo dropdown box
    """

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)
        searchTerm = 'searchTerm' in self.request and self.request['searchTerm'].lower() or ''
        page = self.request['page']
        nr_rows = self.request['rows']
        sord = self.request['sord']
        sidx = self.request['sidx']
        rows = []
        brains = self.bika_setup_catalog(portal_type='IdentifierType', inactive_state='active')
        if brains and searchTerm:
            brains = [ p for p in brains if p.Title.lower().find(searchTerm) > -1 ]
        for p in brains:
            rows.append({'IdentifierType': p.Title, 'Description': p.Description})

        rows = sorted(rows, cmp=lambda x, y: cmp(x.lower(), y.lower()), key=itemgetter(sidx and sidx or 'IdentifierType'))
        if sord == 'desc':
            rows.reverse()
        pages = len(rows) / int(nr_rows)
        pages += divmod(len(rows), int(nr_rows))[1] and 1 or 0
        ret = {'page': page, 'total': pages, 
           'records': len(rows), 
           'rows': rows[(int(page) - 1) * int(nr_rows):int(page) * int(nr_rows)]}
        return json.dumps(ret)