# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/RFC1316-MIB.py
# Compiled at: 2016-02-13 18:26:15
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection', 'ValueRangeConstraint')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Bits, Integer32, iso, IpAddress, NotificationType, Unsigned32, Counter64, MibIdentifier, Gauge32, ObjectIdentity, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, mib_2, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Bits', 'Integer32', 'iso', 'IpAddress', 'NotificationType', 'Unsigned32', 'Counter64', 'MibIdentifier', 'Gauge32', 'ObjectIdentity', 'ModuleIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'TimeTicks', 'mib-2', 'Counter32')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
char = MibIdentifier((1, 3, 6, 1, 2, 1, 19))

class AutonomousType(ObjectIdentifier):
    __module__ = __name__


class InstancePointer(ObjectIdentifier):
    __module__ = __name__


charNumber = MibScalar((1, 3, 6, 1, 2, 1, 19, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charNumber.setDescription('The number of entries in charPortTable, regardless\n                    of their current state.')
charPortTable = MibTable((1, 3, 6, 1, 2, 1, 19, 2))
if mibBuilder.loadTexts:
    charPortTable.setDescription('A list of port entries.  The number of entries is\n                    given by the value of charNumber.')
charPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 19, 2, 1)).setIndexNames((0, 'RFC1316-MIB',
                                                                         'charPortIndex'))
if mibBuilder.loadTexts:
    charPortEntry.setDescription('Status and parameter values for a character port.')
charPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortIndex.setDescription('A unique value for each character port.  Its value\n                    ranges between 1 and the value of charNumber.  By\n                    convention and if possible, hardware port numbers\n                    come first, with a simple, direct mapping.  The\n                    value for each port must remain constant at least\n                    from one re-initialization of the network management\n                    agent to the next.')
charPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 32))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortName.setDescription('An administratively assigned name for the port,\n                    typically with some local significance.')
charPortType = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('physical',
                                                                                                                                                                             1), ('virtual',
                                                                                                                                                                                  2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortType.setDescription("The port's type, 'physical' if the port represents\n                    an external hardware connector, 'virtual' if it does\n                    not.")
charPortHardware = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 4), AutonomousType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortHardware.setDescription("A reference to hardware MIB definitions specific to\n                    a physical port's external connector.  For example,\n                    if the connector is RS-232, then the value of this\n                    object refers to a MIB sub-tree defining objects\n                    specific to RS-232.  If an agent is not configured\n                    to have such values, the agent returns the object\n                    identifier:\n\n                        nullHardware OBJECT IDENTIFIER ::= { 0 0 }\n                    ")
charPortReset = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('ready',
                                                                                                                                                                              1), ('execute',
                                                                                                                                                                                   2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortReset.setDescription("A control to force the port into a clean, initial\n                    state, both hardware and software, disconnecting all\n                    the port's existing sessions.  In response to a\n                    get-request or get-next-request, the agent always\n                    returns 'ready' as the value.  Setting the value to\n                    'execute' causes a reset.")
charPortAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                          1), ('disabled',
                                                                                                                                                                                               2), ('off',
                                                                                                                                                                                                    3), ('maintenance',
                                                                                                                                                                                                         4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortAdminStatus.setDescription("The port's desired state, independent of flow\n                    control.  'enabled' indicates that the port is\n                    allowed to pass characters and form new sessions.\n                    'disabled' indicates that the port is allowed to\n                    pass characters but not form new sessions.  'off'\n                    indicates that the port is not allowed to pass\n                    characters or have any sessions. 'maintenance'\n                    indicates a maintenance mode, exclusive of normal\n                    operation, such as running a test.")
charPortOperStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('up',
                                                                                                                                                                                            1), ('down',
                                                                                                                                                                                                 2), ('maintenance',
                                                                                                                                                                                                      3), ('absent',
                                                                                                                                                                                                           4), ('active',
                                                                                                                                                                                                                5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortOperStatus.setDescription("The port's actual, operational state, independent\n                    of flow control.  'up' indicates able to function\n                    normally.  'down' indicates inability to function\n                    for administrative or operational reasons.\n                    'maintenance' indicates a maintenance mode,\n                    exclusive of normal operation, such as running a\n                    test.  'absent' indicates that port hardware is not\n                    present.  'active' indicates up with a user present\n                    (e.g. logged in).")
charPortLastChange = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 8), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortLastChange.setDescription('The value of sysUpTime at the time the port entered\n                    its current operational state.  If the current state\n                    was entered prior to the last reinitialization of\n                    the local network management subsystem, then this\n                    object contains a zero value.')
charPortInFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                            1), ('xonXoff',
                                                                                                                                                                                                 2), ('hardware',
                                                                                                                                                                                                      3), ('ctsRts',
                                                                                                                                                                                                           4), ('dsrDtr',
                                                                                                                                                                                                                5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortInFlowType.setDescription("The port's type of input flow control.  'none'\n                    indicates no flow control at this level or below.\n                    'xonXoff' indicates software flow control by\n                    recognizing XON and XOFF characters.  'hardware'\n                    indicates flow control delegated to the lower level,\n                    for example a parallel port.\n\n                    'ctsRts' and 'dsrDtr' are specific to RS-232-like\n                    ports.  Although not architecturally pure, they are\n                    included here for simplicity's sake.")
charPortOutFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                              1), ('xonXoff',
                                                                                                                                                                                                   2), ('hardware',
                                                                                                                                                                                                        3), ('ctsRts',
                                                                                                                                                                                                             4), ('dsrDtr',
                                                                                                                                                                                                                  5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortOutFlowType.setDescription("The port's type of output flow control.  'none'\n                    indicates no flow control at this level or below.\n                    'xonXoff' indicates software flow control by\n                    recognizing XON and XOFF characters.  'hardware'\n                    indicates flow control delegated to the lower level,\n                    for example a parallel port.\n\n                    'ctsRts' and 'dsrDtr' are specific to RS-232-like\n                    ports.  Although not architecturally pure, they are\n                    included here for simplicy's sake.")
charPortInFlowState = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                           1), ('unknown',
                                                                                                                                                                                                2), ('stop',
                                                                                                                                                                                                     3), ('go',
                                                                                                                                                                                                          4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortInFlowState.setDescription("The current operational state of input flow control\n                    on the port.  'none' indicates not applicable.\n                    'unknown' indicates this level does not know.\n                    'stop' indicates flow not allowed.  'go' indicates\n                    flow allowed.")
charPortOutFlowState = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                            1), ('unknown',
                                                                                                                                                                                                 2), ('stop',
                                                                                                                                                                                                      3), ('go',
                                                                                                                                                                                                           4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortOutFlowState.setDescription("The current operational state of output flow\n                    control on the port.  'none' indicates not\n                    applicable.  'unknown' indicates this level does not\n                    know.  'stop' indicates flow not allowed.  'go'\n                    indicates flow allowed.")
charPortInCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortInCharacters.setDescription("Total number of characters detected as input from\n                    the port since system re-initialization and while\n                    the port operational state was 'up', 'active', or\n                    'maintenance', including, for example, framing, flow\n                    control (i.e. XON and XOFF), each occurrence of a\n                    BREAK condition, locally-processed input, and input\n                    sent to all sessions.")
charPortOutCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortOutCharacters.setDescription("Total number of characters detected as output to\n                    the port since system re-initialization and while\n                    the port operational state was 'up', 'active', or\n                    'maintenance', including, for example, framing, flow\n                    control (i.e. XON and XOFF), each occurrence of a\n                    BREAK condition, locally-created output, and output\n                    received from all sessions.")
charPortAdminOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 15), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('dynamic',
                                                                                                                                                                                           1), ('network',
                                                                                                                                                                                                2), ('local',
                                                                                                                                                                                                     3), ('none',
                                                                                                                                                                                                          4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortAdminOrigin.setDescription("The administratively allowed origin for\n                    establishing session on the port.  'dynamic' allows\n                    'network' or 'local' session establishment. 'none'\n                    disallows session establishment.")
charPortSessionMaximum = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 16), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charPortSessionMaximum.setDescription('The maximum number of concurrent sessions allowed\n                    on the port.  A value of -1 indicates no maximum.\n                    Setting the maximum to less than the current number\n                    of sessions has unspecified results.')
charPortSessionNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 17), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortSessionNumber.setDescription('The number of open sessions on the port that are in\n                    the connecting, connected, or disconnecting state.')
charPortSessionIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 2, 1, 18), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charPortSessionIndex.setDescription("The value of charSessIndex for the port's first or\n                    only active session.  If the port has no active\n                    session, the agent returns the value zero.")
charSessTable = MibTable((1, 3, 6, 1, 2, 1, 19, 3))
if mibBuilder.loadTexts:
    charSessTable.setDescription('A list of port session entries.')
charSessEntry = MibTableRow((1, 3, 6, 1, 2, 1, 19, 3, 1)).setIndexNames((0, 'RFC1316-MIB',
                                                                         'charSessPortIndex'), (0,
                                                                                                'RFC1316-MIB',
                                                                                                'charSessIndex'))
if mibBuilder.loadTexts:
    charSessEntry.setDescription('Status and parameter values for a character port\n                    session.')
charSessPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessPortIndex.setDescription('The value of charPortIndex for the port to which\n                    this session belongs.')
charSessIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 2), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessIndex.setDescription('The session index in the context of the port, a\n                    non-zero positive integer.  Session indexes within a\n                    port need not be sequential.  Session indexes may be\n                    reused for different ports.  For example, port 1 and\n                    port 3 may both have a session 2 at the same time.\n                    Session indexes may have any valid integer value,\n                    with any meaning convenient to the agent\n                    implementation.')
charSessKill = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('ready',
                                                                                                                                                                             1), ('execute',
                                                                                                                                                                                  2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    charSessKill.setDescription("A control to terminate the session.  In response to\n                    a get-request or get-next-request, the agent always\n                    returns 'ready' as the value.  Setting the value to\n                    'execute' causes termination.")
charSessState = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('connecting',
                                                                                                                                                                                 1), ('connected',
                                                                                                                                                                                      2), ('disconnecting',
                                                                                                                                                                                           3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessState.setDescription("The current operational state of the session,\n                    disregarding flow control.  'connected' indicates\n                    that character data could flow on the network side\n                    of session.  'connecting' indicates moving from\n                    nonexistent toward 'connected'.  'disconnecting'\n                    indicates moving from 'connected' or 'connecting' to\n                    nonexistent.")
charSessProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 5), AutonomousType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessProtocol.setDescription('The network protocol over which the session is\n                    running.  Other OBJECT IDENTIFIER values may be\n                    defined elsewhere, in association with specific\n                    protocols.  However, this document assigns those of\n                    known interest as of this writing.')
wellKnownProtocols = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4))
protocolOther = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 1))
protocolTelnet = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 2))
protocolRlogin = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 3))
protocolLat = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 4))
protocolX29 = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 5))
protocolVtp = MibIdentifier((1, 3, 6, 1, 2, 1, 19, 4, 6))
charSessOperOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('unknown',
                                                                                                                                                                                      1), ('network',
                                                                                                                                                                                           2), ('local',
                                                                                                                                                                                                3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessOperOrigin.setDescription("The session's source of establishment.")
charSessInCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessInCharacters.setDescription("This session's subset of charPortInCharacters.")
charSessOutCharacters = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessOutCharacters.setDescription("This session's subset of charPortOutCharacters.")
charSessConnectionId = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 9), InstancePointer()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessConnectionId.setDescription('A reference to additional local MIB information.\n                    This should be the highest available related MIB,\n                    corresponding to charSessProtocol, such as Telnet.\n                    For example, the value for a TCP connection (in the\n                    absence of a Telnet MIB) is the object identifier of\n                    tcpConnState.  If an agent is not configured to have\n                    such values, the agent returns the object\n                    identifier:\n\n                        nullConnectionId OBJECT IDENTIFIER ::= { 0 0 }\n                    ')
charSessStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 19, 3, 1, 10), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    charSessStartTime.setDescription('The value of sysUpTime in MIB-2 when the session\n                    entered connecting state.')
mibBuilder.exportSymbols('RFC1316-MIB', charSessOutCharacters=charSessOutCharacters, protocolRlogin=protocolRlogin, charNumber=charNumber, wellKnownProtocols=wellKnownProtocols, charPortEntry=charPortEntry, charPortReset=charPortReset, charPortAdminOrigin=charPortAdminOrigin, charSessInCharacters=charSessInCharacters, charPortOperStatus=charPortOperStatus, charSessKill=charSessKill, InstancePointer=InstancePointer, charSessProtocol=charSessProtocol, charSessEntry=charSessEntry, charSessIndex=charSessIndex, charPortLastChange=charPortLastChange, charPortSessionMaximum=charPortSessionMaximum, charSessOperOrigin=charSessOperOrigin, charSessTable=charSessTable, charSessStartTime=charSessStartTime, charPortIndex=charPortIndex, charPortOutCharacters=charPortOutCharacters, protocolX29=protocolX29, protocolLat=protocolLat, charPortType=charPortType, charPortInFlowState=charPortInFlowState, charPortAdminStatus=charPortAdminStatus, charSessState=charSessState, charPortInFlowType=charPortInFlowType, charSessConnectionId=charSessConnectionId, protocolVtp=protocolVtp, charPortOutFlowType=charPortOutFlowType, charPortSessionNumber=charPortSessionNumber, charPortSessionIndex=charPortSessionIndex, protocolOther=protocolOther, charPortHardware=charPortHardware, AutonomousType=AutonomousType, charPortInCharacters=charPortInCharacters, charPortTable=charPortTable, charPortName=charPortName, charSessPortIndex=charSessPortIndex, protocolTelnet=protocolTelnet, char=char, charPortOutFlowState=charPortOutFlowState)