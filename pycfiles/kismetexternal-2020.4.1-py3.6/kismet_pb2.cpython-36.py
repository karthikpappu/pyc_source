# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kismetexternal/kismet_pb2.py
# Compiled at: 2019-07-18 17:53:29
# Size of source mod 2**32: 9481 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='kismet.proto',
  package='KismetExternal',
  syntax='proto2',
  serialized_pb=(_b('\n\x0ckismet.proto\x12\x0eKismetExternal":\n\x07Command\x12\x0f\n\x07command\x18\x01 \x02(\t\x12\r\n\x05seqno\x18\x02 \x02(\r\x12\x0f\n\x07content\x18\x03 \x02(\x0c"¡\x01\n\rMsgbusMessage\x12:\n\x07msgtype\x18\x01 \x02(\x0e2).KismetExternal.MsgbusMessage.MessageType\x12\x0f\n\x07msgtext\x18\x02 \x02(\t"C\n\x0bMessageType\x12\t\n\x05DEBUG\x10\x01\x12\x08\n\x04INFO\x10\x02\x12\t\n\x05ERROR\x10\x04\x12\t\n\x05ALERT\x10\x08\x12\t\n\x05FATAL\x10\x10"\x06\n\x04Ping"\x1a\n\x04Pong\x12\x12\n\nping_seqno\x18\x01 \x02(\r""\n\x10ExternalShutdown\x12\x0e\n\x06reason\x18\x01 \x02(\t"#\n\x0eSystemRegister\x12\x11\n\tsubsystem\x18\x01 \x02(\t')))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_MSGBUSMESSAGE_MESSAGETYPE = _descriptor.EnumDescriptor(name='MessageType',
  full_name='KismetExternal.MsgbusMessage.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
 _descriptor.EnumValueDescriptor(name='DEBUG',
   index=0,
   number=1,
   options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='INFO',
   index=1,
   number=2,
   options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='ERROR',
   index=2,
   number=4,
   options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='ALERT',
   index=3,
   number=8,
   options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='FATAL',
   index=4,
   number=16,
   options=None,
   type=None)],
  containing_type=None,
  options=None,
  serialized_start=187,
  serialized_end=254)
_sym_db.RegisterEnumDescriptor(_MSGBUSMESSAGE_MESSAGETYPE)
_COMMAND = _descriptor.Descriptor(name='Command',
  full_name='KismetExternal.Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='command',
   full_name='KismetExternal.Command.command',
   index=0,
   number=1,
   type=9,
   cpp_type=9,
   label=2,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 _descriptor.FieldDescriptor(name='seqno',
   full_name='KismetExternal.Command.seqno',
   index=1,
   number=2,
   type=13,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 _descriptor.FieldDescriptor(name='content',
   full_name='KismetExternal.Command.content',
   index=2,
   number=3,
   type=12,
   cpp_type=9,
   label=2,
   has_default_value=False,
   default_value=(_b('')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=32,
  serialized_end=90)
_MSGBUSMESSAGE = _descriptor.Descriptor(name='MsgbusMessage',
  full_name='KismetExternal.MsgbusMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='msgtype',
   full_name='KismetExternal.MsgbusMessage.msgtype',
   index=0,
   number=1,
   type=14,
   cpp_type=8,
   label=2,
   has_default_value=False,
   default_value=1,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 _descriptor.FieldDescriptor(name='msgtext',
   full_name='KismetExternal.MsgbusMessage.msgtext',
   index=1,
   number=2,
   type=9,
   cpp_type=9,
   label=2,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[
 _MSGBUSMESSAGE_MESSAGETYPE],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=93,
  serialized_end=254)
_PING = _descriptor.Descriptor(name='Ping',
  full_name='KismetExternal.Ping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=256,
  serialized_end=262)
_PONG = _descriptor.Descriptor(name='Pong',
  full_name='KismetExternal.Pong',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='ping_seqno',
   full_name='KismetExternal.Pong.ping_seqno',
   index=0,
   number=1,
   type=13,
   cpp_type=3,
   label=2,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=264,
  serialized_end=290)
_EXTERNALSHUTDOWN = _descriptor.Descriptor(name='ExternalShutdown',
  full_name='KismetExternal.ExternalShutdown',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='reason',
   full_name='KismetExternal.ExternalShutdown.reason',
   index=0,
   number=1,
   type=9,
   cpp_type=9,
   label=2,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=292,
  serialized_end=326)
_SYSTEMREGISTER = _descriptor.Descriptor(name='SystemRegister',
  full_name='KismetExternal.SystemRegister',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='subsystem',
   full_name='KismetExternal.SystemRegister.subsystem',
   index=0,
   number=1,
   type=9,
   cpp_type=9,
   label=2,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=328,
  serialized_end=363)
_MSGBUSMESSAGE.fields_by_name['msgtype'].enum_type = _MSGBUSMESSAGE_MESSAGETYPE
_MSGBUSMESSAGE_MESSAGETYPE.containing_type = _MSGBUSMESSAGE
DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
DESCRIPTOR.message_types_by_name['MsgbusMessage'] = _MSGBUSMESSAGE
DESCRIPTOR.message_types_by_name['Ping'] = _PING
DESCRIPTOR.message_types_by_name['Pong'] = _PONG
DESCRIPTOR.message_types_by_name['ExternalShutdown'] = _EXTERNALSHUTDOWN
DESCRIPTOR.message_types_by_name['SystemRegister'] = _SYSTEMREGISTER
Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), dict(DESCRIPTOR=_COMMAND,
  __module__='kismet_pb2'))
_sym_db.RegisterMessage(Command)
MsgbusMessage = _reflection.GeneratedProtocolMessageType('MsgbusMessage', (_message.Message,), dict(DESCRIPTOR=_MSGBUSMESSAGE,
  __module__='kismet_pb2'))
_sym_db.RegisterMessage(MsgbusMessage)
Ping = _reflection.GeneratedProtocolMessageType('Ping', (_message.Message,), dict(DESCRIPTOR=_PING,
  __module__='kismet_pb2'))
_sym_db.RegisterMessage(Ping)
Pong = _reflection.GeneratedProtocolMessageType('Pong', (_message.Message,), dict(DESCRIPTOR=_PONG,
  __module__='kismet_pb2'))
_sym_db.RegisterMessage(Pong)
ExternalShutdown = _reflection.GeneratedProtocolMessageType('ExternalShutdown', (_message.Message,), dict(DESCRIPTOR=_EXTERNALSHUTDOWN,
  __module__='kismet_pb2'))
_sym_db.RegisterMessage(ExternalShutdown)
SystemRegister = _reflection.GeneratedProtocolMessageType('SystemRegister', (_message.Message,), dict(DESCRIPTOR=_SYSTEMREGISTER,
  __module__='kismet_pb2'))
_sym_db.RegisterMessage(SystemRegister)