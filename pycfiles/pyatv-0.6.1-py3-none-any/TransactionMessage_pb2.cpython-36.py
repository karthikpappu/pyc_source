# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/TransactionMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 3788 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import TransactionPackets_pb2 as pyatv_dot_mrp_dot_protobuf_dot_TransactionPackets__pb2
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/TransactionMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n+pyatv/mrp/protobuf/TransactionMessage.proto\x1a+pyatv/mrp/protobuf/TransactionPackets.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"H\n\x12TransactionMessage\x12\x0c\n\x04name\x18\x01 \x01(\x04\x12$\n\x07packets\x18\x02 \x01(\x0b2\x13.TransactionPackets:A\n\x12transactionMessage\x12\x10.ProtocolMessage\x18& \x01(\x0b2\x13.TransactionMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_TransactionPackets__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
TRANSACTIONMESSAGE_FIELD_NUMBER = 38
transactionMessage = _descriptor.FieldDescriptor(name='transactionMessage',
  full_name='transactionMessage',
  index=0,
  number=38,
  type=11,
  cpp_type=10,
  label=1,
  has_default_value=False,
  default_value=None,
  message_type=None,
  enum_type=None,
  containing_type=None,
  is_extension=True,
  extension_scope=None,
  serialized_options=None,
  file=DESCRIPTOR)
_TRANSACTIONMESSAGE = _descriptor.Descriptor(name='TransactionMessage',
  full_name='TransactionMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='name',
   full_name='TransactionMessage.name',
   index=0,
   number=1,
   type=4,
   cpp_type=4,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='packets',
   full_name='TransactionMessage.packets',
   index=1,
   number=2,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=134,
  serialized_end=206)
_TRANSACTIONMESSAGE.fields_by_name['packets'].message_type = pyatv_dot_mrp_dot_protobuf_dot_TransactionPackets__pb2._TRANSACTIONPACKETS
DESCRIPTOR.message_types_by_name['TransactionMessage'] = _TRANSACTIONMESSAGE
DESCRIPTOR.extensions_by_name['transactionMessage'] = transactionMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TransactionMessage = _reflection.GeneratedProtocolMessageType('TransactionMessage', (_message.Message,), {'DESCRIPTOR':_TRANSACTIONMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.TransactionMessage_pb2'})
_sym_db.RegisterMessage(TransactionMessage)
transactionMessage.message_type = _TRANSACTIONMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(transactionMessage)