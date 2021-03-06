# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trybnetic/Documents/projects/stuweparser/stuweparser/crawler.py
# Compiled at: 2017-11-02 19:34:26
# Size of source mod 2**32: 1457 bytes
"""
crawler.py provides functionality to crawl the websites of `my-stuwe.de
<https://www.my-stuwe.de/>`_
"""
from urllib.request import Request, urlopen

def crawl(url, headers=None):
    """
    Crawls the website connected to url

    - **parameters**, **types**, **return** and **return types**::
        :param url: defines the url to the website which should be crawled
        :type url: string
        :param headers: defines the headers for the request
        :type headers: dict or None
        :return: a html byte string from the url
        :rtype: bytes
        """
    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
         'Accept-Encoding': 'none', 
         'Accept-Language': 'en-US,en;q=0.8', 
         'Connection': 'keep-alive'}
    try:
        request = Request(url, headers=headers)
        with urlopen(request) as (response):
            html = response.read()
        return html
    except RuntimeError:
        print('An error occurred during HTML crawling.')