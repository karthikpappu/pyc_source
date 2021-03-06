# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/util/pil_fix.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2053 bytes
__doc__ = '\nImporting this module installs support for 16-bit images in PIL.\nThis works by patching objects in the PIL namespace; no files are\nmodified.\n'
from PIL import Image
if Image.VERSION == '1.1.7':
    Image._MODE_CONV['I;16'] = (
     '%su2' % Image._ENDIAN, None)
    Image._fromarray_typemap[((1, 1), '<u2')] = ('I', 'I;16')
if Image.VERSION == '1.1.6':
    Image._MODE_CONV['I;16'] = (
     '%su2' % Image._ENDIAN, None)

    def fromarray(obj, mode=None):
        arr = obj.__array_interface__
        shape = arr['shape']
        ndim = len(shape)
        try:
            strides = arr['strides']
        except KeyError:
            strides = None

        if mode is None:
            typestr = arr['typestr']
            if not typestr[0] == '|':
                if not typestr[0] == Image._ENDIAN:
                    if not typestr[1:] not in ('u1', 'b1', 'i4', 'f4'):
                        raise TypeError('cannot handle data-type')
            elif typestr[0] == Image._ENDIAN:
                typestr = typestr[1:3]
            else:
                typestr = typestr[:2]
            if typestr == 'i4':
                mode = 'I'
            elif typestr == 'u2':
                mode = 'I;16'
            elif typestr == 'f4':
                mode = 'F'
            elif typestr == 'b1':
                mode = '1'
            elif ndim == 2:
                mode = 'L'
            elif ndim == 3:
                mode = 'RGB'
            elif ndim == 4:
                mode = 'RGBA'
            else:
                raise TypeError('Do not understand data.')
        else:
            ndmax = 4
            bad_dims = 0
            if mode in ('1', 'L', 'I', 'P', 'F'):
                ndmax = 2
            elif mode == 'RGB':
                ndmax = 3
        if ndim > ndmax:
            raise ValueError('Too many dimensions.')
        size = shape[:2][::-1]
        if strides is not None:
            obj = obj.tostring()
        return frombuffer(mode, size, obj, 'raw', mode, 0, 1)


    Image.fromarray = fromarray