# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pypomelo/message.py
# Compiled at: 2019-01-03 22:45:50
__doc__ = 'Message encode or decode body of pomelo protocol package\n\nPomelo protocol package :\n\n+++++++++++++++++++++++++++++++++++++++\n+ type +    length    +      body     +\n+++++++++++++++++++++++++++++++++++++++\n 1 bytes    3 bytes      length bytes\n\nBody of package :\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n+  flag  +  message id  +    route    +            data              +\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n 1 byte     0 ~ 5 bytes   0 ~ 256 bytes\n\nFlag of message :\n\n                   1 byte\n++++++++++++++++++++++++++++++++++++++++++\n+          +  message type  +  is route  +\n++++++++++++++++++++++++++++++++++++++++++\n   4 bits          3 bits         1 bit\n\nMessage Types :\n             flag\nrequest :  |----000-| message id | route |\nnotify  :  |----001-| route |\nresponse:  |----010-| message id |\npush    :  |----011-| route |\n\nRoute compress :\n\nflag              route\n|-------0|        | length (1 byte) | utf8 string |\n|-------1|        | route code (2 bytes, big end) |\n'
from __future__ import absolute_import, division, print_function, with_statement
from pypomelo.protobuf import *
from pypomelo.stream import Stream
import json

class Message(object):
    """Encode and decode body of promelo protocol package
    """
    MSG_TYPE_REQUEST = 0
    MSG_TYPE_NOTIFY = 1
    MSG_TYPE_RESPONSE = 2
    MSG_TYPE_PUSH = 3
    MSG_FLAG_BYTES = 1
    MSG_ROUTE_LEN_BYTES = 1
    MSG_ROUTE_CODE_BYTES = 2

    def __init__(self, msg_type, msg_id=0, route='', body={}):
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.route = route
        assert isinstance(body, dict), 'Message body must be a dictionary'
        self.body = body

    def has_id(self):
        return Message.MSG_TYPE_REQUEST == self.msg_type or Message.MSG_TYPE_RESPONSE == self.msg_type

    def has_route(self):
        return Message.MSG_TYPE_RESPONSE != self.msg_type

    def id_len(self):
        if not self.has_id():
            return 0
        ret = 1
        msg_id = self.msg_id >> 7
        while msg_id > 0:
            ret += 1
            msg_id >>= 7

        return ret

    def route_len(self):
        if not self.has_route():
            return 0
        return len(self.route)

    def encode_flag(self, stream, compress_route=True):
        if compress_route:
            stream.write(struct.pack('B', self.msg_type << 1 | 1))
        else:
            stream.write(struct.pack('B', self.msg_type << 1 | 0))

    def encode_id(self, stream):
        assert self.has_id(), "Message type %d don't has id" % self.msg_type
        msg_id = self.msg_id
        while True:
            tmp = msg_id & 127
            nxt = msg_id >> 7
            if nxt != 0:
                tmp += 128
            stream.write(struct.pack('B', tmp))
            msg_id = nxt
            if msg_id == 0:
                break

    def encode_by_route(self, msg_data):
        stream = Stream()
        self.encode_flag(stream, False)
        if self.has_id():
            self.encode_id(stream)
        if self.has_route():
            route_len = self.route_len()
            stream.write(struct.pack('B', route_len))
            stream.write(self.route)
        stream.write(msg_data)
        return stream.getvalue()

    def encode_by_code(self, route_code, msg_data):
        stream = Stream()
        self.encode_flag(stream)
        if self.has_id():
            self.encode_id(stream)
        if self.has_route():
            stream.write(struct.pack('>H', route_code))
        stream.write(msg_data)
        return stream.getvalue()

    def encode(self, route_to_code, client_protos):
        if client_protos is None:
            protos = None
        else:
            protos = client_protos.get(self.route)
        if protos:
            msg_data = protobuf_encode(client_protos, protos, self.body)
        else:
            msg_data = json.dumps(self.body)
        if route_to_code is None:
            code = 0
        else:
            code = route_to_code.get(self.route, 0)
        if code > 0:
            ret = self.encode_by_code(code, msg_data)
        else:
            ret = self.encode_by_route(msg_data)
        return ret

    @classmethod
    def decode_id(cls, stream):
        msg_id = 0
        i = 0
        while True:
            m = struct.unpack('B', stream.read(1))[0]
            msg_id = msg_id + ((m & 127) << 7 * i)
            i += 1
            if 0 == m & 128:
                break

        return msg_id

    @classmethod
    def decode_route(cls, stream, code_to_route, is_route):
        if is_route:
            route_code = struct.unpack('>H', stream.read(2))[0]
            return code_to_route[route_code]
        else:
            route_size = struct.unpack('B', stream.read(1))[0]
            return protobuf_decode_string(stream, route_size)

    @classmethod
    def decode_message(cls, stream, message_type, global_protos, msg_id, route):
        if isinstance(global_protos, dict) and route and global_protos.has_key(route):
            body = protobuf_decode(stream, global_protos, global_protos[route])
        else:
            body = json.loads(stream.read())
        return cls(message_type, msg_id, route, body)

    @classmethod
    def decode(cls, code_to_route, global_protos, data, msgid_to_route=None):
        flag = 15 & struct.unpack('B', data[0])[0]
        message_type = flag >> 1
        is_route = flag & 1
        msg_id = None
        route = None
        stream = Stream(data[1:])
        if message_type == Message.MSG_TYPE_REQUEST:
            msg_id = cls.decode_id(stream)
            route = cls.decode_route(stream, code_to_route, is_route)
        elif message_type == Message.MSG_TYPE_NOTIFY:
            route = cls.decode_route(stream, code_to_route, is_route)
        elif message_type == Message.MSG_TYPE_PUSH:
            route = cls.decode_route(stream, code_to_route, is_route)
        elif message_type == Message.MSG_TYPE_RESPONSE:
            msg_id = cls.decode_id(stream)
            if isinstance(msgid_to_route, dict):
                route = msgid_to_route.get(msg_id)
        return cls.decode_message(stream, message_type, global_protos, msg_id, route)

    @classmethod
    def request(cls, route, request_id, request_data):
        return cls(Message.MSG_TYPE_REQUEST, request_id, route, request_data)

    @classmethod
    def notify(cls, route, notify_data):
        return cls(Message.MSG_TYPE_NOTIFY, None, route, notify_data)