# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/messaging/anonymization/tunnel.py
# Compiled at: 2019-06-07 08:10:38
from __future__ import absolute_import
import logging, random, socket, sys, time
from collections import defaultdict
from struct import unpack_from
from traceback import format_exception
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, maybeDeferred, returnValue, succeed
from twisted.internet.error import MessageLengthError
from twisted.internet.protocol import DatagramProtocol
from ...keyvault.public.libnaclkey import LibNaCLPK
from ...taskmanager import TaskManager
from ...util import blocking_call_on_reactor_thread, cast_to_chr
ORIGINATOR = 0
EXIT_NODE = 1
ORIGINATOR_SALT = 2
EXIT_NODE_SALT = 3
ORIGINATOR_SALT_EXPLICIT = 4
EXIT_NODE_SALT_EXPLICIT = 5
PEER_SOURCE_UNKNOWN = 0
PEER_SOURCE_DHT = 1
PEER_SOURCE_PEX = 2
PEER_FLAG_RELAY = 1
PEER_FLAG_EXIT_ANY = 2
PEER_FLAG_EXIT_IPV8 = 4
CIRCUIT_TYPE_DATA = 'DATA'
CIRCUIT_TYPE_IPV8 = 'IPV8'
CIRCUIT_TYPE_IP_SEEDER = 'IP_SEEDER'
CIRCUIT_TYPE_RP_SEEDER = 'RP_SEEDER'
CIRCUIT_TYPE_RP_DOWNLOADER = 'RP_DOWNLOADER'
CIRCUIT_STATE_READY = 'READY'
CIRCUIT_STATE_EXTENDING = 'EXTENDING'
CIRCUIT_STATE_CLOSING = 'CLOSING'
CIRCUIT_ID_PORT = 1024
PING_INTERVAL = 15.0

class DataChecker(object):

    @staticmethod
    def could_be_utp(data):
        if len(data) < 20:
            return False
        byte1, byte2 = unpack_from('!BB', data)
        if not (0 <= byte1 >> 4 <= 4 and byte1 & 15 == 1):
            return False
        if not 0 <= byte2 <= 2:
            return False
        return True

    @staticmethod
    def could_be_udp_tracker(data):
        if len(data) >= 8 and 0 <= unpack_from('!I', data, 0)[0] <= 3 or len(data) >= 12 and 0 <= unpack_from('!I', data, 8)[0] <= 3:
            return True
        return False

    @staticmethod
    def could_be_dht(data):
        try:
            if len(data) > 1 and data[0:1] == 'd' and data[-1:] == 'e':
                return True
        except:
            pass

        return False

    @staticmethod
    def could_be_ipv8(data):
        return len(data) >= 23 and data[0:1] == '\x00' and data[1:2] in ('\x01', '\x02')

    @staticmethod
    def is_allowed(data):
        return DataChecker.could_be_utp(data) or DataChecker.could_be_udp_tracker(data) or DataChecker.could_be_dht(data) or DataChecker.could_be_ipv8(data)


class Tunnel(object):

    def __init__(self, circuit_id, peer):
        self.circuit_id = circuit_id
        self._peer = peer
        self.creation_time = time.time()
        self.last_activity = time.time()
        self.bytes_up = self.bytes_down = 0
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def peer(self):
        return self._peer

    def beat_heart(self):
        self.last_activity = time.time()


class TunnelExitSocket(Tunnel, DatagramProtocol, TaskManager):

    def __init__(self, circuit_id, peer, overlay):
        Tunnel.__init__(self, circuit_id, peer)
        TaskManager.__init__(self)
        self.overlay = overlay
        self.port = None
        self.ips = defaultdict(int)
        return

    @blocking_call_on_reactor_thread
    def enable(self):
        if not self.enabled:
            self.port = reactor.listenUDP(0, self)

    @property
    def enabled(self):
        return self.port is not None

    def sendto(self, data, destination):
        self.beat_heart()
        if self.check_num_packets(destination, False):
            if DataChecker.is_allowed(data):

                def on_error(failure):
                    self.logger.error("Can't resolve ip address for hostname %s. Failure: %s", destination[0], failure)

                def on_ip_address(ip_address):
                    self.logger.debug('Resolved hostname %s to ip_address %s', destination[0], ip_address)
                    try:
                        self.transport.write(data, (ip_address, destination[1]))
                        self.overlay.increase_bytes_sent(self, len(data))
                    except (AttributeError, MessageLengthError, socket.error) as exception:
                        self.logger.error('Failed to write data to transport: %s. Destination: %r error was: %r', exception, destination, exception)

                try:
                    socket.inet_aton(cast_to_chr(destination[0]))
                    on_ip_address(destination[0])
                except socket.error:
                    resolve_ip_address_deferred = reactor.resolve(destination[0])
                    resolve_ip_address_deferred.addCallbacks(on_ip_address, on_error)
                    self.register_task('resolving_%r' % destination[0], resolve_ip_address_deferred)

            else:
                self.logger.error('dropping forbidden packets from exit socket with circuit_id %d', self.circuit_id)

    def datagramReceived(self, data, source):
        self.beat_heart()
        self.overlay.increase_bytes_received(self, len(data))
        if self.check_num_packets(source, True):
            if DataChecker.is_allowed(data):
                try:
                    self.tunnel_data(source, data)
                except:
                    self.logger.error('Exception occurred while handling incoming exit node data!\n' + ('').join(format_exception(*sys.exc_info())))

            else:
                self.logger.warning('dropping forbidden packets to exit socket with circuit_id %d', self.circuit_id)

    def tunnel_data(self, source, data):
        self.logger.debug('Tunnel data to origin %s for circuit %s', ('0.0.0.0', 0), self.circuit_id)
        self.overlay.send_data([self.peer], self.circuit_id, ('0.0.0.0', 0), source, data)

    @inlineCallbacks
    def close(self):
        """
        Closes the UDP socket if enabled and cancels all pending deferreds.
        :return: A deferred that fires once the UDP socket has closed.
        """
        yield self.wait_for_deferred_tasks()
        self.shutdown_task_manager()
        done_closing_deferred = succeed(None)
        if self.enabled:
            done_closing_deferred = maybeDeferred(self.port.stopListening)
            self.port = None
        res = yield done_closing_deferred
        returnValue(res)
        return

    def check_num_packets(self, ip, incoming):
        if self.ips[ip] < 0:
            return True
        max_packets_without_reply = self.overlay.settings.max_packets_without_reply
        if self.ips[ip] >= (max_packets_without_reply + 1 if incoming else max_packets_without_reply):
            self.overlay.remove_exit_socket(self.circuit_id, destroy=True)
            self.logger.error('too many packets to a destination without a reply, removing exit socket with circuit_id %d', self.circuit_id)
            return False
        if incoming:
            self.ips[ip] = -1
        else:
            self.ips[ip] += 1
        return True


class Circuit(Tunnel):

    def __init__(self, circuit_id, goal_hops=0, ctype=CIRCUIT_TYPE_DATA, callback=None, required_exit=None, info_hash=None):
        super(Circuit, self).__init__(circuit_id, None)
        self.goal_hops = goal_hops
        self.ctype = ctype
        self.callback = callback
        self.required_exit = required_exit
        self.info_hash = info_hash
        self._closing = False
        self._hops = []
        self.unverified_hop = None
        self.hs_session_keys = None
        self.e2e = False
        return

    @property
    def peer(self):
        if self._hops:
            return self._hops[0]
        return self.unverified_hop

    @property
    def hops(self):
        """
        Return a read only tuple version of the hop-list of this circuit
        @rtype tuple[Hop]
        """
        return tuple(self._hops)

    def add_hop(self, hop):
        """
        Adds a hop to the circuits hop collection
        @param Hop hop: the hop to add
        """
        self._hops.append(hop)

    @property
    def state(self):
        """
        The circuit state, can be either:
        CIRCUIT_STATE_CLOSING, CIRCUIT_STATE_EXTENDING or CIRCUIT_STATE_READY
        @rtype: str
        """
        if self._closing:
            return CIRCUIT_STATE_CLOSING
        else:
            if len(self.hops) < self.goal_hops:
                return CIRCUIT_STATE_EXTENDING
            return CIRCUIT_STATE_READY

    def close(self):
        """
        Sets the state of the circuit to CIRCUIT_STATE_CLOSING. This ensures that this circuit
        will not be used to contact new peers.
        """
        self._closing = True

    def __eq__(self, other):
        return other and self.circuit_id == other.circuit_id


class Hop(object):
    """
    Circuit Hop containing the address, its public key and the first part of
    the Diffie-Hellman handshake
    """

    def __init__(self, public_key=None):
        """
        @param None|LibNaCLPK public_key: public key object of the hop
        """
        assert public_key is None or isinstance(public_key, LibNaCLPK)
        self.session_keys = None
        self.dh_first_part = None
        self.dh_secret = None
        self.address = None
        self.public_key = public_key
        return

    @property
    def host(self):
        """
        The hop's hostname
        """
        if self.address:
            return self.address[0]
        return ' UNKNOWN HOST '

    @property
    def port(self):
        """
        The hop's port
        """
        if self.address:
            return self.address[1]
        return ' UNKNOWN PORT '

    @property
    def node_public_key(self):
        """
        The hop's public_key
        """
        if self.public_key:
            return self.public_key.key_to_bin()
        raise RuntimeError('public key unknown')

    @property
    def mid(self):
        return self.public_key.key_to_hash()


class RelayRoute(Tunnel):
    """
    Relay object containing the destination circuit, socket address and whether
    it is online or not
    """

    def __init__(self, circuit_id, peer, rendezvous_relay=False):
        """
        @type sock_addr: (str, int)
        @type circuit_id: int
        @return:
        """
        super(RelayRoute, self).__init__(circuit_id, peer)
        self.rendezvous_relay = rendezvous_relay


class RendezvousPoint(object):

    def __init__(self, circuit, cookie, finished_callback):
        self.circuit = circuit
        self.cookie = cookie
        self.finished_callback = finished_callback
        self.rp_info = None
        return


class IntroductionPoint(object):

    def __init__(self, peer, seeder_pk, source=PEER_SOURCE_UNKNOWN, last_seen=int(time.time())):
        self.peer = peer
        self.seeder_pk = seeder_pk
        self.source = source
        self.last_seen = last_seen

    def __eq__(self, other):
        return self.peer == other.peer and self.seeder_pk == other.seeder_pk

    def __hash__(self):
        return hash((self.peer, self.seeder_pk))


class Swarm(object):

    def __init__(self, info_hash, hops, seeder_sk=None, max_ip_age=300):
        self.info_hash = info_hash
        self.hops = hops
        self.seeder_sk = seeder_sk
        self.max_ip_age = max_ip_age
        self.intro_points = []
        self.connections = {}
        self.last_lookup = 0
        self.transfer_history = [0, 0]

    @property
    def seeding(self):
        return bool(self.seeder_sk)

    @property
    def _active_circuits(self):
        return [ c for c, _ in self.connections.values() if c.state == CIRCUIT_STATE_READY and c.e2e ]

    def add_connection(self, rp_circuit, intro_point_used):
        if rp_circuit.circuit_id not in self.connections:
            self.connections[rp_circuit.circuit_id] = (
             rp_circuit, intro_point_used)

    def remove_connection(self, rp_circuit):
        removed = self.connections.pop(rp_circuit.circuit_id, None)
        if removed:
            circuit, _ = removed
            self.transfer_history[0] += circuit.bytes_up
            self.transfer_history[1] += circuit.bytes_down
        return bool(removed)

    def has_connection(self, seeder_pk):
        return seeder_pk in [ ip.seeder_pk for _, ip in self.connections.values() ]

    def get_num_connections(self):
        return len(self._active_circuits)

    def get_num_connections_incomplete(self):
        return len(self.connections) - self.get_num_connections()

    def add_intro_point(self, ip):
        old_ip = next((i for i in self.intro_points if i == ip), None)
        if old_ip:
            old_ip.last_seen = time.time()
        else:
            self.intro_points.append(ip)
        now = time.time()
        self.intro_points = [ i for i in self.intro_points if i.last_seen + self.max_ip_age >= now ]
        return old_ip or ip

    def remove_intro_point(self, ip):
        try:
            self.intro_points.remove(ip)
        except ValueError:
            pass

    def get_random_intro_point(self):
        if self.intro_points:
            return random.choice(self.intro_points)
        else:
            return

    def get_num_seeders(self):
        seeder_pks = {ip.seeder_pk for ip in self.intro_points}
        for _, ip in self.connections.values():
            seeder_pks.add(ip.seeder_pk)

        return len(seeder_pks)

    def get_total_up(self):
        return sum([ c.bytes_up for c in self._active_circuits ]) + self.transfer_history[0]

    def get_total_down(self):
        return sum([ c.bytes_down for c in self._active_circuits ]) + self.transfer_history[1]