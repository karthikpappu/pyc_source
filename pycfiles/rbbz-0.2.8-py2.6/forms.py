# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbbz/forms.py
# Compiled at: 2014-07-11 22:40:04
from django import forms
from djblets.siteconfig.forms import SiteSettingsForm

class BugzillaAuthSettingsForm(SiteSettingsForm):
    auth_bz_xmlrpc_url = forms.CharField(label='Bugzilla XMLRPC URL', help_text="URL for your Bugzilla installation's XMLRPC interface", required=True)

    class Meta:
        title = 'Bugzilla Backend Settings'