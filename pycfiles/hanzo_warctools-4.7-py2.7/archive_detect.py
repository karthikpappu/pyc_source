# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warctools/archive_detect.py
# Compiled at: 2013-01-14 05:25:26
import gzip
archive_types = []

def is_gzip_file(file_handle):
    signature = file_handle.read(2)
    file_handle.seek(-len(signature), 1)
    return signature == b'\x1f\x8b'


def guess_record_type(file_handle):
    offset = file_handle.tell()
    if is_gzip_file(file_handle):
        nfh = gzip.GzipFile(fileobj=file_handle)
    else:
        nfh = file_handle
    line = nfh.readline()
    file_handle.seek(offset)
    for rx, record in archive_types:
        if rx.match(line):
            return record
    else:
        return

    return


def register_record_type(rx, record):
    archive_types.append((rx, record))