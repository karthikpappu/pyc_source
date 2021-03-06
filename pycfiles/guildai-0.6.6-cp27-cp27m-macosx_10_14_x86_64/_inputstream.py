# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/html5lib/_inputstream.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import text_type, binary_type
from pip._vendor.six.moves import http_client, urllib
import codecs, re
from pip._vendor import webencodings
from .constants import EOF, spaceCharacters, asciiLetters, asciiUppercase
from .constants import _ReparseException
from . import _utils
from io import StringIO
try:
    from io import BytesIO
except ImportError:
    BytesIO = StringIO

spaceCharactersBytes = frozenset([ item.encode(b'ascii') for item in spaceCharacters ])
asciiLettersBytes = frozenset([ item.encode(b'ascii') for item in asciiLetters ])
asciiUppercaseBytes = frozenset([ item.encode(b'ascii') for item in asciiUppercase ])
spacesAngleBrackets = spaceCharactersBytes | frozenset([b'>', b'<'])
invalid_unicode_no_surrogate = b'[\x01-\x08\x0b\x0e-\x1f\x7f-\x9f\ufdd0-\ufdef\ufffe\uffff\U0001fffe\U0001ffff\U0002fffe\U0002ffff\U0003fffe\U0003ffff\U0004fffe\U0004ffff\U0005fffe\U0005ffff\U0006fffe\U0006ffff\U0007fffe\U0007ffff\U0008fffe\U0008ffff\U0009fffe\U0009ffff\U000afffe\U000affff\U000bfffe\U000bffff\U000cfffe\U000cffff\U000dfffe\U000dffff\U000efffe\U000effff\U000ffffe\U000fffff\U0010fffe\U0010ffff]'
if _utils.supports_lone_surrogates:
    assert invalid_unicode_no_surrogate[(-1)] == b']' and invalid_unicode_no_surrogate.count(b']') == 1
    invalid_unicode_re = re.compile(invalid_unicode_no_surrogate[:-1] + eval(b'"\\uD800-\\uDFFF"') + b']')
else:
    invalid_unicode_re = re.compile(invalid_unicode_no_surrogate)
non_bmp_invalid_codepoints = set([131070, 131071, 196606, 196607, 262142,
 262143, 327678, 327679, 393214, 393215,
 458750, 458751, 524286, 524287, 589822,
 589823, 655358, 655359, 720894, 720895,
 786430, 786431, 851966, 851967, 917502,
 917503, 983038, 983039, 1048574, 1048575,
 1114110, 1114111])
ascii_punctuation_re = re.compile(b'[\t-\r -/:-@\\[-`{-~]')
charsUntilRegEx = {}

class BufferedStream(object):
    """Buffering for streams that do not have buffering of their own

    The buffer is implemented as a list of chunks on the assumption that
    joining many strings will be slow since it is O(n**2)
    """

    def __init__(self, stream):
        self.stream = stream
        self.buffer = []
        self.position = [-1, 0]

    def tell(self):
        pos = 0
        for chunk in self.buffer[:self.position[0]]:
            pos += len(chunk)

        pos += self.position[1]
        return pos

    def seek(self, pos):
        assert pos <= self._bufferedBytes()
        offset = pos
        i = 0
        while len(self.buffer[i]) < offset:
            offset -= len(self.buffer[i])
            i += 1

        self.position = [
         i, offset]

    def read(self, bytes):
        if not self.buffer:
            return self._readStream(bytes)
        else:
            if self.position[0] == len(self.buffer) and self.position[1] == len(self.buffer[(-1)]):
                return self._readStream(bytes)
            return self._readFromBuffer(bytes)

    def _bufferedBytes(self):
        return sum([ len(item) for item in self.buffer ])

    def _readStream(self, bytes):
        data = self.stream.read(bytes)
        self.buffer.append(data)
        self.position[0] += 1
        self.position[1] = len(data)
        return data

    def _readFromBuffer(self, bytes):
        remainingBytes = bytes
        rv = []
        bufferIndex = self.position[0]
        bufferOffset = self.position[1]
        while bufferIndex < len(self.buffer) and remainingBytes != 0:
            assert remainingBytes > 0
            bufferedData = self.buffer[bufferIndex]
            if remainingBytes <= len(bufferedData) - bufferOffset:
                bytesToRead = remainingBytes
                self.position = [bufferIndex, bufferOffset + bytesToRead]
            else:
                bytesToRead = len(bufferedData) - bufferOffset
                self.position = [bufferIndex, len(bufferedData)]
                bufferIndex += 1
            rv.append(bufferedData[bufferOffset:bufferOffset + bytesToRead])
            remainingBytes -= bytesToRead
            bufferOffset = 0

        if remainingBytes:
            rv.append(self._readStream(remainingBytes))
        return (b'').join(rv)


def HTMLInputStream(source, **kwargs):
    if isinstance(source, http_client.HTTPResponse) or isinstance(source, urllib.response.addbase) and isinstance(source.fp, http_client.HTTPResponse):
        isUnicode = False
    elif hasattr(source, b'read'):
        isUnicode = isinstance(source.read(0), text_type)
    else:
        isUnicode = isinstance(source, text_type)
    if isUnicode:
        encodings = [ x for x in kwargs if x.endswith(b'_encoding') ]
        if encodings:
            raise TypeError(b'Cannot set an encoding with a unicode input, set %r' % encodings)
        return HTMLUnicodeInputStream(source, **kwargs)
    else:
        return HTMLBinaryInputStream(source, **kwargs)


class HTMLUnicodeInputStream(object):
    """Provides a unicode stream of characters to the HTMLTokenizer.

    This class takes care of character encoding and removing or replacing
    incorrect byte-sequences and also provides column and line tracking.

    """
    _defaultChunkSize = 10240

    def __init__(self, source):
        """Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)

        """
        if not _utils.supports_lone_surrogates:
            self.reportCharacterErrors = None
        elif len(b'\U0010ffff') == 1:
            self.reportCharacterErrors = self.characterErrorsUCS4
        else:
            self.reportCharacterErrors = self.characterErrorsUCS2
        self.newLines = [
         0]
        self.charEncoding = (
         lookupEncoding(b'utf-8'), b'certain')
        self.dataStream = self.openStream(source)
        self.reset()
        return

    def reset(self):
        self.chunk = b''
        self.chunkSize = 0
        self.chunkOffset = 0
        self.errors = []
        self.prevNumLines = 0
        self.prevNumCols = 0
        self._bufferedCharacter = None
        return

    def openStream(self, source):
        """Produces a file object from source.

        source can be either a file object, local filename or a string.

        """
        if hasattr(source, b'read'):
            stream = source
        else:
            stream = StringIO(source)
        return stream

    def _position(self, offset):
        chunk = self.chunk
        nLines = chunk.count(b'\n', 0, offset)
        positionLine = self.prevNumLines + nLines
        lastLinePos = chunk.rfind(b'\n', 0, offset)
        if lastLinePos == -1:
            positionColumn = self.prevNumCols + offset
        else:
            positionColumn = offset - (lastLinePos + 1)
        return (
         positionLine, positionColumn)

    def position(self):
        """Returns (line, col) of the current position in the stream."""
        line, col = self._position(self.chunkOffset)
        return (line + 1, col)

    def char(self):
        """ Read one character from the stream or queue if available. Return
            EOF when EOF is reached.
        """
        if self.chunkOffset >= self.chunkSize:
            if not self.readChunk():
                return EOF
        chunkOffset = self.chunkOffset
        char = self.chunk[chunkOffset]
        self.chunkOffset = chunkOffset + 1
        return char

    def readChunk(self, chunkSize=None):
        if chunkSize is None:
            chunkSize = self._defaultChunkSize
        self.prevNumLines, self.prevNumCols = self._position(self.chunkSize)
        self.chunk = b''
        self.chunkSize = 0
        self.chunkOffset = 0
        data = self.dataStream.read(chunkSize)
        if self._bufferedCharacter:
            data = self._bufferedCharacter + data
            self._bufferedCharacter = None
        elif not data:
            return False
        if len(data) > 1:
            lastv = ord(data[(-1)])
            if lastv == 13 or 55296 <= lastv <= 56319:
                self._bufferedCharacter = data[(-1)]
                data = data[:-1]
        if self.reportCharacterErrors:
            self.reportCharacterErrors(data)
        data = data.replace(b'\r\n', b'\n')
        data = data.replace(b'\r', b'\n')
        self.chunk = data
        self.chunkSize = len(data)
        return True

    def characterErrorsUCS4(self, data):
        for _ in range(len(invalid_unicode_re.findall(data))):
            self.errors.append(b'invalid-codepoint')

    def characterErrorsUCS2(self, data):
        skip = False
        for match in invalid_unicode_re.finditer(data):
            if skip:
                continue
            codepoint = ord(match.group())
            pos = match.start()
            if _utils.isSurrogatePair(data[pos:pos + 2]):
                char_val = _utils.surrogatePairToCodepoint(data[pos:pos + 2])
                if char_val in non_bmp_invalid_codepoints:
                    self.errors.append(b'invalid-codepoint')
                skip = True
            elif codepoint >= 55296 and codepoint <= 57343 and pos == len(data) - 1:
                self.errors.append(b'invalid-codepoint')
            else:
                skip = False
                self.errors.append(b'invalid-codepoint')

    def charsUntil(self, characters, opposite=False):
        """ Returns a string of characters from the stream up to but not
        including any character in 'characters' or EOF. 'characters' must be
        a container that supports the 'in' method and iteration over its
        characters.
        """
        try:
            chars = charsUntilRegEx[(characters, opposite)]
        except KeyError:
            for c in characters:
                assert ord(c) < 128

            regex = (b'').join([ b'\\x%02x' % ord(c) for c in characters ])
            if not opposite:
                regex = b'^%s' % regex
            chars = charsUntilRegEx[(characters, opposite)] = re.compile(b'[%s]+' % regex)

        rv = []
        while True:
            m = chars.match(self.chunk, self.chunkOffset)
            if m is None:
                if self.chunkOffset != self.chunkSize:
                    break
            else:
                end = m.end()
                if end != self.chunkSize:
                    rv.append(self.chunk[self.chunkOffset:end])
                    self.chunkOffset = end
                    break
            rv.append(self.chunk[self.chunkOffset:])
            if not self.readChunk():
                break

        r = (b'').join(rv)
        return r

    def unget(self, char):
        if char is not None:
            if self.chunkOffset == 0:
                self.chunk = char + self.chunk
                self.chunkSize += 1
            else:
                self.chunkOffset -= 1
                assert self.chunk[self.chunkOffset] == char
        return


class HTMLBinaryInputStream(HTMLUnicodeInputStream):
    """Provides a unicode stream of characters to the HTMLTokenizer.

    This class takes care of character encoding and removing or replacing
    incorrect byte-sequences and also provides column and line tracking.

    """

    def __init__(self, source, override_encoding=None, transport_encoding=None, same_origin_parent_encoding=None, likely_encoding=None, default_encoding=b'windows-1252', useChardet=True):
        """Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)

        """
        self.rawStream = self.openStream(source)
        HTMLUnicodeInputStream.__init__(self, self.rawStream)
        self.numBytesMeta = 1024
        self.numBytesChardet = 100
        self.override_encoding = override_encoding
        self.transport_encoding = transport_encoding
        self.same_origin_parent_encoding = same_origin_parent_encoding
        self.likely_encoding = likely_encoding
        self.default_encoding = default_encoding
        self.charEncoding = self.determineEncoding(useChardet)
        assert self.charEncoding[0] is not None
        self.reset()
        return

    def reset(self):
        self.dataStream = self.charEncoding[0].codec_info.streamreader(self.rawStream, b'replace')
        HTMLUnicodeInputStream.reset(self)

    def openStream(self, source):
        """Produces a file object from source.

        source can be either a file object, local filename or a string.

        """
        if hasattr(source, b'read'):
            stream = source
        else:
            stream = BytesIO(source)
        try:
            stream.seek(stream.tell())
        except:
            stream = BufferedStream(stream)

        return stream

    def determineEncoding(self, chardet=True):
        charEncoding = (
         self.detectBOM(), b'certain')
        if charEncoding[0] is not None:
            return charEncoding
        else:
            charEncoding = (
             lookupEncoding(self.override_encoding), b'certain')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             lookupEncoding(self.transport_encoding), b'certain')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             self.detectEncodingMeta(), b'tentative')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             lookupEncoding(self.same_origin_parent_encoding), b'tentative')
            if charEncoding[0] is not None and not charEncoding[0].name.startswith(b'utf-16'):
                return charEncoding
            charEncoding = (
             lookupEncoding(self.likely_encoding), b'tentative')
            if charEncoding[0] is not None:
                return charEncoding
            if chardet:
                try:
                    from pip._vendor.chardet.universaldetector import UniversalDetector
                except ImportError:
                    pass
                else:
                    buffers = []
                    detector = UniversalDetector()
                    while not detector.done:
                        buffer = self.rawStream.read(self.numBytesChardet)
                        assert isinstance(buffer, bytes)
                        if not buffer:
                            break
                        buffers.append(buffer)
                        detector.feed(buffer)

                    detector.close()
                    encoding = lookupEncoding(detector.result[b'encoding'])
                    self.rawStream.seek(0)
                    if encoding is not None:
                        return (encoding, b'tentative')

            charEncoding = (
             lookupEncoding(self.default_encoding), b'tentative')
            if charEncoding[0] is not None:
                return charEncoding
            return (
             lookupEncoding(b'windows-1252'), b'tentative')

    def changeEncoding(self, newEncoding):
        assert self.charEncoding[1] != b'certain'
        newEncoding = lookupEncoding(newEncoding)
        if newEncoding is None:
            return
        else:
            if newEncoding.name in ('utf-16be', 'utf-16le'):
                newEncoding = lookupEncoding(b'utf-8')
                assert newEncoding is not None
            elif newEncoding == self.charEncoding[0]:
                self.charEncoding = (
                 self.charEncoding[0], b'certain')
            else:
                self.rawStream.seek(0)
                self.charEncoding = (newEncoding, b'certain')
                self.reset()
                raise _ReparseException(b'Encoding changed from %s to %s' % (self.charEncoding[0], newEncoding))
            return

    def detectBOM(self):
        """Attempts to detect at BOM at the start of the stream. If
        an encoding can be determined from the BOM return the name of the
        encoding otherwise return None"""
        bomDict = {codecs.BOM_UTF8: b'utf-8', 
           codecs.BOM_UTF16_LE: b'utf-16le', 
           codecs.BOM_UTF16_BE: b'utf-16be', codecs.BOM_UTF32_LE: b'utf-32le', 
           codecs.BOM_UTF32_BE: b'utf-32be'}
        string = self.rawStream.read(4)
        if not isinstance(string, bytes):
            raise AssertionError
            encoding = bomDict.get(string[:3])
            seek = 3
            if not encoding:
                encoding = bomDict.get(string)
                seek = 4
                encoding = encoding or bomDict.get(string[:2])
                seek = 2
        if encoding:
            self.rawStream.seek(seek)
            return lookupEncoding(encoding)
        else:
            self.rawStream.seek(0)
            return
            return

    def detectEncodingMeta(self):
        """Report the encoding declared by the meta element
        """
        buffer = self.rawStream.read(self.numBytesMeta)
        assert isinstance(buffer, bytes)
        parser = EncodingParser(buffer)
        self.rawStream.seek(0)
        encoding = parser.getEncoding()
        if encoding is not None and encoding.name in ('utf-16be', 'utf-16le'):
            encoding = lookupEncoding(b'utf-8')
        return encoding


class EncodingBytes(bytes):
    """String-like object with an associated position and various extra methods
    If the position is ever greater than the string length then an exception is
    raised"""

    def __new__(self, value):
        assert isinstance(value, bytes)
        return bytes.__new__(self, value.lower())

    def __init__(self, value):
        self._position = -1

    def __iter__(self):
        return self

    def __next__(self):
        p = self._position = self._position + 1
        if p >= len(self):
            raise StopIteration
        elif p < 0:
            raise TypeError
        return self[p:p + 1]

    def next(self):
        return self.__next__()

    def previous(self):
        p = self._position
        if p >= len(self):
            raise StopIteration
        elif p < 0:
            raise TypeError
        self._position = p = p - 1
        return self[p:p + 1]

    def setPosition(self, position):
        if self._position >= len(self):
            raise StopIteration
        self._position = position

    def getPosition(self):
        if self._position >= len(self):
            raise StopIteration
        if self._position >= 0:
            return self._position
        else:
            return
            return

    position = property(getPosition, setPosition)

    def getCurrentByte(self):
        return self[self.position:self.position + 1]

    currentByte = property(getCurrentByte)

    def skip(self, chars=spaceCharactersBytes):
        """Skip past a list of characters"""
        p = self.position
        while p < len(self):
            c = self[p:p + 1]
            if c not in chars:
                self._position = p
                return c
            p += 1

        self._position = p
        return

    def skipUntil(self, chars):
        p = self.position
        while p < len(self):
            c = self[p:p + 1]
            if c in chars:
                self._position = p
                return c
            p += 1

        self._position = p
        return

    def matchBytes(self, bytes):
        """Look for a sequence of bytes at the start of a string. If the bytes
        are found return True and advance the position to the byte after the
        match. Otherwise return False and leave the position alone"""
        p = self.position
        data = self[p:p + len(bytes)]
        rv = data.startswith(bytes)
        if rv:
            self.position += len(bytes)
        return rv

    def jumpTo(self, bytes):
        """Look for the next sequence of bytes matching a given sequence. If
        a match is found advance the position to the last byte of the match"""
        newPosition = self[self.position:].find(bytes)
        if newPosition > -1:
            if self._position == -1:
                self._position = 0
            self._position += newPosition + len(bytes) - 1
            return True
        raise StopIteration


class EncodingParser(object):
    """Mini parser for detecting character encoding from meta elements"""

    def __init__(self, data):
        """string - the data to work on for encoding detection"""
        self.data = EncodingBytes(data)
        self.encoding = None
        return

    def getEncoding(self):
        methodDispatch = (
         (
          b'<!--', self.handleComment),
         (
          b'<meta', self.handleMeta),
         (
          b'</', self.handlePossibleEndTag),
         (
          b'<!', self.handleOther),
         (
          b'<?', self.handleOther),
         (
          b'<', self.handlePossibleStartTag))
        for _ in self.data:
            keepParsing = True
            for key, method in methodDispatch:
                if self.data.matchBytes(key):
                    try:
                        keepParsing = method()
                        break
                    except StopIteration:
                        keepParsing = False
                        break

            if not keepParsing:
                break

        return self.encoding

    def handleComment(self):
        """Skip over comments"""
        return self.data.jumpTo(b'-->')

    def handleMeta(self):
        if self.data.currentByte not in spaceCharactersBytes:
            return True
        else:
            hasPragma = False
            pendingEncoding = None
            while True:
                attr = self.getAttribute()
                if attr is None:
                    return True
                if attr[0] == b'http-equiv':
                    hasPragma = attr[1] == b'content-type'
                    if hasPragma and pendingEncoding is not None:
                        self.encoding = pendingEncoding
                        return False
                elif attr[0] == b'charset':
                    tentativeEncoding = attr[1]
                    codec = lookupEncoding(tentativeEncoding)
                    if codec is not None:
                        self.encoding = codec
                        return False
                elif attr[0] == b'content':
                    contentParser = ContentAttrParser(EncodingBytes(attr[1]))
                    tentativeEncoding = contentParser.parse()
                    if tentativeEncoding is not None:
                        codec = lookupEncoding(tentativeEncoding)
                        if codec is not None:
                            if hasPragma:
                                self.encoding = codec
                                return False
                            pendingEncoding = codec

            return

    def handlePossibleStartTag(self):
        return self.handlePossibleTag(False)

    def handlePossibleEndTag(self):
        next(self.data)
        return self.handlePossibleTag(True)

    def handlePossibleTag(self, endTag):
        data = self.data
        if data.currentByte not in asciiLettersBytes:
            if endTag:
                data.previous()
                self.handleOther()
            return True
        c = data.skipUntil(spacesAngleBrackets)
        if c == b'<':
            data.previous()
        else:
            attr = self.getAttribute()
            while attr is not None:
                attr = self.getAttribute()

        return True

    def handleOther(self):
        return self.data.jumpTo(b'>')

    def getAttribute(self):
        """Return a name,value pair for the next attribute in the stream,
        if one is found, or None"""
        data = self.data
        c = data.skip(spaceCharactersBytes | frozenset([b'/']))
        assert c is None or len(c) == 1
        if c in ('>', None):
            return
        else:
            attrName = []
            attrValue = []
            while True:
                if c == b'=' and attrName:
                    break
                elif c in spaceCharactersBytes:
                    c = data.skip()
                    break
                else:
                    if c in ('/', '>'):
                        return ((b'').join(attrName), b'')
                    if c in asciiUppercaseBytes:
                        attrName.append(c.lower())
                    else:
                        if c is None:
                            return
                        attrName.append(c)
                c = next(data)

            if c != b'=':
                data.previous()
                return (
                 (b'').join(attrName), b'')
            next(data)
            c = data.skip()
            if c in ("'", '"'):
                quoteChar = c
                while True:
                    c = next(data)
                    if c == quoteChar:
                        next(data)
                        return (
                         (b'').join(attrName), (b'').join(attrValue))
                    if c in asciiUppercaseBytes:
                        attrValue.append(c.lower())
                    else:
                        attrValue.append(c)

            else:
                if c == b'>':
                    return ((b'').join(attrName), b'')
                if c in asciiUppercaseBytes:
                    attrValue.append(c.lower())
                else:
                    if c is None:
                        return
                    attrValue.append(c)
                while True:
                    c = next(data)
                    if c in spacesAngleBrackets:
                        return ((b'').join(attrName), (b'').join(attrValue))
                    if c in asciiUppercaseBytes:
                        attrValue.append(c.lower())
                    else:
                        if c is None:
                            return
                        attrValue.append(c)

            return


class ContentAttrParser(object):

    def __init__(self, data):
        assert isinstance(data, bytes)
        self.data = data

    def parse(self):
        try:
            self.data.jumpTo(b'charset')
            self.data.position += 1
            self.data.skip()
            if not self.data.currentByte == b'=':
                return
            self.data.position += 1
            self.data.skip()
            if self.data.currentByte in ('"', "'"):
                quoteMark = self.data.currentByte
                self.data.position += 1
                oldPosition = self.data.position
                if self.data.jumpTo(quoteMark):
                    return self.data[oldPosition:self.data.position]
                return
            else:
                oldPosition = self.data.position
                try:
                    self.data.skipUntil(spaceCharactersBytes)
                    return self.data[oldPosition:self.data.position]
                except StopIteration:
                    return self.data[oldPosition:]

        except StopIteration:
            return

        return


def lookupEncoding(encoding):
    """Return the python codec name corresponding to an encoding or None if the
    string doesn't correspond to a valid encoding."""
    if isinstance(encoding, binary_type):
        try:
            encoding = encoding.decode(b'ascii')
        except UnicodeDecodeError:
            return

    if encoding is not None:
        try:
            return webencodings.lookup(encoding)
        except AttributeError:
            return

    else:
        return
    return