# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/snmpmanager.py
# Compiled at: 2008-10-18 18:59:45
import socket, select, logging, Queue, time, os, asyncore
from libsnmp import debug
from libsnmp import asynrole
from libsnmp import rfc1157
from libsnmp import rfc1905
from libsnmp import v1
from libsnmp import v2
log = logging.getLogger('snmp-manager')
typeValDict = {'i': 2, 
   's': 4, 
   'o': 6, 
   't': 67, 
   'a': 64, 
   'c': 65, 
   'C': 70}

class snmpManager(asynrole.manager):
    nextRequestID = 0

    def __init__(self, queueEmpty=None, trapCallback=None, interface=('0.0.0.0', 0), timeout=0.25):
        """ Create a new snmpManager bound to interface
            queueEmpty is a callback of what to do if I run out
            of stuff to do. Default is to wait for more stuff.
        """
        self.queueEmpty = queueEmpty
        self.outbound = Queue.Queue()
        self.callbacks = {}
        self.trapCallback = trapCallback
        asynrole.manager.__init__(self, (self.receiveData, None), interface=interface, timeout=timeout)
        try:
            pass
        except:
            raise

        return

    def assignRequestID(self):
        """ Assign a unique requestID 
        """
        reqID = self.nextRequestID
        self.nextRequestID += 1
        return reqID

    def createGetRequestPDU(self, varbindlist, version=2):
        reqID = self.assignRequestID()
        if version == 1:
            pdu = rfc1157.Get(reqID, varBindList=varbindlist)
        elif version == 2:
            pdu = rfc1905.Get(reqID, varBindList=varbindlist)
        return pdu

    def createGetNextRequestPDU(self, varbindlist, version=2):
        reqID = self.assignRequestID()
        if version == 1:
            pdu = rfc1157.GetNext(reqID, varBindList=varbindlist)
        elif version == 2:
            pdu = rfc1905.GetNext(reqID, varBindList=varbindlist)
        return pdu

    def createSetRequestPDU(self, varbindlist, version=2):
        reqID = self.assignRequestID()
        if version == 1:
            pdu = rfc1157.Set(reqID, varBindList=varbindlist)
        elif version == 2:
            pdu = rfc1905.Set(reqID, varBindList=varbindlist)
        return pdu

    def createGetRequestMessage(self, oid, community='public', version=2):
        """ Creates a message object from a pdu and a
            community string.
        """
        if version == 1:
            objID = rfc1157.ObjectID(oid)
            val = rfc1157.Null()
            varbindlist = rfc1157.VarBindList([rfc1157.VarBind(objID, val)])
            pdu = self.createGetRequestPDU(varbindlist, 1)
            message = rfc1157.Message(community=community, data=pdu)
        elif version == 2:
            objID = rfc1905.ObjectID(oid)
            val = rfc1905.Null()
            varbindlist = rfc1905.VarBindList([rfc1905.VarBind(objID, val)])
            pdu = self.createGetRequestPDU(varbindlist, 2)
            message = rfc1905.Message(community=community, data=pdu)
        else:
            raise ValueError('Unknown version %d' % version)
        return message

    def createGetNextRequestMessage(self, varbindlist, community='public', version=2):
        """ Creates a message object from a pdu and a
            community string.
        """
        pdu = self.createGetNextRequestPDU(varbindlist, version)
        if version == 1:
            return rfc1157.Message(community=community, data=pdu)
        if version == 2:
            return rfc1905.Message(community=community, data=pdu)

    def createSetRequestMessage(self, oid, valtype, value, community='public', version=2):
        """ Creates a message object from a pdu and a
            community string.
        """
        if version == 1:
            objID = rfc1157.ObjectID(oid)
            val = rfc1157.tagDecodeDict[valtype](value)
            varbindlist = rfc1157.VarBindList([rfc1157.VarBind(objID, val)])
            pdu = self.createSetRequestPDU(varbindlist, 1)
            message = rfc1157.Message(community=community, data=pdu)
        elif version == 2:
            objID = rfc1905.ObjectID(oid)
            val = rfc1905.tagDecodeDict[valtype](value)
            varbindlist = rfc1905.VarBindList([rfc1905.VarBind(objID, val)])
            pdu = self.createSetRequestPDU(varbindlist, 1)
            message = rfc1905.Message(community=community, data=pdu)
        else:
            raise ValueError('Unknown version %d' % version)
        return message

    def createTrapMessage(self, pdu, community='public', version=2):
        """ Creates a message object from a pdu and a
            community string.
        """
        if version == 1:
            return v1.createTrapMessage(community=community, data=pdu)
        if version == 2:
            return v2.createTrapMessage(community=community, data=pdu)

    def createTrapPDU(self, varbindlist, version=2, enterprise='.1.3.6.1.4', agentAddr=None, genericTrap=6, specificTrap=0):
        """ Creates a Trap PDU object from a list of strings and integers
            along with a varBindList to make it a bit easier to build a Trap.
        """
        if agentAddr is None:
            agentAddr = self.getsockname()[0]
        if version == 1:
            ent = rfc1157.ObjectID(enterprise)
            agent = rfc1157.NetworkAddress(agentAddr)
            gTrap = rfc1157.GenericTrap(genericTrap)
            sTrap = rfc1157.Integer(specificTrap)
            ts = rfc1157.TimeTicks(self.getSysUptime())
            pdu = rfc1157.TrapPDU(ent, agent, gTrap, sTrap, ts, varbindlist)
        elif version == 2:
            ent = rfc1905.ObjectID(enterprise)
            agent = rfc1905.NetworkAddress(agentAddr)
            gTrap = rfc1157.GenericTrap(genericTrap)
            sTrap = rfc1905.Integer(specificTrap)
            ts = rfc1905.TimeTicks(self.getSysUptime())
            pdu = rfc1157.TrapPDU(ent, agent, gTrap, sTrap, ts, varbindlist)
        return pdu

    def snmpGet(self, oid, remote, callback, community='public', version=2):
        """ snmpGet issues an SNMP Get Request to remote for
            the object ID oid 
            remote is a tuple of (host, port)
            oid is a dotted string eg: .1.2.6.1.0.1.1.3.0
        """
        msg = self.createGetRequestMessage(oid, community, version)
        self.outbound.put((msg, remote))
        self.callbacks[msg.data.requestID] = callback
        return msg.data.requestID

    def snmpGetNext(self, varbindlist, remote, callback, community='public', version=2):
        """ snmpGetNext issues an SNMP Get Next Request to remote for
            the varbindlist that is passed in. It is assumed that you
            have either built a varbindlist yourself or just pass
            one in that was previously returned by an snmpGet or snmpGetNext
        """
        msg = self.createGetNextRequestMessage(varbindlist, community, version)
        self.outbound.put((msg, remote))
        self.callbacks[msg.data.requestID] = callback
        return msg.data.requestID

    def snmpSet(self, oid, valtype, value, remote, callback, community='public', version=2):
        """
        snmpSet is slightly more complex in that you need to pass in
        a combination of oid and value in order to set a variable.
        Depending on the version, this will be built into the appropriate
        varbindlist for message creation.
        valtype should be a tagDecodeDict key
        """
        msg = self.createSetRequestMessage(oid, valtype, value, community, version)
        self.outbound.put((msg, remote))
        self.callbacks[msg.data.requestID] = callback
        return msg.data.requestID

    def snmpTrap(self, remote, trapPDU, community='public', version=2):
        """ Queue up a trap for sending
        """
        msg = self.createTrapMessage(trapPDU, community, version)
        self.outbound.put((msg, remote))

    def receiveData(self, manager, cb_ctx, (data, src), (exc_type, exc_value, exc_traceback)):
        """ This method should be called when data is received
            from a remote host.
        """
        if exc_type is not None:
            raise exc_type(exc_value)
        msg = rfc1905.Message().decode(data)
        if msg.version == 0:
            self.handleV1Message(msg)
        elif msg.version == 1:
            self.handleV2Message(msg)
        else:
            log.error('Unknown message version %d detected' % msg.version)
            log.error('version is a %s' % msg.version())
            raise ValueError('Unknown message version %d detected' % msg.version)
        return

    def handleV1Message(self, msg):
        """ Handle reception of an SNMP version 1 message 
        """
        if isinstance(msg.data, rfc1157.PDU):
            self.callbacks[msg.data.requestID](self, msg)
            del self.callbacks[msg.data.requestID]
        elif isinstance(msg.data, rfc1157.TrapPDU):
            self.trapCallback(self, msg)
        else:
            log.info('Unknown SNMPv1 Message type received')

    def handleV2Message(self, msg):
        """ Handle reception of an SNMP version 2c message
        """
        if isinstance(msg.data, rfc1905.PDU):
            self.callbacks[msg.data.requestID](self, msg)
            del self.callbacks[msg.data.requestID]
        elif isinstance(msg.data, rfc1905.TrapPDU):
            self.trapCallback(self, msg)
        else:
            log.info('Unknown SNMPv2 Message type received')

    def enterpriseOID(self, partialOID):
        """ A convenience method to automagically prepend the
            'enterprise' prefix to the partial OID
        """
        return '.1.3.6.1.2.1.' + partialOID

    def run(self):
        """
        Listen for incoming request thingies
        and send pending requests
        """
        while 1:
            try:
                self.poll()
                request = self.outbound.get(0)
                self.send(request[0].encode(), request[1])
            except Queue.Empty:
                if self.queueEmpty:
                    self.queueEmpty(self)
            except:
                raise

    def getSysUptime(self):
        """ This is a pain because of system dependence
            Each OS has a different way of doing this and I
            cannot find a Python builtin that will do it.
        """
        try:
            uptime = open('/proc/uptime').read().split()
            upsecs = int(float(uptime[0]) * 100)
            return upsecs
        except:
            return 0

    def typeSetter(self, typestring):
        """
        Used to figure out the right tag value key to use in
        snmpSet. This is really only used for a more user-friendly
        way of doing things from a frontend. Use the actual key
        values if you're calling snmpSet programmatically.
        """
        return typeValDict[typestring]