# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/TextEditingAttributesMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 3402 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import TextInputTraitsMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_TextInputTraitsMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/TextEditingAttributesMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n5pyatv/mrp/protobuf/TextEditingAttributesMessage.proto\x1a/pyatv/mrp/protobuf/TextInputTraitsMessage.proto"]\n\x15TextEditingAttributes\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0e\n\x06prompt\x18\x02 \x01(\t\x12%\n\x0binputTraits\x18\x03 \x01(\x0b2\x10.TextInputTraits')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_TextInputTraitsMessage__pb2.DESCRIPTOR])
_TEXTEDITINGATTRIBUTES = _descriptor.Descriptor(name='TextEditingAttributes',
  full_name='TextEditingAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='title',
   full_name='TextEditingAttributes.title',
   index=0,
   number=1,
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
 _descriptor.FieldDescriptor(name='prompt',
   full_name='TextEditingAttributes.prompt',
   index=1,
   number=2,
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
 _descriptor.FieldDescriptor(name='inputTraits',
   full_name='TextEditingAttributes.inputTraits',
   index=2,
   number=3,
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
  serialized_start=106,
  serialized_end=199)
_TEXTEDITINGATTRIBUTES.fields_by_name['inputTraits'].message_type = pyatv_dot_mrp_dot_protobuf_dot_TextInputTraitsMessage__pb2._TEXTINPUTTRAITS
DESCRIPTOR.message_types_by_name['TextEditingAttributes'] = _TEXTEDITINGATTRIBUTES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TextEditingAttributes = _reflection.GeneratedProtocolMessageType('TextEditingAttributes', (_message.Message,), {'DESCRIPTOR':_TEXTEDITINGATTRIBUTES, 
 '__module__':'pyatv.mrp.protobuf.TextEditingAttributesMessage_pb2'})
_sym_db.RegisterMessage(TextEditingAttributes)