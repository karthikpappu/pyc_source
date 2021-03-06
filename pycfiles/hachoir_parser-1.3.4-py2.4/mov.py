# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/video/mov.py
# Compiled at: 2009-11-14 22:49:18
"""
Apple Quicktime Movie (file extension ".mov") parser.

Documents:
- Parsing and Writing QuickTime Files in Java (by Chris Adamson, 02/19/2003)
  http://www.onjava.com/pub/a/onjava/2003/02/19/qt_file_format.html
- QuickTime File Format (official technical reference)
  http://developer.apple.com/documentation/QuickTime/QTFF/qtff.pdf
- Apple QuickTime:
  http://wiki.multimedia.cx/index.php?title=Apple_QuickTime
- File type (ftyp):
  http://www.ftyps.com/

Author: Victor Stinner
Creation: 2 august 2006
"""
from hachoir_parser import Parser
from hachoir_core.field import ParserError, FieldSet, MissingField, UInt8, Int16, UInt16, UInt32, TimestampMac32, String, PascalString8, CString, RawBytes, PaddingBytes
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal

class QTFloat32(FieldSet):
    __module__ = __name__
    static_size = 32

    def createFields(self):
        yield Int16(self, 'int_part')
        yield UInt16(self, 'float_part')

    def createValue(self):
        return self['int_part'].value + float(self['float_part'].value) / 65535

    def createDescription(self):
        return str(self.value)


class AtomList(FieldSet):
    __module__ = __name__

    def createFields(self):
        while not self.eof:
            yield Atom(self, 'atom[]')


class TrackHeader(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt8(self, 'version'), hexadecimal)
        yield RawBytes(self, 'flags', 3)
        yield TimestampMac32(self, 'creation_date')
        yield TimestampMac32(self, 'lastmod_date')
        yield UInt32(self, 'track_id')
        yield PaddingBytes(self, 'reserved[]', 8)
        yield UInt32(self, 'duration')
        yield PaddingBytes(self, 'reserved[]', 8)
        yield Int16(self, 'video_layer', 'Middle is 0, negative in front')
        yield PaddingBytes(self, 'other', 2)
        yield QTFloat32(self, 'geom_a', 'Width scale')
        yield QTFloat32(self, 'geom_b', 'Width rotate')
        yield QTFloat32(self, 'geom_u', 'Width angle')
        yield QTFloat32(self, 'geom_c', 'Height rotate')
        yield QTFloat32(self, 'geom_d', 'Height scale')
        yield QTFloat32(self, 'geom_v', 'Height angle')
        yield QTFloat32(self, 'geom_x', 'Position X')
        yield QTFloat32(self, 'geom_y', 'Position Y')
        yield QTFloat32(self, 'geom_w', 'Divider scale')
        yield QTFloat32(self, 'frame_size_width')
        yield QTFloat32(self, 'frame_size_height')


class HDLR(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt8(self, 'version'), hexadecimal)
        yield RawBytes(self, 'flags', 3)
        yield String(self, 'subtype', 8)
        yield String(self, 'manufacturer', 4)
        yield UInt32(self, 'res_flags')
        yield UInt32(self, 'res_flags_mask')
        if self.root.is_mpeg4:
            yield CString(self, 'name')
        else:
            yield PascalString8(self, 'name')


class MediaHeader(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt8(self, 'version'), hexadecimal)
        yield RawBytes(self, 'flags', 3)
        yield TimestampMac32(self, 'creation_date')
        yield TimestampMac32(self, 'lastmod_date')
        yield UInt32(self, 'time_scale')
        yield UInt32(self, 'duration')
        yield UInt16(self, 'mac_lang')
        yield Int16(self, 'quality')


class ELST(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt8(self, 'version'), hexadecimal)
        yield RawBytes(self, 'flags', 3)
        yield UInt32(self, 'nb_edits')
        yield UInt32(self, 'length')
        yield UInt32(self, 'start')
        yield QTFloat32(self, 'playback_speed')


class Load(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'start')
        yield UInt32(self, 'length')
        yield UInt32(self, 'flags')
        yield UInt32(self, 'hints')


class MovieHeader(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt8(self, 'version'), hexadecimal)
        yield RawBytes(self, 'flags', 3)
        yield TimestampMac32(self, 'creation_date')
        yield TimestampMac32(self, 'lastmod_date')
        yield UInt32(self, 'time_scale')
        yield UInt32(self, 'duration')
        yield QTFloat32(self, 'play_speed')
        yield UInt16(self, 'volume')
        yield PaddingBytes(self, 'reserved[]', 10)
        yield QTFloat32(self, 'geom_a', 'Width scale')
        yield QTFloat32(self, 'geom_b', 'Width rotate')
        yield QTFloat32(self, 'geom_u', 'Width angle')
        yield QTFloat32(self, 'geom_c', 'Height rotate')
        yield QTFloat32(self, 'geom_d', 'Height scale')
        yield QTFloat32(self, 'geom_v', 'Height angle')
        yield QTFloat32(self, 'geom_x', 'Position X')
        yield QTFloat32(self, 'geom_y', 'Position Y')
        yield QTFloat32(self, 'geom_w', 'Divider scale')
        yield UInt32(self, 'preview_start')
        yield UInt32(self, 'preview_length')
        yield UInt32(self, 'still_poster')
        yield UInt32(self, 'sel_start')
        yield UInt32(self, 'sel_length')
        yield UInt32(self, 'current_time')
        yield UInt32(self, 'next_track')


class FileType(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield String(self, 'brand', 4, 'Major brand')
        yield UInt32(self, 'version', 'Version')
        while not self.eof:
            yield String(self, 'compat_brand[]', 4, 'Compatible brand')


class Atom(FieldSet):
    __module__ = __name__
    tag_info = {'moov': (AtomList, 'movie', 'Movie'), 'trak': (AtomList, 'track', 'Track'), 'mdia': (AtomList, 'media', 'Media'), 'edts': (AtomList, 'edts', ''), 'minf': (AtomList, 'minf', ''), 'stbl': (AtomList, 'stbl', ''), 'dinf': (AtomList, 'dinf', ''), 'elst': (ELST, 'edts', ''), 'tkhd': (TrackHeader, 'track_hdr', 'Track header'), 'hdlr': (HDLR, 'hdlr', ''), 'mdhd': (MediaHeader, 'media_hdr', 'Media header'), 'load': (Load, 'load', ''), 'mvhd': (MovieHeader, 'movie_hdr', 'Movie header'), 'ftyp': (FileType, 'file_type', 'File type')}
    tag_handler = [ item[0] for item in tag_info ]
    tag_desc = [ item[1] for item in tag_info ]

    def createFields(self):
        yield UInt32(self, 'size')
        yield String(self, 'tag', 4)
        size = self['size'].value
        if size == 1:
            raise ParserError('Extended size is not supported!')
            size = self['size64'].value
        elif size == 0:
            if self._size is None:
                size = (self.parent.size - self.current_size) / 8 - 8
            else:
                size = (self.size - self.current_size) / 8
        else:
            size = size - 8
        if 0 < size:
            tag = self['tag'].value
            if tag in self.tag_info:
                (handler, name, desc) = self.tag_info[tag]
                yield handler(self, name, desc, size=size * 8)
            else:
                yield RawBytes(self, 'data', size)
        return

    def createDescription(self):
        return 'Atom: %s' % self['tag'].value


class MovFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'mov', 'category': 'video', 'file_ext': ('mov', 'qt', 'mp4', 'm4v', 'm4a', 'm4p', 'm4b'), 'mime': ('video/quicktime', 'video/mp4'), 'min_size': 8 * 8, 'magic': (('moov', 4 * 8),), 'description': 'Apple QuickTime movie'}
    BRANDS = {'mp41': 'video/mp4', 'mp42': 'video/mp4'}
    endian = BIG_ENDIAN

    def __init__(self, *args, **kw):
        Parser.__init__(self, *args, **kw)
        self.is_mpeg4 = False

    def validate(self):
        size = self.stream.readBits(0, 32, self.endian)
        if size < 8:
            return 'Invalid first atom size'
        tag = self.stream.readBytes(4 * 8, 4)
        return tag in ('ftyp', 'moov', 'free')

    def createFields(self):
        while not self.eof:
            yield Atom(self, 'atom[]')

    def createMimeType(self):
        first = self[0]
        try:
            if first['tag'].value != 'ftyp':
                return
            file_type = first['file_type']
            brand = file_type['brand'].value
            if brand in self.BRANDS:
                return self.BRANDS[brand]
            for field in file_type.array('compat_brand'):
                brand = field.value
                if brand in self.BRANDS:
                    return self.BRANDS[brand]

        except MissingField:
            pass

        return