# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/streamio/stream.py
# Compiled at: 2014-02-12 20:13:54
"""stream"""
import zlib, struct
from time import time
from json import loads
from string import strip
import unicodecsv as csv
from py._path.local import LocalPath
from funcy import compact, imap, zipdict

def stream(filename, encoding='utf-8', skipblank=True, strip=True, stripchars='\r\n\t '):
    """Stream every line in the given file.

    :param encoding: A ``str`` indicating the charset/encoding to use.
    :type encoding:  ``str`` or ``None``

    :param filename: A ``str`` filename, A ``py._path.local.LocalPath`` instance or open ``file`` instnace.
    :type filename:  ``str``, ``py._path.local.LocalPath`` or ``file``.

    :param skipblank: Whehter to skip blank lines (sometimes undesirable)
    :type skipblank: ``bool``

    :param strip: Whehter to strip lines of surrounding whitespace (sometimes undesirable)
    :type strip: ``bool``

    :param stripchars: An iterable of characters to strip from the surrounding line. ``line.strip(...)`` is used.
    :type stripchars: ``list``, ``tuple`` or ``str``

    Each line in the file is read, stripped of surrounding whitespace and returned iteratively. Blank lines are ignored.
    If they keyword argument ``encoding`` is provided and is not ``None`` each line in the input strema will be decoded
    using the given encoding, if ``None`` will disable unicode decoding.
    """
    if isinstance(filename, LocalPath):
        fd = filename.open('rU')
    else:
        if isinstance(filename, str):
            fd = open(filename, 'rU')
        else:
            fd = filename
        for line in fd:
            line = line.strip(stripchars) if strip else line
            if line or not skipblank:
                if encoding is not None:
                    yield line.decode(encoding)
                else:
                    yield line

    return


def csvstream(filename, encoding='utf-8', stripchars='\r\n'):
    """Stream every line in the given file interpreting each line as CSV.

    :param filename: A ``str`` filename, A ``py._path.local.LocalPath`` instance or open ``file`` instnace.
    :type filename:  ``str``, ``py._path.local.LocalPath`` or ``file``.

    :param encoding: A ``str`` indicating the charset/encoding to use.
    :type encoding:  ``str``

    :param stripchars: An iterable of characters to strip from the surrounding line. ``line.strip(...)`` is used.
    :type stripchars: ``list``, ``tuple`` or ``str``

    This is a wrapper around ``stream`` where the stream is treated as CSV.
    """
    if isinstance(filename, LocalPath):
        fd = filename.open('rU')
    else:
        if isinstance(filename, str):
            fd = open(filename, 'rU')
        else:
            fd = filename
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(fd.readline().decode(encoding))
        fd.seek(0)
        reader = csv.reader(stream(fd, encoding=None, stripchars=stripchars), encoding=encoding, dialect=dialect)
        for item in reader:
            yield item

    return


def csvdictstream(filename, encoding='utf-8', fields=None, stripchars='\r\n'):
    """Stream every line in the given file interpreting each line as a dictionary of fields to items.

    :param filename: A ``str`` filename, A ``py._path.local.LocalPath`` instance or open ``file`` instnace.
    :type filename:  ``str``, ``py._path.local.LocalPath`` or ``file``.

    :param encoding: A ``str`` indicating the charset/encoding to use.
    :type encoding:  ``str``

    :param stripchars: An iterable of characters to strip from the surrounding line. ``line.strip(...)`` is used.
    :type stripchars: ``list``, ``tuple`` or ``str``

    This is a wrapper around ``csvstream`` where the stream is treated as dict of field(s) to item(s).
    """
    stream = csvstream(filename, encoding=encoding, stripchars=stripchars)
    if fields is None:
        fields = map(strip, next(stream))
    for values in stream:
        yield compact(zipdict(fields, values))

    return


def jsonstream(filename, encoding='utf-8'):
    """Stream every line in the given file interpreting each line as JSON.

    :param filename: A ``str`` filename, A ``py._path.local.LocalPath`` instance or open ``file`` instnace.
    :type filename:  ``str``, ``py._path.local.LocalPath`` or ``file``.

    :param encoding: A ``str`` indicating the charset/encoding to use.
    :type encoding:  ``str``

    :param stripchars: An iterable of characters to strip from the surrounding line. ``line.strip(...)`` is used.
    :type stripchars: ``list``, ``tuple`` or ``str``

    This is a wrappedaround ``stream`` except that it wraps each line in a ``dumps`` call essentially treating
    each line as a piece of valid JSON.
    """
    return imap(loads, stream(filename, encoding=encoding))


def compress(iterable, level=9, encoding='utf-8'):
    """Compress the given iterable of bytes using zlib compressin

    :param iterable: An iterable of bytes to compress using zlib (ZIP)
    :type iterable: An iterable of ``bytes`` (If ``str`` will be encoded)

    :param level: An optional Compression Level
    :type level: ``int`` (Default: 9)

    :param encoding: An optional encoding to use when dealing with an iterable of ``str``
    :type encoding: ``str`` (Default: utf-8)

    :returns: An iterable compressed with zlib
    :rtype: iterable stream of ``bytes``
    """
    yield b'\x1f\x8b'
    yield '\x08'
    yield '\x00'
    yield struct.pack('<L', int(time()) & int('FFFFFFFF', 16))
    yield '\x02'
    yield b'\xff'
    crc = zlib.crc32('')
    size = 0
    zobj = zlib.compressobj(level, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
    for chunk in iterable:
        if not isinstance(chunk, bytes):
            chunk = chunk.encode(encoding)
        size += len(chunk)
        crc = zlib.crc32(chunk, crc)
        yield zobj.compress(chunk)

    yield zobj.flush()
    yield struct.pack('<L', crc & int('FFFFFFFF', 16))
    yield struct.pack('<L', size & int('FFFFFFFF', 16))


__all__ = ('stream', 'csvstream', 'csvdictstream', 'jsonstream', 'compress')