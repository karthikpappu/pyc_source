# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plemp/progressclient.py
# Compiled at: 2010-10-21 11:19:43
__doc__ = "\nProgress-reporting HTTP client for twisted. Based on postr's proxyclient.\n"
from twisted.internet import reactor
from postr import proxyclient as client

class ProgressProducer(object):

    def __init__(self, consumer, data, chunksize, callback):
        self.data = data
        self.callback = callback
        self.chunksize = chunksize
        self.totalSize = len(data)
        self.consumer = consumer
        self.callback(0.0)

    def resumeProducing(self):
        if self.data:
            progress = 1 - len(self.data) / float(self.totalSize)
            self.callback(progress)
            chunk = self.data[:self.chunksize]
            self.data = self.data[self.chunksize:]
            self.consumer.write(chunk)

    def stopProducing(self):
        self.callback(1.0)


class HTTPPageGetter(client.HTTPPageGetter):
    chunksize = 8192
    progressCallback = None

    def connectionMade(self):
        method = getattr(self.factory, 'method', 'GET')
        self.sendCommand(method, self.factory.path)
        self.sendHeader('Host', self.factory.headers.get('host', self.factory.host))
        self.sendHeader('User-Agent', self.factory.agent)
        if self.factory.cookies:
            l = []
            for (cookie, cookval) in self.factory.cookies.items():
                l.append('%s=%s' % (cookie, cookval))

            self.sendHeader('Cookie', ('; ').join(l))
        data = getattr(self.factory, 'postdata', None)
        if data is not None:
            self.sendHeader('Content-Length', str(len(data)))
        for (key, value) in self.factory.headers.items():
            if key.lower() != 'content-length':
                self.sendHeader(key, value)

        self.endHeaders()
        self.headers = {}
        if data is not None:
            if not self.progressCallback:
                self.transport.write(data)
            else:
                self.transport.registerProducer(ProgressProducer(self.transport, data, self.chunksize, self.progressCallback), False)
        return


class HTTPClientFactory(client.HTTPClientFactory):
    protocol = HTTPPageGetter
    progressCallback = None

    def __init__(self, url, method='GET', postdata=None, headers=None, agent='Twisted PageGetter', timeout=0, cookies=None, followRedirect=1, proxy=None, progressCallback=None, chunksize=8192):
        client.HTTPClientFactory.__init__(self, url, method, postdata, headers, agent, timeout, cookies, followRedirect, proxy)
        self.protocol.progressCallback = progressCallback
        self.protocol.chunksize = chunksize


def getPage(url, contextFactory=None, proxy=None, *args, **kwargs):
    """Download a web page as a string.

    Download a page. Return a deferred, which will callback with a
    page (as a string) or errback with a description of the error.

    See HTTPClientFactory to see what extra args can be passed.
    """
    if proxy:
        (scheme, host, port, path) = client._parse(proxy)
        kwargs['proxy'] = proxy
    else:
        (scheme, host, port, path) = client._parse(url)
    factory = HTTPClientFactory(url, *args, **kwargs)
    if scheme == 'https':
        from twisted.internet import ssl
        if contextFactory is None:
            contextFactory = ssl.ClientContextFactory()
        reactor.connectSSL(host, port, factory, contextFactory)
    else:
        reactor.connectTCP(host, port, factory)
    return factory.deferred