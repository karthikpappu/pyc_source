# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/RFC1285-MIB.py
# Compiled at: 2016-02-13 18:26:09
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ConstraintsUnion', 'ValueRangeConstraint')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(iso, Bits, NotificationType, ModuleIdentity, ObjectIdentity, IpAddress, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, transmission, Integer32, Gauge32, Counter32, TimeTicks, Counter64, MibIdentifier) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'Bits', 'NotificationType', 'ModuleIdentity', 'ObjectIdentity', 'IpAddress', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Unsigned32', 'transmission', 'Integer32', 'Gauge32', 'Counter32', 'TimeTicks', 'Counter64', 'MibIdentifier')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
fddi = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15))

class FddiTime(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 2147483647)


class FddiResourceId(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 65535)


class FddiSMTStationIdType(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(8, 8)
    fixedLength = 8


class FddiMACLongAddressType(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(6, 6)
    fixedLength = 6


snmpFddiSMT = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 1))
snmpFddiMAC = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 2))
snmpFddiPATH = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 3))
snmpFddiPORT = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 4))
snmpFddiATTACHMENT = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 5))
snmpFddiChipSets = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 6))
snmpFddiSMTNumber = MibScalar((1, 3, 6, 1, 2, 1, 10, 15, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTNumber.setDescription("The number of SMT implementations (regardless of\n                      their current state) on this network management\n                      application entity.  The value for this variable\n                      must remain constant at least from one re-\n                      initialization of the entity's network management\n                      system to the next re-initialization.")
snmpFddiSMTTable = MibTable((1, 3, 6, 1, 2, 1, 10, 15, 1, 2))
if mibBuilder.loadTexts:
    snmpFddiSMTTable.setDescription('A list of SMT entries.  The number of entries is\n                      given by  the value of snmpFddiSMTNumber.')
snmpFddiSMTEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1)).setIndexNames((0,
                                                                                   'RFC1285-MIB',
                                                                                   'snmpFddiSMTIndex'))
if mibBuilder.loadTexts:
    snmpFddiSMTEntry.setDescription('An SMT entry containing information common to a\n                      given SMT.')
snmpFddiSMTIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTIndex.setDescription("A unique value for each SMT.  Its value ranges\n                      between 1 and the value of snmpFddiSMTNumber.  The\n                      value for each SMT must remain constant at least\n                      from one re-initialization of the entity's network\n                      management system to the next re-initialization.")
snmpFddiSMTStationId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 2), FddiSMTStationIdType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTStationId.setDescription('Uniquely identifies an FDDI station.')
snmpFddiSMTOpVersionId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiSMTOpVersionId.setDescription('The version that this station is using for its\n                      operation (refer to ANSI 7.1.2.2).')
snmpFddiSMTHiVersionId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTHiVersionId.setDescription('The highest version of SMT that this station\n                      supports (refer to ANSI 7.1.2.2).')
snmpFddiSMTLoVersionId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTLoVersionId.setDescription('The lowest version of SMT that this station\n                      supports (refer to ANSI 7.1.2.2).')
snmpFddiSMTMACCt = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTMACCt.setDescription('The number of MACs in the station or\n                      concentrator.')
snmpFddiSMTNonMasterCt = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTNonMasterCt.setDescription('The number of Non Master PORTs (A, B, or S PORTs)\n                      in the station or concentrator.')
snmpFddiSMTMasterCt = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTMasterCt.setDescription('The number of Master PORTs in a node.  If the\n                      node is not a concentrator, the value is zero.')
snmpFddiSMTPathsAvailable = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTPathsAvailable.setDescription('A value that indicates the PATH types available\n                      in the station.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each type of PATH that\n                      this node has available, 2 raised to a power is\n                      added to the sum.  The powers are according to the\n                      following table:\n\n                               Path   Power\n                            Primary   0\n                          Secondary   1\n                              Local   2\n\n                      For example, a station having Primary and Local\n                      PATHs available would have a value of 5 (2**0 +\n                      2**2).')
snmpFddiSMTConfigCapabilities = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1,
                                                10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTConfigCapabilities.setDescription("A value that indicates capabilities that are\n                      present in the node.  If 'holdAvailable' is\n                      present, this indicates support of the optional\n                      Hold Function (refer to ANSI SMT 9.4.3.2).  If\n                      'CF-Wrap-AB' is present, this indicates that the\n                      WRAP_AB state is forced.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each of the configuration\n                      policies currently enforced on the node, 2 raised\n                      to a power is added to the sum.  The powers are\n                      according to the following table:\n\n                                 Policy   Power\n                          holdAvailable   0\n                             CF-Wrap-AB   1 ")
snmpFddiSMTConfigPolicy = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiSMTConfigPolicy.setDescription("A value that indicates the configuration policies\n                      currently enforced in the node (refer to ANSI SMT\n                      9.4.3.2).  The 'configurationHold' policy refers\n                      to the Hold flag, and should not be present only\n                      if the Hold function is supported.  The 'CF-Wrap-\n                      AB' policy refers to the CF_Wrap_AB flag.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each of the configuration\n                      policies currently enforced on the node, 2 raised\n                      to a power is added to the sum.  The powers are\n                      according to the following table:\n\n                                     Policy   Power\n                          configurationHold   0\n                                 CF-Wrap-AB   1 ")
snmpFddiSMTConnectionPolicy = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiSMTConnectionPolicy.setDescription("A value that indicates the connection policies\n                      enforced at the station.  A station sets the\n                      corresponding policy for each of the connection\n                      types that it rejects.  The letter designations, X\n                      and Y, in the 'rejectX-Y' names have the following\n                      significance:  X represents the PC-Type of the\n                      local PORT and Y represents a PC-Neighbor in the\n                      evaluation of Connection-Policy (PC-Type, PC-\n                      Neighbor) that is done to determine the setting of\n                      T-Val(3) in the PC-Signaling sequence (refer to\n                      ANSI Section 9.6.3).\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each of the connection\n                      policies currently enforced on the node, 2 raised\n                      to a power is added to the sum.  The powers are\n                      according to the following table:\n\n                             Policy   Power\n                          rejectA-A   0\n                          rejectA-B   1\n                          rejectA-S   2\n                          rejectA-M   3\n                          rejectB-A   4\n                          rejectB-B   5\n                          rejectB-S   6\n                          rejectB-M   7\n                          rejectS-A   8\n                          rejectS-B   9\n                          rejectS-S   10\n                          rejectS-M   11\n                          rejectM-A   12\n                          rejectM-B   13\n                          rejectM-S   14\n                          rejectM-M   15\n\n                      Implementors should note that the polarity of\n                      these bits is different in different places in an\n                      SMT system.  Implementors should take appropriate\n                      care.")
snmpFddiSMTTNotify = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(2, 30))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiSMTTNotify.setDescription('The timer used in the Neighbor Notification\n                      protocol, reported in seconds and ranging from 2\n                      to 30 seconds (refer to ANSI SMT 8.3.1).')
snmpFddiSMTStatusReporting = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                                   1), ('false',
                                                                                                                                                                                                        2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTStatusReporting.setDescription('Indicates whether the node implements the Status\n                      Reporting Protocol.  This object is included for\n                      compatibility with products that were designed\n                      prior to the adoption of this standard.')
snmpFddiSMTECMState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 15), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(('ec0',
                                                                                                                                                                                                              1), ('ec1',
                                                                                                                                                                                                                   2), ('ec2',
                                                                                                                                                                                                                        3), ('ec3',
                                                                                                                                                                                                                             4), ('ec4',
                                                                                                                                                                                                                                  5), ('ec5',
                                                                                                                                                                                                                                       6), ('ec6',
                                                                                                                                                                                                                                            7), ('ec7',
                                                                                                                                                                                                                                                 8)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTECMState.setDescription('Indicates the current state of the ECM state\n                      machine (refer to ANSI SMT 9.5.2).')
snmpFddiSMTCFState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 16), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('cf0',
                                                                                                                                                                                                       1), ('cf1',
                                                                                                                                                                                                            2), ('cf2',
                                                                                                                                                                                                                 3), ('cf3',
                                                                                                                                                                                                                      4), ('cf4',
                                                                                                                                                                                                                           5), ('cf5',
                                                                                                                                                                                                                                6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTCFState.setDescription('The attachment configuration for the station or\n                      concentrator (refer to ANSI SMT 9.7.4.3).')
snmpFddiSMTHoldState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 17), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('not-implemented',
                                                                                                                                                                                                   1), ('not-holding',
                                                                                                                                                                                                        2), ('holding-prm',
                                                                                                                                                                                                             3), ('holding-sec',
                                                                                                                                                                                                                  4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTHoldState.setDescription("This value indicates the current state of the\n                      Hold function.  The values are determined as\n                      follows:  'holding-prm' is set if the primary ring\n                      is operational and the Recovery Enable Flag is\n                      clear (NOT NO_Flag(primary) AND NOT RE_Flag).  is\n                      set if the secondary ring is operational and the\n                      Recovery Enable Flag is clear (NOT\n                      NO_Flag(secondary) AND NOT RE_Flag).  Ref 9.4.3.\n                      and 10.3.1.  the primary or secondary, i.e., the\n                      Recovery Enable, RE_Flag, is set.")
snmpFddiSMTRemoteDisconnectFlag = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1,
                                                  18), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                     1), ('false',
                                                                                                                                                                          2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiSMTRemoteDisconnectFlag.setDescription('A flag indicating that the station was remotely\n                      disconnected from the network.  A station requires\n                      a Connect Action (SM_CM_CONNECT.request (Connect))\n                      to rejoin and clear the flag (refer to ANSI\n                      6.4.5.2).')
snmpFddiSMTStationAction = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 1, 2, 1, 19), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                                          1), ('connect',
                                                                                                                                                                                                               2), ('disconnect',
                                                                                                                                                                                                                    3), ('path-Test',
                                                                                                                                                                                                                         4), ('self-Test',
                                                                                                                                                                                                                              5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiSMTStationAction.setDescription('This object, when read, always returns a value of\n                      other(1).  The behavior of setting this variable\n                      to each of the acceptable values is as follows:\n\n                      Other:          Results in a badValue error.\n\n                      Connect:        Generates an\n                      SM_CM_Connect.request(connect) signal to CMT\n                      indicating that the ECM State machine is to begin\n                      a connection sequence.  The\n                      fddiSMTRemoteDisconnectFlag is cleared on the\n                      setting of this variable to 1.  See ANSI Ref\n                      9.3.1.1.\n\n                      Disconnect:     Generates an\n                      SM_CM_Connect.request(disconnect) signal to ECM\n                      and sets the fddiSMTRemoteDisconnectFlag.  See\n                      ANSI Ref 9.3.1.1.\n\n                      Path-Test:      Initiates a station path test.\n                      The Path_Test variable (See ANSI Ref. 9.4.1) is\n                      set to Testing.  The results of this action are\n                      not specified in this standard.\n\n                      Self-Test:      Initiates a station self test.\n                      The results of this action are not specified in\n                      this standard.\n\n                      Attempts to set this object to all other values\n                      results in a badValue error.  Agents may elect to\n                      return a badValue error on attempts to set this\n                      variable to path-Test(4) or self-Test(5).')
snmpFddiMACNumber = MibScalar((1, 3, 6, 1, 2, 1, 10, 15, 2, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACNumber.setDescription("The total number of MAC implementations (across\n                      all SMTs) on this network management application\n                      entity.  The value for this variable must remain\n                      constant at least from one re-initialization of\n                      the entity's network management system to the next\n                      re-initialization.")
snmpFddiMACTable = MibTable((1, 3, 6, 1, 2, 1, 10, 15, 2, 2))
if mibBuilder.loadTexts:
    snmpFddiMACTable.setDescription('A list of MAC entries.  The number of entries is\n                      given by the value of snmpFddiMACNumber.')
snmpFddiMACEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1)).setIndexNames((0,
                                                                                   'RFC1285-MIB',
                                                                                   'snmpFddiMACSMTIndex'), (0,
                                                                                                            'RFC1285-MIB',
                                                                                                            'snmpFddiMACIndex'))
if mibBuilder.loadTexts:
    snmpFddiMACEntry.setDescription('A MAC entry containing information common to a\n                      given MAC.')
snmpFddiMACSMTIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACSMTIndex.setDescription('The value of the SMT index associated with this\n                      MAC.')
snmpFddiMACIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACIndex.setDescription("A unique value for each MAC on the managed\n                      entity.  The MAC identified by a particular value\n                      of this index is that identified by the same value\n                      of an ifIndex object instance.  That is, if a MAC\n                      is associated with the interface whose value of\n                      ifIndex in the Internet-Standard MIB is equal to\n                      5, then the value of snmpFddiMACIndex shall also\n                      equal 5.  The value for each MAC must remain\n                      constant at least from one re-initialization of\n                      the entity's network management system to the next\n                      re-initialization.")
snmpFddiMACFrameStatusCapabilities = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2,
                                                     1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1799))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACFrameStatusCapabilities.setDescription("A value that indicates the MAC's bridge and end-\n                      station capabilities for operating in a bridged\n                      FDDI network.\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each capability present,\n                      2 raised to a power is added to the sum.  The\n                      powers are according to the following table:\n\n\n                           Capability    Power\n                           FSC-Type0    0\n                           -- MAC repeats A/C indicators as received on\n                           -- copying with the intent to forward.\n\n                           FSC-Type1    1\n                           -- MAC sets C but not A on copying for\n                           -- forwarding.\n\n                           FSC-Type2    2\n                           -- MAC resets C and sets A on C set and\n                           -- A reset if the frame is not copied and the\n                           -- frame was addressed to this MAC\n\n                           FSC-Type0-programmable    8\n                           -- Type0 capability is programmable\n\n                           FSC-Type1-programmable    9\n                           -- Type1 capability is programmable\n\n                           FSC-Type2-programmable   10\n                           -- Type2 capability is programmable\n                      ")
snmpFddiMACTMaxGreatestLowerBound = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2,
                                                    1, 4), FddiTime()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiMACTMaxGreatestLowerBound.setDescription('The greatest lower bound of T_Max supported for\n                      this MAC.')
snmpFddiMACTVXGreatestLowerBound = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2,
                                                   1, 5), FddiTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACTVXGreatestLowerBound.setDescription('The greatest lower bound of TVX supported for\n                      this MAC.')
snmpFddiMACPathsAvailable = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACPathsAvailable.setDescription('A value that indicates the PATH types available\n                      for this MAC.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each type of PATH that\n                      this MAC has available, 2 raised to a power is\n                      added to the sum.  The powers are according to the\n                      following table:\n\n                               Path   Power\n                            Primary   0\n                          Secondary   1\n                              Local   2 ')
snmpFddiMACCurrentPath = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 4, 8, 16))).clone(namedValues=NamedValues(('unknown',
                                                                                                                                                                                                        1), ('primary',
                                                                                                                                                                                                             2), ('secondary',
                                                                                                                                                                                                                  4), ('local',
                                                                                                                                                                                                                       8), ('isolated',
                                                                                                                                                                                                                            16)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACCurrentPath.setDescription('Indicates the association of the MAC with a\n                      station PATH.')
snmpFddiMACUpstreamNbr = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 8), FddiMACLongAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACUpstreamNbr.setDescription("The MAC's upstream neighbor's long individual MAC\n                      address.  It may be determined by the Neighbor\n                      Information Frame protocol (refer to ANSI SMT\n                      7.2.1).  The value shall be reported as '00 00 00\n                      00 00 00' if it is unknown.")
snmpFddiMACOldUpstreamNbr = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 9), FddiMACLongAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACOldUpstreamNbr.setDescription("The previous value of the MAC's upstream\n                      neighbor's long individual MAC address.  It may be\n                      determined by the Neighbor Information Frame\n                      protocol (refer to ANSI SMT 7.2.1).  The value\n                      shall be reported as '00 00 00 00 00 00' if it is\n                      unknown.")
snmpFddiMACDupAddrTest = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                                  1), ('pass',
                                                                                                                                                                                                       2), ('fail',
                                                                                                                                                                                                            3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACDupAddrTest.setDescription('The Duplicate Address Test flag, Dup_Addr_Test\n                      (refer to ANSI 8.3.1).')
snmpFddiMACPathsRequested = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 11), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiMACPathsRequested.setDescription('A value that indicates PATH(s) desired for this\n                      MAC.\n\n                      The value is a sum which represents the individual\n                      PATHs that are desired.  This value initially\n                      takes the value zero, then for each type of PATH\n                      that this node is, 2 raised to a power is added to\n                      the sum.  The powers are according to the\n                      following table:\n\n                               Path   Power\n                            Primary   0\n                          Secondary   1\n                              Local   2\n                           Isolated   3\n\n                      The precedence order is primary, secondary, local,\n                      and then isolated if multiple PATHs are desired\n                      are set.')
snmpFddiMACDownstreamPORTType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1,
                                                12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('a',
                                                                                                                                                                            1), ('b',
                                                                                                                                                                                 2), ('s',
                                                                                                                                                                                      3), ('m',
                                                                                                                                                                                           4), ('unknown',
                                                                                                                                                                                                5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACDownstreamPORTType.setDescription('Indicates the PC-Type of the first port that is\n                      downstream of this MAC (the exit port).')
snmpFddiMACSMTAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 13), FddiMACLongAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACSMTAddress.setDescription('The 48 bit individual address of the MAC used for\n                      SMT frames.')
snmpFddiMACTReq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 14), FddiTime()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiMACTReq.setDescription('The value of T-Req (refer to ANSI MAC 2.2.1 and\n                      ANSI MAC 7.3.5.2).')
snmpFddiMACTNeg = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 15), FddiTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACTNeg.setDescription('The value of T-Neg (refer to ANSI MAC 2.2.1 and\n                      ANSI MAC 7.3.5.2).')
snmpFddiMACTMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 16), FddiTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACTMax.setDescription('The value of T-Max (refer to ANSI MAC 2.2.1 and\n                      ANSI MAC 7.3.5.2).')
snmpFddiMACTvxValue = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 17), FddiTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACTvxValue.setDescription('The value of TvxValue (refer to ANSI MAC 2.2.1\n                      and ANSI MAC 7.3.5.2).')
snmpFddiMACTMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 18), FddiTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACTMin.setDescription('The value of T-Min (refer to ANSI MAC 2.2.1 and\n                      ANSI MAC 7.3.5.2).')
snmpFddiMACCurrentFrameStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1,
                                                19), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiMACCurrentFrameStatus.setDescription("A value that indicates the MAC's operational\n                      frame status setting functionality.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each functionality\n                      present, 2 raised to a power is added to the sum.\n                      The powers are according to the following table:\n\n                          Functionality   Power\n                              FSC-Type0   0\n                              -- MAC repeats A/C indicators as received\n\n                              FSC-Type1   1\n                              -- MAC sets C but not A on copying for\n                              -- forwarding\n\n                              FSC-Type2   2\n                              -- MAC resets C and sets A on C set and A\n                              -- reset if frame is not copied\n                      ")
snmpFddiMACFrameCts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 20), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACFrameCts.setDescription('Frame_Ct (refer to ANSI MAC 2.2.1).')
snmpFddiMACErrorCts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 21), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACErrorCts.setDescription('Error_Ct (refer to ANSI MAC 2.2.1).')
snmpFddiMACLostCts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 22), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACLostCts.setDescription('Lost_Ct (refer to ANSI MAC 2.2.1).')
snmpFddiMACFrameErrorThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1,
                                                 23), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACFrameErrorThreshold.setDescription('A threshold for determining when a MAC Condition\n                      report should be generated.  The condition is true\n                      when the ratio, ((delta snmpFddiMACLostCt + delta\n                      snmpFddiMACErrorCt) / (delta snmpFddiMACFrameCt +\n                      delta snmpFddiMACLostCt)) x 2**16. exceeds the\n                      threshold.  It is used to determine when a station\n                      has an unacceptable frame error threshold.  The\n                      sampling algorithm is implementation dependent.\n                      Any attempt to set this variable to a value of\n                      less than one shall result in a badValue error.\n                      Those who are familiar with the SNMP management\n                      framework will recognize that thresholds are not\n                      in keeping with the SNMP philosophy.  However,\n                      this variable is supported by underlying SMT\n                      implementations already and maintaining this\n                      threshold should not pose an undue additional\n                      burden on SNMP agent implementors.')
snmpFddiMACFrameErrorRatio = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 24), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACFrameErrorRatio.setDescription('This attribute is the actual ratio, ((delta\n                      snmpFddiMACLostCt + delta snmpFddiMACErrorCt) /\n                      (delta snmpFddiMACFrameCt + delta\n                      snmpFddiMACLostCt)) x 2**16.')
snmpFddiMACRMTState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 25), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(('rm0',
                                                                                                                                                                                                              1), ('rm1',
                                                                                                                                                                                                                   2), ('rm2',
                                                                                                                                                                                                                        3), ('rm3',
                                                                                                                                                                                                                             4), ('rm4',
                                                                                                                                                                                                                                  5), ('rm5',
                                                                                                                                                                                                                                       6), ('rm6',
                                                                                                                                                                                                                                            7), ('rm7',
                                                                                                                                                                                                                                                 8)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACRMTState.setDescription('Indicates the current state of the Ring\n                      Management state machine (refer to ANSI Section\n                      10).')
snmpFddiMACDaFlag = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 26), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                          1), ('false',
                                                                                                                                                                                               2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACDaFlag.setDescription('The RMT flag Duplicate Address Flag, DA_Flag\n                      (refer to ANSI 10.3.1.2).')
snmpFddiMACUnaDaFlag = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 27), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                             1), ('false',
                                                                                                                                                                                                  2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACUnaDaFlag.setDescription('A flag set when the upstream neighbor reports a\n                      duplicate address condition.  Reset when the\n                      condition clears.')
snmpFddiMACFrameCondition = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 28), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                                  1), ('false',
                                                                                                                                                                                                       2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACFrameCondition.setDescription('Indicates the MAC Condition is active when set.\n                      Cleared when the condition clears and on power\n                      up.')
snmpFddiMACChipSet = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 29), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiMACChipSet.setDescription("This object identifies the hardware chip(s) which\n                      is (are) principally responsible for the\n                      implementation of the MAC function.  A few OBJECT\n                      IDENTIFIERS are identified elsewhere in this memo.\n                      For those The assignment of additional OBJECT\n                      IDENTIFIERs to various types of hardware chip sets\n                      is managed by the IANA.  For example, vendors\n                      whose chip sets are not defined in this memo may\n                      request a number from the Internet Assigned\n                      Numbers Authority (IANA) which indicates the\n                      assignment of a enterprise specific subtree which,\n                      among other things, may be used to allocate OBJECT\n                      IDENTIFIER assignments for that enterprise's chip\n                      sets.  Similarly, in the absence of an\n                      appropriately assigned OBJECT IDENTIFIER in this\n                      memo or in an enterprise specific subtree of a\n                      chip vendor, a board or system vendor can request\n                      a number for a subtree from the IANA and make an\n                      appropriate assignment.  It is desired that,\n                      whenever possible, the same OBJECT IDENTIFIER be\n                      used for all chips of a given type.  Consequently,\n                      the assignment made in this memo for a chip, if\n                      any, should be used in preference to any other\n                      assignment and the assignment made by the chip\n                      manufacturer, if any, should be used in preference\n                      to assignments made by users of those chips.  If\n                      the hardware chip set is unknown, the object\n                      identifier\n\n                      unknownChipSet OBJECT IDENTIFIER ::= { 0 0 }\n\n                      is returned.  Note that unknownChipSet is a\n                      syntactically valid object identifier, and any\n                      conformant implementation of ASN.1 and the BER\n                      must be able to generate and recognize this\n                      value.")
snmpFddiMACAction = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 2, 2, 1, 30), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                                   1), ('enableLLCService',
                                                                                                                                                                                                        2), ('disableLLCService',
                                                                                                                                                                                                             3), ('connectMAC',
                                                                                                                                                                                                                  4), ('disconnectMAC',
                                                                                                                                                                                                                       5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiMACAction.setDescription('This object, when read, always returns a value of\n                      other(1).  The behavior of setting this variable\n                      to each of the acceptable values is as follows:\n\n                      Other:                  Results in a badValue\n                                              error.\n\n                      enableLLCService:       enables MAC service to\n                                              higher layers.\n\n                      disableLLCService:      disables MAC service to\n                                              higher layers.\n\n                      connectMAC:             connect this MAC in\n                                              station.\n\n                      disconnectMAC:          disconnect this MAC in\n                                              station.\n\n                      Attempts to set this object to all other values\n                      results in a badValue error.')
snmpFddiPORTNumber = MibScalar((1, 3, 6, 1, 2, 1, 10, 15, 4, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTNumber.setDescription("The total number of PORT implementations (across\n                      all SMTs) on this network management application\n                      entity.  The value for this variable must remain\n                      constant at least from one re-initialization of\n                      the entity's network management system to the next\n                      re-initialization.")
snmpFddiPORTTable = MibTable((1, 3, 6, 1, 2, 1, 10, 15, 4, 2))
if mibBuilder.loadTexts:
    snmpFddiPORTTable.setDescription('A list of PORT entries.  The number of entries is\n                      given by the value of snmpFddiPORTNumber.')
snmpFddiPORTEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1)).setIndexNames((0,
                                                                                    'RFC1285-MIB',
                                                                                    'snmpFddiPORTSMTIndex'), (0,
                                                                                                              'RFC1285-MIB',
                                                                                                              'snmpFddiPORTIndex'))
if mibBuilder.loadTexts:
    snmpFddiPORTEntry.setDescription('A PORT entry containing information common to a\n                      given PORT.')
snmpFddiPORTSMTIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTSMTIndex.setDescription('The value of the SMT index associated with this\n                      PORT.')
snmpFddiPORTIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTIndex.setDescription("A unique value for each PORT within a given SMT.\n                      Its value ranges between 1 and the sum of the\n                      values of snmpFddiSMTNonMasterCt\n                      { snmpFddiSMTEntry 6 } and snmpFddiSMTMasterCt\n                      { snmpFddiSMTEntry 7 } on the given SMT.  The\n                      value for each PORT must remain constant at least\n                      from one re-initialization of the entity's network\n                      management system to the next re-initialization.")
snmpFddiPORTPCType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('a',
                                                                                                                                                                                                1), ('b',
                                                                                                                                                                                                     2), ('s',
                                                                                                                                                                                                          3), ('m',
                                                                                                                                                                                                               4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTPCType.setDescription('PC_Type (refer to ANSI SMT 9.2.2 and ANSI SMT\n                      9.6.3.2).')
snmpFddiPORTPCNeighbor = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('a',
                                                                                                                                                                                                       1), ('b',
                                                                                                                                                                                                            2), ('s',
                                                                                                                                                                                                                 3), ('m',
                                                                                                                                                                                                                      4), ('unknown',
                                                                                                                                                                                                                           5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTPCNeighbor.setDescription('The type (PC_Neighbor) of the remote PORT that is\n                      determined in PC_Signaling in R_Val (1,2) (refer\n                      to ANSI SMT 9.6.3.2).')
snmpFddiPORTConnectionPolicies = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1,
                                                 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTConnectionPolicies.setDescription("A value that indicates the node's PORT policies.\n                      Pc-MAC-LCT, Pc-MAC-Loop, and Pc-MAC-Placement\n                      indicate how the respective PC Signaling\n                      Capability flags should  be set (refer to ANSI SMT\n                      9.4.3.2).\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each PORT policy, 2\n                      raised to a power is added to the sum.  The powers\n                      are according to the following table:\n\n                                    Policy   Power\n                                Pc-MAC-LCT   0\n                               Pc-MAC-Loop   1\n                          Pc-MAC-Placement   2 ")
snmpFddiPORTRemoteMACIndicated = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1,
                                                 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                   1), ('false',
                                                                                                                                                                        2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTRemoteMACIndicated.setDescription('The indication, in PC-Signaling that the remote\n                      partner intends to place a MAC in the output token\n                      PATH of this PORT.  Signaled as R_Val (9) (refer\n                      to ANSI SMT 9.6.3.2).')
snmpFddiPORTCEState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('ce0',
                                                                                                                                                                                                    1), ('ce1',
                                                                                                                                                                                                         2), ('ce2',
                                                                                                                                                                                                              3), ('ce3',
                                                                                                                                                                                                                   4), ('ce4',
                                                                                                                                                                                                                        5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTCEState.setDescription("Indicates the current state of PORT's\n                      Configuration Element (CE) (refer to ANSI 9.7.5).\n                      Note that this value represents the Current Path\n                      information for this PORT.")
snmpFddiPORTPathsRequested = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTPathsRequested.setDescription("A value that indicates the desired association(s)\n                      of the port with a station PATH.  The 'Primary'\n                      Path is the default.  The value of 'Secondary' is\n                      only meaningful for S (slave) or M (master) PORT\n                      PC-Types.  This value effects the setting of the\n                      CF_Insert_S, and CF_Insert_L flags (refer to ANSI\n                      Section 9.4.3).  If the 'Primary' PATH is present,\n                      then the Primary PATH (the default PATH) is\n                      selected.  If the 'Secondary' PATH is present and\n                      the 'Primary' PATH is not present, then the\n                      CF_Insert_S flag is set.  If the 'Local' PATH is\n                      sent and neither the 'Primary' or 'Secondary'\n                      PATHs are sent, then the CF_Insert_L flag is set.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each type of PATH\n                      desired, 2 raised to a power is added to the sum.\n                      The powers are according to the following table:\n\n                               Path   Power\n                            Primary   0\n                          Secondary   1\n                              Local   2\n                           Isolated   3 ")
snmpFddiPORTMACPlacement = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 9), FddiResourceId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTMACPlacement.setDescription('Indicates the upstream MAC, if any, that is\n                      associated with the PORT.  The value shall be zero\n                      if there is no MAC associated with the PORT.\n                      Otherwise, the value shall be equal to the value\n                      of snmpFddiMACIndex associated with the MAC.')
snmpFddiPORTAvailablePaths = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTAvailablePaths.setDescription('A value that indicates the PATH types available\n                      for M and S PORTs.\n\n                      The value is a sum.  This value initially takes\n                      the value zero, then for each type of PATH that\n                      this port has available, 2 raised to a power is\n                      added to the sum.  The powers are according to the\n                      following table:\n\n                               Path   Power\n                            Primary   0\n                          Secondary   1\n                              Local   2 ')
snmpFddiPORTMACLoopTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 11), FddiTime()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTMACLoopTime.setDescription('Time for the optional MAC Local Loop, T_Next(9),\n                      which is greater-than or equal-to 200 milliseconds\n                      (refer to ANSI SMT 9.4.4.2.3).')
snmpFddiPORTTBMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 12), FddiTime()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTTBMax.setDescription('TB_Max (refer to ANSI SMT 9.4.4.2.1).')
snmpFddiPORTBSFlag = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 13), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                           1), ('false',
                                                                                                                                                                                                2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTBSFlag.setDescription('The Break State, BS_Flag (refer to ANSI SMT\n                      9.4.3.4).')
snmpFddiPORTLCTFailCts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTLCTFailCts.setDescription('The count of the consecutive times the link\n                      confidence test (LCT) has failed during connection\n                      management (refer to ANSI 9.4.1).')
snmpFddiPORTLerEstimate = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(4, 15))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTLerEstimate.setDescription('A long term average link error rate.  It ranges\n                      from 10**-4 to 10**-15 and is reported as the\n                      absolute value of the exponent of the estimate.')
snmpFddiPORTLemRejectCts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 16), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTLemRejectCts.setDescription('A link error monitoring count of the times that a\n                      link has been rejected.')
snmpFddiPORTLemCts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTLemCts.setDescription('The aggregate link error monitor error count, set\n                      to zero only on station power_up.')
snmpFddiPORTLerCutoff = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 18), Integer32().subtype(subtypeSpec=ValueRangeConstraint(4, 15))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTLerCutoff.setDescription('The link error rate estimate at which a link\n                      connection will be broken.  It ranges from 10**-4\n                      to 10**-15 and is reported as the absolute value\n                      of the exponent.')
snmpFddiPORTLerAlarm = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 19), Integer32().subtype(subtypeSpec=ValueRangeConstraint(4, 15))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTLerAlarm.setDescription('The link error rate estimate at which a link\n                      connection will generate an alarm.  It ranges from\n                      10**-4 to 10**-15 and is reported as the absolute\n                      value of the exponent of the estimate.')
snmpFddiPORTConnectState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 20), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('disabled',
                                                                                                                                                                                                       1), ('connecting',
                                                                                                                                                                                                            2), ('standby',
                                                                                                                                                                                                                 3), ('active',
                                                                                                                                                                                                                      4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTConnectState.setDescription('An indication of the connect state of this PORT.\n                      Basically, this gives a higher level view of the\n                      state of the connection by grouping PCM states and\n                      the PC-Withhold flag state.  The supported values\n                      and their corresponding PCM states and PC-Withhold\n                      condition, when relevant, are:\n\n                        disabled: (PC0:Off, PC9:Maint)\n\n                      connecting: (PC1(Break) || PC3 (Connect) || PC4\n                      (Next)                 || PC5 (Signal) || PC6\n                      (Join) || PC7 (Verify))             &&\n                      (PC_Withhold = None)\n\n                         standby: (NOT PC_Withhold == None)\n\n                          active: (PC2:Trace || PC8:Active) ')
snmpFddiPORTPCMState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 21), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))).clone(namedValues=NamedValues(('pc0',
                                                                                                                                                                                                                      1), ('pc1',
                                                                                                                                                                                                                           2), ('pc2',
                                                                                                                                                                                                                                3), ('pc3',
                                                                                                                                                                                                                                     4), ('pc4',
                                                                                                                                                                                                                                          5), ('pc5',
                                                                                                                                                                                                                                               6), ('pc6',
                                                                                                                                                                                                                                                    7), ('pc7',
                                                                                                                                                                                                                                                         8), ('pc8',
                                                                                                                                                                                                                                                              9), ('pc9',
                                                                                                                                                                                                                                                                   10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTPCMState.setDescription('(refer to SMT 9.6.2).')
snmpFddiPORTPCWithhold = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 22), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                                  1), ('m-m',
                                                                                                                                                                                                       2), ('other',
                                                                                                                                                                                                            3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTPCWithhold.setDescription('PC_Withhold, (refer to ANSI SMT 9.4.1).')
snmpFddiPORTLerCondition = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 23), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                                 1), ('false',
                                                                                                                                                                                                      2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTLerCondition.setDescription('This variable is set to true whenever LerEstimate\n                      is less than or equal to LerAlarm.')
snmpFddiPORTChipSet = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 24), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiPORTChipSet.setDescription("This object identifies the hardware chip(s) which\n                      is (are) principally responsible for the\n                      implementation of the PORT (PHY) function.  A few\n                      OBJECT IDENTIFIERS are identified elsewhere in\n                      this memo.  For those The assignment of additional\n                      OBJECT IDENTIFIERs to various types of hardware\n                      chip sets is managed by the IANA.  For example,\n                      vendors whose chip sets are not defined in this\n                      memo may request a number from the Internet\n                      Assigned Numbers Authority (IANA) which indicates\n                      the assignment of a enterprise specific subtree\n                      which, among other things, may be used to allocate\n                      OBJECT IDENTIFIER assignments for that\n                      enterprise's chip sets.  Similarly, in the absence\n                      of an appropriately assigned OBJECT IDENTIFIER in\n                      this memo or in an enterprise specific subtree of\n                      a chip vendor, a board or system vendor can\n                      request a number for a subtree from the IANA and\n                      make an appropriate assignment.  It is desired\n                      that, whenever possible, the same OBJECT\n                      IDENTIFIER be used for all chips of a given type.\n                      Consequently, the assignment made in this memo for\n                      a chip, if any, should be used in preference to\n                      any other assignment and the assignment made by\n                      the chip manufacturer, if any, should be used in\n                      preference to assignments made by users of those\n                      chips.  If the hardware chip set is unknown, the\n                      object identifier\n\n                      unknownChipSet OBJECT IDENTIFIER ::= { 0 0 }\n\n                      is returned.  Note that unknownChipSet is a\n                      syntactically valid object identifier, and any\n                      conformant implementation of ASN.1 and the BER\n                      must be able to generate and recognize this\n                      value.")
snmpFddiPORTAction = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 4, 2, 1, 25), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                                       1), ('maintPORT',
                                                                                                                                                                                                            2), ('enablePORT',
                                                                                                                                                                                                                 3), ('disablePORT',
                                                                                                                                                                                                                      4), ('startPORT',
                                                                                                                                                                                                                           5), ('stopPORT',
                                                                                                                                                                                                                                6)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiPORTAction.setDescription("This object, when read, always returns a value of\n                      other(1).  The behavior of setting this variable\n                      to each of the acceptable values is as follows:\n\n                      Other:          Results in a badValue error.\n\n                      maintPORT:      Signal PC_Maint\n\n                      enablePORT:     Signal PC_Enable\n\n                      disablePORT:    Signal PC_Disable\n\n                      startPORT:      Signal PC_Start\n\n                      stopPORT:       Signal PC_Stop\n\n                      Signals cause an SM_CM_CONTROL.request service to\n                      be generated with a control_action of `Signal' and\n                      the `variable' parameter set with the appropriate\n                      value (i.e., PC_Maint, PC_Enable, PC_Disable,\n                      PC_Start, PC_Stop).  Ref. ANSI SMT Section 9.3.2.\n\n                      Attempts to set this object to all other values\n                      results in a badValue error.")
snmpFddiATTACHMENTNumber = MibScalar((1, 3, 6, 1, 2, 1, 10, 15, 5, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTNumber.setDescription("The total number of attachments (across all SMTs)\n                      on this network management application entity.\n                      The value for this variable must remain constant\n                      at least from one re-initialization of the\n                      entity's network management system to the next\n                      re-initialization.")
snmpFddiATTACHMENTTable = MibTable((1, 3, 6, 1, 2, 1, 10, 15, 5, 2))
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTTable.setDescription('A list of ATTACHMENT entries.  The number of\n                      entries is given by the value of\n                      snmpFddiATTACHMENTNumber.')
snmpFddiATTACHMENTEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 15, 5, 2, 1)).setIndexNames((0,
                                                                                          'RFC1285-MIB',
                                                                                          'snmpFddiATTACHMENTSMTIndex'), (0,
                                                                                                                          'RFC1285-MIB',
                                                                                                                          'snmpFddiATTACHMENTIndex'))
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTEntry.setDescription("An ATTACHMENT entry containing information common\n                      to a given set of ATTACHMENTs.\n\n                      The ATTACHMENT Resource represents a PORT or a\n                      pair of PORTs plus the optional associated optical\n                      bypass that are managed as a functional unit.\n                      Because of its relationship to the PORT Objects,\n                      there is a natural association of ATTACHMENT\n                      Resource Indices to the PORT Indices.  The\n                      resource index for the ATTACHMENT is equal to the\n                      associated PORT index for 'single-attachment' and\n                      'concentrator' type snmpFddiATTACHMENTClasses.\n                      For 'dual-attachment' Classes, the ATTACHMENT\n                      Index is the PORT Index of the A PORT of the A/B\n                      PORT Pair that represents the ATTACHMENT.")
snmpFddiATTACHMENTSMTIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 5, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTSMTIndex.setDescription('The value of the SMT index associated with this\n                      ATTACHMENT.')
snmpFddiATTACHMENTIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 5, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTIndex.setDescription("A unique value for each ATTACHMENT on a given\n                      SMT.  Its value ranges between 1 and the sum of\n                      the values of snmpFddiSMTNonMasterCt {\n                      snmpFddiSMTEntry 6 } and snmpFddiSMTMasterCt {\n                      snmpFddiSMTEntry 7 } on the given SMT.  The value\n                      for each ATTACHMENT must remain constant at least\n                      from one re-initialization of the entity's network\n                      management system to the next re-initialization.")
snmpFddiATTACHMENTClass = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 5, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('single-attachment',
                                                                                                                                                                                                  1), ('dual-attachment',
                                                                                                                                                                                                       2), ('concentrator',
                                                                                                                                                                                                            3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTClass.setDescription('The Attachment class.  This  represents a PORT or\n                      a pair of PORTs plus the associated optional\n                      optical bypass that are managed as a functional\n                      unit.  The PORT associations are the following:\n\n                          single-attachment - S PORTs\n                            dual-attachment - A/B PORT Pairs\n                               concentrator - M PORTs ')
snmpFddiATTACHMENTOpticalBypassPresent = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15,
                                                         5, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                    1), ('false',
                                                                                                                                                                                         2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTOpticalBypassPresent.setDescription("The value of this value is false for 'single-\n                      attachment' and { snmpFddiATTACHMENT 11 }.\n                      Correct operation of CMT for single-attachment and\n                      concentrator attachments requires that a bypass\n                      function must not loopback the network side of the\n                      MIC, but only the node side.")
snmpFddiATTACHMENTIMaxExpiration = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 5, 2,
                                                   1, 5), FddiTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTIMaxExpiration.setDescription('I_Max (refer to ANSI SMT 9.4.4.2.1).  It is\n                      recognized that some currently deployed systems do\n                      not implement an optical bypass.  Systems which do\n                      not implement optical bypass should return a value\n                      of 0.')
snmpFddiATTACHMENTInsertedStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 5, 2,
                                                   1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                           1), ('false',
                                                                                                                                                                                2), ('unimplemented',
                                                                                                                                                                                     3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTInsertedStatus.setDescription('Indicates whether the attachment is currently\n                      inserted in the node.')
snmpFddiATTACHMENTInsertPolicy = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 15, 5, 2, 1,
                                                 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                      1), ('false',
                                                                                                                                                                           2), ('unimplemented',
                                                                                                                                                                                3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    snmpFddiATTACHMENTInsertPolicy.setDescription("Indicates the Insert Policy for this Attachment.\n                      Insert: True (1), Don't Insert:  False (2),\n                      Unimplemented (3)")
snmpFddiPHYChipSets = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 6, 1))
snmpFddiMACChipSets = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 6, 2))
snmpFddiPHYMACChipSets = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 15, 6, 3))
mibBuilder.exportSymbols('RFC1285-MIB', snmpFddiMACRMTState=snmpFddiMACRMTState, snmpFddiPORTPathsRequested=snmpFddiPORTPathsRequested, snmpFddiSMTEntry=snmpFddiSMTEntry, snmpFddiPORTPCNeighbor=snmpFddiPORTPCNeighbor, snmpFddiPORTChipSet=snmpFddiPORTChipSet, snmpFddiMACTvxValue=snmpFddiMACTvxValue, snmpFddiMACCurrentFrameStatus=snmpFddiMACCurrentFrameStatus, snmpFddiSMTTable=snmpFddiSMTTable, snmpFddiMACTNeg=snmpFddiMACTNeg, snmpFddiSMTStationId=snmpFddiSMTStationId, snmpFddiPORTEntry=snmpFddiPORTEntry, snmpFddiMACErrorCts=snmpFddiMACErrorCts, snmpFddiPORTRemoteMACIndicated=snmpFddiPORTRemoteMACIndicated, snmpFddiPORTBSFlag=snmpFddiPORTBSFlag, snmpFddiMACDaFlag=snmpFddiMACDaFlag, snmpFddiMACFrameStatusCapabilities=snmpFddiMACFrameStatusCapabilities, snmpFddiPORTCEState=snmpFddiPORTCEState, snmpFddiSMTPathsAvailable=snmpFddiSMTPathsAvailable, snmpFddiPORTTBMax=snmpFddiPORTTBMax, snmpFddiPORTConnectionPolicies=snmpFddiPORTConnectionPolicies, snmpFddiATTACHMENTIMaxExpiration=snmpFddiATTACHMENTIMaxExpiration, snmpFddiSMTStationAction=snmpFddiSMTStationAction, snmpFddiMACPathsAvailable=snmpFddiMACPathsAvailable, snmpFddiPORTTable=snmpFddiPORTTable, snmpFddiPORTNumber=snmpFddiPORTNumber, snmpFddiPHYMACChipSets=snmpFddiPHYMACChipSets, snmpFddiMACDupAddrTest=snmpFddiMACDupAddrTest, snmpFddiPORTPCWithhold=snmpFddiPORTPCWithhold, snmpFddiMACFrameCondition=snmpFddiMACFrameCondition, FddiMACLongAddressType=FddiMACLongAddressType, snmpFddiMACTVXGreatestLowerBound=snmpFddiMACTVXGreatestLowerBound, snmpFddiPORTIndex=snmpFddiPORTIndex, snmpFddiPORTPCType=snmpFddiPORTPCType, snmpFddiMACIndex=snmpFddiMACIndex, snmpFddiPORTLemCts=snmpFddiPORTLemCts, snmpFddiSMTNumber=snmpFddiSMTNumber, snmpFddiSMTConnectionPolicy=snmpFddiSMTConnectionPolicy, snmpFddiSMTMasterCt=snmpFddiSMTMasterCt, snmpFddiMACOldUpstreamNbr=snmpFddiMACOldUpstreamNbr, snmpFddiMACTReq=snmpFddiMACTReq, snmpFddiATTACHMENTInsertPolicy=snmpFddiATTACHMENTInsertPolicy, snmpFddiPORTLerAlarm=snmpFddiPORTLerAlarm, snmpFddiATTACHMENTSMTIndex=snmpFddiATTACHMENTSMTIndex, snmpFddiMACUpstreamNbr=snmpFddiMACUpstreamNbr, snmpFddiSMTMACCt=snmpFddiSMTMACCt, snmpFddiMACSMTAddress=snmpFddiMACSMTAddress, snmpFddiSMTECMState=snmpFddiSMTECMState, snmpFddiMACLostCts=snmpFddiMACLostCts, snmpFddiMACTable=snmpFddiMACTable, snmpFddiATTACHMENTIndex=snmpFddiATTACHMENTIndex, snmpFddiMACChipSet=snmpFddiMACChipSet, snmpFddiPORTLerEstimate=snmpFddiPORTLerEstimate, snmpFddiSMTOpVersionId=snmpFddiSMTOpVersionId, snmpFddiATTACHMENTNumber=snmpFddiATTACHMENTNumber, snmpFddiMACTMax=snmpFddiMACTMax, snmpFddiSMTHoldState=snmpFddiSMTHoldState, fddi=fddi, snmpFddiATTACHMENTEntry=snmpFddiATTACHMENTEntry, snmpFddiPORTLCTFailCts=snmpFddiPORTLCTFailCts, FddiResourceId=FddiResourceId, snmpFddiPORTMACPlacement=snmpFddiPORTMACPlacement, snmpFddiSMTConfigPolicy=snmpFddiSMTConfigPolicy, FddiSMTStationIdType=FddiSMTStationIdType, snmpFddiSMTCFState=snmpFddiSMTCFState, snmpFddiMACDownstreamPORTType=snmpFddiMACDownstreamPORTType, snmpFddiSMTLoVersionId=snmpFddiSMTLoVersionId, snmpFddiChipSets=snmpFddiChipSets, snmpFddiMAC=snmpFddiMAC, snmpFddiPORTSMTIndex=snmpFddiPORTSMTIndex, snmpFddiMACFrameCts=snmpFddiMACFrameCts, snmpFddiPORT=snmpFddiPORT, snmpFddiATTACHMENT=snmpFddiATTACHMENT, snmpFddiATTACHMENTTable=snmpFddiATTACHMENTTable, snmpFddiSMTStatusReporting=snmpFddiSMTStatusReporting, FddiTime=FddiTime, snmpFddiPORTAvailablePaths=snmpFddiPORTAvailablePaths, snmpFddiPORTAction=snmpFddiPORTAction, snmpFddiMACSMTIndex=snmpFddiMACSMTIndex, snmpFddiSMT=snmpFddiSMT, snmpFddiMACNumber=snmpFddiMACNumber, snmpFddiATTACHMENTInsertedStatus=snmpFddiATTACHMENTInsertedStatus, snmpFddiATTACHMENTOpticalBypassPresent=snmpFddiATTACHMENTOpticalBypassPresent, snmpFddiPHYChipSets=snmpFddiPHYChipSets, snmpFddiPORTConnectState=snmpFddiPORTConnectState, snmpFddiPORTPCMState=snmpFddiPORTPCMState, snmpFddiATTACHMENTClass=snmpFddiATTACHMENTClass, snmpFddiMACTMin=snmpFddiMACTMin, snmpFddiSMTRemoteDisconnectFlag=snmpFddiSMTRemoteDisconnectFlag, snmpFddiPORTMACLoopTime=snmpFddiPORTMACLoopTime, snmpFddiMACPathsRequested=snmpFddiMACPathsRequested, snmpFddiMACFrameErrorThreshold=snmpFddiMACFrameErrorThreshold, snmpFddiSMTConfigCapabilities=snmpFddiSMTConfigCapabilities, snmpFddiPORTLerCutoff=snmpFddiPORTLerCutoff, snmpFddiSMTTNotify=snmpFddiSMTTNotify, snmpFddiMACUnaDaFlag=snmpFddiMACUnaDaFlag, snmpFddiMACEntry=snmpFddiMACEntry, snmpFddiMACTMaxGreatestLowerBound=snmpFddiMACTMaxGreatestLowerBound, snmpFddiSMTNonMasterCt=snmpFddiSMTNonMasterCt, snmpFddiMACChipSets=snmpFddiMACChipSets, snmpFddiSMTHiVersionId=snmpFddiSMTHiVersionId, snmpFddiMACAction=snmpFddiMACAction, snmpFddiSMTIndex=snmpFddiSMTIndex, snmpFddiPORTLerCondition=snmpFddiPORTLerCondition, snmpFddiPORTLemRejectCts=snmpFddiPORTLemRejectCts, snmpFddiPATH=snmpFddiPATH, snmpFddiMACFrameErrorRatio=snmpFddiMACFrameErrorRatio, snmpFddiMACCurrentPath=snmpFddiMACCurrentPath)