# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/APPN-MIB.py
# Compiled at: 2016-02-13 18:05:25
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ConstraintsUnion, SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection')
(IANAifType,) = mibBuilder.importSymbols('IANAifType-MIB', 'IANAifType')
(snanauMIB,) = mibBuilder.importSymbols('SNA-NAU-MIB', 'snanauMIB')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(Gauge32, TimeTicks, Unsigned32, Bits, Counter32, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, iso, NotificationType, ObjectIdentity, Integer32, MibIdentifier, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'TimeTicks', 'Unsigned32', 'Bits', 'Counter32', 'Counter64', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'IpAddress', 'iso', 'NotificationType', 'ObjectIdentity', 'Integer32', 'MibIdentifier', 'ModuleIdentity')
(DateAndTime, DisplayString, TimeStamp, VariablePointer, RowPointer, TruthValue, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DateAndTime', 'DisplayString', 'TimeStamp', 'VariablePointer', 'RowPointer', 'TruthValue', 'TextualConvention')
appnMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 34, 4)).setRevisions(('1998-07-15 18:00', '1998-05-26 18:00', '1997-07-31 18:00', '1997-03-31 18:00', '1997-03-20 12:00'))
if mibBuilder.loadTexts:
    appnMIB.setLastUpdated('9807151800Z')
if mibBuilder.loadTexts:
    appnMIB.setOrganization('IETF SNA NAU MIB WG / AIW APPN MIBs SIG')
if mibBuilder.loadTexts:
    appnMIB.setContactInfo('\n\n                        Bob Clouston\n                        Cisco Systems\n                        7025 Kit Creek Road\n                        P.O. Box 14987\n                        Research Triangle Park, NC 27709, USA\n                        Tel:    1 919 472 2333\n                        E-mail: clouston@cisco.com\n\n                        Bob Moore\n                        IBM Corporation\n                        4205 S. Miami Boulevard\n                        BRQA/501\n                        P.O. Box 12195\n                        Research Triangle Park, NC 27709, USA\n                        Tel:    1 919 254 4436\n                        E-mail: remoore@us.ibm.com\n\n                ')
if mibBuilder.loadTexts:
    appnMIB.setDescription('This is the MIB module for objects used to\n                 manage network devices with APPN capabilities.')

class SnaNodeIdentification(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(8, 8)
    fixedLength = 8


class SnaControlPointName(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(3, 17)


class SnaClassOfServiceName(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 8)


class SnaModeName(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 8)


class SnaSenseData(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(8, 8)
    fixedLength = 8


class DisplayableDlcAddress(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 64)


class AppnNodeCounter(Counter32, TextualConvention):
    __module__ = __name__


class AppnPortCounter(Counter32, TextualConvention):
    __module__ = __name__


class AppnLinkStationCounter(Counter32, TextualConvention):
    __module__ = __name__


class AppnTopologyEntryTimeLeft(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 15)


class AppnTgDlcData(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 64)


class AppnTgEffectiveCapacity(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(1, 1)
    fixedLength = 1


class AppnTgSecurity(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 32, 64, 96, 128, 160, 192))
    namedValues = NamedValues(('nonsecure', 1), ('publicSwitchedNetwork', 32), ('undergroundCable',
                                                                                64), ('secureConduit',
                                                                                      96), ('guardedConduit',
                                                                                            128), ('encrypted',
                                                                                                   160), ('guardedRadiation',
                                                                                                          192))


class AppnTgDelay(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(1, 1)
    fixedLength = 1


appnObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1))
appnNode = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1))
appnGeneralInfoAndCaps = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1))
appnNnUniqueInfoAndCaps = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2))
appnEnUniqueCaps = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 3))
appnPortInformation = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4))
appnLinkStationInformation = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5))
appnVrnInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 6))
appnNodeCpName = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 1), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeCpName.setDescription('Administratively assigned network name for this node.')
appnNodeId = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 3), SnaNodeIdentification()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeId.setDescription("This node's Node Identification, which it sends in bytes\n          2-5 of XID.")
appnNodeType = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 4))).clone(namedValues=NamedValues(('networkNode', 1), ('endNode', 2), ('t21len', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeType.setDescription('Type of APPN node:\n\n                networkNode(1) - APPN network node\n                endNode(2)     - APPN end node\n                t21len(4)      - LEN end node\n\n          Note:  A branch network node SHALL return endNode(2)\n          as the value of this object.  A management application\n\n          can distinguish between a branch network node and an\n          actual end node by retrieving the appnNodeBrNn object.')
appnNodeUpTime = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 5), TimeTicks()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeUpTime.setDescription('Amount of time (in hundredths of a second) since the APPN node\n          was last reinitialized.')
appnNodeParallelTg = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeParallelTg.setDescription('Indicates whether this node supports parallel TGs.')
appnNodeAdaptiveBindPacing = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeAdaptiveBindPacing.setDescription('Indicates whether this node supports adaptive bind pacing for\n          dependent LUs.')
appnNodeHprSupport = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noHprSupport', 1), ('hprBaseOnly', 2), ('rtpTower', 3), ('controlFlowsOverRtpTower', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprSupport.setDescription("Indicates this node's level of support for high-performance\n          routing (HPR):\n\n\n             noHprSupport(1)             - no HPR support\n             hprBaseOnly(2)              - HPR base (option set 1400)\n                                           supported\n             rtpTower(3)                 - HPR base and RTP tower\n                                           (option set 1401) supported\n             controlFlowsOverRtpTower(4) - HPR base, RTP tower, and\n                                           control flows over RTP\n                                           (option set 1402) supported\n\n          This object corresponds to cv4580, byte 9, bits 3-4.")
appnNodeMaxSessPerRtpConn = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 9), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeMaxSessPerRtpConn.setDescription('This object represents a configuration parameter indicating\n          the maximum number of sessions that the APPN node is to put on\n          any HPR connection.  The value is zero if not applicable.')
appnNodeHprIntRteSetups = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 10), AppnNodeCounter()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprIntRteSetups.setDescription('The total number of HPR route setups received for routes\n          passing through this node since the node was last\n          reinitialized.')
appnNodeHprIntRteRejects = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 11), AppnNodeCounter()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprIntRteRejects.setDescription('The number of HPR route setups rejected by this node for\n          routes passing through it since the node was last\n          reinitialized.')
appnNodeHprOrgRteSetups = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 12), AppnNodeCounter()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprOrgRteSetups.setDescription('The total number of HPR route setups sent for routes\n          originating in this node since the node was last\n          reinitialized.')
appnNodeHprOrgRteRejects = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 13), AppnNodeCounter()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprOrgRteRejects.setDescription('The number of HPR route setups rejected by other nodes for\n          routes originating in this node since the node was last\n          reinitialized.')
appnNodeHprEndRteSetups = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 14), AppnNodeCounter()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprEndRteSetups.setDescription('The total number of HPR route setups received for routes\n          ending in this node since the node was last reinitialized.')
appnNodeHprEndRteRejects = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 15), AppnNodeCounter()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeHprEndRteRejects.setDescription('The number of HPR route setups rejected by this node for\n          routes ending in it since the node was last reinitialized.')
appnNodeCounterDisconTime = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 16), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeCounterDisconTime.setDescription('The value of the sysUpTime object the last time the APPN node\n          was reinitialized.')
appnNodeLsCounterType = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 17), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('other', 1), ('noAnr', 2), ('anrForLocalNces', 3), ('allAnr', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeLsCounterType.setDescription('Indicates which ANR traffic, if any, the node includes in the\n          counts returned by the APPN link station counters\n          appnLsInXidBytes, appnLsInMsgBytes, appnLsInXidFrames,\n          appnLsInMsgFrames, appnLsOutXidBytes, appnLsOutMsgBytes,\n          appnLsOutXidFrames, and appnLsOutMsgFrames.  These counters\n          are always incremented for ISR traffic.\n\n          The following values are defined:\n\n             other(1)             - the node does something different\n                                    from all the options listed below\n             noAnr(2)             - the node does not include any ANR\n                                    traffic in these counts\n             anrForLocalNces(3)   - the node includes in these counts\n                                    ANR traffic for RTP connections\n                                    that terminate in this node, but\n                                    not ANR traffic for RTP connections\n                                    that pass through this node without\n                                    terminating in it\n             allAnr(4)            - the node includes all ANR traffic\n                                    in these counts.')
appnNodeBrNn = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 18), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeBrNn.setDescription('Indicates whether this node is currently configured as a\n          branch network node.\n\n          Note:  throughout the remainder of this MIB module, branch\n          network node is treated as a third node type, parallel to\n          network node and end node.  This is not how branch network\n          nodes are treated in the base APPN architecture, but it\n\n          increases clarity to do it here.')
appnNodeNnCentralDirectory = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 1), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnCentralDirectory.setDescription('Indicates whether this node supports central directory\n          services.\n\n          This object corresponds to cv4580, byte 8, bit 1.')
appnNodeNnTreeCache = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('noCache', 1), ('cacheNoIncrUpdate', 2), ('cacheWithIncrUpdate', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnTreeCache.setDescription("Indicates this node's level of support for caching of route\n          trees.  Three levels are specified:\n\n             noCache(1)             - caching of route trees is not\n                                      supported\n             cacheNoIncrUpdate(2)   - caching of route trees is\n                                      supported, but without incremental\n                                      updates\n             cacheWithIncrUpdate(3) - caching of route trees with\n                                      incremental updates is supported")
appnNodeNnRouteAddResist = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnRouteAddResist.setDescription('Route addition resistance.\n\n          This administratively assigned value indicates the relative\n          desirability of using this node for intermediate session\n          traffic.  The value, which can be any integer 0-255, is used\n          in route computation.  The lower the value, the more\n          desirable the node is for intermediate routing.\n\n          This object corresponds to cv4580, byte 6.')
appnNodeNnIsr = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 4), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnIsr.setDescription('Indicates whether the node supports intermediate session\n          routing.\n\n          This object corresponds to cv4580, byte 8, bit 2.')
appnNodeNnFrsn = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnFrsn.setDescription('The last flow-reduction sequence number (FRSN) sent by this\n          node in a topology update to an adjacent network node.')
appnNodeNnPeriBorderSup = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnPeriBorderSup.setDescription('Indicates whether this node has peripheral border node\n          support.\n\n          This object corresponds to cv4580, byte 9, bit 0.')
appnNodeNnInterchangeSup = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnInterchangeSup.setDescription('Indicates whether this node has interchange node support.\n\n          This object corresponds to cv4580, byte 9, bit 1.')
appnNodeNnExteBorderSup = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnExteBorderSup.setDescription('Indicates whether this node has extended border node support.\n\n          This object corresponds to cv4580, byte 9, bit 2.')
appnNodeNnSafeStoreFreq = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 32767))).setUnits('TDUs').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    appnNodeNnSafeStoreFreq.setDescription('The topology safe store frequency.\n\n          If this number is not zero, then the topology database is saved\n          each time the total number of topology database updates (TDUs)\n          received by this node increases by this number.  A value of\n          zero indicates that the topology database is not being saved.')
appnNodeNnRsn = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 10), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnRsn.setDescription('Resource sequence number for this node, which it assigns and\n          controls.\n\n          This object corresponds to the numeric value in cv4580, bytes\n          2-5.')
appnNodeNnCongested = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 11), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnCongested.setDescription('Indicates whether this node is congested.  Other network nodes\n          stop routing traffic to this node while this flag is on.\n\n          This object corresponds to cv4580, byte 7, bit 0.')
appnNodeNnIsrDepleted = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 12), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnIsrDepleted.setDescription('Indicate whether intermediated session routing resources are\n          depleted.  Other network nodes stop routing traffic through\n          this node while this flag is on.\n\n          This object corresponds to cv4580, byte 7, bit 1.')
appnNodeNnQuiescing = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 13), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnQuiescing.setDescription('Indicates whether the node is quiescing.\n\n          This object corresponds to cv4580, byte 7, bit 5.')
appnNodeNnGateway = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 2, 14), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeNnGateway.setDescription('Indicates whether the node has gateway services support.\n\n          This object corresponds to cv4580, byte 8, bit 0.')
appnNodeEnModeCosMap = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 3, 1), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeEnModeCosMap.setDescription('Indicates whether this end node supports mode name to COS name\n          mapping.')
appnNodeEnNnServer = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 3, 2), OctetString().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(3, 17)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeEnNnServer.setDescription('The fully qualified name of the current NN server for this end\n          node.  An NN server is identified using the format specified in\n          the SnaControlPointName textual convention.  The value is a\n          zero-length string when there is no active NN server.\n\n          A branch network node shall also implement this object.')
appnNodeEnLuSearch = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 3, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeEnLuSearch.setDescription('Indicates whether the node is to be searched for LUs as part\n          of a network broadcast search.\n\n          A branch network node shall also implement this object.')
appnPortTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1))
if mibBuilder.loadTexts:
    appnPortTable.setDescription("The Port table describes the configuration and current status\n          of the ports used by APPN.  When it is known to the APPN\n          component, an OBJECT IDENTIFIER pointing to additional\n          information related to the port is included.  This may, but\n          need not, be a RowPointer to an ifTable entry for a DLC\n          interface immediately 'below' the port.")
appnPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1)).setIndexNames((0, 'APPN-MIB', 'appnPortName'))
if mibBuilder.loadTexts:
    appnPortEntry.setDescription('The port name is used as the index to this table.')
appnPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10)))
if mibBuilder.loadTexts:
    appnPortName.setDescription('Administratively assigned name for this APPN port.')
appnPortCommand = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('deactivate', 1), ('activate', 2), ('recycle', 3), ('ready', 4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    appnPortCommand.setDescription('Object by which a Management Station can activate, deactivate,\n          or recycle (i.e., cause to be deactivated and then immediately\n          activated) a port, by setting the value to activate(1),\n          deactivate(2), or recycle(3), respectively.  The value ready(4)\n          is returned on GET operations until a SET has been processed;\n          after that the value received on the most recent SET is\n          returned.')
appnPortOperState = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('inactive', 1), ('pendactive', 2), ('active', 3), ('pendinact', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortOperState.setDescription('Indicates the current state of this port:\n\n              inactive(1)   - port is inactive\n              pendactive(2) - port is pending active\n              active(3)     - port is active\n              pendinact(4)  - port is pending inactive')
appnPortDlcType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 4), IANAifType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDlcType.setDescription("The type of DLC interface, distinguished according to the\n          protocol immediately 'below' this layer.")
appnPortPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('leased', 1), ('switched', 2), ('sharedAccessFacilities', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortPortType.setDescription('Identifies the type of line used by this port:\n\n              leased(1)                 - leased line\n              switched(2)               - switched line\n              sharedAccessFacilities(3) - shared access facility, such\n                                          as a LAN.')
appnPortSIMRIM = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortSIMRIM.setDescription('Indicates whether Set Initialization Mode (SIM) and Receive\n          Initialization Mode (RIM) are supported for this port.')
appnPortLsRole = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('primary', 1), ('secondary', 2), ('negotiable', 3), ('abm', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortLsRole.setDescription("Initial role for link stations activated through this port.\n             The values map to the following settings in the initial XID,\n             where 'ABM' indicates asynchronous balanced mode and 'NRM'\n             indicated normal response mode:\n\n                 primary(1):     ABM support = 0     ( = NRM)\n                                 role = 01           ( = primary)\n                 secondary(2):   ABM support = 0     ( = NRM)\n                                 role = 00           ( = secondary)\n                 negotiable(3):  ABM support = 0     ( = NRM)\n                                 role = 11           ( = negotiable)\n                 abm(4):         ABM support = 1     ( = ABM)\n                                 role = 11           ( = negotiable)")
appnPortNegotLs = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortNegotLs.setDescription('Indicates whether the node supports negotiable link stations\n          for this port.')
appnPortDynamicLinkSupport = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 9), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDynamicLinkSupport.setDescription('Indicates whether this node allows call-in on this port from\n          nodes not defined locally.')
appnPortMaxRcvBtuSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(99, 32767))).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortMaxRcvBtuSize.setDescription('Maximum Basic Transmission Unit (BTU) size that a link station\n          on this port can receive.\n\n          This object corresponds to bytes 21-22 of XID3.')
appnPortMaxIframeWindow = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 11), Gauge32()).setUnits('I-frames').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortMaxIframeWindow.setDescription('Maximum number of I-frames that can be received by the XID\n          sender before an acknowledgement is received.')
appnPortDefLsGoodXids = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 12), AppnPortCounter()).setUnits('XID exchanges').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDefLsGoodXids.setDescription('The total number of successful XID exchanges that have\n          occurred on all defined link stations on this port since the\n          last time this port was started.')
appnPortDefLsBadXids = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 13), AppnPortCounter()).setUnits('XID exchanges').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDefLsBadXids.setDescription('The total number of unsuccessful XID exchanges that have\n          occurred on all defined link stations on this port since the\n          last time this port was started.')
appnPortDynLsGoodXids = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 14), AppnPortCounter()).setUnits('XID exchanges').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDynLsGoodXids.setDescription('The total number of successful XID exchanges that have\n          occurred on all dynamic link stations on this port since the\n          last time this port was started.')
appnPortDynLsBadXids = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 15), AppnPortCounter()).setUnits('XID exchanges').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDynLsBadXids.setDescription('The total number of unsuccessful XID exchanges that have\n          occurred on all dynamic link stations on this port since the\n          last time this port was started.')
appnPortSpecific = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 16), RowPointer()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortSpecific.setDescription('Identifies the object, e.g., one in a DLC-specific MIB, that\n          can provide additional information related to this port.\n\n          If the agent is unable to identify such an object, the value\n          0.0 is returned.')
appnPortDlcLocalAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 17), DisplayableDlcAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortDlcLocalAddr.setDescription('Local DLC address of this port.')
appnPortCounterDisconTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 4, 1, 1, 18), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnPortCounterDisconTime.setDescription('The value of the sysUpTime object the last time the port was\n          started.')
appnLsTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1))
if mibBuilder.loadTexts:
    appnLsTable.setDescription('This table contains detailed information about the link\n          station configuration and its current status.')
appnLsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1)).setIndexNames((0, 'APPN-MIB', 'appnLsName'))
if mibBuilder.loadTexts:
    appnLsEntry.setDescription('This table is indexed by the link station name.')
appnLsName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10)))
if mibBuilder.loadTexts:
    appnLsName.setDescription('Administratively assigned name for the link station.\n           The name can be from one to ten characters.')
appnLsCommand = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('deactivate', 1), ('activate', 2), ('recycle', 3), ('ready', 4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    appnLsCommand.setDescription('Object by which a Management Station can activate, deactivate,\n          or recycle (i.e., cause to be deactivated and then immediately\n          reactivated) a link station, by setting the value to\n          activate(1), deactivate(2), or recycle(3), respectively.  The\n          value ready(4) is returned on GET operations until a SET has\n          been processed; after that the value received on the most\n          recent SET is returned.')
appnLsOperState = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))).clone(namedValues=NamedValues(('inactive', 1), ('sentConnectOut', 2), ('pendXidExch', 3), ('sendActAs', 4), ('sendSetMode', 5), ('otherPendingActive', 6), ('active', 7), ('sentDeactAsOrd', 8), ('sentDiscOrd', 9), ('sentDiscImmed', 10), ('otherPendingInact', 11)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsOperState.setDescription("State of this link station.  The comments map these more\n          granular states to the 'traditional' four states for SNA\n          resources.  Values (2) through (5) represent the normal\n          progression of states when a link station is being activated.\n          Value (6) represents some other state of a link station in\n          the process of being activated.  Values (8) through (10)\n          represent different ways a link station can be deactivated.\n          Value (11) represents some other state of a link station in\n          the process of being deactivated.")
appnLsPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsPortName.setDescription('Administratively assigned name for the port associated with\n\n          this link station.  The name can be from one to ten\n          characters.')
appnLsDlcType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 5), IANAifType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsDlcType.setDescription("The type of DLC interface, distinguished according to the\n          protocol immediately 'below' this layer.")
appnLsDynamic = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsDynamic.setDescription('Identifies whether this is a dynamic link station.  Dynamic\n          link stations are created when links that have not been locally\n          defined are established by adjacent nodes.')
appnLsAdjCpName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 7), OctetString().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(3, 17)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsAdjCpName.setDescription("Fully qualified name of the adjacent node for this link\n          station.  An adjacent node is identified using the format\n          specified in the SnaControlPointName textual convention.\n\n          The value of this object is determined as follows:\n\n             1. If the adjacent node's name was received on XID, it\n                is returned.\n\n             2. If the adjacent node's name was not received on XID,\n                but a locally-defined value is available, it is\n                returned.\n\n             3. Otherwise a string of length 0 is returned, indicating\n                that no name is known for the adjacent node.")
appnLsAdjNodeType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 4, 255))).clone(namedValues=NamedValues(('networkNode', 1), ('endNode', 2), ('t21len', 4), ('unknown', 255)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsAdjNodeType.setDescription('Node type of the adjacent node on this link:\n\n                networkNode(1) - APPN network node\n                endNode(2)     - APPN end node\n                t21len(4)      - LEN end node\n                unknown(255)   - the agent does not know the node type\n                                 of the adjacent node\n          ')
appnLsTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 256))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsTgNum.setDescription('Number associated with the TG to this link station, with a\n          range from 0 to 256.  A value of 256 indicates that the TG\n          number has not been negotiated and is unknown at this time.')
appnLsLimResource = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 10), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsLimResource.setDescription('Indicates whether the link station is a limited resource.  A\n          link station that is a limited resource is deactivated when it\n          is no longer in use.')
appnLsActOnDemand = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 11), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsActOnDemand.setDescription('Indicates whether the link station is activatable on demand.\n\n          Such a link station is reported in the topology as active\n          regardless of its actual state, so that it can be considered in\n          route calculations.  If the link station is inactive and is\n          chosen for a route, it will be activated at that time.')
appnLsMigration = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 12), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsMigration.setDescription("Indicates whether this link station will be used for\n          connections to down-level or migration partners.\n\n          In general, migration nodes do not append their CP names on\n          XID3.  Such nodes:  (1) will not support parallel TGs, (2)\n          should be sent an ACTIVATE PHYSICAL UNIT (ACTPU), provided that\n          the partner supports ACTPUs, and (3) should not be sent\n          segmented BINDs.  However, if this node receives an XID3 with\n          an appended CP name, then the partner node will not be treated\n          as a migration node.\n\n           In the case of DYNAMIC TGs this object should be set to 'no'.")
appnLsPartnerNodeId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 13), SnaNodeIdentification()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsPartnerNodeId.setDescription("The partner's Node Identification, from bytes 2-5 of the XID\n          received from the partner.  If this value is not available,\n          then the characters '00000000' are returned.")
appnLsCpCpSessionSupport = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 14), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsCpCpSessionSupport.setDescription("Indicates whether CP-CP sessions are supported by this\n          link station.  For a dynamic link, this object represents\n          the default ('Admin') value.")
appnLsMaxSendBtuSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(99, 32767))).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsMaxSendBtuSize.setDescription("Numeric value between 99 and 32767 inclusive indicating the\n          maximum number of bytes in a Basic Transmission Unit (BTU) sent\n          on this link.\n\n          When the link state (returned by the appnLsOperState object) is\n          inactive or pending active, the value configured at this node\n          is returned.  When the link state is active, the value that was\n          negotiated for it is returned.  This negotiated value is the\n          smaller of the value configured at this node and the partner's\n          maximum receive BTU length, received in XID.")
appnLsInXidBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 16), AppnLinkStationCounter()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsInXidBytes.setDescription('Number of XID bytes received.  All of the bytes in the SNA\n          basic transmission unit (BTU), i.e., all of the bytes in the\n          DLC XID Information Field, are counted.')
appnLsInMsgBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 17), AppnLinkStationCounter()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsInMsgBytes.setDescription('Number of message (I-frame) bytes received.  All of the bytes\n          in the SNA basic transmission unit (BTU), including the\n          transmission header (TH), are counted.')
appnLsInXidFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 18), AppnLinkStationCounter()).setUnits('XID frames').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsInXidFrames.setDescription('Number of XID frames received.')
appnLsInMsgFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 19), AppnLinkStationCounter()).setUnits('I-frames').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsInMsgFrames.setDescription('Number of message (I-frame) frames received.')
appnLsOutXidBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 20), AppnLinkStationCounter()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsOutXidBytes.setDescription('Number of XID bytes sent.  All of the bytes in the SNA basic\n          transmission unit (BTU), i.e., all of the bytes in the DLC XID\n          Information Field, are counted.')
appnLsOutMsgBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 21), AppnLinkStationCounter()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsOutMsgBytes.setDescription('Number of message (I-frame) bytes sent.  All of the bytes\n          in the SNA basic transmission unit (BTU), including the\n          transmission header (TH), are counted.')
appnLsOutXidFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 22), AppnLinkStationCounter()).setUnits('XID frames').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsOutXidFrames.setDescription('Number of XID frames sent.')
appnLsOutMsgFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 23), AppnLinkStationCounter()).setUnits('I-frames').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsOutMsgFrames.setDescription('Number of message (I-frame) frames sent.')
appnLsEchoRsps = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 24), AppnLinkStationCounter()).setUnits('echo responses').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsEchoRsps.setDescription('Number of echo responses returned from adjacent link station.\n          A response should be returned for each test frame sent by this\n          node.  Test frames are sent to adjacent nodes periodically to\n          verify connectivity and to measure the actual round trip time,\n          that is, the time interval from when the test frame is sent\n          until when the response is received.')
appnLsCurrentDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 25), Gauge32()).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsCurrentDelay.setDescription('The time that it took for the last test signal to be sent and\n          returned from this link station to the adjacent link station.\n          This time is represented in milliseconds.')
appnLsMaxDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 26), Gauge32()).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsMaxDelay.setDescription('The longest time it took for a test signal to be sent and\n          returned from this link station to the adjacent link station.\n\n          This time is represented in milliseconds .\n\n          The value 0 is returned if no test signal has been sent and\n          returned.')
appnLsMinDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 27), Gauge32()).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsMinDelay.setDescription('The shortest time it took for a test signal to be sent and\n          returned from this link station to the adjacent link station.\n          This time is represented in milliseconds.\n\n          The value 0 is returned if no test signal has been sent and\n          returned.')
appnLsMaxDelayTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 28), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsMaxDelayTime.setDescription('The time when the longest delay occurred.  This time can be\n          used to identify when this high water mark occurred in relation\n          to other events in the APPN node, for example, the time at\n          which an APPC session was either terminated or failed to be\n          established.  This latter time is available in the\n          appcHistSessTime object in the APPC MIB.\n\n          The value 00000000 is returned if no test signal has been sent\n          and returned.')
appnLsGoodXids = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 29), AppnLinkStationCounter()).setUnits('XID exchanges').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsGoodXids.setDescription('The total number of successful XID exchanges that have\n          occurred on this link station since the time it was started.')
appnLsBadXids = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 30), AppnLinkStationCounter()).setUnits('XID exchanges').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsBadXids.setDescription('The total number of unsuccessful XID exchanges that have\n          occurred on this link station since the time it was started.')
appnLsSpecific = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 31), RowPointer()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsSpecific.setDescription('Identifies the object, e.g., one in a DLC-specific MIB, that\n          can provide additional information related to this link\n          station.\n\n          If the agent is unable to identify such an object, the value\n          0.0 is returned.')
appnLsActiveTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 32), Unsigned32()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsActiveTime.setDescription('The cumulative amount of time since the node was last\n          reinitialized, measured in hundredths of a second, that this\n          link station has been in the active state.  A zero value\n          indicates that the link station has never been active since\n          the node was last reinitialized.')
appnLsCurrentStateTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 33), TimeTicks()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsCurrentStateTime.setDescription('The amount of time, measured in hundredths of a second, that\n\n          the link station has been in its current state.')
appnLsHprSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 34), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noHprSupport', 1), ('hprBaseOnly', 2), ('rtpTower', 3), ('controlFlowsOverRtpTower', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsHprSup.setDescription('Indicates the level of high performance routing (HPR) support\n          over this link:\n\n             noHprSupport(1)             - no HPR support\n             hprBaseOnly(2)              - HPR base (option set 1400)\n                                           supported\n             rtpTower(3)                 - HPR base and RTP tower\n                                           (option set 1401) supported\n             controlFlowsOverRtpTower(4) - HPR base, RTP tower, and\n                                           control flows over RTP\n                                           (option set 1402) supported\n\n          If the link is not active, the defined value is returned.')
appnLsErrRecoSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 35), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsErrRecoSup.setDescription('Indicates whether the link station is supporting\n           HPR link-level error recovery.')
appnLsForAnrLabel = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 36), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsForAnrLabel.setDescription('The forward Automatic Network Routing (ANR) label for this\n          link station.  If the link does not support HPR or the value is\n          unknown, a zero-length string is returned.')
appnLsRevAnrLabel = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 37), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsRevAnrLabel.setDescription('The reverse Automatic Network Routing (ANR) label for this\n          link station.  If the link does not support HPR or the value is\n          unknown, a zero-length string is returned.')
appnLsCpCpNceId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 38), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsCpCpNceId.setDescription('The network connection endpoint identifier (NCE ID) for CP-CP\n          sessions if this node supports the HPR transport tower, a\n          zero-length string if the value is unknown or not meaningful\n          for this node.')
appnLsRouteNceId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 39), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsRouteNceId.setDescription('The network connection endpoint identifier (NCE ID) for Route\n          Setup if this node supports the HPR transport tower, a zero-\n          length string if the value is unknown or not meaningful for\n          this node.')
appnLsBfNceId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 40), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsBfNceId.setDescription('The network connection endpoint identifier (NCE ID) for the\n          APPN/HPR boundary function if this node supports the HPR\n          transport tower, a zero-length string if the value is unknown\n          or not meaningful for this node.')
appnLsLocalAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 41), DisplayableDlcAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsLocalAddr.setDescription('Local address of this link station.')
appnLsRemoteAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 42), DisplayableDlcAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsRemoteAddr.setDescription('Address of the remote link station on this link.')
appnLsRemoteLsName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 43), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 10))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsRemoteLsName.setDescription('Remote link station discovered from the XID exchange.\n          The name can be from one to ten characters.  A zero-length\n          string indicates that the value is not known.')
appnLsCounterDisconTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 44), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsCounterDisconTime.setDescription('The value of the sysUpTime object the last time the link\n          station was started.')
appnLsMltgMember = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 1, 1, 45), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsMltgMember.setDescription("Indicates whether the link is a member of a multi-link TG.  If\n          the link's TG has been brought up as a multi-link TG, then the\n          link is reported as a member of a multi-link TG, even if it is\n\n          currently the only active link in the TG.")
appnLsStatusTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2))
if mibBuilder.loadTexts:
    appnLsStatusTable.setDescription('This table contains information related to exceptional and\n          potentially exceptional conditions that occurred during the\n          activation, XID exchange, and termination of a connection.  No\n          entries are created when these activities proceed normally.\n\n          It is an implementation option when entries are removed from\n          this table.')
appnLsStatusEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1)).setIndexNames((0, 'APPN-MIB', 'appnLsStatusIndex'))
if mibBuilder.loadTexts:
    appnLsStatusEntry.setDescription('This table is indexed by the LsStatusIndex, which is an\n          integer that is continuously updated until it eventually\n          wraps.')
appnLsStatusIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647)))
if mibBuilder.loadTexts:
    appnLsStatusIndex.setDescription('Table index.  The value of the index begins at zero\n           and is incremented up to a maximum value of 2**31-1\n           (2,147,483,647) before wrapping.')
appnLsStatusTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 2), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusTime.setDescription('Time when the exception condition occurred.  This time can be\n          used to identify when this event occurred in relation to other\n          events in the APPN node, for example, the time at which an APPC\n          session was either terminated or failed to be established.\n          This latter time is available in the appcHistSessTime object in\n          the APPC MIB.')
appnLsStatusLsName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusLsName.setDescription('Administratively assigned name for the link station\n          experiencing the condition.')
appnLsStatusCpName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 4), DisplayString().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(3, 17)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusCpName.setDescription("Fully qualified name of the adjacent node for this link\n          station.  An adjacent node is identified using the format\n          specified in the SnaControlPointName textual convention.\n\n          The value of this object is determined as follows:\n\n             1. If the adjacent node's name was received on XID, it\n                is returned.\n\n             2. If the adjacent node's name was not received on XID,\n                but a locally-defined value is available, it is\n                returned.\n\n             3. Otherwise a string of length 0 is returned, indicating\n                that no name is known for the adjacent node.")
appnLsStatusPartnerId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 5), SnaNodeIdentification()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusPartnerId.setDescription("The partner's Node Identification, from bytes 2-5 of the XID\n          received from the partner.  If this value is not available,\n          then the characters '00000000' are returned.")
appnLsStatusTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 256))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusTgNum.setDescription('Number associated with the TG to this link station, with a\n          range from 0 to 256.  A value of 256 indicates that the TG\n          number was unknown at the time of the failure.')
appnLsStatusGeneralSense = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 7), SnaSenseData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusGeneralSense.setDescription('The error sense data associated with the start sequence of\n          activation of a link up to the beginning of the XID sequence.\n\n          This is the sense data that came from Configuration Services\n          whenever the link did not activate or when it went inactive.')
appnLsStatusRetry = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusRetry.setDescription('Indicates whether the node will retry the start request to\n          activate the link.')
appnLsStatusEndSense = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 9), SnaSenseData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusEndSense.setDescription('The sense data associated with the termination of the link\n          connection to adjacent node.\n\n          This is the sense data that came from the DLC layer.')
appnLsStatusXidLocalSense = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 10), SnaSenseData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusXidLocalSense.setDescription('The sense data associated with the rejection of the XID.\n\n          This is the sense data that came from the local node (this\n          node) when it built the XID Negotiation Error control vector\n          (cv22) to send to the remote node.')
appnLsStatusXidRemoteSense = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 11), SnaSenseData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusXidRemoteSense.setDescription('The sense data the adjacent node returned to this node\n          indicating the reason the XID was rejected.\n\n          This is the sense data that came from the remote node in the\n          XID Negotiation Error control vector (cv22) it sent to the\n          local node (this node).')
appnLsStatusXidByteInError = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65536))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusXidByteInError.setDescription("This object identifies the actual byte in the XID that caused\n          the error.  The value 65536 indicates that the object has no\n          meaning.\n\n          For values in the range 0-65535, this object corresponds to\n          bytes 2-3 of the XID Negotiation (X'22') control vector.")
appnLsStatusXidBitInError = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusXidBitInError.setDescription("This object identifies the actual bit in error (0 through 7)\n          within the errored byte of the XID.  The value 8 indicates that\n          this object has no meaning.\n\n          For values in the range 0-7, this object corresponds to byte 4\n          of the XID Negotiation (X'22') control vector.")
appnLsStatusDlcType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 14), IANAifType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusDlcType.setDescription("The type of DLC interface, distinguished according to the\n          protocol immediately 'below' this layer.")
appnLsStatusLocalAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 15), DisplayableDlcAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusLocalAddr.setDescription('Local address of this link station.')
appnLsStatusRemoteAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 5, 2, 1, 16), DisplayableDlcAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLsStatusRemoteAddr.setDescription('Address of the remote link station on this link.')
appnVrnTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 6, 1))
if mibBuilder.loadTexts:
    appnVrnTable.setDescription('This table relates a virtual routing node to an APPN port.')
appnVrnEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 6, 1, 1)).setIndexNames((0, 'APPN-MIB', 'appnVrnName'), (0, 'APPN-MIB', 'appnVrnTgNum'), (0, 'APPN-MIB', 'appnVrnPortName'))
if mibBuilder.loadTexts:
    appnVrnEntry.setDescription('This table is indexed by the virtual routing node name, TG\n          number, and port name.  There will be a matching entry in the\n          appnLocalTgTable to represent status and characteristics of the\n          TG representing each virtual routing node definition.')
appnVrnName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 6, 1, 1, 1), SnaControlPointName())
if mibBuilder.loadTexts:
    appnVrnName.setDescription('Administratively assigned name of the virtual routing node.\n          This is a fully qualified name, and matches the appnLocalTgDest\n          name in the appnLocalTgTable.')
appnVrnTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 6, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts:
    appnVrnTgNum.setDescription('Number associated with the transmission group representing\n          this virtual routing node definition.')
appnVrnPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 6, 1, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnVrnPortName.setDescription('The name of the port this virtual routing node definition is\n          defined to.')
appnNn = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 2))
appnNnTopo = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 1))
appnNnTopology = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2))
appnNnTopoMaxNodes = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 1, 1), Gauge32()).setUnits('node entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTopoMaxNodes.setDescription('Maximum number of node entries allowed in the APPN topology\n\n          database.  It is an implementation choice whether to count only\n          network-node entries, or to count all node entries.  If the\n          number of node entries exceeds this value, APPN will issue an\n          Alert and the node can no longer participate as a network node.\n          The value 0 indicates that the local node has no defined limit,\n          and the number of node entries is bounded only by memory.')
appnNnTopoCurNumNodes = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 1, 2), Gauge32()).setUnits('node entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTopoCurNumNodes.setDescription("Current number of node entries in this node's topology\n          database.  It is an implementation choice whether to count only\n          network-node entries, or to count all node entries, but an\n          implementation must make the same choice here that it makes for\n          the appnNnTopoMaxNodes object.  If this value exceeds the\n          maximum number of nodes allowed (appnNnTopoMaxNodes, if that\n          field in not 0), APPN Alert CPDB002 is issued.")
appnNnTopoNodePurges = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 1, 3), AppnNodeCounter()).setUnits('node entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTopoNodePurges.setDescription("Total number of topology node records purged from this node's\n          topology database since the node was last reinitialized.")
appnNnTopoTgPurges = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 1, 4), AppnNodeCounter()).setUnits('TG entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTopoTgPurges.setDescription("Total number of topology TG records purged from this node's\n          topology database since the node was last reinitialized.")
appnNnTopoTotalTduWars = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 1, 5), AppnNodeCounter()).setUnits('TDU wars').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTopoTotalTduWars.setDescription('Number of TDU wars detected by this node since its last\n          initialization.')
appnNnTopologyFRTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3))
if mibBuilder.loadTexts:
    appnNnTopologyFRTable.setDescription('Portion of the APPN topology database that describes all of\n          the APPN network nodes and virtual routing nodes known to this\n          node.')
appnNnTopologyFREntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1)).setIndexNames((0, 'APPN-MIB', 'appnNnNodeFRFrsn'), (0, 'APPN-MIB', 'appnNnNodeFRName'))
if mibBuilder.loadTexts:
    appnNnTopologyFREntry.setDescription('The FRSN and the fully qualified node name are used to index\n          this table.')
appnNnNodeFRFrsn = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 1), Unsigned32())
if mibBuilder.loadTexts:
    appnNnNodeFRFrsn.setDescription('Flow reduction sequence numbers (FRSNs) are associated with\n          Topology Database Updates (TDUs) and are unique only within\n          each APPN network node.  A TDU can be associated with multiple\n          APPN resources.  This FRSN indicates the last relative time\n          this resource was updated at the agent node.')
appnNnNodeFRName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 2), SnaControlPointName())
if mibBuilder.loadTexts:
    appnNnNodeFRName.setDescription('Administratively assigned network name that is locally defined\n          at each network node.')
appnNnNodeFREntryTimeLeft = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 3), AppnTopologyEntryTimeLeft()).setUnits('days').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFREntryTimeLeft.setDescription('Number of days before deletion of this network node entry.')
appnNnNodeFRType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 3))).clone(namedValues=NamedValues(('networkNode', 1), ('virtualRoutingNode', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRType.setDescription('Type of APPN node.')
appnNnNodeFRRsn = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRRsn.setDescription('Resource sequence number, which is assigned and controlled by\n          the network node that owns this resource.  An odd number\n          indicates that information about the resource is inconsistent.\n\n          This object corresponds to the numeric value in cv4580, bytes\n          2-5.')
appnNnNodeFRRouteAddResist = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRRouteAddResist.setDescription('Route addition resistance.\n\n          This administratively assigned value indicates the relative\n          desirability of using this node for intermediate session\n          traffic.  The value, which can be any integer 0-255, is used\n          in route computation.  The lower the value, the more\n          desirable the node is for intermediate routing.\n\n          This object corresponds to cv4580, byte 6.')
appnNnNodeFRCongested = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRCongested.setDescription('Indicates whether this node is congested.  This node is not be\n          included in route selection by other nodes when this congestion\n          exists.\n\n          This object corresponds to cv4580, byte 7, bit 0.')
appnNnNodeFRIsrDepleted = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRIsrDepleted.setDescription('Indicates whether intermediate session routing resources are\n          depleted.  This node is not included in intermediate route\n          selection by other nodes when resources are depleted.\n\n          This object corresponds to cv4580, byte 7, bit 1.')
appnNnNodeFRQuiescing = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 9), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRQuiescing.setDescription('Indicates whether the node is quiescing.  This node is not\n          included in route selection by other nodes when the node is\n          quiescing.\n\n          This object corresponds to cv4580, byte 7, bit 5.')
appnNnNodeFRGateway = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 10), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRGateway.setDescription('Indicates whether the node provide gateway services.\n\n          This object corresponds to cv4580, byte 8, bit 0.')
appnNnNodeFRCentralDirectory = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 11), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRCentralDirectory.setDescription('Indicates whether the node supports central directory\n          services.\n\n          This object corresponds to cv4580, byte 8, bit 1.')
appnNnNodeFRIsr = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 12), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRIsr.setDescription('Indicates whether the node supports intermediate session\n          routing (ISR).\n\n          This object corresponds to cv4580, byte 8, bit 2.')
appnNnNodeFRGarbageCollect = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 13), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRGarbageCollect.setDescription('Indicates whether the node has been marked for garbage\n          collection (deletion from the topology database) upon the next\n          garbage collection cycle.\n\n          This object corresponds to cv4580, byte 7, bit 3.')
appnNnNodeFRHprSupport = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noHprSupport', 1), ('hprBaseOnly', 2), ('rtpTower', 3), ('controlFlowsOverRtpTower', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRHprSupport.setDescription("Indicates the node's level of support for high-performance\n          routing (HPR):\n\n             noHprSupport(1)             - no HPR support\n             hprBaseOnly(2)              - HPR base (option set 1400)\n                                           supported\n             rtpTower(3)                 - HPR base and RTP tower\n                                           (option set 1401) supported\n             controlFlowsOverRtpTower(4) - HPR base, RTP tower, and\n                                           control flows over RTP\n                                           (option set 1402) supported\n\n          This object corresponds to cv4580, byte 9, bits 3-4.")
appnNnNodeFRPeriBorderSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 15), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRPeriBorderSup.setDescription('Indicates whether this node has peripheral border node\n          support.\n\n          This object corresponds to cv4580, byte 9, bit 0.')
appnNnNodeFRInterchangeSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 16), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRInterchangeSup.setDescription('Indicates whether this node has interchange node support.\n\n          This object corresponds to cv4580, byte 9, bit 1.')
appnNnNodeFRExteBorderSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 17), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRExteBorderSup.setDescription('Indicates whether this node has extended border node\n           support.\n\n          This object corresponds to cv4580, byte 9, bit 2.')
appnNnNodeFRBranchAwareness = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 3, 1, 18), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnNodeFRBranchAwareness.setDescription('Indicates whether this node supports branch awareness.\n\n          This object corresponds to cv4580, byte 8, bit 4.')
appnNnTgTopologyFRTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4))
if mibBuilder.loadTexts:
    appnNnTgTopologyFRTable.setDescription('Portion of the APPN topology database that describes all of\n          the APPN transmissions groups between nodes in the database.')
appnNnTgTopologyFREntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1)).setIndexNames((0, 'APPN-MIB', 'appnNnTgFRFrsn'), (0, 'APPN-MIB', 'appnNnTgFROwner'), (0, 'APPN-MIB', 'appnNnTgFRDest'), (0, 'APPN-MIB', 'appnNnTgFRNum'))
if mibBuilder.loadTexts:
    appnNnTgTopologyFREntry.setDescription('This table is indexed by four columns:  FRSN, TG owner fully\n          qualified node name, TG destination fully qualified node name,\n          and TG number.')
appnNnTgFRFrsn = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 1), Unsigned32())
if mibBuilder.loadTexts:
    appnNnTgFRFrsn.setDescription('Flow reduction sequence numbers (FRSNs) are associated with\n          Topology Database Updates (TDUs) and are unique only within\n          each APPN network node.  A TDU can be associated with multiple\n          APPN resources.  This FRSN indicates the last time this\n          resource was updated at this node.')
appnNnTgFROwner = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 2), SnaControlPointName())
if mibBuilder.loadTexts:
    appnNnTgFROwner.setDescription('Administratively assigned name for the originating node for\n          this TG.  This is the same name specified in the node table.')
appnNnTgFRDest = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 3), SnaControlPointName())
if mibBuilder.loadTexts:
    appnNnTgFRDest.setDescription('Administratively assigned fully qualified network name for the\n          destination node for this TG.')
appnNnTgFRNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts:
    appnNnTgFRNum.setDescription('Number associated with this transmission group.  Range is\n          0-255.')
appnNnTgFREntryTimeLeft = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 5), AppnTopologyEntryTimeLeft()).setUnits('days').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFREntryTimeLeft.setDescription('Number of days before deletion of this network node TG entry\n          if it is not operational or has an odd (inconsistent) RSN.')
appnNnTgFRDestVirtual = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRDestVirtual.setDescription('Indicates whether the destination node is a virtual routing\n          node.')
appnNnTgFRDlcData = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 7), AppnTgDlcData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRDlcData.setDescription('DLC-specific data related to a link connection network.')
appnNnTgFRRsn = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 8), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRRsn.setDescription("Current owning node's resource sequence number for this\n          resource.  An odd number indicates that information about the\n          resource is inconsistent.\n\n          This object corresponds to the numeric value in cv47, bytes\n          2-5")
appnNnTgFROperational = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 9), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFROperational.setDescription('Indicates whether the transmission group is operational.\n\n          This object corresponds to cv47, byte 6, bit 0.')
appnNnTgFRQuiescing = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 10), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRQuiescing.setDescription("Indicates whether the transmission group is quiescing.\n\n          If the TG owner is either an extended border node or a\n          branch-aware network node (indicated, respectively, by\n          the appnNnNodeFRExteBorderSup and appnNnNodeFRBranchAwareness\n          objects in the corresponding appnNnTopologyFREntry), then\n          this indicator is artificially set to TRUE in the APPN\n\n          topology database, to remove the TG from other nodes'\n          route calculations.  A management application can\n          determine whether the TG is actually quiescing by\n          examining its appnLocalTgQuiescing object at the TG owner.\n\n          This object corresponds to cv47, byte 6, bit 2.")
appnNnTgFRCpCpSession = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('supportedUnknownStatus', 1), ('supportedActive', 2), ('notSupported', 3), ('supportedNotActive', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRCpCpSession.setDescription("Indicates whether CP-CP sessions are supported on this TG, and\n          whether the TG owner's contention-winner session is active on\n          this TG.  Some nodes in the network are not able to\n          differentiate support and status of CP-CP sessions, and thus\n          may report the 'supportedUnknownStatus' value.\n\n          This object corresponds to cv47, byte 6, bits 3-4.")
appnNnTgFREffCap = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 12), AppnTgEffectiveCapacity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFREffCap.setDescription('Effective capacity for this TG.')
appnNnTgFRConnCost = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRConnCost.setDescription('Cost per connect time.\n\n          This is an administratively assigned value representing the\n          relative cost per unit of time to use this TG.  Range is from\n\n          0, which means no cost, to 255, which indicates maximum cost.\n\n          This object corresponds to cv47, byte 13.')
appnNnTgFRByteCost = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRByteCost.setDescription('Cost per byte transmitted.\n\n          This is an administratively assigned value representing the\n          relative cost of transmitting a byte over this TG.  Range is\n          from 0, which means no cost, to 255, which indicates maximum\n          cost.\n\n          This object corresponds to cv47, byte 14.')
appnNnTgFRSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 15), AppnTgSecurity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRSecurity.setDescription('Administratively assigned security level of this TG.\n\n          This object corresponds to cv47, byte 16.')
appnNnTgFRDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 16), AppnTgDelay()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRDelay.setDescription('Administratively assigned delay associated with this TG.\n\n          This object corresponds to cv47, byte 17.')
appnNnTgFRUsr1 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 17), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRUsr1.setDescription('First user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.\n\n          This object corresponds to cv47, byte 19.')
appnNnTgFRUsr2 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 18), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRUsr2.setDescription('Second user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.\n\n          This object corresponds to cv47, byte 20.')
appnNnTgFRUsr3 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 19), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRUsr3.setDescription('Third user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.\n\n          This object corresponds to cv47, byte 21.')
appnNnTgFRGarbageCollect = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 20), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRGarbageCollect.setDescription('Indicates whether the TG has been marked for garbage\n          collection (deletion from the topology database) upon the next\n          garbage collection cycle.\n\n          This object corresponds to cv47, byte 6, bit 1.')
appnNnTgFRSubareaNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 21), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRSubareaNum.setDescription('The subarea number associated with this TG.\n\n          This object corresponds to cv4680, bytes m+2 through m+5.')
appnNnTgFRHprSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 22), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRHprSup.setDescription('Indicates whether high performance routing (HPR)\n          is supported over this TG.\n\n          This object corresponds to cv4680, byte m+1, bit 2.')
appnNnTgFRDestHprTrans = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 23), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRDestHprTrans.setDescription('Indicates whether the destination node supports\n          high performance routing (HPR) transport tower.\n\n          This object corresponds to cv4680, byte m+1, bit 7.')
appnNnTgFRTypeIndicator = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 24), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('unknown', 1), ('appnOrBfTg', 2), ('interchangeTg', 3), ('virtualRouteTg', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRTypeIndicator.setDescription('Indicates the type of the TG.\n\n          This object corresponds to cv4680, byte m+1, bits 3-4.')
appnNnTgFRIntersubnet = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 25), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRIntersubnet.setDescription('Indicates whether the transmission group is an intersubnet TG,\n          which defines a border between subnetworks.\n\n          This object corresponds to cv4680, byte m+1, bit 5.')
appnNnTgFRMltgLinkType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 26), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRMltgLinkType.setDescription('This object indicates whether the transmission group is a\n          multi-link TG.  A TG that has been brought up as a multi-link\n          TG is reported as one, even if it currently has only one link\n          active.\n\n          This object corresponds to cv47, byte 6, bit 5.')
appnNnTgFRBranchTg = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 2, 2, 4, 1, 27), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNnTgFRBranchTg.setDescription('Indicates whether the transmission group is a branch TG\n          (equivalently, whether the destination of the transmission\n          group is a branch network node).\n\n          This object corresponds to cv4680, byte m+1, bit 1.')
appnLocalTopology = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 3))
appnLocalTgTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1))
if mibBuilder.loadTexts:
    appnLocalTgTable.setDescription('TG Table describes all of the TGs owned by this node.  The TG\n          destination can be a virtual node, network node, LEN node, or\n          end node.')
appnLocalTgEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1)).setIndexNames((0, 'APPN-MIB', 'appnLocalTgDest'), (0, 'APPN-MIB', 'appnLocalTgNum'))
if mibBuilder.loadTexts:
    appnLocalTgEntry.setDescription('This table is indexed by the destination CpName and the TG\n          number.')
appnLocalTgDest = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 1), SnaControlPointName())
if mibBuilder.loadTexts:
    appnLocalTgDest.setDescription('Administratively assigned name of the destination node for\n          this TG.  This is the fully qualified name of a network node,\n          end node, LEN node, or virtual routing node.')
appnLocalTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts:
    appnLocalTgNum.setDescription('Number associated with this transmission group.')
appnLocalTgDestVirtual = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgDestVirtual.setDescription('Indicates whether the destination node for this TG is a\n          virtual routing node.')
appnLocalTgDlcData = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 4), AppnTgDlcData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgDlcData.setDescription('DLC-specific data related to a link connection network.')
appnLocalTgPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 10))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgPortName.setDescription('Administratively assigned name for the local port associated\n          with this TG.  A zero-length string indicates that this value\n          is unknown.')
appnLocalTgQuiescing = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgQuiescing.setDescription('Indicates whether the transmission group is quiescing.')
appnLocalTgOperational = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgOperational.setDescription('Indicates whether the transmission group is operational.')
appnLocalTgCpCpSession = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('supportedUnknownStatus', 1), ('supportedActive', 2), ('notSupported', 3), ('supportedNotActive', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgCpCpSession.setDescription("Indicates whether CP-CP sessions are supported on this TG, and\n          whether the TG owner's contention-winner session is active on\n          this TG.  Some nodes in the network are not able to\n          differentiate support and status of CP-CP sessions, and thus\n          may report the 'supportedUnknownStatus' value.")
appnLocalTgEffCap = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 9), AppnTgEffectiveCapacity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgEffCap.setDescription('Effective capacity for this TG.')
appnLocalTgConnCost = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgConnCost.setDescription('Cost per connect time:  a value representing the relative cost\n          per unit of time to use the TG.  Range is from 0, which means\n          no cost, to 255.')
appnLocalTgByteCost = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgByteCost.setDescription('Relative cost of transmitting a byte over this link.\n          Range is from 0 (lowest cost) to 255.')
appnLocalTgSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 12), AppnTgSecurity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgSecurity.setDescription('Administratively assigned security level of this TG.')
appnLocalTgDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 13), AppnTgDelay()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgDelay.setDescription('Administratively assigned delay associated with this TG.')
appnLocalTgUsr1 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgUsr1.setDescription('First user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.')
appnLocalTgUsr2 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgUsr2.setDescription('Second user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.')
appnLocalTgUsr3 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgUsr3.setDescription('Third user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.')
appnLocalTgHprSup = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 17), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noHprSupport', 1), ('hprBaseOnly', 2), ('rtpTower', 3), ('controlFlowsOverRtpTower', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgHprSup.setDescription('Indicates the level of high performance routing (HPR) support\n          over this TG :\n\n             noHprSupport(1)             - no HPR support\n             hprBaseOnly(2)              - HPR base (option set 1400)\n                                           supported\n             rtpTower(3)                 - HPR base and RTP tower\n                                           (option set 1401) supported\n             controlFlowsOverRtpTower(4) - HPR base, RTP tower, and\n                                           control flows over RTP\n                                           (option set 1402) supported')
appnLocalTgIntersubnet = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 18), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgIntersubnet.setDescription('Indicates whether the transmission group is an intersubnet TG,\n          which defines a border between subnetworks.')
appnLocalTgMltgLinkType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 19), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgMltgLinkType.setDescription('This object indicates whether the transmission group is a\n          multi-link TG.  A TG that has been brought up as a multi-link\n          TG is reported as one, even if it currently has only one link\n          active.')
appnLocalTgBranchLinkType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 1, 1, 20), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 255))).clone(namedValues=NamedValues(('other', 1), ('uplink', 2), ('downlink', 3), ('downlinkToBranchNetworkNode', 4), ('none', 5), ('unknown', 255)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalTgBranchLinkType.setDescription("Branch link type of this TG:\n             other(1)             = the agent has determined the TG's\n                                    branch link type to be a value other\n                                    than branch uplink or branch\n                                    downlink.  This is the value used\n                                    for a connection network TG owned by\n                                    a branch network node.\n             uplink(2)            = the TG is a branch uplink.\n             downlink(3)          = the TG is a branch downlink to an\n                                    end node.\n             downlinkToBranchNetworkNode(4) = the TG is a branch\n                                    downlink to a cascaded branch\n\n                                    network node.\n             none(5)              = the TG is not a branch TG.\n             unknown(255)         = the agent cannot determine the\n                                    branch link type of the TG.")
appnLocalEnTgTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2))
if mibBuilder.loadTexts:
    appnLocalEnTgTable.setDescription('Table describing all of the TGs owned by the end nodes known\n          to this node via TG registration.  This node does not represent\n          its own view of the TG on behalf of the partner node in this\n          table.  The TG destination can be a virtual routing node,\n          network node, or end node.')
appnLocalEnTgEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1)).setIndexNames((0, 'APPN-MIB', 'appnLocalEnTgOrigin'), (0, 'APPN-MIB', 'appnLocalEnTgDest'), (0, 'APPN-MIB', 'appnLocalEnTgNum'))
if mibBuilder.loadTexts:
    appnLocalEnTgEntry.setDescription('This table requires multiple indexes to uniquely identify each\n          TG.  They are originating CPname, destination CPname, and the\n          TG number.')
appnLocalEnTgOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 1), SnaControlPointName())
if mibBuilder.loadTexts:
    appnLocalEnTgOrigin.setDescription('Administratively assigned name of the origin node for this\n          TG.  This is a fully qualified network name.')
appnLocalEnTgDest = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 2), SnaControlPointName())
if mibBuilder.loadTexts:
    appnLocalEnTgDest.setDescription('Administratively assigned name of the destination node for\n          this TG.  This is the fully qualified name of a network node,\n          end node, LEN node, or virtual routing node.')
appnLocalEnTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts:
    appnLocalEnTgNum.setDescription('Number associated with this transmission group.')
appnLocalEnTgEntryTimeLeft = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 4), AppnTopologyEntryTimeLeft()).setUnits('days').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgEntryTimeLeft.setDescription('Number of days before deletion of this end node TG entry.')
appnLocalEnTgDestVirtual = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 5), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgDestVirtual.setDescription('Indicates whether the destination node is a virtual routing\n          node.')
appnLocalEnTgDlcData = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 6), AppnTgDlcData()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgDlcData.setDescription('DLC-specific data related to a link connection network.')
appnLocalEnTgOperational = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgOperational.setDescription('Indicates whether the transmission group is operational.')
appnLocalEnTgCpCpSession = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('supportedUnknownStatus', 1), ('supportedActive', 2), ('notSupported', 3), ('supportedNotActive', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgCpCpSession.setDescription("Indicates whether CP-CP sessions are supported on this TG, and\n          whether the TG owner's contention-winner session is active on\n          this TG.  Some nodes in the network are not able to\n\n          differentiate support and status of CP-CP sessions, and thus\n          may report the 'supportedUnknownStatus' value.")
appnLocalEnTgEffCap = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 9), AppnTgEffectiveCapacity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgEffCap.setDescription('Effective capacity for this TG.')
appnLocalEnTgConnCost = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgConnCost.setDescription('Cost per connect time:  a value representing the relative cost\n          per unit of time to use the TG.  Range is from 0, which means\n          no cost, to 255.')
appnLocalEnTgByteCost = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgByteCost.setDescription('Relative cost of transmitting a byte over this link.\n          Range is from 0, which means no cost, to 255.')
appnLocalEnTgSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 12), AppnTgSecurity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgSecurity.setDescription('Administratively assigned security level of this TG.')
appnLocalEnTgDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 13), AppnTgDelay()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgDelay.setDescription('Administratively assigned delay associated with this TG.')
appnLocalEnTgUsr1 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgUsr1.setDescription('First user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.')
appnLocalEnTgUsr2 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgUsr2.setDescription('Second user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.')
appnLocalEnTgUsr3 = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgUsr3.setDescription('Third user-defined TG characteristic for this TG.  This is\n          an administratively assigned value associated with the TG.')
appnLocalEnTgMltgLinkType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 3, 2, 1, 17), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnLocalEnTgMltgLinkType.setDescription('This object indicates whether the transmission group is a\n          multi-link TG.  A TG that has been brought up as a multi-link\n          TG is reported as one, even if it currently has only one link\n          active.')
appnDir = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 4))
appnDirPerf = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1))
appnDirMaxCaches = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 1), Unsigned32()).setUnits('directory entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirMaxCaches.setDescription('Maximum number of cache entries allowed.  This is an\n          administratively assigned value.')
appnDirCurCaches = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 2), Gauge32()).setUnits('directory entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirCurCaches.setDescription('Current number of cache entries.')
appnDirCurHomeEntries = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 3), Gauge32()).setUnits('directory entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirCurHomeEntries.setDescription('Current number of home entries.')
appnDirRegEntries = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 4), Gauge32()).setUnits('directory entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirRegEntries.setDescription('Current number of registered entries.')
appnDirInLocates = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 5), AppnNodeCounter()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirInLocates.setDescription('Number of directed Locates received since the node was last\n          reinitialized.')
appnDirInBcastLocates = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 6), AppnNodeCounter()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirInBcastLocates.setDescription('Number of broadcast Locates received since the node was last\n          reinitialized.')
appnDirOutLocates = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 7), AppnNodeCounter()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirOutLocates.setDescription('Number of directed Locates sent since the node was last\n          reinitialized.')
appnDirOutBcastLocates = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 8), AppnNodeCounter()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirOutBcastLocates.setDescription('Number of broadcast Locates sent since the node was last\n          reinitialized.')
appnDirNotFoundLocates = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 9), AppnNodeCounter()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirNotFoundLocates.setDescription("Number of directed Locates returned with a 'not found' since\n          the node was last reinitialized.")
appnDirNotFoundBcastLocates = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 10), AppnNodeCounter()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirNotFoundBcastLocates.setDescription("Number of broadcast Locates returned with a 'not found' since\n          the node was last reinitialized.")
appnDirLocateOutstands = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 1, 11), Gauge32()).setUnits('Locate messages').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirLocateOutstands.setDescription('Current number of outstanding Locates, both directed and\n          broadcast.  This value varies.  A value of zero indicates\n          that no Locates are unanswered.')
appnDirTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2))
if mibBuilder.loadTexts:
    appnDirTable.setDescription('Table containing information about all known LUs.')
appnDirEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1)).setIndexNames((0, 'APPN-MIB', 'appnDirLuName'))
if mibBuilder.loadTexts:
    appnDirEntry.setDescription('This table is indexed by the LU name.')
appnDirLuName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 17)))
if mibBuilder.loadTexts:
    appnDirLuName.setDescription("Fully qualified network LU name in the domain of the\n           serving network node.  Entries take one of three forms:\n\n              - Explicit entries do not contain the character '*'.\n              - Partial wildcard entries have the form 'ccc*', where\n                'ccc' represents one to sixteen characters in a\n                legal SNA LuName.\n              - A full wildcard entry consists of the single\n                character '*'")
appnDirNnServerName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1, 2), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirNnServerName.setDescription('Fully qualified control point (CP) name of the network node\n          server.  For unassociated end node entries, a zero-length\n          string is returned.')
appnDirLuOwnerName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1, 3), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirLuOwnerName.setDescription('Fully qualified CP name of the node at which the LU is\n          located.  This name is the same as the serving NN name when\n          the LU is located at a network node.  It is also the same as\n          the fully qualified LU name when this is the control point\n          LU for this node.')
appnDirLuLocation = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('local', 1), ('domain', 2), ('xdomain', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirLuLocation.setDescription('Specifies the location of the LU with respect to the local\n          node.')
appnDirType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('home', 1), ('cache', 2), ('registered', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirType.setDescription('Directory types are:\n            1 - Home\n                  The LU is in the domain of the local node, and the LU\n                  information has been configured at the local node.\n\n            2 - Cache\n                  The LU has previously been located by a broadcast\n                  search, and the location information has been saved.\n\n\n            3 - Registered\n                  The LU is at an end node that is in the domain\n                  of the local network node.  Registered entries\n                  are registered by the served end node.')
appnDirApparentLuOwnerName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 4, 2, 1, 6), DisplayString().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(3, 17)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnDirApparentLuOwnerName.setDescription("Fully qualified CP name of the node at which the LU appears to\n          be located.  This object and the appnDirLuOwnerName object are\n          related as follows:\n\n          Implementations that support this object save in their\n          directory database information about an LU's owning control\n          point that was communicated in two control vectors:\n\n               -  an Associated Resource Entry (X'3C') CV with resource\n                  type X'00F4' (ENCP)\n\n               -  a Real Owning Control Point (X'4A') CV.\n\n          The X'4A' CV is created by a branch network node to preserve\n          the name of the real owning control point for an LU below the\n          branch network node, before it overwrites this name with its\n          own name in the X'3C' CV.  The X'4A' CV is not present for LUs\n          that are not below branch network nodes.\n\n          If the information a node has about an LU's owning CP came only\n          in a X'3C' CV, then the name from the X'3C' is returned in the\n          appnDirLuOwnerName object, and a null string is returned in\n          this object.\n\n          If the information a node has about an LU's owning CP came in\n          both X'3C' and X'4A' CVs, then the name from the X'4A' is\n          returned in the appnDirLuOwnerName object, and the name from\n          the X'3C' (which will be the branch network node's name) is\n          returned in this object.")
appnCos = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 5))
appnCosModeTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 1))
if mibBuilder.loadTexts:
    appnCosModeTable.setDescription('Table representing all of the defined mode names for this\n          node.  The table contains the matching COS name for each\n          mode name.')
appnCosModeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 1, 1)).setIndexNames((0, 'APPN-MIB', 'appnCosModeName'))
if mibBuilder.loadTexts:
    appnCosModeEntry.setDescription('This table is indexed by the mode name.')
appnCosModeName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 1, 1, 1), SnaModeName())
if mibBuilder.loadTexts:
    appnCosModeName.setDescription('Administratively assigned name for this mode.')
appnCosModeCosName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 1, 1, 2), SnaClassOfServiceName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosModeCosName.setDescription('Administratively assigned name for this class of service.')
appnCosNameTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 2))
if mibBuilder.loadTexts:
    appnCosNameTable.setDescription('Table mapping all of the defined class-of-service names for\n          this node to their network transmission priorities.')
appnCosNameEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 2, 1)).setIndexNames((0, 'APPN-MIB', 'appnCosName'))
if mibBuilder.loadTexts:
    appnCosNameEntry.setDescription('The COS name is the index to this table.')
appnCosName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 2, 1, 1), SnaClassOfServiceName())
if mibBuilder.loadTexts:
    appnCosName.setDescription('Administratively assigned name for this class of service.')
appnCosTransPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('low', 1), ('medium', 2), ('high', 3), ('network', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTransPriority.setDescription("Transmission priority for this class of service:\n\n              low(1)     - (X'01'):  low priority\n              medium(2)  - (X'02'):  medium priority\n              high(3)    - (X'03'):  high priority\n              network(4) - (X'04'):  network priority")
appnCosNodeRowTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3))
if mibBuilder.loadTexts:
    appnCosNodeRowTable.setDescription('This table contains all node-row information for all classes\n          of service defined in this node.')
appnCosNodeRowEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1)).setIndexNames((0, 'APPN-MIB', 'appnCosNodeRowName'), (0, 'APPN-MIB', 'appnCosNodeRowIndex'))
if mibBuilder.loadTexts:
    appnCosNodeRowEntry.setDescription('A node entry for a given class of service.')
appnCosNodeRowName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 1), SnaClassOfServiceName())
if mibBuilder.loadTexts:
    appnCosNodeRowName.setDescription('Administratively assigned name for this class of service.')
appnCosNodeRowIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts:
    appnCosNodeRowIndex.setDescription('Subindex under appnCosNodeRowName, corresponding to a row in\n          the node table for the class of service identified in\n          appnCosNodeRowName.\n\n          For each class of service, this subindex orders rows in the\n          appnCosNodeRowTable in the same order as that used for route\n          calculation in the APPN node.')
appnCosNodeRowWgt = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 64))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosNodeRowWgt.setDescription('Weight to be associated with the nodes that fit the criteria\n          specified by this node row.\n\n          This value can either be a character representation of an\n          integer, or a formula for calculating the weight.')
appnCosNodeRowResistMin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosNodeRowResistMin.setDescription('Minimum route addition resistance value for this node.\n\n          Range of values is 0-255.  The lower the value, the more\n          desirable the node is for intermediate routing.')
appnCosNodeRowResistMax = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosNodeRowResistMax.setDescription('Maximum route addition resistance value for this node.\n          Range of values is 0-255.  The lower the value, the more\n          desirable the node is for intermediate routing.')
appnCosNodeRowMinCongestAllow = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosNodeRowMinCongestAllow.setDescription('Indicates whether low congestion will be tolerated.  This\n          object and appnCosNodeRowMaxCongestAllow together delineate a\n          range of acceptable congestion states for a node.  For the\n          ordered pair (minimum congestion allowed, maximum congestion\n          allowed), the values are interpreted as follows:\n\n           - (0,0):  only low congestion is acceptable\n           - (0,1):  either low or high congestion is acceptable\n           - (1,1):  only high congestion is acceptable.\n\n          Note that the combination (1,0) is not defined, since it\n          would identify a range whose lower bound was high congestion\n          and whose upper bound was low congestion.')
appnCosNodeRowMaxCongestAllow = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 3, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosNodeRowMaxCongestAllow.setDescription('Indicates whether low congestion will be tolerated.  This\n          object and appnCosNodeRowMinCongestAllow together delineate a\n          range of acceptable congestion states for a node.  For the\n          ordered pair (minimum congestion allowed, maximum congestion\n          allowed), the values are interpreted as follows:\n\n           - (0,0):  only low congestion is acceptable\n           - (0,1):  either low or high congestion is acceptable\n           - (1,1):  only high congestion is acceptable.\n\n          Note that the combination (1,0) is not defined, since it\n          would identify a range whose lower bound was high congestion\n          and whose upper bound was low congestion.')
appnCosTgRowTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4))
if mibBuilder.loadTexts:
    appnCosTgRowTable.setDescription('Table containing all the TG-row information for all classes of\n          service defined in this node.')
appnCosTgRowEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1)).setIndexNames((0, 'APPN-MIB', 'appnCosTgRowName'), (0, 'APPN-MIB', 'appnCosTgRowIndex'))
if mibBuilder.loadTexts:
    appnCosTgRowEntry.setDescription('A TG entry for a given class of service.')
appnCosTgRowName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 1), SnaClassOfServiceName())
if mibBuilder.loadTexts:
    appnCosTgRowName.setDescription('Administratively assigned name for this class of service.')
appnCosTgRowIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)))
if mibBuilder.loadTexts:
    appnCosTgRowIndex.setDescription('Subindex under appnCosTgRowName, corresponding to a row in the\n          TG table for the class of service identified in\n          appnCosTgRowName.\n\n          For each class of service, this subindex orders rows in the\n          appnCosTgRowTable in the same order as that used for route\n          calculation in the APPN node.')
appnCosTgRowWgt = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 64))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowWgt.setDescription('Weight to be associated with the TGs that fit the criteria\n          specified by this TG row.\n\n          This value can either be a character representation of an\n          integer, or a formula for calculating the weight.')
appnCosTgRowEffCapMin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 4), AppnTgEffectiveCapacity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowEffCapMin.setDescription('Minimum acceptable capacity for this class of service.')
appnCosTgRowEffCapMax = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 5), AppnTgEffectiveCapacity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowEffCapMax.setDescription('Maximum acceptable capacity for this class of service.')
appnCosTgRowConnCostMin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowConnCostMin.setDescription('Minimum acceptable cost per connect time for this class of\n          service.\n\n          Cost per connect time:  a value representing the relative\n          cost per unit of time to use this TG.  Range is from 0, which\n          means no cost, to 255.')
appnCosTgRowConnCostMax = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowConnCostMax.setDescription('Maximum acceptable cost per connect time for this class of\n          service.\n\n          Cost per connect time:  a value representing the relative\n          cost per unit of time to use this TG.  Range is from 0, which\n          means no cost, to 255.')
appnCosTgRowByteCostMin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowByteCostMin.setDescription('Minimum acceptable cost per byte transmitted for this class\n          of service.\n\n          Cost per byte transmitted:  a value representing the relative\n          cost per unit of time to use this TG.  Range is from 0, which\n          means no cost, to 255.')
appnCosTgRowByteCostMax = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowByteCostMax.setDescription('Maximum acceptable cost per byte transmitted for this class\n          of service.\n\n          Cost per byte transmitted:  a value representing the relative\n          cost of transmitting a byte over this TG.  Range is from 0,\n          which means no cost, to 255.')
appnCosTgRowSecurityMin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 10), AppnTgSecurity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowSecurityMin.setDescription('Minimum acceptable security for this class of service.')
appnCosTgRowSecurityMax = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 11), AppnTgSecurity()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowSecurityMax.setDescription('Maximum acceptable security for this class of service.')
appnCosTgRowDelayMin = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 12), AppnTgDelay()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowDelayMin.setDescription('Minimum acceptable propagation delay for this class of\n\n          service.')
appnCosTgRowDelayMax = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 13), AppnTgDelay()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowDelayMax.setDescription('Maximum acceptable propagation delay for this class of\n          service.')
appnCosTgRowUsr1Min = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowUsr1Min.setDescription('Minimum acceptable value for this user-defined\n          characteristic.')
appnCosTgRowUsr1Max = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowUsr1Max.setDescription('Maximum acceptable value for this user-defined\n          characteristic.')
appnCosTgRowUsr2Min = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowUsr2Min.setDescription('Minimum acceptable value for this user-defined\n          characteristic.')
appnCosTgRowUsr2Max = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 17), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowUsr2Max.setDescription('Maximum acceptable value for this user-defined\n          characteristic.')
appnCosTgRowUsr3Min = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 18), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowUsr3Min.setDescription('Minimum acceptable value for this user-defined\n          characteristic.')
appnCosTgRowUsr3Max = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 5, 4, 1, 19), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnCosTgRowUsr3Max.setDescription('Maximum acceptable value for this user-defined\n          characteristic.')
appnSessIntermediate = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 6))
appnIsInGlobal = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1))
appnIsInGlobeCtrAdminStatus = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('notActive', 1), ('active', 2), ('ready', 3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    appnIsInGlobeCtrAdminStatus.setDescription('Object by which a Management Station can deactivate or\n          activate capture of intermediate-session counts and names, by\n          setting the value to notActive(1) or active(2), respectively.\n          The value ready(3) is returned on GET operations until a SET\n          has been processed; after that the value received on the most\n          recent SET is returned.\n\n          The counts referred to here are the eight objects in the\n          AppnIsInTable, from appnIsInP2SFmdPius through\n          appnIsInS2PNonFmdBytes.  The names are the four objects in this\n          table, from appnIsInPriLuName through appnIsInCosName.\n\n          Setting this object to the following values has the following\n          effects:\n\n              notActive(1)  stop collecting count data.  If a count\n                            is queried, it returns the value 0.\n                            Collection of names may, but need not be,\n                            disabled.\n              active(2)     start collecting count data.  If it is\n                            supported, collection of names is enabled.')
appnIsInGlobeCtrOperStatus = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('notActive', 1), ('active', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInGlobeCtrOperStatus.setDescription('Indicates whether or not the intermediate session counts\n          are active.  The counts referred to here are the eight\n          objects in the AppnIsInTable, from appnIsInP2SFmdPius through\n          appnIsInS2PNonFmdBytes.  These eight counts are of type\n          Unsigned32 rather than Counter32 because when this object\n          enters the notActive state, either because a Management\n          Station has set appnInInGlobeCtrAdminStatus to notActive or\n          because of a locally-initiated transition, the counts are\n          all reset to 0.\n\n          The values for this object are:\n\n              notActive(1):  collection of counts is not active; if it\n                             is queried, a count returns the value 0.\n              active(2):     collection of counts is active.')
appnIsInGlobeCtrStatusTime = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 3), TimeTicks()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInGlobeCtrStatusTime.setDescription('The time since the appnIsInGlobeCtrOperStatus object last\n          changed, measured in hundredths of a second.  This time can be\n          used to identify when this change occurred in relation to other\n          events in the agent, such as the last time the APPN node was\n          reinitialized.')
appnIsInGlobeRscv = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('notActive', 1), ('active', 2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    appnIsInGlobeRscv.setDescription('Indicates the current route selection control vector (RSCV)\n          collection option in effect, and allows a Management Station to\n          change the option.\n\n          The values for this object are:\n\n             notActive(1): collection of route selection control vectors\n                           is not active.\n             active(2):    collection of route selection control vectors\n                           is active.')
appnIsInGlobeRscvTime = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 5), TimeTicks()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInGlobeRscvTime.setDescription('The time since the appnIsInGlobeRscv object last changed,\n          measured in hundredths of a second.  This time can be used to\n          identify when this change occurred in relation to other events\n          in the agent, such as the last time the APPN node was\n          reinitialized.')
appnIsInGlobeActSess = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 6), Gauge32()).setUnits('sessions').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInGlobeActSess.setDescription('The number of currently active intermediate sessions.')
appnIsInGlobeHprBfActSess = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 1, 7), Gauge32()).setUnits('sessions').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInGlobeHprBfActSess.setDescription('The number of currently active HPR intermediate sessions.')
appnIsInTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2))
if mibBuilder.loadTexts:
    appnIsInTable.setDescription('Intermediate Session Information Table')
appnIsInEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1)).setIndexNames((0, 'APPN-MIB', 'appnIsInFqCpName'), (0, 'APPN-MIB', 'appnIsInPcid'))
if mibBuilder.loadTexts:
    appnIsInEntry.setDescription('Entry of Intermediate Session Information Table.')
appnIsInFqCpName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 1), SnaControlPointName())
if mibBuilder.loadTexts:
    appnIsInFqCpName.setDescription('The network-qualified control point name of the node at which\n          the session and PCID originated.  For APPN and LEN nodes, this\n          is either CP name of the APPN node at which the origin LU is\n          located or the CP name of the NN serving the LEN node at which\n          the origin LU is located.  For resources served by a dependent\n          LU requester (DLUR), it is the name of the owning system\n          services control point (SSCP).')
appnIsInPcid = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8))
if mibBuilder.loadTexts:
    appnIsInPcid.setDescription('The procedure correlation identifier (PCID) of a session.  It\n          is an 8-byte value assigned by the primary LU.')
appnIsInSessState = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('inactive', 1), ('pendactive', 2), ('active', 3), ('pendinact', 4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    appnIsInSessState.setDescription('Indicates the state of the session:\n\n              inactive(1)   - session is inactive\n              pendactive(2) - session is pending active\n              active(3)     - session is active\n              pendinact(4)  - session is pending inactive\n\n          Active sessions can be deactivated by setting this object\n          to inactive(1).')
appnIsInPriLuName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 17))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPriLuName.setDescription('The primary LU name of the session.  A zero-length\n          string indicates that this name is not available.')
appnIsInSecLuName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 17))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSecLuName.setDescription('The secondary LU name of the session.  A zero-length\n          string indicates that this name is not available.')
appnIsInModeName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 6), SnaModeName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInModeName.setDescription('The mode name used for this session.')
appnIsInCosName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 7), SnaClassOfServiceName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInCosName.setDescription('The Class of Service (COS) name used for this session.')
appnIsInTransPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('low', 1), ('medium', 2), ('high', 3), ('network', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInTransPriority.setDescription("Transmission priority for this class of service.  Values are:\n\n              low(1)     - (X'01'):  low priority\n              medium(2)  - (X'02'):  medium priority\n              high(3)    - (X'03'):  high priority\n              network(4) - (X'04'):  network priority")
appnIsInSessType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('unknown', 1), ('lu62', 2), ('lu0thru3', 3), ('lu62dlur', 4), ('lu0thru3dlur', 5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSessType.setDescription('The type of intermediate session.  Defined values are\n\n              unknown      The session type is not known.\n\n              lu62         A session between LUs of type 6.2\n                           (as indicated by the LU type in Bind)\n\n              lu0thru3     A session between LUs of type 0, 1, 2, or 3\n                           (as indicated by the LU type in Bind)\n\n              lu62dlur     A session between LUs of type 6.2\n                           (as indicated by the LU type in Bind).\n                           One of the LUs is a dependent LU supported\n                           by the dependent LU requester (DLUR)\n                           function at this node.\n\n              lu0thru3dlur A session between LUs of type 0, 1, 2, or 3\n                           (as indicated by the LU type in Bind)\n                           One of the LUs is a dependent LU supported\n                           by the dependent LU requester (DLUR)\n                           function at this node.')
appnIsInSessUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 10), TimeTicks()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSessUpTime.setDescription('Length of time the session has been active, measured in\n          hundredths of a second.')
appnIsInCtrUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 11), TimeTicks()).setUnits('hundredths of a second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInCtrUpTime.setDescription('Length of time the session counters have been active, measured\n          in hundredths of a second.')
appnIsInP2SFmdPius = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 12), Unsigned32()).setUnits('path information units (PIUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInP2SFmdPius.setDescription('Number of function management data (FMD) path information\n          units (PIUs) sent from the Primary LU to the Secondary LU since\n          the counts were last activated.')
appnIsInS2PFmdPius = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 13), Unsigned32()).setUnits('path information units (PIUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInS2PFmdPius.setDescription('Number of FMD PIUs sent from the Secondary LU to the Primary\n          LU since the counts were last activated.')
appnIsInP2SNonFmdPius = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 14), Unsigned32()).setUnits('path information units (PIUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInP2SNonFmdPius.setDescription('Number of non-FMD PIUs sent from the Primary LU to the\n          Secondary LU since the counts were last activated.')
appnIsInS2PNonFmdPius = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 15), Unsigned32()).setUnits('path information units (PIUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInS2PNonFmdPius.setDescription('Number of non-FMD PIUs sent from the Secondary LU to the\n          Primary LU since the counts were last activated.')
appnIsInP2SFmdBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 16), Unsigned32()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInP2SFmdBytes.setDescription('Number of FMD bytes sent from the Primary LU to the Secondary\n          LU since the counts were last activated.')
appnIsInS2PFmdBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 17), Unsigned32()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInS2PFmdBytes.setDescription('Number of FMD bytes sent from the Secondary LU to the Primary\n          LU since the counts were last activated.')
appnIsInP2SNonFmdBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 18), Unsigned32()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInP2SNonFmdBytes.setDescription('Number of non-FMD bytes sent from the Primary LU to the\n          Secondary LU since the counts were last activated.')
appnIsInS2PNonFmdBytes = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 19), Unsigned32()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInS2PNonFmdBytes.setDescription('Number of non-FMD bytes sent from the Secondary LU to the\n          Primary LU since the counts were last activated.')
appnIsInPsAdjCpName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 20), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsAdjCpName.setDescription('The primary stage adjacent CP name of this session.  If the\n          session stage traverses an RTP connection, the CP name of the\n          remote RTP endpoint is returned.')
appnIsInPsAdjTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 21), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 300))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsAdjTgNum.setDescription("The primary stage adjacent transmission group (TG) number\n          associated with this session.  If the session stage traverses\n          an RTP connection, the value 256 is returned.\n\n          Values between 257 and 300 are available for other possible\n          TG 'stand-ins' that may be added to APPN in the future.")
appnIsInPsSendMaxBtuSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 22), Integer32().subtype(subtypeSpec=ValueRangeConstraint(99, 32767))).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsSendMaxBtuSize.setDescription('The primary stage maximum basic transmission unit (BTU) size\n          for sending data.')
appnIsInPsSendPacingType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 23), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('fixed', 1), ('adaptive', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsSendPacingType.setDescription('The primary stage type of pacing being used for sending data.')
appnIsInPsSendRpc = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 24), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsSendRpc.setDescription('The primary stage send residual pace count.  This represents\n          the primary stage number of message units (MUs) that can still\n          be sent in the current session window.')
appnIsInPsSendNxWndwSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 25), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsSendNxWndwSize.setDescription('The primary stage size of the next window which will be used\n          to send data.')
appnIsInPsRecvPacingType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 26), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('fixed', 1), ('adaptive', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsRecvPacingType.setDescription('The primary stage type of pacing being used for receiving\n          data.')
appnIsInPsRecvRpc = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 27), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsRecvRpc.setDescription('The primary stage receive residual pace count.  This\n          represents the primary stage number of message units (MUs) that\n          can still be received in the current session window.')
appnIsInPsRecvNxWndwSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 28), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInPsRecvNxWndwSize.setDescription('The primary stage size of the next window which will be used\n          to receive data.')
appnIsInSsAdjCpName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 29), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsAdjCpName.setDescription('The secondary stage adjacent CP name of this session.  If the\n          session stage traverses an RTP connection, the CP name of the\n          remote RTP endpoint is returned.')
appnIsInSsAdjTgNum = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 30), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 300))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsAdjTgNum.setDescription("The secondary stage adjacent transmission group (TG) number\n          associated with this session.  If the session stage traverses\n          an RTP connection, the value 256 is returned.\n\n          Values between 257 and 300 are available for other possible\n          TG 'stand-ins' that may be added to APPN in the future.")
appnIsInSsSendMaxBtuSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 31), Integer32().subtype(subtypeSpec=ValueRangeConstraint(99, 32767))).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsSendMaxBtuSize.setDescription('The secondary stage maximum basic transmission unit (BTU) size\n          for sending data.')
appnIsInSsSendPacingType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 32), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('fixed', 1), ('adaptive', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsSendPacingType.setDescription('The secondary stage type of pacing being used for sending\n          data.')
appnIsInSsSendRpc = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 33), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsSendRpc.setDescription('The secondary stage send residual pace count.  This represents\n          the secondary stage number of message units (MUs) that can\n          still be sent in the current session window.')
appnIsInSsSendNxWndwSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 34), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsSendNxWndwSize.setDescription('The secondary stage size of the next window which will be used\n          to send data.')
appnIsInSsRecvPacingType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 35), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('fixed', 1), ('adaptive', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsRecvPacingType.setDescription('The secondary stage type of pacing being used for receiving\n          data.')
appnIsInSsRecvRpc = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 36), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsRecvRpc.setDescription('The secondary stage receive residual pace count.  This\n          represents the secondary stage number of message units (MUs)\n          that can still be received in the current session window.')
appnIsInSsRecvNxWndwSize = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 37), Gauge32()).setUnits('message units (MUs)').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInSsRecvNxWndwSize.setDescription('The secondary stage size of the next window which will be used\n          to receive data.')
appnIsInRouteInfo = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 38), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInRouteInfo.setDescription("The route selection control vector (RSCV X'2B') used for this\n          session.  It is present for APPN nodes; but is not present for\n          LEN nodes.  The format of this vector is described in SNA\n          Formats.  If no RSCV is available, a zero-length string is\n          returned.")
appnIsInRtpNceId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 39), OctetString().subtype(subtypeSpec=ValueSizeConstraint(1, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInRtpNceId.setDescription('The HPR local Network Connection Endpoint of the session.')
appnIsInRtpTcid = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 2, 1, 40), OctetString().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsInRtpTcid.setDescription('The RTP connection local TCID of the session.')
appnIsRtpTable = MibTable((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 3))
if mibBuilder.loadTexts:
    appnIsRtpTable.setDescription('A table indicating how many ISR sessions are transported by\n          each RTP connection.')
appnIsRtpEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 3, 1)).setIndexNames((0, 'APPN-MIB', 'appnIsRtpNceId'), (0, 'APPN-MIB', 'appnIsRtpTcid'))
if mibBuilder.loadTexts:
    appnIsRtpEntry.setDescription('Entry of Intermediate Session RTP Table.')
appnIsRtpNceId = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 3, 1, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(1, 8)))
if mibBuilder.loadTexts:
    appnIsRtpNceId.setDescription('The local Network Connection Endpoint of the RTP connection.')
appnIsRtpTcid = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 3, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8))
if mibBuilder.loadTexts:
    appnIsRtpTcid.setDescription('The local TCID of the RTP connection.')
appnIsRtpSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 4, 1, 6, 3, 1, 3), Gauge32()).setUnits('sessions').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnIsRtpSessions.setDescription('The number of intermediate sessions using this RTP\n          connection.')
appnTraps = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 2))
alertTrap = NotificationType((1, 3, 6, 1, 2, 1, 34, 4, 2, 1)).setObjects(*(('APPN-MIB', 'alertIdNumber'), ('APPN-MIB', 'affectedObject')))
if mibBuilder.loadTexts:
    alertTrap.setDescription('This trap carries a 32-bit SNA Management Services (SNA/MS)\n          Alert ID Number, as specified in SNA/MS Formats.')
alertIdNumber = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 2, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4, 4)).setFixedLength(4)).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    alertIdNumber.setDescription('A 32-bit SNA Management Services (SNA/MS) Alert ID Number, as\n          specified in SNA/MS Formats.')
affectedObject = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 2, 3), VariablePointer()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    affectedObject.setDescription('The MIB object associated with the Alert condition, if there\n          is an object associated with it.  If no associated object can\n          be identified, the value 0.0 is passed in the trap.')
appnConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 3))
appnCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 3, 1))
appnGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 4, 3, 2))
appnCompliance2 = ModuleCompliance((1, 3, 6, 1, 2, 1, 34, 4, 3, 1, 3)).setObjects(*(('APPN-MIB', 'appnGeneralConfGroup2'), ('APPN-MIB', 'appnPortConfGroup'), ('APPN-MIB', 'appnLinkConfGroup2'), ('APPN-MIB', 'appnLocalTgConfGroup2'), ('APPN-MIB', 'appnDirTableConfGroup2'), ('APPN-MIB', 'appnNnUniqueConfGroup'), ('APPN-MIB', 'appnEnUniqueConfGroup'), ('APPN-MIB', 'appnVrnConfGroup'), ('APPN-MIB', 'appnNnTopoConfGroup2'), ('APPN-MIB', 'appnLocalEnTopoConfGroup2'), ('APPN-MIB', 'appnLocalDirPerfConfGroup'), ('APPN-MIB', 'appnCosConfGroup'), ('APPN-MIB', 'appnIntSessConfGroup'), ('APPN-MIB', 'appnHprBaseConfGroup'), ('APPN-MIB', 'appnHprRtpConfGroup'), ('APPN-MIB', 'appnHprCtrlFlowsRtpConfGroup'), ('APPN-MIB', 'appnHprBfConfGroup'), ('APPN-MIB', 'appnTrapConfGroup'), ('APPN-MIB', 'appnTrapNotifGroup'), ('APPN-MIB', 'appnBrNnConfGroup')))
if mibBuilder.loadTexts:
    appnCompliance2.setDescription('The compliance statement for the SNMPv2 entities that\n            implement the APPN MIB.\n\n            In the descriptions for the conditionally mandatory groups that\n            follow, the branch network node is treated as a third node type,\n            parallel to network node and end node.  This is not how branch\n            network nodes are treated in the base APPN architecture, but it\n            increases clarity here to do it.')
appnGeneralConfGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 26)).setObjects(*(('APPN-MIB', 'appnNodeCpName'), ('APPN-MIB', 'appnNodeId'), ('APPN-MIB', 'appnNodeType'), ('APPN-MIB', 'appnNodeUpTime'), ('APPN-MIB', 'appnNodeParallelTg'), ('APPN-MIB', 'appnNodeAdaptiveBindPacing'), ('APPN-MIB', 'appnNodeHprSupport'), ('APPN-MIB', 'appnNodeCounterDisconTime'), ('APPN-MIB', 'appnNodeLsCounterType'), ('APPN-MIB', 'appnNodeBrNn')))
if mibBuilder.loadTexts:
    appnGeneralConfGroup2.setDescription('A collection of objects providing the instrumentation of\n            APPN general information and capabilities.')
appnPortConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 2)).setObjects(*(('APPN-MIB', 'appnPortCommand'), ('APPN-MIB', 'appnPortOperState'), ('APPN-MIB', 'appnPortDlcType'), ('APPN-MIB', 'appnPortPortType'), ('APPN-MIB', 'appnPortSIMRIM'), ('APPN-MIB', 'appnPortLsRole'), ('APPN-MIB', 'appnPortNegotLs'), ('APPN-MIB', 'appnPortDynamicLinkSupport'), ('APPN-MIB', 'appnPortMaxRcvBtuSize'), ('APPN-MIB', 'appnPortMaxIframeWindow'), ('APPN-MIB', 'appnPortDefLsGoodXids'), ('APPN-MIB', 'appnPortDefLsBadXids'), ('APPN-MIB', 'appnPortDynLsGoodXids'), ('APPN-MIB', 'appnPortDynLsBadXids'), ('APPN-MIB', 'appnPortSpecific'), ('APPN-MIB', 'appnPortDlcLocalAddr'), ('APPN-MIB', 'appnPortCounterDisconTime')))
if mibBuilder.loadTexts:
    appnPortConfGroup.setDescription('A collection of objects providing the instrumentation of\n            APPN port information.')
appnLinkConfGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 27)).setObjects(*(('APPN-MIB', 'appnLsCommand'), ('APPN-MIB', 'appnLsOperState'), ('APPN-MIB', 'appnLsPortName'), ('APPN-MIB', 'appnLsDlcType'), ('APPN-MIB', 'appnLsDynamic'), ('APPN-MIB', 'appnLsAdjCpName'), ('APPN-MIB', 'appnLsAdjNodeType'), ('APPN-MIB', 'appnLsTgNum'), ('APPN-MIB', 'appnLsLimResource'), ('APPN-MIB', 'appnLsActOnDemand'), ('APPN-MIB', 'appnLsMigration'), ('APPN-MIB', 'appnLsPartnerNodeId'), ('APPN-MIB', 'appnLsCpCpSessionSupport'), ('APPN-MIB', 'appnLsMaxSendBtuSize'), ('APPN-MIB', 'appnLsInXidBytes'), ('APPN-MIB', 'appnLsInMsgBytes'), ('APPN-MIB', 'appnLsInXidFrames'), ('APPN-MIB', 'appnLsInMsgFrames'), ('APPN-MIB', 'appnLsOutXidBytes'), ('APPN-MIB', 'appnLsOutMsgBytes'), ('APPN-MIB', 'appnLsOutXidFrames'), ('APPN-MIB', 'appnLsOutMsgFrames'), ('APPN-MIB', 'appnLsEchoRsps'), ('APPN-MIB', 'appnLsCurrentDelay'), ('APPN-MIB', 'appnLsMaxDelay'), ('APPN-MIB', 'appnLsMinDelay'), ('APPN-MIB', 'appnLsMaxDelayTime'), ('APPN-MIB', 'appnLsGoodXids'), ('APPN-MIB', 'appnLsBadXids'), ('APPN-MIB', 'appnLsSpecific'), ('APPN-MIB', 'appnLsActiveTime'), ('APPN-MIB', 'appnLsCurrentStateTime'), ('APPN-MIB', 'appnLsHprSup'), ('APPN-MIB', 'appnLsLocalAddr'), ('APPN-MIB', 'appnLsRemoteAddr'), ('APPN-MIB', 'appnLsRemoteLsName'), ('APPN-MIB', 'appnLsStatusTime'), ('APPN-MIB', 'appnLsStatusLsName'), ('APPN-MIB', 'appnLsStatusCpName'), ('APPN-MIB', 'appnLsStatusPartnerId'), ('APPN-MIB', 'appnLsStatusTgNum'), ('APPN-MIB', 'appnLsStatusGeneralSense'), ('APPN-MIB', 'appnLsStatusRetry'), ('APPN-MIB', 'appnLsStatusEndSense'), ('APPN-MIB', 'appnLsStatusXidLocalSense'), ('APPN-MIB', 'appnLsStatusXidRemoteSense'), ('APPN-MIB', 'appnLsStatusXidByteInError'), ('APPN-MIB', 'appnLsStatusXidBitInError'), ('APPN-MIB', 'appnLsStatusDlcType'), ('APPN-MIB', 'appnLsStatusLocalAddr'), ('APPN-MIB', 'appnLsStatusRemoteAddr'), ('APPN-MIB', 'appnLsCounterDisconTime'), ('APPN-MIB', 'appnLsMltgMember')))
if mibBuilder.loadTexts:
    appnLinkConfGroup2.setDescription('A collection of objects providing the instrumentation of\n            APPN link information.')
appnLocalTgConfGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 28)).setObjects(*(('APPN-MIB', 'appnLocalTgDestVirtual'), ('APPN-MIB', 'appnLocalTgDlcData'), ('APPN-MIB', 'appnLocalTgPortName'), ('APPN-MIB', 'appnLocalTgQuiescing'), ('APPN-MIB', 'appnLocalTgOperational'), ('APPN-MIB', 'appnLocalTgCpCpSession'), ('APPN-MIB', 'appnLocalTgEffCap'), ('APPN-MIB', 'appnLocalTgConnCost'), ('APPN-MIB', 'appnLocalTgByteCost'), ('APPN-MIB', 'appnLocalTgSecurity'), ('APPN-MIB', 'appnLocalTgDelay'), ('APPN-MIB', 'appnLocalTgUsr1'), ('APPN-MIB', 'appnLocalTgUsr2'), ('APPN-MIB', 'appnLocalTgUsr3'), ('APPN-MIB', 'appnLocalTgHprSup'), ('APPN-MIB', 'appnLocalTgIntersubnet'), ('APPN-MIB', 'appnLocalTgMltgLinkType')))
if mibBuilder.loadTexts:
    appnLocalTgConfGroup2.setDescription('A collection of objects providing the instrumentation of\n            APPN local TG information.')
appnDirTableConfGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 29)).setObjects(*(('APPN-MIB', 'appnDirNnServerName'), ('APPN-MIB', 'appnDirLuOwnerName'), ('APPN-MIB', 'appnDirLuLocation'), ('APPN-MIB', 'appnDirType'), ('APPN-MIB', 'appnDirApparentLuOwnerName')))
if mibBuilder.loadTexts:
    appnDirTableConfGroup2.setDescription('A collection of objects providing the instrumentation of the\n            APPN directory database.')
appnNnUniqueConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 6)).setObjects(*(('APPN-MIB', 'appnNodeNnCentralDirectory'), ('APPN-MIB', 'appnNodeNnTreeCache'), ('APPN-MIB', 'appnNodeNnRouteAddResist'), ('APPN-MIB', 'appnNodeNnIsr'), ('APPN-MIB', 'appnNodeNnFrsn'), ('APPN-MIB', 'appnNodeNnPeriBorderSup'), ('APPN-MIB', 'appnNodeNnInterchangeSup'), ('APPN-MIB', 'appnNodeNnExteBorderSup'), ('APPN-MIB', 'appnNodeNnSafeStoreFreq'), ('APPN-MIB', 'appnNodeNnRsn'), ('APPN-MIB', 'appnNodeNnCongested'), ('APPN-MIB', 'appnNodeNnIsrDepleted'), ('APPN-MIB', 'appnNodeNnQuiescing'), ('APPN-MIB', 'appnNodeNnGateway')))
if mibBuilder.loadTexts:
    appnNnUniqueConfGroup.setDescription('A collection of objects providing instrumentation unique\n            to APPN network nodes.')
appnEnUniqueConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 7)).setObjects(*(('APPN-MIB', 'appnNodeEnModeCosMap'), ('APPN-MIB', 'appnNodeEnNnServer'), ('APPN-MIB', 'appnNodeEnLuSearch')))
if mibBuilder.loadTexts:
    appnEnUniqueConfGroup.setDescription('A collection of objects providing instrumentation for\n            APPN end nodes.  Some of these objects also appear in the\n            instrumentation for a branch network node.')
appnVrnConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 8)).setObjects(*(('APPN-MIB', 'appnVrnPortName'),))
if mibBuilder.loadTexts:
    appnVrnConfGroup.setDescription('An object providing the instrumentation for virtual\n            routing node support in an APPN node.')
appnNnTopoConfGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 30)).setObjects(*(('APPN-MIB', 'appnNnTopoMaxNodes'), ('APPN-MIB', 'appnNnTopoCurNumNodes'), ('APPN-MIB', 'appnNnTopoNodePurges'), ('APPN-MIB', 'appnNnTopoTgPurges'), ('APPN-MIB', 'appnNnTopoTotalTduWars'), ('APPN-MIB', 'appnNnNodeFREntryTimeLeft'), ('APPN-MIB', 'appnNnNodeFRType'), ('APPN-MIB', 'appnNnNodeFRRsn'), ('APPN-MIB', 'appnNnNodeFRRouteAddResist'), ('APPN-MIB', 'appnNnNodeFRCongested'), ('APPN-MIB', 'appnNnNodeFRIsrDepleted'), ('APPN-MIB', 'appnNnNodeFRQuiescing'), ('APPN-MIB', 'appnNnNodeFRGateway'), ('APPN-MIB', 'appnNnNodeFRCentralDirectory'), ('APPN-MIB', 'appnNnNodeFRIsr'), ('APPN-MIB', 'appnNnNodeFRGarbageCollect'), ('APPN-MIB', 'appnNnNodeFRHprSupport'), ('APPN-MIB', 'appnNnNodeFRPeriBorderSup'), ('APPN-MIB', 'appnNnNodeFRInterchangeSup'), ('APPN-MIB', 'appnNnNodeFRExteBorderSup'), ('APPN-MIB', 'appnNnNodeFRBranchAwareness'), ('APPN-MIB', 'appnNnTgFREntryTimeLeft'), ('APPN-MIB', 'appnNnTgFRDestVirtual'), ('APPN-MIB', 'appnNnTgFRDlcData'), ('APPN-MIB', 'appnNnTgFRRsn'), ('APPN-MIB', 'appnNnTgFROperational'), ('APPN-MIB', 'appnNnTgFRQuiescing'), ('APPN-MIB', 'appnNnTgFRCpCpSession'), ('APPN-MIB', 'appnNnTgFREffCap'), ('APPN-MIB', 'appnNnTgFRConnCost'), ('APPN-MIB', 'appnNnTgFRByteCost'), ('APPN-MIB', 'appnNnTgFRSecurity'), ('APPN-MIB', 'appnNnTgFRDelay'), ('APPN-MIB', 'appnNnTgFRUsr1'), ('APPN-MIB', 'appnNnTgFRUsr2'), ('APPN-MIB', 'appnNnTgFRUsr3'), ('APPN-MIB', 'appnNnTgFRGarbageCollect'), ('APPN-MIB', 'appnNnTgFRSubareaNum'), ('APPN-MIB', 'appnNnTgFRHprSup'), ('APPN-MIB', 'appnNnTgFRDestHprTrans'), ('APPN-MIB', 'appnNnTgFRTypeIndicator'), ('APPN-MIB', 'appnNnTgFRIntersubnet'), ('APPN-MIB', 'appnNnTgFRMltgLinkType'), ('APPN-MIB', 'appnNnTgFRBranchTg')))
if mibBuilder.loadTexts:
    appnNnTopoConfGroup2.setDescription('The appnNnTopoConfGroup is mandatory only for network\n            nodes.')
appnLocalEnTopoConfGroup2 = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 31)).setObjects(*(('APPN-MIB', 'appnLocalEnTgEntryTimeLeft'), ('APPN-MIB', 'appnLocalEnTgDestVirtual'), ('APPN-MIB', 'appnLocalEnTgDlcData'), ('APPN-MIB', 'appnLocalEnTgOperational'), ('APPN-MIB', 'appnLocalEnTgCpCpSession'), ('APPN-MIB', 'appnLocalEnTgEffCap'), ('APPN-MIB', 'appnLocalEnTgConnCost'), ('APPN-MIB', 'appnLocalEnTgByteCost'), ('APPN-MIB', 'appnLocalEnTgSecurity'), ('APPN-MIB', 'appnLocalEnTgDelay'), ('APPN-MIB', 'appnLocalEnTgUsr1'), ('APPN-MIB', 'appnLocalEnTgUsr2'), ('APPN-MIB', 'appnLocalEnTgUsr3'), ('APPN-MIB', 'appnLocalEnTgMltgLinkType')))
if mibBuilder.loadTexts:
    appnLocalEnTopoConfGroup2.setDescription('A collection of objects providing the instrumentation\n            of the information that a network node possesses about\n            the end nodes directly attached to it.')
appnLocalDirPerfConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 11)).setObjects(*(('APPN-MIB', 'appnDirMaxCaches'), ('APPN-MIB', 'appnDirCurCaches'), ('APPN-MIB', 'appnDirCurHomeEntries'), ('APPN-MIB', 'appnDirRegEntries'), ('APPN-MIB', 'appnDirInLocates'), ('APPN-MIB', 'appnDirInBcastLocates'), ('APPN-MIB', 'appnDirOutLocates'), ('APPN-MIB', 'appnDirOutBcastLocates'), ('APPN-MIB', 'appnDirNotFoundLocates'), ('APPN-MIB', 'appnDirNotFoundBcastLocates'), ('APPN-MIB', 'appnDirLocateOutstands')))
if mibBuilder.loadTexts:
    appnLocalDirPerfConfGroup.setDescription('The appnLocalDirPerfConfGroup is mandatory only for APPN\n            network nodes and end nodes.')
appnCosConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 12)).setObjects(*(('APPN-MIB', 'appnCosModeCosName'), ('APPN-MIB', 'appnCosTransPriority'), ('APPN-MIB', 'appnCosNodeRowWgt'), ('APPN-MIB', 'appnCosNodeRowResistMin'), ('APPN-MIB', 'appnCosNodeRowResistMax'), ('APPN-MIB', 'appnCosNodeRowMinCongestAllow'), ('APPN-MIB', 'appnCosNodeRowMaxCongestAllow'), ('APPN-MIB', 'appnCosTgRowWgt'), ('APPN-MIB', 'appnCosTgRowEffCapMin'), ('APPN-MIB', 'appnCosTgRowEffCapMax'), ('APPN-MIB', 'appnCosTgRowConnCostMin'), ('APPN-MIB', 'appnCosTgRowConnCostMax'), ('APPN-MIB', 'appnCosTgRowByteCostMin'), ('APPN-MIB', 'appnCosTgRowByteCostMax'), ('APPN-MIB', 'appnCosTgRowSecurityMin'), ('APPN-MIB', 'appnCosTgRowSecurityMax'), ('APPN-MIB', 'appnCosTgRowDelayMin'), ('APPN-MIB', 'appnCosTgRowDelayMax'), ('APPN-MIB', 'appnCosTgRowUsr1Min'), ('APPN-MIB', 'appnCosTgRowUsr1Max'), ('APPN-MIB', 'appnCosTgRowUsr2Min'), ('APPN-MIB', 'appnCosTgRowUsr2Max'), ('APPN-MIB', 'appnCosTgRowUsr3Min'), ('APPN-MIB', 'appnCosTgRowUsr3Max')))
if mibBuilder.loadTexts:
    appnCosConfGroup.setDescription('The appnCosConfGroup is mandatory only for APPN network\n            nodes and end nodes.')
appnIntSessConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 13)).setObjects(*(('APPN-MIB', 'appnIsInGlobeCtrAdminStatus'), ('APPN-MIB', 'appnIsInGlobeCtrOperStatus'), ('APPN-MIB', 'appnIsInGlobeCtrStatusTime'), ('APPN-MIB', 'appnIsInGlobeRscv'), ('APPN-MIB', 'appnIsInGlobeRscvTime'), ('APPN-MIB', 'appnIsInGlobeActSess'), ('APPN-MIB', 'appnIsInSessState'), ('APPN-MIB', 'appnIsInPriLuName'), ('APPN-MIB', 'appnIsInSecLuName'), ('APPN-MIB', 'appnIsInModeName'), ('APPN-MIB', 'appnIsInCosName'), ('APPN-MIB', 'appnIsInTransPriority'), ('APPN-MIB', 'appnIsInSessType'), ('APPN-MIB', 'appnIsInSessUpTime'), ('APPN-MIB', 'appnIsInCtrUpTime'), ('APPN-MIB', 'appnIsInP2SFmdPius'), ('APPN-MIB', 'appnIsInS2PFmdPius'), ('APPN-MIB', 'appnIsInP2SNonFmdPius'), ('APPN-MIB', 'appnIsInS2PNonFmdPius'), ('APPN-MIB', 'appnIsInP2SFmdBytes'), ('APPN-MIB', 'appnIsInS2PFmdBytes'), ('APPN-MIB', 'appnIsInP2SNonFmdBytes'), ('APPN-MIB', 'appnIsInS2PNonFmdBytes'), ('APPN-MIB', 'appnIsInPsAdjCpName'), ('APPN-MIB', 'appnIsInPsAdjTgNum'), ('APPN-MIB', 'appnIsInPsSendMaxBtuSize'), ('APPN-MIB', 'appnIsInPsSendPacingType'), ('APPN-MIB', 'appnIsInPsSendRpc'), ('APPN-MIB', 'appnIsInPsSendNxWndwSize'), ('APPN-MIB', 'appnIsInPsRecvPacingType'), ('APPN-MIB', 'appnIsInPsRecvRpc'), ('APPN-MIB', 'appnIsInPsRecvNxWndwSize'), ('APPN-MIB', 'appnIsInSsAdjCpName'), ('APPN-MIB', 'appnIsInSsAdjTgNum'), ('APPN-MIB', 'appnIsInSsSendMaxBtuSize'), ('APPN-MIB', 'appnIsInSsSendPacingType'), ('APPN-MIB', 'appnIsInSsSendRpc'), ('APPN-MIB', 'appnIsInSsSendNxWndwSize'), ('APPN-MIB', 'appnIsInSsRecvPacingType'), ('APPN-MIB', 'appnIsInSsRecvRpc'), ('APPN-MIB', 'appnIsInSsRecvNxWndwSize'), ('APPN-MIB', 'appnIsInRouteInfo')))
if mibBuilder.loadTexts:
    appnIntSessConfGroup.setDescription('The appnIntSessConfGroup is mandatory only for network\n            nodes.')
appnHprBaseConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 14)).setObjects(*(('APPN-MIB', 'appnNodeHprIntRteSetups'), ('APPN-MIB', 'appnNodeHprIntRteRejects'), ('APPN-MIB', 'appnLsErrRecoSup'), ('APPN-MIB', 'appnLsForAnrLabel'), ('APPN-MIB', 'appnLsRevAnrLabel')))
if mibBuilder.loadTexts:
    appnHprBaseConfGroup.setDescription('The appnHprBaseConfGroup is mandatory only for nodes that\n            implement the HPR base (APPN option set 1400).')
appnHprRtpConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 15)).setObjects(*(('APPN-MIB', 'appnNodeMaxSessPerRtpConn'), ('APPN-MIB', 'appnNodeHprOrgRteSetups'), ('APPN-MIB', 'appnNodeHprOrgRteRejects'), ('APPN-MIB', 'appnNodeHprEndRteSetups'), ('APPN-MIB', 'appnNodeHprEndRteRejects'), ('APPN-MIB', 'appnLsBfNceId')))
if mibBuilder.loadTexts:
    appnHprRtpConfGroup.setDescription('The appnHprRtpConfGroup is mandatory only for nodes that\n            implement the HPR RTP tower (APPN option set 1401).')
appnHprCtrlFlowsRtpConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 16)).setObjects(*(('APPN-MIB', 'appnLsCpCpNceId'), ('APPN-MIB', 'appnLsRouteNceId')))
if mibBuilder.loadTexts:
    appnHprCtrlFlowsRtpConfGroup.setDescription('The appnHprCtrlFlowsRtpConfGroup is mandatory only for nodes\n            that implement the HPR Control Flows over RTP tower (APPN\n            option set 1402).')
appnHprBfConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 17)).setObjects(*(('APPN-MIB', 'appnIsInGlobeHprBfActSess'), ('APPN-MIB', 'appnIsInRtpNceId'), ('APPN-MIB', 'appnIsInRtpTcid'), ('APPN-MIB', 'appnIsRtpSessions')))
if mibBuilder.loadTexts:
    appnHprBfConfGroup.setDescription('The appnHprBfConfGroup is mandatory only for nodes that\n            implement the APPN/HPR boundary function.')
appnTrapConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 18)).setObjects(*(('APPN-MIB', 'alertIdNumber'), ('APPN-MIB', 'affectedObject')))
if mibBuilder.loadTexts:
    appnTrapConfGroup.setDescription('The appnTrapConfGroup is optional for all APPN nodes.  Nodes\n\n            implementing this group shall also implement the\n            appnTrapNotifGroup.')
appnTrapNotifGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 19)).setObjects(*(('APPN-MIB', 'alertTrap'),))
if mibBuilder.loadTexts:
    appnTrapNotifGroup.setDescription('The appnTrapNotifGroup is optional for all APPN nodes.\n            Nodes implementing this group shall also implement the\n            appnTrapConfGroup.')
appnBrNnConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 20)).setObjects(*(('APPN-MIB', 'appnNodeEnNnServer'), ('APPN-MIB', 'appnNodeEnLuSearch'), ('APPN-MIB', 'appnLocalTgBranchLinkType')))
if mibBuilder.loadTexts:
    appnBrNnConfGroup.setDescription('A collection of objects providing instrumentation for\n            branch network nodes.  Some of these objects also appear\n            in the instrumentation for an end node.\n\n            Note:  A branch network node always returns endNode(2)\n            as the value of the appnNodeType object from the\n            appnGeneralConfGroup2 conformance group.')
appnNodeMibVersion = MibScalar((1, 3, 6, 1, 2, 1, 34, 4, 1, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(11, 11)).setFixedLength(11)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    appnNodeMibVersion.setDescription("The value of LAST-UPDATED from this module's MODULE-IDENTITY\n          macro.  This object gives a Management Station an easy way of\n          determining the level of the MIB supported by an agent.\n\n          Since this object incorporates the Year 2000-unfriendly\n          2-digit year specified in SMI for the LAST-UPDATED field, and\n\n          since it was not found to be particularly useful, it has been\n          deprecated.  No replacement object has been defined.")
appnCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 34, 4, 3, 1, 1)).setObjects(*(('APPN-MIB', 'appnGeneralConfGroup'), ('APPN-MIB', 'appnPortConfGroup'), ('APPN-MIB', 'appnLinkConfGroup'), ('APPN-MIB', 'appnLocalTgConfGroup'), ('APPN-MIB', 'appnDirTableConfGroup'), ('APPN-MIB', 'appnNnUniqueConfGroup'), ('APPN-MIB', 'appnEnUniqueConfGroup'), ('APPN-MIB', 'appnVrnConfGroup'), ('APPN-MIB', 'appnNnTopoConfGroup'), ('APPN-MIB', 'appnLocalEnTopoConfGroup'), ('APPN-MIB', 'appnLocalDirPerfConfGroup'), ('APPN-MIB', 'appnCosConfGroup'), ('APPN-MIB', 'appnIntSessConfGroup'), ('APPN-MIB', 'appnHprBaseConfGroup'), ('APPN-MIB', 'appnHprRtpConfGroup'), ('APPN-MIB', 'appnHprCtrlFlowsRtpConfGroup'), ('APPN-MIB', 'appnHprBfConfGroup'), ('APPN-MIB', 'appnTrapConfGroup'), ('APPN-MIB', 'appnTrapNotifGroup')))
if mibBuilder.loadTexts:
    appnCompliance.setDescription('The compliance statement for the SNMPv2 entities that\n            implement the APPN MIB.\n\n            This is the compliance statement for the RFC 2155-level version\n            of the APPN MIB.  It was deprecated as new objects were added\n            to the MIB for MLTG, branch network node, and other extensions\n            to the APPN architecture.')
appnGeneralConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 1)).setObjects(*(('APPN-MIB', 'appnNodeCpName'), ('APPN-MIB', 'appnNodeMibVersion'), ('APPN-MIB', 'appnNodeId'), ('APPN-MIB', 'appnNodeType'), ('APPN-MIB', 'appnNodeUpTime'), ('APPN-MIB', 'appnNodeParallelTg'), ('APPN-MIB', 'appnNodeAdaptiveBindPacing'), ('APPN-MIB', 'appnNodeHprSupport'), ('APPN-MIB', 'appnNodeCounterDisconTime')))
if mibBuilder.loadTexts:
    appnGeneralConfGroup.setDescription('A collection of objects providing the instrumentation of\n            APPN general information and capabilities.\n\n            This RFC 2155-level group was deprecated when the\n            appnNodeMibVersion object was removed and the\n            appnNodeLsCounterType and appnNodeBrNn objects were added.')
appnLinkConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 3)).setObjects(*(('APPN-MIB', 'appnLsCommand'), ('APPN-MIB', 'appnLsOperState'), ('APPN-MIB', 'appnLsPortName'), ('APPN-MIB', 'appnLsDlcType'), ('APPN-MIB', 'appnLsDynamic'), ('APPN-MIB', 'appnLsAdjCpName'), ('APPN-MIB', 'appnLsAdjNodeType'), ('APPN-MIB', 'appnLsTgNum'), ('APPN-MIB', 'appnLsLimResource'), ('APPN-MIB', 'appnLsActOnDemand'), ('APPN-MIB', 'appnLsMigration'), ('APPN-MIB', 'appnLsPartnerNodeId'), ('APPN-MIB', 'appnLsCpCpSessionSupport'), ('APPN-MIB', 'appnLsMaxSendBtuSize'), ('APPN-MIB', 'appnLsInXidBytes'), ('APPN-MIB', 'appnLsInMsgBytes'), ('APPN-MIB', 'appnLsInXidFrames'), ('APPN-MIB', 'appnLsInMsgFrames'), ('APPN-MIB', 'appnLsOutXidBytes'), ('APPN-MIB', 'appnLsOutMsgBytes'), ('APPN-MIB', 'appnLsOutXidFrames'), ('APPN-MIB', 'appnLsOutMsgFrames'), ('APPN-MIB', 'appnLsEchoRsps'), ('APPN-MIB', 'appnLsCurrentDelay'), ('APPN-MIB', 'appnLsMaxDelay'), ('APPN-MIB', 'appnLsMinDelay'), ('APPN-MIB', 'appnLsMaxDelayTime'), ('APPN-MIB', 'appnLsGoodXids'), ('APPN-MIB', 'appnLsBadXids'), ('APPN-MIB', 'appnLsSpecific'), ('APPN-MIB', 'appnLsActiveTime'), ('APPN-MIB', 'appnLsCurrentStateTime'), ('APPN-MIB', 'appnLsHprSup'), ('APPN-MIB', 'appnLsLocalAddr'), ('APPN-MIB', 'appnLsRemoteAddr'), ('APPN-MIB', 'appnLsRemoteLsName'), ('APPN-MIB', 'appnLsStatusTime'), ('APPN-MIB', 'appnLsStatusLsName'), ('APPN-MIB', 'appnLsStatusCpName'), ('APPN-MIB', 'appnLsStatusPartnerId'), ('APPN-MIB', 'appnLsStatusTgNum'), ('APPN-MIB', 'appnLsStatusGeneralSense'), ('APPN-MIB', 'appnLsStatusRetry'), ('APPN-MIB', 'appnLsStatusEndSense'), ('APPN-MIB', 'appnLsStatusXidLocalSense'), ('APPN-MIB', 'appnLsStatusXidRemoteSense'), ('APPN-MIB', 'appnLsStatusXidByteInError'), ('APPN-MIB', 'appnLsStatusXidBitInError'), ('APPN-MIB', 'appnLsStatusDlcType'), ('APPN-MIB', 'appnLsStatusLocalAddr'), ('APPN-MIB', 'appnLsStatusRemoteAddr'), ('APPN-MIB', 'appnLsCounterDisconTime')))
if mibBuilder.loadTexts:
    appnLinkConfGroup.setDescription('A collection of objects providing the instrumentation of\n            APPN link information.\n\n            This RFC 2155-level group was deprecated when the\n            appnLsMltgMember object was added.')
appnLocalTgConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 4)).setObjects(*(('APPN-MIB', 'appnLocalTgDestVirtual'), ('APPN-MIB', 'appnLocalTgDlcData'), ('APPN-MIB', 'appnLocalTgPortName'), ('APPN-MIB', 'appnLocalTgQuiescing'), ('APPN-MIB', 'appnLocalTgOperational'), ('APPN-MIB', 'appnLocalTgCpCpSession'), ('APPN-MIB', 'appnLocalTgEffCap'), ('APPN-MIB', 'appnLocalTgConnCost'), ('APPN-MIB', 'appnLocalTgByteCost'), ('APPN-MIB', 'appnLocalTgSecurity'), ('APPN-MIB', 'appnLocalTgDelay'), ('APPN-MIB', 'appnLocalTgUsr1'), ('APPN-MIB', 'appnLocalTgUsr2'), ('APPN-MIB', 'appnLocalTgUsr3'), ('APPN-MIB', 'appnLocalTgHprSup'), ('APPN-MIB', 'appnLocalTgIntersubnet')))
if mibBuilder.loadTexts:
    appnLocalTgConfGroup.setDescription('A collection of objects providing the instrumentation of\n            APPN local TG information.\n\n            This RFC 2155-level group was deprecated when the\n            appnLocalTgMltgLinkType object was added.')
appnDirTableConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 5)).setObjects(*(('APPN-MIB', 'appnDirNnServerName'), ('APPN-MIB', 'appnDirLuOwnerName'), ('APPN-MIB', 'appnDirLuLocation'), ('APPN-MIB', 'appnDirType')))
if mibBuilder.loadTexts:
    appnDirTableConfGroup.setDescription('A collection of objects providing the instrumentation of the\n            APPN directory database.\n\n            This RFC 2155-level group was deprecated when the\n            appnDirApparentLuOwnerName object was added.')
appnNnTopoConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 9)).setObjects(*(('APPN-MIB', 'appnNnTopoMaxNodes'), ('APPN-MIB', 'appnNnTopoCurNumNodes'), ('APPN-MIB', 'appnNnTopoNodePurges'), ('APPN-MIB', 'appnNnTopoTgPurges'), ('APPN-MIB', 'appnNnTopoTotalTduWars'), ('APPN-MIB', 'appnNnNodeFREntryTimeLeft'), ('APPN-MIB', 'appnNnNodeFRType'), ('APPN-MIB', 'appnNnNodeFRRsn'), ('APPN-MIB', 'appnNnNodeFRRouteAddResist'), ('APPN-MIB', 'appnNnNodeFRCongested'), ('APPN-MIB', 'appnNnNodeFRIsrDepleted'), ('APPN-MIB', 'appnNnNodeFRQuiescing'), ('APPN-MIB', 'appnNnNodeFRGateway'), ('APPN-MIB', 'appnNnNodeFRCentralDirectory'), ('APPN-MIB', 'appnNnNodeFRIsr'), ('APPN-MIB', 'appnNnNodeFRGarbageCollect'), ('APPN-MIB', 'appnNnNodeFRHprSupport'), ('APPN-MIB', 'appnNnNodeFRPeriBorderSup'), ('APPN-MIB', 'appnNnNodeFRInterchangeSup'), ('APPN-MIB', 'appnNnNodeFRExteBorderSup'), ('APPN-MIB', 'appnNnTgFREntryTimeLeft'), ('APPN-MIB', 'appnNnTgFRDestVirtual'), ('APPN-MIB', 'appnNnTgFRDlcData'), ('APPN-MIB', 'appnNnTgFRRsn'), ('APPN-MIB', 'appnNnTgFROperational'), ('APPN-MIB', 'appnNnTgFRQuiescing'), ('APPN-MIB', 'appnNnTgFRCpCpSession'), ('APPN-MIB', 'appnNnTgFREffCap'), ('APPN-MIB', 'appnNnTgFRConnCost'), ('APPN-MIB', 'appnNnTgFRByteCost'), ('APPN-MIB', 'appnNnTgFRSecurity'), ('APPN-MIB', 'appnNnTgFRDelay'), ('APPN-MIB', 'appnNnTgFRUsr1'), ('APPN-MIB', 'appnNnTgFRUsr2'), ('APPN-MIB', 'appnNnTgFRUsr3'), ('APPN-MIB', 'appnNnTgFRGarbageCollect'), ('APPN-MIB', 'appnNnTgFRSubareaNum'), ('APPN-MIB', 'appnNnTgFRHprSup'), ('APPN-MIB', 'appnNnTgFRDestHprTrans'), ('APPN-MIB', 'appnNnTgFRTypeIndicator'), ('APPN-MIB', 'appnNnTgFRIntersubnet')))
if mibBuilder.loadTexts:
    appnNnTopoConfGroup.setDescription('The appnNnTopoConfGroup is mandatory only for network\n            nodes.\n\n            This RFC 2155-level group was deprecated when the\n            appnNnNodeFRBranchAwareness, appnNnTgFRMltgLinkType, and\n            appnNnFRBranchTg objects were added.')
appnLocalEnTopoConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 4, 3, 2, 10)).setObjects(*(('APPN-MIB', 'appnLocalEnTgEntryTimeLeft'), ('APPN-MIB', 'appnLocalEnTgDestVirtual'), ('APPN-MIB', 'appnLocalEnTgDlcData'), ('APPN-MIB', 'appnLocalEnTgOperational'), ('APPN-MIB', 'appnLocalEnTgCpCpSession'), ('APPN-MIB', 'appnLocalEnTgEffCap'), ('APPN-MIB', 'appnLocalEnTgConnCost'), ('APPN-MIB', 'appnLocalEnTgByteCost'), ('APPN-MIB', 'appnLocalEnTgSecurity'), ('APPN-MIB', 'appnLocalEnTgDelay'), ('APPN-MIB', 'appnLocalEnTgUsr1'), ('APPN-MIB', 'appnLocalEnTgUsr2'), ('APPN-MIB', 'appnLocalEnTgUsr3')))
if mibBuilder.loadTexts:
    appnLocalEnTopoConfGroup.setDescription('The appnLocalEnTopoConfGroup is mandatory only for network\n            nodes.\n\n            This RFC 2155-level group was deprecated when the\n            appnLocalEnTgMltgLinkType object was added.')
mibBuilder.exportSymbols('APPN-MIB', appnLsEntry=appnLsEntry, SnaNodeIdentification=SnaNodeIdentification, appnMIB=appnMIB, appnLocalEnTgUsr1=appnLocalEnTgUsr1, appnTrapNotifGroup=appnTrapNotifGroup, appnLsDynamic=appnLsDynamic, appnLocalTgBranchLinkType=appnLocalTgBranchLinkType, appnLsStatusIndex=appnLsStatusIndex, appnLsStatusRetry=appnLsStatusRetry, appnCosTgRowEntry=appnCosTgRowEntry, appnDirInLocates=appnDirInLocates, appnCompliance=appnCompliance, appnVrnTable=appnVrnTable, appnSessIntermediate=appnSessIntermediate, appnLsCounterDisconTime=appnLsCounterDisconTime, appnLocalTgNum=appnLocalTgNum, appnIsInSsRecvNxWndwSize=appnIsInSsRecvNxWndwSize, appnNnTopologyFRTable=appnNnTopologyFRTable, appnIsInCtrUpTime=appnIsInCtrUpTime, appnIsInP2SNonFmdBytes=appnIsInP2SNonFmdBytes, appnLsStatusXidRemoteSense=appnLsStatusXidRemoteSense, appnLocalTgDest=appnLocalTgDest, appnIsInPsRecvNxWndwSize=appnIsInPsRecvNxWndwSize, PYSNMP_MODULE_ID=appnMIB, appnVrnTgNum=appnVrnTgNum, appnNnTopologyFREntry=appnNnTopologyFREntry, appnLsStatusDlcType=appnLsStatusDlcType, AppnNodeCounter=AppnNodeCounter, appnDirLuLocation=appnDirLuLocation, appnNodeType=appnNodeType, appnCosNodeRowName=appnCosNodeRowName, appnNodeHprIntRteRejects=appnNodeHprIntRteRejects, AppnTgEffectiveCapacity=AppnTgEffectiveCapacity, appnLocalTgByteCost=appnLocalTgByteCost, appnLsStatusTime=appnLsStatusTime, appnLocalTgUsr3=appnLocalTgUsr3, appnLsCurrentDelay=appnLsCurrentDelay, appnNnTgTopologyFRTable=appnNnTgTopologyFRTable, appnLocalEnTgEntry=appnLocalEnTgEntry, appnCosTgRowUsr2Min=appnCosTgRowUsr2Min, appnGeneralInfoAndCaps=appnGeneralInfoAndCaps, appnDirLuOwnerName=appnDirLuOwnerName, appnLocalTgCpCpSession=appnLocalTgCpCpSession, AppnTopologyEntryTimeLeft=AppnTopologyEntryTimeLeft, appnLsRouteNceId=appnLsRouteNceId, appnLsErrRecoSup=appnLsErrRecoSup, appnIsInSsSendRpc=appnIsInSsSendRpc, appnPortInformation=appnPortInformation, appnLocalEnTgDest=appnLocalEnTgDest, appnLsRemoteLsName=appnLsRemoteLsName, appnLocalTgDelay=appnLocalTgDelay, appnHprCtrlFlowsRtpConfGroup=appnHprCtrlFlowsRtpConfGroup, appnObjects=appnObjects, appnNnTgFRTypeIndicator=appnNnTgFRTypeIndicator, appnLsStatusXidBitInError=appnLsStatusXidBitInError, appnPortTable=appnPortTable, appnNnNodeFRRouteAddResist=appnNnNodeFRRouteAddResist, appnLocalEnTgOrigin=appnLocalEnTgOrigin, appnCosTgRowTable=appnCosTgRowTable, appnDirCurHomeEntries=appnDirCurHomeEntries, appnNnUniqueConfGroup=appnNnUniqueConfGroup, appnLocalTgDlcData=appnLocalTgDlcData, appnLocalEnTgSecurity=appnLocalEnTgSecurity, appnCosModeEntry=appnCosModeEntry, appnLsMinDelay=appnLsMinDelay, appnGeneralConfGroup2=appnGeneralConfGroup2, appnLsForAnrLabel=appnLsForAnrLabel, appnNn=appnNn, appnCosTgRowConnCostMax=appnCosTgRowConnCostMax, appnNodeNnPeriBorderSup=appnNodeNnPeriBorderSup, appnLocalTgConfGroup=appnLocalTgConfGroup, appnNnNodeFRGarbageCollect=appnNnNodeFRGarbageCollect, appnNodeNnExteBorderSup=appnNodeNnExteBorderSup, appnNodeAdaptiveBindPacing=appnNodeAdaptiveBindPacing, appnNnNodeFRGateway=appnNnNodeFRGateway, appnLinkStationInformation=appnLinkStationInformation, appnLocalEnTgEffCap=appnLocalEnTgEffCap, appnNnTgFRRsn=appnNnTgFRRsn, appnNnUniqueInfoAndCaps=appnNnUniqueInfoAndCaps, appnLsActOnDemand=appnLsActOnDemand, appnLocalTgDestVirtual=appnLocalTgDestVirtual, affectedObject=affectedObject, appnCosTgRowIndex=appnCosTgRowIndex, AppnPortCounter=AppnPortCounter, appnNnTgFRUsr2=appnNnTgFRUsr2, appnLsLimResource=appnLsLimResource, appnLocalEnTgByteCost=appnLocalEnTgByteCost, appnLocalTgTable=appnLocalTgTable, appnNnNodeFRInterchangeSup=appnNnNodeFRInterchangeSup, appnCosNodeRowResistMin=appnCosNodeRowResistMin, appnNnTopo=appnNnTopo, appnNnTgFRGarbageCollect=appnNnTgFRGarbageCollect, appnDirEntry=appnDirEntry, appnLsGoodXids=appnLsGoodXids, appnLocalDirPerfConfGroup=appnLocalDirPerfConfGroup, appnPortDlcLocalAddr=appnPortDlcLocalAddr, appnIsInFqCpName=appnIsInFqCpName, appnLocalEnTgEntryTimeLeft=appnLocalEnTgEntryTimeLeft, appnHprRtpConfGroup=appnHprRtpConfGroup, appnLsStatusEndSense=appnLsStatusEndSense, appnLsMaxDelay=appnLsMaxDelay, appnNnTopoCurNumNodes=appnNnTopoCurNumNodes, appnBrNnConfGroup=appnBrNnConfGroup, appnNnTgFROperational=appnNnTgFROperational, appnCosNodeRowMaxCongestAllow=appnCosNodeRowMaxCongestAllow, appnIsRtpNceId=appnIsRtpNceId, appnLsBadXids=appnLsBadXids, appnCosNodeRowResistMax=appnCosNodeRowResistMax, appnNnTgFRQuiescing=appnNnTgFRQuiescing, appnIsInSecLuName=appnIsInSecLuName, appnNnNodeFRCongested=appnNnNodeFRCongested, appnLinkConfGroup=appnLinkConfGroup, appnIsInTransPriority=appnIsInTransPriority, appnVrnPortName=appnVrnPortName, appnDirRegEntries=appnDirRegEntries, appnNodeNnIsr=appnNodeNnIsr, appnIsInPsSendMaxBtuSize=appnIsInPsSendMaxBtuSize, alertIdNumber=alertIdNumber, appnNodeParallelTg=appnNodeParallelTg, appnDirApparentLuOwnerName=appnDirApparentLuOwnerName, appnNnNodeFRType=appnNnNodeFRType, appnNodeNnCentralDirectory=appnNodeNnCentralDirectory, appnDirMaxCaches=appnDirMaxCaches, appnPortCounterDisconTime=appnPortCounterDisconTime, appnLocalEnTgDestVirtual=appnLocalEnTgDestVirtual, appnNodeNnTreeCache=appnNodeNnTreeCache, appnCosTgRowEffCapMax=appnCosTgRowEffCapMax, appnLsStatusLocalAddr=appnLsStatusLocalAddr, appnLsStatusPartnerId=appnLsStatusPartnerId, appnLocalEnTgUsr3=appnLocalEnTgUsr3, appnNnTopology=appnNnTopology, appnNnTopoConfGroup2=appnNnTopoConfGroup2, appnNode=appnNode, appnLsInXidBytes=appnLsInXidBytes, appnDirNotFoundLocates=appnDirNotFoundLocates, AppnTgDelay=AppnTgDelay, appnLocalTgHprSup=appnLocalTgHprSup, appnLsStatusXidByteInError=appnLsStatusXidByteInError, appnLocalTgUsr1=appnLocalTgUsr1, appnNnNodeFREntryTimeLeft=appnNnNodeFREntryTimeLeft, appnIsInS2PFmdPius=appnIsInS2PFmdPius, appnTraps=appnTraps, appnNodeNnInterchangeSup=appnNodeNnInterchangeSup, appnLsRevAnrLabel=appnLsRevAnrLabel, appnLsMltgMember=appnLsMltgMember, appnDirTable=appnDirTable, appnIsInPriLuName=appnIsInPriLuName, AppnTgSecurity=AppnTgSecurity, appnPortDynLsBadXids=appnPortDynLsBadXids, appnNnTgFRDestHprTrans=appnNnTgFRDestHprTrans, appnIsRtpTcid=appnIsRtpTcid, appnCosNameEntry=appnCosNameEntry, appnLocalTgOperational=appnLocalTgOperational, appnIsRtpEntry=appnIsRtpEntry, appnLsOutMsgBytes=appnLsOutMsgBytes, appnIsInSessState=appnIsInSessState, appnVrnEntry=appnVrnEntry, appnNnTopoNodePurges=appnNnTopoNodePurges, appnLsLocalAddr=appnLsLocalAddr, appnNodeEnLuSearch=appnNodeEnLuSearch, appnVrnConfGroup=appnVrnConfGroup, appnNnNodeFRRsn=appnNnNodeFRRsn, appnVrnInfo=appnVrnInfo, appnNodeId=appnNodeId, appnLsInMsgBytes=appnLsInMsgBytes, appnCosNodeRowWgt=appnCosNodeRowWgt, appnNnTgFRByteCost=appnNnTgFRByteCost, appnNnTgFRIntersubnet=appnNnTgFRIntersubnet, appnIsInPsRecvRpc=appnIsInPsRecvRpc, appnIsInPsSendNxWndwSize=appnIsInPsSendNxWndwSize, appnPortSIMRIM=appnPortSIMRIM, SnaClassOfServiceName=SnaClassOfServiceName, appnLsCpCpSessionSupport=appnLsCpCpSessionSupport, appnLocalTopology=appnLocalTopology, AppnLinkStationCounter=AppnLinkStationCounter, appnLsMaxDelayTime=appnLsMaxDelayTime, appnCosTgRowDelayMax=appnCosTgRowDelayMax, appnNodeLsCounterType=appnNodeLsCounterType, appnPortDynamicLinkSupport=appnPortDynamicLinkSupport, appnNodeNnQuiescing=appnNodeNnQuiescing, appnLocalEnTgConnCost=appnLocalEnTgConnCost, appnLsTgNum=appnLsTgNum, appnIsInTable=appnIsInTable, appnPortCommand=appnPortCommand, appnLsCommand=appnLsCommand, appnGroups=appnGroups, appnLocalEnTgOperational=appnLocalEnTgOperational, appnPortName=appnPortName, appnPortDlcType=appnPortDlcType, appnIsInS2PFmdBytes=appnIsInS2PFmdBytes, appnIsInRtpNceId=appnIsInRtpNceId, appnNodeHprEndRteSetups=appnNodeHprEndRteSetups, appnNnTgFROwner=appnNnTgFROwner, appnNnTgFREntryTimeLeft=appnNnTgFREntryTimeLeft, appnNnTgTopologyFREntry=appnNnTgTopologyFREntry, appnLsStatusGeneralSense=appnLsStatusGeneralSense, appnIsInP2SNonFmdPius=appnIsInP2SNonFmdPius, appnPortDynLsGoodXids=appnPortDynLsGoodXids, appnNnTgFRCpCpSession=appnNnTgFRCpCpSession, appnCosTgRowWgt=appnCosTgRowWgt, appnNnTopoConfGroup=appnNnTopoConfGroup, appnPortDefLsGoodXids=appnPortDefLsGoodXids, appnNodeMaxSessPerRtpConn=appnNodeMaxSessPerRtpConn, appnNnTgFRSubareaNum=appnNnTgFRSubareaNum, appnNnNodeFRName=appnNnNodeFRName, appnIsInSsAdjCpName=appnIsInSsAdjCpName, appnIsInEntry=appnIsInEntry, appnLsCpCpNceId=appnLsCpCpNceId, appnNodeEnModeCosMap=appnNodeEnModeCosMap, appnLsAdjCpName=appnLsAdjCpName, appnNnNodeFRExteBorderSup=appnNnNodeFRExteBorderSup, appnDirOutBcastLocates=appnDirOutBcastLocates, appnLocalEnTgCpCpSession=appnLocalEnTgCpCpSession, appnLsStatusTgNum=appnLsStatusTgNum, appnPortNegotLs=appnPortNegotLs, appnLocalTgQuiescing=appnLocalTgQuiescing, appnIsInPcid=appnIsInPcid, appnPortEntry=appnPortEntry, appnDirInBcastLocates=appnDirInBcastLocates, appnCosModeTable=appnCosModeTable, appnDirOutLocates=appnDirOutLocates, appnLsInMsgFrames=appnLsInMsgFrames, appnLsBfNceId=appnLsBfNceId, appnCompliance2=appnCompliance2, appnNodeNnIsrDepleted=appnNodeNnIsrDepleted, appnNnTgFRDest=appnNnTgFRDest, appnLsOutXidFrames=appnLsOutXidFrames, appnLsDlcType=appnLsDlcType, appnCosNodeRowIndex=appnCosNodeRowIndex, SnaModeName=SnaModeName, appnNodeNnRsn=appnNodeNnRsn, appnHprBfConfGroup=appnHprBfConfGroup, appnDirPerf=appnDirPerf, appnIsInSsAdjTgNum=appnIsInSsAdjTgNum, appnIsInSsRecvRpc=appnIsInSsRecvRpc, appnCosNodeRowMinCongestAllow=appnCosNodeRowMinCongestAllow, alertTrap=alertTrap, appnDir=appnDir, appnDirLuName=appnDirLuName, appnCosNodeRowEntry=appnCosNodeRowEntry, appnIsInS2PNonFmdBytes=appnIsInS2PNonFmdBytes, appnNnTgFRUsr1=appnNnTgFRUsr1, appnIsInSsRecvPacingType=appnIsInSsRecvPacingType, appnNnNodeFRFrsn=appnNnNodeFRFrsn, appnCosTgRowEffCapMin=appnCosTgRowEffCapMin, appnNnTgFRBranchTg=appnNnTgFRBranchTg, appnNnNodeFRIsrDepleted=appnNnNodeFRIsrDepleted, appnNnTgFRFrsn=appnNnTgFRFrsn, appnLsInXidFrames=appnLsInXidFrames, appnNodeHprIntRteSetups=appnNodeHprIntRteSetups, appnIsInGlobeActSess=appnIsInGlobeActSess, appnEnUniqueCaps=appnEnUniqueCaps, appnCosTgRowByteCostMin=appnCosTgRowByteCostMin, appnGeneralConfGroup=appnGeneralConfGroup)
mibBuilder.exportSymbols('APPN-MIB', appnLsStatusXidLocalSense=appnLsStatusXidLocalSense, appnCosNodeRowTable=appnCosNodeRowTable, appnLocalTgConnCost=appnLocalTgConnCost, appnNnNodeFRQuiescing=appnNnNodeFRQuiescing, appnLocalTgSecurity=appnLocalTgSecurity, appnLocalTgEffCap=appnLocalTgEffCap, appnNnTgFRHprSup=appnNnTgFRHprSup, appnLsStatusCpName=appnLsStatusCpName, appnNnNodeFRIsr=appnNnNodeFRIsr, appnDirType=appnDirType, appnLsActiveTime=appnLsActiveTime, appnLsStatusEntry=appnLsStatusEntry, appnNnTgFRDelay=appnNnTgFRDelay, appnDirNnServerName=appnDirNnServerName, appnCosTransPriority=appnCosTransPriority, appnNodeHprOrgRteRejects=appnNodeHprOrgRteRejects, appnNodeNnRouteAddResist=appnNodeNnRouteAddResist, appnLocalEnTgMltgLinkType=appnLocalEnTgMltgLinkType, appnPortMaxRcvBtuSize=appnPortMaxRcvBtuSize, appnNodeCounterDisconTime=appnNodeCounterDisconTime, appnIsInSsSendPacingType=appnIsInSsSendPacingType, appnCompliances=appnCompliances, appnCosTgRowDelayMin=appnCosTgRowDelayMin, appnNnTgFRMltgLinkType=appnNnTgFRMltgLinkType, appnNodeNnCongested=appnNodeNnCongested, appnLocalEnTopoConfGroup=appnLocalEnTopoConfGroup, appnIntSessConfGroup=appnIntSessConfGroup, appnDirLocateOutstands=appnDirLocateOutstands, appnLsStatusTable=appnLsStatusTable, appnDirNotFoundBcastLocates=appnDirNotFoundBcastLocates, appnNnTgFRDlcData=appnNnTgFRDlcData, appnLsOutMsgFrames=appnLsOutMsgFrames, appnPortPortType=appnPortPortType, appnNnTgFRSecurity=appnNnTgFRSecurity, appnLsAdjNodeType=appnLsAdjNodeType, appnCosTgRowConnCostMin=appnCosTgRowConnCostMin, appnLocalEnTgNum=appnLocalEnTgNum, appnPortConfGroup=appnPortConfGroup, appnLsEchoRsps=appnLsEchoRsps, appnIsRtpTable=appnIsRtpTable, appnIsRtpSessions=appnIsRtpSessions, appnCosTgRowUsr3Min=appnCosTgRowUsr3Min, appnNnTopoMaxNodes=appnNnTopoMaxNodes, appnIsInSessUpTime=appnIsInSessUpTime, appnIsInSessType=appnIsInSessType, appnNnNodeFRPeriBorderSup=appnNnNodeFRPeriBorderSup, appnIsInP2SFmdPius=appnIsInP2SFmdPius, appnIsInGlobeCtrAdminStatus=appnIsInGlobeCtrAdminStatus, appnVrnName=appnVrnName, appnNodeHprEndRteRejects=appnNodeHprEndRteRejects, appnCosModeCosName=appnCosModeCosName, appnCosConfGroup=appnCosConfGroup, appnLsCurrentStateTime=appnLsCurrentStateTime, appnLocalTgIntersubnet=appnLocalTgIntersubnet, appnIsInPsSendRpc=appnIsInPsSendRpc, appnPortOperState=appnPortOperState, appnIsInGlobeRscvTime=appnIsInGlobeRscvTime, appnIsInPsAdjTgNum=appnIsInPsAdjTgNum, appnIsInP2SFmdBytes=appnIsInP2SFmdBytes, appnNodeNnGateway=appnNodeNnGateway, appnIsInPsRecvPacingType=appnIsInPsRecvPacingType, appnLsOperState=appnLsOperState, appnNodeHprOrgRteSetups=appnNodeHprOrgRteSetups, appnHprBaseConfGroup=appnHprBaseConfGroup, appnPortLsRole=appnPortLsRole, appnLsName=appnLsName, SnaControlPointName=SnaControlPointName, appnCosTgRowUsr2Max=appnCosTgRowUsr2Max, appnLocalEnTgTable=appnLocalEnTgTable, appnNnTgFREffCap=appnNnTgFREffCap, appnLsSpecific=appnLsSpecific, appnLsTable=appnLsTable, appnCos=appnCos, appnTrapConfGroup=appnTrapConfGroup, appnNodeMibVersion=appnNodeMibVersion, appnLsOutXidBytes=appnLsOutXidBytes, appnNnNodeFRBranchAwareness=appnNnNodeFRBranchAwareness, appnLocalTgUsr2=appnLocalTgUsr2, appnIsInPsSendPacingType=appnIsInPsSendPacingType, appnLsMigration=appnLsMigration, appnNodeUpTime=appnNodeUpTime, appnLocalEnTopoConfGroup2=appnLocalEnTopoConfGroup2, appnIsInGlobeHprBfActSess=appnIsInGlobeHprBfActSess, SnaSenseData=SnaSenseData, appnLocalEnTgDlcData=appnLocalEnTgDlcData, appnLocalTgConfGroup2=appnLocalTgConfGroup2, appnIsInRtpTcid=appnIsInRtpTcid, appnLsMaxSendBtuSize=appnLsMaxSendBtuSize, appnLocalEnTgDelay=appnLocalEnTgDelay, appnCosTgRowSecurityMin=appnCosTgRowSecurityMin, appnPortDefLsBadXids=appnPortDefLsBadXids, appnLocalTgPortName=appnLocalTgPortName, appnIsInS2PNonFmdPius=appnIsInS2PNonFmdPius, appnNnTgFRUsr3=appnNnTgFRUsr3, appnCosTgRowUsr1Min=appnCosTgRowUsr1Min, appnIsInCosName=appnIsInCosName, appnIsInGlobeCtrStatusTime=appnIsInGlobeCtrStatusTime, appnLinkConfGroup2=appnLinkConfGroup2, appnCosTgRowName=appnCosTgRowName, appnDirCurCaches=appnDirCurCaches, appnNodeCpName=appnNodeCpName, appnIsInPsAdjCpName=appnIsInPsAdjCpName, appnLsHprSup=appnLsHprSup, appnDirTableConfGroup2=appnDirTableConfGroup2, appnNodeEnNnServer=appnNodeEnNnServer, appnLocalEnTgUsr2=appnLocalEnTgUsr2, appnCosModeName=appnCosModeName, appnCosTgRowByteCostMax=appnCosTgRowByteCostMax, appnIsInSsSendNxWndwSize=appnIsInSsSendNxWndwSize, appnCosName=appnCosName, appnPortMaxIframeWindow=appnPortMaxIframeWindow, appnIsInSsSendMaxBtuSize=appnIsInSsSendMaxBtuSize, appnLsPartnerNodeId=appnLsPartnerNodeId, appnIsInModeName=appnIsInModeName, appnNodeHprSupport=appnNodeHprSupport, appnLsStatusLsName=appnLsStatusLsName, appnLocalTgEntry=appnLocalTgEntry, appnNnNodeFRHprSupport=appnNnNodeFRHprSupport, appnNodeNnSafeStoreFreq=appnNodeNnSafeStoreFreq, AppnTgDlcData=AppnTgDlcData, appnLocalTgMltgLinkType=appnLocalTgMltgLinkType, appnCosTgRowUsr1Max=appnCosTgRowUsr1Max, appnConformance=appnConformance, appnNnTgFRConnCost=appnNnTgFRConnCost, appnNnTopoTgPurges=appnNnTopoTgPurges, appnNodeBrNn=appnNodeBrNn, appnNnTgFRDestVirtual=appnNnTgFRDestVirtual, appnEnUniqueConfGroup=appnEnUniqueConfGroup, appnLsStatusRemoteAddr=appnLsStatusRemoteAddr, appnNodeNnFrsn=appnNodeNnFrsn, appnNnNodeFRCentralDirectory=appnNnNodeFRCentralDirectory, DisplayableDlcAddress=DisplayableDlcAddress, appnPortSpecific=appnPortSpecific, appnIsInGlobeCtrOperStatus=appnIsInGlobeCtrOperStatus, appnIsInGlobeRscv=appnIsInGlobeRscv, appnCosNameTable=appnCosNameTable, appnCosTgRowSecurityMax=appnCosTgRowSecurityMax, appnDirTableConfGroup=appnDirTableConfGroup, appnIsInRouteInfo=appnIsInRouteInfo, appnLsPortName=appnLsPortName, appnNnTopoTotalTduWars=appnNnTopoTotalTduWars, appnLsRemoteAddr=appnLsRemoteAddr, appnIsInGlobal=appnIsInGlobal, appnNnTgFRNum=appnNnTgFRNum, appnCosTgRowUsr3Max=appnCosTgRowUsr3Max)