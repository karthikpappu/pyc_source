# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/RS-232-MIB.py
# Compiled at: 2016-02-13 18:27:20
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ValueSizeConstraint, SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ValueSizeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection')
(InterfaceIndex,) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(Unsigned32, Bits, TimeTicks, Counter64, NotificationType, Integer32, MibIdentifier, Gauge32, ObjectIdentity, transmission, IpAddress, ModuleIdentity, Counter32, iso, MibScalar, MibTable, MibTableRow, MibTableColumn) = mibBuilder.importSymbols('SNMPv2-SMI', 'Unsigned32', 'Bits', 'TimeTicks', 'Counter64', 'NotificationType', 'Integer32', 'MibIdentifier', 'Gauge32', 'ObjectIdentity', 'transmission', 'IpAddress', 'ModuleIdentity', 'Counter32', 'iso', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
rs232 = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 33))
if mibBuilder.loadTexts:
    rs232.setLastUpdated('9405261700Z')
if mibBuilder.loadTexts:
    rs232.setOrganization('IETF Character MIB Working Group')
if mibBuilder.loadTexts:
    rs232.setContactInfo('        Bob Stewart\n                Postal: Xyplex, Inc.\n                        295 Foster Street\n                        Littleton, MA 01460\n\n                   Tel: 508-952-4816\n                   Fax: 508-952-4887\n                E-mail: rlstewart@eng.xyplex.com')
if mibBuilder.loadTexts:
    rs232.setDescription('The MIB module for RS-232-like hardware devices.')
rs232Number = MibScalar((1, 3, 6, 1, 2, 1, 10, 33, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232Number.setDescription('The number of ports (regardless of their current\n           state) in the RS-232-like general port table.')
rs232PortTable = MibTable((1, 3, 6, 1, 2, 1, 10, 33, 2))
if mibBuilder.loadTexts:
    rs232PortTable.setDescription('A list of port entries.  The number of entries is\n           given by the value of rs232Number.')
rs232PortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 33, 2, 1)).setIndexNames((0, 'RS-232-MIB',
                                                                              'rs232PortIndex'))
if mibBuilder.loadTexts:
    rs232PortEntry.setDescription('Status and parameter values for a port.')
rs232PortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232PortIndex.setDescription('The value of ifIndex for the port.  By convention\n           and if possible, hardware port numbers map directly\n           to external connectors.  The value for each port must\n           remain constant at least from one re-initialization\n           of the network management agent to the next.')
rs232PortType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                              1), ('rs232',
                                                                                                                                                                                                   2), ('rs422',
                                                                                                                                                                                                        3), ('rs423',
                                                                                                                                                                                                             4), ('v35',
                                                                                                                                                                                                                  5), ('x21',
                                                                                                                                                                                                                       6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232PortType.setDescription("The port's hardware type.")
rs232PortInSigNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232PortInSigNumber.setDescription('The number of input signals for the port in the\n           input signal table (rs232PortInSigTable).  The table\n           contains entries only for those signals the software\n           can detect and that are useful to observe.')
rs232PortOutSigNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232PortOutSigNumber.setDescription('The number of output signals for the port in the\n           output signal table (rs232PortOutSigTable).  The\n           table contains entries only for those signals the\n           software can assert and that are useful to observe.')
rs232PortInSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 5), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232PortInSpeed.setDescription("The port's input speed in bits per second.  Note that\n           non-standard values, such as 9612, are probably not allowed\n           on most implementations.")
rs232PortOutSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 6), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232PortOutSpeed.setDescription("The port's output speed in bits per second.  Note that\n           non-standard values, such as 9612, are probably not allowed\n           on most implementations.")
rs232PortInFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                           1), ('ctsRts',
                                                                                                                                                                                                2), ('dsrDtr',
                                                                                                                                                                                                     3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232PortInFlowType.setDescription("The port's type of input flow control.  'none'\n           indicates no flow control at this level.\n           'ctsRts' and 'dsrDtr' indicate use of the indicated\n           hardware signals.")
rs232PortOutFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                            1), ('ctsRts',
                                                                                                                                                                                                 2), ('dsrDtr',
                                                                                                                                                                                                      3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232PortOutFlowType.setDescription("The port's type of output flow control.  'none'\n           indicates no flow control at this level.\n           'ctsRts' and 'dsrDtr' indicate use of the indicated\n           hardware signals.")
rs232AsyncPortTable = MibTable((1, 3, 6, 1, 2, 1, 10, 33, 3))
if mibBuilder.loadTexts:
    rs232AsyncPortTable.setDescription('A list of asynchronous port entries.  Entries need\n           not exist for synchronous ports.')
rs232AsyncPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 33, 3, 1)).setIndexNames((0,
                                                                                   'RS-232-MIB',
                                                                                   'rs232AsyncPortIndex'))
if mibBuilder.loadTexts:
    rs232AsyncPortEntry.setDescription('Status and parameter values for an asynchronous\n           port.')
rs232AsyncPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232AsyncPortIndex.setDescription('A unique value for each port.  Its value is the\n           same as rs232PortIndex for the port.')
rs232AsyncPortBits = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(5, 8))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232AsyncPortBits.setDescription("The port's number of bits in a character.")
rs232AsyncPortStopBits = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('one',
                                                                                                                                                                                                 1), ('two',
                                                                                                                                                                                                      2), ('oneAndHalf',
                                                                                                                                                                                                           3), ('dynamic',
                                                                                                                                                                                                                4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232AsyncPortStopBits.setDescription("The port's number of stop bits.")
rs232AsyncPortParity = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                                  1), ('odd',
                                                                                                                                                                                                       2), ('even',
                                                                                                                                                                                                            3), ('mark',
                                                                                                                                                                                                                 4), ('space',
                                                                                                                                                                                                                      5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232AsyncPortParity.setDescription("The port's sense of a character parity bit.")
rs232AsyncPortAutobaud = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                           1), ('disabled',
                                                                                                                                                                                                2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232AsyncPortAutobaud.setDescription("A control for the port's ability to automatically\n           sense input speed.\n\n           When rs232PortAutoBaud is 'enabled', a port may\n           autobaud to values different from the set values for\n           speed, parity, and character size.  As a result a\n           network management system may temporarily observe\n           values different from what was previously set.")
rs232AsyncPortParityErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232AsyncPortParityErrs.setDescription("Total number of characters with a parity error,\n           input from the port since system re-initialization\n           and while the port state was 'up' or 'test'.")
rs232AsyncPortFramingErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232AsyncPortFramingErrs.setDescription("Total number of characters with a framing error,\n           input from the port since system re-initialization\n           and while the port state was 'up' or 'test'.")
rs232AsyncPortOverrunErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 3, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232AsyncPortOverrunErrs.setDescription("Total number of characters with an overrun error,\n           input from the port since system re-initialization\n           and while the port state was 'up' or 'test'.")
rs232SyncPortTable = MibTable((1, 3, 6, 1, 2, 1, 10, 33, 4))
if mibBuilder.loadTexts:
    rs232SyncPortTable.setDescription('A list of asynchronous port entries.  Entries need\n           not exist for synchronous ports.')
rs232SyncPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 33, 4, 1)).setIndexNames((0,
                                                                                  'RS-232-MIB',
                                                                                  'rs232SyncPortIndex'))
if mibBuilder.loadTexts:
    rs232SyncPortEntry.setDescription('Status and parameter values for a synchronous\n           port.')
rs232SyncPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232SyncPortIndex.setDescription('A unique value for each port.  Its value is the\n           same as rs232PortIndex for the port.')
rs232SyncPortClockSource = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('internal',
                                                                                                                                                                                                1), ('external',
                                                                                                                                                                                                     2), ('split',
                                                                                                                                                                                                          3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortClockSource.setDescription("Source of the port's bit rate clock. 'split' means\n           the tranmit clock is internal and the receive clock\n           is external.")
rs232SyncPortFrameCheckErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232SyncPortFrameCheckErrs.setDescription("Total number of frames with an invalid frame check\n           sequence, input from the port since system\n           re-initialization and while the port state was 'up'\n           or 'test'.")
rs232SyncPortTransmitUnderrunErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1,
                                                    4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232SyncPortTransmitUnderrunErrs.setDescription("Total number of frames that failed to be\n           transmitted on the port since system\n           re-initialization and while the port state was 'up'\n           or 'test' because data was not available to the\n           transmitter in time.")
rs232SyncPortReceiveOverrunErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232SyncPortReceiveOverrunErrs.setDescription("Total number of frames that failed to be received\n           on the port since system re-initialization and while\n           the port state was 'up' or 'test' because the\n           receiver did not accept the data in time.")
rs232SyncPortInterruptedFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232SyncPortInterruptedFrames.setDescription("Total number of frames that failed to be received\n           or transmitted on the port due to loss of modem\n           signals since system re-initialization and while the\n           port state was 'up' or 'test'.")
rs232SyncPortAbortedFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232SyncPortAbortedFrames.setDescription("Number of frames aborted on the port due to\n           receiving an abort sequence since system\n           re-initialization and while the port state was 'up'\n           or 'test'.")
rs232SyncPortRole = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('dte',
                                                                                                                                                                                      1), ('dce',
                                                                                                                                                                                           2))).clone('dce')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortRole.setDescription('The role the device is playing that is using this port.\n              dte    means the device is performing the role of\n                     data terminal equipment\n              dce    means the device is performing the role of\n                     data circuit-terminating equipment.')
rs232SyncPortEncoding = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('nrz',
                                                                                                                                                                                          1), ('nrzi',
                                                                                                                                                                                               2))).clone('nrz')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortEncoding.setDescription('The bit stream encoding technique that is in effect\n            for this port.\n              nrz    for Non-Return to Zero encoding\n              nrzi   for Non-Return to Zero Inverted encoding.')
rs232SyncPortRTSControl = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('controlled',
                                                                                                                                                                                             1), ('constant',
                                                                                                                                                                                                  2))).clone('constant')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortRTSControl.setDescription("The method used to control the Request To Send (RTS)\n            signal.\n\n              controlled  when the DTE is asserts RTS each time\n                          data needs to be transmitted and drops\n                          RTS at some point after data\n                          transmission begins.\n\n                          If rs232SyncPortRole is 'dte', the\n                          RTS is an output signal. The device\n                          will issue a RTS and wait for a CTS\n                          from the DCE before starting to\n                          transmit.\n\n                          If rs232SyncPortRole is 'dce', the\n                          RTS is an input signal. The device\n                          will issue a CTS only after having\n                          received RTS and waiting the\n                          rs232SyncPortRTSCTSDelay interval.\n\n              constant    when the DTE constantly asserts RTS.")
rs232SyncPortRTSCTSDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 11), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortRTSCTSDelay.setDescription('The interval (in milliseconds) that the DCE must wait\n            after it sees RTS asserted before asserting CTS.  This\n            object exists in support of older synchronous devices\n            that cannot recognize CTS within a certain interval\n            after it asserts RTS.')
rs232SyncPortMode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('fdx',
                                                                                                                                                                                             1), ('hdx',
                                                                                                                                                                                                  2), ('simplex-receive',
                                                                                                                                                                                                       3), ('simplex-send',
                                                                                                                                                                                                            4))).clone('fdx')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortMode.setDescription('The mode of operation of the port with respect to the\n            direction and simultaneity of data transfer.\n              fdx              when frames on the data link can be\n                               transmitted and received at the same\n                               time\n\n              hdx              when frames can either be received\n                               from the data link or transmitted\n                               onto the data link but not at the\n                               same time.\n\n              simplex-receive  when frames can only be received on\n                               this data link.\n\n              simplex-send     when frames can only be sent on this\n                               data link.')
rs232SyncPortIdlePattern = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 13), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('mark',
                                                                                                                                                                                              1), ('space',
                                                                                                                                                                                                   2))).clone('space')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortIdlePattern.setDescription('The bit pattern used to indicate an idle line.')
rs232SyncPortMinFlags = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 4, 1, 14), Integer32().clone(2)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    rs232SyncPortMinFlags.setDescription('The minimum number of flag patterns this port needs in\n            order to recognize the end of one frame and the start\n            of the next.  Plausible values are 1 and 2.')
rs232InSigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 33, 5))
if mibBuilder.loadTexts:
    rs232InSigTable.setDescription('A list of port input control signal entries\n           implemented and visible to the software on the port,\n           and useful to monitor.')
rs232InSigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 33, 5, 1)).setIndexNames((0, 'RS-232-MIB',
                                                                               'rs232InSigPortIndex'), (0,
                                                                                                        'RS-232-MIB',
                                                                                                        'rs232InSigName'))
if mibBuilder.loadTexts:
    rs232InSigEntry.setDescription('Input control signal status for a hardware port.')
rs232InSigPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 5, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232InSigPortIndex.setDescription('The value of rs232PortIndex for the port to which\n           this entry belongs.')
rs232InSigName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 5, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))).clone(namedValues=NamedValues(('rts',
                                                                                                                                                                                                                1), ('cts',
                                                                                                                                                                                                                     2), ('dsr',
                                                                                                                                                                                                                          3), ('dtr',
                                                                                                                                                                                                                               4), ('ri',
                                                                                                                                                                                                                                    5), ('dcd',
                                                                                                                                                                                                                                         6), ('sq',
                                                                                                                                                                                                                                              7), ('srs',
                                                                                                                                                                                                                                                   8), ('srts',
                                                                                                                                                                                                                                                        9), ('scts',
                                                                                                                                                                                                                                                             10), ('sdcd',
                                                                                                                                                                                                                                                                   11)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232InSigName.setDescription('Identification of a hardware signal, as follows:\n\n               rts    Request to Send\n               cts    Clear to Send\n               dsr    Data Set Ready\n               dtr    Data Terminal Ready\n               ri     Ring Indicator\n               dcd    Received Line Signal Detector\n               sq     Signal Quality Detector\n               srs    Data Signaling Rate Selector\n               srts   Secondary Request to Send\n               scts   Secondary Clear to Send\n               sdcd   Secondary Received Line Signal Detector\n           ')
rs232InSigState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 5, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                       1), ('on',
                                                                                                                                                                                            2), ('off',
                                                                                                                                                                                                 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232InSigState.setDescription('The current signal state.')
rs232InSigChanges = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 5, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232InSigChanges.setDescription("The number of times the signal has changed from\n           'on' to 'off' or from 'off' to 'on'.")
rs232OutSigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 33, 6))
if mibBuilder.loadTexts:
    rs232OutSigTable.setDescription('A list of port output control signal entries\n           implemented and visible to the software on the port,\n           and useful to monitor.')
rs232OutSigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 33, 6, 1)).setIndexNames((0,
                                                                                'RS-232-MIB',
                                                                                'rs232OutSigPortIndex'), (0,
                                                                                                          'RS-232-MIB',
                                                                                                          'rs232OutSigName'))
if mibBuilder.loadTexts:
    rs232OutSigEntry.setDescription('Output control signal status for a hardware port.')
rs232OutSigPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 6, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232OutSigPortIndex.setDescription('The value of rs232PortIndex for the port to which\n           this entry belongs.')
rs232OutSigName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 6, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))).clone(namedValues=NamedValues(('rts',
                                                                                                                                                                                                                 1), ('cts',
                                                                                                                                                                                                                      2), ('dsr',
                                                                                                                                                                                                                           3), ('dtr',
                                                                                                                                                                                                                                4), ('ri',
                                                                                                                                                                                                                                     5), ('dcd',
                                                                                                                                                                                                                                          6), ('sq',
                                                                                                                                                                                                                                               7), ('srs',
                                                                                                                                                                                                                                                    8), ('srts',
                                                                                                                                                                                                                                                         9), ('scts',
                                                                                                                                                                                                                                                              10), ('sdcd',
                                                                                                                                                                                                                                                                    11)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232OutSigName.setDescription('Identification of a hardware signal, as follows:\n\n               rts    Request to Send\n               cts    Clear to Send\n               dsr    Data Set Ready\n               dtr    Data Terminal Ready\n               ri     Ring Indicator\n               dcd    Received Line Signal Detector\n               sq     Signal Quality Detector\n               srs    Data Signaling Rate Selector\n               srts   Secondary Request to Send\n               scts   Secondary Clear to Send\n               sdcd   Secondary Received Line Signal Detector\n           ')
rs232OutSigState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 6, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                        1), ('on',
                                                                                                                                                                                             2), ('off',
                                                                                                                                                                                                  3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232OutSigState.setDescription('The current signal state.')
rs232OutSigChanges = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 33, 6, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    rs232OutSigChanges.setDescription("The number of times the signal has changed from\n           'on' to 'off' or from 'off' to 'on'.")
rs232Conformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 33, 7))
rs232Groups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 33, 7, 1))
rs232Compliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 33, 7, 2))
rs232Compliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 33, 7, 2, 1)).setObjects(*(('RS-232-MIB', 'rs232Group'), ('RS-232-MIB', 'rs232AsyncGroup'), ('RS-232-MIB', 'rs232SyncGroup')))
if mibBuilder.loadTexts:
    rs232Compliance.setDescription('The compliance statement for SNMPv2 entities\n               which have RS-232-like hardware interfaces.')
rs232Group = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 33, 7, 1, 1)).setObjects(*(('RS-232-MIB', 'rs232Number'), ('RS-232-MIB', 'rs232PortIndex'), ('RS-232-MIB', 'rs232PortType'), ('RS-232-MIB', 'rs232PortInSigNumber'), ('RS-232-MIB', 'rs232PortOutSigNumber'), ('RS-232-MIB', 'rs232PortInSpeed'), ('RS-232-MIB', 'rs232PortOutSpeed'), ('RS-232-MIB', 'rs232PortInFlowType'), ('RS-232-MIB', 'rs232PortOutFlowType'), ('RS-232-MIB', 'rs232InSigPortIndex'), ('RS-232-MIB', 'rs232InSigName'), ('RS-232-MIB', 'rs232InSigState'), ('RS-232-MIB', 'rs232InSigChanges'), ('RS-232-MIB', 'rs232OutSigPortIndex'), ('RS-232-MIB', 'rs232OutSigName'), ('RS-232-MIB', 'rs232OutSigState'), ('RS-232-MIB', 'rs232OutSigChanges')))
if mibBuilder.loadTexts:
    rs232Group.setDescription('A collection of objects providing information\n                applicable to all RS-232-like interfaces.')
rs232AsyncGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 33, 7, 1, 2)).setObjects(*(('RS-232-MIB', 'rs232AsyncPortIndex'), ('RS-232-MIB', 'rs232AsyncPortBits'), ('RS-232-MIB', 'rs232AsyncPortStopBits'), ('RS-232-MIB', 'rs232AsyncPortParity'), ('RS-232-MIB', 'rs232AsyncPortAutobaud'), ('RS-232-MIB', 'rs232AsyncPortParityErrs'), ('RS-232-MIB', 'rs232AsyncPortFramingErrs'), ('RS-232-MIB', 'rs232AsyncPortOverrunErrs')))
if mibBuilder.loadTexts:
    rs232AsyncGroup.setDescription('A collection of objects providing information\n                applicable to asynchronous RS-232-like interfaces.')
rs232SyncGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 33, 7, 1, 3)).setObjects(*(('RS-232-MIB', 'rs232SyncPortIndex'), ('RS-232-MIB', 'rs232SyncPortClockSource'), ('RS-232-MIB', 'rs232SyncPortFrameCheckErrs'), ('RS-232-MIB', 'rs232SyncPortTransmitUnderrunErrs'), ('RS-232-MIB', 'rs232SyncPortReceiveOverrunErrs'), ('RS-232-MIB', 'rs232SyncPortInterruptedFrames'), ('RS-232-MIB', 'rs232SyncPortAbortedFrames')))
if mibBuilder.loadTexts:
    rs232SyncGroup.setDescription('A collection of objects providing information\n                applicable to synchronous RS-232-like interfaces.')
rs232SyncSDLCGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 33, 7, 1, 4)).setObjects(*(('RS-232-MIB', 'rs232SyncPortRole'), ('RS-232-MIB', 'rs232SyncPortEncoding'), ('RS-232-MIB', 'rs232SyncPortRTSControl'), ('RS-232-MIB', 'rs232SyncPortRTSCTSDelay'), ('RS-232-MIB', 'rs232SyncPortMode'), ('RS-232-MIB', 'rs232SyncPortIdlePattern'), ('RS-232-MIB', 'rs232SyncPortMinFlags')))
if mibBuilder.loadTexts:
    rs232SyncSDLCGroup.setDescription('A collection of objects providing information\n                applicable to synchronous RS-232-like interfaces\n                running SDLC.')
mibBuilder.exportSymbols('RS-232-MIB', rs232OutSigState=rs232OutSigState, rs232SyncPortReceiveOverrunErrs=rs232SyncPortReceiveOverrunErrs, rs232PortInSigNumber=rs232PortInSigNumber, rs232AsyncPortParity=rs232AsyncPortParity, rs232AsyncPortStopBits=rs232AsyncPortStopBits, rs232SyncPortRTSControl=rs232SyncPortRTSControl, rs232SyncPortMinFlags=rs232SyncPortMinFlags, rs232Group=rs232Group, rs232SyncGroup=rs232SyncGroup, rs232AsyncPortIndex=rs232AsyncPortIndex, rs232InSigChanges=rs232InSigChanges, rs232InSigEntry=rs232InSigEntry, rs232AsyncPortBits=rs232AsyncPortBits, rs232PortInFlowType=rs232PortInFlowType, rs232AsyncPortOverrunErrs=rs232AsyncPortOverrunErrs, rs232OutSigName=rs232OutSigName, rs232Compliance=rs232Compliance, rs232SyncPortClockSource=rs232SyncPortClockSource, rs232SyncPortTable=rs232SyncPortTable, rs232SyncPortEncoding=rs232SyncPortEncoding, rs232InSigName=rs232InSigName, rs232Groups=rs232Groups, rs232SyncPortAbortedFrames=rs232SyncPortAbortedFrames, rs232AsyncPortTable=rs232AsyncPortTable, rs232Compliances=rs232Compliances, rs232SyncPortIdlePattern=rs232SyncPortIdlePattern, rs232PortInSpeed=rs232PortInSpeed, rs232InSigState=rs232InSigState, rs232SyncPortInterruptedFrames=rs232SyncPortInterruptedFrames, rs232SyncPortRole=rs232SyncPortRole, rs232SyncPortIndex=rs232SyncPortIndex, rs232PortTable=rs232PortTable, rs232SyncSDLCGroup=rs232SyncSDLCGroup, rs232OutSigPortIndex=rs232OutSigPortIndex, rs232AsyncPortParityErrs=rs232AsyncPortParityErrs, rs232AsyncPortEntry=rs232AsyncPortEntry, rs232SyncPortFrameCheckErrs=rs232SyncPortFrameCheckErrs, rs232PortOutSpeed=rs232PortOutSpeed, rs232PortEntry=rs232PortEntry, rs232InSigTable=rs232InSigTable, rs232OutSigEntry=rs232OutSigEntry, rs232Number=rs232Number, rs232InSigPortIndex=rs232InSigPortIndex, rs232AsyncPortAutobaud=rs232AsyncPortAutobaud, rs232PortOutSigNumber=rs232PortOutSigNumber, rs232=rs232, rs232PortType=rs232PortType, rs232PortIndex=rs232PortIndex, rs232SyncPortTransmitUnderrunErrs=rs232SyncPortTransmitUnderrunErrs, rs232SyncPortRTSCTSDelay=rs232SyncPortRTSCTSDelay, rs232OutSigChanges=rs232OutSigChanges, rs232AsyncPortFramingErrs=rs232AsyncPortFramingErrs, rs232SyncPortMode=rs232SyncPortMode, rs232SyncPortEntry=rs232SyncPortEntry, PYSNMP_MODULE_ID=rs232, rs232Conformance=rs232Conformance, rs232PortOutFlowType=rs232PortOutFlowType, rs232OutSigTable=rs232OutSigTable, rs232AsyncGroup=rs232AsyncGroup)