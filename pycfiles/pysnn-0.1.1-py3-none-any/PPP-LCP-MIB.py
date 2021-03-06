# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/PPP-LCP-MIB.py
# Compiled at: 2016-02-13 18:24:12
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ValueRangeConstraint, SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ValueRangeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueSizeConstraint')
(ifIndex,) = mibBuilder.importSymbols('IF-MIB', 'ifIndex')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Bits, NotificationType, IpAddress, transmission, iso, Unsigned32, Counter64, ModuleIdentity, Integer32, Counter32, MibIdentifier, ObjectIdentity, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Bits', 'NotificationType', 'IpAddress', 'transmission', 'iso', 'Unsigned32', 'Counter64', 'ModuleIdentity', 'Integer32', 'Counter32', 'MibIdentifier', 'ObjectIdentity', 'TimeTicks', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
ppp = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23))
pppLcp = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23, 1))
pppLink = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23, 1, 1))
pppLqr = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23, 1, 2))
pppTests = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23, 1, 3))
pppLinkStatusTable = MibTable((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1))
if mibBuilder.loadTexts:
    pppLinkStatusTable.setDescription('A table containing PPP-link specific variables\n                         for this PPP implementation.')
pppLinkStatusEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1)).setIndexNames((0,
                                                                                        'IF-MIB',
                                                                                        'ifIndex'))
if mibBuilder.loadTexts:
    pppLinkStatusEntry.setDescription('Management information about a particular PPP\n                         Link.')
pppLinkStatusPhysicalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1,
                                             1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusPhysicalIndex.setDescription("The value of ifIndex that identifies the\n                         lower-level interface over which this PPP Link\n                         is operating. This interface would usually be\n                         an HDLC or RS-232 type of interface. If there\n                         is no lower-layer interface element, or there\n                         is no ifEntry for the element, or the element\n                         can not be identified, then the value of this\n                         object is 0.  For example, suppose that PPP is\n                         operating over a serial port. This would use\n                         two entries in the ifTable. The PPP could be\n                         running over `interface' number 123 and the\n                         serial port could be running over `interface'\n                         number 987.  Therefore, ifSpecific.123 would\n                         contain the OBJECT IDENTIFIER ppp\n                         pppLinkStatusPhysicalIndex.123 would contain\n                         987, and ifSpecific.987 would contain the\n                         OBJECT IDENTIFIER for the serial-port's media-\n                         specific MIB.")
pppLinkStatusBadAddresses = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusBadAddresses.setDescription('The number of packets received with an\n                         incorrect Address Field. This counter is a\n                         component of the ifInErrors variable that is\n                         associated with the interface that represents\n                         this PPP Link.')
pppLinkStatusBadControls = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusBadControls.setDescription('The number of packets received on this link\n                         with an incorrect Control Field. This counter\n                         is a component of the ifInErrors variable that\n                         is associated with the interface that\n                         represents this PPP Link.')
pppLinkStatusPacketTooLongs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1,
                                              4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusPacketTooLongs.setDescription('The number of received packets that have been\n                         discarded because their length exceeded the\n                         MRU. This counter is a component of the\n                         ifInErrors variable that is associated with the\n                         interface that represents this PPP Link. NOTE,\n                         packets which are longer than the MRU but which\n                         are successfully received and processed are NOT\n                         included in this count.')
pppLinkStatusBadFCSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusBadFCSs.setDescription('The number of received packets that have been\n                         discarded due to having an incorrect FCS. This\n                         counter is a component of the ifInErrors\n                         variable that is associated with the interface\n                         that represents this PPP Link.')
pppLinkStatusLocalMRU = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483648))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusLocalMRU.setDescription('The current value of the MRU for the local PPP\n                         Entity. This value is the MRU that the remote\n                         entity is using when sending packets to the\n                         local PPP entity. The value of this object is\n                         meaningful only when the link has reached the\n                         open state (ifOperStatus is up).')
pppLinkStatusRemoteMRU = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483648))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusRemoteMRU.setDescription('The current value of the MRU for the remote\n                         PPP Entity. This value is the MRU that the\n                         local entity is using when sending packets to\n                         the remote PPP entity. The value of this object\n                         is meaningful only when the link has reached\n                         the open state (ifOperStatus is up).')
pppLinkStatusLocalToPeerACCMap = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1,
                                                 1, 8), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4, 4)).setFixedLength(4)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusLocalToPeerACCMap.setDescription('The current value of the ACC Map used for\n                         sending packets from the local PPP entity to\n                         the remote PPP entity. The value of this object\n                         is meaningful only when the link has reached\n                         the open state (ifOperStatus is up).')
pppLinkStatusPeerToLocalACCMap = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1,
                                                 1, 9), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4, 4)).setFixedLength(4)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusPeerToLocalACCMap.setDescription('The ACC Map used by the remote PPP entity when\n                         transmitting packets to the local PPP entity.\n                         The value of this object is meaningful only\n                         when the link has reached the open state\n                         (ifOperStatus is up).')
pppLinkStatusLocalToRemoteProtocolCompression = MibTableColumn((1, 3, 6, 1, 2, 1, 10,
                                                                23, 1, 1, 1, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                                   1), ('disabled',
                                                                                                                                                                                                        2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusLocalToRemoteProtocolCompression.setDescription('Indicates whether the local PPP entity will\n                         use Protocol Compression when transmitting\n                         packets to the remote PPP entity. The value of\n                         this object is meaningful only when the link\n                         has reached the open state (ifOperStatus is\n                         up).')
pppLinkStatusRemoteToLocalProtocolCompression = MibTableColumn((1, 3, 6, 1, 2, 1, 10,
                                                                23, 1, 1, 1, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                                   1), ('disabled',
                                                                                                                                                                                                        2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusRemoteToLocalProtocolCompression.setDescription('Indicates whether the remote PPP entity will\n                         use Protocol Compression when transmitting\n                         packets to the local PPP entity. The value of\n                         this object is meaningful only when the link\n                         has reached the open state (ifOperStatus is\n                         up).')
pppLinkStatusLocalToRemoteACCompression = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23,
                                                          1, 1, 1, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                         1), ('disabled',
                                                                                                                                                                                              2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusLocalToRemoteACCompression.setDescription('Indicates whether the local PPP entity will\n                         use Address and Control Compression when\n                         transmitting packets to the remote PPP entity.\n                         The value of this object is meaningful only\n                         when the link has reached the open state\n                         (ifOperStatus is up).')
pppLinkStatusRemoteToLocalACCompression = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23,
                                                          1, 1, 1, 1, 13), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                         1), ('disabled',
                                                                                                                                                                                              2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusRemoteToLocalACCompression.setDescription('Indicates whether the remote PPP entity will\n                         use Address and Control Compression when\n                         transmitting packets to the local PPP entity.\n                         The value of this object is meaningful only\n                         when the link has reached the open state\n                         (ifOperStatus is up).')
pppLinkStatusTransmitFcsSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1,
                                               14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusTransmitFcsSize.setDescription('The size of the Frame Check Sequence (FCS) in\n                         bits that the local node will generate when\n                         sending packets to the remote node. The value\n                         of this object is meaningful only when the link\n                         has reached the open state (ifOperStatus is\n                         up).')
pppLinkStatusReceiveFcsSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 1, 1,
                                              15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLinkStatusReceiveFcsSize.setDescription('The size of the Frame Check Sequence (FCS) in\n                         bits that the remote node will generate when\n                         sending packets to the local node. The value of\n                         this object is meaningful only when the link\n                         has reached the open state (ifOperStatus is\n                         up).')
pppLinkConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2))
if mibBuilder.loadTexts:
    pppLinkConfigTable.setDescription('A table containing the LCP configuration\n                         parameters for this PPP Link. These variables\n                         represent the initial configuration of the PPP\n                         Link. The actual values of the parameters may\n                         be changed when the link is brought up via the\n                         LCP options negotiation mechanism.')
pppLinkConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2, 1)).setIndexNames((0,
                                                                                        'IF-MIB',
                                                                                        'ifIndex'))
if mibBuilder.loadTexts:
    pppLinkConfigEntry.setDescription('Configuration information about a particular\n                         PPP Link.')
pppLinkConfigInitialMRU = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647)).clone(1500)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLinkConfigInitialMRU.setDescription('The initial Maximum Receive Unit (MRU) that\n                         the local PPP entity will advertise to the\n                         remote entity. If the value of this variable is\n                         0 then the local PPP entity will not advertise\n                         any MRU to the remote entity and the default\n                         MRU will be assumed. Changing this object will\n                         have effect when the link is next restarted.')
pppLinkConfigReceiveACCMap = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2, 1,
                                             2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4, 4)).setFixedLength(4).clone(hexValue='ffffffff')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLinkConfigReceiveACCMap.setDescription("The Asynchronous-Control-Character-Map (ACC)\n                         that the local PPP entity requires for use on\n                         its receive side. In effect, this is the ACC\n                         Map that is required in order to ensure that\n                         the local modem will successfully receive all\n                         characters. The actual ACC map used on the\n                         receive side of the link will be a combination\n                         of the local node's pppLinkConfigReceiveACCMap\n                         and the remote node's\n                         pppLinkConfigTransmitACCMap. Changing this\n                         object will have effect when the link is next\n                         restarted.")
pppLinkConfigTransmitACCMap = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2, 1,
                                              3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4, 4)).setFixedLength(4).clone(hexValue='ffffffff')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLinkConfigTransmitACCMap.setDescription("The Asynchronous-Control-Character-Map (ACC)\n                         that the local PPP entity requires for use on\n                         its transmit side. In effect, this is the ACC\n                         Map that is required in order to ensure that\n                         all characters can be successfully transmitted\n                         through the local modem.  The actual ACC map\n                         used on the transmit side of the link will be a\n                         combination of the local node's\n                         pppLinkConfigTransmitACCMap and the remote\n                         node's pppLinkConfigReceiveACCMap. Changing\n                         this object will have effect when the link is\n                         next restarted.")
pppLinkConfigMagicNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('false',
                                                                                                                                                                                                   1), ('true',
                                                                                                                                                                                                        2))).clone('false')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLinkConfigMagicNumber.setDescription('If true(2) then the local node will attempt to\n                         perform Magic Number negotiation with the\n                         remote node. If false(1) then this negotiation\n                         is not performed. In any event, the local node\n                         will comply with any magic number negotiations\n                         attempted by the remote node, per the PPP\n                         specification. Changing this object will have\n                         effect when the link is next restarted.')
pppLinkConfigFcsSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 1, 2, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 128)).clone(16)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLinkConfigFcsSize.setDescription('The size of the FCS, in bits, the local node\n                         will attempt to negotiate for use with the\n                         remote node. Regardless of the value of this\n                         object, the local node will comply with any FCS\n                         size negotiations initiated by the remote node,\n                         per the PPP specification. Changing this object\n                         will have effect when the link is next\n                         restarted.')
pppLqrTable = MibTable((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1))
if mibBuilder.loadTexts:
    pppLqrTable.setDescription('Table containing the LQR parameters and\n                         statistics for the local PPP entity.')
pppLqrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1)).setIndexNames((0,
                                                                                 'IF-MIB',
                                                                                 'ifIndex'))
if mibBuilder.loadTexts:
    pppLqrEntry.setDescription('LQR information for a particular PPP link. A\n                         PPP link will have an entry in this table if\n                         and only if LQR Quality Monitoring has been\n                         successfully negotiated for said link.')
pppLqrQuality = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('good',
                                                                                                                                                                                           1), ('bad',
                                                                                                                                                                                                2), ('not-determined',
                                                                                                                                                                                                     3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrQuality.setDescription("The current quality of the link as declared by\n                         the local PPP entity's Link-Quality Management\n                         modules. No effort is made to define good or\n                         bad, nor the policy used to determine it. The\n                         not-determined value indicates that the entity\n                         does not actually evaluate the link's quality.\n                         This value is used to disambiguate the\n                         `determined to be good' case from the `no\n                         determination made and presumed to be good'\n                         case.")
pppLqrInGoodOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrInGoodOctets.setDescription('The LQR InGoodOctets counter for this link.')
pppLqrLocalPeriod = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483648))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrLocalPeriod.setDescription('The LQR reporting period, in hundredths of a\n                         second that is in effect for the local PPP\n                         entity.')
pppLqrRemotePeriod = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483648))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrRemotePeriod.setDescription('The LQR reporting period, in hundredths of a\n                         second, that is in effect for the remote PPP\n                         entity.')
pppLqrOutLQRs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrOutLQRs.setDescription('The value of the OutLQRs counter on the local\n                         node for the link identified by ifIndex.')
pppLqrInLQRs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 1, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrInLQRs.setDescription('The value of the InLQRs counter on the local\n                         node for the link identified by ifIndex.')
pppLqrConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 2))
if mibBuilder.loadTexts:
    pppLqrConfigTable.setDescription('Table containing the LQR Configuration\n                         parameters for the local PPP entity.')
pppLqrConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 2, 1)).setIndexNames((0,
                                                                                       'IF-MIB',
                                                                                       'ifIndex'))
if mibBuilder.loadTexts:
    pppLqrConfigEntry.setDescription('LQR configuration information for a particular\n                         PPP link.')
pppLqrConfigPeriod = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLqrConfigPeriod.setDescription('The LQR Reporting Period that the local PPP\n                         entity will attempt to negotiate with the\n                         remote entity, in units of hundredths of a\n                         second. Changing this object will have effect\n                         when the link is next restarted.')
pppLqrConfigStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('disabled',
                                                                                                                                                                                             1), ('enabled',
                                                                                                                                                                                                  2))).clone('enabled')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pppLqrConfigStatus.setDescription('If enabled(2) then the local node will attempt\n                         to perform LQR negotiation with the remote\n                         node. If disabled(1) then this negotiation is\n                         not performed. In any event, the local node\n                         will comply with any magic number negotiations\n                         attempted by the remote node, per the PPP\n                         specification. Changing this object will have\n                         effect when the link is next restarted.\n                         Setting this object to the value disabled(1)\n                         has the effect of invalidating the\n                         corresponding entry in the pppLqrConfigTable\n                         object. It is an implementation-specific matter\n                         as to whether the agent removes an invalidated\n                         entry from the table. Accordingly, management\n                         stations must be prepared to receive tabular\n                         information from agents that corresponds to\n                         entries not currently in use.')
pppLqrExtnsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 3))
if mibBuilder.loadTexts:
    pppLqrExtnsTable.setDescription('Table containing additional LQR information\n                         for the local PPP entity.')
pppLqrExtnsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 23, 1, 2, 3, 1)).setIndexNames((0,
                                                                                      'IF-MIB',
                                                                                      'ifIndex'))
if mibBuilder.loadTexts:
    pppLqrExtnsEntry.setDescription('Extended LQR information for a particular PPP\n                         link. Assuming that this group has been\n                         implemented, a PPP link will have an entry in\n                         this table if and only if LQR Quality\n                         Monitoring has been successfully negotiated for\n                         said link.')
pppLqrExtnsLastReceivedLqrPacket = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 23, 1, 2,
                                                   3, 1, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(68, 68)).setFixedLength(68)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pppLqrExtnsLastReceivedLqrPacket.setDescription("This object contains the most recently\n                         received LQR packet.  The format of the packet\n                         is as described in the LQM Protocol\n                         specificiation. All fields of the packet,\n                         including the `save' fields, are stored in this\n                         object.\n\n                         The LQR packet is stored in network byte order.\n                         The LAP-B and PPP headers are not stored in\n                         this object; the first four octets of this\n                         variable contain the Magic-Number field, the\n                         second four octets contain the LastOutLQRs\n                         field and so on. The last four octets of this\n                         object contain the SaveInOctets field of the\n                         LQR packet.")
pppEchoTest = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23, 1, 3, 1))
pppDiscardTest = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 23, 1, 3, 2))
mibBuilder.exportSymbols('PPP-LCP-MIB', pppLqrInGoodOctets=pppLqrInGoodOctets, pppLinkConfigReceiveACCMap=pppLinkConfigReceiveACCMap, pppLqrConfigPeriod=pppLqrConfigPeriod, ppp=ppp, pppLinkConfigMagicNumber=pppLinkConfigMagicNumber, pppLinkStatusRemoteToLocalACCompression=pppLinkStatusRemoteToLocalACCompression, pppLinkStatusPeerToLocalACCMap=pppLinkStatusPeerToLocalACCMap, pppLqrExtnsTable=pppLqrExtnsTable, pppLqrExtnsLastReceivedLqrPacket=pppLqrExtnsLastReceivedLqrPacket, pppLinkConfigTable=pppLinkConfigTable, pppLinkStatusEntry=pppLinkStatusEntry, pppLinkConfigInitialMRU=pppLinkConfigInitialMRU, pppLinkConfigFcsSize=pppLinkConfigFcsSize, pppLinkStatusRemoteMRU=pppLinkStatusRemoteMRU, pppLinkConfigEntry=pppLinkConfigEntry, pppLqrQuality=pppLqrQuality, pppLinkStatusLocalToRemoteACCompression=pppLinkStatusLocalToRemoteACCompression, pppLinkStatusBadAddresses=pppLinkStatusBadAddresses, pppLinkStatusTable=pppLinkStatusTable, pppLinkStatusLocalToPeerACCMap=pppLinkStatusLocalToPeerACCMap, pppDiscardTest=pppDiscardTest, pppLinkStatusReceiveFcsSize=pppLinkStatusReceiveFcsSize, pppLqr=pppLqr, pppLqrConfigStatus=pppLqrConfigStatus, pppLqrEntry=pppLqrEntry, pppLinkStatusPacketTooLongs=pppLinkStatusPacketTooLongs, pppLinkStatusLocalToRemoteProtocolCompression=pppLinkStatusLocalToRemoteProtocolCompression, pppLqrConfigEntry=pppLqrConfigEntry, pppLqrExtnsEntry=pppLqrExtnsEntry, pppLqrTable=pppLqrTable, pppLqrLocalPeriod=pppLqrLocalPeriod, pppLinkStatusRemoteToLocalProtocolCompression=pppLinkStatusRemoteToLocalProtocolCompression, pppLqrConfigTable=pppLqrConfigTable, pppLink=pppLink, pppTests=pppTests, pppLinkStatusBadFCSs=pppLinkStatusBadFCSs, pppEchoTest=pppEchoTest, pppLcp=pppLcp, pppLqrOutLQRs=pppLqrOutLQRs, pppLinkConfigTransmitACCMap=pppLinkConfigTransmitACCMap, pppLinkStatusLocalMRU=pppLinkStatusLocalMRU, pppLqrInLQRs=pppLqrInLQRs, pppLinkStatusTransmitFcsSize=pppLinkStatusTransmitFcsSize, pppLinkStatusBadControls=pppLinkStatusBadControls, pppLinkStatusPhysicalIndex=pppLinkStatusPhysicalIndex, pppLqrRemotePeriod=pppLqrRemotePeriod)