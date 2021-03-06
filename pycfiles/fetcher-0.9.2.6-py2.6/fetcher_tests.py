# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\fetcher_tests.py
# Compiled at: 2010-12-21 07:53:49
__created__ = '2009/09/27'
__author__ = 'xlty.0512@gmail.com'
__author__ = '牧唐 杭州'
from fetcher import *
from unittest import TestCase
import BaseHTTPServer, SimpleHTTPServer
from threading import Thread
import urllib, urlparse, logging

class MySimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        ps = self.path.split('?')
        if len(ps) > 1:
            ps = map(lambda x: x.split('='), ps[(-1)].split('&'))
            if ps:
                ps = dict(ps)
        code = type = leng = text = None
        if 'code' in ps:
            code = int(ps['code'][(-1)])
        if 'type' in ps:
            type = ps['type'][(-1)]
        if 'len' in ps:
            leng = int(ps['len'][(-1)])
        if 'text' in ps:
            text = ps['text'][(-1)]
        if not text:
            text = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>\n\n                <title>Directory listing for</title>\n\n                <body>\n                                                淘宝\n\n                                                中测定发生发生的发生的fsd发送方式地方\n                                                我是中文我是中文, 巍峨哦是中\n                <h2>Directory listing for</h2>\n\n                <hr>\n<ul>\n\n                <img src="./a.jpg"/>\n                </body>\n                </html>').encode('gb2312')
        leng = len(text)
        self.send_response(code or 200)
        self.send_header('Content-type', type or 'text/plain')
        self.send_header('Content-Length', leng or 0)
        self.end_headers()
        self.wfile.write(text)
        self.wfile.close()
        return

    def do_POST(self):
        code = type = leng = text = None
        if 'Content-Length' in self.headers:
            cl = int(self.headers['Content-Length'])
            data = self.rfile.read(cl)
            ps = urlparse.parse_qs(data)
            if 'code' in ps:
                code = int(ps['code'][(-1)])
            if 'type' in ps:
                type = ps['type'][(-1)]
            if 'text' in ps:
                text = ps['text'][(-1)]
            if not text:
                text = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>\n\n                    <title>Directory listing for</title>\n\n                    <body>\n                                                            淘宝\n\n                                                            中测定发生发生的发生的fsd发送方式地方\n                                                        我是中文我是中文, 巍峨哦是中\n                    <h2>Directory listing for</h2>\n\n                    <hr>\n<ul>\n\n                    <img src="./a.jpg"/>\n                    </body>\n                    </html>').encode('gb2312')
            leng = len(text)
        self.send_response(code or 200)
        self.send_header('r-type', 'post')
        self.send_header('Content-type', type or 'text/plain')
        self.send_header('Content-Length', leng or 0)
        self.end_headers()
        self.wfile.write(text)
        self.wfile.close()
        return


def run():

    def run_while_true(server_class=BaseHTTPServer.HTTPServer, handler_class=MySimpleHTTPRequestHandler):
        server_address = ('', 8199)
        httpd = server_class(server_address, handler_class)
        while 1:
            httpd.handle_request()

    run_while_true()


t = Thread(target=run)
t.daemon = True
t.start()

def test_fetcher_fetch():
    fetcher = Fetcher()
    d = fetcher.fetch('http://localhost:8199')
    assert d.code == 200


def test_fetcher_post():
    """
    post request
    """
    fetcher = Fetcher()
    d = fetcher.fetch('http://localhost:8199', 'code=200&pwd=2')
    assert 'r-type' in d.headers
    assert 'post' in d.headers['r-type']
    assert d.code == 200


def test_fetcher_post_local():
    """
    post request
    """
    fetcher = Fetcher()
    d = fetcher.fetch('http://localhost:8199', urllib.urlencode({'wo': 1, '看': 'v'}))
    assert d.code == 200


def test_fetcher_head():
    fetcher = Fetcher()
    d = fetcher.head('http://localhost:8199')
    logging.info(d)
    assert 'Content-Type' in d


def test_charset():
    fetcher = Fetcher()
    d = fetcher.fetch('http://localhost:8199')
    assert 'gb2312' == FetcherUtil.charset(d.content)[0]


def test_decode():
    fetcher = Fetcher()
    d = fetcher.fetch('http://localhost:8199')
    assert '淘宝' not in d.content
    c = FetcherUtil.decode(d.content, 'utf-8')
    assert '淘宝' in c


def test_image_fetcher():
    fetcher = ImageFetcher()
    images = fetcher.fetch('http://localhost:8199/f.htm?x=1&y=2')
    assert images == ['http://localhost:8199/./a.jpg']