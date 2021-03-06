# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/graph_rewriter_pb2.py
# Compiled at: 2020-04-05 20:34:16
# Size of source mod 2**32: 4866 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/graph_rewriter.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n,object_detection/protos/graph_rewriter.proto\x12\x17object_detection.protos"W\n\rGraphRewriter\x12;\n\x0cquantization\x18\x01 \x01(\x0b2%.object_detection.protos.Quantization*\t\x08è\x07\x10\x80\x80\x80\x80\x02"s\n\x0cQuantization\x12\x15\n\x05delay\x18\x01 \x01(\x05:\x06500000\x12\x16\n\x0bweight_bits\x18\x02 \x01(\x05:\x018\x12\x1a\n\x0factivation_bits\x18\x03 \x01(\x05:\x018\x12\x18\n\tsymmetric\x18\x04 \x01(\x08:\x05false')))
_GRAPHREWRITER = _descriptor.Descriptor(name='GraphRewriter',
  full_name='object_detection.protos.GraphRewriter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='quantization',
   full_name='object_detection.protos.GraphRewriter.quantization',
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
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[
 (1000, 536870912)],
  oneofs=[],
  serialized_start=73,
  serialized_end=160)
_QUANTIZATION = _descriptor.Descriptor(name='Quantization',
  full_name='object_detection.protos.Quantization',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='delay',
   full_name='object_detection.protos.Quantization.delay',
   index=0,
   number=1,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=True,
   default_value=500000,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='weight_bits',
   full_name='object_detection.protos.Quantization.weight_bits',
   index=1,
   number=2,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=True,
   default_value=8,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='activation_bits',
   full_name='object_detection.protos.Quantization.activation_bits',
   index=2,
   number=3,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=True,
   default_value=8,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='symmetric',
   full_name='object_detection.protos.Quantization.symmetric',
   index=3,
   number=4,
   type=8,
   cpp_type=7,
   label=1,
   has_default_value=True,
   default_value=False,
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
  serialized_start=162,
  serialized_end=277)
_GRAPHREWRITER.fields_by_name['quantization'].message_type = _QUANTIZATION
DESCRIPTOR.message_types_by_name['GraphRewriter'] = _GRAPHREWRITER
DESCRIPTOR.message_types_by_name['Quantization'] = _QUANTIZATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
GraphRewriter = _reflection.GeneratedProtocolMessageType('GraphRewriter', (_message.Message,), dict(DESCRIPTOR=_GRAPHREWRITER,
  __module__='object_detection.protos.graph_rewriter_pb2'))
_sym_db.RegisterMessage(GraphRewriter)
Quantization = _reflection.GeneratedProtocolMessageType('Quantization', (_message.Message,), dict(DESCRIPTOR=_QUANTIZATION,
  __module__='object_detection.protos.graph_rewriter_pb2'))
_sym_db.RegisterMessage(Quantization)