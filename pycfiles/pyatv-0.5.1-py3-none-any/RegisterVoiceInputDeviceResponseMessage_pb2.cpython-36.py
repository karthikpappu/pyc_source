# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/RegisterVoiceInputDeviceResponseMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 4001 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/RegisterVoiceInputDeviceResponseMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n@pyatv/mrp/protobuf/RegisterVoiceInputDeviceResponseMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"N\n\'RegisterVoiceInputDeviceResponseMessage\x12\x10\n\x08deviceID\x18\x01 \x01(\x05\x12\x11\n\terrorCode\x18\x02 \x01(\x05:k\n\'registerVoiceInputDeviceResponseMessage\x12\x10.ProtocolMessage\x18" \x01(\x0b2(.RegisterVoiceInputDeviceResponseMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
REGISTERVOICEINPUTDEVICERESPONSEMESSAGE_FIELD_NUMBER = 34
registerVoiceInputDeviceResponseMessage = _descriptor.FieldDescriptor(name='registerVoiceInputDeviceResponseMessage',
  full_name='registerVoiceInputDeviceResponseMessage',
  index=0,
  number=34,
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
_REGISTERVOICEINPUTDEVICERESPONSEMESSAGE = _descriptor.Descriptor(name='RegisterVoiceInputDeviceResponseMessage',
  full_name='RegisterVoiceInputDeviceResponseMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='deviceID',
   full_name='RegisterVoiceInputDeviceResponseMessage.deviceID',
   index=0,
   number=1,
   type=5,
   cpp_type=1,
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
 _descriptor.FieldDescriptor(name='errorCode',
   full_name='RegisterVoiceInputDeviceResponseMessage.errorCode',
   index=1,
   number=2,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=False,
   default_value=0,
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
  serialized_start=110,
  serialized_end=188)
DESCRIPTOR.message_types_by_name['RegisterVoiceInputDeviceResponseMessage'] = _REGISTERVOICEINPUTDEVICERESPONSEMESSAGE
DESCRIPTOR.extensions_by_name['registerVoiceInputDeviceResponseMessage'] = registerVoiceInputDeviceResponseMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RegisterVoiceInputDeviceResponseMessage = _reflection.GeneratedProtocolMessageType('RegisterVoiceInputDeviceResponseMessage', (_message.Message,), {'DESCRIPTOR':_REGISTERVOICEINPUTDEVICERESPONSEMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.RegisterVoiceInputDeviceResponseMessage_pb2'})
_sym_db.RegisterMessage(RegisterVoiceInputDeviceResponseMessage)
registerVoiceInputDeviceResponseMessage.message_type = _REGISTERVOICEINPUTDEVICERESPONSEMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(registerVoiceInputDeviceResponseMessage)