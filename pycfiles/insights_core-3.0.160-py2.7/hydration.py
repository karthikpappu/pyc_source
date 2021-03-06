# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/core/hydration.py
# Compiled at: 2019-11-14 13:57:46
import logging, os
from insights.core import archives
from insights.core.context import ClusterArchiveContext, ExecutionContextMeta, HostArchiveContext
log = logging.getLogger(__name__)

def get_all_files(path):
    all_files = []
    for f in archives.get_all_files(path):
        if os.path.isfile(f) and not os.path.islink(f):
            all_files.append(f)

    return all_files


def identify(files):
    common_path, ctx = ExecutionContextMeta.identify(files)
    if ctx:
        return (common_path, ctx)
    common_path = os.path.dirname(os.path.commonprefix(files))
    if not common_path:
        raise archives.InvalidArchive('Unable to determine common path')
    return (common_path, HostArchiveContext)


def create_context(path, context=None):
    top = os.listdir(path)
    arc = [ os.path.join(path, f) for f in top if f.endswith(archives.COMPRESSION_TYPES) ]
    if arc:
        return ClusterArchiveContext(path, all_files=arc)
    all_files = get_all_files(path)
    if not all_files:
        raise archives.InvalidArchive('No files in archive')
    common_path, ctx = identify(all_files)
    context = context or ctx
    return context(common_path, all_files=all_files)