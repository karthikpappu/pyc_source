# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tei_transformer/etreemethods.py
# Compiled at: 2016-02-15 02:46:51
# Size of source mod 2**32: 2359 bytes
from lxml import etree

class EtreeMethods:
    __doc__ = 'A mixin class providing some useful methods for etree elements.'

    def __eq__(self, other):
        if not isinstance(other, EtreeMethods):
            return NotImplemented
        return self.descendants_count() == other.descendants_count()

    def __lt__(self, other):
        if not isinstance(other, EtreeMethods):
            return NotImplemented
        return self.descendants_count() < other.descendants_count()

    def __str__(self):
        return etree.tounicode(self, with_tail=False)

    def descendants_count(self):
        """Number of descendants"""
        if len(self) == 0:
            return 0
        return sum(1 for _ in self.iterdescendants())

    @property
    def localname(self):
        """Tag name without namespace"""
        return etree.QName(self).localname

    def delete(self):
        """Remove this tag from the tree, preserving its tail"""
        parent = self.add_to_previous(self.tail)
        parent.remove(self)

    def unwrap(self):
        """Replace tag with contents, including children"""
        children = list(self.iterchildren(reversed=True))
        if not len(children):
            self.replace_w_str(self.text)
        else:
            parent = self.getparent()
            index = parent.index(self)
            last_child = children[(-1)]
            last_child.tail = self.textjoin(last_child.tail, self.tail)
            parent = self.add_to_previous(self.textjoin(self.text, self.tail))
            for child in children:
                parent.insert(index, child)

    def replace_w_str(self, replacement):
        """Replace tag with string"""
        replacement = self.textjoin(replacement, self.tail)
        parent = self.add_to_previous(replacement)
        parent.remove(self)

    def add_to_previous(self, addition):
        """Add text to the previous tag"""
        previous = self.getprevious()
        parent = self.getparent()
        if previous is not None:
            previous.tail = self.textjoin(previous.tail, addition)
        else:
            parent.text = self.textjoin(parent.text, addition)
        return parent

    @staticmethod
    def textjoin(a, b):
        """Join a and b, replacing either with an empty string
        if their value is not True"""
        return ''.join([a or '', b or ''])