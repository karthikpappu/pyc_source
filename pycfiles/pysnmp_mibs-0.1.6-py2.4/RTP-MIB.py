# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/RTP-MIB.py
# Compiled at: 2016-02-13 18:27:38
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, ConstraintsIntersection, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'ConstraintsIntersection', 'SingleValueConstraint', 'ValueRangeConstraint', 'ValueSizeConstraint')
(InterfaceIndex,) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(TimeTicks, Gauge32, Counter64, iso, NotificationType, ModuleIdentity, mib_2, ObjectIdentity, Unsigned32, Integer32, IpAddress, Counter32, Bits, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn) = mibBuilder.importSymbols('SNMPv2-SMI', 'TimeTicks', 'Gauge32', 'Counter64', 'iso', 'NotificationType', 'ModuleIdentity', 'mib-2', 'ObjectIdentity', 'Unsigned32', 'Integer32', 'IpAddress', 'Counter32', 'Bits', 'MibIdentifier', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn')
(TextualConvention, DisplayString, TruthValue, TDomain, TimeStamp, TestAndIncr, RowStatus, TAddress) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString', 'TruthValue', 'TDomain', 'TimeStamp', 'TestAndIncr', 'RowStatus', 'TAddress')
(Utf8String,) = mibBuilder.importSymbols('SYSAPPL-MIB', 'Utf8String')
rtpMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 87)).setRevisions(('2000-10-02 00:00',))
if mibBuilder.loadTexts:
    rtpMIB.setLastUpdated('200010020000Z')
if mibBuilder.loadTexts:
    rtpMIB.setOrganization('IETF AVT Working Group\n    Email:   rem-conf@es.net')
if mibBuilder.loadTexts:
    rtpMIB.setContactInfo('Mark Baugher\n    Postal: Intel Corporation\n            2111 NE 25th Avenue\n            Hillsboro, OR   97124\n            United States\n    Tel:    +1 503 466 8406\n    Email:  mbaugher@passedge.com\n\n            Bill Strahm\n    Postal: Intel Corporation\n            2111 NE 25th Avenue\n            Hillsboro, OR   97124\n            United States\n    Tel:    +1 503 264 4632\n    Email:  bill.strahm@intel.com\n\n            Irina Suconick\n    Postal: Ennovate Networks\n            60 Codman Hill Rd.,\n            Boxboro, Ma 01719\n    Tel:    +1 781-505-2155\n    Email:  irina@ennovatenetworks.com')
if mibBuilder.loadTexts:
    rtpMIB.setDescription("The managed objects of RTP systems.  The MIB is\n        structured around three types of information.\n        1. General information about RTP sessions such\n           as the session address.\n        2. Information about RTP streams being sent to\n           an RTP session by a particular sender.\n        3. Information about RTP streams received on an\n           RTP session by a particular receiver from a\n           particular sender.\n         There are two types of RTP Systems, RTP hosts and\n         RTP monitors.  As described below, certain objects\n         are unique to a particular type of RTP System.   An\n         RTP host may also function as an RTP monitor.\n         Refer to RFC 1889, 'RTP: A Transport Protocol for\n         Real-Time Applications,' section 3.0, for definitions.")
rtpMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 87, 1))
rtpConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 87, 2))
rtpSessionNewIndex = MibScalar((1, 3, 6, 1, 2, 1, 87, 1, 1), TestAndIncr()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rtpSessionNewIndex.setDescription("This  object  is  used  to  assign  values  to rtpSessionIndex\n       as described in 'Textual Conventions  for  SMIv2'.  For an RTP\n       system that supports the creation of rows, the  network manager\n       would read the  object,  and  then write the value back in\n       the Set that creates a new instance  of rtpSessionEntry.   If\n       the  Set  fails with the code 'inconsistentValue,' then the\n       process must be repeated; If the Set succeeds, then the object\n       is incremented, and the  new  instance  is created according to\n       the manager's directions.  However, if the RTP agent is not\n       acting as a monitor, only the RTP agent may create conceptual\n       rows in the RTP session table.")
rtpSessionInverseTable = MibTable((1, 3, 6, 1, 2, 1, 87, 1, 2))
if mibBuilder.loadTexts:
    rtpSessionInverseTable.setDescription('Maps rtpSessionDomain, rtpSessionRemAddr, and rtpSessionLocAddr\n       TAddress pairs to one or more rtpSessionIndex values, each\n       describing a row in the rtpSessionTable.  This makes it possible\n       to retrieve the row(s) in the rtpSessionTable corresponding to a\n       given session without having to walk the entire (potentially\n       large) table.')
rtpSessionInverseEntry = MibTableRow((1, 3, 6, 1, 2, 1, 87, 1, 2, 1)).setIndexNames((0, 'RTP-MIB', 'rtpSessionDomain'), (0, 'RTP-MIB', 'rtpSessionRemAddr'), (0, 'RTP-MIB', 'rtpSessionLocAddr'), (0, 'RTP-MIB', 'rtpSessionIndex'))
if mibBuilder.loadTexts:
    rtpSessionInverseEntry.setDescription('Each entry corresponds to exactly one entry in the\n       rtpSessionTable - the entry containing the tuple,\n       rtpSessionDomain, rtpSessionRemAddr, rtpSessionLocAddr\n       and rtpSessionIndex.')
rtpSessionInverseStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 2, 1, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionInverseStartTime.setDescription('The value of SysUpTime at the time that this row was\n       created.')
rtpSessionTable = MibTable((1, 3, 6, 1, 2, 1, 87, 1, 3))
if mibBuilder.loadTexts:
    rtpSessionTable.setDescription("There's one entry in rtpSessionTable for each RTP session\n          on which packets are being sent, received, and/or\n          monitored.")
rtpSessionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 87, 1, 3, 1)).setIndexNames((0, 'RTP-MIB', 'rtpSessionIndex'))
if mibBuilder.loadTexts:
    rtpSessionEntry.setDescription("Data in rtpSessionTable uniquely identify an RTP session.  A\n       host RTP agent MUST create a read-only row for each session to\n       which packets are being sent or received.  Rows MUST be created\n       by the RTP Agent at the start of a session when one or more\n       senders or receivers are observed.  Rows created by an RTP agent\n       MUST be deleted when the session is over and there are no\n       rtpRcvrEntry and no rtpSenderEntry for this session.  An RTP\n       session SHOULD be monitored to create management information on\n       all RTP streams being sent or received when the\n       rtpSessionMonitor has the TruthValue of 'true(1)'.  An RTP\n       monitor SHOULD permit row creation with the side effect of\n       causing the RTP System to join the multicast session for the\n       purposes of gathering management information  (additional\n       conceptual rows are created in the rtpRcvrTable and\n       rtpSenderTable).  Thus, rtpSessionTable rows SHOULD be created\n       for RTP session monitoring purposes.  Rows created by a\n       management application SHOULD be deleted via SNMP operations by\n       management applications.  Rows created by management operations\n       are deleted by management operations by setting\n       rtpSessionRowStatus to 'destroy(6)'.")
rtpSessionIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    rtpSessionIndex.setDescription('The index of the conceptual row which is for SNMP purposes\n       only and has no relation to any protocol value.  There is\n       no requirement that these rows are created or maintained\n       sequentially.')
rtpSessionDomain = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 2), TDomain()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    rtpSessionDomain.setDescription("The transport-layer protocol used for sending or receiving\n       the stream of RTP data packets on this session.\n       Cannot be changed if rtpSessionRowStatus is 'active'.")
rtpSessionRemAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 3), TAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    rtpSessionRemAddr.setDescription("The address to which RTP packets are sent by the RTP system.\n      In an IP multicast RTP session, this is the single address used\n      by all senders and receivers of RTP session data.  In a unicast\n      RTP session this is the unicast address of the remote RTP system.\n      'The destination address pair may be common for all participants,\n      as in the case of IP multicast, or may be different for each, as\n      in the case of individual unicast network address pairs.'  See\n      RFC 1889, 'RTP: A Transport Protocol for Real-Time Applications,'\n      sec. 3.  The transport service is identified by rtpSessionDomain.\n      For snmpUDPDomain, this is an IP address and even-numbered UDP\n      Port with the RTCP being sent on the next higher odd-numbered\n      port, see RFC 1889, sec. 5.")
rtpSessionLocAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 4), TAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionLocAddr.setDescription("The local address used by the RTP system.  In an IP multicast\n       RTP session, rtpSessionRemAddr will be the same IP multicast\n       address as rtpSessionLocAddr.  In a unicast RTP session,\n       rtpSessionRemAddr and rtpSessionLocAddr will have different\n       unicast addresses.  See RFC 1889, 'RTP: A Transport Protocol for\n       Real-Time Applications,' sec. 3.  The transport service is\n       identified by rtpSessionDomain.  For snmpUDPDomain, this is an IP\n       address and even-numbered UDP Port with the RTCP being sent on\n       the next higher odd-numbered port, see RFC 1889, sec. 5.")
rtpSessionIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 5), InterfaceIndex()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    rtpSessionIfIndex.setDescription("The ifIndex value is set to the corresponding value\n      from IF-MIB (See RFC 2233, 'The Interfaces Group MIB using\n      SMIv2').  This is the interface that the RTP stream is being sent\n      to or received from, or in the case of an RTP Monitor the\n      interface that RTCP packets will be received on.  Cannot be\n      changed if rtpSessionRowStatus is 'active'.")
rtpSessionSenderJoins = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionSenderJoins.setDescription("The number of senders that have been observed to have\n       joined the session since this conceptual row was created\n       (rtpSessionStartTime).  A sender 'joins' an RTP\n       session by sending to it.  Senders that leave and then\n       re-join following an RTCP BYE (see RFC 1889, 'RTP: A\n       Transport Protocol for Real-Time Applications,' sec. 6.6)\n       or session timeout may be counted twice.  Every time a new\n       RTP sender is detected either using RTP or RTCP, this counter\n       is incremented.")
rtpSessionReceiverJoins = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionReceiverJoins.setDescription("The number of receivers that have been been observed to\n       have joined this session since this conceptual row was\n       created (rtpSessionStartTime).  A receiver 'joins' an RTP\n       session by sending RTCP Receiver Reports to the session.\n       Receivers that leave and then re-join following an RTCP BYE\n       (see RFC 1889, 'RTP: A Transport Protocol for Real-Time\n       Applications,' sec. 6.6) or session timeout may be counted\n       twice.")
rtpSessionByes = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionByes.setDescription("A count of RTCP BYE (see RFC 1889, 'RTP: A Transport\n       Protocol for Real-Time Applications,' sec. 6.6) messages\n       received by this entity.")
rtpSessionStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 9), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionStartTime.setDescription('The value of SysUpTime at the time that this row was\n       created.')
rtpSessionMonitor = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 10), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSessionMonitor.setDescription("Boolean, Set to 'true(1)' if remote senders or receivers in\n       addition to the local RTP System are to be monitored using RTCP.\n       RTP Monitors MUST initialize to 'true(1)' and RTP Hosts SHOULD\n       initialize this 'false(2)'.  Note that because 'host monitor'\n       systems are receiving RTCP from their remote participants they\n       MUST set this value to 'true(1)'.")
rtpSessionRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 3, 1, 11), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    rtpSessionRowStatus.setDescription("Value of 'active' when RTP or RTCP messages are being\n       sent or received by an RTP System.  A newly-created\n       conceptual row must have the all read-create objects\n       initialized before becoming 'active'.\n       A conceptual row that is in the 'notReady' or 'notInService'\n       state MAY be removed after 5  minutes.")
rtpSenderInverseTable = MibTable((1, 3, 6, 1, 2, 1, 87, 1, 4))
if mibBuilder.loadTexts:
    rtpSenderInverseTable.setDescription('Maps rtpSenderAddr, rtpSessionIndex, to the rtpSenderSSRC\n       index of the rtpSenderTable.  This table allows management\n       applications to find entries sorted by rtpSenderAddr rather than\n       sorted by rtpSessionIndex.  Given the rtpSessionDomain and\n       rtpSenderAddr, a set of rtpSessionIndex and rtpSenderSSRC values\n       can be returned from a tree walk.  When rtpSessionIndex is\n       specified in the SNMP Get-Next operations, one or more\n       rtpSenderSSRC values may be returned.')
rtpSenderInverseEntry = MibTableRow((1, 3, 6, 1, 2, 1, 87, 1, 4, 1)).setIndexNames((0, 'RTP-MIB', 'rtpSessionDomain'), (0, 'RTP-MIB', 'rtpSenderAddr'), (0, 'RTP-MIB', 'rtpSessionIndex'), (0, 'RTP-MIB', 'rtpSenderSSRC'))
if mibBuilder.loadTexts:
    rtpSenderInverseEntry.setDescription('Each entry corresponds to exactly one entry in the\n       rtpSenderTable - the entry containing the index pair,\n       rtpSessionIndex, rtpSenderSSRC.')
rtpSenderInverseStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 4, 1, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderInverseStartTime.setDescription('The value of SysUpTime at the time that this row was\n       created.')
rtpSenderTable = MibTable((1, 3, 6, 1, 2, 1, 87, 1, 5))
if mibBuilder.loadTexts:
    rtpSenderTable.setDescription("Table of information about a sender or senders to an RTP\n       Session. RTP sending hosts MUST have an entry in this table\n       for each stream being sent.  RTP receiving hosts MAY have an\n       entry in this table for each sending stream being received by\n       this host.  RTP monitors MUST create an entry for each observed\n       sender to a multicast RTP Session as a side-effect when a\n       conceptual row in the rtpSessionTable is made 'active' by a\n       manager.")
rtpSenderEntry = MibTableRow((1, 3, 6, 1, 2, 1, 87, 1, 5, 1)).setIndexNames((0, 'RTP-MIB', 'rtpSessionIndex'), (0, 'RTP-MIB', 'rtpSenderSSRC'))
if mibBuilder.loadTexts:
    rtpSenderEntry.setDescription("Each entry contains information from a single RTP Sender\n       Synchronization Source (SSRC, see RFC 1889 'RTP: A Transport\n       Protocol for Real-Time Applications' sec.6).  The session is\n       identified to the the SNMP entity by rtpSessionIndex.\n       Rows are removed by the RTP agent when a BYE is received\n       from the sender or when the sender times out (see RFC\n       1889, Sec. 6.2.1) or when the rtpSessionEntry is deleted.")
rtpSenderSSRC = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 1), Unsigned32())
if mibBuilder.loadTexts:
    rtpSenderSSRC.setDescription("The RTP SSRC, or synchronization source identifier of the\n       sender.  The RTP session address plus an SSRC uniquely\n       identify a sender to an RTP session (see RFC 1889, 'RTP: A\n       Transport Protocol for Real-Time Applications' sec.3).")
rtpSenderCNAME = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 2), Utf8String()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderCNAME.setDescription('The RTP canonical name of the sender.')
rtpSenderAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 3), TAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderAddr.setDescription('The unicast transport source address of the sender.  In the\n       case of an RTP Monitor this address is the address that the\n       sender is using to send its RTCP Sender Reports.')
rtpSenderPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 4), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderPackets.setDescription('Count of RTP packets sent by this sender, or observed by\n       an RTP monitor, since rtpSenderStartTime.')
rtpSenderOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 5), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderOctets.setDescription('Count of non-header RTP octets sent by this sender, or observed\n       by an RTP monitor, since rtpSenderStartTime.')
rtpSenderTool = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 6), Utf8String().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderTool.setDescription('Name of the application program source of the stream.')
rtpSenderSRs = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderSRs.setDescription('A count of the number of RTCP Sender Reports that have\n       been sent from this sender, or observed if the RTP entity\n       is a monitor, since rtpSenderStartTime.')
rtpSenderSRTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 8), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderSRTime.setDescription('rtpSenderSRTime is the value of SysUpTime at the time that\n       the last SR was received from this sender, in the case of a\n       monitor or receiving host.  Or sent by this sender, in the\n       case of a sending host.')
rtpSenderPT = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderPT.setDescription("Payload type from the RTP header of the most recently received\n       RTP Packet (see RFC 1889, 'RTP: A Transport Protocol for\n       Real-Time Applications' sec. 5).")
rtpSenderStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 5, 1, 10), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpSenderStartTime.setDescription('The value of SysUpTime at the time that this row was\n       created.')
rtpRcvrInverseTable = MibTable((1, 3, 6, 1, 2, 1, 87, 1, 6))
if mibBuilder.loadTexts:
    rtpRcvrInverseTable.setDescription('Maps rtpRcvrAddr and rtpSessionIndex to the rtpRcvrSRCSSRC and\n       rtpRcvrSSRC indexes of the rtpRcvrTable.  This table allows\n       management applications to find entries sorted by rtpRcvrAddr\n       rather than by rtpSessionIndex. Given rtpSessionDomain and\n       rtpRcvrAddr, a set of rtpSessionIndex, rtpRcvrSRCSSRC, and\n       rtpRcvrSSRC values can be returned from a tree walk.  When\n       rtpSessionIndex is specified in SNMP Get-Next operations, one or\n       more rtpRcvrSRCSSRC and rtpRcvrSSRC pairs may be returned.')
rtpRcvrInverseEntry = MibTableRow((1, 3, 6, 1, 2, 1, 87, 1, 6, 1)).setIndexNames((0, 'RTP-MIB', 'rtpSessionDomain'), (0, 'RTP-MIB', 'rtpRcvrAddr'), (0, 'RTP-MIB', 'rtpSessionIndex'), (0, 'RTP-MIB', 'rtpRcvrSRCSSRC'), (0, 'RTP-MIB', 'rtpRcvrSSRC'))
if mibBuilder.loadTexts:
    rtpRcvrInverseEntry.setDescription('Each entry corresponds to exactly one entry in the\n       rtpRcvrTable - the entry containing the index pair,\n       rtpSessionIndex, rtpRcvrSSRC.')
rtpRcvrInverseStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 6, 1, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrInverseStartTime.setDescription('The value of SysUpTime at the time that this row was\n       created.')
rtpRcvrTable = MibTable((1, 3, 6, 1, 2, 1, 87, 1, 7))
if mibBuilder.loadTexts:
    rtpRcvrTable.setDescription("Table of information about a receiver or receivers of RTP\n       session data. RTP hosts that receive RTP session packets\n       MUST create an entry in this table for that receiver/sender\n       pair.  RTP hosts that send RTP session packets MAY create\n       an entry in this table for each receiver to their stream\n       using RTCP feedback from the RTP group.  RTP monitors\n       create an entry for each observed RTP session receiver as\n       a side effect when a conceptual row in the rtpSessionTable\n       is made 'active' by a manager.")
rtpRcvrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 87, 1, 7, 1)).setIndexNames((0, 'RTP-MIB', 'rtpSessionIndex'), (0, 'RTP-MIB', 'rtpRcvrSRCSSRC'), (0, 'RTP-MIB', 'rtpRcvrSSRC'))
if mibBuilder.loadTexts:
    rtpRcvrEntry.setDescription("Each entry contains information from a single RTP\n       Synchronization Source that is receiving packets from the\n       sender identified by rtpRcvrSRCSSRC (SSRC, see RFC 1889,\n       'RTP: A Transport Protocol for Real-Time Applications'\n       sec.6).  The session is identified to the the RTP Agent entity\n       by rtpSessionIndex.  Rows are removed by the RTP agent when\n       a BYE is received from the sender or when the sender times\n       out (see RFC 1889, Sec. 6.2.1) or when the rtpSessionEntry is\n       deleted.")
rtpRcvrSRCSSRC = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 1), Unsigned32())
if mibBuilder.loadTexts:
    rtpRcvrSRCSSRC.setDescription("The RTP SSRC, or synchronization source identifier of the\n       sender.  The RTP session address plus an SSRC uniquely\n       identify a sender or receiver of an RTP stream (see RFC\n       1889, 'RTP:  A Transport Protocol for Real-Time\n       Applications' sec.3).")
rtpRcvrSSRC = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 2), Unsigned32())
if mibBuilder.loadTexts:
    rtpRcvrSSRC.setDescription("The RTP SSRC, or synchronization source identifier of the\n       receiver.  The RTP session address plus an SSRC uniquely\n       identify a receiver of an RTP stream (see RFC 1889, 'RTP:\n       A Transport Protocol for Real-Time Applications' sec.3).")
rtpRcvrCNAME = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 3), Utf8String()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrCNAME.setDescription('The RTP canonical name of the receiver.')
rtpRcvrAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 4), TAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrAddr.setDescription('The unicast transport address on which the receiver is\n       receiving RTP packets and/or RTCP Receiver Reports.')
rtpRcvrRTT = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 5), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrRTT.setDescription("The round trip time measurement taken by the source of the\n       RTP stream based on the algorithm described on sec. 6 of\n       RFC 1889, 'RTP: A Transport Protocol for Real-Time\n       Applications.'  This algorithm can produce meaningful\n       results when the RTP agent has the same clock as the stream\n       sender (when the RTP monitor is also the sending host for the\n       particular receiver).  Otherwise, the entity should return\n       'noSuchInstance' in response to queries against rtpRcvrRTT.")
rtpRcvrLostPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 6), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrLostPackets.setDescription('A count of RTP  packets lost as observed by this receiver\n       since rtpRcvrStartTime.')
rtpRcvrJitter = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 7), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrJitter.setDescription("An estimate of delay variation as observed by this\n       receiver.  (see RFC 1889, 'RTP: A Transport Protocol\n       for Real-Time Applications' sec.6.3.1 and A.8).")
rtpRcvrTool = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 8), Utf8String().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrTool.setDescription('Name of the application program source of the stream.')
rtpRcvrRRs = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrRRs.setDescription('A count of the number of RTCP Receiver Reports that have\n       been sent from this receiver, or observed if the RTP entity\n       is a monitor, since rtpRcvrStartTime.')
rtpRcvrRRTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 10), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrRRTime.setDescription('rtpRcvrRRTime is the value of SysUpTime at the time that the\n       last RTCP Receiver Report was received from this receiver, in\n       the case of a monitor or RR receiver (the RTP Sender).  It is\n       the  value of SysUpTime at the time that the last RR was sent by\n       this receiver in the case of an RTP receiver sending the RR.')
rtpRcvrPT = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrPT.setDescription("Static or dynamic payload type from the RTP header (see\n       RFC 1889, 'RTP: A Transport Protocol for Real-Time\n       Applications' sec. 5).")
rtpRcvrPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 12), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrPackets.setDescription('Count of RTP packets received by this RTP host receiver\n       since rtpRcvrStartTime.')
rtpRcvrOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 13), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrOctets.setDescription('Count of non-header RTP octets received by this receiving RTP\n       host since rtpRcvrStartTime.')
rtpRcvrStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 87, 1, 7, 1, 14), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rtpRcvrStartTime.setDescription('The value of SysUpTime at the time that this row was\n       created.')
rtpGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 87, 2, 1))
rtpSystemGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 87, 2, 1, 1)).setObjects(*(('RTP-MIB', 'rtpSessionDomain'), ('RTP-MIB', 'rtpSessionRemAddr'), ('RTP-MIB', 'rtpSessionIfIndex'), ('RTP-MIB', 'rtpSessionSenderJoins'), ('RTP-MIB', 'rtpSessionReceiverJoins'), ('RTP-MIB', 'rtpSessionStartTime'), ('RTP-MIB', 'rtpSessionByes'), ('RTP-MIB', 'rtpSessionMonitor'), ('RTP-MIB', 'rtpSenderCNAME'), ('RTP-MIB', 'rtpSenderAddr'), ('RTP-MIB', 'rtpSenderPackets'), ('RTP-MIB', 'rtpSenderOctets'), ('RTP-MIB', 'rtpSenderTool'), ('RTP-MIB', 'rtpSenderSRs'), ('RTP-MIB', 'rtpSenderSRTime'), ('RTP-MIB', 'rtpSenderStartTime'), ('RTP-MIB', 'rtpRcvrCNAME'), ('RTP-MIB', 'rtpRcvrAddr'), ('RTP-MIB', 'rtpRcvrLostPackets'), ('RTP-MIB', 'rtpRcvrJitter'), ('RTP-MIB', 'rtpRcvrTool'), ('RTP-MIB', 'rtpRcvrRRs'), ('RTP-MIB', 'rtpRcvrRRTime'), ('RTP-MIB', 'rtpRcvrStartTime')))
if mibBuilder.loadTexts:
    rtpSystemGroup.setDescription('Objects available to all RTP Systems.')
rtpHostGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 87, 2, 1, 2)).setObjects(*(('RTP-MIB', 'rtpSessionLocAddr'), ('RTP-MIB', 'rtpSenderPT'), ('RTP-MIB', 'rtpRcvrPT'), ('RTP-MIB', 'rtpRcvrRTT'), ('RTP-MIB', 'rtpRcvrOctets'), ('RTP-MIB', 'rtpRcvrPackets')))
if mibBuilder.loadTexts:
    rtpHostGroup.setDescription('Objects that are available to RTP Host systems, but may not\n            be available to RTP Monitor systems.')
rtpMonitorGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 87, 2, 1, 3)).setObjects(*(('RTP-MIB', 'rtpSessionNewIndex'), ('RTP-MIB', 'rtpSessionRowStatus')))
if mibBuilder.loadTexts:
    rtpMonitorGroup.setDescription('Objects used to create rows in the RTP Session Table.  These\n        objects are not needed if the system does not create rows.')
rtpInverseGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 87, 2, 1, 4)).setObjects(*(('RTP-MIB', 'rtpSessionInverseStartTime'), ('RTP-MIB', 'rtpSenderInverseStartTime'), ('RTP-MIB', 'rtpRcvrInverseStartTime')))
if mibBuilder.loadTexts:
    rtpInverseGroup.setDescription('Objects used in the Inverse Lookup Tables.')
rtpCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 87, 2, 2))
rtpHostCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 87, 2, 2, 1)).setObjects(*(('RTP-MIB', 'rtpSystemGroup'), ('RTP-MIB', 'rtpHostGroup'), ('RTP-MIB', 'rtpMonitorGroup'), ('RTP-MIB', 'rtpInverseGroup')))
if mibBuilder.loadTexts:
    rtpHostCompliance.setDescription('Host implementations MUST comply.')
rtpMonitorCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 87, 2, 2, 2)).setObjects(*(('RTP-MIB', 'rtpSystemGroup'), ('RTP-MIB', 'rtpMonitorGroup'), ('RTP-MIB', 'rtpHostGroup'), ('RTP-MIB', 'rtpInverseGroup')))
if mibBuilder.loadTexts:
    rtpMonitorCompliance.setDescription('Monitor implementations must comply.  RTP Monitors are not\n          required to support creation or deletion.')
mibBuilder.exportSymbols('RTP-MIB', rtpRcvrStartTime=rtpRcvrStartTime, rtpRcvrJitter=rtpRcvrJitter, rtpSenderTool=rtpSenderTool, rtpSenderSSRC=rtpSenderSSRC, rtpSessionLocAddr=rtpSessionLocAddr, rtpRcvrInverseStartTime=rtpRcvrInverseStartTime, rtpSessionNewIndex=rtpSessionNewIndex, rtpSessionRemAddr=rtpSessionRemAddr, rtpRcvrOctets=rtpRcvrOctets, rtpSessionInverseStartTime=rtpSessionInverseStartTime, rtpRcvrPackets=rtpRcvrPackets, rtpConformance=rtpConformance, rtpSenderPT=rtpSenderPT, rtpSessionMonitor=rtpSessionMonitor, rtpMonitorCompliance=rtpMonitorCompliance, rtpRcvrLostPackets=rtpRcvrLostPackets, rtpRcvrRRs=rtpRcvrRRs, rtpSessionInverseEntry=rtpSessionInverseEntry, rtpInverseGroup=rtpInverseGroup, rtpSenderSRTime=rtpSenderSRTime, rtpSessionTable=rtpSessionTable, rtpRcvrSSRC=rtpRcvrSSRC, rtpSessionIndex=rtpSessionIndex, rtpSenderAddr=rtpSenderAddr, rtpRcvrRRTime=rtpRcvrRRTime, rtpSenderOctets=rtpSenderOctets, rtpRcvrTable=rtpRcvrTable, rtpMIBObjects=rtpMIBObjects, rtpSessionStartTime=rtpSessionStartTime, rtpSenderInverseStartTime=rtpSenderInverseStartTime, rtpSenderStartTime=rtpSenderStartTime, rtpRcvrTool=rtpRcvrTool, rtpSenderPackets=rtpSenderPackets, rtpRcvrInverseEntry=rtpRcvrInverseEntry, rtpRcvrCNAME=rtpRcvrCNAME, rtpSenderCNAME=rtpSenderCNAME, rtpSessionRowStatus=rtpSessionRowStatus, rtpRcvrSRCSSRC=rtpRcvrSRCSSRC, rtpSessionDomain=rtpSessionDomain, rtpSessionInverseTable=rtpSessionInverseTable, rtpSessionByes=rtpSessionByes, rtpRcvrAddr=rtpRcvrAddr, rtpSessionSenderJoins=rtpSessionSenderJoins, rtpSenderSRs=rtpSenderSRs, rtpRcvrPT=rtpRcvrPT, rtpCompliances=rtpCompliances, rtpSenderEntry=rtpSenderEntry, PYSNMP_MODULE_ID=rtpMIB, rtpRcvrInverseTable=rtpRcvrInverseTable, rtpHostGroup=rtpHostGroup, rtpMonitorGroup=rtpMonitorGroup, rtpRcvrRTT=rtpRcvrRTT, rtpSessionReceiverJoins=rtpSessionReceiverJoins, rtpSenderInverseTable=rtpSenderInverseTable, rtpRcvrEntry=rtpRcvrEntry, rtpSessionIfIndex=rtpSessionIfIndex, rtpGroups=rtpGroups, rtpMIB=rtpMIB, rtpHostCompliance=rtpHostCompliance, rtpSenderTable=rtpSenderTable, rtpSenderInverseEntry=rtpSenderInverseEntry, rtpSessionEntry=rtpSessionEntry, rtpSystemGroup=rtpSystemGroup)