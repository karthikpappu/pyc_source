# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/SetStateMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 6126 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
from pyatv.mrp.protobuf import NowPlayingInfo_pb2 as pyatv_dot_mrp_dot_protobuf_dot_NowPlayingInfo__pb2
from pyatv.mrp.protobuf import SupportedCommands_pb2 as pyatv_dot_mrp_dot_protobuf_dot_SupportedCommands__pb2
from pyatv.mrp.protobuf import PlayerPath_pb2 as pyatv_dot_mrp_dot_protobuf_dot_PlayerPath__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/SetStateMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n(pyatv/mrp/protobuf/SetStateMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto\x1a\'pyatv/mrp/protobuf/NowPlayingInfo.proto\x1a*pyatv/mrp/protobuf/SupportedCommands.proto\x1a#pyatv/mrp/protobuf/PlayerPath.proto"É\x01\n\x0fSetStateMessage\x12\'\n\x0enowPlayingInfo\x18\x01 \x01(\x0b2\x0f.NowPlayingInfo\x12-\n\x11supportedCommands\x18\x02 \x01(\x0b2\x12.SupportedCommands\x12\x11\n\tdisplayID\x18\x04 \x01(\t\x12\x13\n\x0bdisplayName\x18\x05 \x01(\t\x12\x15\n\rplaybackState\x18\x06 \x01(\r\x12\x1f\n\nplayerPath\x18\t \x01(\x0b2\x0b.PlayerPath:;\n\x0fsetStateMessage\x12\x10.ProtocolMessage\x18\t \x01(\x0b2\x10.SetStateMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_NowPlayingInfo__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_SupportedCommands__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_PlayerPath__pb2.DESCRIPTOR])
SETSTATEMESSAGE_FIELD_NUMBER = 9
setStateMessage = _descriptor.FieldDescriptor(name='setStateMessage',
  full_name='setStateMessage',
  index=0,
  number=9,
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
_SETSTATEMESSAGE = _descriptor.Descriptor(name='SetStateMessage',
  full_name='SetStateMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='nowPlayingInfo',
   full_name='SetStateMessage.nowPlayingInfo',
   index=0,
   number=1,
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='supportedCommands',
   full_name='SetStateMessage.supportedCommands',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='displayID',
   full_name='SetStateMessage.displayID',
   index=2,
   number=4,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='displayName',
   full_name='SetStateMessage.displayName',
   index=3,
   number=5,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='playbackState',
   full_name='SetStateMessage.playbackState',
   index=4,
   number=6,
   type=13,
   cpp_type=3,
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
 _descriptor.FieldDescriptor(name='playerPath',
   full_name='SetStateMessage.playerPath',
   index=5,
   number=9,
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
  serialized_start=209,
  serialized_end=410)
_SETSTATEMESSAGE.fields_by_name['nowPlayingInfo'].message_type = pyatv_dot_mrp_dot_protobuf_dot_NowPlayingInfo__pb2._NOWPLAYINGINFO
_SETSTATEMESSAGE.fields_by_name['supportedCommands'].message_type = pyatv_dot_mrp_dot_protobuf_dot_SupportedCommands__pb2._SUPPORTEDCOMMANDS
_SETSTATEMESSAGE.fields_by_name['playerPath'].message_type = pyatv_dot_mrp_dot_protobuf_dot_PlayerPath__pb2._PLAYERPATH
DESCRIPTOR.message_types_by_name['SetStateMessage'] = _SETSTATEMESSAGE
DESCRIPTOR.extensions_by_name['setStateMessage'] = setStateMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SetStateMessage = _reflection.GeneratedProtocolMessageType('SetStateMessage', (_message.Message,), {'DESCRIPTOR':_SETSTATEMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.SetStateMessage_pb2'})
_sym_db.RegisterMessage(SetStateMessage)
setStateMessage.message_type = _SETSTATEMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(setStateMessage)