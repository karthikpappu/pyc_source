# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/consul_srv/query.py
# Compiled at: 2017-06-29 12:11:10
"""
Simple wrapper around dnspython to query a Consul agent over its DNS port and
extract ip address/port information.
"""
from dns.resolver import Resolver
from dns import rdatatype
from collections import namedtuple
SRV = namedtuple('SRV', ['host', 'port'])

class Resolver(Resolver):
    """
    Wrapper around the dnspython Resolver class that implements the `srv`
    method. Takes the address and optional port of a DNS server.
    """

    def __init__(self, server_address, port=8600):
        super(Resolver, self).__init__()
        self.nameservers = [server_address]
        self.nameserver_ports = {server_address: port}

    def _get_host(self, answer):
        for resource in answer.response.additional:
            for record in resource.items:
                if record.rdtype == rdatatype.A:
                    return record.address

        raise ValueError('No host information.')

    def _get_port(self, answer):
        for resource in answer:
            if resource.rdtype == rdatatype.SRV:
                return resource.port

        raise ValueError('No port information.')

    def srv(self, resource):
        """
        Query this resolver's nameserver for the name consul service. Returns a
        named host/port tuple from the first element of the response.
        """
        domain_name = ('{}.service.consul').format(resource)
        answer = self.query(domain_name, 'SRV', tcp=True)
        host = self._get_host(answer)
        port = self._get_port(answer)
        return SRV(host, port)