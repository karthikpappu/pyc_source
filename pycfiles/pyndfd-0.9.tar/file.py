# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/sources/file.py
# Compiled at: 2007-02-15 02:23:59
__doc__ = '\nFile Source\n-----------\n\nA document source for local filesystem.\n\nThe file source watches a path for changes in files matching a set of\ninclude/exclude patterns.\n\nUsage\n~~~~~\n\n::\n\n    file://<path>?include=<glob>&exclude=<glob>\n\n``include=<glob>`` (default: ``*``)\n    Multiple include globs can be provided. Specifies which files should be\n    included in the index.\n\n``exclude=<glob>``\n    Multiple exclude globs can be provided. Specifies which files should be\n    excluded from the index, even if they would otherwise match.\n\nEach file under ``<path>`` is first matched against the includes, then against\nexcludes. If neither match, the file is not included.\n'
import sys, codecs, os
from stat import *
from urlparse import urlsplit, urlunsplit
from urllib import quote, unquote
from pyndexter import *

class FileSource(Source):
    """ Expose a subset of the file system for searching."""
    __module__ = __name__

    def __init__(self, framework, path, include=None, exclude=None, predicate=None):
        Source.__init__(self, framework, include, exclude, predicate)
        self.path = os.path.normpath(path)
        self.encoding = sys.getfilesystemencoding()

    def __iter__(self):

        def walk_path(path):
            path = path.strip(os.path.sep)
            root_path = os.path.join(self.path, path)
            for file in os.listdir(root_path):
                full_path = os.path.join(root_path, file)
                try:
                    stat = os.lstat(full_path)
                except OSError:
                    continue

                if S_ISDIR(stat.st_mode):
                    for uri in walk_path(os.path.join(path, file)):
                        yield uri

                elif self.predicate(URI(scheme='file', path=full_path)) and os.access(full_path, os.R_OK) and S_ISREG(stat.st_mode):
                    yield (
                     URI(scheme='file', path=full_path.decode(self.encoding)), stat)

        for (uri, stat) in walk_path('/'):
            self._state[unicode(uri)] = stat.st_mtime
            yield uri

    def matches(self, uri):
        return uri.scheme == 'file' and uri.path.startswith(self.path) and self.predicate(uri)

    def fetch(self, uri):
        try:
            stat = os.stat(uri.path)
        except Exception, e:
            raise DocumentNotFound(uri, e)

        return Document(uri, source=self, changed=stat.st_mtime, content=self._fetch_content, size=stat.st_size, created=stat.st_ctime)

    def exists(self, uri):
        return os.path.exists(uri.path)

    def __hash__(self):
        return hash('file://' + self.path + ('-').join(self.exclude) + ('+').join(self.include))

    def _fetch_content(self, uri):
        return codecs.open(uri.path, encoding='utf-8', errors='replace').read()


source_factory = PluginFactory(FileSource, include=PluginFactory.List(str), exclude=PluginFactory.List(str))