# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/TOKENRING-MIB.py
# Compiled at: 2016-02-13 18:31:49
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ValueSizeConstraint, ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsUnion', 'ValueRangeConstraint', 'ConstraintsIntersection')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(iso, IpAddress, ModuleIdentity, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, NotificationType, Integer32, TimeTicks, Bits, Counter64, Gauge32, Unsigned32, transmission, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'IpAddress', 'ModuleIdentity', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'NotificationType', 'Integer32', 'TimeTicks', 'Bits', 'Counter64', 'Gauge32', 'Unsigned32', 'transmission', 'Counter32')
(TextualConvention, MacAddress, DisplayString, TimeStamp) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'MacAddress', 'DisplayString', 'TimeStamp')
dot5 = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 9))
if mibBuilder.loadTexts:
    dot5.setLastUpdated('9410231150Z')
if mibBuilder.loadTexts:
    dot5.setOrganization('IETF Interfaces MIB Working Group')
if mibBuilder.loadTexts:
    dot5.setContactInfo('        Keith McCloghrie\n\n             Postal: cisco Systems, Inc.\n                     170 West Tasman Drive,\n                     San Jose, CA 95134-1706\n\n                     US\n\n              Phone: +1 408 526 5260\n              EMail: kzm@cisco.com')
if mibBuilder.loadTexts:
    dot5.setDescription('The MIB module for IEEE Token Ring entities.')
dot5Table = MibTable((1, 3, 6, 1, 2, 1, 10, 9, 1))
if mibBuilder.loadTexts:
    dot5Table.setDescription('This table contains Token Ring interface\n            parameters and state variables, one entry\n            per 802.5 interface.')
dot5Entry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 9, 1, 1)).setIndexNames((0, 'TOKENRING-MIB',
                                                                        'dot5IfIndex'))
if mibBuilder.loadTexts:
    dot5Entry.setDescription('A list of Token Ring status and parameter\n             values for an 802.5 interface.')
dot5IfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5IfIndex.setDescription('The value of this object identifies the\n             802.5 interface for which this entry\n             contains management information.  The\n             value of this object for a particular\n             interface has the same value as the\n             ifIndex object, defined in MIB-II for\n             the same interface.')
dot5Commands = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noop',
                                                                                                                                                                                      1), ('open',
                                                                                                                                                                                           2), ('reset',
                                                                                                                                                                                                3), ('close',
                                                                                                                                                                                                     4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dot5Commands.setDescription("When this object is set to the value of\n             open(2), the station should go into the\n             open state.  The progress and success of\n             the open is given by the values of the\n             objects dot5RingState and\n             dot5RingOpenStatus.\n                 When this object is set to the value\n             of reset(3), then the station should do\n             a reset.  On a reset, all MIB counters\n             should retain their values, if possible.\n             Other side affects are dependent on the\n             hardware chip set.\n                 When this object is set to the value\n             of close(4), the station should go into\n             the stopped state by removing itself\n             from the ring.\n                 Setting this object to a value of\n             noop(1) has no effect.\n                 When read, this object always has a\n             value of noop(1).\n                 The open(2) and close(4) values\n             correspond to the up(1) and down(2) values\n             of MIB-II's ifAdminStatus and ifOperStatus,\n             i.e., the setting of ifAdminStatus and\n\n             dot5Commands affects the values of both\n             dot5Commands and ifOperStatus.")
dot5RingStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 262143))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5RingStatus.setDescription("The current interface status which can\n            be used to diagnose fluctuating problems\n            that can occur on token rings, after a\n            station has successfully been added to\n            the ring.\n               Before an open is completed, this\n            object has the value for the 'no status'\n            condition.  The dot5RingState and\n            dot5RingOpenStatus objects provide for\n            debugging problems when the station\n            can not even enter the ring.\n                The object's value is a sum of\n            values, one for each currently applicable\n            condition.  The following values are\n            defined for various conditions:\n\n                    0 = No Problems detected\n                   32 = Ring Recovery\n                   64 = Single Station\n                  256 = Remove Received\n                  512 = reserved\n                 1024 = Auto-Removal Error\n                 2048 = Lobe Wire Fault\n                 4096 = Transmit Beacon\n                 8192 = Soft Error\n                16384 = Hard Error\n                32768 = Signal Loss\n               131072 = no status, open not completed.")
dot5RingState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('opened',
                                                                                                                                                                                             1), ('closed',
                                                                                                                                                                                                  2), ('opening',
                                                                                                                                                                                                       3), ('closing',
                                                                                                                                                                                                            4), ('openFailure',
                                                                                                                                                                                                                 5), ('ringFailure',
                                                                                                                                                                                                                      6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5RingState.setDescription('The current interface state with respect\n            to entering or leaving the ring.')
dot5RingOpenStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))).clone(namedValues=NamedValues(('noOpen',
                                                                                                                                                                                                                   1), ('badParam',
                                                                                                                                                                                                                        2), ('lobeFailed',
                                                                                                                                                                                                                             3), ('signalLoss',
                                                                                                                                                                                                                                  4), ('insertionTimeout',
                                                                                                                                                                                                                                       5), ('ringFailed',
                                                                                                                                                                                                                                            6), ('beaconing',
                                                                                                                                                                                                                                                 7), ('duplicateMAC',
                                                                                                                                                                                                                                                      8), ('requestFailed',
                                                                                                                                                                                                                                                           9), ('removeReceived',
                                                                                                                                                                                                                                                                10), ('open',
                                                                                                                                                                                                                                                                      11)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5RingOpenStatus.setDescription("This object indicates the success, or the\n            reason for failure, of the station's most\n            recent attempt to enter the ring.")
dot5RingSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('unknown',
                                                                                                                                                                                       1), ('oneMegabit',
                                                                                                                                                                                            2), ('fourMegabit',
                                                                                                                                                                                                 3), ('sixteenMegabit',
                                                                                                                                                                                                      4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dot5RingSpeed.setDescription("The ring-speed at the next insertion into\n            the ring.  Note that this may or may not be\n            different to the current ring-speed which is\n            given by MIB-II's ifSpeed.  For interfaces\n            which do not support changing ring-speed,\n            dot5RingSpeed can only be set to its current\n            value.  When dot5RingSpeed has the value\n            unknown(1), the ring's actual ring-speed is\n            to be used.")
dot5UpStream = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 7), MacAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5UpStream.setDescription('The MAC-address of the up stream neighbor\n             station in the ring.')
dot5ActMonParticipate = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('true',
                                                                                                                                                                                         1), ('false',
                                                                                                                                                                                              2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dot5ActMonParticipate.setDescription('If this object has a value of true(1) then\n            this interface will participate in the\n            active monitor selection process.  If the\n            value is false(2) then it will not.\n            Setting this object does not take effect\n            until the next Active Monitor election, and\n            might not take effect until the next time\n            the interface is opened.')
dot5Functional = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 9), MacAddress()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dot5Functional.setDescription('The bit mask of all Token Ring functional\n            addresses for which this interface will\n            accept frames.')
dot5LastBeaconSent = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 1, 1, 10), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5LastBeaconSent.setDescription("The value of MIB-II's sysUpTime object at which\n            the local system last transmitted a Beacon frame\n            on this interface.")
dot5StatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 9, 2))
if mibBuilder.loadTexts:
    dot5StatsTable.setDescription("A table containing Token Ring statistics,\n            one entry per 802.5 interface.\n                All the statistics are defined using\n            the syntax Counter32 as 32-bit wrap around\n            counters.  Thus, if an interface's\n            hardware maintains these statistics in\n            16-bit counters, then the agent must read\n            the hardware's counters frequently enough\n            to prevent loss of significance, in order\n            to maintain 32-bit counters in software.")
dot5StatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 9, 2, 1)).setIndexNames((0, 'TOKENRING-MIB',
                                                                             'dot5StatsIfIndex'))
if mibBuilder.loadTexts:
    dot5StatsEntry.setDescription('An entry contains the 802.5 statistics\n             for a particular interface.')
dot5StatsIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsIfIndex.setDescription("The value of this object identifies the\n            802.5 interface for which this entry\n            contains management information.  The\n            value of this object for a particular\n            interface has the same value as MIB-II's\n            ifIndex object for the same interface.")
dot5StatsLineErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsLineErrors.setDescription('This counter is incremented when a frame\n            or token is copied or repeated by a\n            station, the E bit is zero in the frame\n            or token and one of the following\n            conditions exists: 1) there is a\n            non-data bit (J or K bit) between the SD\n            and the ED of the frame or token, or\n            2) there is an FCS error in the frame.')
dot5StatsBurstErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsBurstErrors.setDescription('This counter is incremented when a station\n            detects the absence of transitions for five\n            half-bit timers (burst-five error).')
dot5StatsACErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsACErrors.setDescription('This counter is incremented when a station\n            receives an AMP or SMP frame in which A is\n            equal to C is equal to 0, and then receives\n            another SMP frame with A is equal to C is\n            equal to 0 without first receiving an AMP\n            frame. It denotes a station that cannot set\n            the AC bits properly.')
dot5StatsAbortTransErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsAbortTransErrors.setDescription('This counter is incremented when a station\n            transmits an abort delimiter while\n            transmitting.')
dot5StatsInternalErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsInternalErrors.setDescription('This counter is incremented when a station\n            recognizes an internal error.')
dot5StatsLostFrameErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsLostFrameErrors.setDescription('This counter is incremented when a station\n            is transmitting and its TRR timer expires.\n            This condition denotes a condition where a\n            transmitting station in strip mode does not\n            receive the trailer of the frame before the\n            TRR timer goes off.')
dot5StatsReceiveCongestions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsReceiveCongestions.setDescription('This counter is incremented when a station\n            recognizes a frame addressed to its\n            specific address, but has no available\n            buffer space indicating that the station\n            is congested.')
dot5StatsFrameCopiedErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsFrameCopiedErrors.setDescription('This counter is incremented when a station\n            recognizes a frame addressed to its\n            specific address and detects that the FS\n            field A bits are set to 1 indicating a\n            possible line hit or duplicate address.')
dot5StatsTokenErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsTokenErrors.setDescription('This counter is incremented when a station\n            acting as the active monitor recognizes an\n            error condition that needs a token\n            transmitted.')
dot5StatsSoftErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsSoftErrors.setDescription('The number of Soft Errors the interface\n            has detected. It directly corresponds to\n            the number of Report Error MAC frames\n            that this interface has transmitted.\n            Soft Errors are those which are\n            recoverable by the MAC layer protocols.')
dot5StatsHardErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsHardErrors.setDescription('The number of times this interface has\n            detected an immediately recoverable\n            fatal error.  It denotes the number of\n            times this interface is either\n            transmitting or receiving beacon MAC\n            frames.')
dot5StatsSignalLoss = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsSignalLoss.setDescription('The number of times this interface has\n            detected the loss of signal condition from\n            the ring.')
dot5StatsTransmitBeacons = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsTransmitBeacons.setDescription('The number of times this interface has\n            transmitted a beacon frame.')
dot5StatsRecoverys = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsRecoverys.setDescription('The number of Claim Token MAC frames\n            received or transmitted after the interface\n            has received a Ring Purge MAC frame.  This\n            counter signifies the number of times the\n            ring has been purged and is being recovered\n            back into a normal operating state.')
dot5StatsLobeWires = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 16), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsLobeWires.setDescription('The number of times the interface has\n            detected an open or short circuit in the\n            lobe data path.  The adapter will be closed\n            and dot5RingState will signify this\n            condition.')
dot5StatsRemoves = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsRemoves.setDescription('The number of times the interface has\n            received a Remove Ring Station MAC frame\n            request.  When this frame is received\n            the interface will enter the close state\n            and dot5RingState will signify this\n            condition.')
dot5StatsSingles = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 18), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsSingles.setDescription('The number of times the interface has\n            sensed that it is the only station on the\n            ring.  This will happen if the interface\n            is the first one up on a ring, or if\n            there is a hardware problem.')
dot5StatsFreqErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 2, 1, 19), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5StatsFreqErrors.setDescription('The number of times the interface has\n            detected that the frequency of the\n            incoming signal differs from the expected\n            frequency by more than that specified by\n            the IEEE 802.5 standard.')
dot5TimerTable = MibTable((1, 3, 6, 1, 2, 1, 10, 9, 5))
if mibBuilder.loadTexts:
    dot5TimerTable.setDescription('This table contains Token Ring interface\n            timer values, one entry per 802.5\n            interface.')
dot5TimerEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 9, 5, 1)).setIndexNames((0, 'TOKENRING-MIB',
                                                                             'dot5TimerIfIndex'))
if mibBuilder.loadTexts:
    dot5TimerEntry.setDescription('A list of Token Ring timer values for an\n            802.5 interface.')
dot5TimerIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerIfIndex.setDescription("The value of this object identifies the\n             802.5 interface for which this entry\n             contains timer values.  The value of\n\n             this object for a particular interface\n             has the same value as MIB-II's ifIndex\n             object for the same interface.")
dot5TimerReturnRepeat = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 2), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerReturnRepeat.setDescription('The time-out value used to ensure the\n            interface will return to Repeat State, in\n            units of 100 micro-seconds.  The value\n            should be greater than the maximum ring\n            latency.')
dot5TimerHolding = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerHolding.setDescription('Maximum period of time a station is\n            permitted to transmit frames after capturing\n            a token, in units of 100 micro-seconds.')
dot5TimerQueuePDU = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerQueuePDU.setDescription('The time-out value for enqueuing of an SMP\n            PDU after reception of an AMP or SMP\n            frame in which the A and C bits were\n            equal to 0, in units of 100\n            micro-seconds.')
dot5TimerValidTransmit = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerValidTransmit.setDescription('The time-out value used by the active\n            monitor to detect the absence of valid\n            transmissions, in units of 100\n            micro-seconds.')
dot5TimerNoToken = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerNoToken.setDescription('The time-out value used to recover from\n            various-related error situations.\n            If N is the maximum number of stations on\n            the ring, the value of this timer is\n            normally:\n            dot5TimerReturnRepeat + N*dot5TimerHolding.')
dot5TimerActiveMon = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerActiveMon.setDescription('The time-out value used by the active\n            monitor to stimulate the enqueuing of an\n            AMP PDU for transmission, in units of\n            100 micro-seconds.')
dot5TimerStandbyMon = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 8), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerStandbyMon.setDescription('The time-out value used by the stand-by\n            monitors to ensure that there is an active\n            monitor on the ring and to detect a\n            continuous stream of tokens, in units of\n            100 micro-seconds.')
dot5TimerErrorReport = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 9), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerErrorReport.setDescription('The time-out value which determines how\n            often a station shall send a Report Error\n            MAC frame to report its error counters,\n            in units of 100 micro-seconds.')
dot5TimerBeaconTransmit = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 10), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerBeaconTransmit.setDescription('The time-out value which determines how\n            long a station shall remain in the state\n            of transmitting Beacon frames before\n            entering the Bypass state, in units of\n            100 micro-seconds.')
dot5TimerBeaconReceive = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 9, 5, 1, 11), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dot5TimerBeaconReceive.setDescription('The time-out value which determines how\n            long a station shall receive Beacon\n            frames from its downstream neighbor\n            before entering the Bypass state, in\n            units of 100 micro-seconds.')
dot5Tests = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 9, 3))
dot5TestInsertFunc = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 9, 3, 1))
if mibBuilder.loadTexts:
    dot5TestInsertFunc.setDescription("Invoking this test causes the station to test the insert\n        ring logic of the hardware if the station's lobe media\n        cable is connected to a wiring concentrator.  Note that\n        this command inserts the station into the network, and\n        thus, could cause problems if the station is connected\n        to a operational network.")
dot5TestFullDuplexLoopBack = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 9, 3, 2))
if mibBuilder.loadTexts:
    dot5TestFullDuplexLoopBack.setDescription("Invoking this test on a 802.5 interface causes the\n        interface to check the path from memory through the\n        chip set's internal logic and back to memory, thus\n        checking the proper functioning of the system's\n        interface to the chip set.")
dot5ChipSets = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 9, 4))
dot5ChipSetIBM16 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 9, 4, 1))
if mibBuilder.loadTexts:
    dot5ChipSetIBM16.setDescription("IBM's 16/4 Mbs chip set.")
dot5ChipSetTItms380 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 9, 4, 2))
if mibBuilder.loadTexts:
    dot5ChipSetTItms380.setDescription("Texas Instruments' TMS 380 4Mbs chip-set")
dot5ChipSetTItms380c16 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 9, 4, 3))
if mibBuilder.loadTexts:
    dot5ChipSetTItms380c16.setDescription("Texas Instruments' TMS 380C16 16/4 Mbs chip-set")
dot5Conformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 9, 6))
dot5Groups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 9, 6, 1))
dot5Compliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 9, 6, 2))
dot5Compliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 9, 6, 2, 1)).setObjects(*(('TOKENRING-MIB', 'dot5StateGroup'), ('TOKENRING-MIB', 'dot5StatsGroup')))
if mibBuilder.loadTexts:
    dot5Compliance.setDescription('The compliance statement for SNMPv2 entities\n        which implement the IEEE 802.5 MIB.')
dot5StateGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 9, 6, 1, 1)).setObjects(*(('TOKENRING-MIB', 'dot5Commands'), ('TOKENRING-MIB', 'dot5RingStatus'), ('TOKENRING-MIB', 'dot5RingState'), ('TOKENRING-MIB', 'dot5RingOpenStatus'), ('TOKENRING-MIB', 'dot5RingSpeed'), ('TOKENRING-MIB', 'dot5UpStream'), ('TOKENRING-MIB', 'dot5ActMonParticipate'), ('TOKENRING-MIB', 'dot5Functional'), ('TOKENRING-MIB', 'dot5LastBeaconSent')))
if mibBuilder.loadTexts:
    dot5StateGroup.setDescription('A collection of objects providing state information\n        and parameters for IEEE 802.5 interfaces.')
dot5StatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 9, 6, 1, 2)).setObjects(*(('TOKENRING-MIB', 'dot5StatsLineErrors'), ('TOKENRING-MIB', 'dot5StatsBurstErrors'), ('TOKENRING-MIB', 'dot5StatsACErrors'), ('TOKENRING-MIB', 'dot5StatsAbortTransErrors'), ('TOKENRING-MIB', 'dot5StatsInternalErrors'), ('TOKENRING-MIB', 'dot5StatsLostFrameErrors'), ('TOKENRING-MIB', 'dot5StatsReceiveCongestions'), ('TOKENRING-MIB', 'dot5StatsFrameCopiedErrors'), ('TOKENRING-MIB', 'dot5StatsTokenErrors'), ('TOKENRING-MIB', 'dot5StatsSoftErrors'), ('TOKENRING-MIB', 'dot5StatsHardErrors'), ('TOKENRING-MIB', 'dot5StatsSignalLoss'), ('TOKENRING-MIB', 'dot5StatsTransmitBeacons'), ('TOKENRING-MIB', 'dot5StatsRecoverys'), ('TOKENRING-MIB', 'dot5StatsLobeWires'), ('TOKENRING-MIB', 'dot5StatsRemoves'), ('TOKENRING-MIB', 'dot5StatsSingles'), ('TOKENRING-MIB', 'dot5StatsFreqErrors')))
if mibBuilder.loadTexts:
    dot5StatsGroup.setDescription('A collection of objects providing statistics for\n        IEEE 802.5 interfaces.')
mibBuilder.exportSymbols('TOKENRING-MIB', dot5=dot5, dot5StatsACErrors=dot5StatsACErrors, dot5StatsTransmitBeacons=dot5StatsTransmitBeacons, dot5RingOpenStatus=dot5RingOpenStatus, dot5StateGroup=dot5StateGroup, dot5Groups=dot5Groups, dot5Compliances=dot5Compliances, dot5TestInsertFunc=dot5TestInsertFunc, dot5Functional=dot5Functional, dot5StatsBurstErrors=dot5StatsBurstErrors, dot5Table=dot5Table, dot5TimerBeaconReceive=dot5TimerBeaconReceive, dot5StatsHardErrors=dot5StatsHardErrors, dot5TimerValidTransmit=dot5TimerValidTransmit, dot5StatsSingles=dot5StatsSingles, dot5RingState=dot5RingState, dot5TimerStandbyMon=dot5TimerStandbyMon, dot5ChipSets=dot5ChipSets, dot5StatsRecoverys=dot5StatsRecoverys, dot5TestFullDuplexLoopBack=dot5TestFullDuplexLoopBack, dot5ChipSetTItms380c16=dot5ChipSetTItms380c16, dot5StatsLostFrameErrors=dot5StatsLostFrameErrors, dot5Commands=dot5Commands, dot5TimerTable=dot5TimerTable, dot5ChipSetIBM16=dot5ChipSetIBM16, dot5LastBeaconSent=dot5LastBeaconSent, dot5StatsAbortTransErrors=dot5StatsAbortTransErrors, dot5StatsTokenErrors=dot5StatsTokenErrors, dot5StatsSoftErrors=dot5StatsSoftErrors, dot5Tests=dot5Tests, dot5StatsIfIndex=dot5StatsIfIndex, dot5Entry=dot5Entry, dot5StatsRemoves=dot5StatsRemoves, dot5TimerBeaconTransmit=dot5TimerBeaconTransmit, dot5StatsInternalErrors=dot5StatsInternalErrors, dot5StatsLineErrors=dot5StatsLineErrors, dot5StatsReceiveCongestions=dot5StatsReceiveCongestions, dot5TimerNoToken=dot5TimerNoToken, dot5RingSpeed=dot5RingSpeed, dot5TimerErrorReport=dot5TimerErrorReport, dot5TimerReturnRepeat=dot5TimerReturnRepeat, dot5StatsTable=dot5StatsTable, dot5StatsSignalLoss=dot5StatsSignalLoss, dot5ActMonParticipate=dot5ActMonParticipate, dot5TimerEntry=dot5TimerEntry, PYSNMP_MODULE_ID=dot5, dot5StatsEntry=dot5StatsEntry, dot5TimerHolding=dot5TimerHolding, dot5TimerQueuePDU=dot5TimerQueuePDU, dot5StatsGroup=dot5StatsGroup, dot5TimerIfIndex=dot5TimerIfIndex, dot5TimerActiveMon=dot5TimerActiveMon, dot5UpStream=dot5UpStream, dot5StatsFrameCopiedErrors=dot5StatsFrameCopiedErrors, dot5RingStatus=dot5RingStatus, dot5StatsLobeWires=dot5StatsLobeWires, dot5StatsFreqErrors=dot5StatsFreqErrors, dot5ChipSetTItms380=dot5ChipSetTItms380, dot5Conformance=dot5Conformance, dot5IfIndex=dot5IfIndex, dot5Compliance=dot5Compliance)