# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yg/Desktop/uisee/release/swdclient/server_pb2.py
# Compiled at: 2019-10-23 01:55:49
# Size of source mod 2**32: 38008 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='server.proto', package='server', syntax='proto3', serialized_options=None, serialized_pb=_b('\n\x0cserver.proto\x12\x06server"+\n\x08Vector3D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02"6\n\nRotation3D\x12\x0b\n\x03yaw\x18\x01 \x01(\x02\x12\r\n\x05pitch\x18\x02 \x01(\x02\x12\x0c\n\x04roll\x18\x03 \x01(\x02"U\n\tTransform\x12"\n\x08location\x18\x01 \x01(\x0b2\x10.server.Vector3D\x12$\n\x08rotation\x18\x02 \x01(\x0b2\x12.server.Rotation3D"\x9b\x01\n\x0cMotionstatus\x12"\n\x08velocity\x18\x01 \x01(\x0b2\x10.server.Vector3D\x12$\n\naccelerity\x18\x02 \x01(\x0b2\x10.server.Vector3D\x12\x15\n\rforward_speed\x18\x03 \x01(\x02\x12*\n\x10angular_velocity\x18\x04 \x01(\x0b2\x10.server.Vector3D"S\n\x0bBoundingBox\x12"\n\x08location\x18\x01 \x01(\x0b2\x10.server.Vector3D\x12 \n\x06extent\x18\x02 \x01(\x0b2\x10.server.Vector3D"\x98\x01\n\nPedestrian\x12)\n\x0cbounding_box\x18\x01 \x01(\x0b2\x13.server.BoundingBox\x12\x15\n\rforward_speed\x18\x02 \x01(\x02\x12"\n\x08velocity\x18\x03 \x01(\x0b2\x10.server.Vector3D\x12$\n\naccelerity\x18\x04 \x01(\x0b2\x10.server.Vector3D"\x95\x01\n\x07Vehicle\x12)\n\x0cbounding_box\x18\x01 \x01(\x0b2\x13.server.BoundingBox\x12\x15\n\rforward_speed\x18\x02 \x01(\x02\x12"\n\x08velocity\x18\x03 \x01(\x0b2\x10.server.Vector3D\x12$\n\naccelerity\x18\x04 \x01(\x0b2\x10.server.Vector3D"®\x01\n\x0cTrafficLight\x12)\n\x05state\x18\x01 \x01(\x0e2\x1a.server.TrafficLight.State\x12\x12\n\nlight_time\x18\x02 \x01(\x07\x12)\n\x0cbounding_box\x18\x03 \x01(\x0b2\x13.server.BoundingBox"4\n\x05State\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03RED\x10\x01\x12\n\n\x06YELLOW\x10\x02\x12\t\n\x05GREEN\x10\x03"P\n\x0eSpeedLimitSign\x12\x13\n\x0blimit_speed\x18\x01 \x01(\x02\x12)\n\x0cbounding_box\x18\x02 \x01(\x0b2\x13.server.BoundingBox"õ\x01\n\x06Object\x12\n\n\x02id\x18\x01 \x01(\x07\x12$\n\ttransform\x18\x02 \x01(\x0b2\x11.server.Transform\x12(\n\npedestrian\x18\x04 \x01(\x0b2\x12.server.PedestrianH\x00\x12"\n\x07vehicle\x18\x03 \x01(\x0b2\x0f.server.VehicleH\x00\x12-\n\rtraffic_light\x18\x05 \x01(\x0b2\x14.server.TrafficLightH\x00\x122\n\x10speed_limit_sign\x18\x06 \x01(\x0b2\x16.server.SpeedLimitSignH\x00B\x08\n\x06object"¼\x01\n\x07Control\x12\x10\n\x08throttle\x18\x01 \x01(\x02\x12\r\n\x05steer\x18\x02 \x01(\x02\x12\r\n\x05brake\x18\x03 \x01(\x02\x12\x12\n\nhand_brake\x18\x04 \x01(\x08\x12\x0f\n\x07reverse\x18\x05 \x01(\x08\x12\r\n\x05speed\x18\x06 \x01(\x02\x12"\n\x04type\x18\x07 \x01(\x0e2\x14.server.Control.Type")\n\x04Type\x12\x11\n\rTYPE_THROTTLE\x10\x00\x12\x0e\n\nTYPE_SPEED\x10\x01"^\n\x04Task\x12\n\n\x02id\x18\x01 \x01(\x07\x12%\n\x0bstart_point\x18\x02 \x01(\x0b2\x10.server.Vector3D\x12#\n\tend_point\x18\x03 \x01(\x0b2\x10.server.Vector3D"[\n\nRun_Status\x12\'\n\x05state\x18\x01 \x01(\x0e2\x18.server.Run_Status.State"$\n\x05State\x12\x07\n\x03RUN\x10\x00\x12\x08\n\x04STOP\x10\x01\x12\x08\n\x04MOVE\x10\x02"¦\x02\n\x0cMeasurements\x12\x12\n\ntime_stamp\x18\x03 \x01(\x06\x12&\n\nrun_status\x18\x06 \x01(\x0b2\x12.server.Run_Status\x12$\n\ttransform\x18\x01 \x01(\x0b2\x11.server.Transform\x12*\n\x0cmotionstatus\x18\x02 \x01(\x0b2\x14.server.Motionstatus\x12)\n\x0cbounding_box\x18\x0c \x01(\x0b2\x13.server.BoundingBox\x12 \n\x07control\x18\n \x01(\x0b2\x0f.server.Control\x12\x1f\n\x07objects\x18\x04 \x03(\x0b2\x0e.server.Object\x12\x1a\n\x04task\x18\x05 \x01(\x0b2\x0c.server.Taskb\x06proto3'))
_TRAFFICLIGHT_STATE = _descriptor.EnumDescriptor(name='State', full_name='server.TrafficLight.State', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='UNKNOWN', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='RED', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='YELLOW', index=2, number=2, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='GREEN', index=3, number=3, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=885, serialized_end=937)
_sym_db.RegisterEnumDescriptor(_TRAFFICLIGHT_STATE)
_CONTROL_TYPE = _descriptor.EnumDescriptor(name='Type', full_name='server.Control.Type', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='TYPE_THROTTLE', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='TYPE_SPEED', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=1417, serialized_end=1458)
_sym_db.RegisterEnumDescriptor(_CONTROL_TYPE)
_RUN_STATUS_STATE = _descriptor.EnumDescriptor(name='State', full_name='server.Run_Status.State', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='RUN', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='STOP', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MOVE', index=2, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=1611, serialized_end=1647)
_sym_db.RegisterEnumDescriptor(_RUN_STATUS_STATE)
_VECTOR3D = _descriptor.Descriptor(name='Vector3D', full_name='server.Vector3D', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='x', full_name='server.Vector3D.x', index=0, number=1, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='y', full_name='server.Vector3D.y', index=1, number=2, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='z', full_name='server.Vector3D.z', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=24, serialized_end=67)
_ROTATION3D = _descriptor.Descriptor(name='Rotation3D', full_name='server.Rotation3D', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='yaw', full_name='server.Rotation3D.yaw', index=0, number=1, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pitch', full_name='server.Rotation3D.pitch', index=1, number=2, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='roll', full_name='server.Rotation3D.roll', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=69, serialized_end=123)
_TRANSFORM = _descriptor.Descriptor(name='Transform', full_name='server.Transform', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='location', full_name='server.Transform.location', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='rotation', full_name='server.Transform.rotation', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=125, serialized_end=210)
_MOTIONSTATUS = _descriptor.Descriptor(name='Motionstatus', full_name='server.Motionstatus', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='velocity', full_name='server.Motionstatus.velocity', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='accelerity', full_name='server.Motionstatus.accelerity', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='forward_speed', full_name='server.Motionstatus.forward_speed', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='angular_velocity', full_name='server.Motionstatus.angular_velocity', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=213, serialized_end=368)
_BOUNDINGBOX = _descriptor.Descriptor(name='BoundingBox', full_name='server.BoundingBox', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='location', full_name='server.BoundingBox.location', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='extent', full_name='server.BoundingBox.extent', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=370, serialized_end=453)
_PEDESTRIAN = _descriptor.Descriptor(name='Pedestrian', full_name='server.Pedestrian', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='bounding_box', full_name='server.Pedestrian.bounding_box', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='forward_speed', full_name='server.Pedestrian.forward_speed', index=1, number=2, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='velocity', full_name='server.Pedestrian.velocity', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='accelerity', full_name='server.Pedestrian.accelerity', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=456, serialized_end=608)
_VEHICLE = _descriptor.Descriptor(name='Vehicle', full_name='server.Vehicle', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='bounding_box', full_name='server.Vehicle.bounding_box', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='forward_speed', full_name='server.Vehicle.forward_speed', index=1, number=2, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='velocity', full_name='server.Vehicle.velocity', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='accelerity', full_name='server.Vehicle.accelerity', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=611, serialized_end=760)
_TRAFFICLIGHT = _descriptor.Descriptor(name='TrafficLight', full_name='server.TrafficLight', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='state', full_name='server.TrafficLight.state', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='light_time', full_name='server.TrafficLight.light_time', index=1, number=2, type=7, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bounding_box', full_name='server.TrafficLight.bounding_box', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[
 _TRAFFICLIGHT_STATE], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=763, serialized_end=937)
_SPEEDLIMITSIGN = _descriptor.Descriptor(name='SpeedLimitSign', full_name='server.SpeedLimitSign', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='limit_speed', full_name='server.SpeedLimitSign.limit_speed', index=0, number=1, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bounding_box', full_name='server.SpeedLimitSign.bounding_box', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=939, serialized_end=1019)
_OBJECT = _descriptor.Descriptor(name='Object', full_name='server.Object', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='server.Object.id', index=0, number=1, type=7, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='transform', full_name='server.Object.transform', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pedestrian', full_name='server.Object.pedestrian', index=2, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='vehicle', full_name='server.Object.vehicle', index=3, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='traffic_light', full_name='server.Object.traffic_light', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='speed_limit_sign', full_name='server.Object.speed_limit_sign', index=5, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='object', full_name='server.Object.object', index=0, containing_type=None, fields=[])], serialized_start=1022, serialized_end=1267)
_CONTROL = _descriptor.Descriptor(name='Control', full_name='server.Control', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='throttle', full_name='server.Control.throttle', index=0, number=1, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='steer', full_name='server.Control.steer', index=1, number=2, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='brake', full_name='server.Control.brake', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='hand_brake', full_name='server.Control.hand_brake', index=3, number=4, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='reverse', full_name='server.Control.reverse', index=4, number=5, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='speed', full_name='server.Control.speed', index=5, number=6, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='type', full_name='server.Control.type', index=6, number=7, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[
 _CONTROL_TYPE], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1270, serialized_end=1458)
_TASK = _descriptor.Descriptor(name='Task', full_name='server.Task', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='server.Task.id', index=0, number=1, type=7, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='start_point', full_name='server.Task.start_point', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='end_point', full_name='server.Task.end_point', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1460, serialized_end=1554)
_RUN_STATUS = _descriptor.Descriptor(name='Run_Status', full_name='server.Run_Status', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='state', full_name='server.Run_Status.state', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[
 _RUN_STATUS_STATE], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1556, serialized_end=1647)
_MEASUREMENTS = _descriptor.Descriptor(name='Measurements', full_name='server.Measurements', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='time_stamp', full_name='server.Measurements.time_stamp', index=0, number=3, type=6, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='run_status', full_name='server.Measurements.run_status', index=1, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='transform', full_name='server.Measurements.transform', index=2, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='motionstatus', full_name='server.Measurements.motionstatus', index=3, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bounding_box', full_name='server.Measurements.bounding_box', index=4, number=12, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='control', full_name='server.Measurements.control', index=5, number=10, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='objects', full_name='server.Measurements.objects', index=6, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='task', full_name='server.Measurements.task', index=7, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1650, serialized_end=1944)
_TRANSFORM.fields_by_name['location'].message_type = _VECTOR3D
_TRANSFORM.fields_by_name['rotation'].message_type = _ROTATION3D
_MOTIONSTATUS.fields_by_name['velocity'].message_type = _VECTOR3D
_MOTIONSTATUS.fields_by_name['accelerity'].message_type = _VECTOR3D
_MOTIONSTATUS.fields_by_name['angular_velocity'].message_type = _VECTOR3D
_BOUNDINGBOX.fields_by_name['location'].message_type = _VECTOR3D
_BOUNDINGBOX.fields_by_name['extent'].message_type = _VECTOR3D
_PEDESTRIAN.fields_by_name['bounding_box'].message_type = _BOUNDINGBOX
_PEDESTRIAN.fields_by_name['velocity'].message_type = _VECTOR3D
_PEDESTRIAN.fields_by_name['accelerity'].message_type = _VECTOR3D
_VEHICLE.fields_by_name['bounding_box'].message_type = _BOUNDINGBOX
_VEHICLE.fields_by_name['velocity'].message_type = _VECTOR3D
_VEHICLE.fields_by_name['accelerity'].message_type = _VECTOR3D
_TRAFFICLIGHT.fields_by_name['state'].enum_type = _TRAFFICLIGHT_STATE
_TRAFFICLIGHT.fields_by_name['bounding_box'].message_type = _BOUNDINGBOX
_TRAFFICLIGHT_STATE.containing_type = _TRAFFICLIGHT
_SPEEDLIMITSIGN.fields_by_name['bounding_box'].message_type = _BOUNDINGBOX
_OBJECT.fields_by_name['transform'].message_type = _TRANSFORM
_OBJECT.fields_by_name['pedestrian'].message_type = _PEDESTRIAN
_OBJECT.fields_by_name['vehicle'].message_type = _VEHICLE
_OBJECT.fields_by_name['traffic_light'].message_type = _TRAFFICLIGHT
_OBJECT.fields_by_name['speed_limit_sign'].message_type = _SPEEDLIMITSIGN
_OBJECT.oneofs_by_name['object'].fields.append(_OBJECT.fields_by_name['pedestrian'])
_OBJECT.fields_by_name['pedestrian'].containing_oneof = _OBJECT.oneofs_by_name['object']
_OBJECT.oneofs_by_name['object'].fields.append(_OBJECT.fields_by_name['vehicle'])
_OBJECT.fields_by_name['vehicle'].containing_oneof = _OBJECT.oneofs_by_name['object']
_OBJECT.oneofs_by_name['object'].fields.append(_OBJECT.fields_by_name['traffic_light'])
_OBJECT.fields_by_name['traffic_light'].containing_oneof = _OBJECT.oneofs_by_name['object']
_OBJECT.oneofs_by_name['object'].fields.append(_OBJECT.fields_by_name['speed_limit_sign'])
_OBJECT.fields_by_name['speed_limit_sign'].containing_oneof = _OBJECT.oneofs_by_name['object']
_CONTROL.fields_by_name['type'].enum_type = _CONTROL_TYPE
_CONTROL_TYPE.containing_type = _CONTROL
_TASK.fields_by_name['start_point'].message_type = _VECTOR3D
_TASK.fields_by_name['end_point'].message_type = _VECTOR3D
_RUN_STATUS.fields_by_name['state'].enum_type = _RUN_STATUS_STATE
_RUN_STATUS_STATE.containing_type = _RUN_STATUS
_MEASUREMENTS.fields_by_name['run_status'].message_type = _RUN_STATUS
_MEASUREMENTS.fields_by_name['transform'].message_type = _TRANSFORM
_MEASUREMENTS.fields_by_name['motionstatus'].message_type = _MOTIONSTATUS
_MEASUREMENTS.fields_by_name['bounding_box'].message_type = _BOUNDINGBOX
_MEASUREMENTS.fields_by_name['control'].message_type = _CONTROL
_MEASUREMENTS.fields_by_name['objects'].message_type = _OBJECT
_MEASUREMENTS.fields_by_name['task'].message_type = _TASK
DESCRIPTOR.message_types_by_name['Vector3D'] = _VECTOR3D
DESCRIPTOR.message_types_by_name['Rotation3D'] = _ROTATION3D
DESCRIPTOR.message_types_by_name['Transform'] = _TRANSFORM
DESCRIPTOR.message_types_by_name['Motionstatus'] = _MOTIONSTATUS
DESCRIPTOR.message_types_by_name['BoundingBox'] = _BOUNDINGBOX
DESCRIPTOR.message_types_by_name['Pedestrian'] = _PEDESTRIAN
DESCRIPTOR.message_types_by_name['Vehicle'] = _VEHICLE
DESCRIPTOR.message_types_by_name['TrafficLight'] = _TRAFFICLIGHT
DESCRIPTOR.message_types_by_name['SpeedLimitSign'] = _SPEEDLIMITSIGN
DESCRIPTOR.message_types_by_name['Object'] = _OBJECT
DESCRIPTOR.message_types_by_name['Control'] = _CONTROL
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['Run_Status'] = _RUN_STATUS
DESCRIPTOR.message_types_by_name['Measurements'] = _MEASUREMENTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Vector3D = _reflection.GeneratedProtocolMessageType('Vector3D', (_message.Message,), {'DESCRIPTOR': _VECTOR3D, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Vector3D)
Rotation3D = _reflection.GeneratedProtocolMessageType('Rotation3D', (_message.Message,), {'DESCRIPTOR': _ROTATION3D, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Rotation3D)
Transform = _reflection.GeneratedProtocolMessageType('Transform', (_message.Message,), {'DESCRIPTOR': _TRANSFORM, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Transform)
Motionstatus = _reflection.GeneratedProtocolMessageType('Motionstatus', (_message.Message,), {'DESCRIPTOR': _MOTIONSTATUS, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Motionstatus)
BoundingBox = _reflection.GeneratedProtocolMessageType('BoundingBox', (_message.Message,), {'DESCRIPTOR': _BOUNDINGBOX, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(BoundingBox)
Pedestrian = _reflection.GeneratedProtocolMessageType('Pedestrian', (_message.Message,), {'DESCRIPTOR': _PEDESTRIAN, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Pedestrian)
Vehicle = _reflection.GeneratedProtocolMessageType('Vehicle', (_message.Message,), {'DESCRIPTOR': _VEHICLE, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Vehicle)
TrafficLight = _reflection.GeneratedProtocolMessageType('TrafficLight', (_message.Message,), {'DESCRIPTOR': _TRAFFICLIGHT, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(TrafficLight)
SpeedLimitSign = _reflection.GeneratedProtocolMessageType('SpeedLimitSign', (_message.Message,), {'DESCRIPTOR': _SPEEDLIMITSIGN, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(SpeedLimitSign)
Object = _reflection.GeneratedProtocolMessageType('Object', (_message.Message,), {'DESCRIPTOR': _OBJECT, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Object)
Control = _reflection.GeneratedProtocolMessageType('Control', (_message.Message,), {'DESCRIPTOR': _CONTROL, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Control)
Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {'DESCRIPTOR': _TASK, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Task)
Run_Status = _reflection.GeneratedProtocolMessageType('Run_Status', (_message.Message,), {'DESCRIPTOR': _RUN_STATUS, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Run_Status)
Measurements = _reflection.GeneratedProtocolMessageType('Measurements', (_message.Message,), {'DESCRIPTOR': _MEASUREMENTS, 
 '__module__': 'server_pb2'})
_sym_db.RegisterMessage(Measurements)