# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/news.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node
from .utils import parse_date

@six.python_2_unicode_compatible
class News(Node):
    """Represents a News on CrunchBase"""
    KNOWN_PROPERTIES = [
     'title',
     'author',
     'posted_on',
     'url',
     'created_at',
     'updated_at']

    def _coerce_values(self):
        for attr in ['posted_on']:
            if getattr(self, attr, None):
                setattr(self, attr, parse_date(getattr(self, attr)))

        return

    def __str__(self):
        return ('{title} by {author} on {posted_on}').format(title=self.title, author=self.author, posted_on=self.posted_on)

    def __repr__(self):
        return self.__str__()