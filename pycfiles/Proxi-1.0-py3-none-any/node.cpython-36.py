# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/node.py
# Compiled at: 2017-01-21 19:50:32
# Size of source mod 2**32: 2488 bytes
__doc__ = 'Provides structures for representing nodes.'
from __future__ import absolute_import
import socket, struct, typing, attr, netaddr, netaddr.strategy.ipv6
__all__ = 'SocketAddress'

def ipv6_address(addr, resolve=True):
    try:
        return netaddr.IPAddress(addr).ipv6(ipv4_compatible=True)
    except netaddr.AddrFormatError:
        if not resolve or isinstance(addr, int):
            raise
        return ipv6_address((socket.gethostbyname(str(addr))), resolve=False)


@attr.s(frozen=True, slots=True)
class SocketAddress(object):
    """SocketAddress"""
    host = attr.ib(convert=ipv6_address)
    port = attr.ib(convert=int)

    def pack(self):
        """Packs a socket address into a 24-bit struct.

        Returns:
            A bytestring containing the packed host and port.

        """
        port_words = netaddr.strategy.ipv6.int_to_words(self.port, 4, 4)
        return (struct.pack)(*('>8H4H', ), *self.host.words + port_words)

    @classmethod
    def unpack(cls, addr_bytes):
        """Unpacks a 24-bit bytestring to a :class:`SocketAddress`.

        Args:
            addr_bytes: A bytestring containing an IPv6 address as a
                packed binary string followed by a port number.

        Returns:
            A :class:`~.node.SocketAddress` instance.

        """
        unpacked = struct.unpack('>8H4H', addr_bytes)
        port = 0
        for i, word in enumerate(unpacked[8:][::-1]):
            port |= word << 4 * i

        host = netaddr.strategy.ipv6.words_to_int(unpacked[:8])
        return cls(host, port)

    def __bytes__(self):
        return self.pack()

    def __str__(self):
        try:
            return '{}:{}'.format(self.host.ipv4(), self.port)
        except netaddr.AddrConversionError:
            return '{}:{}'.format(self.host, self.port)