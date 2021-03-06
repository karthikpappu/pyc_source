# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/tiostream.py
# Compiled at: 2020-05-12 05:18:07
# Size of source mod 2**32: 3218 bytes
__doc__ = '\ntiostream - I/O functions\n\nCopyright (C) 2010, 2011, 2012, 2013 Arthur de Jong\n\nThis library is free software; you can redistribute it and/or\nmodify it under the terms of the GNU Lesser General Public\nLicense as published by the Free Software Foundation; either\nversion 2.1 of the License, or (at your option) any later version.\n\nThis library is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\nLesser General Public License for more details.\n\nYou should have received a copy of the GNU Lesser General Public\nLicense along with this library; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA\n02110-1301 USA\n'
import socket, struct
STRUCT_INT32 = struct.Struct('!i')
STRUCT_TIMEVAL = struct.Struct('ll')

class TIOStream:
    """TIOStream"""
    __slots__ = ('fp', )

    def __init__(self, fp):
        self.fp = fp

    def read(self, size):
        return self.fp.read(size)

    def read_int32(self):
        return STRUCT_INT32.unpack(self.read(STRUCT_INT32.size))[0]

    def read_bytes(self, maxsize=None):
        num = self.read_int32()
        if maxsize is not None:
            if num >= maxsize:
                raise ValueError('num = %d exceeded maxsize = %d' % (num, maxsize))
        return self.read(num)

    def read_string(self):
        return self.read_bytes().decode('utf-8')

    def read_address(self):
        """Read an address (usually IPv4 or IPv6) from the stream.

        This returns the address as a string representation.
        """
        af = self.read_int32()
        return socket.inet_ntop(af, self.read_bytes(maxsize=64))

    def write(self, value):
        self.fp.write(value)

    def write_int32(self, value):
        self.write(STRUCT_INT32.pack(value))

    def write_bytes(self, value):
        self.write_int32(len(value))
        if value:
            self.write(value)

    def write_string(self, value):
        self.write_bytes(value.encode('utf-8'))

    def write_stringlist(self, value):
        lst = tuple(value)
        self.write_int32(len(lst))
        for string in lst:
            self.write_string(string)

    @staticmethod
    def _to_address--- This code section failed: ---

 L.  92         0  SETUP_FINALLY        24  'to 24'

 L.  93         2  LOAD_GLOBAL              socket
                4  LOAD_ATTR                AF_INET
                6  LOAD_GLOBAL              socket
                8  LOAD_METHOD              inet_pton
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                AF_INET
               14  LOAD_FAST                'value'
               16  CALL_METHOD_2         2  ''
               18  BUILD_TUPLE_2         2 
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.  94        24  DUP_TOP          
               26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                error
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  95        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L.  97        46  LOAD_GLOBAL              socket
               48  LOAD_ATTR                AF_INET6
               50  LOAD_GLOBAL              socket
               52  LOAD_METHOD              inet_pton
               54  LOAD_GLOBAL              socket
               56  LOAD_ATTR                AF_INET6
               58  LOAD_FAST                'value'
               60  CALL_METHOD_2         2  ''
               62  BUILD_TUPLE_2         2 
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 24

    def write_address(self, value):
        """Write an address (usually IPv4 or IPv6) to the stream."""
        af, address = TIOStream._to_address(value)
        self.write_int32(af)
        self.write_bytes(address)

    def close(self):
        try:
            self.fp.close()
        except IOError:
            pass

    def __del__(self):
        self.close()