# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/rsa/rsa/varblock.py
# Compiled at: 2018-07-11 18:15:32
"""VARBLOCK file support

.. deprecated:: 3.4

    The VARBLOCK format is NOT recommended for general use, has been deprecated since
    Python-RSA 3.4, and will be removed in a future release. It's vulnerable to a
    number of attacks:

    1. decrypt/encrypt_bigfile() does not implement `Authenticated encryption`_ nor
       uses MACs to verify messages before decrypting public key encrypted messages.

    2. decrypt/encrypt_bigfile() does not use hybrid encryption (it uses plain RSA)
       and has no method for chaining, so block reordering is possible.

    See `issue #19 on Github`_ for more information.

.. _Authenticated encryption: https://en.wikipedia.org/wiki/Authenticated_encryption
.. _issue #19 on Github: https://github.com/sybrenstuvel/python-rsa/issues/13

The VARBLOCK file format is as follows, where || denotes byte concatenation:

    FILE := VERSION || BLOCK || BLOCK ...

    BLOCK := LENGTH || DATA

    LENGTH := varint-encoded length of the subsequent data. Varint comes from
    Google Protobuf, and encodes an integer into a variable number of bytes.
    Each byte uses the 7 lowest bits to encode the value. The highest bit set
    to 1 indicates the next byte is also part of the varint. The last byte will
    have this bit set to 0.

This file format is called the VARBLOCK format, in line with the varint format
used to denote the block sizes.

"""
import warnings
from rsa._compat import byte, b
ZERO_BYTE = b('\x00')
VARBLOCK_VERSION = 1
warnings.warn("The 'rsa.varblock' module was deprecated in Python-RSA version 3.4 due to security issues in the VARBLOCK format. See https://github.com/sybrenstuvel/python-rsa/issues/13 for more information.", DeprecationWarning)

def read_varint(infile):
    """Reads a varint from the file.

    When the first byte to be read indicates EOF, (0, 0) is returned. When an
    EOF occurs when at least one byte has been read, an EOFError exception is
    raised.

    :param infile: the file-like object to read from. It should have a read()
        method.
    :returns: (varint, length), the read varint and the number of read bytes.
    """
    varint = 0
    read_bytes = 0
    while True:
        char = infile.read(1)
        if len(char) == 0:
            if read_bytes == 0:
                return (0, 0)
            raise EOFError('EOF while reading varint, value is %i so far' % varint)
        byte = ord(char)
        varint += (byte & 127) << 7 * read_bytes
        read_bytes += 1
        if not byte & 128:
            return (varint, read_bytes)


def write_varint(outfile, value):
    """Writes a varint to a file.

    :param outfile: the file-like object to write to. It should have a write()
        method.
    :returns: the number of written bytes.
    """
    if value == 0:
        outfile.write(ZERO_BYTE)
        return 1
    written_bytes = 0
    while value > 0:
        to_write = value & 127
        value >>= 7
        if value > 0:
            to_write |= 128
        outfile.write(byte(to_write))
        written_bytes += 1

    return written_bytes


def yield_varblocks(infile):
    """Generator, yields each block in the input file.

    :param infile: file to read, is expected to have the VARBLOCK format as
        described in the module's docstring.
    @yields the contents of each block.
    """
    first_char = infile.read(1)
    if len(first_char) == 0:
        raise EOFError('Unable to read VARBLOCK version number')
    version = ord(first_char)
    if version != VARBLOCK_VERSION:
        raise ValueError('VARBLOCK version %i not supported' % version)
    while True:
        block_size, read_bytes = read_varint(infile)
        if read_bytes == 0 and block_size == 0:
            break
        block = infile.read(block_size)
        read_size = len(block)
        if read_size != block_size:
            raise EOFError('Block size is %i, but could read only %i bytes' % (
             block_size, read_size))
        yield block


def yield_fixedblocks(infile, blocksize):
    """Generator, yields each block of ``blocksize`` bytes in the input file.

    :param infile: file to read and separate in blocks.
    :returns: a generator that yields the contents of each block
    """
    while True:
        block = infile.read(blocksize)
        read_bytes = len(block)
        if read_bytes == 0:
            break
        yield block
        if read_bytes < blocksize:
            break