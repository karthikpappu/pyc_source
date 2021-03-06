# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_vendor/html5lib/treeadapters/sax.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 1776 bytes
from __future__ import absolute_import, division, unicode_literals
from xml.sax.xmlreader import AttributesNSImpl
from ..constants import adjustForeignAttributes, unadjustForeignAttributes
prefix_mapping = {}
for prefix, localName, namespace in adjustForeignAttributes.values():
    if prefix is not None:
        prefix_mapping[prefix] = namespace

def to_sax(walker, handler):
    """Call SAX-like content handler based on treewalker walker

    :arg walker: the treewalker to use to walk the tree to convert it

    :arg handler: SAX handler to use

    """
    handler.startDocument()
    for prefix, namespace in prefix_mapping.items():
        handler.startPrefixMapping(prefix, namespace)

    for token in walker:
        type = token['type']
        if type == 'Doctype':
            continue
        else:
            if type in ('StartTag', 'EmptyTag'):
                attrs = AttributesNSImpl(token['data'], unadjustForeignAttributes)
                handler.startElementNS((token['namespace'], token['name']), token['name'], attrs)
                if type == 'EmptyTag':
                    handler.endElementNS((token['namespace'], token['name']), token['name'])
                else:
                    if type == 'EndTag':
                        handler.endElementNS((token['namespace'], token['name']), token['name'])
                    else:
                        if type in ('Characters', 'SpaceCharacters'):
                            handler.characters(token['data'])
                        else:
                            if type == 'Comment':
                                pass
                            elif not False:
                                raise AssertionError('Unknown token type')

    for prefix, namespace in prefix_mapping.items():
        handler.endPrefixMapping(prefix)

    handler.endDocument()