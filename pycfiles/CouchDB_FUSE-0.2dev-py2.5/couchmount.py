# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/couchmount.py
# Compiled at: 2009-07-30 07:18:01
from couchdb import Database, Document, ResourceNotFound, Row, Server, ViewResults
import errno, fuse, os, stat, sys
from time import time
try:
    import simplejson as json
except ImportError:
    import json

from urllib import quote, unquote
fuse.fuse_python_api = (0, 2)
COUCHFS_DIRECTORY_PLACEHOLDER = '.couchfs-directory-placeholder'

class CouchStat(fuse.Stat):

    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = os.getuid()
        self.st_gid = os.getgid()
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


def _normalize_path(path):
    return ('/').join([ part for part in path.split('/') if part != '' ])


class CouchFSDocument(fuse.Fuse):

    def __init__(self, mountpoint, uri=None, *args, **kwargs):
        fuse.Fuse.__init__(self, *args, **kwargs)
        (db_uri, doc_id) = uri.rsplit('/', 1)
        self.doc_id = unquote(doc_id)
        self.db = Database(db_uri)

    def get_dirs(self):
        dirs = {}
        attachments = self.db[self.doc_id].get('_attachments', {}).keys()
        for att in attachments:
            parents = [
             '']
            for name in att.split('/'):
                filenames = dirs.setdefault(('/').join(parents[1:]), set())
                if name != COUCHFS_DIRECTORY_PLACEHOLDER:
                    filenames.add(name)
                    parents.append(name)

        return dirs

    def readdir(self, path, offset):
        path = _normalize_path(path)
        for r in ('.', '..'):
            yield fuse.Direntry(r)

        for name in self.get_dirs().get(path, []):
            yield fuse.Direntry(name.encode('utf-8'))

    def getattr(self, path):
        path = _normalize_path(path)
        try:
            st = CouchStat()
            if path == '' or path in self.get_dirs().keys():
                st.st_mode = stat.S_IFDIR | 509
                st.st_nlink = 2
            else:
                att = self.db[self.doc_id].get('_attachments', {})
                data = att[path]
                st.st_mode = stat.S_IFREG | 436
                st.st_nlink = 1
                st.st_size = data['length']
            return st
        except (KeyError, ResourceNotFound):
            return -errno.ENOENT

    def open(self, path, flags):
        path = _normalize_path(path)
        try:
            parts = path.rsplit('/', 1)
            if len(parts) == 1:
                dirname, filename = '', parts[0]
            else:
                (dirname, filename) = parts
            if filename in self.get_dirs()[dirname]:
                return 0
            return -errno.ENOENT
        except (KeyError, ResourceNotFound):
            return -errno.ENOENT

    def read(self, path, size, offset):
        path = _normalize_path(path)
        try:
            data = self.db.get_attachment(self.db[self.doc_id], path)
            slen = len(data)
            if offset < slen:
                if offset + size > slen:
                    size = slen - offset
                buf = data[offset:offset + size]
            else:
                buf = ''
            return buf
        except (KeyError, ResourceNotFound):
            pass

        return -errno.ENOENT

    def write(self, path, buf, offset):
        path = _normalize_path(path)
        try:
            data = self.db.get_attachment(self.db[self.doc_id], path)
            data = data[0:offset] + buf + data[offset + len(buf):]
            self.db.put_attachment(self.db[self.doc_id], data, filename=path)
            return len(buf)
        except (KeyError, ResourceNotFound):
            pass

        return -errno.ENOENT

    def mknod(self, path, mode, dev):
        path = _normalize_path(path)
        self.db.put_attachment(self.db[self.doc_id], '', filename=path)

    def unlink(self, path):
        path = _normalize_path(path)
        parts = path.rsplit('/', 1)
        if len(parts) == 1:
            dirname, filename = '', parts[0]
        else:
            (dirname, filename) = parts
        self.db.delete_attachment(self.db[self.doc_id], path)
        if filename != COUCHFS_DIRECTORY_PLACEHOLDER and len(self.get_dirs().get(dirname, [])) == 0:
            print 'putting to:', '%s/%s' % (dirname, COUCHFS_DIRECTORY_PLACEHOLDER)
            self.db.put_attachment(self.db[self.doc_id], '', filename='%s/%s' % (dirname, COUCHFS_DIRECTORY_PLACEHOLDER))

    def truncate(self, path, size):
        path = _normalize_path(path)
        self.db.put_attachment(self.db[self.doc_id], '', filename=path)
        return 0

    def utime(self, path, times):
        return 0

    def mkdir(self, path, mode):
        path = _normalize_path(path)
        self.db.put_attachment(self.db[self.doc_id], '', filename='%s/%s' % (path, COUCHFS_DIRECTORY_PLACEHOLDER))
        return 0

    def rmdir(self, path):
        path = _normalize_path(path)
        self.db.delete_attachment(self.db[self.doc_id], '%s/%s' % (path, COUCHFS_DIRECTORY_PLACEHOLDER))
        return 0

    def rename(self, pathfrom, pathto):
        pathfrom, pathto = _normalize_path(pathfrom), _normalize_path(pathto)
        data = self.db.get_attachment(self.db[self.doc_id], pathfrom)
        self.db.put_attachment(self.db[self.doc_id], data, filename=pathto)
        self.db.delete_attachment(self.db[self.doc_id], pathfrom)
        return 0

    def fsync(self, path, isfsyncfile):
        return 0

    def statfs(self):
        """
        Should return a tuple with the following 6 elements:
            - blocksize - size of file blocks, in bytes
            - totalblocks - total number of blocks in the filesystem
            - freeblocks - number of free blocks
            - availblocks - number of blocks available to non-superuser
            - totalfiles - total number of file inodes
            - freefiles - nunber of free file inodes
    
        Feel free to set any of the above values to 0, which tells
        the kernel that the info is not available.
        """
        st = fuse.StatVfs()
        block_size = 1024
        blocks = 1048576
        blocks_free = blocks
        blocks_avail = blocks_free
        files = 0
        files_free = 0
        st.f_bsize = block_size
        st.f_frsize = block_size
        st.f_blocks = blocks
        st.f_bfree = blocks_free
        st.f_bavail = blocks_avail
        st.f_files = files
        st.f_ffree = files_free
        return st


class CouchFS(fuse.Fuse):
    """FUSE interface to a CouchDB database."""

    def __init__(self, mountpoint, uri=None, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)
        self.fuse_args.mountpoint = mountpoint
        if uri is not None:
            self.server = Server(uri)
        else:
            self.server = Server()
        return

    def getcouchattrs(self, path):
        attr = self.server
        attrs = [attr]
        parts = [ x for x in path[1:].split('/') if x != '' ]
        i = 0
        for part in parts:
            if isinstance(attr, Database):
                if part == '_view':
                    attr = attr.view('_all_docs')['_design/':'_design/ZZZ']
                    attr.is_view = True
                elif part == '_all_docs':
                    attr = attr.view('_all_docs')
            elif isinstance(attr, ViewResults):
                if getattr(attr, 'is_view', False):
                    attr = list(attr[('_design/' + part)])[0]
                    attr.is_view = True
                else:
                    if attr.view.name != '_all_docs':
                        part = json.loads(unquote(part))
                    results = list(attr.view()[part])
                    if len(results) == 1:
                        attr = results[0]
                    else:
                        attr = attr.view()[part + '/':part + '/ZZZ']
                        if i + 1 < len(parts):
                            parts[i + 1] = '%s/%s' % (part, parts[(i + 1)])
            elif isinstance(attr, Row):
                if getattr(attr, 'is_view', False):
                    db = self.server[parts[0]]
                    attr = db.view('_view/' + ('/').join(parts[i - 1:i + 1]), group=True)
                elif part == 'value':
                    attr = attr.value
            else:
                attr = attr[part]
            attrs.append(attr)
            i += 1

        return attrs

    def getattr(self, path):
        try:
            st = CouchStat()
            attr = self.getcouchattrs(path)[(-1)]
            if isinstance(attr, Server) or isinstance(attr, Database) or isinstance(attr, Document) or isinstance(attr, ViewResults) or isinstance(attr, Row):
                st.st_mode = stat.S_IFDIR | 493
                st.st_nlink = 2
            else:
                data = json.dumps(attr)
                st.st_mode = stat.S_IFREG | 292
                st.st_nlink = 1
                st.st_size = len(data)
            return st
        except (KeyError, ResourceNotFound):
            return -errno.ENOENT

    def readdir(self, path, offset):
        attr = self.getcouchattrs(path)[(-1)]
        for r in ('.', '..'):
            yield fuse.Direntry(r)

        if isinstance(attr, Server):
            for db_name in self.server:
                yield fuse.Direntry(db_name.encode('utf-8'))

            return
        if isinstance(attr, Database):
            yield fuse.Direntry('_all_docs')
            yield fuse.Direntry('_view')
            return
        if isinstance(attr, ViewResults):
            is_view = getattr(attr, 'is_view', False)
            for row in list(attr):
                dirname = row.key
                if attr.view.name != '_all_docs':
                    dirname = quote(json.dumps(row.key))
                else:
                    dirname = dirname.split('/')[attr.options.get('startkey', '').count('/')]
                if is_view:
                    dirname = dirname.split('/')[(-1)]
                yield fuse.Direntry(dirname.encode('utf-8'))

            return
        if isinstance(attr, Row):
            is_view = getattr(attr, 'is_view', False)
            if is_view:
                db = self.getcouchattrs(path)[1]
                for r in db[attr.id]['views']:
                    yield fuse.Direntry(r.encode('utf-8'))

            else:
                yield fuse.Direntry('value')
            return
        for r in attr.keys():
            yield fuse.Direntry(r.encode('utf-8'))

    def open(self, path, flags):
        try:
            attr = self.getcouchattrs(path)[(-1)]
        except (KeyError, ResourceNotFound):
            return -errno.ENOENT

        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if flags & accmode != os.O_RDONLY:
            return -errno.EACCES

    def read(self, path, size, offset):
        try:
            attr = self.getcouchattrs(path)[(-1)]
            data = json.dumps(attr)
            slen = len(data)
            if offset < slen:
                if offset + size > slen:
                    size = slen - offset
                buf = data[offset:offset + size]
            else:
                buf = ''
            return buf
        except (KeyError, ResourceNotFound):
            pass

        return -errno.ENOENT

    def write(self, path, buf, offset):
        pass

    def unlink(self, path):
        attr = self.getcouchattrs(path)[(-1)]

    def mkdir(self, path, mode):
        server = self.getcouchattrs(path)[0]
        if isinstance(server, Server):
            server.create(path.split('/')[(-1)])


def main():
    args = sys.argv[1:]
    if len(args) not in (2, 3):
        print 'CouchDB FUSE Connector: Allows you to browse the _attachments of'
        print ' any CouchDB document on your own filesystem!'
        print
        print 'Remember to URL-encode your <doc_id> appropriately.'
        print
        print 'Usage: python couchmount.py [-d] <http://hostname:port/db/doc_id> <mount-point>'
        sys.exit(-1)
    if len(args) == 1:
        fs = CouchFS(args[0])
    elif len(args) == 2:
        fs = CouchFSDocument(args[1], args[0])
    elif len(args) == 3:
        fs = CouchFSDocument(args[2], args[1])
    fs.parse(errex=1)
    fs.main()


if __name__ == '__main__':
    main()