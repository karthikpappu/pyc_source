# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/bucketlistresultset.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6796 bytes
from boto.compat import urllib, six

def bucket_lister(bucket, prefix='', delimiter='', marker='', headers=None, encoding_type=None):
    """
    A generator function for listing keys in a bucket.
    """
    more_results = True
    k = None
    while more_results:
        rs = bucket.get_all_keys(prefix=prefix, marker=marker, delimiter=delimiter, headers=headers, encoding_type=encoding_type)
        for k in rs:
            yield k

        if k:
            marker = rs.next_marker or k.name
        if marker:
            if encoding_type == 'url':
                if isinstance(marker, six.text_type):
                    marker = marker.encode('utf-8')
                marker = urllib.parse.unquote(marker)
        more_results = rs.is_truncated


class BucketListResultSet(object):
    __doc__ = '\n    A resultset for listing keys within a bucket.  Uses the bucket_lister\n    generator function and implements the iterator interface.  This\n    transparently handles the results paging from S3 so even if you have\n    many thousands of keys within the bucket you can iterate over all\n    keys in a reasonably efficient manner.\n    '

    def __init__(self, bucket=None, prefix='', delimiter='', marker='', headers=None, encoding_type=None):
        self.bucket = bucket
        self.prefix = prefix
        self.delimiter = delimiter
        self.marker = marker
        self.headers = headers
        self.encoding_type = encoding_type

    def __iter__(self):
        return bucket_lister(self.bucket, prefix=self.prefix, delimiter=self.delimiter, marker=self.marker, headers=self.headers, encoding_type=self.encoding_type)


def versioned_bucket_lister(bucket, prefix='', delimiter='', key_marker='', version_id_marker='', headers=None, encoding_type=None):
    """
    A generator function for listing versions in a bucket.
    """
    more_results = True
    k = None
    while more_results:
        rs = bucket.get_all_versions(prefix=prefix, key_marker=key_marker, version_id_marker=version_id_marker, delimiter=delimiter, headers=headers, max_keys=999, encoding_type=encoding_type)
        for k in rs:
            yield k

        key_marker = rs.next_key_marker
        version_id_marker = rs.next_version_id_marker
        more_results = rs.is_truncated


class VersionedBucketListResultSet(object):
    __doc__ = '\n    A resultset for listing versions within a bucket.  Uses the bucket_lister\n    generator function and implements the iterator interface.  This\n    transparently handles the results paging from S3 so even if you have\n    many thousands of keys within the bucket you can iterate over all\n    keys in a reasonably efficient manner.\n    '

    def __init__(self, bucket=None, prefix='', delimiter='', key_marker='', version_id_marker='', headers=None, encoding_type=None):
        self.bucket = bucket
        self.prefix = prefix
        self.delimiter = delimiter
        self.key_marker = key_marker
        self.version_id_marker = version_id_marker
        self.headers = headers
        self.encoding_type = encoding_type

    def __iter__(self):
        return versioned_bucket_lister(self.bucket, prefix=self.prefix, delimiter=self.delimiter, key_marker=self.key_marker, version_id_marker=self.version_id_marker, headers=self.headers, encoding_type=self.encoding_type)


def multipart_upload_lister(bucket, key_marker='', upload_id_marker='', headers=None, encoding_type=None):
    """
    A generator function for listing multipart uploads in a bucket.
    """
    more_results = True
    k = None
    while more_results:
        rs = bucket.get_all_multipart_uploads(key_marker=key_marker, upload_id_marker=upload_id_marker, headers=headers, encoding_type=encoding_type)
        for k in rs:
            yield k

        key_marker = rs.next_key_marker
        upload_id_marker = rs.next_upload_id_marker
        more_results = rs.is_truncated


class MultiPartUploadListResultSet(object):
    __doc__ = '\n    A resultset for listing multipart uploads within a bucket.\n    Uses the multipart_upload_lister generator function and\n    implements the iterator interface.  This\n    transparently handles the results paging from S3 so even if you have\n    many thousands of uploads within the bucket you can iterate over all\n    keys in a reasonably efficient manner.\n    '

    def __init__(self, bucket=None, key_marker='', upload_id_marker='', headers=None, encoding_type=None):
        self.bucket = bucket
        self.key_marker = key_marker
        self.upload_id_marker = upload_id_marker
        self.headers = headers
        self.encoding_type = encoding_type

    def __iter__(self):
        return multipart_upload_lister(self.bucket, key_marker=self.key_marker, upload_id_marker=self.upload_id_marker, headers=self.headers, encoding_type=self.encoding_type)