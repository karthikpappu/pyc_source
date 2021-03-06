# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/ISNS-MIB.py
# Compiled at: 2016-02-13 18:19:11
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection', 'ValueSizeConstraint')
(PhysicalIndex,) = mibBuilder.importSymbols('ENTITY-MIB', 'PhysicalIndex')
(FcAddressIdOrZero, FcNameIdOrZero) = mibBuilder.importSymbols('FC-MGMT-MIB', 'FcAddressIdOrZero', 'FcNameIdOrZero')
(InetPortNumber, InetAddressType, InetAddress) = mibBuilder.importSymbols('INET-ADDRESS-MIB', 'InetPortNumber', 'InetAddressType', 'InetAddress')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(mib_2, Integer32, Gauge32, Counter32, Bits, Counter64, TimeTicks, NotificationType, Unsigned32, IpAddress, MibIdentifier, iso, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'mib-2', 'Integer32', 'Gauge32', 'Counter32', 'Bits', 'Counter64', 'TimeTicks', 'NotificationType', 'Unsigned32', 'IpAddress', 'MibIdentifier', 'iso', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'ModuleIdentity')
(TextualConvention, DisplayString, TruthValue, TimeStamp) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString', 'TruthValue', 'TimeStamp')
isnsMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 163)).setRevisions(('2007-07-11 00:00',))
if mibBuilder.loadTexts:
    isnsMIB.setLastUpdated('200707110000Z')
if mibBuilder.loadTexts:
    isnsMIB.setOrganization('IETF IPS Working Group')
if mibBuilder.loadTexts:
    isnsMIB.setContactInfo('\n           Attn: Kevin Gibbons\n                 2Wire, Inc.\n                 1704 Automation Parkway\n                 San Jose, CA 95131\n                 USA\n                 Tel: +1 408-895-1387\n                 Fax: +1 408-428-9590\n                 Email: kgibbons@yahoo.com\n\n                 G.D. Ramkumar\n                 SnapTell, Inc.\n                 2741 Middlefield Rd, Suite 200\n                 Palo Alto, CA 94306\n                 USA\n                 Tel: +1 650-326-7627\n                 Fax: +1 650-326-7620\n                 Email: gramkumar@stanfordalumni.org\n\n                 Scott Kipp\n                 Brocade\n                 4 McDATA Pkwy\n                 Broomfield, CO 80021\n                 USA\n                 Tel: +1 720-558-3452\n                 Fax: +1 720-558-8999\n                 Email: skipp@brocade.com\n                       ')
if mibBuilder.loadTexts:
    isnsMIB.setDescription('This module defines management information\n                     specific to internet Storage Name Service\n                     (iSNS) management.\n\n                     Copyright (C) The IETF Trust (2007).\n                     This version of this MIB module is part\n                     of RFC 4939; see the RFC itself for full\n                     legal notices.')

class IsnsDiscoveryDomainSetId(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(1, 4294967295)


class IsnsDdsStatusType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('reserved24',
                                                                                                                                                                                                            24), ('reserved25',
                                                                                                                                                                                                                  25), ('reserved26',
                                                                                                                                                                                                                        26), ('reserved27',
                                                                                                                                                                                                                              27), ('reserved28',
                                                                                                                                                                                                                                    28), ('reserved29',
                                                                                                                                                                                                                                          29), ('reserved30',
                                                                                                                                                                                                                                                30), ('ddsEnabled',
                                                                                                                                                                                                                                                      31))


class IsnsDiscoveryDomainId(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(1, 4294967295)


class IsnsDdFeatureType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('reserved24',
                                                                                                                                                                                                            24), ('reserved25',
                                                                                                                                                                                                                  25), ('reserved26',
                                                                                                                                                                                                                        26), ('reserved27',
                                                                                                                                                                                                                              27), ('reserved28',
                                                                                                                                                                                                                                    28), ('reserved29',
                                                                                                                                                                                                                                          29), ('reserved30',
                                                                                                                                                                                                                                                30), ('bootlist',
                                                                                                                                                                                                                                                      31))


class IsnsDdDdsModificationType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('controlNode', 0), ('targetIscsiNode', 1), ('initiatorIscsiNode',
                                                                           2), ('targetIfcpNode',
                                                                                3), ('initiatorIfcpNode',
                                                                                     4))


class IsnsEntityIndexIdOrZero(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(0, 4294967295)


class IsnsPortalGroupIndexId(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(1, 4294967295)


class IsnsPortalIndexId(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(1, 4294967295)


class IsnsPortalPortTypeId(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('udp', 1), ('tcp', 2))


class IsnsPortalGroupTagIdOrNull(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(-1, 65535)


class IsnsPortalSecurityType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('reserved24',
                                                                                                                                                                                                            24), ('tunnelModePreferred',
                                                                                                                                                                                                                  25), ('transportModePreferred',
                                                                                                                                                                                                                        26), ('pfsEnabled',
                                                                                                                                                                                                                              27), ('agressiveModeEnabled',
                                                                                                                                                                                                                                    28), ('mainModeEnabled',
                                                                                                                                                                                                                                          29), ('ikeIPsecEnabled',
                                                                                                                                                                                                                                                30), ('bitmapVALID',
                                                                                                                                                                                                                                                      31))


class IsnsNodeIndexId(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(1, 4294967295)


class IsnsIscsiNodeType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('reserved24',
                                                                                                                                                                                                            24), ('reserved25',
                                                                                                                                                                                                                  25), ('reserved26',
                                                                                                                                                                                                                        26), ('reserved27',
                                                                                                                                                                                                                              27), ('reserved28',
                                                                                                                                                                                                                                    28), ('control',
                                                                                                                                                                                                                                          29), ('initiator',
                                                                                                                                                                                                                                                30), ('target',
                                                                                                                                                                                                                                                      31))


class IsnsFcClassOfServiceType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('reserved24',
                                                                                                                                                                                                            24), ('reserved25',
                                                                                                                                                                                                                  25), ('reserved26',
                                                                                                                                                                                                                        26), ('reserved27',
                                                                                                                                                                                                                              27), ('class3',
                                                                                                                                                                                                                                    28), ('class2',
                                                                                                                                                                                                                                          29))


class IsnsIscsiScnType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('initiatorAndSelfOnly',
                                                                                                                                                                                                            24), ('targetAndSelfOnly',
                                                                                                                                                                                                                  25), ('managementRegistrationScn',
                                                                                                                                                                                                                        26), ('objectRemoved',
                                                                                                                                                                                                                              27), ('objectAdded',
                                                                                                                                                                                                                                    28), ('objectUpdated',
                                                                                                                                                                                                                                          29), ('ddOrDdsMemberRemoved',
                                                                                                                                                                                                                                                30), ('ddOrDdsMemberAdded',
                                                                                                                                                                                                                                                      31))


class IsnsIfcpScnType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('initiatorAndSelfOnly',
                                                                                                                                                                                                            24), ('targetAndSelfOnly',
                                                                                                                                                                                                                  25), ('managementRegistrationScn',
                                                                                                                                                                                                                        26), ('objectRemoved',
                                                                                                                                                                                                                              27), ('objectAdded',
                                                                                                                                                                                                                                    28), ('objectUpdated',
                                                                                                                                                                                                                                          29), ('ddOrDdsMemberRemoved',
                                                                                                                                                                                                                                                30), ('ddOrDdsMemberAdded',
                                                                                                                                                                                                                                                      31))


class IsnsFcPortRoleType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('reserved0', 0), ('reserved1', 1), ('reserved2', 2), ('reserved3',
                                                                                     3), ('reserved4',
                                                                                          4), ('reserved5',
                                                                                               5), ('reserved6',
                                                                                                    6), ('reserved7',
                                                                                                         7), ('reserved8',
                                                                                                              8), ('reserved9',
                                                                                                                   9), ('reserved10',
                                                                                                                        10), ('reserved11',
                                                                                                                              11), ('reserved12',
                                                                                                                                    12), ('reserved13',
                                                                                                                                          13), ('reserved14',
                                                                                                                                                14), ('reserved15',
                                                                                                                                                      15), ('reserved16',
                                                                                                                                                            16), ('reserved17',
                                                                                                                                                                  17), ('reserved18',
                                                                                                                                                                        18), ('reserved19',
                                                                                                                                                                              19), ('reserved20',
                                                                                                                                                                                    20), ('reserved21',
                                                                                                                                                                                          21), ('reserved22',
                                                                                                                                                                                                22), ('reserved23',
                                                                                                                                                                                                      23), ('reserved24',
                                                                                                                                                                                                            24), ('reserved25',
                                                                                                                                                                                                                  25), ('reserved26',
                                                                                                                                                                                                                        26), ('reserved27',
                                                                                                                                                                                                                              27), ('reserved28',
                                                                                                                                                                                                                                    28), ('control',
                                                                                                                                                                                                                                          29), ('initiator',
                                                                                                                                                                                                                                                30), ('target',
                                                                                                                                                                                                                                                      31))


class IsnsSrvrDiscoveryMethodsType(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('dhcp', 0), ('slp', 1), ('multicastGroupHb', 2), ('broadcastHb',
                                                                                 3), ('cfgdServerList',
                                                                                      4), ('other',
                                                                                           5))


isnsNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 0))
isnsObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1))
isnsConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 2))
isnsServerInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1))
isnsServerTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 1))
if mibBuilder.loadTexts:
    isnsServerTable.setDescription('This table provides a list of the iSNS Server instances\n    that are managed through the same SNMP context.')
isnsServerEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'))
if mibBuilder.loadTexts:
    isnsServerEntry.setDescription('This is a row in the iSNS Server instance table.  The number\n    of rows is dependent on the number of iSNS Server instances\n    that are being managed through the same SNMP context.')
isnsServerIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    isnsServerIndex.setDescription('This object uniquely identifies the iSNS Server being\n    managed by the SNMP context and is the key for this table.\n    This is an instance index for each iSNS Server being\n    managed.  The value of this object is used elsewhere in\n    the MIB to reference specific iSNS Servers.')
isnsServerName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerName.setDescription('A non-unique name that can be assigned to the iSNS Server\n    instance.  If not configured, then the string SHALL be\n    zero-length.')
isnsServerIsnsVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(1)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerIsnsVersion.setDescription('The iSNS version value as contained in messages received\n    from the current primary server.  The header of each iSNSP\n    message contains the iSNS version of the sender.  If\n    unknown, the reported value is 0.')
isnsServerVendorInfo = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 4), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerVendorInfo.setDescription("If this server instance is utilizing the product of a\n    particular 'vendor', then this managed object contains\n    that vendor's name and version.  Otherwise, the\n    string SHALL be zero-length.  The format of the string\n    is as follows: Vendor Name, Vendor Version, Vendor\n    Defined Information.\n\n          Field           Description\n        ---------       ----------------\n       Vendor Name      The name of the vendor (if one exists)\n       Vendor Version   The version of the vendor product\n       Vendor Defined   This follows the second comma in the\n                        string, if one exists, and is vendor\n                        defined\n   ")
isnsServerPhysicalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 5), PhysicalIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerPhysicalIndex.setDescription("An index identifying the network interface for this iSNS\n    Server within a network entity.  This index maps to the\n    entPhysicalIndex of entPhysicalTable table in RFC 4133.  The\n    entPhysicalClass value for the table row must be 'port', as\n    the interface must be able to send and receive data.")
isnsServerTcpPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 6), InetPortNumber()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerTcpPort.setDescription('Indicates the TCP port this iSNS instance is accepting\n    iSNSP messages on, generally the iSNS well-known port.\n    The well-known TCP port for iSNSP is 3205.  If TCP is\n    not supported by this server instance, then the value\n    is 0.')
isnsServerUdpPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 7), InetPortNumber()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerUdpPort.setDescription('Indicates the UDP port this iSNS instance is accepting\n    iSNSP messages on; generally, the iSNS well-known port.\n    The well-known UDP port for iSNSP is 3205.  If UDP is\n    not supported by this server instance, then the value\n    is 0.')
isnsServerDiscontinuityTime = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 8), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerDiscontinuityTime.setDescription('The value of sysUpTime on the most recent occasion that\n    this iSNS server became active or suffered a\n    discontinuity.')
isnsServerRole = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('notSet', 1), ('server', 2), ('backupServer', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerRole.setDescription('The current operational mode of this iSNS Server instance.\n\n          Value             Description\n        ---------         ----------------\n         notSet           The iSNS Server role is not\n                          configured.\n         server           The iSNS Server instance is\n                          an operational iSNS Server.\n         backupServer     The iSNS Server instance is\n\n\n\n                          currently acting as a backup.')
isnsServerDiscoveryMethodsEnabled = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 10), IsnsSrvrDiscoveryMethodsType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerDiscoveryMethodsEnabled.setDescription('Indicates the discovery methods currently enabled for\n    this iSNS Server instance.  This allows a client to\n    determine what discovery methods can be used for\n    this iSNS Server.  Additional methods of discovery may\n    also be supported.')
isnsServerDiscoveryMcGroupType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 11), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerDiscoveryMcGroupType.setDescription('The type of Internet address in\n    isnsServerDiscoveryMcGroupAddress.  If the address is\n    specified, then it must be a valid multicast address and the\n    value of this object must be ipv4(1), ipv6(2), ipv4z(3), or\n    ipv6z(4); otherwise, the value of this object is\n    unknown(0), and the value of\n    isnsServerDiscoveryMcGroupAddress is the zero-length string.')
isnsServerDiscoveryMcGroupAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 12), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerDiscoveryMcGroupAddress.setDescription('The multicast group that iSNS Heartbeat messages are\n    sent to if multicast-based discovery has been enabled\n    for this server instance.  If not configured, then the\n    string SHALL be zero-length.  The format of this\n    object is specified by isnsServerDiscoveryMcGroupType.')
isnsServerEsiNonResponseThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 13), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(3)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerEsiNonResponseThreshold.setDescription('Entity Status Inquiry (ESI) Non-Response Threshold -\n\n\n\n    the number of ESI messages that will be sent without\n    receiving a response before an entity is deregistered\n    from the iSNS database.  A value of 0 indicates\n    Entities will never be deregistered due to non-receipt\n    of ESI messages.')
isnsServerEnableControlNodeMgtScn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 14), TruthValue().clone('true')).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerEnableControlNodeMgtScn.setDescription('Indicates if the iSNS Server administrative option to send\n    Management SCNs to Control Nodes is enabled.  Management\n    SCNs are used by Control Nodes to monitor and control an\n    iSNS Server.  If enabled, Control Nodes can register to\n    receive Management SCNs.')
isnsServerDefaultDdDdsStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 15), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('inNoDomain', 1), ('inDefaultDdAndDds', 2))).clone('inNoDomain')).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerDefaultDdDdsStatus.setDescription('This indicates the Discovery Domain (DD) and Discovery\n    Domain Set (DDS) membership status for a new device\n    when registered in the iSNS Server instance.  Either the\n    new device will not be in a DD/DDS, or will be placed\n    into a default DD and default DDS.  The default setting\n    is inNoDomain.')
isnsServerUpdateDdDdsSupported = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 16), IsnsDdDdsModificationType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerUpdateDdDdsSupported.setDescription('The methods that this iSNS Server instance supports\n    to modify Discovery Domains and Discovery Domain Sets.')
isnsServerUpdateDdDdsEnabled = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 1, 1, 17), IsnsDdDdsModificationType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsServerUpdateDdDdsEnabled.setDescription('This indicates the methods this server instance currently\n    allows for modifying Discovery Domains and Discovery\n    Domain Sets.')
isnsNumObjectsTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 2))
if mibBuilder.loadTexts:
    isnsNumObjectsTable.setDescription('Table providing the number of registered objects of each\n    type in the iSNS Server instance.  The number of entries is\n    dependent upon the number of iSNS Server instances being\n    managed.')
isnsNumObjectsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1))
isnsServerEntry.registerAugmentions(('ISNS-MIB', 'isnsNumObjectsEntry'))
isnsNumObjectsEntry.setIndexNames(*isnsServerEntry.getIndexNames())
if mibBuilder.loadTexts:
    isnsNumObjectsEntry.setDescription('Entry of an iSNS Server instance.')
isnsNumDds = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 1), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumDds.setDescription('The current total number of Discovery Domain Sets\n    in this iSNS instance.  This is the number of rows\n    in the isnsDdsTable.')
isnsNumDd = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 2), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumDd.setDescription('The current total number of Discovery Domains\n    in this iSNS instance.  This is the number of rows in the\n    isnsDdTable.')
isnsNumEntities = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 3), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumEntities.setDescription('The current number of Entities registered in this\n    iSNS Server instance.  This is the number of rows in\n    the isnsRegEntityTable for this instance.')
isnsNumPortals = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 4), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumPortals.setDescription('The current total number of Portals registered in iSNS.\n    This is the number of rows in isnsRegPortalTable.')
isnsNumPortalGroups = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 5), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumPortalGroups.setDescription('The current total number of Portal Groups registered in\n    iSNS.  This is the number of rows in isnsRegPgTable.')
isnsNumIscsiNodes = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 6), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumIscsiNodes.setDescription('The current total number of iSCSI node entries registered\n    in the iSNS.  This is the number rows in\n    isnsRegIscsiNodeTable.')
isnsNumFcPorts = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 7), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumFcPorts.setDescription('The current total number of FC Port entries registered\n    in the iSNS.  This is the number of rows in\n    isnsRegFcPortTable.')
isnsNumFcNodes = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 2, 1, 8), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsNumFcNodes.setDescription('The current total number of FC node entries registered\n    in the iSNS.  This is the number of rows in\n    isnsRegFcNodeTable.')
isnsControlNodeInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 3))
isnsControlNodeIscsiTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 1))
if mibBuilder.loadTexts:
    isnsControlNodeIscsiTable.setDescription('Specified iSCSI Nodes that can register or are registered\n    as control nodes.  The number of rows is dependent on the\n    number of iSCSI Control Nodes.')
isnsControlNodeIscsiEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsControlNodeIscsiNodeIndex'))
if mibBuilder.loadTexts:
    isnsControlNodeIscsiEntry.setDescription('This is an iSCSI Control Node entry for a specific iSNS\n    server instance.')
isnsControlNodeIscsiNodeIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 1, 1, 1), IsnsNodeIndexId())
if mibBuilder.loadTexts:
    isnsControlNodeIscsiNodeIndex.setDescription('The index for the iSCSI storage node authorized to act\n    as a control node.')
isnsControlNodeIscsiNodeName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 1, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsControlNodeIscsiNodeName.setDescription('The iSCSI Name of the initiator or target associated with\n    the storage node.  The iSCSI Name cannot be longer than\n    223 bytes.  The iSNS Server internal maximum size is 224\n    bytes to provide NULL termination.  This is the iSCSI Node\n    Name for the storage node authorized and/or acting as a\n    control node.')
isnsControlNodeIscsiIsRegistered = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 1, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsControlNodeIscsiIsRegistered.setDescription('Indicates whether the control node is currently\n     registered in the iSNS Server instance.')
isnsControlNodeIscsiRcvMgtSCN = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 1, 1, 4), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsControlNodeIscsiRcvMgtSCN.setDescription('Indicates whether the Control Node has registered to\n     receive Management SCNs.  Management SCNs are sent to\n     a Control Node if they are enabled, as indicated by\n     isnsServerEnableControlNodeMgtScn, and the Control\n     Node has registered for them.')
isnsControlNodeFcPortTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 2))
if mibBuilder.loadTexts:
    isnsControlNodeFcPortTable.setDescription('Specified FC Ports that can register or are registered as\n    control nodes.  The number of rows is dependent on the\n    number of FC Port Control Nodes.')
isnsControlNodeFcPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 2, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsControlNodeFcPortWwpn'))
if mibBuilder.loadTexts:
    isnsControlNodeFcPortEntry.setDescription('FC Port control node entry.')
isnsControlNodeFcPortWwpn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 2, 1, 1), FcNameIdOrZero().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8))
if mibBuilder.loadTexts:
    isnsControlNodeFcPortWwpn.setDescription('The FC Port World Wide Port Name that can and/or is acting\n    as a Control Node for the specified iSNS Server.  A zero-\n    length string is not valid for this managed object.\n    This managed object, combined with the isnsServerIndex, is\n    the key for this table.')
isnsControlNodeFcPortIsRegistered = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 2, 1, 2), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsControlNodeFcPortIsRegistered.setDescription('Indicates whether the control node is currently\n     registered in the iSNS Server instance.')
isnsControlNodeFcPortRcvMgtSCN = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 3, 2, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsControlNodeFcPortRcvMgtSCN.setDescription('Indicates whether the Control Node has registered to\n     receive Management SCNs.  Management SCNs are sent to\n     a Control Node if they are enabled, as indicated by\n     isnsServerEnableControlNodeMgtScn, and the Control\n     Node has registered for them.')
isnsDdsInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 4))
isnsDdsTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 1))
if mibBuilder.loadTexts:
    isnsDdsTable.setDescription('A table containing configuration information for each\n    Discovery Domain Set (DDS) registered in the iSNS Server\n    instance.  The number of rows in the table is dependent\n    on the number of DDSs registered in the specified iSNS\n    server instance.')
isnsDdsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsDdsId'))
if mibBuilder.loadTexts:
    isnsDdsEntry.setDescription('Information on one Discovery Domain Set (DDS) registered\n    in the iSNS Server instance.')
isnsDdsId = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 1, 1, 1), IsnsDiscoveryDomainSetId())
if mibBuilder.loadTexts:
    isnsDdsId.setDescription('The ID that refers to this Discovery Domain Set and\n    index to the table.')
isnsDdsSymbolicName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 1, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdsSymbolicName.setDescription('The Discovery Domain Set Symbolic Name field contains\n    a unique variable-length description (up to 255 bytes)\n    that is associated with the DDS.  If a Symbolic Name is\n    not provided, then one will be generated by the iSNS\n    server.')
isnsDdsStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 1, 1, 3), IsnsDdsStatusType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdsStatus.setDescription('The status of this Discovery Domain Set (DDS).')
isnsDdsMemberTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 2))
if mibBuilder.loadTexts:
    isnsDdsMemberTable.setDescription('A table containing Discovery Domains (DDs) that have\n    been assigned to specific Discovery Domain Sets (DDSs).\n    The number of rows in the table is dependent on the\n    number of DD to DDS relationships in the iSNS instance.')
isnsDdsMemberEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 2, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsDdsId'), (0, 'ISNS-MIB', 'isnsDdsMemberDdId'))
if mibBuilder.loadTexts:
    isnsDdsMemberEntry.setDescription('The mapping of one Discovery Domain (DD) to a Discovery\n    Domain Set (DDS).  This indicates the DD is a member of\n    the DDS.')
isnsDdsMemberDdId = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 2, 1, 1), IsnsDiscoveryDomainId())
if mibBuilder.loadTexts:
    isnsDdsMemberDdId.setDescription('The ID that identifies the Discovery Domain\n    that is a member of the Discovery Domain Set.')
isnsDdsMemberSymbolicName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 4, 2, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdsMemberSymbolicName.setDescription('The Symbolic Name of the Discovery Domain that is a member\n    of this DDS.  This value SHALL be identical to the object\n    isnsDdSymbolicName for the associated DD ID.')
isnsDdInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 5))
isnsDdTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 1))
if mibBuilder.loadTexts:
    isnsDdTable.setDescription('A table containing configuration information for each\n    Discovery Domain (DD) registered in the iSNS.  The number\n    of rows in the table is dependent on the number of DDs\n    registered in the iSNS instance.')
isnsDdEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsDdId'))
if mibBuilder.loadTexts:
    isnsDdEntry.setDescription('Information on a Discovery Domain (DD) registered in\n    the iSNS Server instance.')
isnsDdId = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 1, 1, 1), IsnsDiscoveryDomainId())
if mibBuilder.loadTexts:
    isnsDdId.setDescription('The ID that refers to this Discovery Domain, and the\n    index to the table.')
isnsDdSymbolicName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 1, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdSymbolicName.setDescription('The Discovery Domain Symbolic Name field contains a\n    unique variable-length description (up to 255 bytes)\n    that is associated with the DD.')
isnsDdFeatures = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 1, 1, 3), IsnsDdFeatureType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdFeatures.setDescription('This defines the features the Discovery Domain has.')
isnsDdIscsiMemberTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 2))
if mibBuilder.loadTexts:
    isnsDdIscsiMemberTable.setDescription('A table containing iSCSI node indexes that have been\n    assigned to specific DDs in this iSNS Server instance.  The\n    number of rows in the table is dependent on the number of\n    relationships between iSCSI Nodes and DDs registered in the\n    iSNS instance.')
isnsDdIscsiMemberEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 2, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsDdId'), (0, 'ISNS-MIB', 'isnsDdIscsiMemberIndex'))
if mibBuilder.loadTexts:
    isnsDdIscsiMemberEntry.setDescription('The mapping of one iSCSI Node to a Discovery Domain to\n    indicate membership in the DD.  The indexes are the iSNS\n    server instance, the DD ID of the Discovery Domain, and\n    the iSCSI Node Index of the iSCSI Node.')
isnsDdIscsiMemberIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 2, 1, 1), IsnsNodeIndexId())
if mibBuilder.loadTexts:
    isnsDdIscsiMemberIndex.setDescription('The index for this member iSCSI node entry.')
isnsDdIscsiMemberName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 2, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 223))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdIscsiMemberName.setDescription('The iSCSI Name associated with the storage node.  The\n    iSCSI Name cannot be longer than 223 bytes.  The iSNS\n    server internal maximum size is 224 bytes to provide\n    NULL termination.  This is the iSCSI Name for the storage\n    node that is a member of the DD.  This value maps 1 to 1\n    to the isnsDdIscsiMemberIndex node index.  The iSCSI Name\n    field is too long to be easily used for an index directly.\n    The node index used for a specific node name is only\n    persistent across iSNS Server reinitializations for nodes\n    that are in a Discovery Domain (DD) or are registered\n    control nodes.  This value is only required during row\n    creation if the storage node is not yet registered in the\n    iSNS Server instance.  If the storage node is not yet\n    registered, then the iSCSI Name MUST be provided with the\n    iSCSI node index during row creation in order to create the\n    1-to-1 mapping.')
isnsDdIscsiMemberIsRegistered = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 2, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdIscsiMemberIsRegistered.setDescription('This indicates whether this member of the DD is currently\n    registered in the iSNS Server instance.  iSCSI Storage\n    Node members do not need to be currently registered in\n    order for their iSCSI Name and Index to be added to\n    a DD.')
isnsDdPortalMemberTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3))
if mibBuilder.loadTexts:
    isnsDdPortalMemberTable.setDescription('A table containing currently registered and unregistered\n    portal objects that have been explicitly assigned to\n    specific DDs.  Explicit assignment of a portal to a DD\n    is only done when a specific set of portals are preferred\n    for use within a DD.  Otherwise, for iSCSI, the Portal\n    Group Object should be used for identifying which portals\n    provide access to which storage nodes.  The number of rows\n    in the table is dependent on the number of explicit\n    relationships between portals and DDs registered in the\n    iSNS.')
isnsDdPortalMemberEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsDdId'), (0, 'ISNS-MIB', 'isnsDdPortalMemberIndex'))
if mibBuilder.loadTexts:
    isnsDdPortalMemberEntry.setDescription('Each entry indicates an explicit addition of a portal to a\n    discovery domain.  The explicit addition of an entity portal\n    to a discovery domain indicates the portal is preferred for\n    access to nodes of the entity for this discovery domain.\n    Registered Portal Group objects are used in iSCSI to\n    indicate mapping of portals to nodes across all discovery\n    domains.  Portals that have been explicitly mapped to a\n    discovery domain will be returned as part of a query that\n    is scoped to that discovery domain.  If no portal of an\n    entity has been explicitly mapped to a discovery domain,\n    then all portals of the entity that provide access to a\n    storage node are returned as part of a query.  The table\n    indexes are the server instance, the DD ID of the Discovery\n    Domain, and the Portal Index of the portal.')
isnsDdPortalMemberIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1, 1), IsnsPortalIndexId())
if mibBuilder.loadTexts:
    isnsDdPortalMemberIndex.setDescription('The index for a portal explicitly contained in the discovery\n    domain.  This managed object, combined with isnsServerIndex\n    and isnsDdId, is the key for this table.')
isnsDdPortalMemberAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1, 2), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdPortalMemberAddressType.setDescription('The type of Inet address in isnsDdPortalMemberAddress.  If\n    the address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value\n    of this object is unknown(0), and the value of\n    isnsDdPortalMemberAddress is the zero-length string.')
isnsDdPortalMemberAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1, 3), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdPortalMemberAddress.setDescription('The Inet Address for the portal.  The format of this\n    object is specified by isnsDdPortalMemberAddressType.')
isnsDdPortalMemberPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1, 4), IsnsPortalPortTypeId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdPortalMemberPortType.setDescription('The port type for the portal, either UDP or TCP.')
isnsDdPortalMemberPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1, 5), InetPortNumber().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdPortalMemberPort.setDescription('The port number for the portal.  Whether the portal\n    type is TCP or UDP is indicated by\n    isnsDdPortalMemberPortType.')
isnsDdPortalMemberIsRegistered = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 3, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdPortalMemberIsRegistered.setDescription('This indicates whether this member of the DD is currently\n    registered in the iSNS Server instance.  Portals that are\n    DD members do not need to be currently registered in\n    order for them to be added to a DD.')
isnsDdFcPortMemberTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 4))
if mibBuilder.loadTexts:
    isnsDdFcPortMemberTable.setDescription('A table containing FC Port World Wide Names (WWN) that\n    have been assigned to specific DDs.  The number of rows\n    in the table is dependent on the number of relationships\n    between FC Ports and DDs registered in the iSNS.')
isnsDdFcPortMemberEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 4, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsDdId'), (0, 'ISNS-MIB', 'isnsDdFcPortMemberPortName'))
if mibBuilder.loadTexts:
    isnsDdFcPortMemberEntry.setDescription('The association of one FC Port with a Discovery Domain.\n    Membership of an FC Port in a Discovery Domain is\n    indicated by creating a row for the appropriate DD ID\n    and FC Port WWN.')
isnsDdFcPortMemberPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 4, 1, 1), FcNameIdOrZero().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8))
if mibBuilder.loadTexts:
    isnsDdFcPortMemberPortName.setDescription('The Port WWN of the FC Port that is a member of the DD.  The\n    value MUST be a valid FC WWN, as per the FC-GS (Fibre Channel -\n    Generic Services) standard.  This managed object, combined\n    with the isnsServerIndex and isnsDdId are the key for this\n    table.  A zero-length string is not a valid value for this\n    managed object.')
isnsDdFcPortMemberIsRegistered = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 5, 4, 1, 2), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsDdFcPortMemberIsRegistered.setDescription('This indicates whether this member of the DD is currently\n    registered in the iSNS Server instance.')
isnsReg = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 6))
isnsRegEntityInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1))
isnsRegEntityTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1))
if mibBuilder.loadTexts:
    isnsRegEntityTable.setDescription('A table containing registered Entity objects in each iSNS\n    server instance.  The number of entries in the table is\n    dependent on the number of Entity objects registered in the\n    iSNS Server instances.  All Entity objects are registered in\n    the iSNS using the iSNS protocol.')
isnsRegEntityEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegEntityIndex'))
if mibBuilder.loadTexts:
    isnsRegEntityEntry.setDescription('Information on one registered Entity object in an iSNS\n    server instance.')
isnsRegEntityIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 1), IsnsEntityIndexIdOrZero().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    isnsRegEntityIndex.setDescription('The Entity Index for this entity.  This index is assigned\n    by the iSNS Server when an Entity is initially registered.\n    The Entity Index can be used to represent a registered\n    Entity object in situations where the Entity EID would\n    be too long/unwieldy.  Zero is not a valid value for this\n    object.')
isnsRegEntityEID = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityEID.setDescription('The EID is a unique registered Entity object identifier, as\n    specified in the iSNS Specification.  This is the iSNS\n    Entity Identifier for the registered Entity object.')
isnsRegEntityProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityProtocol.setDescription('The block storage protocol supported by this entity, as\n    defined in the iSNS Specification, Section 6.2.2.  The\n    following values are initially assigned.\n\n              Type Value       Entity Type\n              ----------       -----------\n                 1             No Protocol\n                 2             iSCSI\n                 3             iFCP\n               All Others      As assigned by IANA\n\n    The full set of current Block Storage Protocols are\n    specified in the IANA-maintained registry of assigned\n    iSNS parameters.  Please refer to RFC 4171 and the iSNS\n    parameters maintained at IANA.')
isnsRegEntityManagementAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 4), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityManagementAddressType.setDescription('The type of Inet address in isnsRegEntityManagementAddress.\n    If the address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value of\n    this object is unknown(0), and the value of\n    isnsRegEntityManagementAddress is the zero-length string.')
isnsRegEntityManagementAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 5), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityManagementAddress.setDescription('The iSNS Management IP Address for the registered Entity\n    object.  The format of this object is specified by\n    isnsRegEntityManagementAddressType.')
isnsRegEntityTimestamp = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 6), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityTimestamp.setDescription('The iSNS Entity Registration Timestamp for the registered\n    Entity object.  This is the most recent date and time that\n    the registered Entity object, and associated registered\n    objects contained in the Entity, were registered or\n    updated.')
isnsRegEntityVersionMin = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 7), Unsigned32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 254), ValueRangeConstraint(255, 255)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityVersionMin.setDescription("The minimum version supported for the block storage protocol\n    specified by isnsRegEntityProtocol.  The protocol version\n    specified can be from 1 to 254.  A value of 255 is a wildcard\n    value, indicating no minimum version value has been specified\n    for this Entity.  Entity registrations with an\n    isnsRegEntityProtocol of 'No Protocol' SHALL have an\n    isnsRegEntityVersionMin value of 0.")
isnsRegEntityVersionMax = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 8), Unsigned32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 254), ValueRangeConstraint(255, 255)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityVersionMax.setDescription("The maximum version supported for the block storage protocol\n    specified by isnsRegEntityProtocol.  The protocol version\n    specified can be from 1 to 254.  A value of 255 is a wildcard\n\n\n\n    value, indicating no maximum version value has been specified\n    for this Entity.  Entity registrations with an\n    isnsRegEntityProtocol of 'No Protocol' SHALL have an\n    isnsRegEntityVersionMax value of 0.")
isnsRegEntityRegistrationPeriod = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 1, 1, 9), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityRegistrationPeriod.setDescription('The iSNS Entity Status Inquiry (ESI) registration period,\n    which indicates the maximum time, in seconds, that the\n    registration will be maintained without receipt of an iSNSP\n    message from the entity.  If the Registration Period is set\n    to 0, then the Entity SHALL NOT be deregistered due to no\n    contact with the entity.')
isnsRegEntityNumObjectsTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2))
if mibBuilder.loadTexts:
    isnsRegEntityNumObjectsTable.setDescription('A table containing information on the number of registered\n    objects associated with a registered Entity in the iSNS\n    server instance.  The number of entries in the table is\n    dependent on the number of registered Entity objects in the\n    iSNS.')
isnsRegEntityNumObjectsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegEntityIndex'))
if mibBuilder.loadTexts:
    isnsRegEntityNumObjectsEntry.setDescription('Information on the number of registered objects associated\n    with a registered Entity object in an iSNS Server instance.')
isnsRegEntityInfoNumPortals = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2, 1, 1), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityInfoNumPortals.setDescription('The number of Portals associated with this Entity.')
isnsRegEntityInfoNumPortalGroups = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2, 1, 2), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityInfoNumPortalGroups.setDescription('The number of Portal Groups associated with this Entity.')
isnsRegEntityInfoNumIscsiNodes = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2, 1, 3), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityInfoNumIscsiNodes.setDescription('The number of iSCSI Storage Nodes associated with this\n    Entity.')
isnsRegEntityInfoNumFcPorts = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2, 1, 4), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityInfoNumFcPorts.setDescription('The number of FC Ports associated with this Entity.')
isnsRegEntityInfoNumFcNodes = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 1, 2, 1, 5), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegEntityInfoNumFcNodes.setDescription('The number of FC Nodes associated with this Entity.')
isnsRegPortalInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2))
isnsRegPortalTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1))
if mibBuilder.loadTexts:
    isnsRegPortalTable.setDescription('A table containing the registered Portals in the iSNS.\n    The number of entries is dependent on the number of\n    Portals registered in the iSNS.')
isnsRegPortalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegEntityIndex'), (0, 'ISNS-MIB', 'isnsRegPortalPortalIndex'))
if mibBuilder.loadTexts:
    isnsRegPortalEntry.setDescription('Information on one registered Entity Portal in the iSNS.\n    The Entity Index is part of the table index to quickly\n    find Portals that support a specific Entity.')
isnsRegPortalPortalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 1), IsnsPortalIndexId())
if mibBuilder.loadTexts:
    isnsRegPortalPortalIndex.setDescription('The index for this Entity Portal.')
isnsRegPortalAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 2), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalAddressType.setDescription('The type of Inet address in isnsRegPortalAddress.  If the\n    address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value\n    of this object is unknown(0), and the value of\n    isnsRegPortalAddress is the zero-length string.')
isnsRegPortalAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 3), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalAddress.setDescription('The Inet Address for this Portal as defined in the iSNS\n    Specification, RFC 4171.  The format of this object is\n    specified by isnsRegPortalAddressType.')
isnsRegPortalPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 4), IsnsPortalPortTypeId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalPortType.setDescription('The port type for this Portal, either UDP or TCP, as\n    defined in the iSNS Specification, RFC 4171.')
isnsRegPortalPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 5), InetPortNumber().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalPort.setDescription('The port number for this Portal as defined in the\n    iSNS Specification, RFC 4171.  Whether the Portal type\n    is TCP or UDP is indicated by isnsRegPortalPortType.')
isnsRegPortalSymbolicName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 6), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalSymbolicName.setDescription('The Symbolic Name for this Portal as defined in the iSNS\n    Specification, RFC 4171.  If not provided, then the string\n    SHALL be zero-length.')
isnsRegPortalEsiInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 7), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalEsiInterval.setDescription('The Entity Status Inquiry (ESI) Interval for this Portal\n    as defined in the iSNS Specification, RFC 4171.  A value of\n    0 indicates that ESI monitoring has not been configured for\n    this Portal.')
isnsRegPortalEsiPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 8), IsnsPortalPortTypeId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalEsiPortType.setDescription('The port type for the ESI Port, either UDP or TCP, as\n    defined in the iSNS Specification, RFC 4171.')
isnsRegPortalEsiPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 9), InetPortNumber()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalEsiPort.setDescription('The TCP or UDP port number used for ESI monitoring.  Whether\n    the port type is TCP or UDP is indicated by\n    isnsRegPortalEsiPortType.  A value of 0 indicates that ESI\n    monitoring is not enabled for this Portal.')
isnsRegPortalScnPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 10), IsnsPortalPortTypeId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalScnPortType.setDescription('The port type for the SCN Port, either UDP or TCP, as\n    defined in the iSNS Specification, RFC 4171.')
isnsRegPortalScnPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 11), InetPortNumber()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalScnPort.setDescription('The TCP or UDP port used to receive SCN messages from the\n    iSNS Server.  Whether the port type is TCP or UDP is\n    indicated by isnsRegPortalScnPortType.  A value of 0\n    indicates that SCN message receipt is not enabled for this\n    Portal.')
isnsRegPortalSecurityInfo = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 2, 1, 1, 12), IsnsPortalSecurityType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPortalSecurityInfo.setDescription('Indicates security attribute settings for the Portal as\n    registered in the iSNS server.  The bit for bitmapVALID must\n    be set in order for this attribute to contain valid\n    information.  Setting a bit to 1 indicates the\n    feature is enabled.')
isnsRegPortalGroupInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3))
isnsRegPgTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1))
if mibBuilder.loadTexts:
    isnsRegPgTable.setDescription('A table containing the registered Portal Groups (PGs) in\n    the iSNS Server instance.  The number of entries is\n    dependent on the number of Portal Groups registered in\n    the iSNS.')
isnsRegPgEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegEntityIndex'), (0, 'ISNS-MIB', 'isnsRegPgIndex'))
if mibBuilder.loadTexts:
    isnsRegPgEntry.setDescription('Information on one registered Portal Group in the iSNS\n    server instance.  The Entity Index is part of the table\n    index to quickly find Portal Groups that support Portals\n    and iSCSI Storage Nodes in a specific Entity.')
isnsRegPgIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 1), IsnsPortalGroupIndexId())
if mibBuilder.loadTexts:
    isnsRegPgIndex.setDescription('The PG Index for this node.  The index is created by the\n    iSNS Server instance for uniquely identifying registered\n    objects.  The PG object is registered at the same time a\n    Portal or Storage Node is registered using the iSNS\n    protocol.')
isnsRegPgIscsiNodeIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 2), IsnsNodeIndexId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgIscsiNodeIndex.setDescription('The index for the iSCSI Node associated with this PG.\n    This index can be used to reference the\n    isnsRegIscsiNodeTable.')
isnsRegPgIscsiName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 3), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 223))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgIscsiName.setDescription('The iSCSI Name of the initiator or target associated with\n    the storage node.  The iSCSI Name cannot be longer than\n    223 bytes.  The iSNS Server internal maximum size is 224\n    bytes to provide NULL termination.  This is the PG iSCSI\n    Name that uniquely identifies the iSCSI Storage Node that\n    is associated with this PG.')
isnsRegPgPortalPortalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 4), IsnsPortalIndexId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgPortalPortalIndex.setDescription('The Portal Index for the Portal associated with this PG.\n    This index can be used to reference the isnsRegPortalTable.')
isnsRegPgPortalAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 5), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgPortalAddressType.setDescription('The type of Inet address in isnsRegPgPortalAddress.  If\n    the address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value\n    of this object is unknown(0), and the value of\n    isnsRegPgPortalAddress is the zero-length string.')
isnsRegPgPortalAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 6), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgPortalAddress.setDescription('The Inet Address for the Portal that is associated with\n    the PG.  The format of this object is specified by\n    isnsRegPgPortalAddressType.')
isnsRegPgPortalPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 7), IsnsPortalPortTypeId()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgPortalPortType.setDescription('The port type, either UDP or TCP, for the Portal that\n    is associated with this registered PG object.')
isnsRegPgPortalPort = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 8), InetPortNumber().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgPortalPort.setDescription('The port number for the Portal that is associated with\n    this registered PG object.  Whether the Portal type is\n    TCP or UDP is indicated by isnsRegPgPortalPortType.')
isnsRegPgPGT = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 3, 1, 1, 9), IsnsPortalGroupTagIdOrNull()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegPgPGT.setDescription('The Portal Group Tag (PGT) for the registered iSCSI Portal\n    Group object in an iSNS Server instance.  This indicates\n    the tag value that the Portal uses for access to the iSCSI\n    Storage Node.  The PGT is used for coordinated access\n    between multiple Portals, as described in the iSCSI\n    Specification, RFC 3720.  A PGT with no association is a\n    NULL value.  The value of -1 indicates a NULL value.')
isnsRegIscsiNodeInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4))
isnsRegIscsiNodeTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1))
if mibBuilder.loadTexts:
    isnsRegIscsiNodeTable.setDescription("A table containing the registered iSCSI Nodes in the iSNS\n    server instance.  Storage devices register using the iSNS\n    protocol.  While a device cannot be registered in an iSNS\n    server using SNMP, an entry can be deleted in order to\n    remove 'stale' entries.  The number of entries is related\n    to the number of iSCSI nodes registered in the iSNS.")
isnsRegIscsiNodeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegEntityIndex'), (0, 'ISNS-MIB', 'isnsRegIscsiNodeIndex'))
if mibBuilder.loadTexts:
    isnsRegIscsiNodeEntry.setDescription('Information on one iSCSI node that has been registered in\n    the iSNS Server instance.  New rows cannot be added using\n    SNMP.')
isnsRegIscsiNodeIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 1), IsnsNodeIndexId())
if mibBuilder.loadTexts:
    isnsRegIscsiNodeIndex.setDescription('The index for this iSCSI node.')
isnsRegIscsiNodeName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 223))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegIscsiNodeName.setDescription('The iSCSI Name of the initiator or target associated with\n    the storage node.  The iSCSI Name cannot be longer than\n    223 bytes.  The iSNS Server internal maximum size is 224\n    bytes to provide NULL termination.  This is the iSCSI Name\n    that uniquely identifies the initiator, initiator/target,\n    target, or control node in the network.')
isnsRegIscsiNodeType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 3), IsnsIscsiNodeType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegIscsiNodeType.setDescription('The Node Type defining the functions of this iSCSI node.')
isnsRegIscsiNodeAlias = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 4), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegIscsiNodeAlias.setDescription('The Alias name of the iSCSI node.  This is a variable-length\n    text-based description of up to 255 bytes.')
isnsRegIscsiNodeScnTypes = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 5), IsnsIscsiScnType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegIscsiNodeScnTypes.setDescription('The State Change Notification (SCN) types enabled for this\n    iSCSI node.')
isnsRegIscsiNodeWwnToken = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 6), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegIscsiNodeWwnToken.setDescription('This contains a globally unique 64-bit integer value that\n    can be used to represent the World Wide Node Name of the\n    iSCSI device in a Fibre Channel fabric.  This identifier is\n    used during the device registration process, and MUST\n    conform to the requirements in RFC 4171.  A zero-length string\n    for this managed object indicates that a Node WWN token has\n    not been assigned.')
isnsRegIscsiNodeAuthMethod = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 4, 1, 1, 7), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegIscsiNodeAuthMethod.setDescription('This attribute contains a null-terminated string containing\n    UTF-8 text listing the iSCSI authentication methods enabled\n    for this iSCSI Node, in order of preference.  The text\n    values used to identify iSCSI authentication methods are\n    embedded in this string attribute and delineated by a\n    comma.  The text values are identical to those found in\n    RFC 3720 - iSCSI.  Additional vendor-specific text values\n    are also possible.')
isnsRegFcNodeInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5))
isnsRegFcNodeTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1))
if mibBuilder.loadTexts:
    isnsRegFcNodeTable.setDescription('A table containing the registered FC Nodes in the iSNS.\n    This supports iFCP as defined in RFC 4172.')
isnsRegFcNodeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegFcNodeWwnn'))
if mibBuilder.loadTexts:
    isnsRegFcNodeEntry.setDescription('Information on one registered FC node that has been\n    registered in the iSNS.')
isnsRegFcNodeWwnn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 1), FcNameIdOrZero().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8))
if mibBuilder.loadTexts:
    isnsRegFcNodeWwnn.setDescription('The FC Node World Wide Node Name as defined in the iSNS\n    Specification, RFC 4171.  A zero-length string is not valid\n    for this managed object.')
isnsRegFcNodeSymbolicName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodeSymbolicName.setDescription('The FC Node Symbolic Name of the node as defined in the\n    iSNS Specification, RFC 4171.  This is a variable-length\n    text-based description.  If not provided, then the string\n    SHALL be zero-length.')
isnsRegFcNodeAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 3), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodeAddressType.setDescription('The type of Inet address in isnsRegFcNodeAddress.  If\n    the address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value\n    of this object is unknown(0), and the value of\n    isnsRegFcNodeAddress is the zero-length string.')
isnsRegFcNodeAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 4), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodeAddress.setDescription('The FC Node Inet address of the node as defined in the\n    iSNS Specification, RFC 4171.  The format of this object is\n    specified by isnsRegFcNodeAddressType.')
isnsRegFcNodeIPA = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodeIPA.setDescription('This managed object identifies the FC Initial Process\n    Associator of the node as defined in the iSNS\n    Specification, RFC 4171.')
isnsRegFcNodeProxyIscsiName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 6), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 223))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodeProxyIscsiName.setDescription('The iSCSI Name used to represent the FC Node in the IP\n    network.  It is used as a pointer to the matching iSCSI Name\n    entry in the iSNS Server.  Its value is usually registered\n    by an FC-iSCSI gateway connecting the IP network to the\n    fabric containing the FC device.')
isnsRegFcNodeNumFcPorts = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 1, 1, 7), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodeNumFcPorts.setDescription('The number of FC Ports associated with this FC Node.')
isnsRegFcPortTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2))
if mibBuilder.loadTexts:
    isnsRegFcPortTable.setDescription('Information on registered FC N_Ports in the iSNS.  FC Ports\n    are associated with registered FC Nodes.  This supports\n    iFCP as defined in RFC 4172.')
isnsRegFcPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegEntityIndex'), (0, 'ISNS-MIB', 'isnsRegFcPortWwpn'))
if mibBuilder.loadTexts:
    isnsRegFcPortEntry.setDescription('Information on one FC Port that has been registered in\n    iSNS.')
isnsRegFcPortWwpn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 1), FcNameIdOrZero().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8))
if mibBuilder.loadTexts:
    isnsRegFcPortWwpn.setDescription("The FC Port's World Wide Port Name as defined in the iSNS\n    Specification, RFC 4171.  A zero-length string is not valid\n    for this managed object.")
isnsRegFcPortID = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 2), FcAddressIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortID.setDescription("The FC Port's Port ID as defined in the iSNS Specification,\n    RFC 4171.")
isnsRegFcPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortType.setDescription("The FC Port Type as defined in the iSNS Specification,\n    RFC 4171, and the Fibre Channel Generic Services\n    Specification.  Current values are as shown below:\n           unknown      (0),\n           nPort        (1),\n\n\n\n           nlPort       (2),\n           fNlPort      (3),\n           fPort        (129),     -- x'81'\n           flPort       (130),     -- x'82'\n           ePort        (132),     -- x'84'\n           bPort        (133),     -- x'85'\n           mFcpPort     (65297),   -- x'FF11'\n           iFcpPort     (65298),   -- x'FF12'\n           unknownEnd   (65535)\n    The future assignment of any additional values will be\n    documented in a revision of RFC 4171.")
isnsRegFcPortSymbolicName = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 4), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortSymbolicName.setDescription('The FC Port Symbolic Name as defined in the iSNS\n    Specification, RFC 4171.  If not provided, then the\n    string SHALL be zero-length.')
isnsRegFcPortFabricPortWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 5), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortFabricPortWwn.setDescription('The Fabric Port WWN for this entry as defined in the iSNS\n    Specification, RFC 4171.  A zero-length string for this\n    managed object indicates that the Fabric Port WWN is not\n    known, or has not yet been registered with the iSNS Server.')
isnsRegFcPortHA = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 6), FcAddressIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortHA.setDescription('The FC Port Hard Address as defined in the iSNS\n    Specification, RFC 4171.')
isnsRegFcPortAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 7), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortAddressType.setDescription('The type of Inet address in isnsRegFcPortAddress.  If\n    the address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value\n    of this object is unknown(0), and the value of\n    isnsRegFcPortAddress is the zero-length string.')
isnsRegFcPortAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 8), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortAddress.setDescription('The FC Port Inet Address as defined in the iSNS\n    Specification, RFC 4171.  The format of this object is\n    specified by isnsRegFcPortAddressType.')
isnsRegFcPortFcCos = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 9), IsnsFcClassOfServiceType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortFcCos.setDescription('The FC Port Class of Service as defined in the iSNS\n    Specification, RFC 4171.')
isnsRegFcPortFc4Types = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 10), OctetString().subtype(subtypeSpec=ValueSizeConstraint(32, 32)).setFixedLength(32)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortFc4Types.setDescription('The FC Port FC-4 Types as defined in the iSNS\n    Specification, RFC 4171.')
isnsRegFcPortFc4Descr = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 11), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(4, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortFc4Descr.setDescription('The FC Port FC-4 Descriptor as defined in the iSNS\n    Specification, RFC 4171.  The FC-4 Descriptor cannot be\n    longer than 255 bytes.  The iSNS Server internal maximum\n    size is 256 bytes to provide NULL termination.')
isnsRegFcPortFc4Features = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 12), OctetString().subtype(subtypeSpec=ValueSizeConstraint(128, 128)).setFixedLength(128)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortFc4Features.setDescription('The FC Port FC-4 Features as defined in the iSNS\n    Specification, RFC 4171.')
isnsRegFcPortScnTypes = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 13), IsnsIfcpScnType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortScnTypes.setDescription('The iFCP State Change Notification (SCN) types enabled for\n    the registered object.')
isnsRegFcPortRole = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 14), IsnsFcPortRoleType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortRole.setDescription('The FC Port Role defines the role of the registered\n    object.')
isnsRegFcPortFcNodeWwnn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 15), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortFcNodeWwnn.setDescription('The FC Node World Wide Node Name that is associated with\n    this FC Port as defined in the iSNS Specification, RFC 4171.\n    This managed object may contain a zero-length string prior\n    to a device registering this value with the iSNS Server.')
isnsRegFcPortPpnWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 2, 1, 16), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcPortPpnWwn.setDescription('The Permanent Port Name (PPN) attribute is the FC Port Name WWPN\n    of the first Storage Node registered in the iSNS Database\n    that is associated with a particular FC Device (FC Node).\n    The PPN of all subsequent Storage Node registrations that\n    are associated with that FC Device (FC Node) SHALL be set\n    to the FC Port Name WWPN of the first Storage Node, as\n    defined in the iSNS Specification, RFC 4171.  This managed\n    object may contain a zero-length string prior to a device\n    registering this value with the iSNS Server.')
isnsRegFcNodePortTable = MibTable((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 3))
if mibBuilder.loadTexts:
    isnsRegFcNodePortTable.setDescription('A table containing the mapping of a registered FC Node and\n    associated registered iFCP Port to the supporting registered\n    Entity object in an iSNS Server instance.')
isnsRegFcNodePortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 3, 1)).setIndexNames((0, 'ISNS-MIB', 'isnsServerIndex'), (0, 'ISNS-MIB', 'isnsRegFcNodeWwnn'), (0, 'ISNS-MIB', 'isnsRegFcPortWwpn'))
if mibBuilder.loadTexts:
    isnsRegFcNodePortEntry.setDescription('Information on one mapping from an FC Node and iFCP Port to\n    an Entity object registered in an iSNS.')
isnsRegFcNodePortEntityIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 163, 1, 1, 6, 5, 3, 1, 1), IsnsEntityIndexIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    isnsRegFcNodePortEntityIndex.setDescription('The Entity Index for the registered Entity object\n    associated with the FC Port and FC Node.  This managed\n    object may contain the value of zero prior to a device\n    registering this value with the iSNS Server.')
isnsNotificationsInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 1, 2))
isnsInstanceInfo = MibScalar((1, 3, 6, 1, 2, 1, 163, 1, 2, 1), SnmpAdminString()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    isnsInstanceInfo.setDescription('Textual information about the notification event and the\n    iSNS Server generating the notification.  An example is:\n    iSNS Server Started.')
isnsAddressNotificationType = MibScalar((1, 3, 6, 1, 2, 1, 163, 1, 2, 2), InetAddressType()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    isnsAddressNotificationType.setDescription('The type of Inet address in isnsAddressNotification.  If\n    the address is specified, then it must be a valid unicast\n    address and the value of this object must be ipv4(1),\n    ipv6(2), ipv4z(3), or ipv6z(4); otherwise, the value\n    of this object is unknown(0), and the value of\n    isnsAddressNotification is the zero-length string.')
isnsAddressNotification = MibScalar((1, 3, 6, 1, 2, 1, 163, 1, 2, 3), InetAddress()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    isnsAddressNotification.setDescription('Identifies the IP address of the iSNS Server.  The format of\n\n\n\n    this object is specified by isnsAddressNotificationType.\n    The IP address will always be specified in the notification\n    unless an error causes the IP address to not be known.')
isnsTcpPortNotification = MibScalar((1, 3, 6, 1, 2, 1, 163, 1, 2, 4), InetPortNumber()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    isnsTcpPortNotification.setDescription('Indicates the TCP port the iSNS Server is using,\n    or 0 if TCP-based registrations are not supported.')
isnsUdpPortNotification = MibScalar((1, 3, 6, 1, 2, 1, 163, 1, 2, 5), InetPortNumber()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    isnsUdpPortNotification.setDescription('Indicates the UDP port the iSNS Server is using,\n    or 0 if UDP-based registrations are not supported.')
isnsServerStart = NotificationType((1, 3, 6, 1, 2, 1, 163, 0, 1)).setObjects(*(('ISNS-MIB', 'isnsInstanceInfo'), ('ISNS-MIB', 'isnsAddressNotificationType'), ('ISNS-MIB', 'isnsAddressNotification'), ('ISNS-MIB', 'isnsTcpPortNotification'), ('ISNS-MIB', 'isnsUdpPortNotification')))
if mibBuilder.loadTexts:
    isnsServerStart.setDescription('This notification is sent when an iSNS Server begins\n    operation.  The notification provides the following:\n           isnsInstanceInfo : iSNS Server textual information\n           isnsAddressTypeNotification : iSNS Server address type\n           isnsAddressNotification : iSNS Server address\n           isnsTcpPortNotification : iSNS Server TCP Port\n           isnsUdpPortNotification : iSNS Server UDP Port\n   ')
isnsServerShutdown = NotificationType((1, 3, 6, 1, 2, 1, 163, 0, 2)).setObjects(*(('ISNS-MIB', 'isnsInstanceInfo'), ('ISNS-MIB', 'isnsAddressNotificationType'), ('ISNS-MIB', 'isnsAddressNotification'), ('ISNS-MIB', 'isnsTcpPortNotification'), ('ISNS-MIB', 'isnsUdpPortNotification')))
if mibBuilder.loadTexts:
    isnsServerShutdown.setDescription('This notification is sent when an iSNS Server is\n    shutdown.  The notification provides the following:\n           isnsInstanceInfo : iSNS Server textual information\n           isnsAddressTypeNotification : iSNS Server address type\n           isnsAddressNotification : iSNS Server address\n           isnsTcpPortNotification : iSNS Server TCP Port\n           isnsUdpPortNotification : iSNS Server UDP Port\n   ')
isnsCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 2, 1))
isnsIscsiServerCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 163, 2, 1, 1)).setObjects(*(('ISNS-MIB', 'isnsServerAttributesGroup'), ('ISNS-MIB', 'isnsServerIscsiControlNodeGroup'), ('ISNS-MIB', 'isnsServerIscsiDdsDdObjGroup'), ('ISNS-MIB', 'isnsServerRegIscsiObjGroup'), ('ISNS-MIB', 'isnsServerNumObjectsGroup'), ('ISNS-MIB', 'isnsNotificationsObjGroup'), ('ISNS-MIB', 'isnsServerNotificationGroup')))
if mibBuilder.loadTexts:
    isnsIscsiServerCompliance.setDescription('Initial compliance statement for an iSNS Server\n    providing support to iSCSI clients.')
isnsIfcpServerCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 163, 2, 1, 2)).setObjects(*(('ISNS-MIB', 'isnsServerAttributesGroup'), ('ISNS-MIB', 'isnsServerIfcpPortControlNodeGroup'), ('ISNS-MIB', 'isnsServerIfcpDdsDdObjGroup'), ('ISNS-MIB', 'isnsServerRegIfcpObjGroup'), ('ISNS-MIB', 'isnsServerNumObjectsGroup'), ('ISNS-MIB', 'isnsNotificationsObjGroup'), ('ISNS-MIB', 'isnsServerNotificationGroup')))
if mibBuilder.loadTexts:
    isnsIfcpServerCompliance.setDescription('Initial compliance statement for an iSNS Server\n    providing support to iFCP Clients.')
isnsGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 163, 2, 2))
isnsServerAttributesGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 1)).setObjects(*(('ISNS-MIB', 'isnsServerName'), ('ISNS-MIB', 'isnsServerIsnsVersion'), ('ISNS-MIB', 'isnsServerVendorInfo'), ('ISNS-MIB', 'isnsServerPhysicalIndex'), ('ISNS-MIB', 'isnsServerTcpPort'), ('ISNS-MIB', 'isnsServerUdpPort'), ('ISNS-MIB', 'isnsServerDiscontinuityTime'), ('ISNS-MIB', 'isnsServerRole'), ('ISNS-MIB', 'isnsServerDiscoveryMethodsEnabled'), ('ISNS-MIB', 'isnsServerDiscoveryMcGroupType'), ('ISNS-MIB', 'isnsServerDiscoveryMcGroupAddress'), ('ISNS-MIB', 'isnsServerEsiNonResponseThreshold'), ('ISNS-MIB', 'isnsServerEnableControlNodeMgtScn'), ('ISNS-MIB', 'isnsServerDefaultDdDdsStatus'), ('ISNS-MIB', 'isnsServerUpdateDdDdsSupported'), ('ISNS-MIB', 'isnsServerUpdateDdDdsEnabled')))
if mibBuilder.loadTexts:
    isnsServerAttributesGroup.setDescription('iSNS Server attributes.')
isnsServerNumObjectsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 2)).setObjects(*(('ISNS-MIB', 'isnsNumDds'), ('ISNS-MIB', 'isnsNumDd'), ('ISNS-MIB', 'isnsNumEntities'), ('ISNS-MIB', 'isnsNumPortals'), ('ISNS-MIB', 'isnsNumPortalGroups'), ('ISNS-MIB', 'isnsNumIscsiNodes'), ('ISNS-MIB', 'isnsNumFcPorts'), ('ISNS-MIB', 'isnsNumFcNodes'), ('ISNS-MIB', 'isnsRegEntityInfoNumPortals'), ('ISNS-MIB', 'isnsRegEntityInfoNumPortalGroups'), ('ISNS-MIB', 'isnsRegEntityInfoNumIscsiNodes'), ('ISNS-MIB', 'isnsRegEntityInfoNumFcPorts'), ('ISNS-MIB', 'isnsRegEntityInfoNumFcNodes')))
if mibBuilder.loadTexts:
    isnsServerNumObjectsGroup.setDescription('Managed objects indicating the number of registered objects\n    in an iSNS Server or the number of registered objects\n    associated with a registered Entity.  These managed objects\n    are optional to implement.')
isnsServerIscsiControlNodeGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 3)).setObjects(*(('ISNS-MIB', 'isnsControlNodeIscsiNodeName'), ('ISNS-MIB', 'isnsControlNodeIscsiIsRegistered'), ('ISNS-MIB', 'isnsControlNodeIscsiRcvMgtSCN')))
if mibBuilder.loadTexts:
    isnsServerIscsiControlNodeGroup.setDescription('iSNS Server iSCSI control node managed objects.')
isnsServerIfcpPortControlNodeGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 4)).setObjects(*(('ISNS-MIB', 'isnsControlNodeFcPortIsRegistered'), ('ISNS-MIB', 'isnsControlNodeFcPortRcvMgtSCN')))
if mibBuilder.loadTexts:
    isnsServerIfcpPortControlNodeGroup.setDescription('iSNS Server iFCP Port control node managed objects.')
isnsServerIscsiDdsDdObjGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 5)).setObjects(*(('ISNS-MIB', 'isnsDdsSymbolicName'), ('ISNS-MIB', 'isnsDdsStatus'), ('ISNS-MIB', 'isnsDdsMemberSymbolicName'), ('ISNS-MIB', 'isnsDdSymbolicName'), ('ISNS-MIB', 'isnsDdFeatures'), ('ISNS-MIB', 'isnsDdIscsiMemberName'), ('ISNS-MIB', 'isnsDdIscsiMemberIsRegistered'), ('ISNS-MIB', 'isnsDdPortalMemberAddressType'), ('ISNS-MIB', 'isnsDdPortalMemberAddress'), ('ISNS-MIB', 'isnsDdPortalMemberPortType'), ('ISNS-MIB', 'isnsDdPortalMemberPort'), ('ISNS-MIB', 'isnsDdPortalMemberIsRegistered')))
if mibBuilder.loadTexts:
    isnsServerIscsiDdsDdObjGroup.setDescription('iSNS Server DDS and DD managed objects for iSCSI.')
isnsServerIfcpDdsDdObjGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 6)).setObjects(*(('ISNS-MIB', 'isnsDdsSymbolicName'), ('ISNS-MIB', 'isnsDdsStatus'), ('ISNS-MIB', 'isnsDdSymbolicName'), ('ISNS-MIB', 'isnsDdFeatures'), ('ISNS-MIB', 'isnsDdPortalMemberAddressType'), ('ISNS-MIB', 'isnsDdPortalMemberAddress'), ('ISNS-MIB', 'isnsDdPortalMemberPortType'), ('ISNS-MIB', 'isnsDdPortalMemberPort'), ('ISNS-MIB', 'isnsDdPortalMemberIsRegistered'), ('ISNS-MIB', 'isnsDdFcPortMemberIsRegistered')))
if mibBuilder.loadTexts:
    isnsServerIfcpDdsDdObjGroup.setDescription('iSNS Server DDS and DD managed objects for iFCP.')
isnsServerRegIscsiObjGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 7)).setObjects(*(('ISNS-MIB', 'isnsRegEntityEID'), ('ISNS-MIB', 'isnsRegEntityProtocol'), ('ISNS-MIB', 'isnsRegEntityManagementAddressType'), ('ISNS-MIB', 'isnsRegEntityManagementAddress'), ('ISNS-MIB', 'isnsRegEntityTimestamp'), ('ISNS-MIB', 'isnsRegEntityVersionMin'), ('ISNS-MIB', 'isnsRegEntityVersionMax'), ('ISNS-MIB', 'isnsRegEntityRegistrationPeriod'), ('ISNS-MIB', 'isnsRegEntityInfoNumPortals'), ('ISNS-MIB', 'isnsRegEntityInfoNumPortalGroups'), ('ISNS-MIB', 'isnsRegEntityInfoNumIscsiNodes'), ('ISNS-MIB', 'isnsRegEntityInfoNumFcPorts'), ('ISNS-MIB', 'isnsRegEntityInfoNumFcNodes'), ('ISNS-MIB', 'isnsRegPortalAddressType'), ('ISNS-MIB', 'isnsRegPortalAddress'), ('ISNS-MIB', 'isnsRegPortalPortType'), ('ISNS-MIB', 'isnsRegPortalPort'), ('ISNS-MIB', 'isnsRegPortalSymbolicName'), ('ISNS-MIB', 'isnsRegPortalEsiInterval'), ('ISNS-MIB', 'isnsRegPortalEsiPortType'), ('ISNS-MIB', 'isnsRegPortalEsiPort'), ('ISNS-MIB', 'isnsRegPortalScnPortType'), ('ISNS-MIB', 'isnsRegPortalScnPort'), ('ISNS-MIB', 'isnsRegPortalSecurityInfo'), ('ISNS-MIB', 'isnsRegPgIscsiNodeIndex'), ('ISNS-MIB', 'isnsRegPgIscsiName'), ('ISNS-MIB', 'isnsRegPgPortalPortalIndex'), ('ISNS-MIB', 'isnsRegPgPortalAddressType'), ('ISNS-MIB', 'isnsRegPgPortalAddress'), ('ISNS-MIB', 'isnsRegPgPortalPortType'), ('ISNS-MIB', 'isnsRegPgPortalPort'), ('ISNS-MIB', 'isnsRegPgPGT'), ('ISNS-MIB', 'isnsRegIscsiNodeName'), ('ISNS-MIB', 'isnsRegIscsiNodeType'), ('ISNS-MIB', 'isnsRegIscsiNodeAlias'), ('ISNS-MIB', 'isnsRegIscsiNodeScnTypes'), ('ISNS-MIB', 'isnsRegIscsiNodeWwnToken'), ('ISNS-MIB', 'isnsRegIscsiNodeAuthMethod')))
if mibBuilder.loadTexts:
    isnsServerRegIscsiObjGroup.setDescription('iSNS Server registered iSCSI managed objects.')
isnsServerRegIfcpObjGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 8)).setObjects(*(('ISNS-MIB', 'isnsRegEntityEID'), ('ISNS-MIB', 'isnsRegEntityProtocol'), ('ISNS-MIB', 'isnsRegEntityManagementAddressType'), ('ISNS-MIB', 'isnsRegEntityManagementAddress'), ('ISNS-MIB', 'isnsRegEntityTimestamp'), ('ISNS-MIB', 'isnsRegEntityVersionMin'), ('ISNS-MIB', 'isnsRegEntityVersionMax'), ('ISNS-MIB', 'isnsRegEntityRegistrationPeriod'), ('ISNS-MIB', 'isnsRegEntityInfoNumPortals'), ('ISNS-MIB', 'isnsRegEntityInfoNumPortalGroups'), ('ISNS-MIB', 'isnsRegEntityInfoNumIscsiNodes'), ('ISNS-MIB', 'isnsRegEntityInfoNumFcPorts'), ('ISNS-MIB', 'isnsRegEntityInfoNumFcNodes'), ('ISNS-MIB', 'isnsRegPortalAddressType'), ('ISNS-MIB', 'isnsRegPortalAddress'), ('ISNS-MIB', 'isnsRegPortalPortType'), ('ISNS-MIB', 'isnsRegPortalPort'), ('ISNS-MIB', 'isnsRegPortalSymbolicName'), ('ISNS-MIB', 'isnsRegPortalEsiInterval'), ('ISNS-MIB', 'isnsRegPortalEsiPortType'), ('ISNS-MIB', 'isnsRegPortalEsiPort'), ('ISNS-MIB', 'isnsRegPortalScnPortType'), ('ISNS-MIB', 'isnsRegPortalScnPort'), ('ISNS-MIB', 'isnsRegPortalSecurityInfo'), ('ISNS-MIB', 'isnsRegFcPortID'), ('ISNS-MIB', 'isnsRegFcPortType'), ('ISNS-MIB', 'isnsRegFcPortSymbolicName'), ('ISNS-MIB', 'isnsRegFcPortFabricPortWwn'), ('ISNS-MIB', 'isnsRegFcPortHA'), ('ISNS-MIB', 'isnsRegFcPortAddressType'), ('ISNS-MIB', 'isnsRegFcPortAddress'), ('ISNS-MIB', 'isnsRegFcPortFcCos'), ('ISNS-MIB', 'isnsRegFcPortFc4Types'), ('ISNS-MIB', 'isnsRegFcPortFc4Descr'), ('ISNS-MIB', 'isnsRegFcPortFc4Features'), ('ISNS-MIB', 'isnsRegFcPortScnTypes'), ('ISNS-MIB', 'isnsRegFcPortRole'), ('ISNS-MIB', 'isnsRegFcPortFcNodeWwnn'), ('ISNS-MIB', 'isnsRegFcPortPpnWwn'), ('ISNS-MIB', 'isnsRegFcNodeSymbolicName'), ('ISNS-MIB', 'isnsRegFcNodeAddressType'), ('ISNS-MIB', 'isnsRegFcNodeAddress'), ('ISNS-MIB', 'isnsRegFcNodeIPA'), ('ISNS-MIB', 'isnsRegFcNodeProxyIscsiName'), ('ISNS-MIB', 'isnsRegFcNodeNumFcPorts'), ('ISNS-MIB', 'isnsRegFcNodePortEntityIndex')))
if mibBuilder.loadTexts:
    isnsServerRegIfcpObjGroup.setDescription('iSNS Server registered iFCP managed objects.')
isnsNotificationsObjGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 9)).setObjects(*(('ISNS-MIB', 'isnsInstanceInfo'), ('ISNS-MIB', 'isnsAddressNotificationType'), ('ISNS-MIB', 'isnsAddressNotification'), ('ISNS-MIB', 'isnsTcpPortNotification'), ('ISNS-MIB', 'isnsUdpPortNotification')))
if mibBuilder.loadTexts:
    isnsNotificationsObjGroup.setDescription('iSNS Notification managed objects.')
isnsServerNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 163, 2, 2, 10)).setObjects(*(('ISNS-MIB', 'isnsServerStart'), ('ISNS-MIB', 'isnsServerShutdown')))
if mibBuilder.loadTexts:
    isnsServerNotificationGroup.setDescription('iSNS Server Notification managed objects.')
mibBuilder.exportSymbols('ISNS-MIB', IsnsDiscoveryDomainSetId=IsnsDiscoveryDomainSetId, isnsRegEntityEID=isnsRegEntityEID, isnsRegEntityInfo=isnsRegEntityInfo, isnsRegFcPortFc4Types=isnsRegFcPortFc4Types, isnsRegEntityVersionMax=isnsRegEntityVersionMax, isnsNumPortalGroups=isnsNumPortalGroups, isnsDdsMemberDdId=isnsDdsMemberDdId, isnsNotificationsInfo=isnsNotificationsInfo, isnsRegPortalEsiInterval=isnsRegPortalEsiInterval, isnsRegEntityManagementAddress=isnsRegEntityManagementAddress, isnsControlNodeIscsiEntry=isnsControlNodeIscsiEntry, IsnsIscsiScnType=IsnsIscsiScnType, isnsRegEntityProtocol=isnsRegEntityProtocol, isnsRegFcPortRole=isnsRegFcPortRole, isnsRegIscsiNodeScnTypes=isnsRegIscsiNodeScnTypes, isnsRegFcPortPpnWwn=isnsRegFcPortPpnWwn, isnsServerIscsiControlNodeGroup=isnsServerIscsiControlNodeGroup, isnsDdIscsiMemberName=isnsDdIscsiMemberName, isnsRegIscsiNodeInfo=isnsRegIscsiNodeInfo, isnsRegFcNodeNumFcPorts=isnsRegFcNodeNumFcPorts, IsnsIscsiNodeType=IsnsIscsiNodeType, isnsRegEntityInfoNumPortalGroups=isnsRegEntityInfoNumPortalGroups, IsnsFcClassOfServiceType=IsnsFcClassOfServiceType, IsnsDiscoveryDomainId=IsnsDiscoveryDomainId, IsnsPortalSecurityType=IsnsPortalSecurityType, isnsServerName=isnsServerName, isnsRegFcPortType=isnsRegFcPortType, isnsDdIscsiMemberTable=isnsDdIscsiMemberTable, isnsRegEntityInfoNumFcPorts=isnsRegEntityInfoNumFcPorts, isnsRegFcNodePortEntityIndex=isnsRegFcNodePortEntityIndex, isnsAddressNotification=isnsAddressNotification, isnsServerUdpPort=isnsServerUdpPort, isnsRegFcPortWwpn=isnsRegFcPortWwpn, isnsIfcpServerCompliance=isnsIfcpServerCompliance, isnsDdsSymbolicName=isnsDdsSymbolicName, isnsServerIfcpDdsDdObjGroup=isnsServerIfcpDdsDdObjGroup, isnsNumDd=isnsNumDd, isnsRegPortalInfo=isnsRegPortalInfo, isnsConformance=isnsConformance, isnsRegFcNodeWwnn=isnsRegFcNodeWwnn, isnsRegEntityRegistrationPeriod=isnsRegEntityRegistrationPeriod, isnsRegFcPortFc4Descr=isnsRegFcPortFc4Descr, isnsRegPgPortalPortalIndex=isnsRegPgPortalPortalIndex, isnsControlNodeIscsiNodeIndex=isnsControlNodeIscsiNodeIndex, isnsRegFcNodeAddressType=isnsRegFcNodeAddressType, isnsDdEntry=isnsDdEntry, isnsAddressNotificationType=isnsAddressNotificationType, isnsRegEntityTable=isnsRegEntityTable, isnsRegPgPortalAddress=isnsRegPgPortalAddress, isnsDdIscsiMemberIndex=isnsDdIscsiMemberIndex, isnsDdPortalMemberAddressType=isnsDdPortalMemberAddressType, isnsRegFcPortFabricPortWwn=isnsRegFcPortFabricPortWwn, isnsServerUpdateDdDdsSupported=isnsServerUpdateDdDdsSupported, isnsNumFcNodes=isnsNumFcNodes, isnsControlNodeFcPortWwpn=isnsControlNodeFcPortWwpn, isnsRegFcPortSymbolicName=isnsRegFcPortSymbolicName, isnsNumEntities=isnsNumEntities, isnsRegPgEntry=isnsRegPgEntry, isnsRegEntityNumObjectsTable=isnsRegEntityNumObjectsTable, IsnsPortalGroupTagIdOrNull=IsnsPortalGroupTagIdOrNull, isnsServerUpdateDdDdsEnabled=isnsServerUpdateDdDdsEnabled, isnsServerNumObjectsGroup=isnsServerNumObjectsGroup, isnsServerStart=isnsServerStart, IsnsSrvrDiscoveryMethodsType=IsnsSrvrDiscoveryMethodsType, isnsServerEsiNonResponseThreshold=isnsServerEsiNonResponseThreshold, isnsServerRegIscsiObjGroup=isnsServerRegIscsiObjGroup, isnsRegFcNodeEntry=isnsRegFcNodeEntry, isnsControlNodeFcPortEntry=isnsControlNodeFcPortEntry, isnsControlNodeFcPortRcvMgtSCN=isnsControlNodeFcPortRcvMgtSCN, isnsDdInfo=isnsDdInfo, isnsRegFcPortFcCos=isnsRegFcPortFcCos, isnsRegPortalScnPort=isnsRegPortalScnPort, isnsRegFcPortFc4Features=isnsRegFcPortFc4Features, isnsControlNodeFcPortTable=isnsControlNodeFcPortTable, isnsRegPgIscsiNodeIndex=isnsRegPgIscsiNodeIndex, isnsRegPortalGroupInfo=isnsRegPortalGroupInfo, isnsControlNodeIscsiNodeName=isnsControlNodeIscsiNodeName, isnsRegEntityVersionMin=isnsRegEntityVersionMin, isnsRegEntityInfoNumIscsiNodes=isnsRegEntityInfoNumIscsiNodes, isnsDdIscsiMemberEntry=isnsDdIscsiMemberEntry, isnsServerDiscoveryMethodsEnabled=isnsServerDiscoveryMethodsEnabled, isnsControlNodeIscsiIsRegistered=isnsControlNodeIscsiIsRegistered, IsnsPortalGroupIndexId=IsnsPortalGroupIndexId, isnsRegPortalAddressType=isnsRegPortalAddressType, isnsServerRegIfcpObjGroup=isnsServerRegIfcpObjGroup, isnsRegIscsiNodeType=isnsRegIscsiNodeType, isnsDdsId=isnsDdsId, isnsDdsTable=isnsDdsTable, IsnsIfcpScnType=IsnsIfcpScnType, IsnsNodeIndexId=IsnsNodeIndexId, isnsNumFcPorts=isnsNumFcPorts, isnsRegPortalEsiPort=isnsRegPortalEsiPort, isnsRegIscsiNodeIndex=isnsRegIscsiNodeIndex, isnsRegPgPortalPort=isnsRegPgPortalPort, PYSNMP_MODULE_ID=isnsMIB, isnsRegIscsiNodeWwnToken=isnsRegIscsiNodeWwnToken, isnsServerAttributesGroup=isnsServerAttributesGroup, isnsServerDiscoveryMcGroupAddress=isnsServerDiscoveryMcGroupAddress, isnsTcpPortNotification=isnsTcpPortNotification, isnsRegFcNodeAddress=isnsRegFcNodeAddress, isnsDdPortalMemberIsRegistered=isnsDdPortalMemberIsRegistered, isnsRegPortalSymbolicName=isnsRegPortalSymbolicName, isnsRegFcNodeInfo=isnsRegFcNodeInfo, isnsRegFcNodePortTable=isnsRegFcNodePortTable, isnsDdsMemberSymbolicName=isnsDdsMemberSymbolicName, isnsRegFcPortID=isnsRegFcPortID, isnsNotifications=isnsNotifications, isnsControlNodeFcPortIsRegistered=isnsControlNodeFcPortIsRegistered, isnsRegFcNodeTable=isnsRegFcNodeTable, isnsDdId=isnsDdId, isnsDdFcPortMemberEntry=isnsDdFcPortMemberEntry, isnsRegEntityIndex=isnsRegEntityIndex, isnsDdsEntry=isnsDdsEntry, isnsRegPortalScnPortType=isnsRegPortalScnPortType, isnsRegPgPGT=isnsRegPgPGT, IsnsDdDdsModificationType=IsnsDdDdsModificationType, isnsObjects=isnsObjects, isnsRegPortalAddress=isnsRegPortalAddress, isnsServerIsnsVersion=isnsServerIsnsVersion, isnsRegPortalPort=isnsRegPortalPort, IsnsDdFeatureType=IsnsDdFeatureType, isnsRegPgIndex=isnsRegPgIndex, isnsRegPgPortalPortType=isnsRegPgPortalPortType, isnsRegPgTable=isnsRegPgTable, isnsServerInfo=isnsServerInfo, isnsRegFcPortEntry=isnsRegFcPortEntry, isnsCompliances=isnsCompliances, isnsRegFcPortScnTypes=isnsRegFcPortScnTypes, isnsServerTable=isnsServerTable, isnsNumObjectsTable=isnsNumObjectsTable, isnsRegFcPortHA=isnsRegFcPortHA, IsnsFcPortRoleType=IsnsFcPortRoleType, isnsRegFcNodeIPA=isnsRegFcNodeIPA, isnsRegPgPortalAddressType=isnsRegPgPortalAddressType, isnsDdsMemberTable=isnsDdsMemberTable, isnsRegEntityTimestamp=isnsRegEntityTimestamp, isnsRegPortalPortType=isnsRegPortalPortType, isnsNumObjectsEntry=isnsNumObjectsEntry, IsnsPortalIndexId=IsnsPortalIndexId, IsnsEntityIndexIdOrZero=IsnsEntityIndexIdOrZero, isnsRegFcNodeSymbolicName=isnsRegFcNodeSymbolicName, isnsServerRole=isnsServerRole, IsnsPortalPortTypeId=IsnsPortalPortTypeId, isnsServerEnableControlNodeMgtScn=isnsServerEnableControlNodeMgtScn, isnsServerTcpPort=isnsServerTcpPort, isnsRegEntityInfoNumPortals=isnsRegEntityInfoNumPortals, isnsDdsMemberEntry=isnsDdsMemberEntry, isnsRegEntityEntry=isnsRegEntityEntry, isnsServerIndex=isnsServerIndex, isnsRegEntityInfoNumFcNodes=isnsRegEntityInfoNumFcNodes, isnsRegIscsiNodeAuthMethod=isnsRegIscsiNodeAuthMethod, isnsUdpPortNotification=isnsUdpPortNotification, isnsServerDiscontinuityTime=isnsServerDiscontinuityTime, isnsDdIscsiMemberIsRegistered=isnsDdIscsiMemberIsRegistered, isnsDdTable=isnsDdTable, isnsServerPhysicalIndex=isnsServerPhysicalIndex, isnsIscsiServerCompliance=isnsIscsiServerCompliance, isnsRegPgIscsiName=isnsRegPgIscsiName, isnsRegIscsiNodeName=isnsRegIscsiNodeName, isnsServerVendorInfo=isnsServerVendorInfo, isnsRegFcNodeProxyIscsiName=isnsRegFcNodeProxyIscsiName, isnsRegFcNodePortEntry=isnsRegFcNodePortEntry, isnsDdPortalMemberPortType=isnsDdPortalMemberPortType, isnsControlNodeInfo=isnsControlNodeInfo, isnsGroups=isnsGroups, isnsRegFcPortAddressType=isnsRegFcPortAddressType, isnsDdFcPortMemberTable=isnsDdFcPortMemberTable, isnsServerIfcpPortControlNodeGroup=isnsServerIfcpPortControlNodeGroup, isnsDdsInfo=isnsDdsInfo, isnsControlNodeIscsiTable=isnsControlNodeIscsiTable, isnsServerNotificationGroup=isnsServerNotificationGroup, isnsDdPortalMemberTable=isnsDdPortalMemberTable, isnsMIB=isnsMIB, isnsNumIscsiNodes=isnsNumIscsiNodes, isnsDdSymbolicName=isnsDdSymbolicName, IsnsDdsStatusType=IsnsDdsStatusType, isnsRegEntityNumObjectsEntry=isnsRegEntityNumObjectsEntry, isnsDdPortalMemberAddress=isnsDdPortalMemberAddress, isnsRegPortalEsiPortType=isnsRegPortalEsiPortType, isnsRegIscsiNodeTable=isnsRegIscsiNodeTable, isnsServerDiscoveryMcGroupType=isnsServerDiscoveryMcGroupType, isnsServerShutdown=isnsServerShutdown, isnsServerIscsiDdsDdObjGroup=isnsServerIscsiDdsDdObjGroup, isnsNotificationsObjGroup=isnsNotificationsObjGroup, isnsDdFcPortMemberPortName=isnsDdFcPortMemberPortName, isnsRegFcPortAddress=isnsRegFcPortAddress, isnsControlNodeIscsiRcvMgtSCN=isnsControlNodeIscsiRcvMgtSCN, isnsDdsStatus=isnsDdsStatus, isnsDdFeatures=isnsDdFeatures, isnsRegPortalSecurityInfo=isnsRegPortalSecurityInfo, isnsRegPortalPortalIndex=isnsRegPortalPortalIndex, isnsInstanceInfo=isnsInstanceInfo, isnsServerDefaultDdDdsStatus=isnsServerDefaultDdDdsStatus, isnsNumDds=isnsNumDds, isnsDdFcPortMemberIsRegistered=isnsDdFcPortMemberIsRegistered, isnsServerEntry=isnsServerEntry, isnsRegFcPortTable=isnsRegFcPortTable, isnsReg=isnsReg, isnsRegIscsiNodeEntry=isnsRegIscsiNodeEntry, isnsDdPortalMemberEntry=isnsDdPortalMemberEntry, isnsRegEntityManagementAddressType=isnsRegEntityManagementAddressType, isnsRegFcPortFcNodeWwnn=isnsRegFcPortFcNodeWwnn, isnsRegPortalEntry=isnsRegPortalEntry, isnsDdPortalMemberPort=isnsDdPortalMemberPort, isnsDdPortalMemberIndex=isnsDdPortalMemberIndex, isnsRegIscsiNodeAlias=isnsRegIscsiNodeAlias, isnsRegPortalTable=isnsRegPortalTable, isnsNumPortals=isnsNumPortals)