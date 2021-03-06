# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/Printer-MIB.py
# Compiled at: 2016-02-13 18:12:48
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, ValueRangeConstraint, SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'ValueRangeConstraint', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection')
(hrStorageIndex, hrDeviceIndex) = mibBuilder.importSymbols('HOST-RESOURCES-MIB', 'hrStorageIndex', 'hrDeviceIndex')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(Bits, ModuleIdentity, Counter32, IpAddress, Unsigned32, MibIdentifier, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, mib_2, NotificationType, Counter64, TimeTicks, Gauge32, Integer32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Bits', 'ModuleIdentity', 'Counter32', 'IpAddress', 'Unsigned32', 'MibIdentifier', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'iso', 'mib-2', 'NotificationType', 'Counter64', 'TimeTicks', 'Gauge32', 'Integer32')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
printmib = ModuleIdentity((1, 3, 6, 1, 2, 1, 43))
if mibBuilder.loadTexts:
    printmib.setLastUpdated('9810070000Z')
if mibBuilder.loadTexts:
    printmib.setOrganization('IETF Printer MIB Working Group')
if mibBuilder.loadTexts:
    printmib.setContactInfo('Randy Turner\n           Sharp Laboratories of America\n           5750 NW Pacific Rim Blvd\n           Camas, WA 98607\n           rturner@sharplabs.com')
if mibBuilder.loadTexts:
    printmib.setDescription('The MIB module for management of printers.')

class PrtMediaUnitTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4))
    namedValues = NamedValues(('tenThousandthsOfInches', 3), ('micrometers', 4))


class PrtCapacityUnitTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4, 8, 16, 17))
    namedValues = NamedValues(('tenThousandthsOfInches', 3), ('micrometers', 4), ('sheets',
                                                                                  8), ('feet',
                                                                                       16), ('meters',
                                                                                             17))


class PrtPrintOrientationTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4))
    namedValues = NamedValues(('other', 1), ('portrait', 3), ('landscape', 4))


class PrtCoverStatusTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4, 5, 6))
    namedValues = NamedValues(('other', 1), ('coverOpen', 3), ('coverClosed', 4), ('interlockOpen',
                                                                                   5), ('interlockClosed',
                                                                                        6))


class PrtSubUnitStatusTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 126)


class PresentOnOff(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4, 5))
    namedValues = NamedValues(('other', 1), ('on', 3), ('off', 4), ('notPresent', 5))


class CodedCharSet(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1))
    namedValues = NamedValues(('other', 1))


class PrtGeneralResetTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4, 5, 6))
    namedValues = NamedValues(('notResetting', 3), ('powerCycleReset', 4), ('resetToNVRAM',
                                                                            5), ('resetToFactoryDefaults',
                                                                                 6))


class PrtChannelStateTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4))
    namedValues = NamedValues(('other', 1), ('printDataAccepted', 3), ('noDataAccepted',
                                                                       4))


class PrtChannelTypeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43))
    namedValues = NamedValues(('other', 1), ('chSerialPort', 3), ('chParallelPort',
                                                                  4), ('chIEEE1284Port',
                                                                       5), ('chSCSIPort',
                                                                            6), ('chAppleTalkPAP',
                                                                                 7), ('chLPDServer',
                                                                                      8), ('chNetwareRPrinter',
                                                                                           9), ('chNetwarePServer',
                                                                                                10), ('chPort9100',
                                                                                                      11), ('chAppSocket',
                                                                                                            12), ('chFTP',
                                                                                                                  13), ('chTFTP',
                                                                                                                        14), ('chDLCLLCPort',
                                                                                                                              15), ('chIBM3270',
                                                                                                                                    16), ('chIBM5250',
                                                                                                                                          17), ('chFax',
                                                                                                                                                18), ('chIEEE1394',
                                                                                                                                                      19), ('chTransport1',
                                                                                                                                                            20), ('chCPAP',
                                                                                                                                                                  21), ('chPCPrint',
                                                                                                                                                                        26), ('chServerMessageBlock',
                                                                                                                                                                              27), ('chPSM',
                                                                                                                                                                                    28), ('chSystemObjectManager',
                                                                                                                                                                                          31), ('chDECLAT',
                                                                                                                                                                                                32), ('chNPAP',
                                                                                                                                                                                                      33), ('chUSB',
                                                                                                                                                                                                            34), ('chIRDA',
                                                                                                                                                                                                                  35), ('chPrintXChange',
                                                                                                                                                                                                                        36), ('chPortTCP',
                                                                                                                                                                                                                              37), ('chBidirPortTCP',
                                                                                                                                                                                                                                    38), ('chUNPP',
                                                                                                                                                                                                                                          39), ('chAppleTalkADSP',
                                                                                                                                                                                                                                                40), ('chPortSPX',
                                                                                                                                                                                                                                                      41), ('chPortHTTP',
                                                                                                                                                                                                                                                            42), ('chNDPS',
                                                                                                                                                                                                                                                                  43))


class PrtInterpreterLangFamilyTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('langPCL', 3), ('langHPGL',
                                                                             4), ('langPJL',
                                                                                  5), ('langPS',
                                                                                       6), ('langIPDS',
                                                                                            7), ('langPPDS',
                                                                                                 8), ('langEscapeP',
                                                                                                      9), ('langEpson',
                                                                                                           10), ('langDDIF',
                                                                                                                 11), ('langInterpress',
                                                                                                                       12), ('langISO6429',
                                                                                                                             13), ('langLineData',
                                                                                                                                   14), ('langMODCA',
                                                                                                                                         15), ('langREGIS',
                                                                                                                                               16), ('langSCS',
                                                                                                                                                     17), ('langSPDL',
                                                                                                                                                           18), ('langTEK4014',
                                                                                                                                                                 19), ('langPDS',
                                                                                                                                                                       20), ('langIGP',
                                                                                                                                                                             21), ('langCodeV',
                                                                                                                                                                                   22), ('langDSCDSE',
                                                                                                                                                                                         23), ('langWPS',
                                                                                                                                                                                               24), ('langLN03',
                                                                                                                                                                                                     25), ('langCCITT',
                                                                                                                                                                                                           26), ('langQUIC',
                                                                                                                                                                                                                 27), ('langCPAP',
                                                                                                                                                                                                                       28), ('langDecPPL',
                                                                                                                                                                                                                             29), ('langSimpleText',
                                                                                                                                                                                                                                   30), ('langNPAP',
                                                                                                                                                                                                                                         31), ('langDOC',
                                                                                                                                                                                                                                               32), ('langimPress',
                                                                                                                                                                                                                                                     33), ('langPinwriter',
                                                                                                                                                                                                                                                           34), ('langNPDL',
                                                                                                                                                                                                                                                                 35), ('langNEC201PL',
                                                                                                                                                                                                                                                                       36), ('langAutomatic',
                                                                                                                                                                                                                                                                             37), ('langPages',
                                                                                                                                                                                                                                                                                   38), ('langLIPS',
                                                                                                                                                                                                                                                                                         39), ('langTIFF',
                                                                                                                                                                                                                                                                                               40), ('langDiagnostic',
                                                                                                                                                                                                                                                                                                     41), ('langPSPrinter',
                                                                                                                                                                                                                                                                                                           42), ('langCaPSL',
                                                                                                                                                                                                                                                                                                                 43), ('langEXCL',
                                                                                                                                                                                                                                                                                                                       44), ('langLCDS',
                                                                                                                                                                                                                                                                                                                             45), ('langXES',
                                                                                                                                                                                                                                                                                                                                   46), ('langPCLXL',
                                                                                                                                                                                                                                                                                                                                         47), ('langART',
                                                                                                                                                                                                                                                                                                                                               48), ('langTIPSI',
                                                                                                                                                                                                                                                                                                                                                     49), ('langPrescribe',
                                                                                                                                                                                                                                                                                                                                                           50), ('langLinePrinter',
                                                                                                                                                                                                                                                                                                                                                                 51), ('langIDP',
                                                                                                                                                                                                                                                                                                                                                                       52), ('langXJCL',
                                                                                                                                                                                                                                                                                                                                                                             53), ('langPDF',
                                                                                                                                                                                                                                                                                                                                                                                   54), ('langRPDL',
                                                                                                                                                                                                                                                                                                                                                                                         55), ('langIntermecIPL',
                                                                                                                                                                                                                                                                                                                                                                                               56), ('langUBIFingerprint',
                                                                                                                                                                                                                                                                                                                                                                                                     57), ('langUBIDirectProtocol',
                                                                                                                                                                                                                                                                                                                                                                                                           58), ('langFujitsu',
                                                                                                                                                                                                                                                                                                                                                                                                                 59))


class PrtInputTypeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('sheetFeedAutoRemovableTray',
                                                             3), ('sheetFeedAutoNonRemovableTray',
                                                                  4), ('sheetFeedManual',
                                                                       5), ('continuousRoll',
                                                                            6), ('continuousFanFold',
                                                                                 7))


class PrtOutputTypeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('removableBin', 3), ('unRemovableBin',
                                                                                  4), ('continuousRollDevice',
                                                                                       5), ('mailBox',
                                                                                            6), ('continuousFanFold',
                                                                                                 7))


class PrtOutputStackingOrderTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(2, 3, 4))
    namedValues = NamedValues(('unknown', 2), ('firstToLast', 3), ('lastToFirst', 4))


class PrtOutputPageDeliveryOrientationTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4))
    namedValues = NamedValues(('faceUp', 3), ('faceDown', 4))


class PrtMarkerMarkTechTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('electrophotographicLED',
                                                             3), ('electrophotographicLaser',
                                                                  4), ('electrophotographicOther',
                                                                       5), ('impactMovingHeadDotMatrix9pin',
                                                                            6), ('impactMovingHeadDotMatrix24pin',
                                                                                 7), ('impactMovingHeadDotMatrixOther',
                                                                                      8), ('impactMovingHeadFullyFormed',
                                                                                           9), ('impactBand',
                                                                                                10), ('impactOther',
                                                                                                      11), ('inkjetAqueous',
                                                                                                            12), ('inkjetSolid',
                                                                                                                  13), ('inkjetOther',
                                                                                                                        14), ('pen',
                                                                                                                              15), ('thermalTransfer',
                                                                                                                                    16), ('thermalSensitive',
                                                                                                                                          17), ('thermalDiffusion',
                                                                                                                                                18), ('thermalOther',
                                                                                                                                                      19), ('electroerosion',
                                                                                                                                                            20), ('electrostatic',
                                                                                                                                                                  21), ('photographicMicrofiche',
                                                                                                                                                                        22), ('photographicImagesetter',
                                                                                                                                                                              23), ('photographicOther',
                                                                                                                                                                                    24), ('ionDeposition',
                                                                                                                                                                                          25), ('eBeam',
                                                                                                                                                                                                26), ('typesetter',
                                                                                                                                                                                                      27))


class PrtMarkerCounterUnitTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4, 5, 6, 7, 8, 9, 11, 16, 17))
    namedValues = NamedValues(('tenThousandthsOfInches', 3), ('micrometers', 4), ('characters',
                                                                                  5), ('lines',
                                                                                       6), ('impressions',
                                                                                            7), ('sheets',
                                                                                                 8), ('dotRow',
                                                                                                      9), ('hours',
                                                                                                           11), ('feet',
                                                                                                                 16), ('meters',
                                                                                                                       17))


class PrtMarkerSuppliesTypeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('toner', 3), ('wasteToner',
                                                                           4), ('ink',
                                                                                5), ('inkCartridge',
                                                                                     6), ('inkRibbon',
                                                                                          7), ('wasteInk',
                                                                                               8), ('opc',
                                                                                                    9), ('developer',
                                                                                                         10), ('fuserOil',
                                                                                                               11), ('solidWax',
                                                                                                                     12), ('ribbonWax',
                                                                                                                           13), ('wasteWax',
                                                                                                                                 14), ('fuser',
                                                                                                                                       15), ('coronaWire',
                                                                                                                                             16), ('fuserOilWick',
                                                                                                                                                   17), ('cleanerUnit',
                                                                                                                                                         18), ('fuserCleaningPad',
                                                                                                                                                               19), ('transferUnit',
                                                                                                                                                                     20), ('tonerCartridge',
                                                                                                                                                                           21), ('fuserOiler',
                                                                                                                                                                                 22), ('water',
                                                                                                                                                                                       23), ('wasteWater',
                                                                                                                                                                                             24), ('glueWaterAdditive',
                                                                                                                                                                                                   25), ('wastePaper',
                                                                                                                                                                                                         26), ('bindingSupply',
                                                                                                                                                                                                               27), ('bandingSupply',
                                                                                                                                                                                                                     28), ('stitchingWire',
                                                                                                                                                                                                                           29), ('shrinkWrap',
                                                                                                                                                                                                                                 30), ('paperWrap',
                                                                                                                                                                                                                                       31), ('staples',
                                                                                                                                                                                                                                             32), ('inserts',
                                                                                                                                                                                                                                                   33), ('covers',
                                                                                                                                                                                                                                                         34))


class PrtMarkerSuppliesSupplyUnitTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18))
    namedValues = NamedValues(('tenThousandthsOfInches', 3), ('micrometers', 4), ('impressions',
                                                                                  7), ('sheets',
                                                                                       8), ('hours',
                                                                                            11), ('thousandthsOfOunces',
                                                                                                  12), ('tenthsOfGrams',
                                                                                                        13), ('hundrethsOfFluidOunces',
                                                                                                              14), ('tenthsOfMilliliters',
                                                                                                                    15), ('feet',
                                                                                                                          16), ('meters',
                                                                                                                                17), ('items',
                                                                                                                                      18))


class PrtMarkerSuppliesClassTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4))
    namedValues = NamedValues(('other', 1), ('supplyThatIsConsumed', 3), ('receptacleThatIsFilled',
                                                                          4))


class PrtMarkerColorantRoleTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4))
    namedValues = NamedValues(('other', 1), ('process', 3), ('spot', 4))


class PrtMediaPathMaxSpeedPrintUnitTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4, 5, 6, 7, 8, 9, 16, 17))
    namedValues = NamedValues(('tenThousandthsOfInchesPerHour', 3), ('micrometersPerHour',
                                                                     4), ('charactersPerHour',
                                                                          5), ('linesPerHour',
                                                                               6), ('impressionsPerHour',
                                                                                    7), ('sheetsPerHour',
                                                                                         8), ('dotRowPerHour',
                                                                                              9), ('feetPerHour',
                                                                                                   16), ('metersPerHour',
                                                                                                         17))


class PrtMediaPathTypeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('longEdgeBindingDuplex',
                                                             3), ('shortEdgeBindingDuplex',
                                                                  4), ('simplex', 5))


class PrtInterpreterTwoWayTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(3, 4))
    namedValues = NamedValues(('yes', 3), ('no', 4))


class PrtConsoleColorTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('white', 3), ('red', 4), ('green',
                                                                                       5), ('blue',
                                                                                            6), ('cyan',
                                                                                                 7), ('magenta',
                                                                                                      8), ('yellow',
                                                                                                           9), ('orange',
                                                                                                                10))


class PrtAlertSeverityLevelTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4, 5))
    namedValues = NamedValues(('other', 1), ('criticalBinaryChangeEvent', 3), ('warningUnaryChangeEvent',
                                                                               4), ('warningBinaryChangeEvent',
                                                                                    5))


class PrtAlertTrainingLevelTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('untrained', 3), ('trained',
                                                                               4), ('fieldService',
                                                                                    5), ('management',
                                                                                         6), ('noInterventionRequired',
                                                                                              7))


class PrtAlertGroupTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 30, 31, 32, 33))
    namedValues = NamedValues(('other', 1), ('hostResourcesMIBStorageTable', 3), ('hostResourcesMIBDeviceTable',
                                                                                  4), ('generalPrinter',
                                                                                       5), ('cover',
                                                                                            6), ('localization',
                                                                                                 7), ('input',
                                                                                                      8), ('output',
                                                                                                           9), ('marker',
                                                                                                                10), ('markerSupplies',
                                                                                                                      11), ('markerColorant',
                                                                                                                            12), ('mediaPath',
                                                                                                                                  13), ('channel',
                                                                                                                                        14), ('interpreter',
                                                                                                                                              15), ('consoleDisplayBuffer',
                                                                                                                                                    16), ('consoleLights',
                                                                                                                                                          17), ('alert',
                                                                                                                                                                18), ('finDevice',
                                                                                                                                                                      30), ('finSupply',
                                                                                                                                                                            31), ('finSupplyMediaInput',
                                                                                                                                                                                  32), ('finAttributeTable',
                                                                                                                                                                                        33))


class PrtAlertCodeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 501, 502, 503, 504, 505, 506, 507, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 901, 902, 903, 904, 1001, 1002, 1003, 1004, 1005, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1301, 1302, 1303, 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1509, 1801))
    namedValues = NamedValues(('other', 1), ('unknown', 2), ('coverOpened', 3), ('coverClosed', 4), ('interlockOpened', 5), ('interlockClosed', 6), ('configurationChanged', 7), ('jammed', 8), ('subunitMissing', 9), ('subunitLifeAlmostOver', 10), ('subunitLifeOver', 11), ('subunitAlmostEmpty', 12), ('subunitEmpty', 13), ('subunitAlmostFull', 14), ('subunitFull', 15), ('subunitNearLimit', 16), ('subunitAtLimit', 17), ('subunitOpened', 18), ('subunitClosed', 19), ('subunitTurnedOn', 20), ('subunitTurnedOff', 21), ('subunitOffline', 22), ('subunitPowerSaver', 23), ('subunitWarmingUp', 24), ('subunitAdded', 25), ('subunitRemoved', 26), ('subunitResourceAdded', 27), ('subunitResourceRemoved', 28), ('subunitRecoverableFailure', 29), ('subunitUnrecoverableFailure', 30), ('subunitRecoverableStorageError', 31), ('subunitUnrecoverableStorageError', 32), ('subunitMotorFailure', 33), ('subunitMemoryExhausted', 34), ('subunitUnderTemperature', 35), ('subunitOverTemperature', 36), ('subunitTimingFailure', 37), ('subunitThermistorFailure', 38), ('doorOpen', 501), ('doorClosed', 502), ('poweredUp', 503), ('poweredDown', 504), ('printerNMSReset', 505), ('printerManualReset', 506), ('printerReadyToPrint', 507), ('inputMediaTrayMissing', 801), ('inputMediaSizeChanged', 802), ('inputMediaWeightChanged', 803), ('inputMediaTypeChanged', 804), ('inputMediaColorChanged', 805), ('inputMediaFormPartsChange', 806), ('inputMediaSupplyLow', 807), ('inputMediaSupplyEmpty', 808), ('inputMediaChangeRequest', 809), ('inputManualInputRequest', 810), ('inputTrayPositionFailure', 811), ('inputTrayElevationFailure', 812), ('inputCannotFeedSizeSelected', 813), ('outputMediaTrayMissing', 901), ('outputMediaTrayAlmostFull', 902), ('outputMediaTrayFull', 903), ('outputMailboxSelectFailure', 904), ('markerFuserUnderTemperature', 1001), ('markerFuserOverTemperature', 1002), ('markerFuserTimingFailure', 1003), ('markerFuserThermistorFailure', 1004), ('markerAdjustingPrintQuality', 1005), ('markerTonerEmpty', 1101), ('markerInkEmpty', 1102), ('markerPrintRibbonEmpty', 1103), ('markerTonerAlmostEmpty', 1104), ('markerInkAlmostEmpty', 1105), ('markerPrintRibbonAlmostEmpty', 1106), ('markerWasteTonerReceptacleAlmostFull', 1107), ('markerWasteInkReceptacleAlmostFull', 1108), ('markerWasteTonerReceptacleFull', 1109), ('markerWasteInkReceptacleFull', 1110), ('markerOpcLifeAlmostOver', 1111), ('markerOpcLifeOver', 1112), ('markerDeveloperAlmostEmpty', 1113), ('markerDeveloperEmpty', 1114), ('markerTonerCartridgeMissing', 1115), ('mediaPathMediaTrayMissing', 1301), ('mediaPathMediaTrayAlmostFull', 1302), ('mediaPathMediaTrayFull', 1303), ('interpreterMemoryIncreased', 1501), ('interpreterMemoryDecreased', 1502), ('interpreterCartridgeAdded', 1503), ('interpreterCartridgeDeleted', 1504), ('interpreterResourceAdded', 1505), ('interpreterResourceDeleted', 1506), ('interpreterResourceUnavailable', 1507), ('interpreterComplexPageEncountered', 1509), ('alertRemovalOfBinaryChangeEntry', 1801))


prtGeneral = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 5))
prtGeneralTable = MibTable((1, 3, 6, 1, 2, 1, 43, 5, 1))
if mibBuilder.loadTexts:
    prtGeneralTable.setDescription('A table of general information per printer.\n        Objects in this table are defined in various\n        places in the MIB, nearby the groups to\n        which they apply.  They are all defined\n        here to minimize the number of tables that would\n        otherwise need to exist.')
prtGeneralEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 5, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'))
if mibBuilder.loadTexts:
    prtGeneralEntry.setDescription("An entry exists in this table for each device entry in\n         the host resources MIB device table with a device type\n         of 'printer'")
prtGeneralConfigChanges = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtGeneralConfigChanges.setDescription("Counts configuration changes within the printer. A\n         configuration change is defined to be an action that\n         results in a change to any MIB object other than those\n         that reflect status or level, or those that act as\n         counters or gauges. In addition, any action that results\n         in a row being added or deleted from any table in the\n         Printer MIB is considered a configuration change. Such\n         changes will often affect the capability of the printer\n         to service certain types of print jobs. Management\n         applications may cache infrequently changed\n         configuration information about sub-units within the\n         printer. This object should be incremented whenever the\n         agent wishes to notify management applications that any\n         cached configuration information for this device is to\n         be considered 'stale'. At this point, the management\n         application should flush any configuration information\n         cached about this device and fetch new configuration\n         information.\n\n         The following are examples of actions that would cause\n         the prtGeneralConfigChanges object to be incremented:\n\n         - Adding an output bin\n         - Changing the media in a sensing input tray\n         - Changing the value of prtInputMediaType\n         Note that the prtGeneralConfigChanges counter would not\n         be incremented when an input tray is removed, or the\n         level of an input device changes.")
prtGeneralCurrentLocalization = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtGeneralCurrentLocalization.setDescription('The value of the prtLocalizationIndex corresponding to\n          the current language, country, and character set to be\n          used for localized string values that are identified as\n          being dependent on the value of this object.  Note that\n          this object does not apply to localized strings in the\n          prtConsole group or to any object that is not\n          explicitly identified as being localized according to\n          prtGeneralCurrentLocalization.')
prtGeneralReset = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 3), PrtGeneralResetTC()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtGeneralReset.setDescription("Setting this value to 'powerCycleReset',\n         'resetToNVRAM', or 'resetToFactoryDefaults' will result\n         in the resetting of the printer.  When read, this object\n         will always have the value 'notResetting(3)', and a SET\n         of the value 'notResetting' shall have no effect on the\n         printer.  Some of the defined values are optional.\n         However, every implementation must support at least the\n         values 'notResetting' and 'resetToNVRAM'.")
prtGeneralCurrentOperator = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtGeneralCurrentOperator.setDescription("The name of the person who is responsible for operating\n         this printer. It is suggested that this string include\n         information that would enable other humans to reach the\n         operator, such as a phone number. As a convention to\n         facilitate automatic notification of the operator by the\n         agent or the network management station, the phone\n         number, fax number or email address should be placed on\n         a separate line starting with ASCII LF (hex 0x0A) and\n         the ASCII text string (without the quotes): 'phone: ',\n         'fax: ', and 'email: ', respectively. Phone numbers may\n         contain digits, spaces and parentheses, which shall be\n         ignored. Phone numbers may also include ASCII comma\n         characters(hex 2C) that are used to indicate a two-\n         second pause during the dialing sequence. If either the\n         phone, fax, or email information is not available, then\n         a line should not be included for this information.\n\n         NOTE: For interoperability purposes, it is advisable to\n         use email addresses formatted according to RFC 822\n         requirements.")
prtGeneralServicePerson = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtGeneralServicePerson.setDescription("The name of the person responsible for servicing this\n         printer. It is suggested that this string include\n         information that would enable other humans to reach the\n         service person, such as a phone number. As a convention\n         to facilitate automatic notification of the service\n         person by the agent or a network management station, the\n         phone number, fax number or email address should be\n         placed on a separate line starting with ASCII LF (hex\n         0x0A) and the ASCII text string (without the quotes):\n         'phone: ', 'fax: ', and 'email: ', respectively. Phone\n         numbers may contain digits, spaces and parentheses,\n         which shall be ignored. Phone numbers can also include\n         one or more ASCII comma characters(hex 2C) to indicate a\n         two-second pause during the dialing sequence. If either\n         the phone, fax, or email information is not available,\n         then a line should not included for this information.\n\n         NOTE: For interoperability purposes, it is advisable to\n         use email addresses formatted according to RFC 822\n         requirements.")
prtInputDefaultIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 6), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputDefaultIndex.setDescription('The value of prtInputIndex corresponding to the default\n         input sub-unit: that is, this object selects the default\n         source of input media.\n\n         This value shall be -1 if there is no default input\n         subunit specified for the printer as a whole.  In this\n         case, the actual default input subunit may be specified\n         by means outside the scope of this MIB, such as by each\n         interpreter in a printer with multiple interpreters.')
prtOutputDefaultIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 7), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputDefaultIndex.setDescription('The value of prtOutputIndex corresponding to the\n         default output sub-unit; that is, this object selects\n         the default output destination.\n\n         This value shall be -1 if there is no default output\n         subunit specified for the printer as a whole.  In this\n         case, the actual default output subunit may be specified\n         by means outside the scope of this MIB, such as by each\n         interpreter in a printer with multiple interpreters.')
prtMarkerDefaultIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtMarkerDefaultIndex.setDescription('The value of prtMarkerIndex corresponding to the\n        default marker sub-unit; that is, this object selects the\n        default marker.')
prtMediaPathDefaultIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtMediaPathDefaultIndex.setDescription('The value of prtMediaPathIndex corresponding to\n        the default media path; that is, the selection of the\n        default media path.')
prtConsoleLocalization = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtConsoleLocalization.setDescription('The value of the prtLocalizationIndex corresponding to\n         the language, country, and character set to be used for\n         the console.  This localization applies both to the\n         actual display on the console as well as the encoding of\n         these console objects in management operations.')
prtConsoleNumberOfDisplayLines = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtConsoleNumberOfDisplayLines.setDescription("The number of lines on the printer's physical\n        display.  This value is 0 if there are no lines on the\n        physical display or if there is no physical display")
prtConsoleNumberOfDisplayChars = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtConsoleNumberOfDisplayChars.setDescription('The number of characters per line displayed on the\n         physical display. This value is 0 if there are no lines\n         on the physical display or if there is no physical\n         display')
prtConsoleDisable = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 13), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(3, 4, 5, 6, 7))).clone(namedValues=NamedValues(('operatorConsoleEnabled', 3), ('operatorConsoleDisabled', 4), ('operatorConsoleEnabledLevel1', 5), ('operatorConsoleEnabledLevel2', 6), ('operatorConsoleEnabledLevel3', 7)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtConsoleDisable.setDescription("If the object prtConsoleDisable has value\n         'operatorConsoleDisabled' then input is not accepted\n         from the operator console. If the object\n         prtConsoleDisable has the value 'operatorConsoleEnabled'\n         then input is accepted from the operator console. If the\n         object prtConsoleDisable has the value\n         'operatorConsoleEnabledLevel1',\n         'operatorConsoleEnabledLevel2' or\n         'operatorConsoleEnabledLevel3' then limited input is\n         accepted from the operator console; the limitations are\n         product specific, however, the limitations are generally\n         less restrictive for operatorConsoleEnabledLevel1 than\n         for operatorConsoleEnabledLeve2, which is less\n         restrictive than operatorConsoleEnabledLevel3.\n\n         The value of the prtConsoleDisable object is a type-2\n         enumeration.")
prtAuxiliarySheetStartupPage = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 14), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtAuxiliarySheetStartupPage.setDescription('Used to enable or disable printing a startup page. If\n         enabled, a startup page will be printed shortly after\n         power-up, when the device is ready. Typical startup\n         pages include test patterns and/or printer configuration\n         information.')
prtAuxiliarySheetBannerPage = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 15), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtAuxiliarySheetBannerPage.setDescription('Used to enable or disable printing banner pages at the\n         beginning of jobs. This is a master switch which applies\n         to all jobs, regardless of interpreter.')
prtGeneralPrinterName = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 16), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtGeneralPrinterName.setDescription("An administrator-specified name for this printer.\n         Depending upon implementation of this printer, the value\n         of this object may or may not be same as the value for\n         the MIB-II 'SysName' object.")
prtGeneralSerialNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 17), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtGeneralSerialNumber.setDescription('A recorded serial number for this device that indexes\n         some type device catalog or inventory. This value is\n         usually set by the device manufacturer but the MIB\n         supports the option of writing for this object for site-\n         specific administration of device inventory or\n         tracking.')
prtAlertCriticalEvents = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 18), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertCriticalEvents.setDescription('A running counter of the number of critical alert\n         events that have been recorded in the alert table. The\n         value of this object is RESET in the event of a power\n         cycle operation (i.e., the value is not persistent.')
prtAlertAllEvents = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 1, 1, 19), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertAllEvents.setDescription('A running counter of the total number of alert event\n         entries (critical and non-critical) that have been\n         recorded in the alert table')
prtCover = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 6))
prtCoverTable = MibTable((1, 3, 6, 1, 2, 1, 43, 6, 1))
if mibBuilder.loadTexts:
    prtCoverTable.setDescription('A table of the covers and interlocks of the printer.')
prtCoverEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 6, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtCoverIndex'))
if mibBuilder.loadTexts:
    prtCoverEntry.setDescription("Information about a cover or interlock.\n        Entries may exist in the table for each device\n        index with a device type of 'printer'.")
prtCoverIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 6, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtCoverIndex.setDescription('A unique value used by the printer to identify this\n         Cover sub-unit.  Although these values may change due to\n         a major reconfiguration of the device (e.g. the addition\n         of new cover sub-units to the printer), values are\n         expected to remain stable across successive printer\n         power cycles.')
prtCoverDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 6, 1, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtCoverDescription.setDescription('The manufacturer provided cover sub-mechanism name in\n         the localization specified by\n         prtGeneralCurrentLocalization.')
prtCoverStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 6, 1, 1, 3), PrtCoverStatusTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtCoverStatus.setDescription('The status of this cover sub-unit.')
prtLocalization = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 7))
prtLocalizationTable = MibTable((1, 3, 6, 1, 2, 1, 43, 7, 1))
if mibBuilder.loadTexts:
    prtLocalizationTable.setDescription('The available localizations in this printer.')
prtLocalizationEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 7, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtLocalizationIndex'))
if mibBuilder.loadTexts:
    prtLocalizationEntry.setDescription("A description of a localization.\n        Entries may exist in the table for each device\n        index with a device type of 'printer'.")
prtLocalizationIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 7, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtLocalizationIndex.setDescription('A unique value used by the printer to identify this\n         localization entry.  Although these values may change\n         due to a major reconfiguration of the device (e.g., the\n         addition of new localization data to the printer),\n         values are expected to remain stable across successive\n         printer power cycles.')
prtLocalizationLanguage = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 7, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 2))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtLocalizationLanguage.setDescription('A two character language code from ISO 639.  Examples\n         en, gb, ca, fr, de.')
prtLocalizationCountry = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 7, 1, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 2))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtLocalizationCountry.setDescription('A two character country code from ISO 3166, a blank\n         string (two space characters) shall indicate that the\n         country is not defined.  Examples: US, FR, DE, ...')
prtLocalizationCharacterSet = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 7, 1, 1, 4), CodedCharSet()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtLocalizationCharacterSet.setDescription('The coded character set used for this localization.')
prtStorageRefTable = MibTable((1, 3, 6, 1, 2, 1, 43, 5, 2))
if mibBuilder.loadTexts:
    prtStorageRefTable.setDescription('')
prtStorageRefEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 5, 2, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrStorageIndex'), (0, 'Printer-MIB', 'prtStorageRefSeqNumber'))
if mibBuilder.loadTexts:
    prtStorageRefEntry.setDescription('This table will have an entry for each entry in the\n         Host Resources MIB storage table that represents storage\n         associated with a printer managed by this agent.')
prtStorageRefSeqNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtStorageRefSeqNumber.setDescription('This value will be unique amongst all entries with a\n         common value of hrStorageIndex. This object allows a\n         storage entry to point to the multiple printer devices\n         with which it is associated.')
prtStorageRefIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtStorageRefIndex.setDescription('The value of the hrDeviceIndex of the printer device\n         that this storageEntry is associated with.')
prtDeviceRefTable = MibTable((1, 3, 6, 1, 2, 1, 43, 5, 3))
if mibBuilder.loadTexts:
    prtDeviceRefTable.setDescription('')
prtDeviceRefEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 5, 3, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtDeviceRefSeqNumber'))
if mibBuilder.loadTexts:
    prtDeviceRefEntry.setDescription('This table will have an entry for each entry in the\n         Host Resources MIB device table that represents a device\n         associated with a printer managed by this agent.')
prtDeviceRefSeqNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtDeviceRefSeqNumber.setDescription('This value will be unique amongst all entries with a\n         common value of hrDeviceIndex. This object allows a\n         device entry to point to the multiple printer devices\n         with which it is associated.')
prtDeviceRefIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 5, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtDeviceRefIndex.setDescription('The value of the hrDeviceIndex of the printer device\n         that this deviceEntry is associated with.')
prtInput = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 8))
prtInputTable = MibTable((1, 3, 6, 1, 2, 1, 43, 8, 2))
if mibBuilder.loadTexts:
    prtInputTable.setDescription('A table of the devices capable of providing media for\n         input to the printing process.')
prtInputEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 8, 2, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtInputIndex'))
if mibBuilder.loadTexts:
    prtInputEntry.setDescription("Attributes of a device capable of providing media for\n         input to the printing process. Entries may exist in the\n         table for each device index with a device type of\n         'printer'.")
prtInputIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtInputIndex.setDescription('A unique value used by the printer to identify this\n         input sub-unit. Although these values may change due to\n         a major reconfiguration of the device (e.g. the addition\n         of n input sub-units to the printer), values are\n         expected to remain stable across successive printer\n         power cycles.')
prtInputType = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 2), PrtInputTypeTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputType.setDescription('The type of technology (discriminated primarily\n         according to feeder mechanism type) employed by the\n         input sub-unit.  Note, the Optional Input Class provides\n         for a descriptor field to further qualify the other\n         choice.')
prtInputDimUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 3), PrtMediaUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputDimUnit.setDescription('The unit of measurement for use calculating and relaying\n         dimensional values for this input sub-unit.')
prtInputMediaDimFeedDirDeclared = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 4), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaDimFeedDirDeclared.setDescription('This object provides the value of the declared\n         dimension, in the feed direction, of the media that is\n         (or, if empty, was or will be) in this input sub-unit.\n         The feed direction is the direction in which the media\n         is fed on this sub-unit.  This dimension is measured in\n         input sub-unit dimensional units (prtInputDimUnit).  If\n         this input sub-unit can reliably sense this value, the\n         value is sensed by the printer and may not be changed by\n         management requests.  Otherwise, the value may be\n         changed. The value (-1) means other and specifically\n         means that this sub-unit places no restriction on this\n         parameter.\n\n         The value (-2) indicates unknown.')
prtInputMediaDimXFeedDirDeclared = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 5), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaDimXFeedDirDeclared.setDescription('This object provides the value of the declared\n         dimension, in the cross feed direction, of the media\n         that is (or, if empty, was or will be) in this input\n         sub-unit.  The cross  feed direction is ninety degrees\n         relative to the feed direction associated with this sub-\n         unit. This dimension is measured in input sub-unit\n         dimensional units (prtInputDimUnit).  If this input sub-\n         unit can reliably sense this value, the value is sensed\n         by the printer and may not be changed by management\n         requests. Otherwise, the value may be changed. The value\n         (-1) means other and specifically means that this sub-\n         unit places no restriction on this parameter. The value\n         (-2) indicates unknown.')
prtInputMediaDimFeedDirChosen = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputMediaDimFeedDirChosen.setDescription('The printer will act as if media of the chosen\n         dimension (in the feed direction) is present in this\n         input source.  Note that this value will be used even if\n         the input tray is empty. Feed dimension measurements are\n         taken relative to the feed direction associated with\n         that sub-unit and are in input sub-unit dimensional\n         units (MediaUnit). If the printer supports the declared\n         dimension, the granted dimension is the same as the\n         declared dimension. If not, the granted dimension is set\n         to the closest dimension that the printer supports when\n         the declared dimension is set. The value (-1) means\n         other and specifically indicates that this sub-unit\n         places no restriction on this parameter. The value (-2)\n         indicates unknown.')
prtInputMediaDimXFeedDirChosen = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputMediaDimXFeedDirChosen.setDescription('The printer will act as if media of the chosen\n         dimension (in the cross feed direction) is present in\n         this input source. Note that this value will be used\n         even if the input tray is empty.  The cross feed\n         direction is ninety degrees relative to the feed\n         direction associated with this sub-unit. This dimension\n         is measured in input sub-unit dimensional units\n         (MediaUnit).  If the printer supports the declare\n         dimension, the granted dimension is the same as the\n         declared dimension. If not, the granted dimension is set\n         to the closest dimension that the printer supports when\n         the declared dimension is set. The value (-1) means\n         other and specifically indicates that this sub-unit\n         places no restriction on this parameter.  The value (-2)\n         indicates unknown.')
prtInputCapacityUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 8), PrtCapacityUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputCapacityUnit.setDescription('The unit of measurement for use in calculating and\n         relaying capacity values for this input sub-unit.')
prtInputMaxCapacity = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 9), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMaxCapacity.setDescription('The maximum capacity of the input sub-unit in input\n         sub-unit capacity units (PrtCapacityUnitTC).  There is\n         no convention associated with the media itself so this\n         value reflects claimed capacity. If this input sub-unit\n         can reliably sense this value, the value is sensed by\n         the printer and may not be changed by management\n         requests; otherwise, the value may be written (by a\n         Remote Control Panel or a Management Application). The\n         value (-1) means other and specifically indicates that\n         the sub-unit places no restrictions on this parameter.\n         The value (-2) means unknown.')
prtInputCurrentLevel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 10), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputCurrentLevel.setDescription('The current capacity of the input sub-unit in input\n         sub-unit capacity units (PrtCapacityUnitTC). If this\n         input sub-unit can reliably sense this value, the value\n         is sensed by the printer and may not be changed by\n         management requests; otherwise, the value may be written\n         (by a Remote Control Panel or a Management Application).\n         The value (-1) means other and specifically indicates\n         that the sub-unit places no restrictions on this\n         parameter. The value (-2) means unknown. The value (-3)\n         means that the printer knows that at least one unit\n         remains.')
prtInputStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 11), PrtSubUnitStatusTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputStatus.setDescription('The current status of this input sub-unit.')
prtInputMediaName = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 12), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaName.setDescription("A description of the media contained in this input sub-\n         unit; This description is intended for display to a\n         human operator. This description is not processed by the\n         printer.  It is used to provide information not\n         expressible in terms of the other media attributes (e.g.\n         prtInputMediaDimFeedDirChosen,\n         prtInputMediaDimXFeedDirChosen, prtInputMediaWeight,\n         prtInputMediaType). An example would be 'legal tender\n         bond paper'.")
prtInputName = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 13), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputName.setDescription('The name assigned to this input sub-unit.')
prtInputVendorName = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 14), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputVendorName.setDescription('The vendor name of this input sub-unit.')
prtInputModel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 15), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputModel.setDescription('The model name of this input sub-unit.')
prtInputVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 16), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputVersion.setDescription('The version of this input sub-unit.')
prtInputSerialNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 17), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputSerialNumber.setDescription('The serial number assigned to this input sub-unit.')
prtInputDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 18), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInputDescription.setDescription('A free-form text description of this input sub-unit in\n         the localization specified by\n         prtGeneralCurrentLocalization.')
prtInputSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 19), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputSecurity.setDescription('Indicates if this input sub-unit has some security\n         associated with it.')
prtInputMediaWeight = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 20), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaWeight.setDescription('The weight of the medium associated with this input\n         sub-unit in grams / per meter squared. The value (-2)\n         means unknown.')
prtInputMediaType = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 21), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaType.setDescription('The name of the type of medium associated with this\n         input sub-unit. This name need not be processed by the\n         printer; it might simply be displayed to an operator.\n         The standardized string values from ISO 10175 (DPA) and\n         ISO 10180 (SPDL) are:\n\n         stationery       Separately cut sheets of an opaque\n                          material\n         transparency     Separately cut sheets of a transparent\n                          material\n         envelope         Envelopes that can be used for\n                          conventional mailing purposes\n         envelope-plain   Envelopes that are not preprinted and\n                          have no windows\n         envelope-window  Envelopes that have windows for\n                          addressing purposes\n         continuous-long  Continuously connected sheets of an\n                          opaque material connected along the\n                          long edge\n         continuous-short Continuously connected sheets of an\n                          opaque material connected along the\n                          short edge\n         tab-stock        Media with tabs\n         multi-part-form  Form medium composed of multiple layers\n                          not pre-attached to one another; each\n                          sheet may be drawn separately from an\n                          input source\n         labels           Label stock\n         multi-layer      Form medium composed of multiple layers\n                          which are pre-attached to one another;\n                          e.g., for use with impact printers.\n\n         Implementers may add additional string values. The\n         naming\n         conventions in ISO 9070 are recommended in order to\n         avoid\n         potential name clashes.')
prtInputMediaColor = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 22), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaColor.setDescription('The name of the color of the medium associated with\n        this input sub-unit using standardized string values\n        from ISO 10175 (DPA) and ISO 10180 (SPDL) which are:\n\n        other\n        unknown\n        white\n        pink\n        yellow\n        buff\n        goldenrod\n        blue\n        green\n        transparent\n\n        Implementers may add additional string values. The naming\n        conventions in ISO 9070 are recommended in order to avoid\n        potential name clashes.')
prtInputMediaFormParts = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 23), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaFormParts.setDescription('The number of parts associated with the medium\n         associated with this input sub-unit if the medium is a\n         multi-part form.  The value (-1) means other and\n         specifically indicates that the device places no\n         restrictions on this parameter.  The value (-2) means\n         unknown.')
prtInputMediaLoadTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 24), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputMediaLoadTimeout.setDescription("When the printer is not able to print due to a subunit\n         being empty or the requested media must be manually\n         loaded, the printer will wait for the duration (in\n         seconds) specified by this object. Upon expiration of\n         the time-out, the printer will take the action specified\n         by prtInputNextIndex.\n\n         The event which causes the printer to enter the waiting\n         state is product specific. If the printer is not waiting\n         for manually fed media, it may switch from an empty\n         subunit to a different subunit without waiting for the\n         time-out to expire.\n\n         A value of (-1) implies 'other' or 'infinite' which\n         translates to 'wait forever'. The action which causes\n         printing to continue is product specific. A value of (-\n         2) implies 'unknown'.")
prtInputNextIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 8, 2, 1, 25), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInputNextIndex.setDescription("The value of prtInputIndex corresponding to the input\n         subunit which will be used when this input subunit is\n         emptied and the time-out specified by\n         prtInputMediaLoadTimeout expires. A value of zero(0)\n         indicates that auto input switching will not occur when\n         this input subunit is emptied. If the time-out specified\n         by prtInputLoadMediaTimeout expires and this value is\n         zero(0), the job will be aborted. A value of (-1) means\n         other. The value (-2) means 'unknown' and specifically\n         indicates that an implementation specific method will\n         determine the next input subunit to use at the time this\n         subunit is emptied and the time-out expires. The value(-\n         3) means input switching is not supported for this\n         subunit.")
prtOutput = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 9))
prtOutputTable = MibTable((1, 3, 6, 1, 2, 1, 43, 9, 2))
if mibBuilder.loadTexts:
    prtOutputTable.setDescription('A table of the devices capable of receiving media\n         delivered from the printing process.')
prtOutputEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 9, 2, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtOutputIndex'))
if mibBuilder.loadTexts:
    prtOutputEntry.setDescription("Attributes of a device capable of receiving media\n         delivered from the printing process. Entries may exist\n         in the table for each device index with a device type of\n         'printer'.")
prtOutputIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtOutputIndex.setDescription('A unique value used by this printer to identify this\n        output sub-unit. Although these values may change due\n        to a major reconfiguration of the sub-unit (e.g.  the\n        addition of new output devices to the printer), values\n        are expected to remain stable across successive printer\n        power cycles.')
prtOutputType = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 2), PrtOutputTypeTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputType.setDescription('The type of technology supported by this output sub-\n         unit.')
prtOutputCapacityUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 3), PrtCapacityUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputCapacityUnit.setDescription('The unit of measurement for use in calculating and\n         relaying capacity values for this output sub-unit.')
prtOutputMaxCapacity = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 4), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputMaxCapacity.setDescription('The maximum capacity of this output sub-unit in output\n         sub-unit capacity units (PrtCapacityUnitTC). There is no\n         convention associated with the media itself so this\n         value essentially reflects claimed capacity. If this\n         output sub-unit can reliably sense this value, the value\n         is sensed by the printer and may not be changed by\n         management requests; otherwise, the value may be written\n         (by a Remote Control Panel or a Management Application).\n         The value (-1) means other and specifically indicates\n         that the sub-unit places no restrictions on this\n         parameter. The value (-2) means unknown.')
prtOutputRemainingCapacity = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 5), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputRemainingCapacity.setDescription('The remaining capacity of the possible output sub-unit\n         capacity in output sub-unit capacity units\n         (PrtCapacityUnitTC)of this output sub-unit. If this\n         output sub-unit can reliably sense this value, the value\n         is sensed by the printer and may not be modified by\n         management requests; otherwise, the value may be written\n         (by a Remote Control Panel or a Management Application).\n         The value (-1) means other and specifically indicates\n         that the sub-unit places no restrictions on this\n         parameter.  The value (-2) means unknown.  The value (-\n         3) means that the printer knows that there remains\n         capacity for at least one unit.')
prtOutputStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 6), PrtSubUnitStatusTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputStatus.setDescription('The current status of this output sub-unit.')
prtOutputName = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 7), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputName.setDescription('The name assigned to this output sub-unit.')
prtOutputVendorName = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 8), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputVendorName.setDescription('The vendor name of this output sub-unit.')
prtOutputModel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 9), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputModel.setDescription('The model name assigned to this output sub-unit.')
prtOutputVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 10), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputVersion.setDescription('The version of this output sub-unit.')
prtOutputSerialNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 11), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputSerialNumber.setDescription('The serial number assigned to this output sub-unit.')
prtOutputDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 12), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputDescription.setDescription('A free-form text description of this output sub-unit in\n         the localization specified by\n         prtGeneralCurrentLocalization.')
prtOutputSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 13), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputSecurity.setDescription('Indicates if this output sub-unit has some security\n         associated with it and if that security is enabled or\n         not.')
prtOutputDimUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 14), PrtMediaUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtOutputDimUnit.setDescription('The unit of measurement for use in calculating and\n         relaying dimensional values for this output sub-unit.')
prtOutputMaxDimFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 15), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputMaxDimFeedDir.setDescription('The maximum dimensions supported by this output sub-unit\n        for measurements taken parallel relative to the feed\n        direction associated with that sub-unit in output\n        sub-unit dimensional units (MediaUnit). If this output\n        sub-unit can reliably sense this value, the value is\n        sensed by the printer and may not be changed with\n        management protocol operations.')
prtOutputMaxDimXFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 16), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputMaxDimXFeedDir.setDescription('The maximum dimensions supported by this output sub-unit\n        for measurements taken ninety degrees relative to the\n        feed direction associated with that sub-unit in output\n        sub-unit dimensional units (MediaUnit). If this output\n        sub-unit can reliably sense this value, the value is\n        sensed by the printer and may not be changed with\n        management protocol operations.')
prtOutputMinDimFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 17), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputMinDimFeedDir.setDescription('The minimum dimensions supported by this output sub-unit\n        for measurements taken parallel relative to the feed\n        direction associated with that sub-unit in output\n        sub-unit dimensional units (DimUnit).  If this output\n        sub-unit can reliably sense this value, the value is\n        sensed by the printer and may not be changed with\n        management protocol operations.')
prtOutputMinDimXFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 18), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputMinDimXFeedDir.setDescription('The minimum dimensions supported by this output sub-unit\n        for measurements taken ninety degrees relative to the\n        feed direction associated with that sub-unit in output\n        sub-unit dimensional units (DimUnit). If this output\n        sub-unit can reliably sense this value, the value is\n        sensed by the printer and may not be changed with\n        management protocol operations.')
prtOutputStackingOrder = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 19), PrtOutputStackingOrderTC()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputStackingOrder.setDescription("The current state of the stacking order for the\n        associated output sub-unit. 'FirstToLast' means\n        that as pages are output the front of the next page is\n        placed against the back of the previous page.\n        'LasttoFirst' means that as pages are output the back\n        of the next page is placed against the front of the\n        previous page.")
prtOutputPageDeliveryOrientation = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 20), PrtOutputPageDeliveryOrientationTC()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputPageDeliveryOrientation.setDescription("The reading surface that will be 'up' when pages are\n        delivered to the associated output sub-unit. Values are\n        faceUp and faceDown. (Note: interpretation of these\n        values is in general context-dependent based on locale;\n        presentation of these values to an end-user should be\n        normalized to the expectations of the user).")
prtOutputBursting = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 21), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputBursting.setDescription('This object indicates that the outputting sub-unit\n         supports bursting, and if so, whether the feature is\n         enabled. Bursting is the process by which continuous\n         media is separated into individual sheets, typically by\n         bursting along pre-formed perforations.')
prtOutputDecollating = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 22), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputDecollating.setDescription('This object indicates that the output supports\n         decollating, and if so, whether the feature is enabled.\n         Decollating is the process by which the individual parts\n         within a multi-part form are separated and sorted into\n         separate stacks for each part.')
prtOutputPageCollated = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 23), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputPageCollated.setDescription('This object indicates that the output sub-unit supports\n         page collation, and if so, whether the feature is\n         enabled. See glossary for definition of how this\n         document defines collation.')
prtOutputOffsetStacking = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 9, 2, 1, 24), PresentOnOff()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtOutputOffsetStacking.setDescription('This object indicates that the output supports offset\n         stacking, and if so, whether the feature is enabled. See\n         glossary for how Offset Stacking is defined by this\n         document.')
prtMarker = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 10))
prtMarkerTable = MibTable((1, 3, 6, 1, 2, 1, 43, 10, 2))
if mibBuilder.loadTexts:
    prtMarkerTable.setDescription('')
prtMarkerEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 10, 2, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtMarkerIndex'))
if mibBuilder.loadTexts:
    prtMarkerEntry.setDescription("Entries may exist in the table for each device index\n         with a device type of 'printer'.")
prtMarkerIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtMarkerIndex.setDescription('A unique value used by the printer to identify this\n         marking SubUnit.  Although these values may change due\n         to a major reconfiguration of the device (e.g. the\n         addition of new marking sub-units to the printer),\n         values are expected to remain stable across successive\n         printer power cycles.')
prtMarkerMarkTech = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 2), PrtMarkerMarkTechTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerMarkTech.setDescription('The type of marking technology used for this marking\n         sub-unit.')
prtMarkerCounterUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 3), PrtMarkerCounterUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerCounterUnit.setDescription('The unit that will be used by the printer when\n         reporting counter values for this marking sub-unit.  The\n         time units of measure are provided for a device like a\n         strip recorder that does not or cannot track the\n         physical dimensions of the media and does not use\n         characters, lines or sheets.')
prtMarkerLifeCount = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerLifeCount.setDescription('The count of the number of units of measure counted\n         during the life of printer using units of measure as\n         specified by prtMarkerCounterUnit.')
prtMarkerPowerOnCount = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerPowerOnCount.setDescription('The count of the number of units of measure counted\n         since the equipment was most recently powered on using\n         units of measure as specified by prtMarkerCounterUnit.')
prtMarkerProcessColorants = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerProcessColorants.setDescription('The number of process colors supported by this marker.\n         A process color of 1 implies monochrome.  The value of\n         this object and prtMarkerSpotColorants cannot both be 0.\n         The value of prtMarkerProcessColorants must be 0 or\n         greater.')
prtMarkerSpotColorants = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSpotColorants.setDescription('The number of spot colors supported by this marker. The\n         value of this object and prtMarkerProcessColorants\n         cannot both be 0.  Must be 0 or greater.')
prtMarkerAddressabilityUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(3, 4))).clone(namedValues=NamedValues(('tenThousandthsOfInches', 3), ('micrometers', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerAddressabilityUnit.setDescription("The unit of measure of distances, as applied to the\n         marker's resolution.")
prtMarkerAddressabilityFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 9), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerAddressabilityFeedDir.setDescription("The maximum number of addressable marking positions in\n         the feed direction per 10000 units of measure specified\n         by prtMarkerAddressabilityUnit.  A value of (-1) implies\n         'other' or 'infinite' while a value of (-2) implies\n         'unknown'.")
prtMarkerAddressabilityXFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 10), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerAddressabilityXFeedDir.setDescription("The maximum number of addressable marking positions in\n         the cross feed direction in 10000 units of measure\n         specified by prtMarkerAddressabilityUnit.  A value of (-\n         1) implies 'other' or 'infinite' while a value of (-2)\n         implies 'unknown'.")
prtMarkerNorthMargin = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 11), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerNorthMargin.setDescription('The margin, in units identified by\n         prtMarkerAddressabilityUnit, from the leading edge of\n         the medium as the medium flows through the marking\n         engine with the side to be imaged facing the observer.\n         The leading edge is the North edge and the other edges\n         are defined by the normal compass layout of  directions\n         with the compass facing the observer.  Printing within\n         the area bounded by all four margins is guaranteed for\n         all interpreters.   The value (-2) means unknown.')
prtMarkerSouthMargin = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 12), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSouthMargin.setDescription('The margin from the South edge  (see\n         prtMarkerNorthMargin) of the medium in units identified\n         by prtMarkerAddressabilityUnit.  Printing within the\n         area bounded by all four margins  is guaranteed for all\n         interpreters. The value (-2) means unknown.')
prtMarkerWestMargin = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 13), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerWestMargin.setDescription('The margin from the West edge (see\n         prtMarkerNorthMargin) of the medium in units identified\n         by prtMarkerAddressabilityUnit. Printing within the area\n         bounded by all four margins is guaranteed for all\n         interpreters. The value (-2) means unknown.')
prtMarkerEastMargin = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 14), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerEastMargin.setDescription('The margin from the East edge (see\n         prtMarkerNorthMargin) of the medium in units identified\n         by prtMarkerAddressabilityUnit. Printing within the area\n         bounded by all four margins is guaranteed for all\n         interpreters. The value (-2) means unknown.')
prtMarkerStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 15), PrtSubUnitStatusTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerStatus.setDescription('The current status of this marker sub-unit.')
prtMarkerSupplies = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 11))
prtMarkerSuppliesTable = MibTable((1, 3, 6, 1, 2, 1, 43, 11, 1))
if mibBuilder.loadTexts:
    prtMarkerSuppliesTable.setDescription('A table of the marker supplies available on this\n         printer.')
prtMarkerSuppliesEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 11, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtMarkerSuppliesIndex'))
if mibBuilder.loadTexts:
    prtMarkerSuppliesEntry.setDescription("Attributes of a marker supply. Entries may exist in the\n         table for each device index with a device type of\n         'printer'.")
prtMarkerSuppliesIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtMarkerSuppliesIndex.setDescription('A unique value used by the printer to identify this\n         marker supply.  Although these values may change due to\n         a major reconfiguration of the device (e.g. the addition\n         of new marker supplies to the printer), values are\n         expected to remain stable across successive power\n         cycles.')
prtMarkerSuppliesMarkerIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSuppliesMarkerIndex.setDescription('The value of prtMarkerIndex corresponding to the\n         marking sub-unit with which this marker supply sub-unit\n         is associated.')
prtMarkerSuppliesColorantIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSuppliesColorantIndex.setDescription('The value of prtMarkerColorantIndex corresponding to\n         the colorant with which this marker supply sub-unit is\n         associated.  This value shall be 0 if there is no\n         colorant table or if this supply does not depend on a\n         single specified colorant.')
prtMarkerSuppliesClass = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 4), PrtMarkerSuppliesClassTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSuppliesClass.setDescription('Indicates whether this supply entity represents a\n         supply that is consumed or a receptacle that is filled.')
prtMarkerSuppliesType = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 5), PrtMarkerSuppliesTypeTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSuppliesType.setDescription('The type of this supply.')
prtMarkerSuppliesDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSuppliesDescription.setDescription('The description of this supply container/receptacle in\n         the localization specified by\n         prtGeneralCurrentLocalization.')
prtMarkerSuppliesSupplyUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 7), PrtMarkerSuppliesSupplyUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerSuppliesSupplyUnit.setDescription('Unit of measure of this marker supply\n         container/receptacle.')
prtMarkerSuppliesMaxCapacity = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 8), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtMarkerSuppliesMaxCapacity.setDescription('The maximum capacity of this supply\n         container/receptacle expressed in\n         prtMarkerSuppliesSupplyUnit. If this supply\n         container/receptacle can reliably sense this value, the\n         value is reported by the printer and is read-only;\n         otherwise, the value may be written (by a Remote Control\n         Panel or a Management Application). The value (-1) means\n         other and specifically indicates that the sub-unit\n         places no restrictions on this parameter. The value (-2)\n         means unknown.')
prtMarkerSuppliesLevel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 11, 1, 1, 9), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtMarkerSuppliesLevel.setDescription('The current level if this supply is a container;\n         remaining space if this supply is a receptacle. If this\n         supply container/receptacle can reliably sense this\n         value, the value is reported by the printer and is read-\n         only; otherwise, the value may be written (by a Remote\n         Control Panel or a Management Application). The value (-\n         1) means other and specifically indicates that the sub-\n         unit places no restrictions on this parameter. The value\n         (-2) means unknown.  A value of (-3) means that the\n         printer knows that there is some supply/remaining space,\n         respectively.')
prtMarkerColorant = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 12))
prtMarkerColorantTable = MibTable((1, 3, 6, 1, 2, 1, 43, 12, 1))
if mibBuilder.loadTexts:
    prtMarkerColorantTable.setDescription('A table of all of the colorants available on the\n         printer.')
prtMarkerColorantEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 12, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtMarkerColorantIndex'))
if mibBuilder.loadTexts:
    prtMarkerColorantEntry.setDescription("Attributes of a colorant available on the printer.\n         Entries may exist in the table for each device index\n         with a device type of 'printer'.")
prtMarkerColorantIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 12, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtMarkerColorantIndex.setDescription('A unique value used by the printer to identify this\n        colorant. Although these values may change due to a major\n        reconfiguration of the device (e.g. the addition of new\n        colorants to the printer).')
prtMarkerColorantMarkerIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 12, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerColorantMarkerIndex.setDescription('The value of prtMarkerIndex corresponding to the marker\n         sub-unit with which this colorant entry is associated.')
prtMarkerColorantRole = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 12, 1, 1, 3), PrtMarkerColorantRoleTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerColorantRole.setDescription('The role played by this colorant.')
prtMarkerColorantValue = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 12, 1, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerColorantValue.setDescription('The name of the color of this colorant using\n         standardized string names from ISO 10175 (DPA) and ISO\n         10180 (SPDL) which are:\n           other\n           unknown\n           white\n           red\n           green\n           blue\n           cyan\n           magenta\n           yellow\n           black\n         Implementers may add additional string values. The\n         naming conventions in ISO 9070 are recommended in order\n         to avoid potential name clashes')
prtMarkerColorantTonality = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 12, 1, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMarkerColorantTonality.setDescription('The distinct levels of tonality realizable by a marking\n         sub-unit when using this colorant.  This value does not\n         include the number of levels of tonal difference that an\n         interpreter can obtain by techniques such as half\n         toning. This value must be at least 2.')
prtMediaPath = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 13))
prtMediaPathTable = MibTable((1, 3, 6, 1, 2, 1, 43, 13, 4))
if mibBuilder.loadTexts:
    prtMediaPathTable.setDescription('')
prtMediaPathEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 13, 4, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtMediaPathIndex'))
if mibBuilder.loadTexts:
    prtMediaPathEntry.setDescription("Entries may exist in the table for each device index\n         with a device type of 'printer'.")
prtMediaPathIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtMediaPathIndex.setDescription('A unique value used by the printer to identify this\n         media path. Although these values may change due to a\n         major reconfiguration of the device (e.g. the addition\n         of new media paths to the printer), values are expected\n         to remain stable across successive printer power\n         cycles.')
prtMediaPathMaxSpeedPrintUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 2), PrtMediaPathMaxSpeedPrintUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMaxSpeedPrintUnit.setDescription('The unit of measure used in specifying the speed of all\n         media paths in the printer.')
prtMediaPathMediaSizeUnit = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 3), PrtMediaUnitTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMediaSizeUnit.setDescription('The units of measure of media size for use in\n         calculating and relaying dimensional values for all\n         media paths in the printer.')
prtMediaPathMaxSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMaxSpeed.setDescription("The maximum printing speed of this media path expressed\n         in prtMediaPathMaxSpeedUnit's.  A value of (-1) implies\n         'other'.")
prtMediaPathMaxMediaFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMaxMediaFeedDir.setDescription("The maximum physical media size in the feed direction\n         of this media path expressed in units of measure\n         specified by PrtMediaPathMediaSizeUnit.  A value of (-1)\n         implies 'unlimited' a value of (-2) implies 'unknown'")
prtMediaPathMaxMediaXFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMaxMediaXFeedDir.setDescription("The maximum physical media size across the feed\n         direction of this media path expressed in units of\n         measure specified by prtMediaPathMediaSizeUnit.  A value\n         of (-2) implies 'unknown'.")
prtMediaPathMinMediaFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMinMediaFeedDir.setDescription("The minimum physical media size in the feed direction\n         of this media path expressed in units of measure\n         specified by prtMediaPathMediaSizeUnit. A value of (-2)\n         implies 'unknown'.")
prtMediaPathMinMediaXFeedDir = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 8), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathMinMediaXFeedDir.setDescription("The minimum physical media size across the feed\n         direction of this media path expressed in units of\n         measure specified by prtMediaPathMediaSizeUnit.  A value\n         of (-2) implies 'unknown'.")
prtMediaPathType = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 9), PrtMediaPathTypeTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathType.setDescription('The type of the media path for this media path.')
prtMediaPathDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 10), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathDescription.setDescription('The manufacturer-provided description of this media\n         path in the localization specified by\n         prtGeneralCurrentLocalization.')
prtMediaPathStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 13, 4, 1, 11), PrtSubUnitStatusTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtMediaPathStatus.setDescription('The current status of this media path.')
prtChannel = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 14))
prtChannelTable = MibTable((1, 3, 6, 1, 2, 1, 43, 14, 1))
if mibBuilder.loadTexts:
    prtChannelTable.setDescription('')
prtChannelEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 14, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtChannelIndex'))
if mibBuilder.loadTexts:
    prtChannelEntry.setDescription("Entries may exist in the table for each device index\n         with a device type of 'printer'.")
prtChannelIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtChannelIndex.setDescription('A unique value used by the printer to identify this\n         data channel.  Although these values may change due to a\n         major reconfiguration of the device (e.g. the addition\n         of new data channels to the printer), values are\n         expected to remain stable across successive printer\n         power cycles.')
prtChannelType = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 2), PrtChannelTypeTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtChannelType.setDescription('The type of this print data channel.  This object\n         provides the linkage to ChannelType-specific groups that\n         may (conceptually) extend the prtChannelTable with\n         additional details about that channel.')
prtChannelProtocolVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 63))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtChannelProtocolVersion.setDescription('The version of the protocol used on this channel.  The\n         format used for version numbering depends on\n         prtChannelType.')
prtChannelCurrentJobCntlLangIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 4), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtChannelCurrentJobCntlLangIndex.setDescription('The value of prtInterpreterIndex corresponding to the\n         Control Language Interpreter for this channel. This\n         interpreter defines the syntax used for control\n         functions, such as querying or changing environment\n         variables and identifying job boundaries (e.g. PJL,\n         PostScript, NPAP). A value of zero indicates that there\n         is no current Job Control Language Interpreter for this\n         channel')
prtChannelDefaultPageDescLangIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 5), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtChannelDefaultPageDescLangIndex.setDescription('The value of prtInterpreterIndex corresponding to the\n         Page Description Language Interpreter for this channel.\n         This interpreter defines the default Page Description\n         Language interpreter to be used for the print data\n         unless the Control Language is used to select a specific\n         interpreter (e.g., PCL, PostScript Language, auto-\n         sense). A value of zero indicates that there is no\n         default page description language interpreter for this\n         channel.')
prtChannelState = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 6), PrtChannelStateTC()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtChannelState.setDescription('The state of this print data channel. The value\n         determines whether control information and print data is\n         allowed through this channel or not.')
prtChannelIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 7), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtChannelIfIndex.setDescription('The value of ifIndex (in the ifTable; see the interface\n         section of MIB-2/RFC 1213) which corresponds to this\n         channel. When more than one row of the ifTable is\n         relevant, this is the index of the row representing the\n         topmost layer in the interface hierarchy.  A value of\n         zero indicates that no interface is associated with this\n         channel.')
prtChannelStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 8), PrtSubUnitStatusTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtChannelStatus.setDescription('The current status of the channel.')
prtChannelInformation = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 14, 1, 1, 9), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtChannelInformation.setDescription("Auxiliary information to allow a printing application\n         to use the channel for data submission to the printer.\n         An application capable of using a specific\n         PrtChannelType should be able to use the combined\n         information from the prtChannelInformation and other\n         channel and interface group objects to 'bootstrap' its\n         use of the channel.  prtChannelInformation is not\n         intended to provide a general channel description, nor\n         to provide information that is available once the\n         channel is in use.\n\n         The encoding and interpretation of the\n         prtChannelInformation object is specific to channel\n         type.  The description of each PrtChannelType enum value\n         for which prtChannelInformation is defined specifies the\n         appropriate encoding and interpretation, including\n         interaction with other objects.  For channel types that\n         do not specify a prtChannelInformation value, its value\n         shall be null (0 length).\n\n         When a new PrtChannelType enumeration value is\n         registered, its accompanying description must specify\n         the encoding and interpretation of the\n         prtChannelInformation value for the channel type.\n         prtChannelInformation semantics for an existing\n         PrtChannelType may be added or amended in the same\n         manner as described in section 2.4.1 for type 2\n         enumeration values.\n\n         The prtChannelInformation specifies values for a\n         collection of channel attributes, represented as text\n         according to the following rules:\n\n         1. The prtChannelInformation is not affected by\n         localization.\n\n         2. The prtChannelInformation is a list of entries\n         representing the attribute values.  Each entry consists\n         of the following items, in order:\n\n         a. a keyword, composed of alphabetic characters (A-Z,\n         a-z) represented by their NVT ASCII [NVT ASCII] codes,\n         that identifies a channel attribute,\n         b. the NVT ASCII code for an Equals Sign (=) (code 61)\n         to delimit the keyword,\n\n         c. a data value encoded using rules specific to the\n         PrtChannelType to with the prtChannelInformation applies\n         which must in no case allow an octet with value 10 (the\n         NVT ASCII Line Feed code),\n\n         d. the NVT ASCII code for a Line Feed character (code\n         10) to delimit the data value.\n\n         No other octets shall be present.\n\n         Keywords are case-sensitive.  Conventionally, keywords\n         are capitalized (including each word of a multi-word\n         keyword) and since they occupy space in the\n         prtChannelInformation, they are kept short.\n\n         3. If a channel attribute has multiple values, it is\n         represented by multiple entries with the same keyword,\n         each specifying one value. Otherwise, there shall be at\n         most one entry for each attribute.\n\n         4. By default, entries may appear in any order.  If\n         there are ordering constraints for particular entries,\n         these must be specified in their definitions.\n\n         5. The prtChannelInformation value by default consists\n         of text represented by NVT ASCII graphics character\n         codes. However, other representations may be specified:\n\n         a. In cases where the prtChannelInformation value\n         contains information not normally coded in textual form,\n         whatever symbolic representation is conventionally used\n         for the information should be used for encoding the\n         prtChannelInformation value. (For instance, a binary\n         port value might be represented as a decimal number\n         using NVT ASCII codes.) Such encoding must be specified\n         in the definition of the value.\n\n         b. The value may contain textual information in a\n         character set other than NVT ASCII graphics characters.\n         (For instance, an identifier might consist of ISO 10646\n         text encoded using the UTF-8 encoding scheme.) Such a\n         character set and its encoding must be specified in the\n         definition of the value.\n\n         6. For each PrtChannelType for which\n         prtChannelInformation entries are defined, the\n         descriptive text associated with the PrtChannelType\n         enumeration value shall specify the following\n         information for each entry:\n\n         Title:        Brief description phrase, e.g.: 'Port\n                       name', 'Service Name', etc.\n\n         Keyword:      The keyword value, e.g.: 'Port' or\n                       'Service'\n\n         Syntax:       The encoding of the entry value if it\n                       cannot be directly represented by NVT\n                       ASCII.\n\n         Status:       'Mandatory', 'Optional', or 'Conditionally\n                       Mandatory'\n\n         Multiplicity: 'Single' or 'Multiple' to indicate whether\n                       the entry may be present multiple times.\n\n         Description:  Description of the use of the entry, other\n                       information required to complete the\n                       definition (e.g.: ordering constraints,\n                       interactions between entries).\n\n         Applications that interpret prtChannelInformation should\n         ignore unrecognized entries, so they are not affected if\n         new entry types are added.")
prtInterpreter = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 15))
prtInterpreterTable = MibTable((1, 3, 6, 1, 2, 1, 43, 15, 1))
if mibBuilder.loadTexts:
    prtInterpreterTable.setDescription('')
prtInterpreterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 15, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtInterpreterIndex'))
if mibBuilder.loadTexts:
    prtInterpreterEntry.setDescription("Entries may exist in the table for each device index\n         with a device type of 'printer'.")
prtInterpreterIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtInterpreterIndex.setDescription('A unique value for each PDL or control language for\n         which there exists an interpreter or emulator in the\n         printer. The value is used to identify this interpreter.\n         Although these values may change due to a major\n         reconfiguration of the device (e.g. the addition of new\n         interpreters to the printer), values are expected to\n         remain stable across successive printer power cycles.')
prtInterpreterLangFamily = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 2), PrtInterpreterLangFamilyTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterLangFamily.setDescription('The family name of a Page Description Language (PDL) or\n         control language which this interpreter in the printer\n         can interpret or emulate.')
prtInterpreterLangLevel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 31))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterLangLevel.setDescription("The level of the language which this interpreter is\n         interpreting or emulating.  This might contain a value\n         like '5e' for an interpreter which is emulating level 5e\n         of the PCL language. It might contain '2' for an\n         interpreter which is emulating level 2 of the PostScript\n         language. Similarly it might contain '2' for an\n         interpreter which is emulating level 2 of the HPGL\n         language.")
prtInterpreterLangVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 31))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterLangVersion.setDescription('The date code or version of the language which this\n         interpreter is interpreting or emulating.')
prtInterpreterDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterDescription.setDescription('A string to identify this interpreter in the\n         localization specified by prtGeneralCurrentLocalization\n         as opposed to the language which is being interpreted.\n         It is anticipated that this string will allow\n         manufacturers to unambiguously identify their\n         interpreters.')
prtInterpreterVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 6), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 31))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterVersion.setDescription('The date code, version number, or other product\n         specific information tied to this interpreter.  This\n         value is associated with the interpreter, rather than\n         with the version of the language which is being\n         interpreted or emulated.')
prtInterpreterDefaultOrientation = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 7), PrtPrintOrientationTC()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInterpreterDefaultOrientation.setDescription('The current orientation default for this interpreter.\n         This value may be overridden for a particular job (e.g.,\n         by a command in the input data stream).')
prtInterpreterFeedAddressability = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 8), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterFeedAddressability.setDescription('The maximum interpreter addressability in the feed\n         direction in 10000 prtMarkerAddressabilityUnits (see\n         prtMarkerAddressabilityFeedDir ) for this interpreter.\n         The value (-1) means other and specifically indicates\n         that the sub-unit places no restrictions on this\n         parameter.')
prtInterpreterXFeedAddressability = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 9), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterXFeedAddressability.setDescription('The maximum interpreter addressability in the cross\n         feed direction in 10000 prtMarkerAddressabilityUnits\n         (see prtMarkerAddressabilityXFeedDir) for this\n         interpreter. The value (-1) means other and specifically\n         indicates that the sub-unit places no restrictions on\n         this parameter.')
prtInterpreterDefaultCharSetIn = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 10), CodedCharSet()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInterpreterDefaultCharSetIn.setDescription('The default coded character set for input octets\n         encountered outside a context in which the Page\n         Description Language established the interpretation of\n         the octets. (Input octets are presented to the\n         interpreter through a path defined in the channel\n         group.) This value shall be (2) if there is no default.')
prtInterpreterDefaultCharSetOut = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 11), CodedCharSet()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtInterpreterDefaultCharSetOut.setDescription("The default character set for data coming from this\n         interpreter through the printer's output channel (i.e.\n         the 'backchannel'). This value shall be (2) if there is\n         no default.")
prtInterpreterTwoWay = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 15, 1, 1, 12), PrtInterpreterTwoWayTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtInterpreterTwoWay.setDescription('Indicates whether or not this interpreter returns\n         information back to the host.')
prtConsoleDisplayBuffer = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 16))
prtConsoleDisplayBufferTable = MibTable((1, 3, 6, 1, 2, 1, 43, 16, 5))
if mibBuilder.loadTexts:
    prtConsoleDisplayBufferTable.setDescription('Physical display buffer for printer console display or\n         operator panel')
prtConsoleDisplayBufferEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 16, 5, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtConsoleDisplayBufferIndex'))
if mibBuilder.loadTexts:
    prtConsoleDisplayBufferEntry.setDescription("This table contains one entry for each physical line on\n         the display.  Lines cannot be added or deleted. Entries\n         may exist in the table for each device index with a\n         device type of 'printer'.")
prtConsoleDisplayBufferIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 16, 5, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtConsoleDisplayBufferIndex.setDescription('A unique value for each console line in the printer.\n         The value is used to identify this console line.\n         Although these values may change due to a major\n         reconfiguration of the device (e.g. the addition of new\n         console lines to the printer). Values are normally\n         expected to remain stable across successive printer\n         power cycles.')
prtConsoleDisplayBufferText = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 16, 5, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtConsoleDisplayBufferText.setDescription("The content of a line in the logical display buffer of\n         the operator's console of the printer.  When a write\n         operation occurs, normally a critical message, to one of\n         the LineText strings, the agent should make that line\n         displayable if a physical display is present.  Writing a\n         zero length string clears the line.  It is an\n         implementation-specific matter as to whether the agent\n         allows a line to be overwritten before it has been\n         cleared. Printer generated strings shall be in the\n         localization specified by prtConsoleLocalization.\n         Management Application generated strings should be\n         localized by the Management Application.")
prtConsoleLights = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 17))
prtConsoleLightTable = MibTable((1, 3, 6, 1, 2, 1, 43, 17, 6))
if mibBuilder.loadTexts:
    prtConsoleLightTable.setDescription('')
prtConsoleLightEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 17, 6, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtConsoleLightIndex'))
if mibBuilder.loadTexts:
    prtConsoleLightEntry.setDescription("Entries may exist in the table for each device index\n         with a device type of 'printer'.")
prtConsoleLightIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 17, 6, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    prtConsoleLightIndex.setDescription('A unique value used by the printer to identify this\n         light. Although these values may change due to a major\n         reconfiguration of the device (e.g. the addition of new\n         lights to the printer). Values are normally expected to\n         remain stable across successive printer power cycles.')
prtConsoleOnTime = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 17, 6, 1, 2), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtConsoleOnTime.setDescription('This object, in conjunction with prtConsoleOffTime,\n         defines the current status of the light.  If both\n         prtConsoleOnTime and prtConsoleOffTime are non-zero, the\n         lamp is blinking and the values presented define the on\n         time and off time, respectively, in milliseconds. If\n         prtConsoleOnTime is zero and prtConsoleOffTime is non-\n         zero, the lamp is off. If prtConsoleOffTime is zero and\n         prtConsoleOnTime is non-zero, the lamp is on. If both\n         values are zero the lamp is off.')
prtConsoleOffTime = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 17, 6, 1, 3), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prtConsoleOffTime.setDescription('This object, in conjunction with prtConsoleOnTime,\n         defines the current status of the light. If both\n         prtConsoleOnTime and prtConsoleOffTime are non-zero, the\n         lamp is blinking and the values presented define the on\n         time and off time, respectively, in milliseconds. If\n         prtConsoleOnTime is zero and prtConsoleOffTime is non-\n         zero, the lamp is off. If prtConsoleOffTime is zero and\n         prtConsoleOnTime is non-zero, the lamp is on. If both\n         values are zero the lamp is off.')
prtConsoleColor = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 17, 6, 1, 4), PrtConsoleColorTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtConsoleColor.setDescription('The color of this light.')
prtConsoleDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 17, 6, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtConsoleDescription.setDescription('The vendor description or label of this light in the\n         localization specified by prtConsoleLocalization.')
prtAlert = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 18))
prtAlertTable = MibTable((1, 3, 6, 1, 2, 1, 43, 18, 1))
if mibBuilder.loadTexts:
    prtAlertTable.setDescription('')
prtAlertEntry = MibTableRow((1, 3, 6, 1, 2, 1, 43, 18, 1, 1)).setIndexNames((0, 'HOST-RESOURCES-MIB', 'hrDeviceIndex'), (0, 'Printer-MIB', 'prtAlertIndex'))
if mibBuilder.loadTexts:
    prtAlertEntry.setDescription("Entries may exist in the table for each device\n        index with a device type of 'printer'.")
prtAlertIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertIndex.setDescription('The index value used to determine which alerts have\n         been added or removed from the alert table. This is an\n         incrementing integer starting from zero every time the\n         printer is reset.  When the printer adds an alert to the\n         table, that alert is assigned the next higher integer\n         value from the last item entered into the table.  If the\n         index value reaches its maximum value, the next item\n         entered will cause the index value to roll over and\n         start at zero again.  The first event placed in the\n         alert table after a reset of the printer shall have an\n         index value of 1.  NOTE: The management application will\n         read the alert table when a trap or event notification\n         occurs or at a periodic rate and then parse the table to\n         determine if any new entries were added by comparing the\n         last known index value with the current highest index\n         value. The management application will then update its\n         copy of the alert table.  When the printer discovers\n         that an alert is no longer active, the printer shall\n         remove the row for that alert from the table and shall\n         reduce the number of rows in the table.  The printer may\n         add or delete any number of rows from the table at any\n         time.  The management station can detect when binary\n         change alerts have been deleted by requesting an\n         attribute of each alert, and noting alerts as deleted\n         when that retrieval is not possible.')
prtAlertSeverityLevel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 2), PrtAlertSeverityLevelTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertSeverityLevel.setDescription('The level of severity of this alert table entry.  The\n         printer determines the severity level assigned to each\n         entry into the table.')
prtAlertTrainingLevel = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 3), PrtAlertTrainingLevelTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertTrainingLevel.setDescription('See textual convention PrtAlertTrainingLevelTC')
prtAlertGroup = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 4), PrtAlertGroupTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertGroup.setDescription('The type of sub-unit within the printer model that this\n         alert is related. Input, output, and markers are\n         examples of printer model groups, i.e., examples of\n         types of sub-units. Wherever possible, these\n         enumerations match the sub-identifier that identifies\n         the relevant table in the printmib.')
prtAlertGroupIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertGroupIndex.setDescription('An index of the row within the principle table in the\n         group identified by prtAlertGroup that represents the\n         sub-unit of the printer that caused this alert.  The\n         combination of the prtAlertGroup and the\n         prtAlertGroupIndex defines exactly which printer sub-\n         unit caused the alert; for example, Input #3, Output #2,\n         and Marker #1. Every object in this MIB is indexed with\n         hrDeviceIndex and optionally, another index variable.\n         If this other index variable is present in the table\n         that generated the alert, it will be used as the value\n         for this object.  Otherwise, this value shall be -1.')
prtAlertLocation = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertLocation.setDescription('The sub-unit location that is defined by the printer\n         manufacturer to further refine the location of this\n         alert within the designated sub-unit.  The location is\n         used in conjunction with the Group and GroupIndex\n         values; for example, there is an alert in Input #2 at\n         location number 7. The value (-2) indicates unknown')
prtAlertCode = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 7), PrtAlertCodeTC()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertCode.setDescription('See associated textual convention PrtAlertCodeTC')
prtAlertDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 8), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertDescription.setDescription("A description of this alert entry in the localization\n         specified by prtGeneralCurrentLocalization.  The\n         description is provided by the printer to further\n         elaborate on the enumerated alert or provide information\n         in the case where the code is classified as 'other' or\n         'unknown'.  The printer is required to return a\n         description string but the string may be a null\n         string.")
prtAlertTime = MibTableColumn((1, 3, 6, 1, 2, 1, 43, 18, 1, 1, 9), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prtAlertTime.setDescription('The value of sysUpTime at the time that this alert was\n         generated.')
printerV1Alert = ObjectIdentity((1, 3, 6, 1, 2, 1, 43, 18, 2))
if mibBuilder.loadTexts:
    printerV1Alert.setDescription('The value of the enterprise-specific OID in an SNMPv1\n         trap sent signaling a critical event in the\n         prtAlertTable.')
printerV2AlertPrefix = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 18, 2, 0))
printerV2Alert = NotificationType((1, 3, 6, 1, 2, 1, 43, 18, 2, 0, 1)).setObjects(*(('Printer-MIB', 'prtAlertIndex'), ('Printer-MIB', 'prtAlertSeverityLevel'), ('Printer-MIB', 'prtAlertGroup'), ('Printer-MIB', 'prtAlertGroupIndex'), ('Printer-MIB', 'prtAlertLocation'), ('Printer-MIB', 'prtAlertCode')))
if mibBuilder.loadTexts:
    printerV2Alert.setDescription('This trap is sent whenever a critical event is added to\n         the prtAlertTable.')
prtMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 2))
prtMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 43, 2, 1)).setObjects(*(('Printer-MIB', 'prtGeneralGroup'), ('Printer-MIB', 'prtInputGroup'), ('Printer-MIB', 'prtOutputGroup'), ('Printer-MIB', 'prtMarkerGroup'), ('Printer-MIB', 'prtMediaPathGroup'), ('Printer-MIB', 'prtChannelGroup'), ('Printer-MIB', 'prtInterpreterGroup'), ('Printer-MIB', 'prtConsoleGroup'), ('Printer-MIB', 'prtAlertTableGroup')))
if mibBuilder.loadTexts:
    prtMIBCompliance.setDescription('The compliance statement for agents that implement the\n        printer MIB.')
prtMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 43, 2, 2))
prtGeneralGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 1)).setObjects(*(('Printer-MIB', 'prtGeneralConfigChanges'), ('Printer-MIB', 'prtGeneralCurrentLocalization'), ('Printer-MIB', 'prtGeneralReset'), ('Printer-MIB', 'prtCoverDescription'), ('Printer-MIB', 'prtCoverStatus'), ('Printer-MIB', 'prtLocalizationLanguage'), ('Printer-MIB', 'prtLocalizationCountry'), ('Printer-MIB', 'prtLocalizationCharacterSet'), ('Printer-MIB', 'prtStorageRefIndex'), ('Printer-MIB', 'prtDeviceRefIndex'), ('Printer-MIB', 'prtGeneralPrinterName'), ('Printer-MIB', 'prtGeneralSerialNumber')))
if mibBuilder.loadTexts:
    prtGeneralGroup.setDescription('The general printer group.')
prtResponsiblePartyGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 2)).setObjects(*(('Printer-MIB', 'prtGeneralCurrentOperator'), ('Printer-MIB', 'prtGeneralServicePerson')))
if mibBuilder.loadTexts:
    prtResponsiblePartyGroup.setDescription('The responsible party group contains contact\n         information for humans responsible for the printer.')
prtInputGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 3)).setObjects(*(('Printer-MIB', 'prtInputDefaultIndex'), ('Printer-MIB', 'prtInputType'), ('Printer-MIB', 'prtInputDimUnit'), ('Printer-MIB', 'prtInputMediaDimFeedDirDeclared'), ('Printer-MIB', 'prtInputMediaDimXFeedDirDeclared'), ('Printer-MIB', 'prtInputMediaDimFeedDirChosen'), ('Printer-MIB', 'prtInputMediaDimXFeedDirChosen'), ('Printer-MIB', 'prtInputCapacityUnit'), ('Printer-MIB', 'prtInputMaxCapacity'), ('Printer-MIB', 'prtInputCurrentLevel'), ('Printer-MIB', 'prtInputStatus'), ('Printer-MIB', 'prtInputMediaName')))
if mibBuilder.loadTexts:
    prtInputGroup.setDescription('The input group.')
prtExtendedInputGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 4)).setObjects(*(('Printer-MIB', 'prtInputName'), ('Printer-MIB', 'prtInputVendorName'), ('Printer-MIB', 'prtInputModel'), ('Printer-MIB', 'prtInputVersion'), ('Printer-MIB', 'prtInputSerialNumber'), ('Printer-MIB', 'prtInputDescription'), ('Printer-MIB', 'prtInputSecurity')))
if mibBuilder.loadTexts:
    prtExtendedInputGroup.setDescription('The extended input group.')
prtInputMediaGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 5)).setObjects(*(('Printer-MIB', 'prtInputMediaWeight'), ('Printer-MIB', 'prtInputMediaType'), ('Printer-MIB', 'prtInputMediaColor'), ('Printer-MIB', 'prtInputMediaFormParts')))
if mibBuilder.loadTexts:
    prtInputMediaGroup.setDescription('The input media group.')
prtOutputGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 6)).setObjects(*(('Printer-MIB', 'prtOutputDefaultIndex'), ('Printer-MIB', 'prtOutputType'), ('Printer-MIB', 'prtOutputCapacityUnit'), ('Printer-MIB', 'prtOutputMaxCapacity'), ('Printer-MIB', 'prtOutputRemainingCapacity'), ('Printer-MIB', 'prtOutputStatus')))
if mibBuilder.loadTexts:
    prtOutputGroup.setDescription('The output group.')
prtExtendedOutputGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 7)).setObjects(*(('Printer-MIB', 'prtOutputName'), ('Printer-MIB', 'prtOutputVendorName'), ('Printer-MIB', 'prtOutputModel'), ('Printer-MIB', 'prtOutputVersion'), ('Printer-MIB', 'prtOutputSerialNumber'), ('Printer-MIB', 'prtOutputDescription'), ('Printer-MIB', 'prtOutputSecurity')))
if mibBuilder.loadTexts:
    prtExtendedOutputGroup.setDescription('The extended output group.')
prtOutputDimensionsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 8)).setObjects(*(('Printer-MIB', 'prtOutputDimUnit'), ('Printer-MIB', 'prtOutputMaxDimFeedDir'), ('Printer-MIB', 'prtOutputMaxDimXFeedDir'), ('Printer-MIB', 'prtOutputMinDimFeedDir'), ('Printer-MIB', 'prtOutputMinDimXFeedDir')))
if mibBuilder.loadTexts:
    prtOutputDimensionsGroup.setDescription('The output dimensions group')
prtOutputFeaturesGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 9)).setObjects(*(('Printer-MIB', 'prtOutputStackingOrder'), ('Printer-MIB', 'prtOutputPageDeliveryOrientation'), ('Printer-MIB', 'prtOutputBursting'), ('Printer-MIB', 'prtOutputDecollating'), ('Printer-MIB', 'prtOutputPageCollated'), ('Printer-MIB', 'prtOutputOffsetStacking')))
if mibBuilder.loadTexts:
    prtOutputFeaturesGroup.setDescription('The output features group.')
prtMarkerGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 10)).setObjects(*(('Printer-MIB', 'prtMarkerDefaultIndex'), ('Printer-MIB', 'prtMarkerMarkTech'), ('Printer-MIB', 'prtMarkerCounterUnit'), ('Printer-MIB', 'prtMarkerLifeCount'), ('Printer-MIB', 'prtMarkerPowerOnCount'), ('Printer-MIB', 'prtMarkerProcessColorants'), ('Printer-MIB', 'prtMarkerSpotColorants'), ('Printer-MIB', 'prtMarkerAddressabilityUnit'), ('Printer-MIB', 'prtMarkerAddressabilityFeedDir'), ('Printer-MIB', 'prtMarkerAddressabilityXFeedDir'), ('Printer-MIB', 'prtMarkerNorthMargin'), ('Printer-MIB', 'prtMarkerSouthMargin'), ('Printer-MIB', 'prtMarkerWestMargin'), ('Printer-MIB', 'prtMarkerEastMargin'), ('Printer-MIB', 'prtMarkerStatus')))
if mibBuilder.loadTexts:
    prtMarkerGroup.setDescription('The marker group.')
prtMarkerSuppliesGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 11)).setObjects(*(('Printer-MIB', 'prtMarkerSuppliesMarkerIndex'), ('Printer-MIB', 'prtMarkerSuppliesColorantIndex'), ('Printer-MIB', 'prtMarkerSuppliesClass'), ('Printer-MIB', 'prtMarkerSuppliesType'), ('Printer-MIB', 'prtMarkerSuppliesDescription'), ('Printer-MIB', 'prtMarkerSuppliesSupplyUnit'), ('Printer-MIB', 'prtMarkerSuppliesMaxCapacity'), ('Printer-MIB', 'prtMarkerSuppliesLevel')))
if mibBuilder.loadTexts:
    prtMarkerSuppliesGroup.setDescription('The marker supplies group.')
prtMarkerColorantGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 12)).setObjects(*(('Printer-MIB', 'prtMarkerColorantMarkerIndex'), ('Printer-MIB', 'prtMarkerColorantRole'), ('Printer-MIB', 'prtMarkerColorantValue'), ('Printer-MIB', 'prtMarkerColorantTonality')))
if mibBuilder.loadTexts:
    prtMarkerColorantGroup.setDescription('The marker colorant group.')
prtMediaPathGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 13)).setObjects(*(('Printer-MIB', 'prtMediaPathDefaultIndex'), ('Printer-MIB', 'prtMediaPathMaxSpeedPrintUnit'), ('Printer-MIB', 'prtMediaPathMediaSizeUnit'), ('Printer-MIB', 'prtMediaPathMaxSpeed'), ('Printer-MIB', 'prtMediaPathMaxMediaFeedDir'), ('Printer-MIB', 'prtMediaPathMaxMediaXFeedDir'), ('Printer-MIB', 'prtMediaPathMinMediaFeedDir'), ('Printer-MIB', 'prtMediaPathMinMediaXFeedDir'), ('Printer-MIB', 'prtMediaPathType'), ('Printer-MIB', 'prtMediaPathDescription'), ('Printer-MIB', 'prtMediaPathStatus')))
if mibBuilder.loadTexts:
    prtMediaPathGroup.setDescription('The media path group.')
prtChannelGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 14)).setObjects(*(('Printer-MIB', 'prtChannelType'), ('Printer-MIB', 'prtChannelProtocolVersion'), ('Printer-MIB', 'prtChannelCurrentJobCntlLangIndex'), ('Printer-MIB', 'prtChannelDefaultPageDescLangIndex'), ('Printer-MIB', 'prtChannelState'), ('Printer-MIB', 'prtChannelIfIndex'), ('Printer-MIB', 'prtChannelStatus'), ('Printer-MIB', 'prtChannelInformation')))
if mibBuilder.loadTexts:
    prtChannelGroup.setDescription('The channel group.')
prtInterpreterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 15)).setObjects(*(('Printer-MIB', 'prtInterpreterLangFamily'), ('Printer-MIB', 'prtInterpreterLangLevel'), ('Printer-MIB', 'prtInterpreterLangVersion'), ('Printer-MIB', 'prtInterpreterDescription'), ('Printer-MIB', 'prtInterpreterVersion'), ('Printer-MIB', 'prtInterpreterDefaultOrientation'), ('Printer-MIB', 'prtInterpreterFeedAddressability'), ('Printer-MIB', 'prtInterpreterXFeedAddressability'), ('Printer-MIB', 'prtInterpreterDefaultCharSetIn'), ('Printer-MIB', 'prtInterpreterDefaultCharSetOut'), ('Printer-MIB', 'prtInterpreterTwoWay')))
if mibBuilder.loadTexts:
    prtInterpreterGroup.setDescription('The interpreter group.')
prtConsoleGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 16)).setObjects(*(('Printer-MIB', 'prtConsoleLocalization'), ('Printer-MIB', 'prtConsoleNumberOfDisplayLines'), ('Printer-MIB', 'prtConsoleNumberOfDisplayChars'), ('Printer-MIB', 'prtConsoleDisable'), ('Printer-MIB', 'prtConsoleDisplayBufferText'), ('Printer-MIB', 'prtConsoleOnTime'), ('Printer-MIB', 'prtConsoleOffTime'), ('Printer-MIB', 'prtConsoleColor'), ('Printer-MIB', 'prtConsoleDescription')))
if mibBuilder.loadTexts:
    prtConsoleGroup.setDescription('The console group.')
prtAlertTableGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 17)).setObjects(*(('Printer-MIB', 'prtAlertIndex'), ('Printer-MIB', 'prtAlertCriticalEvents'), ('Printer-MIB', 'prtAlertAllEvents'), ('Printer-MIB', 'prtAlertSeverityLevel'), ('Printer-MIB', 'prtAlertTrainingLevel'), ('Printer-MIB', 'prtAlertGroup'), ('Printer-MIB', 'prtAlertGroupIndex'), ('Printer-MIB', 'prtAlertLocation'), ('Printer-MIB', 'prtAlertCode'), ('Printer-MIB', 'prtAlertDescription'), ('Printer-MIB', 'prtAlertTime')))
if mibBuilder.loadTexts:
    prtAlertTableGroup.setDescription('The alert table group.')
prtAuxiliarySheetGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 19)).setObjects(*(('Printer-MIB', 'prtAuxiliarySheetStartupPage'), ('Printer-MIB', 'prtAuxiliarySheetBannerPage')))
if mibBuilder.loadTexts:
    prtAuxiliarySheetGroup.setDescription('The auxiliary sheet group.')
prtInputSwitchingGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 43, 2, 2, 20)).setObjects(*(('Printer-MIB', 'prtInputMediaLoadTimeout'), ('Printer-MIB', 'prtInputNextIndex')))
if mibBuilder.loadTexts:
    prtInputSwitchingGroup.setDescription('The input switching group.')
mibBuilder.exportSymbols('Printer-MIB', prtInputStatus=prtInputStatus, prtChannelState=prtChannelState, prtGeneralPrinterName=prtGeneralPrinterName, prtMIBCompliance=prtMIBCompliance, prtMarkerEntry=prtMarkerEntry, prtInputEntry=prtInputEntry, prtGeneralServicePerson=prtGeneralServicePerson, prtConsoleNumberOfDisplayChars=prtConsoleNumberOfDisplayChars, prtConsoleDescription=prtConsoleDescription, prtInputGroup=prtInputGroup, prtConsoleDisplayBufferText=prtConsoleDisplayBufferText, printerV2AlertPrefix=printerV2AlertPrefix, prtCoverIndex=prtCoverIndex, prtDeviceRefEntry=prtDeviceRefEntry, prtAuxiliarySheetStartupPage=prtAuxiliarySheetStartupPage, prtMarkerAddressabilityFeedDir=prtMarkerAddressabilityFeedDir, prtStorageRefIndex=prtStorageRefIndex, prtOutputBursting=prtOutputBursting, prtMediaPath=prtMediaPath, prtOutputOffsetStacking=prtOutputOffsetStacking, prtInterpreterTwoWay=prtInterpreterTwoWay, prtAlertCode=prtAlertCode, prtGeneralEntry=prtGeneralEntry, prtInputMediaDimXFeedDirChosen=prtInputMediaDimXFeedDirChosen, prtMediaPathMinMediaFeedDir=prtMediaPathMinMediaFeedDir, prtInputNextIndex=prtInputNextIndex, PrtInterpreterLangFamilyTC=PrtInterpreterLangFamilyTC, PrtPrintOrientationTC=PrtPrintOrientationTC, PrtCoverStatusTC=PrtCoverStatusTC, prtGeneralReset=prtGeneralReset, prtMediaPathGroup=prtMediaPathGroup, prtAlertDescription=prtAlertDescription, prtChannel=prtChannel, prtInputMediaDimFeedDirDeclared=prtInputMediaDimFeedDirDeclared, prtOutputRemainingCapacity=prtOutputRemainingCapacity, prtInterpreterDefaultOrientation=prtInterpreterDefaultOrientation, prtMarkerDefaultIndex=prtMarkerDefaultIndex, prtInterpreterTable=prtInterpreterTable, prtOutputCapacityUnit=prtOutputCapacityUnit, prtConsoleOnTime=prtConsoleOnTime, prtCoverTable=prtCoverTable, prtInterpreterLangLevel=prtInterpreterLangLevel, prtInterpreterGroup=prtInterpreterGroup, prtMIBConformance=prtMIBConformance, prtOutputVendorName=prtOutputVendorName, prtInputSecurity=prtInputSecurity, prtConsoleColor=prtConsoleColor, prtGeneralGroup=prtGeneralGroup, prtInputMediaName=prtInputMediaName, PrtMarkerColorantRoleTC=PrtMarkerColorantRoleTC, PrtOutputPageDeliveryOrientationTC=PrtOutputPageDeliveryOrientationTC, prtMarkerColorantIndex=prtMarkerColorantIndex, prtLocalizationIndex=prtLocalizationIndex, prtMarkerSuppliesLevel=prtMarkerSuppliesLevel, prtMediaPathType=prtMediaPathType, prtResponsiblePartyGroup=prtResponsiblePartyGroup, prtInputMediaType=prtInputMediaType, prtMarkerColorantValue=prtMarkerColorantValue, prtAuxiliarySheetGroup=prtAuxiliarySheetGroup, PrtGeneralResetTC=PrtGeneralResetTC, prtGeneralSerialNumber=prtGeneralSerialNumber, prtMarkerSuppliesClass=prtMarkerSuppliesClass, PrtMarkerSuppliesClassTC=PrtMarkerSuppliesClassTC, prtMarkerSupplies=prtMarkerSupplies, prtAlertGroupIndex=prtAlertGroupIndex, CodedCharSet=CodedCharSet, prtMarkerLifeCount=prtMarkerLifeCount, prtInputMediaWeight=prtInputMediaWeight, prtMarkerMarkTech=prtMarkerMarkTech, prtLocalizationEntry=prtLocalizationEntry, prtAlertIndex=prtAlertIndex, prtMarkerSouthMargin=prtMarkerSouthMargin, prtMarkerIndex=prtMarkerIndex, prtInputMediaGroup=prtInputMediaGroup, prtAlertCriticalEvents=prtAlertCriticalEvents, prtInputCapacityUnit=prtInputCapacityUnit, prtChannelEntry=prtChannelEntry, prtMediaPathDefaultIndex=prtMediaPathDefaultIndex, prtMarkerGroup=prtMarkerGroup, prtAlertSeverityLevel=prtAlertSeverityLevel, prtChannelTable=prtChannelTable, prtAlertTableGroup=prtAlertTableGroup, prtGeneral=prtGeneral, prtMediaPathDescription=prtMediaPathDescription, prtGeneralCurrentLocalization=prtGeneralCurrentLocalization, prtMarkerWestMargin=prtMarkerWestMargin, prtMediaPathMaxSpeedPrintUnit=prtMediaPathMaxSpeedPrintUnit, PrtChannelTypeTC=PrtChannelTypeTC, prtInputSerialNumber=prtInputSerialNumber, prtInputName=prtInputName, prtCover=prtCover, prtMarkerSpotColorants=prtMarkerSpotColorants, prtMarkerColorantRole=prtMarkerColorantRole, prtMarkerEastMargin=prtMarkerEastMargin, prtInputMediaDimXFeedDirDeclared=prtInputMediaDimXFeedDirDeclared, prtMediaPathEntry=prtMediaPathEntry, prtOutputTable=prtOutputTable, prtInterpreterFeedAddressability=prtInterpreterFeedAddressability, prtConsoleDisplayBufferEntry=prtConsoleDisplayBufferEntry, prtMediaPathMaxMediaFeedDir=prtMediaPathMaxMediaFeedDir, prtMarkerColorantGroup=prtMarkerColorantGroup, prtAlert=prtAlert, prtConsoleLightTable=prtConsoleLightTable, prtOutputVersion=prtOutputVersion, prtInterpreterDefaultCharSetIn=prtInterpreterDefaultCharSetIn, prtInputMediaColor=prtInputMediaColor, prtMarkerSuppliesColorantIndex=prtMarkerSuppliesColorantIndex, PrtInputTypeTC=PrtInputTypeTC, prtGeneralConfigChanges=prtGeneralConfigChanges, prtStorageRefEntry=prtStorageRefEntry, prtInputVendorName=prtInputVendorName, PrtAlertSeverityLevelTC=PrtAlertSeverityLevelTC, prtLocalization=prtLocalization, prtMarkerSuppliesMaxCapacity=prtMarkerSuppliesMaxCapacity, prtChannelType=prtChannelType, prtInputCurrentLevel=prtInputCurrentLevel, PrtMarkerSuppliesTypeTC=PrtMarkerSuppliesTypeTC, prtMarkerSuppliesSupplyUnit=prtMarkerSuppliesSupplyUnit, printerV2Alert=printerV2Alert, prtLocalizationLanguage=prtLocalizationLanguage, prtInterpreterDefaultCharSetOut=prtInterpreterDefaultCharSetOut, prtCoverEntry=prtCoverEntry, prtMarkerSuppliesIndex=prtMarkerSuppliesIndex, prtCoverStatus=prtCoverStatus, prtAlertAllEvents=prtAlertAllEvents, prtOutputMaxCapacity=prtOutputMaxCapacity, prtOutputPageDeliveryOrientation=prtOutputPageDeliveryOrientation, PrtAlertCodeTC=PrtAlertCodeTC, prtInputMaxCapacity=prtInputMaxCapacity, PrtSubUnitStatusTC=PrtSubUnitStatusTC, prtMediaPathTable=prtMediaPathTable, prtOutputGroup=prtOutputGroup, prtMarkerPowerOnCount=prtMarkerPowerOnCount, prtMarkerNorthMargin=prtMarkerNorthMargin, PrtMediaPathMaxSpeedPrintUnitTC=PrtMediaPathMaxSpeedPrintUnitTC, prtInputDimUnit=prtInputDimUnit, prtInputModel=prtInputModel, prtOutputModel=prtOutputModel, prtGeneralTable=prtGeneralTable, PrtOutputStackingOrderTC=PrtOutputStackingOrderTC, prtAlertTable=prtAlertTable, prtConsoleGroup=prtConsoleGroup, prtOutputMinDimFeedDir=prtOutputMinDimFeedDir, prtOutputDimensionsGroup=prtOutputDimensionsGroup, prtLocalizationCountry=prtLocalizationCountry, prtDeviceRefTable=prtDeviceRefTable, prtAlertEntry=prtAlertEntry, prtConsoleDisplayBufferTable=prtConsoleDisplayBufferTable, prtOutputMaxDimFeedDir=prtOutputMaxDimFeedDir, prtMarkerSuppliesTable=prtMarkerSuppliesTable, PrtOutputTypeTC=PrtOutputTypeTC, prtOutputName=prtOutputName, prtChannelProtocolVersion=prtChannelProtocolVersion, prtInterpreterLangFamily=prtInterpreterLangFamily, prtInputMediaFormParts=prtInputMediaFormParts, prtInputTable=prtInputTable, prtMarkerSuppliesDescription=prtMarkerSuppliesDescription, prtOutputType=prtOutputType, prtInputIndex=prtInputIndex, printerV1Alert=printerV1Alert, prtChannelGroup=prtChannelGroup, prtMarker=prtMarker, prtMarkerSuppliesEntry=prtMarkerSuppliesEntry, prtMediaPathMinMediaXFeedDir=prtMediaPathMinMediaXFeedDir, prtMediaPathStatus=prtMediaPathStatus, prtMarkerColorantEntry=prtMarkerColorantEntry, prtOutputEntry=prtOutputEntry, prtLocalizationTable=prtLocalizationTable, prtMarkerSuppliesType=prtMarkerSuppliesType, prtConsoleDisplayBuffer=prtConsoleDisplayBuffer, prtMarkerColorantMarkerIndex=prtMarkerColorantMarkerIndex, PrtMediaPathTypeTC=PrtMediaPathTypeTC, prtExtendedInputGroup=prtExtendedInputGroup, PrtMarkerMarkTechTC=PrtMarkerMarkTechTC, prtOutputStatus=prtOutputStatus, prtMarkerColorantTonality=prtMarkerColorantTonality, prtInterpreterIndex=prtInterpreterIndex, prtOutputSerialNumber=prtOutputSerialNumber, prtMarkerStatus=prtMarkerStatus, PYSNMP_MODULE_ID=printmib, prtOutputDimUnit=prtOutputDimUnit, prtMediaPathIndex=prtMediaPathIndex, prtMarkerSuppliesGroup=prtMarkerSuppliesGroup, prtOutputDefaultIndex=prtOutputDefaultIndex, prtOutputStackingOrder=prtOutputStackingOrder, prtInterpreterEntry=prtInterpreterEntry, prtConsoleDisable=prtConsoleDisable, PrtChannelStateTC=PrtChannelStateTC, PrtAlertGroupTC=PrtAlertGroupTC, prtInputDescription=prtInputDescription, prtInputSwitchingGroup=prtInputSwitchingGroup, prtAlertLocation=prtAlertLocation, prtInterpreterXFeedAddressability=prtInterpreterXFeedAddressability, prtChannelStatus=prtChannelStatus, prtChannelInformation=prtChannelInformation, prtExtendedOutputGroup=prtExtendedOutputGroup, prtConsoleLightIndex=prtConsoleLightIndex, prtInputMediaDimFeedDirChosen=prtInputMediaDimFeedDirChosen, prtMarkerTable=prtMarkerTable, prtOutputDescription=prtOutputDescription, PrtAlertTrainingLevelTC=PrtAlertTrainingLevelTC, prtInputType=prtInputType, prtChannelDefaultPageDescLangIndex=prtChannelDefaultPageDescLangIndex, PrtMarkerCounterUnitTC=PrtMarkerCounterUnitTC, prtInputMediaLoadTimeout=prtInputMediaLoadTimeout, PrtCapacityUnitTC=PrtCapacityUnitTC, prtDeviceRefIndex=prtDeviceRefIndex, prtMarkerProcessColorants=prtMarkerProcessColorants, prtChannelCurrentJobCntlLangIndex=prtChannelCurrentJobCntlLangIndex, prtConsoleLightEntry=prtConsoleLightEntry, prtInputDefaultIndex=prtInputDefaultIndex, prtOutputFeaturesGroup=prtOutputFeaturesGroup, PrtConsoleColorTC=PrtConsoleColorTC, prtAlertTrainingLevel=prtAlertTrainingLevel, prtConsoleOffTime=prtConsoleOffTime, prtCoverDescription=prtCoverDescription, prtStorageRefSeqNumber=prtStorageRefSeqNumber, prtOutput=prtOutput, prtMarkerColorant=prtMarkerColorant, prtAlertGroup=prtAlertGroup, prtOutputPageCollated=prtOutputPageCollated, prtOutputDecollating=prtOutputDecollating, prtOutputMaxDimXFeedDir=prtOutputMaxDimXFeedDir, prtInterpreterDescription=prtInterpreterDescription, prtAlertTime=prtAlertTime, prtOutputIndex=prtOutputIndex, prtMarkerColorantTable=prtMarkerColorantTable, prtOutputMinDimXFeedDir=prtOutputMinDimXFeedDir, prtInterpreter=prtInterpreter, prtInterpreterLangVersion=prtInterpreterLangVersion, prtConsoleNumberOfDisplayLines=prtConsoleNumberOfDisplayLines, PrtMediaUnitTC=PrtMediaUnitTC, printmib=printmib, prtInput=prtInput, prtMarkerAddressabilityXFeedDir=prtMarkerAddressabilityXFeedDir, prtMediaPathMaxMediaXFeedDir=prtMediaPathMaxMediaXFeedDir, prtChannelIndex=prtChannelIndex, prtChannelIfIndex=prtChannelIfIndex, prtGeneralCurrentOperator=prtGeneralCurrentOperator, prtLocalizationCharacterSet=prtLocalizationCharacterSet, prtConsoleLocalization=prtConsoleLocalization, prtMIBGroups=prtMIBGroups, prtMarkerAddressabilityUnit=prtMarkerAddressabilityUnit, PresentOnOff=PresentOnOff, prtConsoleLights=prtConsoleLights, prtAuxiliarySheetBannerPage=prtAuxiliarySheetBannerPage, PrtInterpreterTwoWayTC=PrtInterpreterTwoWayTC, prtStorageRefTable=prtStorageRefTable, PrtMarkerSuppliesSupplyUnitTC=PrtMarkerSuppliesSupplyUnitTC, prtOutputSecurity=prtOutputSecurity, prtMediaPathMediaSizeUnit=prtMediaPathMediaSizeUnit, prtMarkerSuppliesMarkerIndex=prtMarkerSuppliesMarkerIndex, prtDeviceRefSeqNumber=prtDeviceRefSeqNumber, prtConsoleDisplayBufferIndex=prtConsoleDisplayBufferIndex)
mibBuilder.exportSymbols('Printer-MIB', prtMediaPathMaxSpeed=prtMediaPathMaxSpeed, prtInputVersion=prtInputVersion, prtInterpreterVersion=prtInterpreterVersion, prtMarkerCounterUnit=prtMarkerCounterUnit)