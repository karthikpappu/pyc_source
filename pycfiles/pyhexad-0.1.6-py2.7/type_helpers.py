# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\type_helpers.py
# Compiled at: 2015-03-06 08:16:41
import h5py, numpy as np
h5array_dtypes = {'BYTE': np.dtype(np.int8), 
   'DOUBLE': np.dtype(np.float64), 
   'FLOAT': np.dtype(np.float32), 
   'FLOAT32': np.dtype(np.float32), 
   'FLOAT64': np.dtype(np.float64), 
   'INT': np.dtype(np.int32), 
   'INT8': np.dtype(np.int8), 
   'INT16': np.dtype(np.int16), 
   'INT32': np.dtype(np.int32), 
   'INT64': np.dtype(np.int64), 
   'LONG': np.dtype(np.int64), 
   'SHORT': np.dtype(np.int16), 
   'SINGLE': np.dtype(np.float32), 
   'UBYTE': np.dtype(np.uint8), 
   'UINT': np.dtype(np.uint32), 
   'UINT8': np.dtype(np.uint8), 
   'UINT16': np.dtype(np.uint16), 
   'UINT32': np.dtype(np.uint32), 
   'UINT64': np.dtype(np.uint64), 
   'ULONG': np.dtype(np.uint64), 
   'USHORT': np.dtype(np.uint16)}
scalar_dtypes = {'BYTE': np.dtype(np.int8), 
   'DOUBLE': np.dtype(np.float64), 
   'FLOAT': np.dtype(np.float32), 
   'FLOAT32': np.dtype(np.float32), 
   'FLOAT64': np.dtype(np.float64), 
   'INT': np.dtype(np.int32), 
   'INT8': np.dtype(np.int8), 
   'INT16': np.dtype(np.int16), 
   'INT32': np.dtype(np.int32), 
   'INT64': np.dtype(np.int64), 
   'LONG': np.dtype(np.int64), 
   'SHORT': np.dtype(np.int16), 
   'SINGLE': np.dtype(np.float32), 
   'STRING': h5py.special_dtype(vlen=str), 
   'UBYTE': np.dtype(np.uint8), 
   'UINT': np.dtype(np.uint32), 
   'UINT8': np.dtype(np.uint8), 
   'UINT16': np.dtype(np.uint16), 
   'UINT32': np.dtype(np.uint32), 
   'UINT64': np.dtype(np.uint64), 
   'ULONG': np.dtype(np.uint64), 
   'USHORT': np.dtype(np.uint16)}
dtype_excel_substitute = {np.dtype(np.double): np.dtype(np.float64), 
   np.dtype(np.float32): np.dtype(np.float64), 
   np.dtype(np.float64): np.dtype(np.float64), 
   np.dtype(np.int8): np.dtype(np.int32), 
   np.dtype(np.int16): np.dtype(np.int32), 
   np.dtype(np.int32): np.dtype(np.int32), 
   np.dtype(np.int64): np.dtype(np.int32), 
   np.dtype(np.single): np.dtype(np.float64), 
   np.dtype(np.uint8): np.dtype(np.int32), 
   np.dtype(np.uint16): np.dtype(np.int32), 
   np.dtype(np.uint32): np.dtype(np.int32), 
   np.dtype(np.uint64): np.dtype(np.int32)}

def is_supported_h5array_type(dty):
    if not isinstance(dty, np.dtype):
        return False
    else:
        if dty in h5array_dtypes.values():
            return True
        if dty.char in ('S', 'U') or dty == scalar_dtypes['STRING']:
            return True
        return False


def is_supported_h5table_type(dty):
    if not isinstance(dty, np.dtype):
        return False
    else:
        if dty.fields is None:
            return False
        for k in dty.fields:
            field_type = dty.fields[k][0]
            if not (is_supported_h5array_type(field_type) or field_type.char == 'S'):
                return False

        return True


def excel_dtype(dty):
    if not isinstance(dty, np.dtype):
        raise TypeError('Numpy dtype expected.')
    if dty.fields is None:
        if dty in dtype_excel_substitute.keys():
            return dtype_excel_substitute[dty]
        if dty.char in ('S', 'U') or dty == scalar_dtypes['STRING']:
            return scalar_dtypes['STRING']
        raise Exception('Unsupported scalar type.')
    else:
        spec = []
        for n in dty.names:
            field_type = dty.fields[n][0]
            if field_type.char != 'S':
                spec.append((n, excel_dtype(field_type)))
            else:
                spec.append((n, field_type))

        return np.dtype(spec)
    return


def dims_tuple_string(s):
    """
    Convert a string of dimensions 'DIM0 DIM1 ...' into a
    comma separated list 'DIM0, DIM1, ...' bearing in mind
    that Numpy wants (DIM0,) instead of (DIM0)
    """
    if not isinstance(s, str):
        raise TypeError('String expected.')
    dims = s.strip()
    a = dims.split(' ')
    rk = len(a)
    if rk == 0 or rk > 32:
        raise Exception('Invalid array rank found.')
    result = ''
    for i in range(0, rk):
        if int(a[i]) <= 0:
            raise Exception('Invalid array dimension found.')
        result = result + a[i]
        if i == 0:
            result = result + ','

    return result


def parse_dtype(s):
    """
    Given a string description, this function returns a corresponding
    Numpy dtype object.
    """
    if not isinstance(s, str):
        raise TypeError('String expected.')
    t = s
    if s.find(':') > 0:
        t = s[0:s.find(':')]
    alow = t.find('[')
    ahigh = t.find(']')
    dims = None
    if alow > 0:
        if ahigh < 0:
            raise Exception('Incomplete array type?')
        if alow > ahigh or alow == ahigh - 1:
            raise Exception('Invalid array dimensions.')
        dims = dims_tuple_string(t[alow + 1:ahigh])
    else:
        alow = len(t)
    btype = t[0:alow]
    if btype.upper() not in scalar_dtypes.keys():
        raise Exception('Unsupported scalar type found.')
    else:
        if dims is None:
            return scalar_dtypes[btype.upper()]
        else:
            return np.dtype('(%s)%s' % (dims, t[0:alow]))

    return


def dtype_to_hexad(dt):
    """
    Given a NumPy dtype object, this function returns a PyHexad string
    rendering.
    """
    if not isinstance(dt, np.dtype):
        raise TypeError('NumPy dtype expected.')
    if dt.kind in ('i', 'u', 'f', 'S'):
        if dt.kind != 'S':
            return dt.name
        else:
            if dt.isbuiltin == 1:
                return 'string'
            return 'string%d' % dt.itemsize

    else:
        if dt.subdtype is not None:
            return str(dt)
        else:
            if dt.fields is not None:
                ret = ''
                size = len(dt.fields)
                for i in range(size):
                    k = dt.names[i]
                    dp = k.replace(',', '\\,')
                    ret += '%s,%s' % (dp, dtype_to_hexad(dt.fields[k][0]))
                    if i < size - 1:
                        ret += ','

                return str(ret)
            return str(dt)

    return