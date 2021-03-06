# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/core/archives.py
# Compiled at: 2020-04-30 14:03:01
import logging, os, tempfile
from contextlib import contextmanager
from insights.util import fs, subproc, which
from insights.util.content_type import from_file as content_type_from_file
logger = logging.getLogger(__name__)
COMPRESSION_TYPES = ('zip', 'tar', 'gz', 'bz2', 'xz')

class InvalidArchive(Exception):

    def __init__(self, msg):
        super(InvalidArchive, self).__init__(msg)
        self.msg = msg


class InvalidContentType(InvalidArchive):

    def __init__(self, content_type):
        self.msg = 'Invalid content type: "%s"' % content_type
        super(InvalidContentType, self).__init__(self.msg)
        self.content_type = content_type


class ZipExtractor(object):

    def __init__(self, timeout=None):
        self.content_type = 'application/zip'
        self.timeout = timeout
        self.tmp_dir = None
        self.created_tmp_dir = False
        return

    def from_path(self, path, extract_dir=None, content_type=None):
        self.tmp_dir = tempfile.mkdtemp(prefix='insights-', dir=extract_dir)
        self.created_tmp_dir = True
        command = 'unzip -n -q -d %s %s' % (self.tmp_dir, path)
        subproc.call(command, timeout=self.timeout)
        return self


class TarExtractor(object):

    def __init__(self, timeout=None):
        self.timeout = timeout
        self.tmp_dir = None
        self.created_tmp_dir = False
        return

    TAR_FLAGS = {'application/x-xz': '-J', 
       'application/x-gzip': '-I igzip' if which('igzip') else '-z', 
       'application/gzip': '-I igzip' if which('igzip') else '-z', 
       'application/x-bzip2': '-j', 
       'application/x-tar': ''}

    def _tar_flag_for_content_type(self, content_type):
        flag = self.TAR_FLAGS.get(content_type)
        if flag is None:
            raise InvalidContentType(content_type)
        return flag

    def from_path(self, path, extract_dir=None, content_type=None):
        if os.path.isdir(path):
            self.tmp_dir = path
        else:
            self.content_type = content_type or content_type_from_file(path)
            tar_flag = self._tar_flag_for_content_type(self.content_type)
            self.tmp_dir = tempfile.mkdtemp(prefix='insights-', dir=extract_dir)
            self.created_tmp_dir = True
            command = 'tar --delay-directory-restore %s -x --exclude=*/dev/null -f %s -C %s' % (tar_flag, path, self.tmp_dir)
            logging.debug("Extracting files in '%s'", self.tmp_dir)
            subproc.call(command, timeout=self.timeout)
        return self


class Extraction(object):

    def __init__(self, tmp_dir, content_type):
        self.tmp_dir = tmp_dir
        self.content_type = content_type


@contextmanager
def extract(path, timeout=None, extract_dir=None, content_type=None):
    """
    Extract path into a temporary directory in `extract_dir`.

    Yields an object containing the temporary path and the content type of the
    original archive.

    If the extraction takes longer than `timeout` seconds, the temporary path
    is removed, and an exception is raised.
    """
    content_type = content_type or content_type_from_file(path)
    if content_type == 'application/zip':
        extractor = ZipExtractor(timeout=timeout)
    else:
        extractor = TarExtractor(timeout=timeout)
    try:
        ctx = extractor.from_path(path, extract_dir=extract_dir, content_type=content_type)
        content_type = extractor.content_type
        yield Extraction(ctx.tmp_dir, content_type)
    finally:
        if extractor.created_tmp_dir:
            fs.remove(extractor.tmp_dir, chmod=True)