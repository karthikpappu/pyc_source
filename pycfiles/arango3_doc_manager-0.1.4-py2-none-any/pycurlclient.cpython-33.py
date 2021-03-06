# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../arango/clients/pycurlclient.py
# Compiled at: 2013-09-26 14:12:21
# Size of source mod 2**32: 2833 bytes
try:
    import StringIO
except ImportError:
    from io import StringIO

import pycurl
from .base import RequestsBase
__all__ = ('PyCurlClient', )
CONTINUE_HEADER = 'HTTP/1.1 100 (Continue)'

def performer(func):
    """
    Decorator to simplify work with PyCURL
    """

    def wrap(cls, *args, **kwargs):
        client, buf = func(cls, *args, **kwargs)
        return PyCurlClient.build_response(*PyCurlClient.perform(client, buf))

    return wrap


class PyCurlClient(RequestsBase):
    """PyCurlClient"""
    DEBUG = False
    IPRESOLVE = pycurl.IPRESOLVE_V4
    encoding = 'utf-8'

    @classmethod
    def client(cls, url):
        client = pycurl.Curl()
        buf = StringIO.StringIO()
        if cls.DEBUG:
            client.setopt(pycurl.VERBOSE, True)
        client.setopt(pycurl.IPRESOLVE, cls.IPRESOLVE)
        client.setopt(pycurl.URL, url)
        client.setopt(pycurl.HEADER, 1)
        client.setopt(pycurl.NOSIGNAL, 1)
        client.setopt(pycurl.WRITEFUNCTION, buf.write)
        return (
         client, buf)

    @classmethod
    def perform(cls, client, buf):
        client.perform()
        client.close()
        return cls.parse_response(buf)

    @classmethod
    def parse_response(cls, buf):
        response = buf.getvalue()
        if CONTINUE_HEADER in response:
            response = response.split('\r\n\r\n', 1)[(-1)]
        headers, body = response.split('\r\n\r\n', 1)
        status, heads = headers.split('\r\n', 1)
        headers = dict([map(str.strip, h.split(':', 1)) for h in heads.split('\r\n') if h])
        proto, status, message = status.split(' ', 2)
        return (
         int(status), message, headers, body)

    @classmethod
    @performer
    def get(cls, url):
        return cls.client(url)

    @classmethod
    @performer
    def post(cls, url, data=None):
        client, buf = cls.client(url)
        client.setopt(pycurl.POST, True)
        data = data or ''
        client.setopt(pycurl.POSTFIELDS, data.encode(cls.encoding))
        return (
         client, buf)

    @classmethod
    @performer
    def delete(cls, url, data=None):
        client, buf = cls.client(url)
        client.setopt(pycurl.CUSTOMREQUEST, 'delete')
        return (
         client, buf)

    @classmethod
    @performer
    def put(cls, url, data=None):
        data = data or ''
        content = StringIO.StringIO(data.encode(cls.encoding))
        client, buf = cls.client(url)
        client.setopt(pycurl.PUT, True)
        client.setopt(pycurl.UPLOAD, True)
        client.setopt(pycurl.READFUNCTION, content.read)
        client.setopt(pycurl.INFILESIZE, len(data))
        return (
         client, buf)