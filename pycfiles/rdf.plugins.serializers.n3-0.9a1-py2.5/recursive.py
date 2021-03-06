# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/n3/recursive.py
# Compiled at: 2008-04-06 15:53:32
from rdf.term import BNode
from rdf.term import Literal
from rdf.term import URIRef
from rdf.term import RDF
from rdf.term import RDFS
from rdf.serializer import Serializer

class RecursiveSerializer(Serializer):
    topClasses = [
     RDFS['Class']]
    predicateOrder = [RDF['type'], RDFS['label']]
    maxDepth = 10
    indentString = '  '

    def __init__(self, store):
        super(RecursiveSerializer, self).__init__(store)
        self.stream = None
        self.reset()
        return

    def addNamespace(self, prefix, uri):
        self.namespaces[prefix] = uri

    def checkSubject(self, subject):
        """Check to see if the subject should be serialized yet"""
        if self.isDone(subject) or subject not in self._subjects or subject in self._topLevels and self.depth > 1 or isinstance(subject, URIRef) and self.depth >= self.maxDepth:
            return False
        return True

    def isDone(self, subject):
        """Return true if subject is serialized"""
        return subject in self._serialized

    def orderSubjects(self):
        seen = {}
        subjects = []
        for classURI in self.topClasses:
            members = list(self.store.subjects(RDF['type'], classURI))
            members.sort()
            for member in members:
                subjects.append(member)
                self._topLevels[member] = True
                seen[member] = True

        recursable = [ (isinstance(subject, BNode), self.refCount(subject), subject) for subject in self._subjects if subject not in seen ]
        recursable.sort()
        subjects.extend([ subject for (isbnode, refs, subject) in recursable ])
        return subjects

    def preprocess(self):
        for triple in self.store.triples((None, None, None)):
            self.preprocessTriple(triple)

        return

    def preprocessTriple(self, (s, p, o)):
        references = self.refCount(o) + 1
        self._references[o] = references
        self._subjects[s] = True

    def refCount(self, node):
        """Return the number of times this node has been referenced in the object position"""
        return self._references.get(node, 0)

    def reset(self):
        self.depth = 0
        self.lists = {}
        self.namespaces = {}
        self._references = {}
        self._serialized = {}
        self._subjects = {}
        self._topLevels = {}

    def buildPredicateHash(self, subject):
        """Build a hash key by predicate to a list of objects for the given subject"""
        properties = {}
        for (s, p, o) in self.store.triples((subject, None, None)):
            oList = properties.get(p, [])
            oList.append(o)
            properties[p] = oList

        return properties

    def sortProperties(self, properties):
        """Take a hash from predicate uris to lists of values.
           Sort the lists of values.  Return a sorted list of properties."""
        for (prop, objects) in properties.items():
            objects.sort()

        propList = []
        seen = {}
        for prop in self.predicateOrder:
            if prop in properties and prop not in seen:
                propList.append(prop)
                seen[prop] = True

        props = properties.keys()
        props.sort()
        for prop in props:
            if prop not in seen:
                propList.append(prop)
                seen[prop] = True

        return propList

    def subjectDone(self, subject):
        """Mark a subject as done."""
        self._serialized[subject] = True

    def indent(self, modifier=0):
        """Returns indent string multiplied by the depth"""
        return (self.depth + modifier) * self.indentString

    def write(self, text):
        """Write text in given encoding."""
        self.stream.write(text.encode(self.encoding, 'replace'))