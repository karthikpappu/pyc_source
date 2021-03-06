# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: gen-py/shared/SharedService.py
# Compiled at: 2009-08-22 04:17:15
from thrift.Thrift import *
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

class Iface:

    def getStruct(self, key):
        """
    Parameters:
     - key
    """
        pass


class Client(Iface):

    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot != None:
            self._oprot = oprot
        self._seqid = 0
        return

    def getStruct(self, key):
        """
    Parameters:
     - key
    """
        self.send_getStruct(key)
        return self.recv_getStruct()

    def send_getStruct(self, key):
        self._oprot.writeMessageBegin('getStruct', TMessageType.CALL, self._seqid)
        args = getStruct_args()
        args.key = key
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_getStruct(self):
        (fname, mtype, rseqid) = self._iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.readMessageEnd()
            raise x
        result = getStruct_result()
        result.read(self._iprot)
        self._iprot.readMessageEnd()
        if result.success != None:
            return result.success
        else:
            raise TApplicationException(TApplicationException.MISSING_RESULT, 'getStruct failed: unknown result')
            return


class Processor(Iface, TProcessor):

    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap['getStruct'] = Processor.process_getStruct

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % name)
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_getStruct(self, seqid, iprot, oprot):
        args = getStruct_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getStruct_result()
        result.success = self._handler.getStruct(args.key)
        oprot.writeMessageBegin('getStruct', TMessageType.REPLY, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


class getStruct_args(object):
    """
  Attributes:
   - key
  """
    thrift_spec = (
     None,
     (
      1, TType.I32, 'key', None, None))

    def __init__(self, key=None):
        self.key = key

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                (fname, ftype, fid) = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.I32:
                        self.key = iprot.readI32()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('getStruct_args')
            if self.key != None:
                oprot.writeFieldBegin('key', TType.I32, 1)
                oprot.writeI32(self.key)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for (key, value) in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class getStruct_result(object):
    """
  Attributes:
   - success
  """
    thrift_spec = (
     (
      0, TType.STRUCT, 'success', (SharedStruct, SharedStruct.thrift_spec), None),)

    def __init__(self, success=None):
        self.success = success

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                (fname, ftype, fid) = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 0:
                    if ftype == TType.STRUCT:
                        self.success = SharedStruct()
                        self.success.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('getStruct_result')
            if self.success != None:
                oprot.writeFieldBegin('success', TType.STRUCT, 0)
                self.success.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for (key, value) in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other