# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DS0-MIB.py
# Compiled at: 2016-02-13 18:10:48
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, SingleValueConstraint, ConstraintsIntersection, ConstraintsUnion, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'SingleValueConstraint', 'ConstraintsIntersection', 'ConstraintsUnion', 'ValueRangeConstraint')
(InterfaceIndex, ifIndex, InterfaceIndexOrZero) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex', 'ifIndex', 'InterfaceIndexOrZero')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, Unsigned32, Gauge32, ModuleIdentity, transmission, Counter64, iso, IpAddress, NotificationType, Bits, ObjectIdentity, Counter32, TimeTicks) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'Unsigned32', 'Gauge32', 'ModuleIdentity', 'transmission', 'Counter64', 'iso', 'IpAddress', 'NotificationType', 'Bits', 'ObjectIdentity', 'Counter32', 'TimeTicks')
(DisplayString, TextualConvention, TruthValue) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention', 'TruthValue')
ds0 = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 81)).setRevisions(('1998-05-24 20:10', ))
if mibBuilder.loadTexts:
    ds0.setLastUpdated('9807161630Z')
if mibBuilder.loadTexts:
    ds0.setOrganization('IETF Trunk MIB Working Group')
if mibBuilder.loadTexts:
    ds0.setContactInfo('        David Fowler\n\n          Postal: Newbridge Networks Corporation\n                  600 March Road\n                  Kanata, Ontario, Canada K2K 2E6\n\n                  Tel: +1 613 591 3600\n                  Fax: +1 613 599 3619\n\n          E-mail: davef@newbridge.com')
if mibBuilder.loadTexts:
    ds0.setDescription('The MIB module to describe\n             DS0 interfaces objects.')
dsx0ConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 81, 1))
if mibBuilder.loadTexts:
    dsx0ConfigTable.setDescription('The DS0 Configuration table.')
dsx0ConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 81, 1, 1)).setIndexNames((0, 'IF-MIB',
                                                                               'ifIndex'))
if mibBuilder.loadTexts:
    dsx0ConfigEntry.setDescription('An entry in the DS0 Configuration table.  There\n               is an entry in this table for each DS0 interface.')
dsx0Ds0ChannelNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 31))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx0Ds0ChannelNumber.setDescription('This object indicates the channel number of the\n               ds0 on its DS1/E1.')
dsx0RobbedBitSignalling = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 2), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx0RobbedBitSignalling.setDescription('This object indicates if Robbed Bit Signalling is\n               turned on or off for a given ds0.  This only\n               applies to DS0s on a DS1 link.  For E1 links the\n               value is always off (false).')
dsx0CircuitIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx0CircuitIdentifier.setDescription("This object contains the transmission vendor's\n               circuit identifier, for the purpose of\n               facilitating troubleshooting.")
dsx0IdleCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx0IdleCode.setDescription('This object contains the code transmitted in the\n               ABCD bits when the ds0 is not connected and\n               dsx0TransmitCodesEnable is enabled.  The object is\n               a bitmap and the various bit positions are:\n                     1     D bit\n                     2     C bit\n                     4     B bit\n                     8     A bit')
dsx0SeizedCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx0SeizedCode.setDescription('This object contains the code transmitted in the\n               ABCD bits when the ds0 is connected and\n               dsx0TransmitCodesEnable is enabled.  The object is\n               a bitmap and the various bit positions are:\n                     1     D bit\n                     2     C bit\n                     4     B bit\n                     8     A bit')
dsx0ReceivedCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx0ReceivedCode.setDescription('This object contains the code being received in\n               the ABCD bits.  The object is a bitmap and the\n               various bit positions are:\n                     1     D bit\n                     2     C bit\n                     4     B bit\n                     8     A bit')
dsx0TransmitCodesEnable = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 7), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx0TransmitCodesEnable.setDescription('This object determines if the idle and seized\n               codes are transmitted. If the value of this object\n               is true then the codes are transmitted.')
dsx0Ds0BundleMappedIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 1, 1, 8), InterfaceIndexOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx0Ds0BundleMappedIfIndex.setDescription('This object indicates the ifIndex value assigned\n               by the agent for the ds0Bundle(82) ifEntry to\n               which the given ds0(81) ifEntry may belong.\n\n               If the given ds0(81) ifEntry does not belong to\n               any ds0Bundle(82) ifEntry, then this object has a\n               value of zero.\n\n               While this object provides information that can\n               also be found in the ifStackTable, it provides\n               this same information with a single table lookup,\n               rather than by walking the ifStackTable to find\n               the possibly non-existent ds0Bundle(82) ifEntry\n               that may be stacked above the given ds0(81)\n               ifTable entry.')
dsx0ChanMappingTable = MibTable((1, 3, 6, 1, 2, 1, 10, 81, 3))
if mibBuilder.loadTexts:
    dsx0ChanMappingTable.setDescription('The DS0 Channel Mapping table.  This table maps a\n               DS0 channel number on a particular DS1/E1 into an\n               ifIndex.')
dsx0ChanMappingEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 81, 3, 1)).setIndexNames((0,
                                                                                    'IF-MIB',
                                                                                    'ifIndex'), (0,
                                                                                                 'DS0-MIB',
                                                                                                 'dsx0Ds0ChannelNumber'))
if mibBuilder.loadTexts:
    dsx0ChanMappingEntry.setDescription('An entry in the DS0 Channel Mapping table.  There\n               is an entry in this table corresponding to each\n               ds0 ifEntry within any interface that is\n               channelized to the individual ds0 ifEntry level.\n\n               This table is intended to facilitate mapping from\n               channelized interface / channel number to DS0\n               ifEntry.  (e.g. mapping (DS1 ifIndex, DS0 Channel\n               Number) -> ifIndex)\n\n               While this table provides information that can\n               also be found in the ifStackTable and\n               dsx0ConfigTable, it provides this same information\n               with a single table lookup, rather than by walking\n               the ifStackTable to find the various constituent\n               ds0 ifTable entries, and testing various\n               dsx0ConfigTable entries to check for the entry\n               with the applicable DS0 channel number.')
dsx0ChanMappedIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 81, 3, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx0ChanMappedIfIndex.setDescription('This object indicates the ifIndex value assigned\n               by the agent for the individual ds0 ifEntry that\n               corresponds to the given DS0 channel number\n               (specified by the INDEX element\n               dsx0Ds0ChannelNumber) of the given channelized\n               interface (specified by INDEX element ifIndex).')
ds0Conformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 81, 2))
ds0Groups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 81, 2, 1))
ds0Compliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 81, 2, 2))
ds0Compliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 81, 2, 2, 1)).setObjects(*(('DS0-MIB', 'ds0ConfigGroup'), ))
if mibBuilder.loadTexts:
    ds0Compliance.setDescription('The compliance statement for DS0 interfaces.')
ds0ConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 81, 2, 1, 1)).setObjects(*(('DS0-MIB', 'dsx0Ds0ChannelNumber'), ('DS0-MIB', 'dsx0RobbedBitSignalling'), ('DS0-MIB', 'dsx0CircuitIdentifier'), ('DS0-MIB', 'dsx0IdleCode'), ('DS0-MIB', 'dsx0SeizedCode'), ('DS0-MIB', 'dsx0ReceivedCode'), ('DS0-MIB', 'dsx0TransmitCodesEnable'), ('DS0-MIB', 'dsx0Ds0BundleMappedIfIndex'), ('DS0-MIB', 'dsx0ChanMappedIfIndex')))
if mibBuilder.loadTexts:
    ds0ConfigGroup.setDescription('A collection of objects providing configuration\n               information applicable to all DS0 interfaces.')
mibBuilder.exportSymbols('DS0-MIB', dsx0ChanMappingTable=dsx0ChanMappingTable, dsx0ChanMappedIfIndex=dsx0ChanMappedIfIndex, dsx0RobbedBitSignalling=dsx0RobbedBitSignalling, dsx0ChanMappingEntry=dsx0ChanMappingEntry, dsx0ConfigEntry=dsx0ConfigEntry, dsx0Ds0ChannelNumber=dsx0Ds0ChannelNumber, dsx0SeizedCode=dsx0SeizedCode, ds0Compliance=ds0Compliance, ds0Conformance=ds0Conformance, dsx0ConfigTable=dsx0ConfigTable, dsx0CircuitIdentifier=dsx0CircuitIdentifier, dsx0TransmitCodesEnable=dsx0TransmitCodesEnable, dsx0ReceivedCode=dsx0ReceivedCode, ds0Groups=ds0Groups, ds0Compliances=ds0Compliances, ds0=ds0, dsx0IdleCode=dsx0IdleCode, PYSNMP_MODULE_ID=ds0, dsx0Ds0BundleMappedIfIndex=dsx0Ds0BundleMappedIfIndex, ds0ConfigGroup=ds0ConfigGroup)