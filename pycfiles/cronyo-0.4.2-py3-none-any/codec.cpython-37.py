# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/idna/idna/codec.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 3299 bytes
from .core import encode, decode, alabel, ulabel, IDNAError
import codecs, re
_unicode_dots_re = re.compile('[.。．｡]')

class Codec(codecs.Codec):

    def encode(self, data, errors='strict'):
        if errors != 'strict':
            raise IDNAError('Unsupported error handling "{0}"'.format(errors))
        else:
            return data or ('', 0)
        return (encode(data), len(data))

    def decode(self, data, errors='strict'):
        if errors != 'strict':
            raise IDNAError('Unsupported error handling "{0}"'.format(errors))
        else:
            return data or ('', 0)
        return (decode(data), len(data))


class IncrementalEncoder(codecs.BufferedIncrementalEncoder):

    def _buffer_encode(self, data, errors, final):
        if errors != 'strict':
            raise IDNAError('Unsupported error handling "{0}"'.format(errors))
        else:
            if not data:
                return ('', 0)
            labels = _unicode_dots_re.split(data)
            trailing_dot = ''
            if labels:
                if not labels[(-1)]:
                    trailing_dot = '.'
                    del labels[-1]
                else:
                    if not final:
                        del labels[-1]
                        if labels:
                            trailing_dot = '.'
        result = []
        size = 0
        for label in labels:
            result.append(alabel(label))
            if size:
                size += 1
            size += len(label)

        result = '.'.join(result) + trailing_dot
        size += len(trailing_dot)
        return (result, size)


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):

    def _buffer_decode(self, data, errors, final):
        if errors != 'strict':
            raise IDNAError('Unsupported error handling "{0}"'.format(errors))
        else:
            if not data:
                return ('', 0)
            if isinstance(data, unicode):
                labels = _unicode_dots_re.split(data)
            else:
                data = str(data)
                unicode(data, 'ascii')
                labels = data.split('.')
            trailing_dot = ''
            if labels:
                if not labels[(-1)]:
                    trailing_dot = '.'
                    del labels[-1]
                else:
                    if not final:
                        del labels[-1]
                        if labels:
                            trailing_dot = '.'
        result = []
        size = 0
        for label in labels:
            result.append(ulabel(label))
            if size:
                size += 1
            size += len(label)

        result = '.'.join(result) + trailing_dot
        size += len(trailing_dot)
        return (result, size)


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='idna',
      encode=(Codec().encode),
      decode=(Codec().decode),
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamwriter=StreamWriter,
      streamreader=StreamReader)