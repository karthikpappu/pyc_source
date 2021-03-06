# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DS3-MIB.py
# Compiled at: 2016-02-13 18:11:02
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, ValueSizeConstraint, ValueRangeConstraint, SingleValueConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'ValueSizeConstraint', 'ValueRangeConstraint', 'SingleValueConstraint', 'ConstraintsIntersection')
(InterfaceIndex,) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex')
(PerfTotalCount, PerfIntervalCount, PerfCurrentCount) = mibBuilder.importSymbols('PerfHist-TC-MIB', 'PerfTotalCount', 'PerfIntervalCount', 'PerfCurrentCount')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(transmission, ModuleIdentity, Integer32, MibIdentifier, Counter64, iso, Unsigned32, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter32, IpAddress, TimeTicks, NotificationType, Gauge32, Bits, ObjectIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'transmission', 'ModuleIdentity', 'Integer32', 'MibIdentifier', 'Counter64', 'iso', 'Unsigned32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter32', 'IpAddress', 'TimeTicks', 'NotificationType', 'Gauge32', 'Bits', 'ObjectIdentity')
(DisplayString, TruthValue, TextualConvention, TimeStamp) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TruthValue', 'TextualConvention', 'TimeStamp')
ds3 = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 30))
if mibBuilder.loadTexts:
    ds3.setLastUpdated('9609261755Z')
if mibBuilder.loadTexts:
    ds3.setOrganization('IETF Trunk MIB Working Group')
if mibBuilder.loadTexts:
    ds3.setContactInfo('        David Fowler\n\n                 Postal: Newbridge Networks Corporation\n                         600 March Road\n                         Kanata, Ontario, Canada K2K 2E6\n\n                         Tel: +1 613 591 3600\n                         Fax: +1 613 599 3669\n\n                 E-mail: davef@newbridge.com')
if mibBuilder.loadTexts:
    ds3.setDescription('The is the MIB module that describes\n                    DS3 and E3 interfaces objects.')
dsx3ConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 5))
if mibBuilder.loadTexts:
    dsx3ConfigTable.setDescription('The DS3/E3 Configuration table.')
dsx3ConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 5, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3LineIndex'))
if mibBuilder.loadTexts:
    dsx3ConfigEntry.setDescription('An entry in the DS3/E3 Configuration table.')
dsx3LineIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3LineIndex.setDescription('This object should be made equal to ifIndex.  The\n                      next paragraph describes its previous usage.\n                      Making the object equal to ifIndex allows propoer\n                      use of ifStackTable.\n\n                      Previously, this object was the identifier of a\n                      DS3/E3 Interface on a managed device.  If there is\n                      an ifEntry that is directly associated with this\n                      and only this DS3/E3 interface, it should have the\n                      same value as ifIndex.  Otherwise, number the\n                      dsx3LineIndices with an unique identifier\n                      following the rules of choosing a number that is\n                      greater than ifNumber and numbering the inside\n                      interfaces (e.g., equipment side) with even\n                      numbers and outside interfaces (e.g, network side)\n                      with odd numbers.')
dsx3IfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 2), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IfIndex.setDescription('This value for this object is equal to the value\n                      of ifIndex from the Interfaces table of MIB II\n                      (RFC 1213).')
dsx3TimeElapsed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 899))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TimeElapsed.setDescription('The number of seconds that have elapsed since the\n                      beginning of the near end current error-\n                      measurement period.')
dsx3ValidIntervals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3ValidIntervals.setDescription('The number of previous near end intervals for\n                      which valid data was collected.  The value will be\n                      96 unless the interface was brought online within\n                      the last 24 hours, in which case the value will be\n                      the number of complete 15 minute near end\n                      intervals since the interface has been online.  In\n                      the case where the agent is a proxy, it is\n                      possible that some intervals are unavailable.  In\n                      this case, this interval is the maximum interval\n                      number for which valid data is available.')
dsx3LineType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(('dsx3other', 1), ('dsx3M23', 2), ('dsx3SYNTRAN', 3), ('dsx3CbitParity', 4), ('dsx3ClearChannel', 5), ('e3other', 6), ('e3Framed', 7), ('e3Plcp', 8)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3LineType.setDescription('This variable indicates the variety of DS3 C-bit\n                      or E3 application implementing this interface. The\n                      type of interface affects the interpretation of\n                      the usage and error statistics.  The rate of DS3\n                      is 44.736 Mbps and E3 is 34.368 Mbps.  The\n                      dsx3ClearChannel value means that the C-bits are\n                      not used except for sending/receiving AIS.\n                      The values, in sequence, describe:\n\n                      TITLE:            SPECIFICATION:\n                      dsx3M23            ANSI T1.107-1988 [9]\n                      dsx3SYNTRAN        ANSI T1.107-1988 [9]\n                      dsx3CbitParity     ANSI T1.107a-1990 [9a]\n                      dsx3ClearChannel   ANSI T1.102-1987 [8]\n\n\n                      e3Framed           CCITT G.751 [12]\n                      e3Plcp             ETSI T/NA(91)18 [13].')
dsx3LineCoding = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('dsx3Other', 1), ('dsx3B3ZS', 2), ('e3HDB3', 3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3LineCoding.setDescription('This variable describes the variety of Zero Code\n                      Suppression used on this interface, which in turn\n                      affects a number of its characteristics.\n\n                      dsx3B3ZS and e3HDB3 refer to the use of specified\n                      patterns of normal bits and bipolar violations\n                      which are used to replace sequences of zero bits\n                      of a specified length.')
dsx3SendCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('dsx3SendNoCode', 1), ('dsx3SendLineCode', 2), ('dsx3SendPayloadCode', 3), ('dsx3SendResetCode', 4), ('dsx3SendDS1LoopCode', 5), ('dsx3SendTestPattern', 6)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3SendCode.setDescription('This variable indicates what type of code is\n                      being sent across the DS3/E3 interface by the\n                      device.  (These are optional for E3 interfaces.)\n                      Setting this variable causes the interface to\n                      begin sending the code requested.\n                      The values mean:\n\n                         dsx3SendNoCode\n                             sending looped or normal data\n\n\n                         dsx3SendLineCode\n                             sending a request for a line loopback\n\n                         dsx3SendPayloadCode\n                             sending a request for a payload loopback\n                             (i.e., all DS1/E1s in a DS3/E3 frame)\n\n                         dsx3SendResetCode\n                             sending a loopback deactivation request\n\n                         dsx3SendDS1LoopCode\n                             requesting to loopback a particular DS1/E1\n                             within a DS3/E3 frame\n\n                         dsx3SendTestPattern\n                             sending a test pattern.')
dsx3CircuitIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 8), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3CircuitIdentifier.setDescription("This variable contains the transmission vendor's\n                      circuit identifier, for the purpose of\n                      facilitating troubleshooting.")
dsx3LoopbackConfig = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('dsx3NoLoop', 1), ('dsx3PayloadLoop', 2), ('dsx3LineLoop', 3), ('dsx3OtherLoop', 4), ('dsx3InwardLoop', 5), ('dsx3DualLoop', 6)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3LoopbackConfig.setDescription("This variable represents the desired loopback\n                    configuration of the DS3/E3 interface.\n                    The values mean:\n\n                    dsx3NoLoop\n\n\n                      Not in the loopback state.  A device that is\n                      not capable of performing a loopback on\n                      the interface shall always return this as\n                      its value.\n\n                    dsx3PayloadLoop\n                      The received signal at this interface is looped\n                      through the device.  Typically the received signal\n                      is looped back for retransmission after it has\n                      passed through the device's framing function.\n\n                    dsx3LineLoop\n                      The received signal at this interface does not\n                      go through the device (minimum penetration) but\n                      is looped back out.\n\n                    dsx3OtherLoop\n                      Loopbacks that are not defined here.\n\n                    dsx3InwardLoop\n                      The sent signal at this interface is looped back\n                      through the device.\n\n                    dsx3DualLoop\n                      Both dsx1LineLoop and dsx1InwardLoop will be\n                      active simultaneously.")
dsx3LineStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 4095))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3LineStatus.setDescription('This variable indicates the Line Status of the\n                      interface.  It contains loopback state information\n                      and failure state information.  The dsx3LineStatus\n                      is a bit map represented as a sum, therefore, it\n                      can represent multiple failures and a loopback\n                      (see dsx3LoopbackConfig object for the type of\n                      loopback) simultaneously.  The dsx3NoAlarm must be\n                      set if and only if no other flag is set.\n\n                      If the dsx3loopbackState bit is set, the loopback\n                      in effect can be determined from the\n                      dsx3loopbackConfig object.\n\n\n            The various bit positions are:\n             1     dsx3NoAlarm         No alarm present\n             2     dsx3RcvRAIFailure   Receiving Yellow/Remote\n                                       Alarm Indication\n             4     dsx3XmitRAIAlarm    Transmitting Yellow/Remote\n                                       Alarm Indication\n             8     dsx3RcvAIS          Receiving AIS failure state\n            16     dsx3XmitAIS         Transmitting AIS\n            32     dsx3LOF             Receiving LOF failure state\n            64     dsx3LOS             Receiving LOS failure state\n           128     dsx3LoopbackState   Looping the received signal\n           256     dsx3RcvTestCode     Receiving a Test Pattern\n           512     dsx3OtherFailure    any line status not defined\n                                       here\n          1024     dsx3UnavailSigState Near End in Unavailable Signal\n                                       State\n          2048     dsx3NetEquipOOS     Carrier Equipment Out of Service')
dsx3TransmitClockSource = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('external', 1), ('internal', 2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3TransmitClockSource.setDescription('The source of Transmit Clock.\n\n                 loopTiming indicates that the recovered receive clock\n                 is used as the transmit clock.\n\n                 localTiming indicates that a local clock source is\n                 used.\n\n                 throughTiming indicates that transmit clock is derived\n                 from the recovered receive clock of another DS3\n                 interface.')
dsx3InvalidIntervals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3InvalidIntervals.setDescription('The number of intervals for which no valid data\n                      is available.')
dsx3LineLength = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 64000))).setUnits('meters').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3LineLength.setDescription('The length of the ds3 line in meters.  This\n                      object provides information for line build out\n                      circuitry if it exists and can use this object to\n                      adjust the line build out.')
dsx3LineStatusLastChange = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 14), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3LineStatusLastChange.setDescription("The value of MIB II's sysUpTime object at the\n                      time this DS3/E3 entered its current line status\n                      state.  If the current state was entered prior to\n                      the last re-initialization of the proxy-agent,\n                      then this object contains a zero value.")
dsx3LineStatusChangeTrapEnable = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 15), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2))).clone('disabled')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3LineStatusChangeTrapEnable.setDescription('Indicates whether dsx3LineStatusChange traps\n                      should be generated for this interface.')
dsx3LoopbackStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 5, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3LoopbackStatus.setDescription('This variable represents the current state of the\n                      loopback on the DS3 interface.  It contains\n                      information about loopbacks established by a\n                      manager and remotely from the far end.\n\n                      The dsx3LoopbackStatus is a bit map represented as\n                      a sum, therefore is can represent multiple\n                      loopbacks simultaneously.\n\n                      The various bit positions are:\n                       1  dsx3NoLoopback\n                       2  dsx3NearEndPayloadLoopback\n                       4  dsx3NearEndLineLoopback\n                       8  dsx3NearEndOtherLoopback\n                      16  dsx3NearEndInwardLoopback\n                      32  dsx3FarEndPayloadLoopback\n                      64  dsx3FarEndLineLoopback')
dsx3CurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 6))
if mibBuilder.loadTexts:
    dsx3CurrentTable.setDescription('The DS3/E3 current table contains various\n                      statistics being collected for the current 15\n                      minute interval.')
dsx3CurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 6, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3CurrentIndex'))
if mibBuilder.loadTexts:
    dsx3CurrentEntry.setDescription('An entry in the DS3/E3 Current table.')
dsx3CurrentIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentIndex.setDescription('The index value which uniquely identifies the\n                      DS3/E3 interface to which this entry is\n                      applicable.  The interface identified by a\n\n\n                      particular value of this index is the same\n                      interface as identified by the same value an\n                      dsx3LineIndex object instance.')
dsx3CurrentPESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 2), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentPESs.setDescription('The counter associated with the number of P-bit\n                      Errored Seconds, encountered by a DS3 interface in\n                      the current 15 minute interval.  noSuchInstance\n                      will be returned if no data is available.')
dsx3CurrentPSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentPSESs.setDescription('The counter associated with the number of P-bit\n                      Severely Errored Seconds, encountered by a DS3\n                      interface in the current 15 minute interval.\n                      noSuchInstance will be returned if no data is\n                      available.')
dsx3CurrentSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentSEFSs.setDescription('The counter associated with the number of\n                      Severely Errored Framing Seconds, encountered by a\n                      DS3/E3 interface in the current 15 minute\n                      interval.  noSuchInstance will be returned if no\n                      data is available.')
dsx3CurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 5), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentUASs.setDescription('The counter associated with the number of\n                      Unavailable Seconds, encountered by a DS3\n                      interface in the current 15 minute interval.\n                      noSuchInstance will be returned if no data is\n                      available.')
dsx3CurrentLCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 6), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentLCVs.setDescription('The counter associated with the number of Line\n                      Coding Violations encountered by a DS3/E3\n                      interface in the current 15 minute interval.\n                      noSuchInstance will be returned if no data is\n                      available.')
dsx3CurrentPCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 7), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentPCVs.setDescription('The counter associated with the number of P-bit\n                      Coding Violations, encountered by a DS3 interface\n                      in the current 15 minute interval.  noSuchInstance\n                      will be returned if no data is available.')
dsx3CurrentLESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 8), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentLESs.setDescription('The number of Line Errored Seconds encountered by\n                      a DS3/E3 interface in the current 15 minute\n                      interval.  noSuchInstance will be returned if no\n                      data is available.')
dsx3CurrentCCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 9), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentCCVs.setDescription('The number of C-bit Coding Violations encountered\n                      by a DS3 interface in the current 15 minute\n                      interval.  noSuchInstance will be returned if no\n                      data is available.')
dsx3CurrentCESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 10), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentCESs.setDescription('The number of C-bit Errored Seconds encountered\n                      by a DS3 interface in the current 15 minute\n                      interval.  noSuchInstance will be returned if no\n                      data is available.')
dsx3CurrentCSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 6, 1, 11), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3CurrentCSESs.setDescription('The number of C-bit Severely Errored Seconds\n                      encountered by a DS3 interface in the current 15\n                      minute interval.  noSuchInstance will be returned\n                      if no data is available.')
dsx3IntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 7))
if mibBuilder.loadTexts:
    dsx3IntervalTable.setDescription('The DS3/E3 Interval Table contains various\n                      statistics collected by each DS3/E3 Interface over\n                      the previous 24 hours of operation.  The past 24\n                      hours are broken into 96 completed 15 minute\n                      intervals.')
dsx3IntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 7, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3IntervalIndex'), (0, 'DS3-MIB', 'dsx3IntervalNumber'))
if mibBuilder.loadTexts:
    dsx3IntervalEntry.setDescription('An entry in the DS3/E3 Interval table.')
dsx3IntervalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalIndex.setDescription('The index value which uniquely identifies the\n                      DS3/E3 interface to which this entry is\n                      applicable.  The interface identified by a\n                      particular value of this index is the same\n                      interface as identified by the same value an\n                      dsx3LineIndex object instance.')
dsx3IntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalNumber.setDescription('A number between 1 and 96, where 1 is the most\n                      recently completed 15 minute interval and 96 is\n                      the 15 minutes interval completed 23 hours and 45\n                      minutes prior to interval 1.')
dsx3IntervalPESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalPESs.setDescription('The counter associated with the number of P-bit\n                      Errored Seconds, encountered by a DS3 interface in\n                      one of the previous 96, individual 15 minute,\n                      intervals. In the case where the agent is a proxy\n                      and valid data is not available, return\n                      noSuchInstance.')
dsx3IntervalPSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalPSESs.setDescription('The counter associated with the number of P-bit\n                      Severely Errored Seconds, encountered by a DS3\n                      interface in one of the previous 96, individual 15\n                      minute, intervals. In the case where the agent is\n                      a proxy and valid data is not available, return\n                      noSuchInstance.')
dsx3IntervalSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalSEFSs.setDescription('The counter associated with the number of\n                      Severely Errored Framing Seconds, encountered by a\n                      DS3/E3 interface in one of the previous 96,\n                      individual 15 minute, intervals. In the case where\n                      the agent is a proxy and valid data is not\n                      available, return noSuchInstance.')
dsx3IntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 6), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalUASs.setDescription('The counter associated with the number of\n                      Unavailable Seconds, encountered by a DS3\n                      interface in one of the previous 96, individual 15\n                      minute, intervals. In the case where the agent is\n                      a proxy and valid data is not available, return\n                      noSuchInstance. This object may decrease if the\n                      occurance of unavailable seconds occurs across an\n                      inteval boundary.')
dsx3IntervalLCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 7), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalLCVs.setDescription('The counter associated with the number of Line\n                      Coding Violations encountered by a DS3/E3\n                      interface in one of the previous 96, individual 15\n                      minute, intervals. In the case where the agent is\n                      a proxy and valid data is not available, return\n                      noSuchInstance.')
dsx3IntervalPCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 8), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalPCVs.setDescription('The counter associated with the number of P-bit\n                      Coding Violations, encountered by a DS3 interface\n                      in one of the previous 96, individual 15 minute,\n                      intervals. In the case where the agent is a proxy\n                      and valid data is not available, return\n                      noSuchInstance.')
dsx3IntervalLESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 9), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalLESs.setDescription('The number of Line Errored  Seconds  (BPVs  or\n                      illegal  zero  sequences) encountered by a DS3/E3\n                      interface in one of the previous 96, individual 15\n                      minute, intervals. In the case where the agent is\n                      a proxy and valid data is not available, return\n                      noSuchInstance.')
dsx3IntervalCCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 10), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalCCVs.setDescription('The number of C-bit Coding Violations encountered\n                      by a DS3 interface in one of the previous 96,\n                      individual 15 minute, intervals. In the case where\n                      the agent is a proxy and valid data is not\n                      available, return noSuchInstance.')
dsx3IntervalCESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 11), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalCESs.setDescription('The number of C-bit Errored Seconds encountered\n                      by a DS3 interface in one of the previous 96,\n                      individual 15 minute, intervals. In the case where\n                      the agent is a proxy and valid data is not\n                      available, return noSuchInstance.')
dsx3IntervalCSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 12), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalCSESs.setDescription('The number of C-bit Severely Errored Seconds\n                      encountered by a DS3 interface in one of the\n                      previous 96, individual 15 minute, intervals. In\n                      the case where the agent is a proxy and valid data\n                      is not available, return noSuchInstance.')
dsx3IntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 7, 1, 13), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3IntervalValidData.setDescription('This variable indicates if there is valid data\n                      for this interval.')
dsx3TotalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 8))
if mibBuilder.loadTexts:
    dsx3TotalTable.setDescription('The DS3/E3 Total Table contains the cumulative\n                      sum of the various statistics for the 24 hour\n                      period preceding the current interval.')
dsx3TotalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 8, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3TotalIndex'))
if mibBuilder.loadTexts:
    dsx3TotalEntry.setDescription('An entry in the DS3/E3 Total table.')
dsx3TotalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalIndex.setDescription('The index value which uniquely identifies the\n                      DS3/E3 interface to which this entry is\n                      applicable.  The interface identified by a\n                      particular value of this index is the same\n\n\n                      interface as identified by the same value an\n                      dsx3LineIndex object instance.')
dsx3TotalPESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 2), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalPESs.setDescription('The counter associated with the number of P-bit\n                      Errored Seconds, encountered by a DS3 interface in\n                      the previous 24 hour interval. Invalid 15 minute\n                      intervals count as 0.')
dsx3TotalPSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 3), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalPSESs.setDescription('The counter associated with the number of P-bit\n                      Severely Errored Seconds, encountered by a DS3\n                      interface in the previous 24 hour interval.\n                      Invalid 15 minute intervals count as 0.')
dsx3TotalSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 4), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalSEFSs.setDescription('The counter associated with the number of\n                      Severely Errored Framing Seconds, encountered by a\n                      DS3/E3 interface in the previous 24 hour interval.\n                      Invalid 15 minute intervals count as 0.')
dsx3TotalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 5), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalUASs.setDescription('The counter associated with the number of\n                      Unavailable Seconds, encountered by a DS3\n                      interface in the previous 24 hour interval.\n\n\n                      Invalid 15 minute intervals count as 0.')
dsx3TotalLCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 6), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalLCVs.setDescription('The counter associated with the number of Line\n                      Coding Violations encountered by a DS3/E3\n                      interface in the previous 24 hour interval.\n                      Invalid 15 minute intervals count as 0.')
dsx3TotalPCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 7), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalPCVs.setDescription('The counter associated with the number of P-bit\n                      Coding Violations, encountered by a DS3 interface\n                      in the previous 24 hour interval. Invalid 15\n                      minute intervals count as 0.')
dsx3TotalLESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 8), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalLESs.setDescription('The number of Line Errored  Seconds  (BPVs  or\n                      illegal  zero  sequences) encountered by a DS3/E3\n                      interface in the previous 24 hour interval.\n                      Invalid 15 minute intervals count as 0.')
dsx3TotalCCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 9), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalCCVs.setDescription('The number of C-bit Coding Violations encountered\n                      by a DS3 interface in the previous 24 hour\n                      interval. Invalid 15 minute intervals count as 0.')
dsx3TotalCESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 10), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalCESs.setDescription('The number of C-bit Errored Seconds encountered\n                      by a DS3 interface in the previous 24 hour\n                      interval. Invalid 15 minute intervals count as 0.')
dsx3TotalCSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 8, 1, 11), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3TotalCSESs.setDescription('The number of C-bit Severely Errored Seconds\n                      encountered by a DS3 interface in the previous 24\n                      hour interval. Invalid 15 minute intervals count\n                      as 0.')
dsx3FarEndConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 9))
if mibBuilder.loadTexts:
    dsx3FarEndConfigTable.setDescription('The DS3 Far End Configuration Table contains\n                      configuration information reported in the C-bits\n                      from the remote end.')
dsx3FarEndConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 9, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3FarEndLineIndex'))
if mibBuilder.loadTexts:
    dsx3FarEndConfigEntry.setDescription('An entry in the DS3 Far End Configuration table.')
dsx3FarEndLineIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 9, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndLineIndex.setDescription('The index value which uniquely identifies the DS3\n                      interface to which this entry is applicable.  The\n                      interface identified by a particular value of this\n                      index is the same interface as identified by the\n                      same value an dsx3LineIndex object instance.')
dsx3FarEndEquipCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 9, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 10))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3FarEndEquipCode.setDescription('This is the Far End Equipment Identification code\n                      that describes the specific piece of equipment.\n                      It is sent within the Path Identification\n                      Message.')
dsx3FarEndLocationIDCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 9, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 11))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3FarEndLocationIDCode.setDescription('This is the Far End Location Identification code\n                      that describes the specific location of the\n                      equipment.  It is sent within the Path\n                      Identification Message.')
dsx3FarEndFrameIDCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 9, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 10))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3FarEndFrameIDCode.setDescription('This is the Far End Frame Identification code\n                      that identifies where the equipment is located\n                      within a building at a given location.  It is sent\n                      within the Path Identification Message.')
dsx3FarEndUnitCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 9, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 6))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3FarEndUnitCode.setDescription('This is the Far End code that identifies the\n                      equipment location within a bay.  It is sent\n                      within the Path Identification Message.')
dsx3FarEndFacilityIDCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 9, 1, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 38))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3FarEndFacilityIDCode.setDescription('This code identifies a specific Far End DS3 path.\n                      It is sent within the Path Identification\n                      Message.')
dsx3FarEndCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 10))
if mibBuilder.loadTexts:
    dsx3FarEndCurrentTable.setDescription('The DS3 Far End Current table contains various\n                      statistics being collected for the current 15\n                      minute interval.  The statistics are collected\n                      from the far end block error code within the C-\n                      bits.')
dsx3FarEndCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 10, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3FarEndCurrentIndex'))
if mibBuilder.loadTexts:
    dsx3FarEndCurrentEntry.setDescription('An entry in the DS3 Far End Current table.')
dsx3FarEndCurrentIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndCurrentIndex.setDescription('The index value which uniquely identifies the DS3\n                      interface to which this entry is applicable.  The\n                      interface identified by a particular value of this\n                      index is identical to the interface identified by\n                      the same value of dsx3LineIndex.')
dsx3FarEndTimeElapsed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 899))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndTimeElapsed.setDescription('The number of seconds that have elapsed since the\n                      beginning of the far end current error-measurement\n                      period.')
dsx3FarEndValidIntervals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndValidIntervals.setDescription('The number of previous far end intervals for\n                      which valid data was collected.  The value will be\n                      96 unless the interface was brought online within\n                      the last 24 hours, in which case the value will be\n                      the number of complete 15 minute far end intervals\n                      since the interface has been online.')
dsx3FarEndCurrentCESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndCurrentCESs.setDescription('The counter associated with the number of Far Far\n                      End C-bit Errored Seconds encountered by a DS3\n                      interface in the current 15 minute interval.\n                      noSuchInstance will be returned if no data is\n                      available.')
dsx3FarEndCurrentCSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 5), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndCurrentCSESs.setDescription('The counter associated with the number of Far End\n                      C-bit Severely Errored Seconds encountered by a\n                      DS3 interface in the current 15 minute interval.\n                      noSuchInstance will be returned if no data is\n                      available.')
dsx3FarEndCurrentCCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 6), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndCurrentCCVs.setDescription('The counter associated with the number of Far End\n                      C-bit Coding Violations reported via the far end\n                      block error count encountered by a DS3 interface\n                      in the current 15 minute interval.  noSuchInstance\n                      will be returned if no data is available.')
dsx3FarEndCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 7), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndCurrentUASs.setDescription('The counter associated with the number of Far End\n                      unavailable seconds encountered by a DS3 interface\n                      in the current 15 minute interval.  noSuchInstance\n                      will be returned if no data is available.')
dsx3FarEndInvalidIntervals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 10, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndInvalidIntervals.setDescription('The number of intervals for which no valid data\n                      is available.')
dsx3FarEndIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 11))
if mibBuilder.loadTexts:
    dsx3FarEndIntervalTable.setDescription('The DS3 Far End Interval Table contains various\n                      statistics collected by each DS3 interface over\n                      the previous 24 hours of operation.  The past 24\n                      hours are broken into 96 completed 15 minute\n                      intervals.')
dsx3FarEndIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 11, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3FarEndIntervalIndex'), (0, 'DS3-MIB', 'dsx3FarEndIntervalNumber'))
if mibBuilder.loadTexts:
    dsx3FarEndIntervalEntry.setDescription('An entry in the DS3 Far End Interval table.')
dsx3FarEndIntervalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalIndex.setDescription('The index value which uniquely identifies the DS3\n                      interface to which this entry is applicable.  The\n                      interface identified by a particular value of this\n                      index is identical to the interface identified by\n                      the same value of dsx3LineIndex.')
dsx3FarEndIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalNumber.setDescription('A number between 1 and 96, where 1 is the most\n                      recently completed 15 minute interval and 96 is\n                      the 15 minutes interval completed 23 hours and 45\n                      minutes prior to interval 1.')
dsx3FarEndIntervalCESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalCESs.setDescription('The counter associated with the number of Far End\n                      C-bit Errored Seconds encountered by a DS3\n                      interface in one of the previous 96, individual 15\n                      minute, intervals. In the case where the agent is\n                      a proxy and valid data is not available, return\n                      noSuchInstance.')
dsx3FarEndIntervalCSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalCSESs.setDescription('The counter associated with the number of Far End\n                      C-bit Severely Errored Seconds encountered by a\n                      DS3 interface in one of the previous 96,\n                      individual 15 minute, intervals. In the case where\n                      the agent is a proxy and valid data is not\n                      available, return noSuchInstance.')
dsx3FarEndIntervalCCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalCCVs.setDescription('The counter associated with the number of Far End\n                      C-bit Coding Violations reported via the far end\n                      block error count encountered by a DS3 interface\n                      in one of the previous 96, individual 15 minute,\n                      intervals. In the case where the agent is a proxy\n                      and valid data is not available, return\n                      noSuchInstance.')
dsx3FarEndIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 6), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalUASs.setDescription('The counter associated with the number of Far End\n                      unavailable seconds encountered by a DS3 interface\n                      in one of the previous 96, individual 15 minute,\n                      intervals. In the case where the agent is a proxy\n                      and valid data is not available, return\n                      noSuchInstance.')
dsx3FarEndIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 11, 1, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndIntervalValidData.setDescription('This variable indicates if there is valid data\n                      for this interval.')
dsx3FarEndTotalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 12))
if mibBuilder.loadTexts:
    dsx3FarEndTotalTable.setDescription('The DS3 Far End Total Table contains the\n\n\n                      cumulative sum of the various statistics for the\n                      24 hour period preceding the current interval.')
dsx3FarEndTotalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 12, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3FarEndTotalIndex'))
if mibBuilder.loadTexts:
    dsx3FarEndTotalEntry.setDescription('An entry in the DS3 Far End Total table.')
dsx3FarEndTotalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 12, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndTotalIndex.setDescription('The index value which uniquely identifies the DS3\n                      interface to which this entry is applicable.  The\n                      interface identified by a particular value of this\n                      index is identical to the interface identified by\n                      the same value of dsx3LineIndex.')
dsx3FarEndTotalCESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 12, 1, 2), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndTotalCESs.setDescription('The counter associated with the number of Far End\n                      C-bit Errored Seconds encountered by a DS3\n                      interface in the previous 24 hour interval.\n                      Invalid 15 minute intervals count as 0.')
dsx3FarEndTotalCSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 12, 1, 3), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndTotalCSESs.setDescription('The counter associated with the number of Far End\n                      C-bit Severely Errored Seconds encountered by a\n                      DS3 interface in the previous 24 hour interval.\n                      Invalid 15 minute intervals count as 0.')
dsx3FarEndTotalCCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 12, 1, 4), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndTotalCCVs.setDescription('The counter associated with the number of Far End\n                      C-bit Coding Violations reported via the far end\n                      block error count encountered by a DS3 interface\n                      in the previous 24 hour interval. Invalid 15\n                      minute intervals count as 0.')
dsx3FarEndTotalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 12, 1, 5), PerfTotalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FarEndTotalUASs.setDescription('The counter associated with the number of Far End\n                      unavailable seconds encountered by a DS3 interface\n                      in the previous 24 hour interval.  Invalid 15\n                      minute intervals count as 0.')
dsx3FracTable = MibTable((1, 3, 6, 1, 2, 1, 10, 30, 13))
if mibBuilder.loadTexts:
    dsx3FracTable.setDescription('This table is deprecated in favour of using\n                      ifStackTable.\n\n                      Implementation of this table was optional.  It was\n                      designed for those systems dividing a DS3/E3 into\n                      channels containing different data streams that\n                      are of local interest.\n\n                      The DS3/E3 fractional table identifies which\n                      DS3/E3 channels associated with a CSU are being\n                      used to support a logical interface, i.e., an\n                      entry in the interfaces table from the Internet-\n                      standard MIB.\n\n                      For example, consider a DS3 device with 4 high\n                      speed links carrying router traffic, a feed for\n                      voice, a feed for video, and a synchronous channel\n                      for a non-routed protocol.  We might describe the\n                      allocation of channels, in the dsx3FracTable, as\n                      follows:\n                      dsx3FracIfIndex.2. 1 = 3  dsx3FracIfIndex.2.15 = 4\n                      dsx3FracIfIndex.2. 2 = 3  dsx3FracIfIndex.2.16 = 6\n                      dsx3FracIfIndex.2. 3 = 3  dsx3FracIfIndex.2.17 = 6\n                      dsx3FracIfIndex.2. 4 = 3  dsx3FracIfIndex.2.18 = 6\n                      dsx3FracIfIndex.2. 5 = 3  dsx3FracIfIndex.2.19 = 6\n                      dsx3FracIfIndex.2. 6 = 3  dsx3FracIfIndex.2.20 = 6\n                      dsx3FracIfIndex.2. 7 = 4  dsx3FracIfIndex.2.21 = 6\n                      dsx3FracIfIndex.2. 8 = 4  dsx3FracIfIndex.2.22 = 6\n                      dsx3FracIfIndex.2. 9 = 4  dsx3FracIfIndex.2.23 = 6\n                      dsx3FracIfIndex.2.10 = 4  dsx3FracIfIndex.2.24 = 6\n                      dsx3FracIfIndex.2.11 = 4  dsx3FracIfIndex.2.25 = 6\n                      dsx3FracIfIndex.2.12 = 5  dsx3FracIfIndex.2.26 = 6\n                      dsx3FracIfIndex.2.13 = 5  dsx3FracIfIndex.2.27 = 6\n                      dsx3FracIfIndex.2.14 = 5  dsx3FracIfIndex.2.28 = 6\n                      For dsx3M23, dsx3 SYNTRAN, dsx3CbitParity, and\n                      dsx3ClearChannel  there are 28 legal channels,\n\n\n                      numbered 1 throug h 28.\n\n                      For e3Framed there are 16 legal channels, numbered\n                      1 through 16.  The channels (1..16) correspond\n                      directly to the equivalently numbered time-slots.')
dsx3FracEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 30, 13, 1)).setIndexNames((0, 'DS3-MIB', 'dsx3FracIndex'), (0, 'DS3-MIB', 'dsx3FracNumber'))
if mibBuilder.loadTexts:
    dsx3FracEntry.setDescription('An entry in the DS3 Fractional table.')
dsx3FracIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 13, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FracIndex.setDescription('The index value which uniquely identifies  the\n                      DS3  interface  to which this entry is applicable\n                      The interface identified by a  particular value\n                      of  this  index is the same interface as\n                      identified by the same value  an  dsx3LineIndex\n                      object instance.')
dsx3FracNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 13, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 31))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx3FracNumber.setDescription('The channel number for this entry.')
dsx3FracIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 30, 13, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx3FracIfIndex.setDescription('An index value that uniquely identifies an\n                      interface.  The interface identified by a\n                      particular value of this index is the same\n                      interface as  identified by the same value an\n                      ifIndex object instance. If no interface is\n                      currently using a channel, the value should be\n                      zero.  If a single interface occupies more  than\n                      one  time slot,  that ifIndex value will be found\n                      in multiple time slots.')
ds3Conformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 30, 14))
ds3Groups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 30, 14, 1))
ds3Compliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 30, 14, 2))
ds3Compliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 30, 14, 2, 1)).setObjects(*(('DS3-MIB', 'ds3NearEndConfigGroup'), ('DS3-MIB', 'ds3NearEndStatisticsGroup'), ('DS3-MIB', 'ds3FarEndGroup'), ('DS3-MIB', 'ds3NearEndOptionalConfigGroup')))
if mibBuilder.loadTexts:
    ds3Compliance.setDescription('The compliance statement for DS3/E3 interfaces.')
ds3NearEndConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 30, 14, 1, 1)).setObjects(*(('DS3-MIB', 'dsx3LineIndex'), ('DS3-MIB', 'dsx3TimeElapsed'), ('DS3-MIB', 'dsx3ValidIntervals'), ('DS3-MIB', 'dsx3LineType'), ('DS3-MIB', 'dsx3LineCoding'), ('DS3-MIB', 'dsx3SendCode'), ('DS3-MIB', 'dsx3CircuitIdentifier'), ('DS3-MIB', 'dsx3LoopbackConfig'), ('DS3-MIB', 'dsx3LineStatus'), ('DS3-MIB', 'dsx3TransmitClockSource'), ('DS3-MIB', 'dsx3InvalidIntervals'), ('DS3-MIB', 'dsx3LineLength'), ('DS3-MIB', 'dsx3LoopbackStatus')))
if mibBuilder.loadTexts:
    ds3NearEndConfigGroup.setDescription('A collection of objects providing configuration\n                      information applicable to all DS3/E3 interfaces.')
ds3NearEndStatisticsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 30, 14, 1, 2)).setObjects(*(('DS3-MIB', 'dsx3CurrentIndex'), ('DS3-MIB', 'dsx3CurrentPESs'), ('DS3-MIB', 'dsx3CurrentPSESs'), ('DS3-MIB', 'dsx3CurrentSEFSs'), ('DS3-MIB', 'dsx3CurrentUASs'), ('DS3-MIB', 'dsx3CurrentLCVs'), ('DS3-MIB', 'dsx3CurrentPCVs'), ('DS3-MIB', 'dsx3CurrentLESs'), ('DS3-MIB', 'dsx3CurrentCCVs'), ('DS3-MIB', 'dsx3CurrentCESs'), ('DS3-MIB', 'dsx3CurrentCSESs'), ('DS3-MIB', 'dsx3IntervalIndex'), ('DS3-MIB', 'dsx3IntervalNumber'), ('DS3-MIB', 'dsx3IntervalPESs'), ('DS3-MIB', 'dsx3IntervalPSESs'), ('DS3-MIB', 'dsx3IntervalSEFSs'), ('DS3-MIB', 'dsx3IntervalUASs'), ('DS3-MIB', 'dsx3IntervalLCVs'), ('DS3-MIB', 'dsx3IntervalPCVs'), ('DS3-MIB', 'dsx3IntervalLESs'), ('DS3-MIB', 'dsx3IntervalCCVs'), ('DS3-MIB', 'dsx3IntervalCESs'), ('DS3-MIB', 'dsx3IntervalCSESs'), ('DS3-MIB', 'dsx3IntervalValidData'), ('DS3-MIB', 'dsx3TotalIndex'), ('DS3-MIB', 'dsx3TotalPESs'), ('DS3-MIB', 'dsx3TotalPSESs'), ('DS3-MIB', 'dsx3TotalSEFSs'), ('DS3-MIB', 'dsx3TotalUASs'), ('DS3-MIB', 'dsx3TotalLCVs'), ('DS3-MIB', 'dsx3TotalPCVs'), ('DS3-MIB', 'dsx3TotalLESs'), ('DS3-MIB', 'dsx3TotalCCVs'), ('DS3-MIB', 'dsx3TotalCESs'), ('DS3-MIB', 'dsx3TotalCSESs')))
if mibBuilder.loadTexts:
    ds3NearEndStatisticsGroup.setDescription('A collection of objects providing statistics\n                      information applicable to all DS3/E3 interfaces.')
ds3FarEndGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 30, 14, 1, 3)).setObjects(*(('DS3-MIB', 'dsx3FarEndLineIndex'), ('DS3-MIB', 'dsx3FarEndEquipCode'), ('DS3-MIB', 'dsx3FarEndLocationIDCode'), ('DS3-MIB', 'dsx3FarEndFrameIDCode'), ('DS3-MIB', 'dsx3FarEndUnitCode'), ('DS3-MIB', 'dsx3FarEndFacilityIDCode'), ('DS3-MIB', 'dsx3FarEndCurrentIndex'), ('DS3-MIB', 'dsx3FarEndTimeElapsed'), ('DS3-MIB', 'dsx3FarEndValidIntervals'), ('DS3-MIB', 'dsx3FarEndCurrentCESs'), ('DS3-MIB', 'dsx3FarEndCurrentCSESs'), ('DS3-MIB', 'dsx3FarEndCurrentCCVs'), ('DS3-MIB', 'dsx3FarEndCurrentUASs'), ('DS3-MIB', 'dsx3FarEndInvalidIntervals'), ('DS3-MIB', 'dsx3FarEndIntervalIndex'), ('DS3-MIB', 'dsx3FarEndIntervalNumber'), ('DS3-MIB', 'dsx3FarEndIntervalCESs'), ('DS3-MIB', 'dsx3FarEndIntervalCSESs'), ('DS3-MIB', 'dsx3FarEndIntervalCCVs'), ('DS3-MIB', 'dsx3FarEndIntervalUASs'), ('DS3-MIB', 'dsx3FarEndIntervalValidData'), ('DS3-MIB', 'dsx3FarEndTotalIndex'), ('DS3-MIB', 'dsx3FarEndTotalCESs'), ('DS3-MIB', 'dsx3FarEndTotalCSESs'), ('DS3-MIB', 'dsx3FarEndTotalCCVs'), ('DS3-MIB', 'dsx3FarEndTotalUASs')))
if mibBuilder.loadTexts:
    ds3FarEndGroup.setDescription('A collection of objects providing remote\n                      configuration and statistics information\n                      applicable to C-bit Parity and SYNTRAN DS3\n                      interfaces.')
ds3DeprecatedGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 30, 14, 1, 4)).setObjects(*(('DS3-MIB', 'dsx3IfIndex'), ('DS3-MIB', 'dsx3FracIndex'), ('DS3-MIB', 'dsx3FracNumber'), ('DS3-MIB', 'dsx3FracIfIndex')))
if mibBuilder.loadTexts:
    ds3DeprecatedGroup.setDescription('A collection of obsolete objects that may be\n                      implemented for backwards compatibility.')
ds3NearEndOptionalConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 30, 14, 1, 5)).setObjects(*(('DS3-MIB', 'dsx3LineStatusLastChange'), ('DS3-MIB', 'dsx3LineStatusChangeTrapEnable')))
if mibBuilder.loadTexts:
    ds3NearEndOptionalConfigGroup.setDescription('A collection of objects that may be implemented\n                      on DS3/E3 interfaces.')
ds3Traps = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 30, 15))
dsx3LineStatusChange = NotificationType((1, 3, 6, 1, 2, 1, 10, 30, 15, 0, 1)).setObjects(*(('DS3-MIB', 'dsx3LineStatus'), ('DS3-MIB', 'dsx3LineStatusLastChange')))
if mibBuilder.loadTexts:
    dsx3LineStatusChange.setDescription('A dsx3LineStatusChange trap is sent when the\n                      value of an instance dsx1LineStatus changes. It\n                      can be utilized by an NMS to trigger polls.  When\n                      the line status change results in a lower level\n                      line status change (i.e. ds1), then no traps for\n                      the lower level are sent.')
mibBuilder.exportSymbols('DS3-MIB', dsx3IntervalLCVs=dsx3IntervalLCVs, ds3FarEndGroup=ds3FarEndGroup, dsx3TotalSEFSs=dsx3TotalSEFSs, dsx3FarEndTimeElapsed=dsx3FarEndTimeElapsed, dsx3FarEndValidIntervals=dsx3FarEndValidIntervals, dsx3LineStatusChange=dsx3LineStatusChange, dsx3TotalPCVs=dsx3TotalPCVs, dsx3IntervalIndex=dsx3IntervalIndex, dsx3TotalPESs=dsx3TotalPESs, dsx3LineType=dsx3LineType, dsx3CurrentEntry=dsx3CurrentEntry, dsx3IntervalTable=dsx3IntervalTable, dsx3CurrentPCVs=dsx3CurrentPCVs, dsx3ValidIntervals=dsx3ValidIntervals, dsx3FracIndex=dsx3FracIndex, dsx3InvalidIntervals=dsx3InvalidIntervals, dsx3LineIndex=dsx3LineIndex, dsx3ConfigTable=dsx3ConfigTable, dsx3IntervalUASs=dsx3IntervalUASs, ds3Compliances=ds3Compliances, dsx3LineCoding=dsx3LineCoding, dsx3FracEntry=dsx3FracEntry, dsx3FarEndIntervalValidData=dsx3FarEndIntervalValidData, dsx3FarEndTotalTable=dsx3FarEndTotalTable, dsx3TotalTable=dsx3TotalTable, dsx3IntervalPCVs=dsx3IntervalPCVs, dsx3FarEndTotalUASs=dsx3FarEndTotalUASs, dsx3CurrentTable=dsx3CurrentTable, dsx3IntervalLESs=dsx3IntervalLESs, dsx3CurrentLESs=dsx3CurrentLESs, dsx3TotalCSESs=dsx3TotalCSESs, ds3DeprecatedGroup=ds3DeprecatedGroup, dsx3FarEndTotalIndex=dsx3FarEndTotalIndex, dsx3TotalPSESs=dsx3TotalPSESs, ds3Compliance=ds3Compliance, dsx3LineStatus=dsx3LineStatus, dsx3FarEndCurrentCCVs=dsx3FarEndCurrentCCVs, dsx3FarEndTotalEntry=dsx3FarEndTotalEntry, dsx3IntervalCSESs=dsx3IntervalCSESs, dsx3FarEndCurrentCSESs=dsx3FarEndCurrentCSESs, dsx3FarEndIntervalCESs=dsx3FarEndIntervalCESs, dsx3FarEndFacilityIDCode=dsx3FarEndFacilityIDCode, dsx3FarEndFrameIDCode=dsx3FarEndFrameIDCode, dsx3TotalCCVs=dsx3TotalCCVs, dsx3LineStatusChangeTrapEnable=dsx3LineStatusChangeTrapEnable, dsx3SendCode=dsx3SendCode, dsx3FarEndCurrentTable=dsx3FarEndCurrentTable, ds3NearEndOptionalConfigGroup=ds3NearEndOptionalConfigGroup, dsx3FarEndIntervalCCVs=dsx3FarEndIntervalCCVs, dsx3TotalLESs=dsx3TotalLESs, dsx3FarEndIntervalCSESs=dsx3FarEndIntervalCSESs, PYSNMP_MODULE_ID=ds3, dsx3TotalLCVs=dsx3TotalLCVs, dsx3FarEndIntervalEntry=dsx3FarEndIntervalEntry, dsx3CurrentLCVs=dsx3CurrentLCVs, dsx3FarEndIntervalIndex=dsx3FarEndIntervalIndex, dsx3IntervalPSESs=dsx3IntervalPSESs, dsx3LineLength=dsx3LineLength, dsx3FarEndIntervalTable=dsx3FarEndIntervalTable, dsx3IntervalNumber=dsx3IntervalNumber, dsx3FarEndConfigTable=dsx3FarEndConfigTable, dsx3FarEndUnitCode=dsx3FarEndUnitCode, dsx3FarEndTotalCSESs=dsx3FarEndTotalCSESs, dsx3FarEndLocationIDCode=dsx3FarEndLocationIDCode, dsx3IntervalPESs=dsx3IntervalPESs, dsx3FarEndLineIndex=dsx3FarEndLineIndex, dsx3FarEndInvalidIntervals=dsx3FarEndInvalidIntervals, dsx3FracIfIndex=dsx3FracIfIndex, dsx3ConfigEntry=dsx3ConfigEntry, dsx3CurrentPSESs=dsx3CurrentPSESs, dsx3IntervalSEFSs=dsx3IntervalSEFSs, dsx3CircuitIdentifier=dsx3CircuitIdentifier, dsx3TotalUASs=dsx3TotalUASs, dsx3CurrentCESs=dsx3CurrentCESs, dsx3FarEndTotalCESs=dsx3FarEndTotalCESs, dsx3IntervalEntry=dsx3IntervalEntry, ds3Traps=ds3Traps, dsx3CurrentUASs=dsx3CurrentUASs, dsx3IntervalValidData=dsx3IntervalValidData, dsx3CurrentCSESs=dsx3CurrentCSESs, dsx3CurrentPESs=dsx3CurrentPESs, dsx3TimeElapsed=dsx3TimeElapsed, dsx3LoopbackConfig=dsx3LoopbackConfig, dsx3TotalEntry=dsx3TotalEntry, dsx3FarEndCurrentCESs=dsx3FarEndCurrentCESs, dsx3TotalIndex=dsx3TotalIndex, dsx3FracNumber=dsx3FracNumber, dsx3FarEndConfigEntry=dsx3FarEndConfigEntry, ds3=ds3, dsx3CurrentIndex=dsx3CurrentIndex, dsx3FarEndIntervalNumber=dsx3FarEndIntervalNumber, dsx3LineStatusLastChange=dsx3LineStatusLastChange, dsx3FarEndCurrentIndex=dsx3FarEndCurrentIndex, dsx3FarEndCurrentUASs=dsx3FarEndCurrentUASs, dsx3LoopbackStatus=dsx3LoopbackStatus, dsx3CurrentCCVs=dsx3CurrentCCVs, dsx3IntervalCCVs=dsx3IntervalCCVs, dsx3FracTable=dsx3FracTable, dsx3FarEndCurrentEntry=dsx3FarEndCurrentEntry, dsx3CurrentSEFSs=dsx3CurrentSEFSs, ds3Groups=ds3Groups, dsx3FarEndEquipCode=dsx3FarEndEquipCode, dsx3TransmitClockSource=dsx3TransmitClockSource, dsx3FarEndTotalCCVs=dsx3FarEndTotalCCVs, ds3Conformance=ds3Conformance, dsx3IntervalCESs=dsx3IntervalCESs, ds3NearEndConfigGroup=ds3NearEndConfigGroup, dsx3TotalCESs=dsx3TotalCESs, dsx3IfIndex=dsx3IfIndex, ds3NearEndStatisticsGroup=ds3NearEndStatisticsGroup, dsx3FarEndIntervalUASs=dsx3FarEndIntervalUASs)