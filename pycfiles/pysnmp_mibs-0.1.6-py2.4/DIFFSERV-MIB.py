# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DIFFSERV-MIB.py
# Compiled at: 2016-02-13 18:07:36
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, ConstraintsIntersection, ValueRangeConstraint, ConstraintsUnion, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ValueRangeConstraint', 'ConstraintsUnion', 'SingleValueConstraint')
(Dscp, DscpOrAny) = mibBuilder.importSymbols('DIFFSERV-DSCP-TC', 'Dscp', 'DscpOrAny')
(InterfaceIndexOrZero, ifIndex) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndexOrZero', 'ifIndex')
(InetAddressType, InetPortNumber, InetAddressPrefixLength, InetAddress) = mibBuilder.importSymbols('INET-ADDRESS-MIB', 'InetAddressType', 'InetPortNumber', 'InetAddressPrefixLength', 'InetAddress')
(BurstSize,) = mibBuilder.importSymbols('INTEGRATED-SERVICES-MIB', 'BurstSize')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, Bits, ModuleIdentity, mib_2, Counter32, zeroDotZero, ObjectIdentity, IpAddress, Integer32, MibIdentifier, Unsigned32, TimeTicks, Gauge32, NotificationType, iso) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'Bits', 'ModuleIdentity', 'mib-2', 'Counter32', 'zeroDotZero', 'ObjectIdentity', 'IpAddress', 'Integer32', 'MibIdentifier', 'Unsigned32', 'TimeTicks', 'Gauge32', 'NotificationType', 'iso')
(RowStatus, TextualConvention, RowPointer, StorageType, DisplayString, AutonomousType) = mibBuilder.importSymbols('SNMPv2-TC', 'RowStatus', 'TextualConvention', 'RowPointer', 'StorageType', 'DisplayString', 'AutonomousType')
diffServMib = ModuleIdentity((1, 3, 6, 1, 2, 1, 97)).setRevisions(('2002-02-07 00:00', ))
if mibBuilder.loadTexts:
    diffServMib.setLastUpdated('200202070000Z')
if mibBuilder.loadTexts:
    diffServMib.setOrganization('IETF Differentiated Services WG')
if mibBuilder.loadTexts:
    diffServMib.setContactInfo('   Fred Baker\n                Cisco Systems\n                1121 Via Del Rey\n                Santa Barbara, CA 93117, USA\n                E-mail: fred@cisco.com\n                \n                Kwok Ho Chan\n                Nortel Networks\n                600 Technology Park Drive\n                Billerica, MA 01821, USA\n                E-mail: khchan@nortelnetworks.com\n                \n                Andrew Smith\n                Harbour Networks\n                Jiuling Building\n                \n                21 North Xisanhuan Ave.\n                Beijing, 100089, PRC\n                E-mail: ah_smith@acm.org\n                \n                Differentiated Services Working Group:\n                diffserv@ietf.org')
if mibBuilder.loadTexts:
    diffServMib.setDescription('This MIB defines the objects necessary to manage a device that\n            uses the Differentiated Services Architecture described in RFC\n            2475. The Conceptual Model of a Differentiated Services Router\n            provides supporting information on how such a router is modeled.')
diffServMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1))
diffServMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 2))
diffServMIBAdmin = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 3))

class IndexInteger(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(1, 4294967295)


class IndexIntegerNextFree(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(0, 4294967295)


class IfDirection(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('inbound', 1), ('outbound', 2))


diffServDataPath = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 1))
diffServDataPathTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 1, 1))
if mibBuilder.loadTexts:
    diffServDataPathTable.setDescription('The data path table contains RowPointers indicating the start of\n            the functional data path for each interface and traffic direction\n            in this device. These may merge, or be separated into parallel\n            data paths.')
diffServDataPathEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 1, 1, 1)).setIndexNames((0,
                                                                                       'IF-MIB',
                                                                                       'ifIndex'), (0,
                                                                                                    'DIFFSERV-MIB',
                                                                                                    'diffServDataPathIfDirection'))
if mibBuilder.loadTexts:
    diffServDataPathEntry.setDescription('An entry in the data path table indicates the start of a single\n            Differentiated Services Functional Data Path in this device.\n    \n            These are associated with individual interfaces, logical or\n            physical, and therefore are instantiated by ifIndex. Therefore,\n            the interface index must have been assigned, according to the\n            procedures applicable to that, before it can be meaningfully\n            used. Generally, this means that the interface must exist.\n    \n            When diffServDataPathStorage is of type nonVolatile, however,\n            this may reflect the configuration for an interface whose ifIndex\n            has been assigned but for which the supporting implementation is\n            not currently present.')
diffServDataPathIfDirection = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 1, 1, 1, 1), IfDirection())
if mibBuilder.loadTexts:
    diffServDataPathIfDirection.setDescription('IfDirection specifies whether the reception or transmission path\n            for this interface is in view.')
diffServDataPathStart = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 1, 1, 1, 2), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServDataPathStart.setDescription('This selects the first Differentiated Services Functional Data\n            Path Element to handle traffic for this data path. This\n            RowPointer should point to an instance of one of:\n              diffServClfrEntry\n              diffServMeterEntry\n              diffServActionEntry\n              diffServAlgDropEntry\n              diffServQEntry\n    \n            A value of zeroDotZero in this attribute indicates that no\n            Differentiated Services treatment is performed on traffic of this\n            data path. A pointer with the value zeroDotZero normally\n            terminates a functional data path.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServDataPathStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 1, 1, 1, 3), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServDataPathStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServDataPathStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 1, 1, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServDataPathStatus.setDescription('The status of this conceptual row. All writable objects in this\n            row may be modified at any time.')
diffServClassifier = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 2))
diffServClfrNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 2, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServClfrNextFree.setDescription('This object contains an unused value for diffServClfrId, or a\n            zero to indicate that none exist.')
diffServClfrTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 2, 2))
if mibBuilder.loadTexts:
    diffServClfrTable.setDescription('This table enumerates all the diffserv classifier functional\n            data path elements of this device.  The actual classification\n            definitions are defined in diffServClfrElementTable entries\n            belonging to each classifier.\n    \n            An entry in this table, pointed to by a RowPointer specifying an\n            instance of diffServClfrStatus, is frequently used as the name\n            for a set of classifier elements, which all use the index\n            diffServClfrId. Per the semantics of the classifier element\n            table, these entries constitute one or more unordered sets of\n            tests which may be simultaneously applied to a message to\n            classify it.\n    \n            The primary function of this table is to ensure that the value of\n            diffServClfrId is unique before attempting to use it in creating\n            a diffServClfrElementEntry. Therefore, the diffServClfrEntry must\n            be created on the same SET as the diffServClfrElementEntry, or\n            before the diffServClfrElementEntry is created.')
diffServClfrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 2, 2, 1)).setIndexNames((0,
                                                                                   'DIFFSERV-MIB',
                                                                                   'diffServClfrId'))
if mibBuilder.loadTexts:
    diffServClfrEntry.setDescription("An entry in the classifier table describes a single classifier.\n            All classifier elements belonging to the same classifier use the\n            classifier's diffServClfrId as part of their index.")
diffServClfrId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServClfrId.setDescription('An index that enumerates the classifier entries.  Managers\n            should obtain new values for row creation in this table by\n            reading diffServClfrNextFree.')
diffServClfrStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 2, 1, 2), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServClfrStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 2, 1, 3), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServClfrElementNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 2, 3), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServClfrElementNextFree.setDescription('This object contains an unused value for diffServClfrElementId,\n            or a zero to indicate that none exist.')
diffServClfrElementTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 2, 4))
if mibBuilder.loadTexts:
    diffServClfrElementTable.setDescription('The classifier element table enumerates the relationship between\n            classification patterns and subsequent downstream Differentiated\n            Services Functional Data Path elements.\n            diffServClfrElementSpecific points to a filter that specifies the\n            classification parameters. A classifier may use filter tables of\n            different types together.\n    \n            One example of a filter table defined in this MIB is\n            diffServMultiFieldClfrTable, for IP Multi-Field Classifiers\n            (MFCs). Such an entry might identify anything from a single\n            micro-flow (an identifiable sub-session packet stream directed\n            from one sending transport to the receiving transport or\n            transports), or aggregates of those such as the traffic from a\n            host, traffic for an application, or traffic between two hosts\n            using an application and a given DSCP. The standard Behavior\n            Aggregate used in the Differentiated Services Architecture is\n            encoded as a degenerate case of such an aggregate - the traffic\n            using a particular DSCP value.\n    \n            Filter tables for other filter types may be defined elsewhere.')
diffServClfrElementEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1)).setIndexNames((0,
                                                                                          'DIFFSERV-MIB',
                                                                                          'diffServClfrId'), (0,
                                                                                                              'DIFFSERV-MIB',
                                                                                                              'diffServClfrElementId'))
if mibBuilder.loadTexts:
    diffServClfrElementEntry.setDescription('An entry in the classifier element table describes a single\n            element of the classifier.')
diffServClfrElementId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServClfrElementId.setDescription('An index that enumerates the Classifier Element entries.\n            Managers obtain new values for row creation in this table by\n            reading diffServClfrElementNextFree.')
diffServClfrElementPrecedence = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrElementPrecedence.setDescription('The relative order in which classifier elements are applied:\n            higher numbers represent classifier element with higher\n            precedence.  Classifier elements with the same order must be\n            unambiguous i.e. they must define non-overlapping patterns, and\n            are considered to be applied simultaneously to the traffic\n            stream. Classifier elements with different order may overlap in\n            their filters:  the classifier element with the highest order\n            that matches is taken.\n    \n            On a given interface, there must be a complete classifier in\n            place at all times in the ingress direction.  This means one or\n            more filters must match any possible pattern. There is no such\n            requirement in the egress direction.')
diffServClfrElementNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1, 3), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrElementNext.setDescription('This attribute provides one branch of the fan-out functionality\n            of a classifier described in the Informal Differentiated Services\n            Model section 4.1.\n    \n            This selects the next Differentiated Services Functional Data\n            Path Element to handle traffic for this data path. This\n            RowPointer should point to an instance of one of:\n              diffServClfrEntry\n              diffServMeterEntry\n              diffServActionEntry\n              diffServAlgDropEntry\n              diffServQEntry\n    \n            A value of zeroDotZero in this attribute indicates no further\n            Differentiated Services treatment is performed on traffic of this\n            data path. The use of zeroDotZero is the normal usage for the\n            last functional data path element of the current data path.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServClfrElementSpecific = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1, 4), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrElementSpecific.setDescription('A pointer to a valid entry in another table, filter table, that\n            describes the applicable classification parameters, e.g. an entry\n            in diffServMultiFieldClfrTable.\n    \n            The value zeroDotZero is interpreted to match anything not\n            matched by another classifier element - only one such entry may\n            exist for each classifier.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the element is ignored.')
diffServClfrElementStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrElementStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServClfrElementStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 4, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServClfrElementStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServMultiFieldClfrNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 2, 5), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrNextFree.setDescription('This object contains an unused value for\n            diffServMultiFieldClfrId, or a zero to indicate that none exist.')
diffServMultiFieldClfrTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 2, 6))
if mibBuilder.loadTexts:
    diffServMultiFieldClfrTable.setDescription('A table of IP Multi-field Classifier filter entries that a\n            system may use to identify IP traffic.')
diffServMultiFieldClfrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1)).setIndexNames((0,
                                                                                             'DIFFSERV-MIB',
                                                                                             'diffServMultiFieldClfrId'))
if mibBuilder.loadTexts:
    diffServMultiFieldClfrEntry.setDescription('An IP Multi-field Classifier entry describes a single filter.')
diffServMultiFieldClfrId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServMultiFieldClfrId.setDescription('An index that enumerates the MultiField Classifier filter\n            entries.  Managers obtain new values for row creation in this\n            table by reading diffServMultiFieldClfrNextFree.')
diffServMultiFieldClfrAddrType = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1,
                                                 2), InetAddressType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrAddrType.setDescription('The type of IP address used by this classifier entry.  While\n            other types of addresses are defined in the InetAddressType\n            textual convention, and DNS names, a classifier can only look at\n            packets on the wire. Therefore, this object is limited to IPv4\n            and IPv6 addresses.')
diffServMultiFieldClfrDstAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 3), InetAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrDstAddr.setDescription("The IP address to match against the packet's destination IP\n            address. This may not be a DNS name, but may be an IPv4 or IPv6\n            prefix.  diffServMultiFieldClfrDstPrefixLength indicates the\n            number of bits that are relevant.")
diffServMultiFieldClfrDstPrefixLength = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2,
                                                        6, 1, 4), InetAddressPrefixLength()).setUnits('bits').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrDstPrefixLength.setDescription('The length of the CIDR Prefix carried in\n            diffServMultiFieldClfrDstAddr. In IPv4 addresses, a length of 0\n            indicates a match of any address; a length of 32 indicates a\n            match of a single host address, and a length between 0 and 32\n            indicates the use of a CIDR Prefix. IPv6 is similar, except that\n            prefix lengths range from 0..128.')
diffServMultiFieldClfrSrcAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 5), InetAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrSrcAddr.setDescription("The IP address to match against the packet's source IP address.\n            This may not be a DNS name, but may be an IPv4 or IPv6 prefix.\n            diffServMultiFieldClfrSrcPrefixLength indicates the number of\n            bits that are relevant.")
diffServMultiFieldClfrSrcPrefixLength = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2,
                                                        6, 1, 6), InetAddressPrefixLength()).setUnits('bits').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrSrcPrefixLength.setDescription('The length of the CIDR Prefix carried in\n            diffServMultiFieldClfrSrcAddr. In IPv4 addresses, a length of 0\n            indicates a match of any address; a length of 32 indicates a\n            match of a single host address, and a length between 0 and 32\n            indicates the use of a CIDR Prefix. IPv6 is similar, except that\n            prefix lengths range from 0..128.')
diffServMultiFieldClfrDscp = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 7), DscpOrAny().clone(-1)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrDscp.setDescription('The value that the DSCP in the packet must have to match this\n            entry. A value of -1 indicates that a specific DSCP value has not\n            been defined and thus all DSCP values are considered a match.')
diffServMultiFieldClfrFlowId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 8), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 1048575))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrFlowId.setDescription('The flow identifier in an IPv6 header.')
diffServMultiFieldClfrProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1,
                                                 9), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)).clone(255)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrProtocol.setDescription('The IP protocol to match against the IPv4 protocol number or the\n            IPv6 Next- Header number in the packet. A value of 255 means\n            match all.  Note the protocol number of 255 is reserved by IANA,\n            and Next-Header number of 0 is used in IPv6.')
diffServMultiFieldClfrDstL4PortMin = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6,
                                                     1, 10), InetPortNumber()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrDstL4PortMin.setDescription('The minimum value that the layer-4 destination port number in\n            the packet must have in order to match this classifier entry.')
diffServMultiFieldClfrDstL4PortMax = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6,
                                                     1, 11), InetPortNumber().clone(65535)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrDstL4PortMax.setDescription('The maximum value that the layer-4 destination port number in\n            the packet must have in order to match this classifier entry.\n            This value must be equal to or greater than the value specified\n            for this entry in diffServMultiFieldClfrDstL4PortMin.')
diffServMultiFieldClfrSrcL4PortMin = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6,
                                                     1, 12), InetPortNumber()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrSrcL4PortMin.setDescription('The minimum value that the layer-4 source port number in the\n            packet must have in order to match this classifier entry.')
diffServMultiFieldClfrSrcL4PortMax = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6,
                                                     1, 13), InetPortNumber().clone(65535)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrSrcL4PortMax.setDescription('The maximum value that the layer-4 source port number in the\n            packet must have in order to match this classifier entry. This\n            value must be equal to or greater than the value specified for\n            this entry in diffServMultiFieldClfrSrcL4PortMin.')
diffServMultiFieldClfrStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 14), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServMultiFieldClfrStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 2, 6, 1, 15), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMultiFieldClfrStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServMeter = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 3))
diffServMeterNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 3, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServMeterNextFree.setDescription('This object contains an unused value for diffServMeterId, or a\n            zero to indicate that none exist.')
diffServMeterTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 3, 2))
if mibBuilder.loadTexts:
    diffServMeterTable.setDescription('This table enumerates specific meters that a system may use to\n            police a stream of traffic. The traffic stream to be metered is\n            determined by the Differentiated Services Functional Data Path\n            Element(s) upstream of the meter i.e. by the object(s) that point\n            to each entry in this table.  This may include all traffic on an\n            interface.\n    \n            Specific meter details are to be found in table entry referenced\n            by diffServMeterSpecific.')
diffServMeterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1)).setIndexNames((0,
                                                                                    'DIFFSERV-MIB',
                                                                                    'diffServMeterId'))
if mibBuilder.loadTexts:
    diffServMeterEntry.setDescription('An entry in the meter table describes a single conformance level\n            of a meter.')
diffServMeterId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServMeterId.setDescription('An index that enumerates the Meter entries.  Managers obtain new\n            values for row creation in this table by reading\n            diffServMeterNextFree.')
diffServMeterSucceedNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1, 2), RowPointer().clone((0,
                                                                                                     0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMeterSucceedNext.setDescription('If the traffic does conform, this selects the next\n            Differentiated Services Functional Data Path element to handle\n            traffic for this data path. This RowPointer should point to an\n            instance of one of:\n              diffServClfrEntry\n              diffServMeterEntry\n              diffServActionEntry\n              diffServAlgDropEntry\n              diffServQEntry\n    \n            A value of zeroDotZero in this attribute indicates that no\n            further Differentiated Services treatment is performed on traffic\n            of this data path. The use of zeroDotZero is the normal usage for\n            the last functional data path element of the current data path.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServMeterFailNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1, 3), RowPointer().clone((0,
                                                                                                  0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMeterFailNext.setDescription('If the traffic does not conform, this selects the next\n            Differentiated Services Functional Data Path element to handle\n            traffic for this data path. This RowPointer should point to an\n            instance of one of:\n              diffServClfrEntry\n              diffServMeterEntry\n              diffServActionEntry\n              diffServAlgDropEntry\n              diffServQEntry\n    \n            A value of zeroDotZero in this attribute indicates no further\n            Differentiated Services treatment is performed on traffic of this\n            data path. The use of zeroDotZero is the normal usage for the\n            last functional data path element of the current data path.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServMeterSpecific = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1, 4), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMeterSpecific.setDescription('This indicates the behavior of the meter by pointing to an entry\n            containing detailed parameters. Note that entries in that\n            specific table must be managed explicitly.\n    \n            For example, diffServMeterSpecific may point to an entry in\n            diffServTBParamTable, which contains an instance of a single set\n            of Token Bucket parameters.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the meter always succeeds.')
diffServMeterStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMeterStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServMeterStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 3, 2, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMeterStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServTBParam = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 4))
diffServTBParamNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 4, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServTBParamNextFree.setDescription('This object contains an unused value for diffServTBParamId, or a\n            zero to indicate that none exist.')
diffServTBParamTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 4, 2))
if mibBuilder.loadTexts:
    diffServTBParamTable.setDescription('This table enumerates a single set of token bucket meter\n            parameters that a system may use to police a stream of traffic.\n            Such meters are modeled here as having a single rate and a single\n            burst size. Multiple entries are used when multiple rates/burst\n            sizes are needed.')
diffServTBParamEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1)).setIndexNames((0,
                                                                                      'DIFFSERV-MIB',
                                                                                      'diffServTBParamId'))
if mibBuilder.loadTexts:
    diffServTBParamEntry.setDescription('An entry that describes a single set of token bucket\n            parameters.')
diffServTBParamId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServTBParamId.setDescription('An index that enumerates the Token Bucket Parameter entries.\n            Managers obtain new values for row creation in this table by\n            reading diffServTBParamNextFree.')
diffServTBParamType = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 2), AutonomousType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServTBParamType.setDescription('The Metering algorithm associated with the Token Bucket\n            parameters.  zeroDotZero indicates this is unknown.\n    \n            Standard values for generic algorithms:\n            diffServTBParamSimpleTokenBucket, diffServTBParamAvgRate,\n            diffServTBParamSrTCMBlind, diffServTBParamSrTCMAware,\n            diffServTBParamTrTCMBlind, diffServTBParamTrTCMAware, and\n            diffServTBParamTswTCM are specified in this MIB as OBJECT-\n            IDENTITYs; additional values may be further specified in other\n            MIBs.')
diffServTBParamRate = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('kilobits per second').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServTBParamRate.setDescription('The token-bucket rate, in kilobits per second (kbps). This\n            attribute is used for:\n            1. CIR in RFC 2697 for srTCM\n            2. CIR and PIR in RFC 2698 for trTCM\n            3. CTR and PTR in RFC 2859 for TSWTCM\n            4. AverageRate in RFC 3290.')
diffServTBParamBurstSize = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 4), BurstSize()).setUnits('Bytes').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServTBParamBurstSize.setDescription('The maximum number of bytes in a single transmission burst. This\n            attribute is used for:\n            1. CBS and EBS in RFC 2697 for srTCM\n            2. CBS and PBS in RFC 2698 for trTCM\n            3. Burst Size in RFC 3290.')
diffServTBParamInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 5), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('microseconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServTBParamInterval.setDescription('The time interval used with the token bucket.  For:\n            1. Average Rate Meter, the Informal Differentiated Services Model\n               section 5.2.1, - Delta.\n            2. Simple Token Bucket Meter, the Informal Differentiated\n               Services Model section 5.1, - time interval t.\n            3. RFC 2859 TSWTCM, - AVG_INTERVAL.\n            4. RFC 2697 srTCM, RFC 2698 trTCM, - token bucket update time\n               interval.')
diffServTBParamStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServTBParamStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServTBParamStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 4, 2, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServTBParamStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServTBMeters = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 3, 1))
diffServTBParamSimpleTokenBucket = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 1))
if mibBuilder.loadTexts:
    diffServTBParamSimpleTokenBucket.setDescription('Two Parameter Token Bucket Meter as described in the Informal\n            Differentiated Services Model section 5.2.3.')
diffServTBParamAvgRate = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 2))
if mibBuilder.loadTexts:
    diffServTBParamAvgRate.setDescription('Average Rate Meter as described in the Informal Differentiated\n            Services Model section 5.2.1.')
diffServTBParamSrTCMBlind = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 3))
if mibBuilder.loadTexts:
    diffServTBParamSrTCMBlind.setDescription("Single Rate Three Color Marker Metering as defined by RFC 2697,\n            in the `Color Blind' mode as described by the RFC.")
diffServTBParamSrTCMAware = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 4))
if mibBuilder.loadTexts:
    diffServTBParamSrTCMAware.setDescription("Single Rate Three Color Marker Metering as defined by RFC 2697,\n            in the `Color Aware' mode as described by the RFC.")
diffServTBParamTrTCMBlind = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 5))
if mibBuilder.loadTexts:
    diffServTBParamTrTCMBlind.setDescription("Two Rate Three Color Marker Metering as defined by RFC 2698, in\n            the `Color Blind' mode as described by the RFC.")
diffServTBParamTrTCMAware = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 6))
if mibBuilder.loadTexts:
    diffServTBParamTrTCMAware.setDescription("Two Rate Three Color Marker Metering as defined by RFC 2698, in\n            the `Color Aware' mode as described by the RFC.")
diffServTBParamTswTCM = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 1, 7))
if mibBuilder.loadTexts:
    diffServTBParamTswTCM.setDescription('Time Sliding Window Three Color Marker Metering as defined by\n            RFC 2859.')
diffServAction = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 5))
diffServActionNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 5, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServActionNextFree.setDescription('This object contains an unused value for diffServActionId, or a\n            zero to indicate that none exist.')
diffServActionTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 5, 2))
if mibBuilder.loadTexts:
    diffServActionTable.setDescription('The Action Table enumerates actions that can be performed to a\n            stream of traffic. Multiple actions can be concatenated. For\n            example, traffic exiting from a meter may be counted, marked, and\n            potentially dropped before entering a queue.\n    \n            Specific actions are indicated by diffServActionSpecific which\n            points to an entry of a specific action type parameterizing the\n            action in detail.')
diffServActionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1)).setIndexNames((0,
                                                                                     'DIFFSERV-MIB',
                                                                                     'diffServActionId'))
if mibBuilder.loadTexts:
    diffServActionEntry.setDescription('Each entry in the action table allows description of one\n            specific action to be applied to traffic.')
diffServActionId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServActionId.setDescription('An index that enumerates the Action entries.  Managers obtain\n            new values for row creation in this table by reading\n            diffServActionNextFree.')
diffServActionInterface = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1, 2), InterfaceIndexOrZero()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServActionInterface.setDescription("The interface index (value of ifIndex) that this action occurs\n            on. This may be derived from the diffServDataPathStartEntry's\n            index by extension through the various RowPointers. However, as\n            this may be difficult for a network management station, it is\n            placed here as well.  If this is indeterminate, the value is\n            zero.\n    \n            This is of especial relevance when reporting the counters which\n            may apply to traffic crossing an interface:\n               diffServCountActOctets,\n               diffServCountActPkts,\n               diffServAlgDropOctets,\n               diffServAlgDropPkts,\n               diffServAlgRandomDropOctets, and\n               diffServAlgRandomDropPkts.\n    \n            It is also especially relevant to the queue and scheduler which\n            may be subsequently applied.")
diffServActionNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1, 3), RowPointer().clone((0,
                                                                                               0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServActionNext.setDescription('This selects the next Differentiated Services Functional Data\n            Path Element to handle traffic for this data path. This\n            RowPointer should point to an instance of one of:\n              diffServClfrEntry\n              diffServMeterEntry\n              diffServActionEntry\n              diffServAlgDropEntry\n              diffServQEntry\n    \n            A value of zeroDotZero in this attribute indicates no further\n            Differentiated Services treatment is performed on traffic of this\n            data path. The use of zeroDotZero is the normal usage for the\n            last functional data path element of the current data path.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServActionSpecific = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1, 4), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServActionSpecific.setDescription('A pointer to an object instance providing additional information\n            for the type of action indicated by this action table entry.\n    \n            For the standard actions defined by this MIB module, this should\n            point to either a diffServDscpMarkActEntry or a\n            diffServCountActEntry. For other actions, it may point to an\n            object instance defined in some other MIB.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the Meter should be treated as\n            if it were not present.  This may lead to incorrect policy\n            behavior.')
diffServActionStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServActionStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServActionStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 2, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServActionStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServDscpMarkActTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 5, 3))
if mibBuilder.loadTexts:
    diffServDscpMarkActTable.setDescription('This table enumerates specific DSCPs used for marking or\n            remarking the DSCP field of IP packets. The entries of this table\n            may be referenced by a diffServActionSpecific attribute.')
diffServDscpMarkActEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 5, 3, 1)).setIndexNames((0,
                                                                                          'DIFFSERV-MIB',
                                                                                          'diffServDscpMarkActDscp'))
if mibBuilder.loadTexts:
    diffServDscpMarkActEntry.setDescription('An entry in the DSCP mark action table that describes a single\n            DSCP used for marking.')
diffServDscpMarkActDscp = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 3, 1, 1), Dscp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServDscpMarkActDscp.setDescription('The DSCP that this Action will store into the DSCP field of the\n            subject. It is quite possible that the only packets subject to\n            this Action are already marked with this DSCP. Note also that\n            Differentiated Services processing may result in packet being\n            marked on both ingress to a network and on egress from it, and\n            that ingress and egress can occur in the same router.')
diffServCountActNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 5, 4), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServCountActNextFree.setDescription('This object contains an unused value for\n            diffServCountActId, or a zero to indicate that none exist.')
diffServCountActTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 5, 5))
if mibBuilder.loadTexts:
    diffServCountActTable.setDescription('This table contains counters for all the traffic passing through\n            an action element.')
diffServCountActEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 5, 5, 1)).setIndexNames((0,
                                                                                       'DIFFSERV-MIB',
                                                                                       'diffServCountActId'))
if mibBuilder.loadTexts:
    diffServCountActEntry.setDescription('An entry in the count action table describes a single set of\n            traffic counters.')
diffServCountActId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 5, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServCountActId.setDescription('An index that enumerates the Count Action entries.  Managers\n            obtain new values for row creation in this table by reading\n            diffServCountActNextFree.')
diffServCountActOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 5, 1, 2), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServCountActOctets.setDescription('The number of octets at the Action data path element.\n    \n            Discontinuities in the value of this counter can occur at re-\n            initialization of the management system and at other times as\n            indicated by the value of ifCounterDiscontinuityTime on the\n            relevant interface.')
diffServCountActPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 5, 1, 3), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServCountActPkts.setDescription('The number of packets at the Action data path element.\n    \n            Discontinuities in the value of this counter can occur at re-\n            initialization of the management system and at other times as\n            indicated by the value of ifCounterDiscontinuityTime on the\n            relevant interface.')
diffServCountActStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 5, 1, 4), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServCountActStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServCountActStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 5, 5, 1, 5), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServCountActStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServAlgDrop = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 6))
diffServAlgDropNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 6, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServAlgDropNextFree.setDescription('This object contains an unused value for diffServAlgDropId, or a\n            zero to indicate that none exist.')
diffServAlgDropTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 6, 2))
if mibBuilder.loadTexts:
    diffServAlgDropTable.setDescription('The algorithmic drop table contains entries describing an\n            element that drops packets according to some algorithm.')
diffServAlgDropEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1)).setIndexNames((0,
                                                                                      'DIFFSERV-MIB',
                                                                                      'diffServAlgDropId'))
if mibBuilder.loadTexts:
    diffServAlgDropEntry.setDescription('An entry describes a process that drops packets according to\n            some algorithm. Further details of the algorithm type are to be\n            found in diffServAlgDropType and with more detail parameter entry\n            pointed to by diffServAlgDropSpecific when necessary.')
diffServAlgDropId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServAlgDropId.setDescription('An index that enumerates the Algorithmic Dropper entries.\n            Managers obtain new values for row creation in this table by\n            reading diffServAlgDropNextFree.')
diffServAlgDropType = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                                   1), ('tailDrop',
                                                                                                                                                                                                        2), ('headDrop',
                                                                                                                                                                                                             3), ('randomDrop',
                                                                                                                                                                                                                  4), ('alwaysDrop',
                                                                                                                                                                                                                       5)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropType.setDescription("The type of algorithm used by this dropper. The value other(1)\n            requires further specification in some other MIB module.\n    \n            In the tailDrop(2) algorithm, diffServAlgDropQThreshold\n            represents the maximum depth of the queue, pointed to by\n            diffServAlgDropQMeasure, beyond which all newly arriving packets\n            will be dropped.\n    \n            In the headDrop(3) algorithm, if a packet arrives when the\n            current depth of the queue, pointed to by\n            diffServAlgDropQMeasure, is at diffServAlgDropQThreshold, packets\n            currently at the head of the queue are dropped to make room for\n            the new packet to be enqueued at the tail of the queue.\n    \n            In the randomDrop(4) algorithm, on packet arrival, an Active\n            Queue Management algorithm is executed which may randomly drop a\n            packet. This algorithm may be proprietary, and it may drop either\n            the arriving packet or another packet in the queue.\n            diffServAlgDropSpecific points to a diffServRandomDropEntry that\n            describes the algorithm. For this algorithm,\n            diffServAlgDropQThreshold is understood to be the absolute\n            maximum size of the queue and additional parameters are described\n            in diffServRandomDropTable.\n    \n            The alwaysDrop(5) algorithm is as its name specifies; always\n            drop. In this case, the other configuration values in this Entry\n            are not meaningful; There is no useful 'next' processing step,\n            there is no queue, and parameters describing the queue are not\n            useful. Therefore, diffServAlgDropNext, diffServAlgDropMeasure,\n            and diffServAlgDropSpecific are all zeroDotZero.")
diffServAlgDropNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 3), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropNext.setDescription('This selects the next Differentiated Services Functional Data\n            Path Element to handle traffic for this data path. This\n            RowPointer should point to an instance of one of:\n              diffServClfrEntry\n              diffServMeterEntry\n              diffServActionEntry\n              diffServQEntry\n    \n            A value of zeroDotZero in this attribute indicates no further\n            Differentiated Services treatment is performed on traffic of this\n            data path. The use of zeroDotZero is the normal usage for the\n            last functional data path element of the current data path.\n    \n            When diffServAlgDropType is alwaysDrop(5), this object is\n            ignored.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServAlgDropQMeasure = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 4), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropQMeasure.setDescription('Points to an entry in the diffServQTable to indicate the queue\n            that a drop algorithm is to monitor when deciding whether to drop\n            a packet. If the row pointed to does not exist, the algorithmic\n            dropper element is considered inactive.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServAlgDropQThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 5), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('Bytes').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropQThreshold.setDescription('A threshold on the depth in bytes of the queue being measured at\n            which a trigger is generated to the dropping algorithm, unless\n            diffServAlgDropType is alwaysDrop(5) where this object is\n            ignored.\n    \n            For the tailDrop(2) or headDrop(3) algorithms, this represents\n            the depth of the queue, pointed to by diffServAlgDropQMeasure, at\n            which the drop action will take place. Other algorithms will need\n            to define their own semantics for this threshold.')
diffServAlgDropSpecific = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 6), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropSpecific.setDescription('Points to a table entry that provides further detail regarding a\n            drop algorithm.\n    \n            Entries with diffServAlgDropType equal to other(1) may have this\n            point to a table defined in another MIB module.\n    \n            Entries with diffServAlgDropType equal to randomDrop(4) must have\n            this point to an entry in diffServRandomDropTable.\n    \n            For all other algorithms specified in this MIB, this should take\n            the value zeroDotZero.\n    \n            The diffServAlgDropType is authoritative for the type of the drop\n            algorithm and the specific parameters for the drop algorithm\n            needs to be evaluated based on the diffServAlgDropType.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServAlgDropOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 7), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServAlgDropOctets.setDescription('The number of octets that have been deterministically dropped by\n            this drop process.\n    \n            Discontinuities in the value of this counter can occur at re-\n            initialization of the management system and at other times as\n            indicated by the value of ifCounterDiscontinuityTime on the\n            relevant interface.')
diffServAlgDropPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 8), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServAlgDropPkts.setDescription('The number of packets that have been deterministically dropped\n            by this drop process.\n    \n            Discontinuities in the value of this counter can occur at re-\n            initialization of the management system and at other times as\n            indicated by the value of ifCounterDiscontinuityTime on the\n            relevant interface.')
diffServAlgRandomDropOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 9), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServAlgRandomDropOctets.setDescription('The number of octets that have been randomly dropped by this\n            drop process.  This counter applies, therefore, only to random\n            droppers.\n    \n            Discontinuities in the value of this counter can occur at re-\n            initialization of the management system and at other times as\n            indicated by the value of ifCounterDiscontinuityTime on the\n            relevant interface.')
diffServAlgRandomDropPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 10), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServAlgRandomDropPkts.setDescription('The number of packets that have been randomly dropped by this\n            drop process. This counter applies, therefore, only to random\n            droppers.\n    \n            Discontinuities in the value of this counter can occur at re-\n            initialization of the management system and at other times as\n            indicated by the value of ifCounterDiscontinuityTime on the\n            relevant interface.')
diffServAlgDropStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 11), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServAlgDropStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 2, 1, 12), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServAlgDropStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServRandomDropNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 6, 3), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServRandomDropNextFree.setDescription('This object contains an unused value for diffServRandomDropId,\n            or a zero to indicate that none exist.')
diffServRandomDropTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 6, 4))
if mibBuilder.loadTexts:
    diffServRandomDropTable.setDescription('The random drop table contains entries describing a process that\n            drops packets randomly. Entries in this table are pointed to by\n            diffServAlgDropSpecific.')
diffServRandomDropEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1)).setIndexNames((0,
                                                                                         'DIFFSERV-MIB',
                                                                                         'diffServRandomDropId'))
if mibBuilder.loadTexts:
    diffServRandomDropEntry.setDescription('An entry describes a process that drops packets according to a\n            random algorithm.')
diffServRandomDropId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServRandomDropId.setDescription('An index that enumerates the Random Drop entries.  Managers\n            obtain new values for row creation in this table by reading\n            diffServRandomDropNextFree.')
diffServRandomDropMinThreshBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1,
                                                   2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('bytes').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropMinThreshBytes.setDescription('The average queue depth in bytes, beyond which traffic has a\n            non-zero probability of being dropped. Changes in this variable\n            may or may not be reflected in the reported value of\n            diffServRandomDropMinThreshPkts.')
diffServRandomDropMinThreshPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1,
                                                  3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('packets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropMinThreshPkts.setDescription('The average queue depth in packets, beyond which traffic has a\n            non-zero probability of being dropped. Changes in this variable\n            may or may not be reflected in the reported value of\n            diffServRandomDropMinThreshBytes.')
diffServRandomDropMaxThreshBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1,
                                                   4), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('bytes').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropMaxThreshBytes.setDescription('The average queue depth beyond which traffic has a probability\n            indicated by diffServRandomDropProbMax of being dropped or\n            marked. Note that this differs from the physical queue limit,\n            which is stored in diffServAlgDropQThreshold. Changes in this\n            variable may or may not be reflected in the reported value of\n            diffServRandomDropMaxThreshPkts.')
diffServRandomDropMaxThreshPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1,
                                                  5), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('packets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropMaxThreshPkts.setDescription('The average queue depth beyond which traffic has a probability\n            indicated by diffServRandomDropProbMax of being dropped or\n            marked. Note that this differs from the physical queue limit,\n            which is stored in diffServAlgDropQThreshold. Changes in this\n            variable may or may not be reflected in the reported value of\n            diffServRandomDropMaxThreshBytes.')
diffServRandomDropProbMax = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1, 6), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 1000))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropProbMax.setDescription('The worst case random drop probability, expressed in drops per\n            thousand packets.\n    \n            For example, if in the worst case every arriving packet may be\n            dropped (100%) for a period, this has the value 1000.\n            Alternatively, if in the worst case only one percent (1%) of\n            traffic may be dropped, it has the value 10.')
diffServRandomDropWeight = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1, 7), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65536))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropWeight.setDescription('The weighting of past history in affecting the Exponentially\n            Weighted Moving Average function that calculates the current\n            average queue depth.  The equation uses\n            diffServRandomDropWeight/65536 as the coefficient for the new\n            sample in the equation, and (65536 -\n            diffServRandomDropWeight)/65536 as the coefficient of the old\n            value.\n    \n            Implementations may limit the values of diffServRandomDropWeight\n            to a subset of the possible range of values, such as powers of\n            two. Doing this would facilitate implementation of the\n            Exponentially Weighted Moving Average using shift instructions or\n            registers.')
diffServRandomDropSamplingRate = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1,
                                                 8), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 1000000))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropSamplingRate.setDescription('The number of times per second the queue is sampled for queue\n            average calculation.  A value of zero is used to mean that the\n            queue is sampled approximately each time a packet is enqueued (or\n            dequeued).')
diffServRandomDropStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1, 9), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServRandomDropStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 6, 4, 1, 10), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServRandomDropStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServQueue = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 7))
diffServQNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 7, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServQNextFree.setDescription('This object contains an unused value for diffServQId, or a zero\n            to indicate that none exist.')
diffServQTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 7, 2))
if mibBuilder.loadTexts:
    diffServQTable.setDescription('The Queue Table enumerates the individual queues.  Note that the\n            MIB models queuing systems as composed of individual queues, one\n            per class of traffic, even though they may in fact be structured\n            as classes of traffic scheduled using a common calendar queue, or\n            in other ways.')
diffServQEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1)).setIndexNames((0,
                                                                                'DIFFSERV-MIB',
                                                                                'diffServQId'))
if mibBuilder.loadTexts:
    diffServQEntry.setDescription('An entry in the Queue Table describes a single queue or class of\n            traffic.')
diffServQId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServQId.setDescription('An index that enumerates the Queue entries.  Managers obtain new\n            values for row creation in this table by reading\n            diffServQNextFree.')
diffServQNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1, 2), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServQNext.setDescription('This selects the next Differentiated Services Scheduler.  The\n            RowPointer must point to a diffServSchedulerEntry.\n    \n            A value of zeroDotZero in this attribute indicates an incomplete\n            diffServQEntry instance. In such a case, the entry has no\n            operational effect, since it has no parameters to give it\n            meaning.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServQMinRate = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1, 3), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServQMinRate.setDescription('This RowPointer indicates the diffServMinRateEntry that the\n            scheduler, pointed to by diffServQNext, should use to service\n            this queue.\n    \n            If the row pointed to is zeroDotZero, the minimum rate and\n            priority is unspecified.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServQMaxRate = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1, 4), RowPointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServQMaxRate.setDescription('This RowPointer indicates the diffServMaxRateEntry that the\n            scheduler, pointed to by diffServQNext, should use to service\n            this queue.\n    \n            If the row pointed to is zeroDotZero, the maximum rate is the\n            line speed of the interface.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServQStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServQStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServQStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 7, 2, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServQStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServScheduler = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 1, 8))
diffServSchedulerNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 8, 1), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServSchedulerNextFree.setDescription('This object contains an unused value for diffServSchedulerId, or\n            a zero to indicate that none exist.')
diffServSchedulerTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 8, 2))
if mibBuilder.loadTexts:
    diffServSchedulerTable.setDescription('The Scheduler Table enumerates packet schedulers. Multiple\n            scheduling algorithms can be used on a given data path, with each\n            algorithm described by one diffServSchedulerEntry.')
diffServSchedulerEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1)).setIndexNames((0,
                                                                                        'DIFFSERV-MIB',
                                                                                        'diffServSchedulerId'))
if mibBuilder.loadTexts:
    diffServSchedulerEntry.setDescription('An entry in the Scheduler Table describing a single instance of\n            a scheduling algorithm.')
diffServSchedulerId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServSchedulerId.setDescription('An index that enumerates the Scheduler entries.  Managers obtain\n            new values for row creation in this table by reading\n            diffServSchedulerNextFree.')
diffServSchedulerNext = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 2), RowPointer().clone((0,
                                                                                                  0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServSchedulerNext.setDescription('This selects the next Differentiated Services Functional Data\n            Path Element to handle traffic for this data path. This normally\n            is null (zeroDotZero), or points to a diffServSchedulerEntry or a\n            diffServQEntry.\n    \n            However, this RowPointer may also point to an instance of:\n              diffServClfrEntry,\n              diffServMeterEntry,\n              diffServActionEntry,\n              diffServAlgDropEntry.\n    \n            It would point another diffServSchedulerEntry when implementing\n            multiple scheduler methods for the same data path, such as having\n            one set of queues scheduled by WRR and that group participating\n            in a priority scheduling system in which other queues compete\n            with it in that way.  It might also point to a second scheduler\n            in a hierarchical scheduling system.\n    \n            If the row pointed to is zeroDotZero, no further Differentiated\n            Services treatment is performed on traffic of this data path.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServSchedulerMethod = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 3), AutonomousType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServSchedulerMethod.setDescription('The scheduling algorithm used by this Scheduler. zeroDotZero\n            indicates that this is unknown.  Standard values for generic\n            algorithms: diffServSchedulerPriority, diffServSchedulerWRR, and\n            diffServSchedulerWFQ are specified in this MIB; additional values\n            may be further specified in other MIBs.')
diffServSchedulerMinRate = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 4), RowPointer().clone((0,
                                                                                                     0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServSchedulerMinRate.setDescription('This RowPointer indicates the entry in diffServMinRateTable\n            which indicates the priority or minimum output rate from this\n            scheduler. This attribute is used only when there is more than\n            one level of scheduler.\n    \n            When it has the value zeroDotZero, it indicates that no minimum\n            rate or priority is imposed.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServSchedulerMaxRate = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 5), RowPointer().clone((0,
                                                                                                     0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServSchedulerMaxRate.setDescription('This RowPointer indicates the entry in diffServMaxRateTable\n            which indicates the maximum output rate from this scheduler.\n            When more than one maximum rate applies (eg, when a multi-rate\n            shaper is in view), it points to the first of those rate entries.\n            This attribute is used only when there is more than one level of\n            scheduler.\n    \n            When it has the value zeroDotZero, it indicates that no maximum\n            rate is imposed.\n    \n            Setting this to point to a target that does not exist results in\n            an inconsistentValue error.  If the row pointed to is removed or\n            becomes inactive by other means, the treatment is as if this\n            attribute contains a value of zeroDotZero.')
diffServSchedulerStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServSchedulerStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServSchedulerStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 2, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServSchedulerStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServSchedulers = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 3, 2))
diffServSchedulerPriority = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 2, 1))
if mibBuilder.loadTexts:
    diffServSchedulerPriority.setDescription('For use with diffServSchedulerMethod to indicate the Priority\n            scheduling method.  This is defined as an algorithm in which the\n            presence of data in a queue or set of queues absolutely precludes\n            dequeue from another queue or set of queues of lower priority.\n            Note that attributes from diffServMinRateEntry of the\n            queues/schedulers feeding this scheduler are used when\n            determining the next packet to schedule.')
diffServSchedulerWRR = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 2, 2))
if mibBuilder.loadTexts:
    diffServSchedulerWRR.setDescription('For use with diffServSchedulerMethod to indicate the Weighted\n            Round Robin scheduling method, defined as any algorithm in which\n            a set of queues are visited in a fixed order, and varying amounts\n            of traffic are removed from each queue in turn to implement an\n            average output rate by class. Notice attributes from\n            diffServMinRateEntry of the queues/schedulers feeding this\n            scheduler are used when determining the next packet to schedule.')
diffServSchedulerWFQ = ObjectIdentity((1, 3, 6, 1, 2, 1, 97, 3, 2, 3))
if mibBuilder.loadTexts:
    diffServSchedulerWFQ.setDescription('For use with diffServSchedulerMethod to indicate the Weighted\n            Fair Queuing scheduling method, defined as any algorithm in which\n            a set of queues are conceptually visited in some order, to\n            implement an average output rate by class. Notice attributes from\n            diffServMinRateEntry of the queues/schedulers feeding this\n            scheduler are used when determining the next packet to schedule.')
diffServMinRateNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 8, 3), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServMinRateNextFree.setDescription('This object contains an unused value for diffServMinRateId, or a\n            zero to indicate that none exist.')
diffServMinRateTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 8, 4))
if mibBuilder.loadTexts:
    diffServMinRateTable.setDescription('The Minimum Rate Parameters Table enumerates individual sets of\n            scheduling parameter that can be used/reused by Queues and\n            Schedulers.')
diffServMinRateEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1)).setIndexNames((0,
                                                                                      'DIFFSERV-MIB',
                                                                                      'diffServMinRateId'))
if mibBuilder.loadTexts:
    diffServMinRateEntry.setDescription('An entry in the Minimum Rate Parameters Table describes a single\n            set of scheduling parameters for use by one or more queues or\n            schedulers.')
diffServMinRateId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServMinRateId.setDescription('An index that enumerates the Scheduler Parameter entries.\n            Managers obtain new values for row creation in this table by\n            reading diffServMinRateNextFree.')
diffServMinRatePriority = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMinRatePriority.setDescription("The priority of this input to the associated scheduler, relative\n            to the scheduler's other inputs. A queue or scheduler with a\n            larger numeric value will be served before another with a smaller\n            numeric value.")
diffServMinRateAbsolute = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1, 3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('kilobits per second').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMinRateAbsolute.setDescription('The minimum absolute rate, in kilobits/sec, that a downstream\n            scheduler element should allocate to this queue. If the value is\n            zero, then there is effectively no minimum rate guarantee. If the\n            value is non-zero, the scheduler will assure the servicing of\n            this queue to at least this rate.\n    \n            Note that this attribute value and that of\n            diffServMinRateRelative are coupled: changes to one will affect\n            the value of the other. They are linked by the following\n            equation, in that setting one will change the other:\n    \n              diffServMinRateRelative =\n                       (diffServMinRateAbsolute*1000000)/ifSpeed\n    \n            or, if appropriate:\n    \n              diffServMinRateRelative = diffServMinRateAbsolute/ifHighSpeed')
diffServMinRateRelative = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1, 4), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMinRateRelative.setDescription('The minimum rate that a downstream scheduler element should\n            allocate to this queue, relative to the maximum rate of the\n            interface as reported by ifSpeed or ifHighSpeed, in units of\n            1/1000 of 1. If the value is zero, then there is effectively no\n            minimum rate guarantee. If the value is non-zero, the scheduler\n            will assure the servicing of this queue to at least this rate.\n    \n            Note that this attribute value and that of\n            diffServMinRateAbsolute are coupled: changes to one will affect\n            the value of the other. They are linked by the following\n            equation, in that setting one will change the other:\n    \n              diffServMinRateRelative =\n                       (diffServMinRateAbsolute*1000000)/ifSpeed\n    \n            or, if appropriate:\n    \n              diffServMinRateRelative = diffServMinRateAbsolute/ifHighSpeed')
diffServMinRateStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMinRateStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServMinRateStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 4, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMinRateStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServMaxRateNextFree = MibScalar((1, 3, 6, 1, 2, 1, 97, 1, 8, 5), IndexIntegerNextFree()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    diffServMaxRateNextFree.setDescription('This object contains an unused value for diffServMaxRateId, or a\n            zero to indicate that none exist.')
diffServMaxRateTable = MibTable((1, 3, 6, 1, 2, 1, 97, 1, 8, 6))
if mibBuilder.loadTexts:
    diffServMaxRateTable.setDescription('The Maximum Rate Parameter Table enumerates individual sets of\n            scheduling parameter that can be used/reused by Queues and\n            Schedulers.')
diffServMaxRateEntry = MibTableRow((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1)).setIndexNames((0,
                                                                                      'DIFFSERV-MIB',
                                                                                      'diffServMaxRateId'), (0,
                                                                                                             'DIFFSERV-MIB',
                                                                                                             'diffServMaxRateLevel'))
if mibBuilder.loadTexts:
    diffServMaxRateEntry.setDescription('An entry in the Maximum Rate Parameter Table describes a single\n            set of scheduling parameters for use by one or more queues or\n            schedulers.')
diffServMaxRateId = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 1), IndexInteger())
if mibBuilder.loadTexts:
    diffServMaxRateId.setDescription('An index that enumerates the Maximum Rate Parameter entries.\n            Managers obtain new values for row creation in this table by\n            reading diffServMaxRateNextFree.')
diffServMaxRateLevel = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 32)))
if mibBuilder.loadTexts:
    diffServMaxRateLevel.setDescription("An index that indicates which level of a multi-rate shaper is\n            being given its parameters. A multi-rate shaper has some number\n            of rate levels. Frame Relay's dual rate specification refers to a\n            'committed' and an 'excess' rate; ATM's dual rate specification\n            refers to a 'mean' and a 'peak' rate. This table is generalized\n            to support an arbitrary number of rates. The committed or mean\n            rate is level 1, the peak rate (if any) is the highest level rate\n            configured, and if there are other rates they are distributed in\n            monotonically increasing order between them.")
diffServMaxRateAbsolute = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 3), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setUnits('kilobits per second').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMaxRateAbsolute.setDescription('The maximum rate in kilobits/sec that a downstream scheduler\n            element should allocate to this queue. If the value is zero, then\n            there is effectively no maximum rate limit and that the scheduler\n            should attempt to be work conserving for this queue. If the value\n            is non-zero, the scheduler will limit the servicing of this queue\n            to, at most, this rate in a non-work-conserving manner.\n    \n            Note that this attribute value and that of\n            diffServMaxRateRelative are coupled: changes to one will affect\n            the value of the other. They are linked by the following\n            equation, in that setting one will change the other:\n    \n              diffServMaxRateRelative =\n                       (diffServMaxRateAbsolute*1000000)/ifSpeed\n    \n            or, if appropriate:\n    \n              diffServMaxRateRelative = diffServMaxRateAbsolute/ifHighSpeed')
diffServMaxRateRelative = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 4), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMaxRateRelative.setDescription('The maximum rate that a downstream scheduler element should\n            allocate to this queue, relative to the maximum rate of the\n            interface as reported by ifSpeed or ifHighSpeed, in units of\n            1/1000 of 1. If the value is zero, then there is effectively no\n            maximum rate limit and the scheduler should attempt to be work\n            conserving for this queue. If the value is non-zero, the\n            scheduler will limit the servicing of this queue to, at most,\n            this rate in a non-work-conserving manner.\n    \n            Note that this attribute value and that of\n            diffServMaxRateAbsolute are coupled: changes to one will affect\n            the value of the other. They are linked by the following\n            equation, in that setting one will change the other:\n    \n              diffServMaxRateRelative =\n                       (diffServMaxRateAbsolute*1000000)/ifSpeed\n    \n            or, if appropriate:\n    \n              diffServMaxRateRelative = diffServMaxRateAbsolute/ifHighSpeed')
diffServMaxRateThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 5), BurstSize()).setUnits('Bytes').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMaxRateThreshold.setDescription('The number of bytes of queue depth at which the rate of a\n            multi-rate scheduler will increase to the next output rate. In\n            the last conceptual row for such a shaper, this threshold is\n            ignored and by convention is zero.')
diffServMaxRateStorage = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMaxRateStorage.setDescription("The storage type for this conceptual row.  Conceptual rows\n            having the value 'permanent' need not allow write-access to any\n            columnar objects in the row.")
diffServMaxRateStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 97, 1, 8, 6, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    diffServMaxRateStatus.setDescription("The status of this conceptual row. All writable objects in this\n            row may be modified at any time. Setting this variable to\n            'destroy' when the MIB contains one or more RowPointers pointing\n            to it results in destruction being delayed until the row is no\n            longer used.")
diffServMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 2, 1))
diffServMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 97, 2, 2))
diffServMIBFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 97, 2, 1, 1)).setObjects(*(('IF-MIB', 'ifCounterDiscontinuityGroup'), ('DIFFSERV-MIB', 'diffServMIBDataPathGroup'), ('DIFFSERV-MIB', 'diffServMIBClfrGroup'), ('DIFFSERV-MIB', 'diffServMIBClfrElementGroup'), ('DIFFSERV-MIB', 'diffServMIBMultiFieldClfrGroup'), ('DIFFSERV-MIB', 'diffServMIBActionGroup'), ('DIFFSERV-MIB', 'diffServMIBAlgDropGroup'), ('DIFFSERV-MIB', 'diffServMIBQGroup'), ('DIFFSERV-MIB', 'diffServMIBSchedulerGroup'), ('DIFFSERV-MIB', 'diffServMIBMaxRateGroup'), ('DIFFSERV-MIB', 'diffServMIBMinRateGroup'), ('DIFFSERV-MIB', 'diffServMIBCounterGroup'), ('DIFFSERV-MIB', 'diffServMIBMeterGroup'), ('DIFFSERV-MIB', 'diffServMIBTBParamGroup'), ('DIFFSERV-MIB', 'diffServMIBDscpMarkActGroup'), ('DIFFSERV-MIB', 'diffServMIBRandomDropGroup')))
if mibBuilder.loadTexts:
    diffServMIBFullCompliance.setDescription('When this MIB is implemented with support for read-create, then\n            such an implementation can claim full compliance. Such devices\n            can then be both monitored and configured with this MIB.')
diffServMIBReadOnlyCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 97, 2, 1, 2)).setObjects(*(('IF-MIB', 'ifCounterDiscontinuityGroup'), ('DIFFSERV-MIB', 'diffServMIBDataPathGroup'), ('DIFFSERV-MIB', 'diffServMIBClfrGroup'), ('DIFFSERV-MIB', 'diffServMIBClfrElementGroup'), ('DIFFSERV-MIB', 'diffServMIBMultiFieldClfrGroup'), ('DIFFSERV-MIB', 'diffServMIBActionGroup'), ('DIFFSERV-MIB', 'diffServMIBAlgDropGroup'), ('DIFFSERV-MIB', 'diffServMIBQGroup'), ('DIFFSERV-MIB', 'diffServMIBSchedulerGroup'), ('DIFFSERV-MIB', 'diffServMIBMaxRateGroup'), ('DIFFSERV-MIB', 'diffServMIBMinRateGroup'), ('DIFFSERV-MIB', 'diffServMIBCounterGroup'), ('DIFFSERV-MIB', 'diffServMIBMeterGroup'), ('DIFFSERV-MIB', 'diffServMIBTBParamGroup'), ('DIFFSERV-MIB', 'diffServMIBDscpMarkActGroup'), ('DIFFSERV-MIB', 'diffServMIBRandomDropGroup')))
if mibBuilder.loadTexts:
    diffServMIBReadOnlyCompliance.setDescription('When this MIB is implemented without support for read-create\n            (i.e. in read-only mode), then such an implementation can claim\n            read-only compliance. Such a device can then be monitored but can\n            not be configured with this MIB.')
diffServMIBDataPathGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 1)).setObjects(*(('DIFFSERV-MIB', 'diffServDataPathStart'), ('DIFFSERV-MIB', 'diffServDataPathStorage'), ('DIFFSERV-MIB', 'diffServDataPathStatus')))
if mibBuilder.loadTexts:
    diffServMIBDataPathGroup.setDescription('The Data Path Group defines the MIB Objects that describe a\n            functional data path.')
diffServMIBClfrGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 2)).setObjects(*(('DIFFSERV-MIB', 'diffServClfrNextFree'), ('DIFFSERV-MIB', 'diffServClfrStorage'), ('DIFFSERV-MIB', 'diffServClfrStatus')))
if mibBuilder.loadTexts:
    diffServMIBClfrGroup.setDescription('The Classifier Group defines the MIB Objects that describe the\n            list the starts of individual classifiers.')
diffServMIBClfrElementGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 3)).setObjects(*(('DIFFSERV-MIB', 'diffServClfrElementNextFree'), ('DIFFSERV-MIB', 'diffServClfrElementPrecedence'), ('DIFFSERV-MIB', 'diffServClfrElementNext'), ('DIFFSERV-MIB', 'diffServClfrElementSpecific'), ('DIFFSERV-MIB', 'diffServClfrElementStorage'), ('DIFFSERV-MIB', 'diffServClfrElementStatus')))
if mibBuilder.loadTexts:
    diffServMIBClfrElementGroup.setDescription('The Classifier Element Group defines the MIB Objects that\n            describe the classifier elements that make up a generic\n            classifier.')
diffServMIBMultiFieldClfrGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 4)).setObjects(*(('DIFFSERV-MIB', 'diffServMultiFieldClfrNextFree'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrAddrType'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrDstAddr'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrDstPrefixLength'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrFlowId'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrSrcAddr'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrSrcPrefixLength'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrDscp'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrProtocol'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrDstL4PortMin'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrDstL4PortMax'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrSrcL4PortMin'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrSrcL4PortMax'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrStorage'), ('DIFFSERV-MIB', 'diffServMultiFieldClfrStatus')))
if mibBuilder.loadTexts:
    diffServMIBMultiFieldClfrGroup.setDescription('The Multi-field Classifier Group defines the MIB Objects that\n            describe a classifier element for matching on various fields of\n            an IP and upper-layer protocol header.')
diffServMIBMeterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 5)).setObjects(*(('DIFFSERV-MIB', 'diffServMeterNextFree'), ('DIFFSERV-MIB', 'diffServMeterSucceedNext'), ('DIFFSERV-MIB', 'diffServMeterFailNext'), ('DIFFSERV-MIB', 'diffServMeterSpecific'), ('DIFFSERV-MIB', 'diffServMeterStorage'), ('DIFFSERV-MIB', 'diffServMeterStatus')))
if mibBuilder.loadTexts:
    diffServMIBMeterGroup.setDescription('The Meter Group defines the objects used in describing a generic\n            meter element.')
diffServMIBTBParamGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 6)).setObjects(*(('DIFFSERV-MIB', 'diffServTBParamNextFree'), ('DIFFSERV-MIB', 'diffServTBParamType'), ('DIFFSERV-MIB', 'diffServTBParamRate'), ('DIFFSERV-MIB', 'diffServTBParamBurstSize'), ('DIFFSERV-MIB', 'diffServTBParamInterval'), ('DIFFSERV-MIB', 'diffServTBParamStorage'), ('DIFFSERV-MIB', 'diffServTBParamStatus')))
if mibBuilder.loadTexts:
    diffServMIBTBParamGroup.setDescription('The Token-Bucket Meter Group defines the objects used in\n            describing a token bucket meter element.')
diffServMIBActionGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 7)).setObjects(*(('DIFFSERV-MIB', 'diffServActionNextFree'), ('DIFFSERV-MIB', 'diffServActionNext'), ('DIFFSERV-MIB', 'diffServActionSpecific'), ('DIFFSERV-MIB', 'diffServActionStorage'), ('DIFFSERV-MIB', 'diffServActionInterface'), ('DIFFSERV-MIB', 'diffServActionStatus')))
if mibBuilder.loadTexts:
    diffServMIBActionGroup.setDescription('The Action Group defines the objects used in describing a\n            generic action element.')
diffServMIBDscpMarkActGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 8)).setObjects(*(('DIFFSERV-MIB', 'diffServDscpMarkActDscp'), ))
if mibBuilder.loadTexts:
    diffServMIBDscpMarkActGroup.setDescription('The DSCP Mark Action Group defines the objects used in\n            describing a DSCP Marking Action element.')
diffServMIBCounterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 9)).setObjects(*(('DIFFSERV-MIB', 'diffServCountActOctets'), ('DIFFSERV-MIB', 'diffServCountActPkts'), ('DIFFSERV-MIB', 'diffServAlgDropOctets'), ('DIFFSERV-MIB', 'diffServAlgDropPkts'), ('DIFFSERV-MIB', 'diffServAlgRandomDropOctets'), ('DIFFSERV-MIB', 'diffServAlgRandomDropPkts'), ('DIFFSERV-MIB', 'diffServCountActStorage'), ('DIFFSERV-MIB', 'diffServCountActStatus'), ('DIFFSERV-MIB', 'diffServCountActNextFree')))
if mibBuilder.loadTexts:
    diffServMIBCounterGroup.setDescription('A collection of objects providing information specific to\n            packet-oriented network interfaces.')
diffServMIBAlgDropGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 10)).setObjects(*(('DIFFSERV-MIB', 'diffServAlgDropNextFree'), ('DIFFSERV-MIB', 'diffServAlgDropType'), ('DIFFSERV-MIB', 'diffServAlgDropNext'), ('DIFFSERV-MIB', 'diffServAlgDropQMeasure'), ('DIFFSERV-MIB', 'diffServAlgDropQThreshold'), ('DIFFSERV-MIB', 'diffServAlgDropSpecific'), ('DIFFSERV-MIB', 'diffServAlgDropStorage'), ('DIFFSERV-MIB', 'diffServAlgDropStatus')))
if mibBuilder.loadTexts:
    diffServMIBAlgDropGroup.setDescription('The Algorithmic Drop Group contains the objects that describe\n            algorithmic dropper operation and configuration.')
diffServMIBRandomDropGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 11)).setObjects(*(('DIFFSERV-MIB', 'diffServRandomDropNextFree'), ('DIFFSERV-MIB', 'diffServRandomDropMinThreshBytes'), ('DIFFSERV-MIB', 'diffServRandomDropMinThreshPkts'), ('DIFFSERV-MIB', 'diffServRandomDropMaxThreshBytes'), ('DIFFSERV-MIB', 'diffServRandomDropMaxThreshPkts'), ('DIFFSERV-MIB', 'diffServRandomDropProbMax'), ('DIFFSERV-MIB', 'diffServRandomDropWeight'), ('DIFFSERV-MIB', 'diffServRandomDropSamplingRate'), ('DIFFSERV-MIB', 'diffServRandomDropStorage'), ('DIFFSERV-MIB', 'diffServRandomDropStatus')))
if mibBuilder.loadTexts:
    diffServMIBRandomDropGroup.setDescription('The Random Drop Group augments the Algorithmic Drop Group for\n            random dropper operation and configuration.')
diffServMIBQGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 12)).setObjects(*(('DIFFSERV-MIB', 'diffServQNextFree'), ('DIFFSERV-MIB', 'diffServQNext'), ('DIFFSERV-MIB', 'diffServQMinRate'), ('DIFFSERV-MIB', 'diffServQMaxRate'), ('DIFFSERV-MIB', 'diffServQStorage'), ('DIFFSERV-MIB', 'diffServQStatus')))
if mibBuilder.loadTexts:
    diffServMIBQGroup.setDescription("The Queue Group contains the objects that describe an\n            interface's queues.")
diffServMIBSchedulerGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 13)).setObjects(*(('DIFFSERV-MIB', 'diffServSchedulerNextFree'), ('DIFFSERV-MIB', 'diffServSchedulerNext'), ('DIFFSERV-MIB', 'diffServSchedulerMethod'), ('DIFFSERV-MIB', 'diffServSchedulerMinRate'), ('DIFFSERV-MIB', 'diffServSchedulerMaxRate'), ('DIFFSERV-MIB', 'diffServSchedulerStorage'), ('DIFFSERV-MIB', 'diffServSchedulerStatus')))
if mibBuilder.loadTexts:
    diffServMIBSchedulerGroup.setDescription('The Scheduler Group contains the objects that describe packet\n            schedulers on interfaces.')
diffServMIBMinRateGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 14)).setObjects(*(('DIFFSERV-MIB', 'diffServMinRateNextFree'), ('DIFFSERV-MIB', 'diffServMinRatePriority'), ('DIFFSERV-MIB', 'diffServMinRateAbsolute'), ('DIFFSERV-MIB', 'diffServMinRateRelative'), ('DIFFSERV-MIB', 'diffServMinRateStorage'), ('DIFFSERV-MIB', 'diffServMinRateStatus')))
if mibBuilder.loadTexts:
    diffServMIBMinRateGroup.setDescription("The Minimum Rate Parameter Group contains the objects that\n            describe packet schedulers' minimum rate or priority guarantees.")
diffServMIBMaxRateGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 97, 2, 2, 15)).setObjects(*(('DIFFSERV-MIB', 'diffServMaxRateNextFree'), ('DIFFSERV-MIB', 'diffServMaxRateAbsolute'), ('DIFFSERV-MIB', 'diffServMaxRateRelative'), ('DIFFSERV-MIB', 'diffServMaxRateThreshold'), ('DIFFSERV-MIB', 'diffServMaxRateStorage'), ('DIFFSERV-MIB', 'diffServMaxRateStatus')))
if mibBuilder.loadTexts:
    diffServMIBMaxRateGroup.setDescription("The Maximum Rate Parameter Group contains the objects that\n            describe packet schedulers' maximum rate guarantees.")
mibBuilder.exportSymbols('DIFFSERV-MIB', diffServAlgRandomDropPkts=diffServAlgRandomDropPkts, diffServAlgDropOctets=diffServAlgDropOctets, diffServClfrElementId=diffServClfrElementId, diffServMIBSchedulerGroup=diffServMIBSchedulerGroup, diffServQId=diffServQId, diffServMIBMultiFieldClfrGroup=diffServMIBMultiFieldClfrGroup, diffServTBParamTswTCM=diffServTBParamTswTCM, diffServActionEntry=diffServActionEntry, diffServMultiFieldClfrStatus=diffServMultiFieldClfrStatus, diffServMib=diffServMib, diffServSchedulerMethod=diffServSchedulerMethod, diffServMIBReadOnlyCompliance=diffServMIBReadOnlyCompliance, diffServClfrStorage=diffServClfrStorage, diffServMIBClfrElementGroup=diffServMIBClfrElementGroup, diffServMultiFieldClfrDstL4PortMin=diffServMultiFieldClfrDstL4PortMin, diffServMaxRateStorage=diffServMaxRateStorage, diffServMultiFieldClfrDscp=diffServMultiFieldClfrDscp, diffServDscpMarkActTable=diffServDscpMarkActTable, diffServMIBGroups=diffServMIBGroups, diffServMinRateTable=diffServMinRateTable, diffServTBParamBurstSize=diffServTBParamBurstSize, diffServClfrTable=diffServClfrTable, diffServDscpMarkActDscp=diffServDscpMarkActDscp, diffServSchedulerId=diffServSchedulerId, diffServScheduler=diffServScheduler, diffServClfrElementEntry=diffServClfrElementEntry, diffServMinRateStatus=diffServMinRateStatus, diffServClfrElementSpecific=diffServClfrElementSpecific, diffServQEntry=diffServQEntry, diffServAlgDropNextFree=diffServAlgDropNextFree, diffServActionNext=diffServActionNext, diffServMaxRateId=diffServMaxRateId, diffServDataPath=diffServDataPath, diffServTBParamTrTCMBlind=diffServTBParamTrTCMBlind, diffServMIBAdmin=diffServMIBAdmin, diffServAlgDropStatus=diffServAlgDropStatus, diffServSchedulerTable=diffServSchedulerTable, diffServMinRateAbsolute=diffServMinRateAbsolute, diffServMaxRateNextFree=diffServMaxRateNextFree, diffServClassifier=diffServClassifier, diffServQueue=diffServQueue, diffServActionNextFree=diffServActionNextFree, diffServMIBDscpMarkActGroup=diffServMIBDscpMarkActGroup, diffServAlgDrop=diffServAlgDrop, diffServCountActStorage=diffServCountActStorage, diffServTBParamTrTCMAware=diffServTBParamTrTCMAware, diffServSchedulerStorage=diffServSchedulerStorage, diffServSchedulerStatus=diffServSchedulerStatus, diffServRandomDropProbMax=diffServRandomDropProbMax, diffServClfrElementStorage=diffServClfrElementStorage, diffServTBParamStatus=diffServTBParamStatus, diffServDscpMarkActEntry=diffServDscpMarkActEntry, diffServAlgDropQMeasure=diffServAlgDropQMeasure, diffServRandomDropId=diffServRandomDropId, diffServClfrElementStatus=diffServClfrElementStatus, diffServMeterTable=diffServMeterTable, diffServMeterStorage=diffServMeterStorage, diffServMIBMinRateGroup=diffServMIBMinRateGroup, diffServMIBMaxRateGroup=diffServMIBMaxRateGroup, diffServMIBClfrGroup=diffServMIBClfrGroup, diffServQNext=diffServQNext, PYSNMP_MODULE_ID=diffServMib, diffServMultiFieldClfrDstAddr=diffServMultiFieldClfrDstAddr, diffServTBMeters=diffServTBMeters, diffServCountActNextFree=diffServCountActNextFree, diffServAlgDropSpecific=diffServAlgDropSpecific, diffServRandomDropMinThreshPkts=diffServRandomDropMinThreshPkts, diffServAlgDropEntry=diffServAlgDropEntry, diffServMIBFullCompliance=diffServMIBFullCompliance, diffServMIBActionGroup=diffServMIBActionGroup, diffServSchedulerEntry=diffServSchedulerEntry, diffServMaxRateLevel=diffServMaxRateLevel, diffServDataPathStatus=diffServDataPathStatus, diffServRandomDropTable=diffServRandomDropTable, diffServTBParamId=diffServTBParamId, diffServCountActEntry=diffServCountActEntry, diffServMIBQGroup=diffServMIBQGroup, diffServMeterSpecific=diffServMeterSpecific, diffServClfrElementNextFree=diffServClfrElementNextFree, diffServActionStorage=diffServActionStorage, diffServMIBTBParamGroup=diffServMIBTBParamGroup, diffServMinRatePriority=diffServMinRatePriority, diffServAction=diffServAction, diffServSchedulerWFQ=diffServSchedulerWFQ, diffServSchedulerPriority=diffServSchedulerPriority, diffServMIBCounterGroup=diffServMIBCounterGroup, diffServAlgDropStorage=diffServAlgDropStorage, diffServMaxRateTable=diffServMaxRateTable, diffServQStorage=diffServQStorage, diffServMultiFieldClfrDstPrefixLength=diffServMultiFieldClfrDstPrefixLength, diffServMultiFieldClfrId=diffServMultiFieldClfrId, diffServMeter=diffServMeter, diffServMultiFieldClfrDstL4PortMax=diffServMultiFieldClfrDstL4PortMax, diffServAlgDropQThreshold=diffServAlgDropQThreshold, diffServActionTable=diffServActionTable, diffServMultiFieldClfrSrcL4PortMax=diffServMultiFieldClfrSrcL4PortMax, diffServMultiFieldClfrTable=diffServMultiFieldClfrTable, diffServMaxRateRelative=diffServMaxRateRelative, diffServQStatus=diffServQStatus, diffServMIBRandomDropGroup=diffServMIBRandomDropGroup, diffServMinRateNextFree=diffServMinRateNextFree, diffServSchedulerMaxRate=diffServSchedulerMaxRate, diffServMeterNextFree=diffServMeterNextFree, diffServDataPathStorage=diffServDataPathStorage, diffServSchedulerNext=diffServSchedulerNext, diffServMultiFieldClfrAddrType=diffServMultiFieldClfrAddrType, diffServQNextFree=diffServQNextFree, diffServMIBAlgDropGroup=diffServMIBAlgDropGroup, diffServTBParamNextFree=diffServTBParamNextFree, diffServMultiFieldClfrSrcL4PortMin=diffServMultiFieldClfrSrcL4PortMin, diffServClfrElementTable=diffServClfrElementTable, diffServMeterSucceedNext=diffServMeterSucceedNext, diffServAlgDropNext=diffServAlgDropNext, diffServMultiFieldClfrSrcPrefixLength=diffServMultiFieldClfrSrcPrefixLength, diffServTBParam=diffServTBParam, diffServDataPathTable=diffServDataPathTable, diffServMultiFieldClfrSrcAddr=diffServMultiFieldClfrSrcAddr, diffServMultiFieldClfrFlowId=diffServMultiFieldClfrFlowId, diffServSchedulerNextFree=diffServSchedulerNextFree, diffServSchedulerWRR=diffServSchedulerWRR, diffServClfrElementPrecedence=diffServClfrElementPrecedence, diffServCountActPkts=diffServCountActPkts, diffServRandomDropStatus=diffServRandomDropStatus, diffServTBParamInterval=diffServTBParamInterval, diffServTBParamAvgRate=diffServTBParamAvgRate, diffServRandomDropWeight=diffServRandomDropWeight, diffServMultiFieldClfrNextFree=diffServMultiFieldClfrNextFree, diffServClfrStatus=diffServClfrStatus, diffServActionStatus=diffServActionStatus, diffServMultiFieldClfrEntry=diffServMultiFieldClfrEntry, diffServMeterEntry=diffServMeterEntry, diffServTBParamSimpleTokenBucket=diffServTBParamSimpleTokenBucket, diffServMinRateEntry=diffServMinRateEntry, diffServMultiFieldClfrStorage=diffServMultiFieldClfrStorage, diffServMaxRateEntry=diffServMaxRateEntry, diffServAlgRandomDropOctets=diffServAlgRandomDropOctets, diffServTBParamRate=diffServTBParamRate, diffServAlgDropId=diffServAlgDropId, diffServCountActOctets=diffServCountActOctets, diffServRandomDropStorage=diffServRandomDropStorage, diffServCountActId=diffServCountActId, diffServMinRateId=diffServMinRateId, IndexIntegerNextFree=IndexIntegerNextFree, diffServTBParamSrTCMBlind=diffServTBParamSrTCMBlind, diffServAlgDropTable=diffServAlgDropTable, diffServAlgDropType=diffServAlgDropType, diffServMeterId=diffServMeterId, diffServRandomDropNextFree=diffServRandomDropNextFree, diffServMIBDataPathGroup=diffServMIBDataPathGroup, diffServDataPathEntry=diffServDataPathEntry, diffServMIBObjects=diffServMIBObjects, diffServTBParamSrTCMAware=diffServTBParamSrTCMAware, diffServClfrId=diffServClfrId, diffServMIBConformance=diffServMIBConformance, diffServRandomDropEntry=diffServRandomDropEntry, IfDirection=IfDirection, diffServQMinRate=diffServQMinRate, diffServDataPathStart=diffServDataPathStart, diffServRandomDropMaxThreshPkts=diffServRandomDropMaxThreshPkts, diffServMaxRateThreshold=diffServMaxRateThreshold, diffServMeterFailNext=diffServMeterFailNext, diffServSchedulerMinRate=diffServSchedulerMinRate, diffServActionInterface=diffServActionInterface, diffServCountActTable=diffServCountActTable, diffServQMaxRate=diffServQMaxRate, diffServMIBCompliances=diffServMIBCompliances, diffServClfrNextFree=diffServClfrNextFree, diffServQTable=diffServQTable, diffServClfrEntry=diffServClfrEntry, diffServMinRateStorage=diffServMinRateStorage, diffServMeterStatus=diffServMeterStatus, diffServRandomDropMinThreshBytes=diffServRandomDropMinThreshBytes, diffServClfrElementNext=diffServClfrElementNext, diffServMaxRateStatus=diffServMaxRateStatus, diffServRandomDropSamplingRate=diffServRandomDropSamplingRate, diffServTBParamTable=diffServTBParamTable, IndexInteger=IndexInteger, diffServMultiFieldClfrProtocol=diffServMultiFieldClfrProtocol, diffServMIBMeterGroup=diffServMIBMeterGroup, diffServActionId=diffServActionId, diffServRandomDropMaxThreshBytes=diffServRandomDropMaxThreshBytes, diffServTBParamEntry=diffServTBParamEntry, diffServMinRateRelative=diffServMinRateRelative, diffServAlgDropPkts=diffServAlgDropPkts, diffServDataPathIfDirection=diffServDataPathIfDirection, diffServCountActStatus=diffServCountActStatus, diffServSchedulers=diffServSchedulers, diffServTBParamType=diffServTBParamType, diffServTBParamStorage=diffServTBParamStorage, diffServMaxRateAbsolute=diffServMaxRateAbsolute, diffServActionSpecific=diffServActionSpecific)