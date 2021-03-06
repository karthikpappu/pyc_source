# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/webencodings/webencodings/tests.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 6563 bytes
"""

    webencodings.tests
    ~~~~~~~~~~~~~~~~~~

    A basic test suite for Encoding.

    :copyright: Copyright 2012 by Simon Sapin
    :license: BSD, see LICENSE for details.

"""
from __future__ import unicode_literals
from . import lookup, LABELS, decode, encode, iter_decode, iter_encode, IncrementalDecoder, IncrementalEncoder, UTF8

def assert_raises(exception, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except exception:
        return
    else:
        raise AssertionError('Did not raise %s.' % exception)


def test_labels():
    if not lookup('utf-8').name == 'utf-8':
        raise AssertionError
    else:
        if not lookup('Utf-8').name == 'utf-8':
            raise AssertionError
        else:
            if not lookup('UTF-8').name == 'utf-8':
                raise AssertionError
            else:
                if not lookup('utf8').name == 'utf-8':
                    raise AssertionError
                else:
                    if not lookup('utf8').name == 'utf-8':
                        raise AssertionError
                    else:
                        if not lookup('utf8 ').name == 'utf-8':
                            raise AssertionError
                        else:
                            if not lookup(' \r\nutf8\t').name == 'utf-8':
                                raise AssertionError
                            else:
                                assert lookup('u8') is None
                                assert lookup('utf-8\xa0') is None
                            assert lookup('US-ASCII').name == 'windows-1252'
                        assert lookup('iso-8859-1').name == 'windows-1252'
                    assert lookup('latin1').name == 'windows-1252'
                assert lookup('LATIN1').name == 'windows-1252'
            assert lookup('latin-1') is None
        assert lookup('LATİN1') is None


def test_all_labels():
    for label in LABELS:
        if not decode(b'', label) == ('', lookup(label)):
            raise AssertionError
        else:
            if not encode('', label) == b'':
                raise AssertionError
            else:
                for repeat in (0, 1, 12):
                    output, _ = iter_decode([b''] * repeat, label)
                    assert list(output) == []
                    assert list(iter_encode([''] * repeat, label)) == []

                decoder = IncrementalDecoder(label)
                assert decoder.decode(b'') == ''
                assert decoder.decode(b'', final=True) == ''
            encoder = IncrementalEncoder(label)
            assert encoder.encode('') == b''
        assert encoder.encode('', final=True) == b''

    for name in set(LABELS.values()):
        assert lookup(name).name == name


def test_invalid_label():
    assert_raises(LookupError, decode, b'\xef\xbb\xbf\xc3\xa9', 'invalid')
    assert_raises(LookupError, encode, 'é', 'invalid')
    assert_raises(LookupError, iter_decode, [], 'invalid')
    assert_raises(LookupError, iter_encode, [], 'invalid')
    assert_raises(LookupError, IncrementalDecoder, 'invalid')
    assert_raises(LookupError, IncrementalEncoder, 'invalid')


def test_decode():
    if not decode(b'\x80', 'latin1') == ('€', lookup('latin1')):
        raise AssertionError
    else:
        if not decode(b'\x80', lookup('latin1')) == ('€', lookup('latin1')):
            raise AssertionError
        else:
            if not decode(b'\xc3\xa9', 'utf8') == ('é', lookup('utf8')):
                raise AssertionError
            else:
                if not decode(b'\xc3\xa9', UTF8) == ('é', lookup('utf8')):
                    raise AssertionError
                else:
                    if not decode(b'\xc3\xa9', 'ascii') == ('Ã©', lookup('ascii')):
                        raise AssertionError
                    else:
                        if not decode(b'\xef\xbb\xbf\xc3\xa9', 'ascii') == ('é', lookup('utf8')):
                            raise AssertionError
                        else:
                            if not decode(b'\xfe\xff\x00\xe9', 'ascii') == ('é', lookup('utf-16be')):
                                raise AssertionError
                            else:
                                if not decode(b'\xff\xfe\xe9\x00', 'ascii') == ('é', lookup('utf-16le')):
                                    raise AssertionError
                                elif not decode(b'\xfe\xff\xe9\x00', 'ascii') == ('\ue900', lookup('utf-16be')):
                                    raise AssertionError
                                assert decode(b'\xff\xfe\x00\xe9', 'ascii') == ('\ue900', lookup('utf-16le'))
                            assert decode(b'\x00\xe9', 'UTF-16BE') == ('é', lookup('utf-16be'))
                        assert decode(b'\xe9\x00', 'UTF-16LE') == ('é', lookup('utf-16le'))
                    assert decode(b'\xe9\x00', 'UTF-16') == ('é', lookup('utf-16le'))
                assert decode(b'\xe9\x00', 'UTF-16BE') == ('\ue900', lookup('utf-16be'))
            assert decode(b'\x00\xe9', 'UTF-16LE') == ('\ue900', lookup('utf-16le'))
        assert decode(b'\x00\xe9', 'UTF-16') == ('\ue900', lookup('utf-16le'))


def test_encode():
    if not encode('é', 'latin1') == b'\xe9':
        raise AssertionError
    else:
        if not encode('é', 'utf8') == b'\xc3\xa9':
            raise AssertionError
        else:
            if not encode('é', 'utf8') == b'\xc3\xa9':
                raise AssertionError
            elif not encode('é', 'utf-16') == b'\xe9\x00':
                raise AssertionError
            assert encode('é', 'utf-16le') == b'\xe9\x00'
        assert encode('é', 'utf-16be') == b'\x00\xe9'


def test_iter_decode():

    def iter_decode_to_string(input, fallback_encoding):
        output, _encoding = iter_decode(input, fallback_encoding)
        return ''.join(output)

    if not iter_decode_to_string([], 'latin1') == '':
        raise AssertionError
    else:
        if not iter_decode_to_string([b''], 'latin1') == '':
            raise AssertionError
        else:
            if not iter_decode_to_string([b'\xe9'], 'latin1') == 'é':
                raise AssertionError
            else:
                if not iter_decode_to_string([b'hello'], 'latin1') == 'hello':
                    raise AssertionError
                else:
                    if not iter_decode_to_string([b'he', b'llo'], 'latin1') == 'hello':
                        raise AssertionError
                    else:
                        if not iter_decode_to_string([b'hell', b'o'], 'latin1') == 'hello':
                            raise AssertionError
                        else:
                            if not iter_decode_to_string([b'\xc3\xa9'], 'latin1') == 'Ã©':
                                raise AssertionError
                            else:
                                if not iter_decode_to_string([b'\xef\xbb\xbf\xc3\xa9'], 'latin1') == 'é':
                                    raise AssertionError
                                else:
                                    assert iter_decode_to_string([
                                     b'\xef\xbb\xbf', b'\xc3', b'\xa9'], 'latin1') == 'é'
                                    assert iter_decode_to_string([
                                     b'\xef\xbb\xbf', b'a', b'\xc3'], 'latin1') == 'a�'
                                assert iter_decode_to_string([
                                 b'', b'\xef', b'', b'', b'\xbb\xbf\xc3', b'\xa9'], 'latin1') == 'é'
                            assert iter_decode_to_string([b'\xef\xbb\xbf'], 'latin1') == ''
                        assert iter_decode_to_string([b'\xef\xbb'], 'latin1') == 'ï»'
                    assert iter_decode_to_string([b'\xfe\xff\x00\xe9'], 'latin1') == 'é'
                assert iter_decode_to_string([b'\xff\xfe\xe9\x00'], 'latin1') == 'é'
            assert iter_decode_to_string([
             b'', b'\xff', b'', b'', b'\xfe\xe9', b'\x00'], 'latin1') == 'é'
        assert iter_decode_to_string([
         b'', b'h\xe9', b'llo'], 'x-user-defined') == 'h\uf7e9llo'


def test_iter_encode():
    if not (b'').join(iter_encode([], 'latin1')) == b'':
        raise AssertionError
    else:
        if not (b'').join(iter_encode([''], 'latin1')) == b'':
            raise AssertionError
        else:
            if not (b'').join(iter_encode(['é'], 'latin1')) == b'\xe9':
                raise AssertionError
            else:
                if not (b'').join(iter_encode(['', 'é', '', ''], 'latin1')) == b'\xe9':
                    raise AssertionError
                elif not (b'').join(iter_encode(['', 'é', '', ''], 'utf-16')) == b'\xe9\x00':
                    raise AssertionError
                assert (b'').join(iter_encode(['', 'é', '', ''], 'utf-16le')) == b'\xe9\x00'
            assert (b'').join(iter_encode(['', 'é', '', ''], 'utf-16be')) == b'\x00\xe9'
        assert (b'').join(iter_encode([
         '', 'h\uf7e9', '', 'llo'], 'x-user-defined')) == b'h\xe9llo'


def test_x_user_defined():
    encoded = b'2,\x0c\x0b\x1aO\xd9#\xcb\x0f\xc9\xbbt\xcf\xa8\xca'
    decoded = '2,\x0c\x0b\x1aO\uf7d9#\uf7cb\x0f\uf7c9\uf7bbt\uf7cf\uf7a8\uf7ca'
    encoded = b'aa'
    decoded = 'aa'
    if not decode(encoded, 'x-user-defined') == (decoded, lookup('x-user-defined')):
        raise AssertionError
    elif not encode(decoded, 'x-user-defined') == encoded:
        raise AssertionError