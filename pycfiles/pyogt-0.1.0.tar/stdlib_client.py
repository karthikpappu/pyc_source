# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/network/stdlib_client.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import urllib2, os
from pyogp.lib.base.exc import HTTPError
from webob import Request, Response

class StdLibClient(object):
    """ implement a REST client on top of urllib2 """
    __module__ = __name__

    def GET(self, url, headers={}):
        """ GET a resource """
        request = urllib2.Request(url, headers=headers)
        try:
            result = urllib2.urlopen(request)
        except urllib2.HTTPError, error:
            raise HTTPError(error.code, error.msg, error.fp)

        headerlist = result.headers.items()
        status = '%s %s' % (result.code, result.msg)
        response = Response(body=result.read(), status=status, headerlist=headerlist)
        return response

    def POST(self, url, data, headers={}):
        """ POST data to a resource """
        request = urllib2.Request(url, data, headers=headers)
        try:
            result = urllib2.urlopen(request)
        except urllib2.HTTPError, error:
            raise HTTPError(error.code, error.msg, error.fp)

        headerlist = result.headers.items()
        status = '%s %s' % (result.code, result.msg)
        response = Response(body=result.read(), status=status, headerlist=headerlist)
        return response