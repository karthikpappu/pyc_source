# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\iframe.py
# Compiled at: 2005-02-12 22:37:15
from xml.dom import XMLNS_NAMESPACE
from xml.sax import ContentHandler
import xml.dom
from string import *
import re, copy, rng
from rng import *
from Ft.Xml import XPath, cDomlette
import Ft.Xml
from types import *
from sax2dom_chunker import sax2dom_chunker
from Ft.Xml import Domlette
methods = {'http://relaxng.org/ns/structure/1.0': 'iFrameRNG', 'http://www.w3.org/1999/XSL/Transform': 'iFrameXSLT', 'http://namespaces.xmlschemata.org/xvif/datatypes': 'iFrameTypes', 'http://simonstl.com/ns/fragments/': 'iFrameRegFrag'}

class Transform(rng._Pattern, rng._Callback):
    __module__ = __name__

    def __init__(self):
        rng._Pattern.__init__(self)
        self.type = ''
        self.module = None
        self.apply = ''
        self.applyElt = None
        return

    def startElementNS(self, schema, name, qname, attrs):
        self.parent = schema.previousElement()
        self.context = copy.deepcopy(schema.context)
        rng._Callback.startElementNS(self, schema, name, qname, attrs)

    def append(self, child):
        if child.__class__ == Apply:
            self.applyElt = child
        else:
            raise RngSchemaInvalidException, 'Unsupported iframe construct'

    def set_type(self, context, value):
        if methods.has_key(value):
            module = __import__(methods[value])
            if 'transform' not in dir(module):
                raise RngSchemaInvalidException, 'Unsupported transformation type: %s' % value
            else:
                self.type = value
        else:
            raise RngSchemaInvalidException, 'Unsupported transformation type: %s' % value

    def set_apply(self, context, value):
        self.apply = value

    def transform(self, node):
        module = __import__(methods[self.type])
        return module.transform(self, node)


class Apply(rng._Container, rng._Callback):
    __module__ = __name__

    def __init__(self):
        rng._Container.__init__(self)
        self.dom = None
        self.type = ''
        return

    def startElementNS(self, schema, name, qname, attrs):
        rng._Callback.startElementNS(self, schema, name, qname, attrs)
        self.type = schema.previousElement().type
        if self.type != 'http://relaxng.org/ns/structure/1.0':
            rng._Callback.startElementNS(self, schema, name, qname, attrs)
            self.handler = sax2dom_chunker(domimpl=Domlette.implementation)
            schema.divertEventsTo(self.handler)

    def endElementNS(self, schema, name, qname):
        if self.type == 'http://relaxng.org/ns/structure/1.0':
            rng._Container.endElementNS(self, schema, name, qname)
        else:
            rng._Callback.endElementNS(self, schema, name, qname)
            self.dom = self.handler.get_root_node()


class Validate(Transform):
    __module__ = __name__

    def set_type(self, context, value):
        if methods.has_key(value):
            module = __import__(methods[value])
            if 'validate' not in dir(module):
                raise RngSchemaInvalidException, 'Unsupported transformation type: %s' % value
            else:
                self.type = value
        else:
            raise RngSchemaInvalidException, 'Unsupported transformation type: %s' % value

    def transform(self, node):
        module = __import__(methods[self.type])
        res = module.validate(self, node)
        if res == None:
            return res
        else:
            return node
        return


class Pipe(rng._Pattern, rng._Callback):
    __module__ = __name__

    def __init__(self):
        rng._Pattern.__init__(self)
        self.children = []

    def startElementNS(self, schema, name, qname, attrs):
        rng._Callback.startElementNS(self, schema, name, qname, attrs)

    def append(self, child):
        self.children.append(child)

    def deriv(self, node):
        for t in self.children:
            node = t.transform(node)
            if node == None:
                return rng.NotAllowed()

        return rng.Empty()
        return