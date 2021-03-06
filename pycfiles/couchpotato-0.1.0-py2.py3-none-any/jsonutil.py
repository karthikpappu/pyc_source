# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/jsonutil.py
# Compiled at: 2009-07-21 09:44:12
from cStringIO import StringIO
from jsonish import pythonjson
from schemaish.type import File
import base64
from dottedish import flatten, dotted

class CouchishFile(File):

    def __init__(self, file, filename, mimetype, id=None, doc_id=None, inline=False, b64=False, metadata=None):
        self.file = file
        self.filename = filename
        self.mimetype = mimetype
        self.id = id
        self.doc_id = doc_id
        self.inline = inline
        self.b64 = b64
        if metadata is None:
            metadata = {}
        self.metadata = metadata
        return

    def __repr__(self):
        return '<couchish.jsonutil.CouchishFile file="%r" filename="%s", mimetype="%s", id="%s", doc_id="%s", inline="%s", b64="%s", metadata="%r" >' % (getattr(self, 'file', None), self.filename, self.mimetype, self.id, getattr(self, 'doc_id', None), getattr(self, 'inline', None), getattr(self, 'b64', None), getattr(self, 'metadata', {}))


class AttachmentFileLike(object):
    """
    A lazy-loading file-like object that reads the attachment via the session
    on first call to read().

    This object *must* stay close to the session instance so should never be
    serialised by default. Instances are therefore marked un unpicklable,
    uncopyable, etc to avoid them accidentally "leaking out".
    """

    def __init__(self, session, doc_id, filename):
        self.session = session
        self.doc_id = doc_id
        self.filename = filename
        self._file = None
        return

    def read(self, *a, **k):
        if self._file is None:
            data = self.session.get_attachment(self.doc_id, self.filename)
            self._file = StringIO(data)
        return self._file.read(*a, **k)

    def __getstate__(self):
        return False


def file_to_dict(obj):
    d = {'__type__': 'file', 
       'filename': obj.filename, 
       'mimetype': obj.mimetype, 
       'id': getattr(obj, 'id', None)}
    if hasattr(obj, 'metadata') and obj.metadata:
        d['metadata'] = obj.metadata
    if hasattr(obj, 'doc_id') and obj.doc_id is not None:
        d['doc_id'] = obj.doc_id
    if hasattr(obj, 'inline') and obj.inline is not False:
        d['inline'] = obj.inline
    file = getattr(obj, 'file', None)
    if isinstance(file, AttachmentFileLike):
        pass
    elif file and hasattr(obj, 'b64'):
        d['base64'] = obj.file
    elif file and obj.file is not None:
        d['base64'] = base64.encodestring(file.read())
    return d


def file_from_dict(obj):
    filename = obj['filename']
    mimetype = obj['mimetype']
    inline = obj.get('inline', False)
    id = obj.get('id')
    doc_id = obj.get('doc_id')
    metadata = obj.get('metadata', {})
    if 'base64' in obj:
        data = obj['base64']
        return CouchishFile(data, filename, mimetype, id=id, doc_id=doc_id, inline=inline, b64=True, metadata=metadata)
    else:
        if 'file' in obj:
            data = obj['file']
            return CouchishFile(data, filename, mimetype, id=id, doc_id=doc_id, inline=inline, metadata=metadata)
        else:
            return CouchishFile(None, filename, mimetype, id=id, doc_id=doc_id, metadata=metadata)
        return


pythonjson.json.register_type(File, file_to_dict, file_from_dict, 'file')
pythonjson.json.register_type(CouchishFile, file_to_dict, file_from_dict, 'file')
pythonjson.decode_mapping['file'] = file_from_dict
pythonjson.encode_mapping[File] = ('file', file_to_dict)
pythonjson.encode_mapping[CouchishFile] = ('file', file_to_dict)

def encode_to_dict(obj):
    return pythonjson.encode_to_dict(obj)


def decode_from_dict(d, session=None):
    obj = pythonjson.decode_from_dict(d)
    obj = add_id_and_attr_to_files(obj, session)
    return obj


def add_id_and_attr_to_files(data, session=None):
    if not isinstance(data, dict):
        return data
    dd = dotted(data)
    for (k, f) in flatten(data):
        if isinstance(f, File):
            if '_id' in dd and '_rev' in dd:
                if session:
                    f.file = AttachmentFileLike(session, dd['_id'], f.id)
                f.doc_id = dd['_id']
                f.rev = dd['_rev']
            segments = k.split('.')
            for n in xrange(1, len(segments)):
                subpath = ('.').join(segments[:-n])
                if '_id' in dd[subpath] and '_rev' in dd[subpath]:
                    f.doc_id = dd[subpath]['_id']
                    f.rev = dd[subpath]['_rev']

    return data


dumps = pythonjson.dumps
loads = pythonjson.loads