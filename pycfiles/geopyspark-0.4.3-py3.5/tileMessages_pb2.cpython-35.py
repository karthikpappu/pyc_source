# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotrellis/protobuf/tileMessages_pb2.py
# Compiled at: 2018-11-28 11:44:02
# Size of source mod 2**32: 10069 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='tileMessages.proto', package='protos', syntax='proto3', serialized_pb=_b('\n\x12tileMessages.proto\x12\x06protos"Á\x01\n\rProtoCellType\x120\n\x08dataType\x18\x01 \x01(\x0e2\x1e.protos.ProtoCellType.DataType\x12\n\n\x02nd\x18\x02 \x01(\x01\x12\x11\n\thasNoData\x18\x03 \x01(\x08"_\n\x08DataType\x12\x07\n\x03BIT\x10\x00\x12\x08\n\x04BYTE\x10\x01\x12\t\n\x05UBYTE\x10\x02\x12\t\n\x05SHORT\x10\x03\x12\n\n\x06USHORT\x10\x04\x12\x07\n\x03INT\x10\x05\x12\t\n\x05FLOAT\x10\x06\x12\n\n\x06DOUBLE\x10\x07"³\x01\n\tProtoTile\x12\x0c\n\x04cols\x18\x01 \x01(\x05\x12\x0c\n\x04rows\x18\x02 \x01(\x05\x12\'\n\x08cellType\x18\x03 \x01(\x0b2\x15.protos.ProtoCellType\x12\x17\n\x0bsint32Cells\x18\x04 \x03(\x11B\x02\x10\x01\x12\x17\n\x0buint32Cells\x18\x05 \x03(\rB\x02\x10\x01\x12\x16\n\nfloatCells\x18\x06 \x03(\x02B\x02\x10\x01\x12\x17\n\x0bdoubleCells\x18\x07 \x03(\x01B\x02\x10\x01"6\n\x12ProtoMultibandTile\x12 \n\x05tiles\x18\x01 \x03(\x0b2\x11.protos.ProtoTileb\x06proto3'))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_PROTOCELLTYPE_DATATYPE = _descriptor.EnumDescriptor(name='DataType', full_name='protos.ProtoCellType.DataType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='BIT', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='BYTE', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='UBYTE', index=2, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SHORT', index=3, number=3, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='USHORT', index=4, number=4, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INT', index=5, number=5, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='FLOAT', index=6, number=6, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='DOUBLE', index=7, number=7, options=None, type=None)], containing_type=None, options=None, serialized_start=129, serialized_end=224)
_sym_db.RegisterEnumDescriptor(_PROTOCELLTYPE_DATATYPE)
_PROTOCELLTYPE = _descriptor.Descriptor(name='ProtoCellType', full_name='protos.ProtoCellType', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='dataType', full_name='protos.ProtoCellType.dataType', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='nd', full_name='protos.ProtoCellType.nd', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='hasNoData', full_name='protos.ProtoCellType.hasNoData', index=2, number=3, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _PROTOCELLTYPE_DATATYPE], options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=31, serialized_end=224)
_PROTOTILE = _descriptor.Descriptor(name='ProtoTile', full_name='protos.ProtoTile', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='cols', full_name='protos.ProtoTile.cols', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='rows', full_name='protos.ProtoTile.rows', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='cellType', full_name='protos.ProtoTile.cellType', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sint32Cells', full_name='protos.ProtoTile.sint32Cells', index=3, number=4, type=17, cpp_type=1, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))),
 _descriptor.FieldDescriptor(name='uint32Cells', full_name='protos.ProtoTile.uint32Cells', index=4, number=5, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))),
 _descriptor.FieldDescriptor(name='floatCells', full_name='protos.ProtoTile.floatCells', index=5, number=6, type=2, cpp_type=6, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))),
 _descriptor.FieldDescriptor(name='doubleCells', full_name='protos.ProtoTile.doubleCells', index=6, number=7, type=1, cpp_type=5, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')))], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=227, serialized_end=406)
_PROTOMULTIBANDTILE = _descriptor.Descriptor(name='ProtoMultibandTile', full_name='protos.ProtoMultibandTile', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='tiles', full_name='protos.ProtoMultibandTile.tiles', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=408, serialized_end=462)
_PROTOCELLTYPE.fields_by_name['dataType'].enum_type = _PROTOCELLTYPE_DATATYPE
_PROTOCELLTYPE_DATATYPE.containing_type = _PROTOCELLTYPE
_PROTOTILE.fields_by_name['cellType'].message_type = _PROTOCELLTYPE
_PROTOMULTIBANDTILE.fields_by_name['tiles'].message_type = _PROTOTILE
DESCRIPTOR.message_types_by_name['ProtoCellType'] = _PROTOCELLTYPE
DESCRIPTOR.message_types_by_name['ProtoTile'] = _PROTOTILE
DESCRIPTOR.message_types_by_name['ProtoMultibandTile'] = _PROTOMULTIBANDTILE
ProtoCellType = _reflection.GeneratedProtocolMessageType('ProtoCellType', (_message.Message,), dict(DESCRIPTOR=_PROTOCELLTYPE, __module__='tileMessages_pb2'))
_sym_db.RegisterMessage(ProtoCellType)
ProtoTile = _reflection.GeneratedProtocolMessageType('ProtoTile', (_message.Message,), dict(DESCRIPTOR=_PROTOTILE, __module__='tileMessages_pb2'))
_sym_db.RegisterMessage(ProtoTile)
ProtoMultibandTile = _reflection.GeneratedProtocolMessageType('ProtoMultibandTile', (_message.Message,), dict(DESCRIPTOR=_PROTOMULTIBANDTILE, __module__='tileMessages_pb2'))
_sym_db.RegisterMessage(ProtoMultibandTile)
_PROTOTILE.fields_by_name['sint32Cells'].has_options = True
_PROTOTILE.fields_by_name['sint32Cells']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_PROTOTILE.fields_by_name['uint32Cells'].has_options = True
_PROTOTILE.fields_by_name['uint32Cells']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_PROTOTILE.fields_by_name['floatCells'].has_options = True
_PROTOTILE.fields_by_name['floatCells']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_PROTOTILE.fields_by_name['doubleCells'].has_options = True
_PROTOTILE.fields_by_name['doubleCells']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))