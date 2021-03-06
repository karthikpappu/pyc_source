# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/indexers/hyperestraier.py
# Compiled at: 2007-02-14 19:14:54
__doc__ = '\nHyperestraier\n-------------\n\nAdapter for Hyperestraier_ using the swigged bindings.\n\n.. _Hyperestraier: http://hyperestraier.sourceforge.net/\n\nUsage\n~~~~~\n\n::\n\n    hyperestraier://<path>?hype_mode=<int>\n\n``hype_mode`` (default: auto)\n    Override the default ``READONLY``/``READWRITE`` modes in Pyndexter and use\n    Hyperestraier database open modes. See the Hyperestraier docs for details.\n\nInstallation\n~~~~~~~~~~~~\n\nInstall your distributions Hyperestraier package (typically the package\n``hyperestraier``).\n\nIf your distribution also includes the SWIG bindings as packages, install\nthese, otherwise:\n\n::\n\n    wget http://hyperestraier.sourceforge.net/binding/hyper_estraier_wrappers-0.0.15.tar.gz\n    tar xfzv hyper_estraier_wrappers-0.0.15.tar.gz\n    cd hyper_estraier_wrappers-0.0.15\n    make\n    make install\n'
import os, HyperEstraier
from pyndexter import *
__all__ = [
 'HyperestraierIndexer', 'HyperestraierResult']

class HyperestraierIndexer(Indexer):
    """ Pyndexter adapter for the Hyperestraier indexer. """
    __module__ = __name__

    def __init__(self, framework, path, hype_mode=None):
        Indexer.__init__(self, framework)
        self.hype_mode = hype_mode
        path = path.encode('utf-8')
        self.path = path
        self.db_path = os.path.join(path, 'hyperestraier.db').encode('utf-8')
        self.state_path = os.path.join(path, 'state.db')
        if framework.mode == READWRITE:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        if self.hype_mode is None:
            self.hype_mode = HyperEstraier.Database.DBREADER
            if self.framework.mode == READWRITE:
                self.hype_mode |= HyperEstraier.Database.DBWRITER | HyperEstraier.Database.DBCREAT
        self.db = HyperEstraier.Database()
        self.db.open(self.db_path, self.hype_mode)
        return

    def index(self, document):
        hdoc = HyperEstraier.Document()
        for (k, v) in document.attributes.iteritems():
            hdoc.add_attr(unicode('@' + k).encode('utf-8'), unicode(v).encode('utf-8'))

        for line in document.content.splitlines():
            hdoc.add_text(line.encode('utf-8'))

        self.db.put_doc(hdoc, 1)

    def discard(self, uri):
        uuri = unicode(uri).encode('utf-8')
        id = self.db.uri_to_id(uuri)
        if id == -1:
            raise DocumentNotFound(uri)
        self.db.out_doc(id, HyperEstraier.Database.ODCLEAN)

    def fetch(self, uri):
        uuri = unicode(uri).encode('utf-8')
        id = self.db.uri_to_id(uuri)
        if id == -1:
            raise DocumentNotFound(uri)
        doc = self.db.get_doc(id, 0)
        attributes = self._translate_attributes(doc)
        return Document(content=('\n').join([ t.decode('utf-8') for t in doc.texts() ]), quality=0.99, **attributes)

    def search(self, query):
        phrase = query.as_string(not_='ANDNOT ')
        return self.hype_search(phrase, query, simple=False)

    def optimise(self):
        self.db.optimize()

    def flush(self):
        self.db.sync()

    def close(self):
        self.db.close()
        self.db = None
        return

    def hype_search(self, phrase, query, simple=True, order=None):
        """ Full Hyperestraier search phrase. """
        cond = HyperEstraier.Condition()
        cond.set_phrase(phrase.encode('utf-8'))
        search = self.db.search(cond, 0)
        return HyperestraierResult(self, query, search)

    def _translate_attributes(self, hdoc):
        attributes = {}
        for k in hdoc.attr_names():
            if k[0] == '@':
                attributes[k[1:]] = hdoc.attr(k).decode('utf-8')
            else:
                attributes[k] = hdoc.attr(k).decode('utf-8')

        attributes['uri'] = URI(attributes['uri'])
        return attributes


indexer_factory = PluginFactory(HyperestraierIndexer, hype_mode=int)

class HyperestraierResult(Result):
    __module__ = __name__

    def __iter__(self):
        for id in self.context:
            yield self._translate(id)

    def __len__(self):
        return len(self.context)

    def __getitem__(self, index):
        return self._translate(self.context[index])

    def _translate(self, id):
        doc = self.indexer.db.get_doc(id, 0)
        return Hit(current=self.indexer.framework.fetch, indexed=self.indexer.fetch, **self.indexer._translate_attributes(doc))