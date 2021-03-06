# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wsgixml/util.py
# Compiled at: 2006-09-19 09:39:26
from urllib import quote

class iterwrapper:
    """
    Wraps the response body iterator from the application to meet WSGI
    requirements.
    """

    def __init__(self, wrapped, responder):
        """
        wrapped - the iterator coming from the application
        response_chunk_handler - a callable for any processing of a
            response body chunk before passing it on to the server.
        """
        self._wrapped = iter(wrapped)
        self._responder = responder(self._wrapped)
        if hasattr(wrapped, 'close'):
            self.close = self._wrapped.close

    def __iter__(self):
        return self

    def next(self):
        return self._responder.next()


def get_request_url(environ):
    url = environ['wsgi.url_scheme'] + '://'
    if environ.get('HTTP_HOST'):
        url += environ['HTTP_HOST']
    else:
        url += environ['SERVER_NAME']
        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
                url += ':' + environ['SERVER_PORT']
        elif environ['SERVER_PORT'] != '80':
            url += ':' + environ['SERVER_PORT']
    url += quote(environ.get('SCRIPT_NAME', ''))
    url += quote(environ.get('PATH_INFO', ''))
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    return url