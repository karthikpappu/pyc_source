# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DIAL-CONTROL-MIB.py
# Compiled at: 2016-02-13 18:07:23
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion, ValueRangeConstraint, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ConstraintsUnion', 'ValueRangeConstraint', 'SingleValueConstraint')
(IANAifType,) = mibBuilder.importSymbols('IANAifType-MIB', 'IANAifType')
(ifIndex, InterfaceIndex, ifOperStatus, InterfaceIndexOrZero) = mibBuilder.importSymbols('IF-MIB', 'ifIndex', 'InterfaceIndex', 'ifOperStatus', 'InterfaceIndexOrZero')
(ObjectGroup, NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'NotificationGroup', 'ModuleCompliance')
(Counter64, IpAddress, Gauge32, MibIdentifier, Unsigned32, MibScalar, MibTable, MibTableRow, MibTableColumn, Bits, Integer32, iso, NotificationType, Counter32, TimeTicks, ObjectIdentity, transmission, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'Counter64', 'IpAddress', 'Gauge32', 'MibIdentifier', 'Unsigned32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Bits', 'Integer32', 'iso', 'NotificationType', 'Counter32', 'TimeTicks', 'ObjectIdentity', 'transmission', 'ModuleIdentity')
(RowStatus, TimeStamp, DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'RowStatus', 'TimeStamp', 'DisplayString', 'TextualConvention')
dialControlMib = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 21))
if mibBuilder.loadTexts:
    dialControlMib.setLastUpdated('9609231544Z')
if mibBuilder.loadTexts:
    dialControlMib.setOrganization('IETF ISDN Working Group')
if mibBuilder.loadTexts:
    dialControlMib.setContactInfo('        Guenter Roeck\n             Postal: cisco Systems\n                     170 West Tasman Drive\n                     San Jose, CA 95134\n                     U.S.A.\n             Phone:  +1 408 527 3143\n             E-mail: groeck@cisco.com')
if mibBuilder.loadTexts:
    dialControlMib.setDescription('The MIB module to describe peer information for\n             demand access and possibly other kinds of interfaces.')

class AbsoluteCounter32(Gauge32, TextualConvention):
    __module__ = __name__


dialControlMibObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 1))
dialCtlConfiguration = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 1, 1))
dialCtlAcceptMode = MibScalar((1, 3, 6, 1, 2, 1, 10, 21, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('acceptNone', 1), ('acceptAll', 2), ('acceptKnown', 3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dialCtlAcceptMode.setDescription('The security level for acceptance of incoming calls.\n             acceptNone(1)  - incoming calls will not be accepted\n             acceptAll(2)   - incoming calls will be accepted,\n                              even if there is no matching entry\n                              in the dialCtlPeerCfgTable\n             acceptKnown(3) - incoming calls will be accepted only\n                              if there is a matching entry in the\n                              dialCtlPeerCfgTable\n            ')
dialCtlTrapEnable = MibScalar((1, 3, 6, 1, 2, 1, 10, 21, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2))).clone('disabled')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dialCtlTrapEnable.setDescription('This object indicates whether dialCtlPeerCallInformation\n             and dialCtlPeerCallSetup traps should be generated for\n             all peers. If the value of this object is enabled(1),\n             traps will be generated for all peers. If the value\n             of this object is disabled(2), traps will be generated\n             only for peers having dialCtlPeerCfgTrapEnable set\n             to enabled(1).')
dialCtlPeer = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 1, 2))
dialCtlPeerCfgTable = MibTable((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1))
if mibBuilder.loadTexts:
    dialCtlPeerCfgTable.setDescription('The list of peers from which the managed device\n             will accept calls or to which it will place them.')
dialCtlPeerCfgEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1)).setIndexNames((0, 'DIAL-CONTROL-MIB', 'dialCtlPeerCfgId'), (0, 'IF-MIB', 'ifIndex'))
if mibBuilder.loadTexts:
    dialCtlPeerCfgEntry.setDescription('Configuration data for a single Peer. This entry is\n             effectively permanent, and contains information\n             to identify the peer, how to connect to the peer,\n             how to identify the peer and its permissions.\n             The value of dialCtlPeerCfgOriginateAddress must be\n             specified before a new row in this table can become\n             active(1). Any writeable parameters in an existing entry\n             can be modified while the entry is active. The modification\n             will take effect when the peer in question will be\n             called the next time.\n             An entry in this table can only be created if the\n             associated ifEntry already exists.')
dialCtlPeerCfgId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    dialCtlPeerCfgId.setDescription('This object identifies a single peer. There may\n             be several entries in this table for one peer,\n             defining different ways of reaching this peer.\n             Thus, there may be several entries in this table\n             with the same value of dialCtlPeerCfgId.\n             Multiple entries for one peer may be used to support\n             multilink as well as backup lines.\n             A single peer will be identified by a unique value\n             of this object. Several entries for one peer MUST\n             have the same value of dialCtlPeerCfgId, but different\n             ifEntries and thus different values of ifIndex.')
dialCtlPeerCfgIfType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 2), IANAifType().clone('other')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgIfType.setDescription('The interface type to be used for calling this peer.\n             In case of ISDN, the value of isdn(63) is to be used.')
dialCtlPeerCfgLowerIf = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 3), InterfaceIndexOrZero()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgLowerIf.setDescription('ifIndex value of an interface the peer will have to be\n             called on. For example, on an ISDN interface, this can be\n             the ifIndex value of a D channel or the ifIndex value of a\n             B channel, whatever is appropriate for a given peer.\n             As an example, for Basic Rate leased lines it will be\n             necessary to specify a B channel ifIndex, while for\n\n\n\n\n             semi-permanent connections the D channel ifIndex has\n             to be specified.\n             If the interface can be dynamically assigned, this object\n             has a value of zero.')
dialCtlPeerCfgOriginateAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 4), DisplayString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgOriginateAddress.setDescription("Call Address at which the peer will be called.\n             Think of this as the set of characters following 'ATDT '\n             or the 'phone number' included in a D channel call request.\n\n             The structure of this information will be switch type\n             specific. If there is no address information required\n             for reaching the peer, i.e., for leased lines,\n             this object will be a zero length string.")
dialCtlPeerCfgAnswerAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 5), DisplayString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgAnswerAddress.setDescription('Calling Party Number information element, as for example\n             passed in an ISDN SETUP message by a PBX or switch,\n             for incoming calls.\n             This address can be used to identify the peer.\n             If this address is either unknown or identical\n             to dialCtlPeerCfgOriginateAddress, this object will be\n             a zero length string.')
dialCtlPeerCfgSubAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 6), DisplayString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgSubAddress.setDescription('Subaddress at which the peer will be called.\n             If the subaddress is undefined for the given media or\n             unused, this is a zero length string.')
dialCtlPeerCfgClosedUserGroup = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 7), DisplayString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgClosedUserGroup.setDescription('Closed User Group at which the peer will be called.\n             If the Closed User Group is undefined for the given media\n             or unused, this is a zero length string.')
dialCtlPeerCfgSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgSpeed.setDescription('The desired information transfer speed in bits/second\n             when calling this peer.\n             The detailed media specific information, e.g. information\n             type and information transfer rate for ISDN circuits,\n             has to be extracted from this object.\n             If the transfer speed to be used is unknown or the default\n             speed for this type of interfaces, the value of this object\n             may be zero.')
dialCtlPeerCfgInfoType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))).clone(namedValues=NamedValues(('other', 1), ('speech', 2), ('unrestrictedDigital', 3), ('unrestrictedDigital56', 4), ('restrictedDigital', 5), ('audio31', 6), ('audio7', 7), ('video', 8), ('packetSwitched', 9), ('fax', 10))).clone('other')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgInfoType.setDescription('The Information Transfer Capability to be used when\n             calling this peer.\n\n             speech(2) refers to a non-data connection, whereas\n             audio31(6) and audio7(7) refer to data mode\n             connections.')
dialCtlPeerCfgPermission = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('originate', 1), ('answer', 2), ('both', 3), ('callback', 4), ('none', 5))).clone('both')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgPermission.setDescription("Applicable permissions. callback(4) either rejects the\n             call and then calls back, or uses the 'Reverse charging'\n             information element if it is available.\n             Note that callback(4) is supposed to control charging, not\n             security, and applies to callback prior to accepting a\n             call. Callback for security reasons can be handled using\n             PPP callback.")
dialCtlPeerCfgInactivityTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgInactivityTimer.setDescription('The connection will be automatically disconnected\n             if no longer carrying useful data for a time\n             period, in seconds, specified in this object.\n             Useful data in this context refers to forwarding\n             packets, including routing information; it\n             excludes the encapsulator maintenance frames.\n             A value of zero means the connection will not be\n             automatically taken down due to inactivity,\n             which implies that it is a dedicated circuit.')
dialCtlPeerCfgMinDuration = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgMinDuration.setDescription('Minimum duration of a call in seconds, starting from the\n             time the call is connected until the call is disconnected.\n             This is to accomplish the fact that in most countries\n             charging applies to units of time, which should be matched\n             as closely as possible.')
dialCtlPeerCfgMaxDuration = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgMaxDuration.setDescription("Maximum call duration in seconds. Zero means 'unlimited'.")
dialCtlPeerCfgCarrierDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgCarrierDelay.setDescription('The call timeout time in seconds. The default value\n             of zero means that the call timeout as specified for\n             the media in question will apply.')
dialCtlPeerCfgCallRetries = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgCallRetries.setDescription('The number of calls to a non-responding address\n             that may be made. A retry count of zero means\n             there is no bound. The intent is to bound\n             the number of successive calls to an address\n             which is inaccessible, or which refuses those calls.\n\n             Some countries regulate the number of call retries\n             to a given peer that can be made.')
dialCtlPeerCfgRetryDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgRetryDelay.setDescription('The time in seconds between call retries if a peer\n             cannot be reached.\n             A value of zero means that call retries may be done\n             without any delay.')
dialCtlPeerCfgFailureDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 17), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgFailureDelay.setDescription('The time in seconds after which call attempts are\n             to be placed again after a peer has been noticed\n             to be unreachable, i.e. after dialCtlPeerCfgCallRetries\n             unsuccessful call attempts.\n             A value of zero means that a peer will not be called\n             again after dialCtlPeerCfgCallRetries unsuccessful call\n             attempts.')
dialCtlPeerCfgTrapEnable = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 18), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2))).clone('disabled')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgTrapEnable.setDescription('This object indicates whether dialCtlPeerCallInformation\n             and dialCtlPeerCallSetup traps should be generated for\n             this peer.')
dialCtlPeerCfgStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 1, 1, 19), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dialCtlPeerCfgStatus.setDescription('Status of one row in this table.')
dialCtlPeerStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2))
if mibBuilder.loadTexts:
    dialCtlPeerStatsTable.setDescription('Statistics information for each peer entry.\n             There will be one entry in this table for each entry\n             in the dialCtlPeerCfgTable.')
dialCtlPeerStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1))
dialCtlPeerCfgEntry.registerAugmentions(('DIAL-CONTROL-MIB', 'dialCtlPeerStatsEntry'))
dialCtlPeerStatsEntry.setIndexNames(*dialCtlPeerCfgEntry.getIndexNames())
if mibBuilder.loadTexts:
    dialCtlPeerStatsEntry.setDescription('Statistics information for a single Peer. This entry\n             is effectively permanent, and contains information\n             describing the last call attempt as well as supplying\n             statistical information.')
dialCtlPeerStatsConnectTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 1), AbsoluteCounter32()).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsConnectTime.setDescription('Accumulated connect time to the peer since system startup.\n             This is the total connect time, i.e. the connect time\n             for outgoing calls plus the time for incoming calls.')
dialCtlPeerStatsChargedUnits = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 2), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsChargedUnits.setDescription("The total number of charging units applying to this\n             peer since system startup.\n             Only the charging units applying to the local interface,\n             i.e. for originated calls or for calls with 'Reverse\n             charging' being active, will be counted here.")
dialCtlPeerStatsSuccessCalls = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 3), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsSuccessCalls.setDescription('Number of completed calls to this peer.')
dialCtlPeerStatsFailCalls = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 4), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsFailCalls.setDescription('Number of failed call attempts to this peer since system\n             startup.')
dialCtlPeerStatsAcceptCalls = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 5), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsAcceptCalls.setDescription('Number of calls from this peer accepted since system\n             startup.')
dialCtlPeerStatsRefuseCalls = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 6), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsRefuseCalls.setDescription('Number of calls from this peer refused since system\n             startup.')
dialCtlPeerStatsLastDisconnectCause = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 7), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 4))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsLastDisconnectCause.setDescription('The encoded network cause value associated with the last\n             call.\n             This object will be updated whenever a call is started\n             or cleared.\n             The value of this object will depend on the interface type\n             as well as on the protocol and protocol version being\n             used on this interface. Some references for possible cause\n             values are given below.')
dialCtlPeerStatsLastDisconnectText = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 8), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsLastDisconnectText.setDescription('ASCII text describing the reason for the last call\n             termination.\n\n             This object exists because it would be impossible for\n             a management station to store all possible cause values\n             for all types of interfaces. It should be used only if\n             a management station is unable to decode the value of\n             dialCtlPeerStatsLastDisconnectCause.\n\n             This object will be updated whenever a call is started\n             or cleared.')
dialCtlPeerStatsLastSetupTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 2, 2, 1, 9), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dialCtlPeerStatsLastSetupTime.setDescription('The value of sysUpTime when the last call to this peer\n             was started.\n             For ISDN media, this will be the time when the setup\n             message was received from or sent to the network.\n             This object will be updated whenever a call is started\n             or cleared.')
callActive = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 1, 3))
callActiveTable = MibTable((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1))
if mibBuilder.loadTexts:
    callActiveTable.setDescription('A table containing information about active\n             calls to a specific destination.')
callActiveEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1)).setIndexNames((0, 'DIAL-CONTROL-MIB', 'callActiveSetupTime'), (0, 'DIAL-CONTROL-MIB', 'callActiveIndex'))
if mibBuilder.loadTexts:
    callActiveEntry.setDescription('The information regarding a single active Connection.\n             An entry in this table will be created when a call is\n             started. An entry in this table will be deleted when\n             an active call clears.')
callActiveSetupTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 1), TimeStamp())
if mibBuilder.loadTexts:
    callActiveSetupTime.setDescription('The value of sysUpTime when the call associated to this\n             entry was started. This will be useful for an NMS to\n             retrieve all calls after a specific time. Also, this object\n             can be useful in finding large delays between the time the\n             call was started and the time the call was connected.\n             For ISDN media, this will be the time when the setup\n             message was received from or sent to the network.')
callActiveIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    callActiveIndex.setDescription('Small index variable to distinguish calls that start in\n             the same hundredth of a second.')
callActivePeerAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 3), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActivePeerAddress.setDescription('The number this call is connected to. If the number is\n             not available, then it will have a length of zero.')
callActivePeerSubAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 4), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActivePeerSubAddress.setDescription('The subaddress this call is connected to. If the subaddress\n             is undefined or not available, this will be a zero length\n             string.')
callActivePeerId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActivePeerId.setDescription('This is the Id value of the peer table entry\n             to which this call was made. If a peer table entry\n             for this call does not exist or is unknown, the value\n             of this object will be zero.')
callActivePeerIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActivePeerIfIndex.setDescription('This is the ifIndex value of the peer table entry\n             to which this call was made. If a peer table entry\n             for this call does not exist or is unknown, the value\n             of this object will be zero.')
callActiveLogicalIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 7), InterfaceIndexOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveLogicalIfIndex.setDescription('This is the ifIndex value of the logical interface through\n             which this call was made. For ISDN media, this would be\n             the ifIndex of the B channel which was used for this call.\n             If the ifIndex value is unknown, the value of this object\n             will be zero.')
callActiveConnectTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 8), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveConnectTime.setDescription('The value of sysUpTime when the call was connected.\n             If the call is not connected, this object will have a\n             value of zero.')
callActiveCallState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('unknown', 1), ('connecting', 2), ('connected', 3), ('active', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveCallState.setDescription('The current call state.\n             unknown(1)     - The call state is unknown.\n             connecting(2)  - A connection attempt (outgoing call)\n                              is being made.\n             connected(3)   - An incoming call is in the process\n                              of validation.\n             active(4)      - The call is active.\n            ')
callActiveCallOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('originate', 1), ('answer', 2), ('callback', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveCallOrigin.setDescription('The call origin.')
callActiveChargedUnits = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 11), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveChargedUnits.setDescription('The number of charged units for this connection.\n             For incoming calls or if charging information is\n             not supplied by the switch, the value of this object\n             will be zero.')
callActiveInfoType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))).clone(namedValues=NamedValues(('other', 1), ('speech', 2), ('unrestrictedDigital', 3), ('unrestrictedDigital56', 4), ('restrictedDigital', 5), ('audio31', 6), ('audio7', 7), ('video', 8), ('packetSwitched', 9), ('fax', 10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveInfoType.setDescription('The information type for this call.')
callActiveTransmitPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 13), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveTransmitPackets.setDescription('The number of packets which were transmitted for this\n             call.')
callActiveTransmitBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 14), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveTransmitBytes.setDescription('The number of bytes which were transmitted for this\n             call.')
callActiveReceivePackets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 15), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveReceivePackets.setDescription('The number of packets which were received for this\n             call.')
callActiveReceiveBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 3, 1, 1, 16), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callActiveReceiveBytes.setDescription('The number of bytes which were received for this call.')
callHistory = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 1, 4))
callHistoryTableMaxLength = MibScalar((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    callHistoryTableMaxLength.setDescription('The upper limit on the number of entries that the\n             callHistoryTable may contain.  A value of 0\n             will prevent any history from being retained. When\n             this table is full, the oldest entry will be deleted\n             and the new one will be created.')
callHistoryRetainTimer = MibScalar((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setUnits('minutes').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    callHistoryRetainTimer.setDescription('The minimum amount of time that an callHistoryEntry\n             will be maintained before being deleted. A value of\n             0 will prevent any history from being retained in the\n             callHistoryTable, but will neither prevent callCompletion\n             traps being generated nor affect other tables.')
callHistoryTable = MibTable((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3))
if mibBuilder.loadTexts:
    callHistoryTable.setDescription('A table containing information about specific\n             calls to a specific destination.')
callHistoryEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1)).setIndexNames((0, 'DIAL-CONTROL-MIB', 'callActiveSetupTime'), (0, 'DIAL-CONTROL-MIB', 'callActiveIndex'))
if mibBuilder.loadTexts:
    callHistoryEntry.setDescription('The information regarding a single Connection.')
callHistoryPeerAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 1), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryPeerAddress.setDescription('The number this call was connected to. If the number is\n             not available, then it will have a length of zero.')
callHistoryPeerSubAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryPeerSubAddress.setDescription('The subaddress this call was connected to. If the subaddress\n             is undefined or not available, this will be a zero length\n             string.')
callHistoryPeerId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryPeerId.setDescription('This is the Id value of the peer table entry\n             to which this call was made. If a peer table entry\n             for this call does not exist, the value of this object\n             will be zero.')
callHistoryPeerIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryPeerIfIndex.setDescription('This is the ifIndex value of the peer table entry\n             to which this call was made. If a peer table entry\n             for this call does not exist, the value of this object\n             will be zero.')
callHistoryLogicalIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 5), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryLogicalIfIndex.setDescription('This is the ifIndex value of the logical interface through\n             which this call was made. For ISDN media, this would be\n             the ifIndex of the B channel which was used for this call.')
callHistoryDisconnectCause = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 4))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryDisconnectCause.setDescription('The encoded network cause value associated with this call.\n\n             The value of this object will depend on the interface type\n             as well as on the protocol and protocol version being\n             used on this interface. Some references for possible cause\n             values are given below.')
callHistoryDisconnectText = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 7), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryDisconnectText.setDescription('ASCII text describing the reason for call termination.\n\n             This object exists because it would be impossible for\n             a management station to store all possible cause values\n             for all types of interfaces. It should be used only if\n             a management station is unable to decode the value of\n             dialCtlPeerStatsLastDisconnectCause.')
callHistoryConnectTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 8), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryConnectTime.setDescription('The value of sysUpTime when the call was connected.')
callHistoryDisconnectTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 9), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryDisconnectTime.setDescription('The value of sysUpTime when the call was disconnected.')
callHistoryCallOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('originate', 1), ('answer', 2), ('callback', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryCallOrigin.setDescription('The call origin.')
callHistoryChargedUnits = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 11), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryChargedUnits.setDescription('The number of charged units for this connection.\n             For incoming calls or if charging information is\n             not supplied by the switch, the value of this object\n             will be zero.')
callHistoryInfoType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))).clone(namedValues=NamedValues(('other', 1), ('speech', 2), ('unrestrictedDigital', 3), ('unrestrictedDigital56', 4), ('restrictedDigital', 5), ('audio31', 6), ('audio7', 7), ('video', 8), ('packetSwitched', 9), ('fax', 10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryInfoType.setDescription('The information type for this call.')
callHistoryTransmitPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 13), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryTransmitPackets.setDescription('The number of packets which were transmitted while this\n             call was active.')
callHistoryTransmitBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 14), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryTransmitBytes.setDescription('The number of bytes which were transmitted while this\n             call was active.')
callHistoryReceivePackets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 15), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryReceivePackets.setDescription('The number of packets which were received while this\n             call was active.')
callHistoryReceiveBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 21, 1, 4, 3, 1, 16), AbsoluteCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    callHistoryReceiveBytes.setDescription('The number of bytes which were received while this\n             call was active.')
dialControlMibTrapPrefix = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 2))
dialControlMibTraps = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 2, 0))
dialCtlPeerCallInformation = NotificationType((1, 3, 6, 1, 2, 1, 10, 21, 2, 0, 1)).setObjects(*(('DIAL-CONTROL-MIB', 'callHistoryPeerId'), ('DIAL-CONTROL-MIB', 'callHistoryPeerIfIndex'), ('DIAL-CONTROL-MIB', 'callHistoryLogicalIfIndex'), ('DIAL-CONTROL-MIB', 'ifOperStatus'), ('DIAL-CONTROL-MIB', 'callHistoryPeerAddress'), ('DIAL-CONTROL-MIB', 'callHistoryPeerSubAddress'), ('DIAL-CONTROL-MIB', 'callHistoryDisconnectCause'), ('DIAL-CONTROL-MIB', 'callHistoryConnectTime'), ('DIAL-CONTROL-MIB', 'callHistoryDisconnectTime'), ('DIAL-CONTROL-MIB', 'callHistoryInfoType'), ('DIAL-CONTROL-MIB', 'callHistoryCallOrigin')))
if mibBuilder.loadTexts:
    dialCtlPeerCallInformation.setDescription('This trap/inform is sent to the manager whenever\n             a successful call clears, or a failed call attempt\n             is determined to have ultimately failed. In the\n             event that call retry is active, then this is after\n             all retry attempts have failed. However, only one such\n             trap is sent in between successful call attempts;\n             subsequent call attempts result in no trap.\n             ifOperStatus will return the operational status of the\n             virtual interface associated with the peer to whom\n             this call was made to.')
dialCtlPeerCallSetup = NotificationType((1, 3, 6, 1, 2, 1, 10, 21, 2, 0, 2)).setObjects(*(('DIAL-CONTROL-MIB', 'callActivePeerId'), ('DIAL-CONTROL-MIB', 'callActivePeerIfIndex'), ('DIAL-CONTROL-MIB', 'callActiveLogicalIfIndex'), ('DIAL-CONTROL-MIB', 'ifOperStatus'), ('DIAL-CONTROL-MIB', 'callActivePeerAddress'), ('DIAL-CONTROL-MIB', 'callActivePeerSubAddress'), ('DIAL-CONTROL-MIB', 'callActiveInfoType'), ('DIAL-CONTROL-MIB', 'callActiveCallOrigin')))
if mibBuilder.loadTexts:
    dialCtlPeerCallSetup.setDescription('This trap/inform is sent to the manager whenever\n             a call setup message is received or sent.\n             ifOperStatus will return the operational status of the\n             virtual interface associated with the peer to whom\n             this call was made to.')
dialControlMibConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 3))
dialControlMibCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 3, 1))
dialControlMibGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 21, 3, 2))
dialControlMibCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 21, 3, 1, 1)).setObjects(*(('DIAL-CONTROL-MIB', 'dialControlGroup'), ('DIAL-CONTROL-MIB', 'callActiveGroup'), ('DIAL-CONTROL-MIB', 'callHistoryGroup')))
if mibBuilder.loadTexts:
    dialControlMibCompliance.setDescription('The compliance statement for entities which\n             implement the DIAL CONTROL MIB')
dialControlGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 21, 3, 2, 1)).setObjects(*(('DIAL-CONTROL-MIB', 'dialCtlAcceptMode'), ('DIAL-CONTROL-MIB', 'dialCtlTrapEnable'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgIfType'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgLowerIf'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgOriginateAddress'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgAnswerAddress'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgSubAddress'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgClosedUserGroup'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgSpeed'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgInfoType'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgPermission'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgInactivityTimer'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgMinDuration'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgMaxDuration'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgCarrierDelay'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgCallRetries'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgRetryDelay'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgFailureDelay'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgTrapEnable'), ('DIAL-CONTROL-MIB', 'dialCtlPeerCfgStatus'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsConnectTime'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsChargedUnits'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsSuccessCalls'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsFailCalls'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsAcceptCalls'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsRefuseCalls'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsLastDisconnectCause'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsLastDisconnectText'), ('DIAL-CONTROL-MIB', 'dialCtlPeerStatsLastSetupTime')))
if mibBuilder.loadTexts:
    dialControlGroup.setDescription('A collection of objects providing the DIAL CONTROL\n             capability.')
callActiveGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 21, 3, 2, 2)).setObjects(*(('DIAL-CONTROL-MIB', 'callActivePeerAddress'), ('DIAL-CONTROL-MIB', 'callActivePeerSubAddress'), ('DIAL-CONTROL-MIB', 'callActivePeerId'), ('DIAL-CONTROL-MIB', 'callActivePeerIfIndex'), ('DIAL-CONTROL-MIB', 'callActiveLogicalIfIndex'), ('DIAL-CONTROL-MIB', 'callActiveConnectTime'), ('DIAL-CONTROL-MIB', 'callActiveCallState'), ('DIAL-CONTROL-MIB', 'callActiveCallOrigin'), ('DIAL-CONTROL-MIB', 'callActiveChargedUnits'), ('DIAL-CONTROL-MIB', 'callActiveInfoType'), ('DIAL-CONTROL-MIB', 'callActiveTransmitPackets'), ('DIAL-CONTROL-MIB', 'callActiveTransmitBytes'), ('DIAL-CONTROL-MIB', 'callActiveReceivePackets'), ('DIAL-CONTROL-MIB', 'callActiveReceiveBytes')))
if mibBuilder.loadTexts:
    callActiveGroup.setDescription('A collection of objects providing the active call\n             capability.')
callHistoryGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 21, 3, 2, 3)).setObjects(*(('DIAL-CONTROL-MIB', 'callHistoryTableMaxLength'), ('DIAL-CONTROL-MIB', 'callHistoryRetainTimer'), ('DIAL-CONTROL-MIB', 'callHistoryPeerAddress'), ('DIAL-CONTROL-MIB', 'callHistoryPeerSubAddress'), ('DIAL-CONTROL-MIB', 'callHistoryPeerId'), ('DIAL-CONTROL-MIB', 'callHistoryPeerIfIndex'), ('DIAL-CONTROL-MIB', 'callHistoryLogicalIfIndex'), ('DIAL-CONTROL-MIB', 'callHistoryDisconnectCause'), ('DIAL-CONTROL-MIB', 'callHistoryDisconnectText'), ('DIAL-CONTROL-MIB', 'callHistoryConnectTime'), ('DIAL-CONTROL-MIB', 'callHistoryDisconnectTime'), ('DIAL-CONTROL-MIB', 'callHistoryCallOrigin'), ('DIAL-CONTROL-MIB', 'callHistoryChargedUnits'), ('DIAL-CONTROL-MIB', 'callHistoryInfoType'), ('DIAL-CONTROL-MIB', 'callHistoryTransmitPackets'), ('DIAL-CONTROL-MIB', 'callHistoryTransmitBytes'), ('DIAL-CONTROL-MIB', 'callHistoryReceivePackets'), ('DIAL-CONTROL-MIB', 'callHistoryReceiveBytes')))
if mibBuilder.loadTexts:
    callHistoryGroup.setDescription('A collection of objects providing the Call History\n             capability.')
mibBuilder.exportSymbols('DIAL-CONTROL-MIB', dialCtlPeerStatsAcceptCalls=dialCtlPeerStatsAcceptCalls, dialCtlPeerStatsSuccessCalls=dialCtlPeerStatsSuccessCalls, callActiveGroup=callActiveGroup, callHistoryConnectTime=callHistoryConnectTime, dialCtlPeer=dialCtlPeer, callHistoryTransmitBytes=callHistoryTransmitBytes, callHistoryDisconnectCause=callHistoryDisconnectCause, dialCtlPeerCfgEntry=dialCtlPeerCfgEntry, dialCtlPeerStatsLastDisconnectCause=dialCtlPeerStatsLastDisconnectCause, dialCtlPeerCallSetup=dialCtlPeerCallSetup, callHistoryRetainTimer=callHistoryRetainTimer, callActiveSetupTime=callActiveSetupTime, callHistory=callHistory, dialCtlPeerStatsLastDisconnectText=dialCtlPeerStatsLastDisconnectText, callActiveReceiveBytes=callActiveReceiveBytes, dialCtlPeerStatsLastSetupTime=dialCtlPeerStatsLastSetupTime, callActivePeerAddress=callActivePeerAddress, callActiveInfoType=callActiveInfoType, dialCtlPeerCfgIfType=dialCtlPeerCfgIfType, dialCtlConfiguration=dialCtlConfiguration, dialControlMibTraps=dialControlMibTraps, callHistoryTransmitPackets=callHistoryTransmitPackets, dialCtlPeerCfgInfoType=dialCtlPeerCfgInfoType, dialCtlPeerStatsRefuseCalls=dialCtlPeerStatsRefuseCalls, dialCtlPeerStatsConnectTime=dialCtlPeerStatsConnectTime, callActivePeerId=callActivePeerId, callHistoryChargedUnits=callHistoryChargedUnits, callActiveLogicalIfIndex=callActiveLogicalIfIndex, callHistoryTable=callHistoryTable, dialCtlPeerCfgAnswerAddress=dialCtlPeerCfgAnswerAddress, dialCtlPeerCfgClosedUserGroup=dialCtlPeerCfgClosedUserGroup, callActiveIndex=callActiveIndex, callActiveEntry=callActiveEntry, callActivePeerIfIndex=callActivePeerIfIndex, callHistoryDisconnectTime=callHistoryDisconnectTime, callActiveReceivePackets=callActiveReceivePackets, dialControlMibObjects=dialControlMibObjects, callHistoryTableMaxLength=callHistoryTableMaxLength, callActiveCallOrigin=callActiveCallOrigin, dialControlGroup=dialControlGroup, callHistoryReceiveBytes=callHistoryReceiveBytes, dialCtlPeerCfgInactivityTimer=dialCtlPeerCfgInactivityTimer, PYSNMP_MODULE_ID=dialControlMib, dialCtlPeerCfgSpeed=dialCtlPeerCfgSpeed, dialCtlTrapEnable=dialCtlTrapEnable, callHistoryPeerSubAddress=callHistoryPeerSubAddress, callHistoryPeerId=callHistoryPeerId, callActiveConnectTime=callActiveConnectTime, dialCtlPeerStatsFailCalls=dialCtlPeerStatsFailCalls, dialCtlPeerCfgId=dialCtlPeerCfgId, dialCtlPeerCfgCallRetries=dialCtlPeerCfgCallRetries, callActive=callActive, dialCtlPeerStatsTable=dialCtlPeerStatsTable, callHistoryPeerAddress=callHistoryPeerAddress, dialCtlPeerCfgRetryDelay=dialCtlPeerCfgRetryDelay, callHistoryDisconnectText=callHistoryDisconnectText, dialCtlPeerCfgLowerIf=dialCtlPeerCfgLowerIf, callActiveTable=callActiveTable, dialCtlPeerCfgMinDuration=dialCtlPeerCfgMinDuration, dialCtlPeerCfgCarrierDelay=dialCtlPeerCfgCarrierDelay, dialControlMibTrapPrefix=dialControlMibTrapPrefix, dialControlMibCompliance=dialControlMibCompliance, dialCtlPeerCfgSubAddress=dialCtlPeerCfgSubAddress, callHistoryReceivePackets=callHistoryReceivePackets, callActiveTransmitBytes=callActiveTransmitBytes, callHistoryLogicalIfIndex=callHistoryLogicalIfIndex, callActiveChargedUnits=callActiveChargedUnits, callActiveTransmitPackets=callActiveTransmitPackets, callHistoryGroup=callHistoryGroup, callHistoryCallOrigin=callHistoryCallOrigin, dialCtlPeerCfgMaxDuration=dialCtlPeerCfgMaxDuration, dialControlMib=dialControlMib, dialCtlPeerCallInformation=dialCtlPeerCallInformation, AbsoluteCounter32=AbsoluteCounter32, callHistoryEntry=callHistoryEntry, callHistoryInfoType=callHistoryInfoType, dialControlMibCompliances=dialControlMibCompliances, callHistoryPeerIfIndex=callHistoryPeerIfIndex, callActiveCallState=callActiveCallState, dialControlMibConformance=dialControlMibConformance, dialCtlPeerCfgFailureDelay=dialCtlPeerCfgFailureDelay, dialCtlPeerStatsEntry=dialCtlPeerStatsEntry, dialCtlPeerStatsChargedUnits=dialCtlPeerStatsChargedUnits, callActivePeerSubAddress=callActivePeerSubAddress, dialCtlAcceptMode=dialCtlAcceptMode, dialCtlPeerCfgTrapEnable=dialCtlPeerCfgTrapEnable, dialCtlPeerCfgTable=dialCtlPeerCfgTable, dialCtlPeerCfgStatus=dialCtlPeerCfgStatus, dialCtlPeerCfgOriginateAddress=dialCtlPeerCfgOriginateAddress, dialCtlPeerCfgPermission=dialCtlPeerCfgPermission, dialControlMibGroups=dialControlMibGroups)