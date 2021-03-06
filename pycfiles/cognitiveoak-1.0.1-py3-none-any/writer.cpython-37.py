# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\segpy\writer.py
# Compiled at: 2019-12-13 21:48:37
# Size of source mod 2**32: 2831 bytes
import os, sys
sys.path.append(os.path.dirname(__file__)[:-6][:-4][:-13])
from cognitivegeo.src.segpy.encoding import ASCII, is_supported_encoding, UnsupportedEncodingError
from cognitivegeo.src.segpy.packer import HeaderPacker
from cognitivegeo.src.segpy.trace_header import TraceHeaderRev1
from cognitivegeo.src.segpy.toolkit import write_textual_reel_header, write_binary_reel_header, write_trace_header, write_trace_samples, write_extended_textual_headers

def write_segy(fh, seg_y_data, encoding=None, trace_header_format=TraceHeaderRev1, endian='>', progress=None):
    """
    Args:
        fh: A file-like object open for binary write.

        seg_y_data:  An object from which the headers and trace_samples data can be retrieved. Requires the following
            properties and methods:
              seg_y_data.textual_reel_header
              seg_y_data.binary_reel_header
              seg_y_data.extended_textual_header
              seg_y_data.trace_indexes
              seg_y_data.trace_header(trace_index)
              seg_y_data.trace_samples(trace_index)

              seg_y_data.encoding
              seg_y_data.endian

              One such legitimate object would be a SegYReader instance.

        trace_header_format: The class which defines the layout of the trace header. Defaults to TraceHeaderRev1.

        encoding: Optional encoding for text data. Typically 'cp037' for EBCDIC or 'ascii' for ASCII. If omitted, the
            seg_y_data object will be queries for an encoding property.

        endian: Big endian by default. If omitted, the seg_y_data object will be queried for an encoding property.

        progress: An optional progress bar object.

    Raises:
        UnsupportedEncodingError: If the specified encoding is neither ASCII nor EBCDIC
        UnicodeError: If textual data provided cannot be encoded into the required encoding.
    """
    encoding = encoding or 
    if not is_supported_encoding(encoding):
        raise UnsupportedEncodingError('Writing SEG Y', encoding)
    write_textual_reel_header(fh, seg_y_data.textual_reel_header, encoding)
    write_binary_reel_header(fh, seg_y_data.binary_reel_header, endian)
    write_extended_textual_headers(fh, seg_y_data.extended_textual_header, encoding)
    trace_header_packer = HeaderPacker(trace_header_format, endian)
    for trace_index in seg_y_data.trace_indexes():
        write_trace_header(fh, seg_y_data.trace_header(trace_index), trace_header_packer)
        write_trace_samples(fh, (seg_y_data.trace_samples(trace_index)), (seg_y_data.data_sample_format), endian=endian)