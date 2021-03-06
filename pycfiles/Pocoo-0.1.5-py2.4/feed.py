# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/feed.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.utils.feed
    ~~~~~~~~~~~~~~~~

    Provides a Feed class to create RSS Feeds.

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
import time
from datetime import datetime
from xml.dom.minidom import Document
from email.Utils import formatdate

class Feed(object):
    __module__ = __name__

    def __init__(self, ctx, title, description, link):
        self.ctx = ctx
        self.title = title
        self.description = description
        self.link = ctx.make_external_url(link)
        self.items = []
        self._last_update = None
        return

    def add_item(self, title, author, link, description, pub_date):
        if self._last_update is None or pub_date > self._last_update:
            self._last_update = pub_date
        date = pub_date or datetime.utcnow()
        date = formatdate(time.mktime(date.timetuple()) + date.microsecond / 1000000.0)
        self.items.append({'title': title, 'author': author, 'link': self.ctx.make_external_url(link), 'description': description, 'pubDate': date})
        return

    def generate(self):
        doc = Document()
        Element = doc.createElement
        Text = doc.createTextNode
        rss = doc.appendChild(Element('rss'))
        rss.setAttribute('version', '2.0')
        channel = rss.appendChild(Element('channel'))
        for key in ('title', 'description', 'link'):
            value = getattr(self, key)
            channel.appendChild(Element(key)).appendChild(Text(value))

        date = self._last_update or datetime.utcnow()
        date = formatdate(time.mktime(date.timetuple()) + date.microsecond / 1000000.0)
        channel.appendChild(Element('pubDate')).appendChild(Text(date))
        for item in self.items:
            d = Element('item')
            for key in ('title', 'author', 'link', 'description', 'pubDate'):
                d.appendChild(Element(key)).appendChild(Text(item[key]))

            channel.appendChild(d)

        return doc.toxml('utf-8')

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.link)