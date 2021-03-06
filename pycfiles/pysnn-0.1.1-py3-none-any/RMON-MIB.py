# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/RMON-MIB.py
# Compiled at: 2016-02-13 18:04:25
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ConstraintsUnion, ValueRangeConstraint, ValueSizeConstraint, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ConstraintsUnion', 'ValueRangeConstraint', 'ValueSizeConstraint', 'SingleValueConstraint')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(ModuleIdentity, IpAddress, Bits, Gauge32, mib_2, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, Counter64, MibIdentifier, ObjectIdentity, NotificationType, Counter32, Unsigned32, TimeTicks, Integer32) = mibBuilder.importSymbols('SNMPv2-SMI', 'ModuleIdentity', 'IpAddress', 'Bits', 'Gauge32', 'mib-2', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'iso', 'Counter64', 'MibIdentifier', 'ObjectIdentity', 'NotificationType', 'Counter32', 'Unsigned32', 'TimeTicks', 'Integer32')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
rmonMibModule = ModuleIdentity((1, 3, 6, 1, 2, 1, 16, 20, 8)).setRevisions(('2000-05-11 00:00', '1995-02-01 00:00', '1991-11-01 00:00'))
if mibBuilder.loadTexts:
    rmonMibModule.setLastUpdated('200005110000Z')
if mibBuilder.loadTexts:
    rmonMibModule.setOrganization('IETF RMON MIB Working Group')
if mibBuilder.loadTexts:
    rmonMibModule.setContactInfo('Steve Waldbusser\n            Phone: +1-650-948-6500\n            Fax:   +1-650-745-0671\n            Email: waldbusser@nextbeacon.com')
if mibBuilder.loadTexts:
    rmonMibModule.setDescription('Remote network monitoring devices, often called\n            monitors or probes, are instruments that exist for\n            the purpose of managing a network. This MIB defines\n            objects for managing remote network monitoring devices.')
rmon = MibIdentifier((1, 3, 6, 1, 2, 1, 16))

class OwnerString(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 127)


class EntryStatus(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))
    namedValues = NamedValues(('valid', 1), ('createRequest', 2), ('underCreation',
                                                                   3), ('invalid',
                                                                        4))


statistics = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 1))
history = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 2))
alarm = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 3))
hosts = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 4))
hostTopN = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 5))
matrix = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 6))
filter = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 7))
capture = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 8))
event = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 9))
rmonConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 20))
etherStatsTable = MibTable((1, 3, 6, 1, 2, 1, 16, 1, 1))
if mibBuilder.loadTexts:
    etherStatsTable.setDescription('A list of Ethernet statistics entries.')
etherStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 1, 1, 1)).setIndexNames((0, 'RMON-MIB', 'etherStatsIndex'))
if mibBuilder.loadTexts:
    etherStatsEntry.setDescription('A collection of statistics kept for a particular\n            Ethernet interface.  As an example, an instance of the\n            etherStatsPkts object might be named etherStatsPkts.1')
etherStatsIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsIndex.setDescription('The value of this object uniquely identifies this\n            etherStats entry.')
etherStatsDataSource = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 2), ObjectIdentifier()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    etherStatsDataSource.setDescription('This object identifies the source of the data that\n            this etherStats entry is configured to analyze.  This\n            source can be any ethernet interface on this device.\n            In order to identify a particular interface, this object\n            shall identify the instance of the ifIndex object,\n            defined in RFC 2233 [17], for the desired interface.\n            For example, if an entry were to receive data from\n            interface #1, this object would be set to ifIndex.1.\n            \n            The statistics in this group reflect all packets\n            on the local network segment attached to the identified\n            interface.\n            \n            An agent may or may not be able to tell if fundamental\n            changes to the media of the interface have occurred and\n            necessitate an invalidation of this entry.  For example, a\n            hot-pluggable ethernet card could be pulled out and replaced\n            by a token-ring card.  In such a case, if the agent has such\n            knowledge of the change, it is recommended that it\n            invalidate this entry.\n            \n            This object may not be modified if the associated\n            etherStatsStatus object is equal to valid(1).')
etherStatsDropEvents = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsDropEvents.setDescription('The total number of events in which packets\n            were dropped by the probe due to lack of resources.\n            Note that this number is not necessarily the number of\n            packets dropped; it is just the number of times this\n            condition has been detected.')
etherStatsOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 4), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsOctets.setDescription('The total number of octets of data (including\n            those in bad packets) received on the\n            network (excluding framing bits but including\n            FCS octets).\n\n            This object can be used as a reasonable estimate of\n            10-Megabit ethernet utilization.  If greater precision is\n            desired, the etherStatsPkts and etherStatsOctets objects\n            should be sampled before and after a common interval.  The\n            differences in the sampled values are Pkts and Octets,\n            respectively, and the number of seconds in the interval is\n            Interval.  These values are used to calculate the Utilization\n            as follows:\n            \n                            Pkts * (9.6 + 6.4) + (Octets * .8)\n            Utilization = -------------------------------------\n                                  Interval * 10,000\n            \n            The result of this equation is the value Utilization which\n            is the percent utilization of the ethernet segment on a\n            scale of 0 to 100 percent.')
etherStatsPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 5), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts.setDescription('The total number of packets (including bad packets,\n            broadcast packets, and multicast packets) received.')
etherStatsBroadcastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 6), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsBroadcastPkts.setDescription('The total number of good packets received that were\n            directed to the broadcast address.  Note that this\n            does not include multicast packets.')
etherStatsMulticastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 7), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsMulticastPkts.setDescription('The total number of good packets received that were\n            directed to a multicast address.  Note that this number\n            does not include packets directed to the broadcast\n            address.')
etherStatsCRCAlignErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 8), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsCRCAlignErrors.setDescription('The total number of packets received that\n            had a length (excluding framing bits, but\n            including FCS octets) of between 64 and 1518\n            octets, inclusive, but had either a bad\n            Frame Check Sequence (FCS) with an integral\n            number of octets (FCS Error) or a bad FCS with\n            a non-integral number of octets (Alignment Error).')
etherStatsUndersizePkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 9), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsUndersizePkts.setDescription('The total number of packets received that were\n            less than 64 octets long (excluding framing bits,\n            but including FCS octets) and were otherwise well\n            formed.')
etherStatsOversizePkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 10), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsOversizePkts.setDescription('The total number of packets received that were\n            longer than 1518 octets (excluding framing bits,\n            but including FCS octets) and were otherwise\n            well formed.')
etherStatsFragments = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 11), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsFragments.setDescription('The total number of packets received that were less than\n            64 octets in length (excluding framing bits but including\n            FCS octets) and had either a bad Frame Check Sequence\n            (FCS) with an integral number of octets (FCS Error) or a\n            bad FCS with a non-integral number of octets (Alignment\n            Error).\n            \n            Note that it is entirely normal for etherStatsFragments to\n            increment.  This is because it counts both runts (which are\n            normal occurrences due to collisions) and noise hits.')
etherStatsJabbers = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 12), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsJabbers.setDescription('The total number of packets received that were\n            longer than 1518 octets (excluding framing bits,\n            but including FCS octets), and had either a bad\n            Frame Check Sequence (FCS) with an integral number\n            of octets (FCS Error) or a bad FCS with a non-integral\n            number of octets (Alignment Error).\n            \n            Note that this definition of jabber is different\n            than the definition in IEEE-802.3 section 8.2.1.5\n            (10BASE5) and section 10.3.1.4 (10BASE2).  These\n            documents define jabber as the condition where any\n            packet exceeds 20 ms.  The allowed range to detect\n            jabber is between 20 ms and 150 ms.')
etherStatsCollisions = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 13), Counter32()).setUnits('Collisions').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsCollisions.setDescription('The best estimate of the total number of collisions\n            on this Ethernet segment.\n            \n            The value returned will depend on the location of the\n            RMON probe. Section 8.2.1.3 (10BASE-5) and section\n            10.3.1.3 (10BASE-2) of IEEE standard 802.3 states that a\n            station must detect a collision, in the receive mode, if\n            three or more stations are transmitting simultaneously.  A\n            repeater port must detect a collision when two or more\n            stations are transmitting simultaneously.  Thus a probe\n            placed on a repeater port could record more collisions\n            than a probe connected to a station on the same segment\n            would.\n            \n            Probe location plays a much smaller role when considering\n            10BASE-T.  14.2.1.4 (10BASE-T) of IEEE standard 802.3\n            defines a collision as the simultaneous presence of signals\n            on the DO and RD circuits (transmitting and receiving\n            at the same time).  A 10BASE-T station can only detect\n            collisions when it is transmitting.  Thus probes placed on\n            a station and a repeater, should report the same number of\n            collisions.\n            \n            Note also that an RMON probe inside a repeater should\n            ideally report collisions between the repeater and one or\n            more other hosts (transmit collisions as defined by IEEE\n            802.3k) plus receiver collisions observed on any coax\n            segments to which the repeater is connected.')
etherStatsPkts64Octets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 14), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts64Octets.setDescription('The total number of packets (including bad\n            packets) received that were 64 octets in length\n            (excluding framing bits but including FCS octets).')
etherStatsPkts65to127Octets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 15), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts65to127Octets.setDescription('The total number of packets (including bad\n            packets) received that were between\n            65 and 127 octets in length inclusive\n            (excluding framing bits but including FCS octets).')
etherStatsPkts128to255Octets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 16), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts128to255Octets.setDescription('The total number of packets (including bad\n            packets) received that were between\n            128 and 255 octets in length inclusive\n            (excluding framing bits but including FCS octets).')
etherStatsPkts256to511Octets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 17), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts256to511Octets.setDescription('The total number of packets (including bad\n            packets) received that were between\n            256 and 511 octets in length inclusive\n            (excluding framing bits but including FCS octets).')
etherStatsPkts512to1023Octets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 18), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts512to1023Octets.setDescription('The total number of packets (including bad\n            packets) received that were between\n            512 and 1023 octets in length inclusive\n            (excluding framing bits but including FCS octets).')
etherStatsPkts1024to1518Octets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 19), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherStatsPkts1024to1518Octets.setDescription('The total number of packets (including bad\n            packets) received that were between\n            1024 and 1518 octets in length inclusive\n            (excluding framing bits but including FCS octets).')
etherStatsOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 20), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    etherStatsOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
etherStatsStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 1, 1, 1, 21), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    etherStatsStatus.setDescription('The status of this etherStats entry.')
historyControlTable = MibTable((1, 3, 6, 1, 2, 1, 16, 2, 1))
if mibBuilder.loadTexts:
    historyControlTable.setDescription('A list of history control entries.')
historyControlEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 2, 1, 1)).setIndexNames((0, 'RMON-MIB', 'historyControlIndex'))
if mibBuilder.loadTexts:
    historyControlEntry.setDescription('A list of parameters that set up a periodic sampling of\n            statistics.  As an example, an instance of the\n            historyControlInterval object might be named\n            historyControlInterval.2')
historyControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    historyControlIndex.setDescription('An index that uniquely identifies an entry in the\n            historyControl table.  Each such entry defines a\n            set of samples at a particular interval for an\n            interface on the device.')
historyControlDataSource = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 2), ObjectIdentifier()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    historyControlDataSource.setDescription('This object identifies the source of the data for\n            which historical data was collected and\n            placed in a media-specific table on behalf of this\n            historyControlEntry.  This source can be any\n            interface on this device.  In order to identify\n            a particular interface, this object shall identify\n            the instance of the ifIndex object, defined\n            in  RFC 2233 [17], for the desired interface.\n            For example, if an entry were to receive data from\n            interface #1, this object would be set to ifIndex.1.\n            \n            The statistics in this group reflect all packets\n            on the local network segment attached to the identified\n            interface.\n            \n            An agent may or may not be able to tell if fundamental\n            changes to the media of the interface have occurred and\n            necessitate an invalidation of this entry.  For example, a\n            hot-pluggable ethernet card could be pulled out and replaced\n            by a token-ring card.  In such a case, if the agent has such\n            knowledge of the change, it is recommended that it\n            invalidate this entry.\n            \n            This object may not be modified if the associated\n            historyControlStatus object is equal to valid(1).')
historyControlBucketsRequested = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)).clone(50)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    historyControlBucketsRequested.setDescription('The requested number of discrete time intervals\n            over which data is to be saved in the part of the\n            media-specific table associated with this\n            historyControlEntry.\n            \n            When this object is created or modified, the probe\n            should set historyControlBucketsGranted as closely to\n            this object as is possible for the particular probe\n            implementation and available resources.')
historyControlBucketsGranted = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    historyControlBucketsGranted.setDescription('The number of discrete sampling intervals\n            over which data shall be saved in the part of\n            the media-specific table associated with this\n            historyControlEntry.\n            When the associated historyControlBucketsRequested\n            object is created or modified, the probe\n            should set this object as closely to the requested\n            value as is possible for the particular\n            probe implementation and available resources.  The\n            probe must not lower this value except as a result\n            of a modification to the associated\n            historyControlBucketsRequested object.\n            \n            There will be times when the actual number of\n            buckets associated with this entry is less than\n            the value of this object.  In this case, at the\n            end of each sampling interval, a new bucket will\n            be added to the media-specific table.\n            \n            When the number of buckets reaches the value of\n            this object and a new bucket is to be added to the\n            media-specific table, the oldest bucket associated\n            with this historyControlEntry shall be deleted by\n            the agent so that the new bucket can be added.\n            \n            When the value of this object changes to a value less\n            than the current value, entries are deleted\n            from the media-specific table associated with this\n            historyControlEntry.  Enough of the oldest of these\n            entries shall be deleted by the agent so that their\n            number remains less than or equal to the new value of\n            this object.\n            \n            When the value of this object changes to a value greater\n            than the current value, the number of associated media-\n            specific entries may be allowed to grow.')
historyControlInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 3600)).clone(1800)).setUnits('Seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    historyControlInterval.setDescription("The interval in seconds over which the data is\n            sampled for each bucket in the part of the\n            media-specific table associated with this\n            historyControlEntry.  This interval can\n            be set to any number of seconds between 1 and\n            3600 (1 hour).\n\n            Because the counters in a bucket may overflow at their\n\n            maximum value with no indication, a prudent manager will\n            take into account the possibility of overflow in any of\n            the associated counters.  It is important to consider the\n            minimum time in which any counter could overflow on a\n            particular media type and set the historyControlInterval\n            object to a value less than this interval.  This is\n            typically most important for the 'octets' counter in any\n            media-specific table.  For example, on an Ethernet\n            network, the etherHistoryOctets counter could overflow\n            in about one hour at the Ethernet's maximum\n            utilization.\n            \n            This object may not be modified if the associated\n            historyControlStatus object is equal to valid(1).")
historyControlOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 6), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    historyControlOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
historyControlStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 1, 1, 7), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    historyControlStatus.setDescription('The status of this historyControl entry.\n            \n            Each instance of the media-specific table associated\n            with this historyControlEntry will be deleted by the agent\n            if this historyControlEntry is not equal to valid(1).')
etherHistoryTable = MibTable((1, 3, 6, 1, 2, 1, 16, 2, 2))
if mibBuilder.loadTexts:
    etherHistoryTable.setDescription('A list of Ethernet history entries.')
etherHistoryEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 2, 2, 1)).setIndexNames((0, 'RMON-MIB', 'etherHistoryIndex'), (0, 'RMON-MIB', 'etherHistorySampleIndex'))
if mibBuilder.loadTexts:
    etherHistoryEntry.setDescription('An historical sample of Ethernet statistics on a particular\n            Ethernet interface.  This sample is associated with the\n            historyControlEntry which set up the parameters for\n            a regular collection of these samples.  As an example, an\n            instance of the etherHistoryPkts object might be named\n            etherHistoryPkts.2.89')
etherHistoryIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryIndex.setDescription('The history of which this entry is a part.  The\n            history identified by a particular value of this\n            index is the same history as identified\n            by the same value of historyControlIndex.')
etherHistorySampleIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistorySampleIndex.setDescription('An index that uniquely identifies the particular\n            sample this entry represents among all samples\n            associated with the same historyControlEntry.\n            This index starts at 1 and increases by one\n            as each new sample is taken.')
etherHistoryIntervalStart = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 3), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryIntervalStart.setDescription('The value of sysUpTime at the start of the interval\n            over which this sample was measured.  If the probe\n            keeps track of the time of day, it should start\n            the first sample of the history at a time such that\n            when the next hour of the day begins, a sample is\n            started at that instant.  Note that following this\n            rule may require the probe to delay collecting the\n            first sample of the history, as each sample must be\n            of the same interval.  Also note that the sample which\n            is currently being collected is not accessible in this\n            table until the end of its interval.')
etherHistoryDropEvents = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryDropEvents.setDescription('The total number of events in which packets\n            were dropped by the probe due to lack of resources\n            during this sampling interval.  Note that this number\n            is not necessarily the number of packets dropped, it\n            is just the number of times this condition has been\n            detected.')
etherHistoryOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 5), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryOctets.setDescription('The total number of octets of data (including\n            those in bad packets) received on the\n            network (excluding framing bits but including\n            FCS octets).')
etherHistoryPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 6), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryPkts.setDescription('The number of packets (including bad packets)\n            received during this sampling interval.')
etherHistoryBroadcastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 7), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryBroadcastPkts.setDescription('The number of good packets received during this\n            sampling interval that were directed to the\n            broadcast address.')
etherHistoryMulticastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 8), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryMulticastPkts.setDescription('The number of good packets received during this\n            sampling interval that were directed to a\n            multicast address.  Note that this number does not\n            include packets addressed to the broadcast address.')
etherHistoryCRCAlignErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 9), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryCRCAlignErrors.setDescription('The number of packets received during this\n            sampling interval that had a length (excluding\n            framing bits but including FCS octets) between\n            64 and 1518 octets, inclusive, but had either a bad Frame\n            Check Sequence (FCS) with an integral number of octets\n            (FCS Error) or a bad FCS with a non-integral number\n            of octets (Alignment Error).')
etherHistoryUndersizePkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 10), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryUndersizePkts.setDescription('The number of packets received during this\n            sampling interval that were less than 64 octets\n            long (excluding framing bits but including FCS\n            octets) and were otherwise well formed.')
etherHistoryOversizePkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 11), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryOversizePkts.setDescription('The number of packets received during this\n            sampling interval that were longer than 1518\n            octets (excluding framing bits but including\n            FCS octets) but were otherwise well formed.')
etherHistoryFragments = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 12), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryFragments.setDescription('The total number of packets received during this\n            sampling interval that were less than 64 octets in\n            length (excluding framing bits but including FCS\n            octets) had either a bad Frame Check Sequence (FCS)\n            with an integral number of octets (FCS Error) or a bad\n            FCS with a non-integral number of octets (Alignment\n            Error).\n            \n            Note that it is entirely normal for etherHistoryFragments to\n            increment.  This is because it counts both runts (which are\n            normal occurrences due to collisions) and noise hits.')
etherHistoryJabbers = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 13), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryJabbers.setDescription('The number of packets received during this\n            sampling interval that were longer than 1518 octets\n            (excluding framing bits but including FCS octets),\n            and  had either a bad Frame Check Sequence (FCS)\n            with an integral number of octets (FCS Error) or\n            a bad FCS with a non-integral number of octets\n            (Alignment Error).\n            \n            Note that this definition of jabber is different\n            than the definition in IEEE-802.3 section 8.2.1.5\n            (10BASE5) and section 10.3.1.4 (10BASE2).  These\n            documents define jabber as the condition where any\n            packet exceeds 20 ms.  The allowed range to detect\n            jabber is between 20 ms and 150 ms.')
etherHistoryCollisions = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 14), Counter32()).setUnits('Collisions').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryCollisions.setDescription('The best estimate of the total number of collisions\n            on this Ethernet segment during this sampling\n            interval.\n            \n            The value returned will depend on the location of the\n            RMON probe. Section 8.2.1.3 (10BASE-5) and section\n            10.3.1.3 (10BASE-2) of IEEE standard 802.3 states that a\n            station must detect a collision, in the receive mode, if\n            three or more stations are transmitting simultaneously.  A\n            repeater port must detect a collision when two or more\n            stations are transmitting simultaneously.  Thus a probe\n            placed on a repeater port could record more collisions\n            than a probe connected to a station on the same segment\n            would.\n            \n            Probe location plays a much smaller role when considering\n            10BASE-T.  14.2.1.4 (10BASE-T) of IEEE standard 802.3\n            defines a collision as the simultaneous presence of signals\n            on the DO and RD circuits (transmitting and receiving\n            at the same time).  A 10BASE-T station can only detect\n            collisions when it is transmitting.  Thus probes placed on\n            a station and a repeater, should report the same number of\n            collisions.\n            \n            Note also that an RMON probe inside a repeater should\n            ideally report collisions between the repeater and one or\n            more other hosts (transmit collisions as defined by IEEE\n            802.3k) plus receiver collisions observed on any coax\n            segments to which the repeater is connected.')
etherHistoryUtilization = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 2, 2, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 10000))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherHistoryUtilization.setDescription('The best estimate of the mean physical layer\n            network utilization on this interface during this\n            sampling interval, in hundredths of a percent.')
alarmTable = MibTable((1, 3, 6, 1, 2, 1, 16, 3, 1))
if mibBuilder.loadTexts:
    alarmTable.setDescription('A list of alarm entries.')
alarmEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 3, 1, 1)).setIndexNames((0, 'RMON-MIB', 'alarmIndex'))
if mibBuilder.loadTexts:
    alarmEntry.setDescription('A list of parameters that set up a periodic checking\n            for alarm conditions.  For example, an instance of the\n            alarmValue object might be named alarmValue.8')
alarmIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    alarmIndex.setDescription('An index that uniquely identifies an entry in the\n            alarm table.  Each such entry defines a\n            diagnostic sample at a particular interval\n            for an object on the device.')
alarmInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 2), Integer32()).setUnits('Seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmInterval.setDescription('The interval in seconds over which the data is\n            sampled and compared with the rising and falling\n            thresholds.  When setting this variable, care\n            should be taken in the case of deltaValue\n            sampling - the interval should be set short enough\n            that the sampled variable is very unlikely to\n            increase or decrease by more than 2^31 - 1 during\n            a single sampling interval.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmVariable = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 3), ObjectIdentifier()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmVariable.setDescription('The object identifier of the particular variable to be\n            sampled.  Only variables that resolve to an ASN.1 primitive\n            type of INTEGER (INTEGER, Integer32, Counter32, Counter64,\n            Gauge, or TimeTicks) may be sampled.\n            \n            Because SNMP access control is articulated entirely\n            in terms of the contents of MIB views, no access\n            control mechanism exists that can restrict the value of\n            this object to identify only those objects that exist\n            in a particular MIB view.  Because there is thus no\n            acceptable means of restricting the read access that\n            could be obtained through the alarm mechanism, the\n            probe must only grant write access to this object in\n            those views that have read access to all objects on\n            the probe.\n            \n            During a set operation, if the supplied variable name is\n            not available in the selected MIB view, a badValue error\n            must be returned.  If at any time the variable name of\n            an established alarmEntry is no longer available in the\n            selected MIB view, the probe must change the status of\n            this alarmEntry to invalid(4).\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmSampleType = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('absoluteValue', 1), ('deltaValue', 2)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmSampleType.setDescription('The method of sampling the selected variable and\n            calculating the value to be compared against the\n            thresholds.  If the value of this object is\n            absoluteValue(1), the value of the selected variable\n            will be compared directly with the thresholds at the\n            end of the sampling interval.  If the value of this\n            object is deltaValue(2), the value of the selected\n            variable at the last sample will be subtracted from\n            the current value, and the difference compared with\n            the thresholds.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmValue = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    alarmValue.setDescription('The value of the statistic during the last sampling\n            period.  For example, if the sample type is deltaValue,\n            this value will be the difference between the samples\n            at the beginning and end of the period.  If the sample\n            type is absoluteValue, this value will be the sampled\n            value at the end of the period.\n            This is the value that is compared with the rising and\n            falling thresholds.\n            \n            The value during the current sampling period is not\n            made available until the period is completed and will\n            remain available until the next period completes.')
alarmStartupAlarm = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('risingAlarm', 1), ('fallingAlarm', 2), ('risingOrFallingAlarm', 3)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmStartupAlarm.setDescription('The alarm that may be sent when this entry is first\n            set to valid.  If the first sample after this entry\n            becomes valid is greater than or equal to the\n            risingThreshold and alarmStartupAlarm is equal to\n            risingAlarm(1) or risingOrFallingAlarm(3), then a single\n            rising alarm will be generated.  If the first sample\n            after this entry becomes valid is less than or equal\n            to the fallingThreshold and alarmStartupAlarm is equal\n            to fallingAlarm(2) or risingOrFallingAlarm(3), then a\n            single falling alarm will be generated.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmRisingThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 7), Integer32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmRisingThreshold.setDescription('A threshold for the sampled statistic.  When the current\n            sampled value is greater than or equal to this threshold,\n            and the value at the last sampling interval was less than\n            this threshold, a single event will be generated.\n            A single event will also be generated if the first\n            sample after this entry becomes valid is greater than or\n            equal to this threshold and the associated\n            alarmStartupAlarm is equal to risingAlarm(1) or\n            risingOrFallingAlarm(3).\n            \n            After a rising event is generated, another such event\n            will not be generated until the sampled value\n            falls below this threshold and reaches the\n            alarmFallingThreshold.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmFallingThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 8), Integer32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmFallingThreshold.setDescription('A threshold for the sampled statistic.  When the current\n            sampled value is less than or equal to this threshold,\n            and the value at the last sampling interval was greater than\n            this threshold, a single event will be generated.\n            A single event will also be generated if the first\n            sample after this entry becomes valid is less than or\n            equal to this threshold and the associated\n            alarmStartupAlarm is equal to fallingAlarm(2) or\n            risingOrFallingAlarm(3).\n            \n            After a falling event is generated, another such event\n            will not be generated until the sampled value\n            rises above this threshold and reaches the\n            alarmRisingThreshold.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmRisingEventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmRisingEventIndex.setDescription('The index of the eventEntry that is\n            used when a rising threshold is crossed.  The\n            eventEntry identified by a particular value of\n            this index is the same as identified by the same value\n            of the eventIndex object.  If there is no\n            corresponding entry in the eventTable, then\n            no association exists.  In particular, if this value\n            is zero, no associated event will be generated, as\n            zero is not a valid event index.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmFallingEventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmFallingEventIndex.setDescription('The index of the eventEntry that is\n            used when a falling threshold is crossed.  The\n            eventEntry identified by a particular value of\n            this index is the same as identified by the same value\n            of the eventIndex object.  If there is no\n            corresponding entry in the eventTable, then\n            no association exists.  In particular, if this value\n            is zero, no associated event will be generated, as\n            zero is not a valid event index.\n            \n            This object may not be modified if the associated\n            alarmStatus object is equal to valid(1).')
alarmOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 11), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
alarmStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 3, 1, 1, 12), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    alarmStatus.setDescription('The status of this alarm entry.')
hostControlTable = MibTable((1, 3, 6, 1, 2, 1, 16, 4, 1))
if mibBuilder.loadTexts:
    hostControlTable.setDescription('A list of host table control entries.')
hostControlEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 4, 1, 1)).setIndexNames((0, 'RMON-MIB', 'hostControlIndex'))
if mibBuilder.loadTexts:
    hostControlEntry.setDescription('A list of parameters that set up the discovery of hosts\n            on a particular interface and the collection of statistics\n            about these hosts.  For example, an instance of the\n            hostControlTableSize object might be named\n            hostControlTableSize.1')
hostControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostControlIndex.setDescription('An index that uniquely identifies an entry in the\n            hostControl table.  Each such entry defines\n            a function that discovers hosts on a particular interface\n            and places statistics about them in the hostTable and\n            the hostTimeTable on behalf of this hostControlEntry.')
hostControlDataSource = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 1, 1, 2), ObjectIdentifier()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostControlDataSource.setDescription('This object identifies the source of the data for\n            this instance of the host function.  This source\n            can be any interface on this device.  In order\n            to identify a particular interface, this object shall\n            identify the instance of the ifIndex object, defined\n            in RFC 2233 [17], for the desired interface.\n            For example, if an entry were to receive data from\n            interface #1, this object would be set to ifIndex.1.\n    \n            The statistics in this group reflect all packets\n            on the local network segment attached to the identified\n            interface.\n    \n            An agent may or may not be able to tell if fundamental\n            changes to the media of the interface have occurred and\n            necessitate an invalidation of this entry.  For example, a\n            hot-pluggable ethernet card could be pulled out and replaced\n            by a token-ring card.  In such a case, if the agent has such\n            knowledge of the change, it is recommended that it\n            invalidate this entry.\n    \n            This object may not be modified if the associated\n            hostControlStatus object is equal to valid(1).')
hostControlTableSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 1, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostControlTableSize.setDescription('The number of hostEntries in the hostTable and the\n            hostTimeTable associated with this hostControlEntry.')
hostControlLastDeleteTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 1, 1, 4), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostControlLastDeleteTime.setDescription('The value of sysUpTime when the last entry\n            was deleted from the portion of the hostTable\n            associated with this hostControlEntry.  If no\n            deletions have occurred, this value shall be zero.')
hostControlOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 1, 1, 5), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostControlOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
hostControlStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 1, 1, 6), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostControlStatus.setDescription('The status of this hostControl entry.\n    \n            If this object is not equal to valid(1), all associated\n            entries in the hostTable, hostTimeTable, and the\n            hostTopNTable shall be deleted by the agent.')
hostTable = MibTable((1, 3, 6, 1, 2, 1, 16, 4, 2))
if mibBuilder.loadTexts:
    hostTable.setDescription('A list of host entries.')
hostEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 4, 2, 1)).setIndexNames((0, 'RMON-MIB', 'hostIndex'), (0, 'RMON-MIB', 'hostAddress'))
if mibBuilder.loadTexts:
    hostEntry.setDescription('A collection of statistics for a particular host that has\n            been discovered on an interface of this device.  For example,\n            an instance of the hostOutBroadcastPkts object might be\n            named hostOutBroadcastPkts.1.6.8.0.32.27.3.176')
hostAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 1), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostAddress.setDescription('The physical address of this host.')
hostCreationOrder = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostCreationOrder.setDescription("An index that defines the relative ordering of\n            the creation time of hosts captured for a\n            particular hostControlEntry.  This index shall\n            be between 1 and N, where N is the value of\n            the associated hostControlTableSize.  The ordering\n            of the indexes is based on the order of each entry's\n            insertion into the table, in which entries added earlier\n            have a lower index value than entries added later.\n    \n            It is important to note that the order for a\n            particular entry may change as an (earlier) entry\n            is deleted from the table.  Because this order may\n            change, management stations should make use of the\n            hostControlLastDeleteTime variable in the\n            hostControlEntry associated with the relevant\n            portion of the hostTable.  By observing\n            this variable, the management station may detect\n            the circumstances where a previous association\n            between a value of hostCreationOrder\n            and a hostEntry may no longer hold.")
hostIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostIndex.setDescription('The set of collected host statistics of which\n            this entry is a part.  The set of hosts\n            identified by a particular value of this\n            index is associated with the hostControlEntry\n            as identified by the same value of hostControlIndex.')
hostInPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 4), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostInPkts.setDescription('The number of good packets transmitted to this\n            address since it was added to the hostTable.')
hostOutPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 5), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostOutPkts.setDescription('The number of packets, including bad packets, transmitted\n            by this address since it was added to the hostTable.')
hostInOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 6), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostInOctets.setDescription('The number of octets transmitted to this address since\n            it was added to the hostTable (excluding framing\n            bits but including FCS octets), except for those\n            octets in bad packets.')
hostOutOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 7), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostOutOctets.setDescription('The number of octets transmitted by this address since\n            it was added to the hostTable (excluding framing\n            bits but including FCS octets), including those\n            octets in bad packets.')
hostOutErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 8), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostOutErrors.setDescription('The number of bad packets transmitted by this address\n            since this host was added to the hostTable.')
hostOutBroadcastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 9), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostOutBroadcastPkts.setDescription('The number of good packets transmitted by this\n            address that were directed to the broadcast address\n            since this host was added to the hostTable.')
hostOutMulticastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 2, 1, 10), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostOutMulticastPkts.setDescription('The number of good packets transmitted by this\n            address that were directed to a multicast address\n            since this host was added to the hostTable.\n            Note that this number does not include packets\n            directed to the broadcast address.')
hostTimeTable = MibTable((1, 3, 6, 1, 2, 1, 16, 4, 3))
if mibBuilder.loadTexts:
    hostTimeTable.setDescription('A list of time-ordered host table entries.')
hostTimeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 4, 3, 1)).setIndexNames((0, 'RMON-MIB', 'hostTimeIndex'), (0, 'RMON-MIB', 'hostTimeCreationOrder'))
if mibBuilder.loadTexts:
    hostTimeEntry.setDescription('A collection of statistics for a particular host that has\n            been discovered on an interface of this device.  This\n            collection includes the relative ordering of the creation\n            time of this object.  For example, an instance of the\n            hostTimeOutBroadcastPkts object might be named\n            hostTimeOutBroadcastPkts.1.687')
hostTimeAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 1), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeAddress.setDescription('The physical address of this host.')
hostTimeCreationOrder = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeCreationOrder.setDescription("An index that uniquely identifies an entry in\n            the hostTime table among those entries associated\n            with the same hostControlEntry.  This index shall\n            be between 1 and N, where N is the value of\n            the associated hostControlTableSize.  The ordering\n            of the indexes is based on the order of each entry's\n            insertion into the table, in which entries added earlier\n            have a lower index value than entries added later.\n            Thus the management station has the ability to\n            learn of new entries added to this table without\n            downloading the entire table.\n    \n            It is important to note that the index for a\n            particular entry may change as an (earlier) entry\n            is deleted from the table.  Because this order may\n            change, management stations should make use of the\n            hostControlLastDeleteTime variable in the\n            hostControlEntry associated with the relevant\n            portion of the hostTimeTable.  By observing\n            this variable, the management station may detect\n            the circumstances where a download of the table\n            may have missed entries, and where a previous\n            association between a value of hostTimeCreationOrder\n            and a hostTimeEntry may no longer hold.")
hostTimeIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeIndex.setDescription('The set of collected host statistics of which\n            this entry is a part.  The set of hosts\n            identified by a particular value of this\n            index is associated with the hostControlEntry\n            as identified by the same value of hostControlIndex.')
hostTimeInPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 4), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeInPkts.setDescription('The number of good packets transmitted to this\n            address since it was added to the hostTimeTable.')
hostTimeOutPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 5), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeOutPkts.setDescription('The number of packets, including bad packets, transmitted\n            by this address since it was added to the hostTimeTable.')
hostTimeInOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 6), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeInOctets.setDescription('The number of octets transmitted to this address since\n            it was added to the hostTimeTable (excluding framing\n            bits but including FCS octets), except for those\n            octets in bad packets.')
hostTimeOutOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 7), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeOutOctets.setDescription('The number of octets transmitted by this address since\n            it was added to the hostTimeTable (excluding framing\n            bits but including FCS octets), including those\n            octets in bad packets.')
hostTimeOutErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 8), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeOutErrors.setDescription('The number of bad packets transmitted by this address\n            since this host was added to the hostTimeTable.')
hostTimeOutBroadcastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 9), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeOutBroadcastPkts.setDescription('The number of good packets transmitted by this\n            address that were directed to the broadcast address\n            since this host was added to the hostTimeTable.')
hostTimeOutMulticastPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 4, 3, 1, 10), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTimeOutMulticastPkts.setDescription('The number of good packets transmitted by this\n            address that were directed to a multicast address\n            since this host was added to the hostTimeTable.\n            Note that this number does not include packets directed\n            to the broadcast address.')
hostTopNControlTable = MibTable((1, 3, 6, 1, 2, 1, 16, 5, 1))
if mibBuilder.loadTexts:
    hostTopNControlTable.setDescription('A list of top N host control entries.')
hostTopNControlEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 5, 1, 1)).setIndexNames((0, 'RMON-MIB', 'hostTopNControlIndex'))
if mibBuilder.loadTexts:
    hostTopNControlEntry.setDescription('A set of parameters that control the creation of a report\n            of the top N hosts according to several metrics.  For\n            example, an instance of the hostTopNDuration object might\n            be named hostTopNDuration.3')
hostTopNControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNControlIndex.setDescription('An index that uniquely identifies an entry\n            in the hostTopNControl table.  Each such\n            entry defines one top N report prepared for\n            one interface.')
hostTopNHostIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostTopNHostIndex.setDescription('The host table for which a top N report will be prepared\n            on behalf of this entry.  The host table identified by a\n            particular value of this index is associated with the same\n            host table as identified by the same value of\n            hostIndex.\n    \n            This object may not be modified if the associated\n            hostTopNStatus object is equal to valid(1).')
hostTopNRateBase = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))).clone(namedValues=NamedValues(('hostTopNInPkts', 1), ('hostTopNOutPkts', 2), ('hostTopNInOctets', 3), ('hostTopNOutOctets', 4), ('hostTopNOutErrors', 5), ('hostTopNOutBroadcastPkts', 6), ('hostTopNOutMulticastPkts', 7)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostTopNRateBase.setDescription('The variable for each host that the hostTopNRate\n            variable is based upon.\n    \n            This object may not be modified if the associated\n            hostTopNStatus object is equal to valid(1).')
hostTopNTimeRemaining = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 4), Integer32()).setUnits('Seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostTopNTimeRemaining.setDescription('The number of seconds left in the report currently being\n            collected.  When this object is modified by the management\n            station, a new collection is started, possibly aborting\n            a currently running report.  The new value is used\n            as the requested duration of this report, which is\n            loaded into the associated hostTopNDuration object.\n    \n            When this object is set to a non-zero value, any\n            associated hostTopNEntries shall be made\n            inaccessible by the monitor.  While the value of this\n            object is non-zero, it decrements by one per second until\n            it reaches zero.  During this time, all associated\n            hostTopNEntries shall remain inaccessible.  At the time\n            that this object decrements to zero, the report is made\n            accessible in the hostTopNTable.  Thus, the hostTopN\n            table needs to be created only at the end of the collection\n            interval.')
hostTopNDuration = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 5), Integer32()).setUnits('Seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNDuration.setDescription('The number of seconds that this report has collected\n            during the last sampling interval, or if this\n            report is currently being collected, the number\n            of seconds that this report is being collected\n            during this sampling interval.\n    \n            When the associated hostTopNTimeRemaining object is set,\n            this object shall be set by the probe to the same value\n            and shall not be modified until the next time\n            the hostTopNTimeRemaining is set.\n    \n            This value shall be zero if no reports have been\n            requested for this hostTopNControlEntry.')
hostTopNRequestedSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 6), Integer32().clone(10)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostTopNRequestedSize.setDescription('The maximum number of hosts requested for the top N\n            table.\n    \n            When this object is created or modified, the probe\n            should set hostTopNGrantedSize as closely to this\n            object as is possible for the particular probe\n            implementation and available resources.')
hostTopNGrantedSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNGrantedSize.setDescription('The maximum number of hosts in the top N table.\n    \n            When the associated hostTopNRequestedSize object is\n            created or modified, the probe should set this\n            object as closely to the requested value as is possible\n            for the particular implementation and available\n            resources. The probe must not lower this value except\n            as a result of a set to the associated\n            hostTopNRequestedSize object.\n    \n            Hosts with the highest value of hostTopNRate shall be\n            placed in this table in decreasing order of this rate\n            until there is no more room or until there are no more\n            hosts.')
hostTopNStartTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 8), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNStartTime.setDescription('The value of sysUpTime when this top N report was\n            last started.  In other words, this is the time that\n            the associated hostTopNTimeRemaining object was\n            modified to start the requested report.')
hostTopNOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 9), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostTopNOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
hostTopNStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 1, 1, 10), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hostTopNStatus.setDescription('The status of this hostTopNControl entry.\n    \n            If this object is not equal to valid(1), all associated\n            hostTopNEntries shall be deleted by the agent.')
hostTopNTable = MibTable((1, 3, 6, 1, 2, 1, 16, 5, 2))
if mibBuilder.loadTexts:
    hostTopNTable.setDescription('A list of top N host entries.')
hostTopNEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 5, 2, 1)).setIndexNames((0, 'RMON-MIB', 'hostTopNReport'), (0, 'RMON-MIB', 'hostTopNIndex'))
if mibBuilder.loadTexts:
    hostTopNEntry.setDescription('A set of statistics for a host that is part of a top N\n            report.  For example, an instance of the hostTopNRate\n            object might be named hostTopNRate.3.10')
hostTopNReport = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNReport.setDescription('This object identifies the top N report of which\n            this entry is a part.  The set of hosts\n            identified by a particular value of this\n            object is part of the same report as identified\n            by the same value of the hostTopNControlIndex object.')
hostTopNIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNIndex.setDescription('An index that uniquely identifies an entry in\n            the hostTopN table among those in the same report.\n            This index is between 1 and N, where N is the\n            number of entries in this table.  Increasing values\n            of hostTopNIndex shall be assigned to entries with\n            decreasing values of hostTopNRate until index N\n            is assigned to the entry with the lowest value of\n            hostTopNRate or there are no more hostTopNEntries.')
hostTopNAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 2, 1, 3), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNAddress.setDescription('The physical address of this host.')
hostTopNRate = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 5, 2, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hostTopNRate.setDescription("The amount of change in the selected variable\n            during this sampling interval.  The selected\n            variable is this host's instance of the object\n            selected by hostTopNRateBase.")
matrixControlTable = MibTable((1, 3, 6, 1, 2, 1, 16, 6, 1))
if mibBuilder.loadTexts:
    matrixControlTable.setDescription('A list of information entries for the\n            traffic matrix on each interface.')
matrixControlEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 6, 1, 1)).setIndexNames((0, 'RMON-MIB', 'matrixControlIndex'))
if mibBuilder.loadTexts:
    matrixControlEntry.setDescription('Information about a traffic matrix on a particular\n            interface.  For example, an instance of the\n            matrixControlLastDeleteTime object might be named\n            matrixControlLastDeleteTime.1')
matrixControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixControlIndex.setDescription('An index that uniquely identifies an entry in the\n            matrixControl table.  Each such entry defines\n            a function that discovers conversations on a particular\n            interface and places statistics about them in the\n            matrixSDTable and the matrixDSTable on behalf of this\n            matrixControlEntry.')
matrixControlDataSource = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 1, 1, 2), ObjectIdentifier()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    matrixControlDataSource.setDescription('This object identifies the source of\n            the data from which this entry creates a traffic matrix.\n            This source can be any interface on this device.  In\n            order to identify a particular interface, this object\n            shall identify the instance of the ifIndex object,\n            defined in RFC 2233 [17], for the desired\n            interface.  For example, if an entry were to receive data\n            from interface #1, this object would be set to ifIndex.1.\n    \n            The statistics in this group reflect all packets\n            on the local network segment attached to the identified\n            interface.\n    \n            An agent may or may not be able to tell if fundamental\n            changes to the media of the interface have occurred and\n            necessitate an invalidation of this entry.  For example, a\n            hot-pluggable ethernet card could be pulled out and replaced\n            by a token-ring card.  In such a case, if the agent has such\n            knowledge of the change, it is recommended that it\n            invalidate this entry.\n    \n            This object may not be modified if the associated\n            matrixControlStatus object is equal to valid(1).')
matrixControlTableSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 1, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixControlTableSize.setDescription('The number of matrixSDEntries in the matrixSDTable\n            for this interface.  This must also be the value of\n            the number of entries in the matrixDSTable for this\n            interface.')
matrixControlLastDeleteTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 1, 1, 4), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixControlLastDeleteTime.setDescription('The value of sysUpTime when the last entry\n            was deleted from the portion of the matrixSDTable\n            or matrixDSTable associated with this matrixControlEntry.\n            If no deletions have occurred, this value shall be\n            zero.')
matrixControlOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 1, 1, 5), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    matrixControlOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
matrixControlStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 1, 1, 6), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    matrixControlStatus.setDescription('The status of this matrixControl entry.\n            If this object is not equal to valid(1), all associated\n            entries in the matrixSDTable and the matrixDSTable\n            shall be deleted by the agent.')
matrixSDTable = MibTable((1, 3, 6, 1, 2, 1, 16, 6, 2))
if mibBuilder.loadTexts:
    matrixSDTable.setDescription('A list of traffic matrix entries indexed by\n            source and destination MAC address.')
matrixSDEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 6, 2, 1)).setIndexNames((0, 'RMON-MIB', 'matrixSDIndex'), (0, 'RMON-MIB', 'matrixSDSourceAddress'), (0, 'RMON-MIB', 'matrixSDDestAddress'))
if mibBuilder.loadTexts:
    matrixSDEntry.setDescription('A collection of statistics for communications between\n            two addresses on a particular interface.  For example,\n            an instance of the matrixSDPkts object might be named\n            matrixSDPkts.1.6.8.0.32.27.3.176.6.8.0.32.10.8.113')
matrixSDSourceAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 2, 1, 1), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixSDSourceAddress.setDescription('The source physical address.')
matrixSDDestAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 2, 1, 2), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixSDDestAddress.setDescription('The destination physical address.')
matrixSDIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 2, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixSDIndex.setDescription('The set of collected matrix statistics of which\n            this entry is a part.  The set of matrix statistics\n            identified by a particular value of this index\n            is associated with the same matrixControlEntry\n            as identified by the same value of matrixControlIndex.')
matrixSDPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 2, 1, 4), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixSDPkts.setDescription('The number of packets transmitted from the source\n            address to the destination address (this number includes\n            bad packets).')
matrixSDOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 2, 1, 5), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixSDOctets.setDescription('The number of octets (excluding framing bits but\n            including FCS octets) contained in all packets\n            transmitted from the source address to the\n            destination address.')
matrixSDErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 2, 1, 6), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixSDErrors.setDescription('The number of bad packets transmitted from\n            the source address to the destination address.')
matrixDSTable = MibTable((1, 3, 6, 1, 2, 1, 16, 6, 3))
if mibBuilder.loadTexts:
    matrixDSTable.setDescription('A list of traffic matrix entries indexed by\n            destination and source MAC address.')
matrixDSEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 6, 3, 1)).setIndexNames((0, 'RMON-MIB', 'matrixDSIndex'), (0, 'RMON-MIB', 'matrixDSDestAddress'), (0, 'RMON-MIB', 'matrixDSSourceAddress'))
if mibBuilder.loadTexts:
    matrixDSEntry.setDescription('A collection of statistics for communications between\n            two addresses on a particular interface.  For example,\n            an instance of the matrixSDPkts object might be named\n            matrixSDPkts.1.6.8.0.32.10.8.113.6.8.0.32.27.3.176')
matrixDSSourceAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 3, 1, 1), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixDSSourceAddress.setDescription('The source physical address.')
matrixDSDestAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 3, 1, 2), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixDSDestAddress.setDescription('The destination physical address.')
matrixDSIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 3, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixDSIndex.setDescription('The set of collected matrix statistics of which\n            this entry is a part.  The set of matrix statistics\n            identified by a particular value of this index\n            is associated with the same matrixControlEntry\n            as identified by the same value of matrixControlIndex.')
matrixDSPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 3, 1, 4), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixDSPkts.setDescription('The number of packets transmitted from the source\n            address to the destination address (this number includes\n            bad packets).')
matrixDSOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 3, 1, 5), Counter32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixDSOctets.setDescription('The number of octets (excluding framing bits\n            but including FCS octets) contained in all packets\n            transmitted from the source address to the\n            destination address.')
matrixDSErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 6, 3, 1, 6), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    matrixDSErrors.setDescription('The number of bad packets transmitted from\n            the source address to the destination address.')
filterTable = MibTable((1, 3, 6, 1, 2, 1, 16, 7, 1))
if mibBuilder.loadTexts:
    filterTable.setDescription('A list of packet filter entries.')
filterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 7, 1, 1)).setIndexNames((0, 'RMON-MIB', 'filterIndex'))
if mibBuilder.loadTexts:
    filterEntry.setDescription('A set of parameters for a packet filter applied on a\n            particular interface.  As an example, an instance of the\n            filterPktData object might be named filterPktData.12')
filterIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    filterIndex.setDescription('An index that uniquely identifies an entry\n            in the filter table.  Each such entry defines\n            one filter that is to be applied to every packet\n            received on an interface.')
filterChannelIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterChannelIndex.setDescription('This object identifies the channel of which this filter\n            is a part.  The filters identified by a particular value\n            of this object are associated with the same channel as\n            identified by the same value of the channelIndex object.')
filterPktDataOffset = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 3), Integer32()).setUnits('Octets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktDataOffset.setDescription('The offset from the beginning of each packet where\n            a match of packet data will be attempted.  This offset\n            is measured from the point in the physical layer\n            packet after the framing bits, if any.  For example,\n            in an Ethernet frame, this point is at the beginning of\n            the destination MAC address.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).')
filterPktData = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 4), OctetString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktData.setDescription('The data that is to be matched with the input packet.\n            For each packet received, this filter and the accompanying\n            filterPktDataMask and filterPktDataNotMask will be\n            adjusted for the offset.  The only bits relevant to this\n            match algorithm are those that have the corresponding\n            filterPktDataMask bit equal to one.  The following three\n            rules are then applied to every packet:\n    \n            (1) If the packet is too short and does not have data\n                corresponding to part of the filterPktData, the packet\n                will fail this data match.\n    \n            (2) For each relevant bit from the packet with the\n                corresponding filterPktDataNotMask bit set to zero, if\n                the bit from the packet is not equal to the corresponding\n                bit from the filterPktData, then the packet will fail\n                this data match.\n    \n            (3) If for every relevant bit from the packet with the\n                corresponding filterPktDataNotMask bit set to one, the\n                bit from the packet is equal to the corresponding bit\n                from the filterPktData, then the packet will fail this\n                data match.\n    \n            Any packets that have not failed any of the three matches\n            above have passed this data match.  In particular, a zero\n            length filter will match any packet.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).')
filterPktDataMask = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 5), OctetString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktDataMask.setDescription("The mask that is applied to the match process.\n            After adjusting this mask for the offset, only those\n            bits in the received packet that correspond to bits set\n            in this mask are relevant for further processing by the\n            match algorithm.  The offset is applied to filterPktDataMask\n            in the same way it is applied to the filter.  For the\n            purposes of the matching algorithm, if the associated\n            filterPktData object is longer than this mask, this mask is\n            conceptually extended with '1' bits until it reaches the\n            length of the filterPktData object.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).")
filterPktDataNotMask = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 6), OctetString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktDataNotMask.setDescription("The inversion mask that is applied to the match\n            process.  After adjusting this mask for the offset,\n            those relevant bits in the received packet that correspond\n            to bits cleared in this mask must all be equal to their\n            corresponding bits in the filterPktData object for the packet\n            to be accepted.  In addition, at least one of those relevant\n            bits in the received packet that correspond to bits set in\n            this mask must be different to its corresponding bit in the\n            filterPktData object.\n    \n            For the purposes of the matching algorithm, if the associated\n            filterPktData object is longer than this mask, this mask is\n            conceptually extended with '0' bits until it reaches the\n            length of the filterPktData object.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).")
filterPktStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 7), Integer32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktStatus.setDescription("The status that is to be matched with the input packet.\n            The only bits relevant to this match algorithm are those that\n            have the corresponding filterPktStatusMask bit equal to one.\n            The following two rules are then applied to every packet:\n    \n            (1) For each relevant bit from the packet status with the\n                corresponding filterPktStatusNotMask bit set to zero, if\n                the bit from the packet status is not equal to the\n                corresponding bit from the filterPktStatus, then the\n                packet will fail this status match.\n    \n            (2) If for every relevant bit from the packet status with the\n                corresponding filterPktStatusNotMask bit set to one, the\n                bit from the packet status is equal to the corresponding\n                bit from the filterPktStatus, then the packet will fail\n                this status match.\n    \n            Any packets that have not failed either of the two matches\n            above have passed this status match.  In particular, a zero\n            length status filter will match any packet's status.\n    \n            The value of the packet status is a sum.  This sum\n            initially takes the value zero.  Then, for each\n            error, E, that has been discovered in this packet,\n            2 raised to a value representing E is added to the sum.\n            The errors and the bits that represent them are dependent\n            on the media type of the interface that this channel\n            is receiving packets from.\n    \n            The errors defined for a packet captured off of an\n            Ethernet interface are as follows:\n    \n                bit #    Error\n                    0    Packet is longer than 1518 octets\n                    1    Packet is shorter than 64 octets\n                    2    Packet experienced a CRC or Alignment error\n    \n            For example, an Ethernet fragment would have a\n            value of 6 (2^1 + 2^2).\n    \n            As this MIB is expanded to new media types, this object\n            will have other media-specific errors defined.\n    \n            For the purposes of this status matching algorithm, if the\n            packet status is longer than this filterPktStatus object,\n            this object is conceptually extended with '0' bits until it\n            reaches the size of the packet status.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).")
filterPktStatusMask = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 8), Integer32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktStatusMask.setDescription("The mask that is applied to the status match process.\n            Only those bits in the received packet that correspond to\n            bits set in this mask are relevant for further processing\n            by the status match algorithm.  For the purposes\n            of the matching algorithm, if the associated filterPktStatus\n            object is longer than this mask, this mask is conceptually\n            extended with '1' bits until it reaches the size of the\n            filterPktStatus.  In addition, if a packet status is longer\n            than this mask, this mask is conceptually extended with '0'\n            bits until it reaches the size of the packet status.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).")
filterPktStatusNotMask = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 9), Integer32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterPktStatusNotMask.setDescription("The inversion mask that is applied to the status match\n            process.  Those relevant bits in the received packet status\n            that correspond to bits cleared in this mask must all be\n            equal to their corresponding bits in the filterPktStatus\n            object for the packet to be accepted.  In addition, at least\n            one of those relevant bits in the received packet status\n            that correspond to bits set in this mask must be different\n            to its corresponding bit in the filterPktStatus object for\n            the packet to be accepted.\n    \n            For the purposes of the matching algorithm, if the associated\n            filterPktStatus object or a packet status is longer than this\n            mask, this mask is conceptually extended with '0' bits until\n            it reaches the longer of the lengths of the filterPktStatus\n            object and the packet status.\n    \n            This object may not be modified if the associated\n            filterStatus object is equal to valid(1).")
filterOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 10), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
filterStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 1, 1, 11), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    filterStatus.setDescription('The status of this filter entry.')
channelTable = MibTable((1, 3, 6, 1, 2, 1, 16, 7, 2))
if mibBuilder.loadTexts:
    channelTable.setDescription('A list of packet channel entries.')
channelEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 7, 2, 1)).setIndexNames((0, 'RMON-MIB', 'channelIndex'))
if mibBuilder.loadTexts:
    channelEntry.setDescription('A set of parameters for a packet channel applied on a\n            particular interface.  As an example, an instance of the\n            channelMatches object might be named channelMatches.3')
channelIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    channelIndex.setDescription('An index that uniquely identifies an entry in the channel\n            table.  Each such entry defines one channel, a logical\n            data and event stream.\n    \n            It is suggested that before creating a channel, an\n            application should scan all instances of the\n            filterChannelIndex object to make sure that there are no\n            pre-existing filters that would be inadvertently be linked\n            to the channel.')
channelIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelIfIndex.setDescription('The value of this object uniquely identifies the\n            interface on this remote network monitoring device to which\n            the associated filters are applied to allow data into this\n            channel.  The interface identified by a particular value\n            of this object is the same interface as identified by the\n            same value of the ifIndex object, defined in RFC 2233 [17].\n    \n            The filters in this group are applied to all packets on\n            the local network segment attached to the identified\n            interface.\n    \n            An agent may or may not be able to tell if fundamental\n            changes to the media of the interface have occurred and\n            necessitate an invalidation of this entry.  For example, a\n            hot-pluggable ethernet card could be pulled out and replaced\n            by a token-ring card.  In such a case, if the agent has such\n            knowledge of the change, it is recommended that it\n            invalidate this entry.\n    \n            This object may not be modified if the associated\n            channelStatus object is equal to valid(1).')
channelAcceptType = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('acceptMatched', 1), ('acceptFailed', 2)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelAcceptType.setDescription('This object controls the action of the filters\n            associated with this channel.  If this object is equal\n            to acceptMatched(1), packets will be accepted to this\n            channel if they are accepted by both the packet data and\n            packet status matches of an associated filter.  If\n            this object is equal to acceptFailed(2), packets will\n            be accepted to this channel only if they fail either\n            the packet data match or the packet status match of\n            each of the associated filters.\n    \n            In particular, a channel with no associated filters will\n            match no packets if set to acceptMatched(1) case and will\n            match all packets in the acceptFailed(2) case.\n    \n            This object may not be modified if the associated\n            channelStatus object is equal to valid(1).')
channelDataControl = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('on', 1), ('off', 2))).clone('off')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelDataControl.setDescription('This object controls the flow of data through this channel.\n            If this object is on(1), data, status and events flow\n            through this channel.  If this object is off(2), data,\n            status and events will not flow through this channel.')
channelTurnOnEventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelTurnOnEventIndex.setDescription('The value of this object identifies the event\n            that is configured to turn the associated\n            channelDataControl from off to on when the event is\n            generated.  The event identified by a particular value\n            of this object is the same event as identified by the\n            same value of the eventIndex object.  If there is no\n            corresponding entry in the eventTable, then no\n            association exists.  In fact, if no event is intended\n            for this channel, channelTurnOnEventIndex must be\n            set to zero, a non-existent event index.\n            This object may not be modified if the associated\n            channelStatus object is equal to valid(1).')
channelTurnOffEventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelTurnOffEventIndex.setDescription('The value of this object identifies the event\n            that is configured to turn the associated\n            channelDataControl from on to off when the event is\n            generated.  The event identified by a particular value\n            of this object is the same event as identified by the\n            same value of the eventIndex object.  If there is no\n            corresponding entry in the eventTable, then no\n            association exists.  In fact, if no event is intended\n            for this channel, channelTurnOffEventIndex must be\n            set to zero, a non-existent event index.\n    \n            This object may not be modified if the associated\n            channelStatus object is equal to valid(1).')
channelEventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelEventIndex.setDescription('The value of this object identifies the event\n            that is configured to be generated when the\n            associated channelDataControl is on and a packet\n            is matched.  The event identified by a particular value\n            of this object is the same event as identified by the\n            same value of the eventIndex object.  If there is no\n            corresponding entry in the eventTable, then no\n            association exists.  In fact, if no event is intended\n            for this channel, channelEventIndex must be\n            set to zero, a non-existent event index.\n    \n            This object may not be modified if the associated\n            channelStatus object is equal to valid(1).')
channelEventStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('eventReady', 1), ('eventFired', 2), ('eventAlwaysReady', 3))).clone('eventReady')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelEventStatus.setDescription('The event status of this channel.\n    \n            If this channel is configured to generate events\n            when packets are matched, a means of controlling\n            the flow of those events is often needed.  When\n            this object is equal to eventReady(1), a single\n            event may be generated, after which this object\n            will be set by the probe to eventFired(2).  While\n            in the eventFired(2) state, no events will be\n            generated until the object is modified to\n            eventReady(1) (or eventAlwaysReady(3)).  The\n            management station can thus easily respond to a\n            notification of an event by re-enabling this object.\n    \n            If the management station wishes to disable this\n            flow control and allow events to be generated\n            at will, this object may be set to\n            eventAlwaysReady(3).  Disabling the flow control\n            is discouraged as it can result in high network\n            traffic or other performance problems.')
channelMatches = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 9), Counter32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    channelMatches.setDescription('The number of times this channel has matched a packet.\n            Note that this object is updated even when\n            channelDataControl is set to off.')
channelDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 10), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelDescription.setDescription('A comment describing this channel.')
channelOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 11), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
channelStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 7, 2, 1, 12), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    channelStatus.setDescription('The status of this channel entry.')
bufferControlTable = MibTable((1, 3, 6, 1, 2, 1, 16, 8, 1))
if mibBuilder.loadTexts:
    bufferControlTable.setDescription('A list of buffers control entries.')
bufferControlEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 8, 1, 1)).setIndexNames((0, 'RMON-MIB', 'bufferControlIndex'))
if mibBuilder.loadTexts:
    bufferControlEntry.setDescription('A set of parameters that control the collection of a stream\n            of packets that have matched filters.  As an example, an\n            instance of the bufferControlCaptureSliceSize object might\n            be named bufferControlCaptureSliceSize.3')
bufferControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bufferControlIndex.setDescription('An index that uniquely identifies an entry\n            in the bufferControl table.  The value of this\n            index shall never be zero.  Each such\n            entry defines one set of packets that is\n            captured and controlled by one or more filters.')
bufferControlChannelIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlChannelIndex.setDescription('An index that identifies the channel that is the\n            source of packets for this bufferControl table.\n            The channel identified by a particular value of this\n            index is the same as identified by the same value of\n            the channelIndex object.\n    \n            This object may not be modified if the associated\n            bufferControlStatus object is equal to valid(1).')
bufferControlFullStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('spaceAvailable', 1), ('full', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bufferControlFullStatus.setDescription('This object shows whether the buffer has room to\n            accept new packets or if it is full.\n    \n            If the status is spaceAvailable(1), the buffer is\n            accepting new packets normally.  If the status is\n            full(2) and the associated bufferControlFullAction\n            object is wrapWhenFull, the buffer is accepting new\n            packets by deleting enough of the oldest packets\n            to make room for new ones as they arrive.  Otherwise,\n            if the status is full(2) and the\n            bufferControlFullAction object is lockWhenFull,\n            then the buffer has stopped collecting packets.\n    \n            When this object is set to full(2) the probe must\n            not later set it to spaceAvailable(1) except in the\n            case of a significant gain in resources such as\n            an increase of bufferControlOctetsGranted.  In\n            particular, the wrap-mode action of deleting old\n            packets to make room for newly arrived packets\n            must not affect the value of this object.')
bufferControlFullAction = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('lockWhenFull', 1), ('wrapWhenFull', 2)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlFullAction.setDescription('Controls the action of the buffer when it\n            reaches the full status.  When in the lockWhenFull(1)\n            state and a packet is added to the buffer that\n            fills the buffer, the bufferControlFullStatus will\n            be set to full(2) and this buffer will stop capturing\n            packets.')
bufferControlCaptureSliceSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 5), Integer32().clone(100)).setUnits('Octets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlCaptureSliceSize.setDescription('The maximum number of octets of each packet\n            that will be saved in this capture buffer.\n            For example, if a 1500 octet packet is received by\n            the probe and this object is set to 500, then only\n            500 octets of the packet will be stored in the\n            associated capture buffer.  If this variable is set\n            to 0, the capture buffer will save as many octets\n            as is possible.\n    \n            This object may not be modified if the associated\n            bufferControlStatus object is equal to valid(1).')
bufferControlDownloadSliceSize = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 6), Integer32().clone(100)).setUnits('Octets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlDownloadSliceSize.setDescription('The maximum number of octets of each packet\n            in this capture buffer that will be returned in\n            an SNMP retrieval of that packet.  For example,\n            if 500 octets of a packet have been stored in the\n            associated capture buffer, the associated\n            bufferControlDownloadOffset is 0, and this\n            object is set to 100, then the captureBufferPacket\n            object that contains the packet will contain only\n            the first 100 octets of the packet.\n    \n            A prudent manager will take into account possible\n            interoperability or fragmentation problems that may\n            occur if the download slice size is set too large.\n            In particular, conformant SNMP implementations are not\n            required to accept messages whose length exceeds 484\n            octets, although they are encouraged to support larger\n            datagrams whenever feasible.')
bufferControlDownloadOffset = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 7), Integer32()).setUnits('Octets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlDownloadOffset.setDescription('The offset of the first octet of each packet\n            in this capture buffer that will be returned in\n            an SNMP retrieval of that packet.  For example,\n            if 500 octets of a packet have been stored in the\n            associated capture buffer and this object is set to\n            100, then the captureBufferPacket object that\n            contains the packet will contain bytes starting\n            100 octets into the packet.')
bufferControlMaxOctetsRequested = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 8), Integer32().clone(-1)).setUnits('Octets').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlMaxOctetsRequested.setDescription('The requested maximum number of octets to be\n            saved in this captureBuffer, including any\n            implementation-specific overhead. If this variable\n            is set to -1, the capture buffer will save as many\n            octets as is possible.\n    \n            When this object is created or modified, the probe\n            should set bufferControlMaxOctetsGranted as closely\n            to this object as is possible for the particular probe\n            implementation and available resources.  However, if\n            the object has the special value of -1, the probe\n            must set bufferControlMaxOctetsGranted to -1.')
bufferControlMaxOctetsGranted = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 9), Integer32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bufferControlMaxOctetsGranted.setDescription('The maximum number of octets that can be\n            saved in this captureBuffer, including overhead.\n            If this variable is -1, the capture buffer will save\n            as many octets as possible.\n    \n            When the bufferControlMaxOctetsRequested object is\n            created or modified, the probe should set this object\n            as closely to the requested value as is possible for the\n            particular probe implementation and available resources.\n            However, if the request object has the special value\n            of -1, the probe must set this object to -1.\n    \n            The probe must not lower this value except as a result of\n            a modification to the associated\n            bufferControlMaxOctetsRequested object.\n    \n            When this maximum number of octets is reached\n            and a new packet is to be added to this\n            capture buffer and the corresponding\n            bufferControlFullAction is set to wrapWhenFull(2),\n            enough of the oldest packets associated with this\n            capture buffer shall be deleted by the agent so\n            that the new packet can be added.  If the corresponding\n            bufferControlFullAction is set to lockWhenFull(1),\n            the new packet shall be discarded.  In either case,\n            the probe must set bufferControlFullStatus to\n            full(2).\n    \n            When the value of this object changes to a value less\n            than the current value, entries are deleted from\n            the captureBufferTable associated with this\n            bufferControlEntry.  Enough of the\n            oldest of these captureBufferEntries shall be\n            deleted by the agent so that the number of octets\n            used remains less than or equal to the new value of\n            this object.\n    \n            When the value of this object changes to a value greater\n            than the current value, the number of associated\n            captureBufferEntries may be allowed to grow.')
bufferControlCapturedPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 10), Integer32()).setUnits('Packets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bufferControlCapturedPackets.setDescription('The number of packets currently in this captureBuffer.')
bufferControlTurnOnTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 11), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bufferControlTurnOnTime.setDescription('The value of sysUpTime when this capture buffer was\n            first turned on.')
bufferControlOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 12), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlOwner.setDescription('The entity that configured this entry and is therefore\n            using the resources assigned to it.')
bufferControlStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 1, 1, 13), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bufferControlStatus.setDescription('The status of this buffer Control Entry.')
captureBufferTable = MibTable((1, 3, 6, 1, 2, 1, 16, 8, 2))
if mibBuilder.loadTexts:
    captureBufferTable.setDescription('A list of packets captured off of a channel.')
captureBufferEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 8, 2, 1)).setIndexNames((0, 'RMON-MIB', 'captureBufferControlIndex'), (0, 'RMON-MIB', 'captureBufferIndex'))
if mibBuilder.loadTexts:
    captureBufferEntry.setDescription('A packet captured off of an attached network.  As an\n            example, an instance of the captureBufferPacketData\n            object might be named captureBufferPacketData.3.1783')
captureBufferControlIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferControlIndex.setDescription('The index of the bufferControlEntry with which\n            this packet is associated.')
captureBufferIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferIndex.setDescription('An index that uniquely identifies an entry\n            in the captureBuffer table associated with a\n            particular bufferControlEntry.  This index will\n            start at 1 and increase by one for each new packet\n            added with the same captureBufferControlIndex.\n    \n            Should this value reach 2147483647, the next packet\n            added with the same captureBufferControlIndex shall\n            cause this value to wrap around to 1.')
captureBufferPacketID = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferPacketID.setDescription("An index that describes the order of packets\n            that are received on a particular interface.\n            The packetID of a packet captured on an\n            interface is defined to be greater than the\n            packetID's of all packets captured previously on\n            the same interface.  As the captureBufferPacketID\n            object has a maximum positive value of 2^31 - 1,\n            any captureBufferPacketID object shall have the\n            value of the associated packet's packetID mod 2^31.")
captureBufferPacketData = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 4), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferPacketData.setDescription('The data inside the packet, starting at the beginning\n            of the packet plus any offset specified in the\n            associated bufferControlDownloadOffset, including any\n            link level headers.  The length of the data in this object\n            is the minimum of the length of the captured packet minus\n            the offset, the length of the associated\n            bufferControlCaptureSliceSize minus the offset, and the\n            associated bufferControlDownloadSliceSize.  If this minimum\n            is less than zero, this object shall have a length of zero.')
captureBufferPacketLength = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 5), Integer32()).setUnits('Octets').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferPacketLength.setDescription('The actual length (off the wire) of the packet stored\n            in this entry, including FCS octets.')
captureBufferPacketTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 6), Integer32()).setUnits('Milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferPacketTime.setDescription('The number of milliseconds that had passed since\n            this capture buffer was first turned on when this\n            packet was captured.')
captureBufferPacketStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 8, 2, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    captureBufferPacketStatus.setDescription("A value which indicates the error status of this packet.\n    \n            The value of this object is defined in the same way as\n            filterPktStatus.  The value is a sum.  This sum\n            initially takes the value zero.  Then, for each\n            error, E, that has been discovered in this packet,\n            2 raised to a value representing E is added to the sum.\n    \n            The errors defined for a packet captured off of an\n            Ethernet interface are as follows:\n    \n                bit #    Error\n                    0    Packet is longer than 1518 octets\n                    1    Packet is shorter than 64 octets\n                    2    Packet experienced a CRC or Alignment error\n                    3    First packet in this capture buffer after\n                         it was detected that some packets were\n                         not processed correctly.\n                    4    Packet's order in buffer is only approximate\n                         (May only be set for packets sent from\n                         the probe)\n    \n            For example, an Ethernet fragment would have a\n            value of 6 (2^1 + 2^2).\n    \n            As this MIB is expanded to new media types, this object\n            will have other media-specific errors defined.")
eventTable = MibTable((1, 3, 6, 1, 2, 1, 16, 9, 1))
if mibBuilder.loadTexts:
    eventTable.setDescription('A list of events to be generated.')
eventEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 9, 1, 1)).setIndexNames((0, 'RMON-MIB', 'eventIndex'))
if mibBuilder.loadTexts:
    eventEntry.setDescription('A set of parameters that describe an event to be generated\n            when certain conditions are met.  As an example, an instance\n            of the eventLastTimeSent object might be named\n            eventLastTimeSent.6')
eventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    eventIndex.setDescription('An index that uniquely identifies an entry in the\n            event table.  Each such entry defines one event that\n            is to be generated when the appropriate conditions\n            occur.')
eventDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    eventDescription.setDescription('A comment describing this event entry.')
eventType = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none', 1), ('log', 2), ('snmptrap', 3), ('logandtrap', 4)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    eventType.setDescription('The type of notification that the probe will make\n            about this event.  In the case of log, an entry is\n            made in the log table for each event.  In the case of\n            snmp-trap, an SNMP trap is sent to one or more\n            management stations.')
eventCommunity = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 127))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    eventCommunity.setDescription('If an SNMP trap is to be sent, it will be sent to\n            the SNMP community specified by this octet string.')
eventLastTimeSent = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 5), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    eventLastTimeSent.setDescription('The value of sysUpTime at the time this event\n            entry last generated an event.  If this entry has\n            not generated any events, this value will be\n            zero.')
eventOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 6), OwnerString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    eventOwner.setDescription("The entity that configured this entry and is therefore\n            using the resources assigned to it.\n            \n            If this object contains a string starting with 'monitor'\n            and has associated entries in the log table, all connected\n            management stations should retrieve those log entries,\n            as they may have significance to all management stations\n            connected to this device")
eventStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 1, 1, 7), EntryStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    eventStatus.setDescription('The status of this event entry.\n            \n            If this object is not equal to valid(1), all associated\n            log entries shall be deleted by the agent.')
logTable = MibTable((1, 3, 6, 1, 2, 1, 16, 9, 2))
if mibBuilder.loadTexts:
    logTable.setDescription('A list of events that have been logged.')
logEntry = MibTableRow((1, 3, 6, 1, 2, 1, 16, 9, 2, 1)).setIndexNames((0, 'RMON-MIB', 'logEventIndex'), (0, 'RMON-MIB', 'logIndex'))
if mibBuilder.loadTexts:
    logEntry.setDescription('A set of data describing an event that has been\n            logged.  For example, an instance of the logDescription\n            object might be named logDescription.6.47')
logEventIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logEventIndex.setDescription('The event entry that generated this log\n            entry.  The log identified by a particular\n            value of this index is associated with the same\n            eventEntry as identified by the same value\n            of eventIndex.')
logIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logIndex.setDescription('An index that uniquely identifies an entry\n            in the log table amongst those generated by the\n            same eventEntries.  These indexes are\n            assigned beginning with 1 and increase by one\n            with each new log entry.  The association\n            between values of logIndex and logEntries\n            is fixed for the lifetime of each logEntry.\n            The agent may choose to delete the oldest\n            instances of logEntry as required because of\n            lack of memory.  It is an implementation-specific\n            matter as to when this deletion may occur.')
logTime = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 2, 1, 3), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logTime.setDescription('The value of sysUpTime when this log entry was created.')
logDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 16, 9, 2, 1, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logDescription.setDescription('An implementation dependent description of the\n            event that activated this log entry.')
rmonEventsV2 = ObjectIdentity((1, 3, 6, 1, 2, 1, 16, 0))
if mibBuilder.loadTexts:
    rmonEventsV2.setDescription('Definition point for RMON notifications.')
risingAlarm = NotificationType((1, 3, 6, 1, 2, 1, 16, 0, 1)).setObjects(*(('RMON-MIB', 'alarmIndex'), ('RMON-MIB', 'alarmVariable'), ('RMON-MIB', 'alarmSampleType'), ('RMON-MIB', 'alarmValue'), ('RMON-MIB', 'alarmRisingThreshold')))
if mibBuilder.loadTexts:
    risingAlarm.setDescription('The SNMP trap that is generated when an alarm\n            entry crosses its rising threshold and generates\n            an event that is configured for sending SNMP\n            traps.')
fallingAlarm = NotificationType((1, 3, 6, 1, 2, 1, 16, 0, 2)).setObjects(*(('RMON-MIB', 'alarmIndex'), ('RMON-MIB', 'alarmVariable'), ('RMON-MIB', 'alarmSampleType'), ('RMON-MIB', 'alarmValue'), ('RMON-MIB', 'alarmFallingThreshold')))
if mibBuilder.loadTexts:
    fallingAlarm.setDescription('The SNMP trap that is generated when an alarm\n            entry crosses its falling threshold and generates\n            an event that is configured for sending SNMP\n            traps.')
rmonCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 20, 9))
rmonGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 16, 20, 10))
rmonCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 16, 20, 9, 1)).setObjects(*(('RMON-MIB', 'rmonEtherStatsGroup'), ('RMON-MIB', 'rmonHistoryControlGroup'), ('RMON-MIB', 'rmonEthernetHistoryGroup'), ('RMON-MIB', 'rmonAlarmGroup'), ('RMON-MIB', 'rmonHostGroup'), ('RMON-MIB', 'rmonHostTopNGroup'), ('RMON-MIB', 'rmonMatrixGroup'), ('RMON-MIB', 'rmonFilterGroup'), ('RMON-MIB', 'rmonPacketCaptureGroup'), ('RMON-MIB', 'rmonEventGroup')))
if mibBuilder.loadTexts:
    rmonCompliance.setDescription('The requirements for conformance to the RMON MIB. At least\n            one of the groups in this module must be implemented to\n            conform to the RMON MIB. Implementations of this MIB\n            must also implement the system group of MIB-II [16] and the\n            IF-MIB [17].')
rmonEtherStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 1)).setObjects(*(('RMON-MIB', 'etherStatsIndex'), ('RMON-MIB', 'etherStatsDataSource'), ('RMON-MIB', 'etherStatsDropEvents'), ('RMON-MIB', 'etherStatsOctets'), ('RMON-MIB', 'etherStatsPkts'), ('RMON-MIB', 'etherStatsBroadcastPkts'), ('RMON-MIB', 'etherStatsMulticastPkts'), ('RMON-MIB', 'etherStatsCRCAlignErrors'), ('RMON-MIB', 'etherStatsUndersizePkts'), ('RMON-MIB', 'etherStatsOversizePkts'), ('RMON-MIB', 'etherStatsFragments'), ('RMON-MIB', 'etherStatsJabbers'), ('RMON-MIB', 'etherStatsCollisions'), ('RMON-MIB', 'etherStatsPkts64Octets'), ('RMON-MIB', 'etherStatsPkts65to127Octets'), ('RMON-MIB', 'etherStatsPkts128to255Octets'), ('RMON-MIB', 'etherStatsPkts256to511Octets'), ('RMON-MIB', 'etherStatsPkts512to1023Octets'), ('RMON-MIB', 'etherStatsPkts1024to1518Octets'), ('RMON-MIB', 'etherStatsOwner'), ('RMON-MIB', 'etherStatsStatus')))
if mibBuilder.loadTexts:
    rmonEtherStatsGroup.setDescription('The RMON Ethernet Statistics Group.')
rmonHistoryControlGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 2)).setObjects(*(('RMON-MIB', 'historyControlIndex'), ('RMON-MIB', 'historyControlDataSource'), ('RMON-MIB', 'historyControlBucketsRequested'), ('RMON-MIB', 'historyControlBucketsGranted'), ('RMON-MIB', 'historyControlInterval'), ('RMON-MIB', 'historyControlOwner'), ('RMON-MIB', 'historyControlStatus')))
if mibBuilder.loadTexts:
    rmonHistoryControlGroup.setDescription('The RMON History Control Group.')
rmonEthernetHistoryGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 3)).setObjects(*(('RMON-MIB', 'etherHistoryIndex'), ('RMON-MIB', 'etherHistorySampleIndex'), ('RMON-MIB', 'etherHistoryIntervalStart'), ('RMON-MIB', 'etherHistoryDropEvents'), ('RMON-MIB', 'etherHistoryOctets'), ('RMON-MIB', 'etherHistoryPkts'), ('RMON-MIB', 'etherHistoryBroadcastPkts'), ('RMON-MIB', 'etherHistoryMulticastPkts'), ('RMON-MIB', 'etherHistoryCRCAlignErrors'), ('RMON-MIB', 'etherHistoryUndersizePkts'), ('RMON-MIB', 'etherHistoryOversizePkts'), ('RMON-MIB', 'etherHistoryFragments'), ('RMON-MIB', 'etherHistoryJabbers'), ('RMON-MIB', 'etherHistoryCollisions'), ('RMON-MIB', 'etherHistoryUtilization')))
if mibBuilder.loadTexts:
    rmonEthernetHistoryGroup.setDescription('The RMON Ethernet History Group.')
rmonAlarmGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 4)).setObjects(*(('RMON-MIB', 'alarmIndex'), ('RMON-MIB', 'alarmInterval'), ('RMON-MIB', 'alarmVariable'), ('RMON-MIB', 'alarmSampleType'), ('RMON-MIB', 'alarmValue'), ('RMON-MIB', 'alarmStartupAlarm'), ('RMON-MIB', 'alarmRisingThreshold'), ('RMON-MIB', 'alarmFallingThreshold'), ('RMON-MIB', 'alarmRisingEventIndex'), ('RMON-MIB', 'alarmFallingEventIndex'), ('RMON-MIB', 'alarmOwner'), ('RMON-MIB', 'alarmStatus')))
if mibBuilder.loadTexts:
    rmonAlarmGroup.setDescription('The RMON Alarm Group.')
rmonHostGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 5)).setObjects(*(('RMON-MIB', 'hostControlIndex'), ('RMON-MIB', 'hostControlDataSource'), ('RMON-MIB', 'hostControlTableSize'), ('RMON-MIB', 'hostControlLastDeleteTime'), ('RMON-MIB', 'hostControlOwner'), ('RMON-MIB', 'hostControlStatus'), ('RMON-MIB', 'hostAddress'), ('RMON-MIB', 'hostCreationOrder'), ('RMON-MIB', 'hostIndex'), ('RMON-MIB', 'hostInPkts'), ('RMON-MIB', 'hostOutPkts'), ('RMON-MIB', 'hostInOctets'), ('RMON-MIB', 'hostOutOctets'), ('RMON-MIB', 'hostOutErrors'), ('RMON-MIB', 'hostOutBroadcastPkts'), ('RMON-MIB', 'hostOutMulticastPkts'), ('RMON-MIB', 'hostTimeAddress'), ('RMON-MIB', 'hostTimeCreationOrder'), ('RMON-MIB', 'hostTimeIndex'), ('RMON-MIB', 'hostTimeInPkts'), ('RMON-MIB', 'hostTimeOutPkts'), ('RMON-MIB', 'hostTimeInOctets'), ('RMON-MIB', 'hostTimeOutOctets'), ('RMON-MIB', 'hostTimeOutErrors'), ('RMON-MIB', 'hostTimeOutBroadcastPkts'), ('RMON-MIB', 'hostTimeOutMulticastPkts')))
if mibBuilder.loadTexts:
    rmonHostGroup.setDescription('The RMON Host Group.')
rmonHostTopNGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 6)).setObjects(*(('RMON-MIB', 'hostTopNControlIndex'), ('RMON-MIB', 'hostTopNHostIndex'), ('RMON-MIB', 'hostTopNRateBase'), ('RMON-MIB', 'hostTopNTimeRemaining'), ('RMON-MIB', 'hostTopNDuration'), ('RMON-MIB', 'hostTopNRequestedSize'), ('RMON-MIB', 'hostTopNGrantedSize'), ('RMON-MIB', 'hostTopNStartTime'), ('RMON-MIB', 'hostTopNOwner'), ('RMON-MIB', 'hostTopNStatus'), ('RMON-MIB', 'hostTopNReport'), ('RMON-MIB', 'hostTopNIndex'), ('RMON-MIB', 'hostTopNAddress'), ('RMON-MIB', 'hostTopNRate')))
if mibBuilder.loadTexts:
    rmonHostTopNGroup.setDescription("The RMON Host Top 'N' Group.")
rmonMatrixGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 7)).setObjects(*(('RMON-MIB', 'matrixControlIndex'), ('RMON-MIB', 'matrixControlDataSource'), ('RMON-MIB', 'matrixControlTableSize'), ('RMON-MIB', 'matrixControlLastDeleteTime'), ('RMON-MIB', 'matrixControlOwner'), ('RMON-MIB', 'matrixControlStatus'), ('RMON-MIB', 'matrixSDSourceAddress'), ('RMON-MIB', 'matrixSDDestAddress'), ('RMON-MIB', 'matrixSDIndex'), ('RMON-MIB', 'matrixSDPkts'), ('RMON-MIB', 'matrixSDOctets'), ('RMON-MIB', 'matrixSDErrors'), ('RMON-MIB', 'matrixDSSourceAddress'), ('RMON-MIB', 'matrixDSDestAddress'), ('RMON-MIB', 'matrixDSIndex'), ('RMON-MIB', 'matrixDSPkts'), ('RMON-MIB', 'matrixDSOctets'), ('RMON-MIB', 'matrixDSErrors')))
if mibBuilder.loadTexts:
    rmonMatrixGroup.setDescription('The RMON Matrix Group.')
rmonFilterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 8)).setObjects(*(('RMON-MIB', 'filterIndex'), ('RMON-MIB', 'filterChannelIndex'), ('RMON-MIB', 'filterPktDataOffset'), ('RMON-MIB', 'filterPktData'), ('RMON-MIB', 'filterPktDataMask'), ('RMON-MIB', 'filterPktDataNotMask'), ('RMON-MIB', 'filterPktStatus'), ('RMON-MIB', 'filterPktStatusMask'), ('RMON-MIB', 'filterPktStatusNotMask'), ('RMON-MIB', 'filterOwner'), ('RMON-MIB', 'filterStatus'), ('RMON-MIB', 'channelIndex'), ('RMON-MIB', 'channelIfIndex'), ('RMON-MIB', 'channelAcceptType'), ('RMON-MIB', 'channelDataControl'), ('RMON-MIB', 'channelTurnOnEventIndex'), ('RMON-MIB', 'channelTurnOffEventIndex'), ('RMON-MIB', 'channelEventIndex'), ('RMON-MIB', 'channelEventStatus'), ('RMON-MIB', 'channelMatches'), ('RMON-MIB', 'channelDescription'), ('RMON-MIB', 'channelOwner'), ('RMON-MIB', 'channelStatus')))
if mibBuilder.loadTexts:
    rmonFilterGroup.setDescription('The RMON Filter Group.')
rmonPacketCaptureGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 9)).setObjects(*(('RMON-MIB', 'bufferControlIndex'), ('RMON-MIB', 'bufferControlChannelIndex'), ('RMON-MIB', 'bufferControlFullStatus'), ('RMON-MIB', 'bufferControlFullAction'), ('RMON-MIB', 'bufferControlCaptureSliceSize'), ('RMON-MIB', 'bufferControlDownloadSliceSize'), ('RMON-MIB', 'bufferControlDownloadOffset'), ('RMON-MIB', 'bufferControlMaxOctetsRequested'), ('RMON-MIB', 'bufferControlMaxOctetsGranted'), ('RMON-MIB', 'bufferControlCapturedPackets'), ('RMON-MIB', 'bufferControlTurnOnTime'), ('RMON-MIB', 'bufferControlOwner'), ('RMON-MIB', 'bufferControlStatus'), ('RMON-MIB', 'captureBufferControlIndex'), ('RMON-MIB', 'captureBufferIndex'), ('RMON-MIB', 'captureBufferPacketID'), ('RMON-MIB', 'captureBufferPacketData'), ('RMON-MIB', 'captureBufferPacketLength'), ('RMON-MIB', 'captureBufferPacketTime'), ('RMON-MIB', 'captureBufferPacketStatus')))
if mibBuilder.loadTexts:
    rmonPacketCaptureGroup.setDescription('The RMON Packet Capture Group.')
rmonEventGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 10)).setObjects(*(('RMON-MIB', 'eventIndex'), ('RMON-MIB', 'eventDescription'), ('RMON-MIB', 'eventType'), ('RMON-MIB', 'eventCommunity'), ('RMON-MIB', 'eventLastTimeSent'), ('RMON-MIB', 'eventOwner'), ('RMON-MIB', 'eventStatus'), ('RMON-MIB', 'logEventIndex'), ('RMON-MIB', 'logIndex'), ('RMON-MIB', 'logTime'), ('RMON-MIB', 'logDescription')))
if mibBuilder.loadTexts:
    rmonEventGroup.setDescription('The RMON Event Group.')
rmonNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 16, 20, 10, 11)).setObjects(*(('RMON-MIB', 'risingAlarm'), ('RMON-MIB', 'fallingAlarm')))
if mibBuilder.loadTexts:
    rmonNotificationGroup.setDescription('The RMON Notification Group.')
mibBuilder.exportSymbols('RMON-MIB', alarmStartupAlarm=alarmStartupAlarm, channelIndex=channelIndex, etherStatsDataSource=etherStatsDataSource, etherStatsUndersizePkts=etherStatsUndersizePkts, history=history, etherStatsOversizePkts=etherStatsOversizePkts, channelTurnOnEventIndex=channelTurnOnEventIndex, hostCreationOrder=hostCreationOrder, channelTurnOffEventIndex=channelTurnOffEventIndex, rmonEventGroup=rmonEventGroup, alarmOwner=alarmOwner, etherStatsCollisions=etherStatsCollisions, EntryStatus=EntryStatus, historyControlDataSource=historyControlDataSource, etherHistoryUtilization=etherHistoryUtilization, hosts=hosts, etherStatsJabbers=etherStatsJabbers, hostTable=hostTable, filterPktStatusNotMask=filterPktStatusNotMask, captureBufferPacketLength=captureBufferPacketLength, filterPktDataOffset=filterPktDataOffset, bufferControlDownloadSliceSize=bufferControlDownloadSliceSize, matrixControlOwner=matrixControlOwner, matrixControlIndex=matrixControlIndex, captureBufferControlIndex=captureBufferControlIndex, bufferControlDownloadOffset=bufferControlDownloadOffset, hostTopNStartTime=hostTopNStartTime, captureBufferPacketData=captureBufferPacketData, bufferControlTable=bufferControlTable, eventCommunity=eventCommunity, matrixDSDestAddress=matrixDSDestAddress, matrixSDPkts=matrixSDPkts, etherStatsEntry=etherStatsEntry, matrixDSErrors=matrixDSErrors, hostTopNRate=hostTopNRate, hostInOctets=hostInOctets, rmon=rmon, hostControlStatus=hostControlStatus, alarmFallingThreshold=alarmFallingThreshold, filterPktStatusMask=filterPktStatusMask, logIndex=logIndex, rmonAlarmGroup=rmonAlarmGroup, historyControlOwner=historyControlOwner, captureBufferIndex=captureBufferIndex, hostOutMulticastPkts=hostOutMulticastPkts, fallingAlarm=fallingAlarm, matrixSDDestAddress=matrixSDDestAddress, matrixControlTableSize=matrixControlTableSize, filter=filter, rmonMatrixGroup=rmonMatrixGroup, filterTable=filterTable, alarmValue=alarmValue, matrixDSTable=matrixDSTable, eventEntry=eventEntry, eventType=eventType, etherHistoryIntervalStart=etherHistoryIntervalStart, etherHistoryCollisions=etherHistoryCollisions, alarmFallingEventIndex=alarmFallingEventIndex, bufferControlMaxOctetsGranted=bufferControlMaxOctetsGranted, hostTimeOutOctets=hostTimeOutOctets, alarmStatus=alarmStatus, etherHistoryOversizePkts=etherHistoryOversizePkts, rmonCompliance=rmonCompliance, channelTable=channelTable, historyControlStatus=historyControlStatus, etherStatsFragments=etherStatsFragments, etherStatsBroadcastPkts=etherStatsBroadcastPkts, hostControlDataSource=hostControlDataSource, hostTopNDuration=hostTopNDuration, hostTopNControlTable=hostTopNControlTable, historyControlBucketsRequested=historyControlBucketsRequested, hostOutPkts=hostOutPkts, hostTimeIndex=hostTimeIndex, logTime=logTime, bufferControlCaptureSliceSize=bufferControlCaptureSliceSize, matrixDSSourceAddress=matrixDSSourceAddress, hostInPkts=hostInPkts, logTable=logTable, etherStatsPkts65to127Octets=etherStatsPkts65to127Octets, statistics=statistics, filterPktDataMask=filterPktDataMask, hostControlTableSize=hostControlTableSize, hostOutOctets=hostOutOctets, etherHistoryJabbers=etherHistoryJabbers, bufferControlCapturedPackets=bufferControlCapturedPackets, etherStatsOctets=etherStatsOctets, historyControlIndex=historyControlIndex, rmonConformance=rmonConformance, hostTimeCreationOrder=hostTimeCreationOrder, eventTable=eventTable, event=event, hostOutErrors=hostOutErrors, hostTimeAddress=hostTimeAddress, bufferControlOwner=bufferControlOwner, hostTopNRateBase=hostTopNRateBase, rmonEthernetHistoryGroup=rmonEthernetHistoryGroup, hostEntry=hostEntry, matrixDSPkts=matrixDSPkts, channelIfIndex=channelIfIndex, captureBufferPacketStatus=captureBufferPacketStatus, hostIndex=hostIndex, eventStatus=eventStatus, channelMatches=channelMatches, hostTopNTable=hostTopNTable, matrixControlDataSource=matrixControlDataSource, channelDescription=channelDescription, OwnerString=OwnerString, bufferControlChannelIndex=bufferControlChannelIndex, hostTopNAddress=hostTopNAddress, eventIndex=eventIndex, matrixSDEntry=matrixSDEntry, etherHistoryTable=etherHistoryTable, hostControlIndex=hostControlIndex, hostTimeOutErrors=hostTimeOutErrors, rmonHistoryControlGroup=rmonHistoryControlGroup, matrixSDIndex=matrixSDIndex, filterPktData=filterPktData, bufferControlEntry=bufferControlEntry, matrix=matrix, hostTopNIndex=hostTopNIndex, hostControlTable=hostControlTable, captureBufferPacketID=captureBufferPacketID, etherHistoryCRCAlignErrors=etherHistoryCRCAlignErrors, etherStatsOwner=etherStatsOwner, hostOutBroadcastPkts=hostOutBroadcastPkts, hostTimeInPkts=hostTimeInPkts, eventOwner=eventOwner, matrixDSOctets=matrixDSOctets, alarmVariable=alarmVariable, etherStatsDropEvents=etherStatsDropEvents, matrixSDTable=matrixSDTable, hostTopNControlEntry=hostTopNControlEntry, hostTopN=hostTopN, matrixControlStatus=matrixControlStatus, etherStatsMulticastPkts=etherStatsMulticastPkts, etherStatsTable=etherStatsTable, channelEventStatus=channelEventStatus, etherHistoryOctets=etherHistoryOctets, hostTopNHostIndex=hostTopNHostIndex, rmonMibModule=rmonMibModule, historyControlEntry=historyControlEntry, bufferControlTurnOnTime=bufferControlTurnOnTime, historyControlTable=historyControlTable, etherHistoryFragments=etherHistoryFragments, hostTimeOutBroadcastPkts=hostTimeOutBroadcastPkts, hostTopNTimeRemaining=hostTopNTimeRemaining, matrixControlLastDeleteTime=matrixControlLastDeleteTime, etherStatsPkts512to1023Octets=etherStatsPkts512to1023Octets, hostControlEntry=hostControlEntry, PYSNMP_MODULE_ID=rmonMibModule, bufferControlMaxOctetsRequested=bufferControlMaxOctetsRequested, alarmInterval=alarmInterval, channelStatus=channelStatus, hostTopNGrantedSize=hostTopNGrantedSize, filterOwner=filterOwner, etherHistoryEntry=etherHistoryEntry, bufferControlStatus=bufferControlStatus, etherStatsPkts=etherStatsPkts, alarmTable=alarmTable, matrixSDSourceAddress=matrixSDSourceAddress, filterStatus=filterStatus, filterPktDataNotMask=filterPktDataNotMask, etherHistoryDropEvents=etherHistoryDropEvents, alarmIndex=alarmIndex, hostTopNEntry=hostTopNEntry, captureBufferEntry=captureBufferEntry, etherStatsIndex=etherStatsIndex, hostTopNStatus=hostTopNStatus, etherHistoryBroadcastPkts=etherHistoryBroadcastPkts, bufferControlFullAction=bufferControlFullAction, matrixControlEntry=matrixControlEntry, historyControlBucketsGranted=historyControlBucketsGranted, etherStatsCRCAlignErrors=etherStatsCRCAlignErrors, rmonCompliances=rmonCompliances, hostControlLastDeleteTime=hostControlLastDeleteTime, hostControlOwner=hostControlOwner, filterIndex=filterIndex, filterPktStatus=filterPktStatus, bufferControlIndex=bufferControlIndex, bufferControlFullStatus=bufferControlFullStatus, rmonHostTopNGroup=rmonHostTopNGroup, rmonGroups=rmonGroups, hostTimeOutMulticastPkts=hostTimeOutMulticastPkts, hostTimeTable=hostTimeTable, matrixDSEntry=matrixDSEntry, filterEntry=filterEntry, etherStatsPkts1024to1518Octets=etherStatsPkts1024to1518Octets, capture=capture, alarmSampleType=alarmSampleType, historyControlInterval=historyControlInterval, filterChannelIndex=filterChannelIndex, rmonHostGroup=rmonHostGroup, etherHistoryIndex=etherHistoryIndex, rmonEventsV2=rmonEventsV2, etherStatsStatus=etherStatsStatus, hostAddress=hostAddress, matrixSDOctets=matrixSDOctets, captureBufferTable=captureBufferTable, eventLastTimeSent=eventLastTimeSent, etherStatsPkts128to255Octets=etherStatsPkts128to255Octets, etherHistoryMulticastPkts=etherHistoryMulticastPkts, hostTopNReport=hostTopNReport, rmonEtherStatsGroup=rmonEtherStatsGroup, hostTopNOwner=hostTopNOwner, alarm=alarm, hostTimeEntry=hostTimeEntry, channelDataControl=channelDataControl, channelEntry=channelEntry, alarmEntry=alarmEntry, hostTimeOutPkts=hostTimeOutPkts, channelOwner=channelOwner, logDescription=logDescription, hostTimeInOctets=hostTimeInOctets, etherHistorySampleIndex=etherHistorySampleIndex, eventDescription=eventDescription, hostTopNRequestedSize=hostTopNRequestedSize, etherStatsPkts256to511Octets=etherStatsPkts256to511Octets, etherHistoryUndersizePkts=etherHistoryUndersizePkts, matrixDSIndex=matrixDSIndex, channelEventIndex=channelEventIndex, rmonFilterGroup=rmonFilterGroup, channelAcceptType=channelAcceptType, etherHistoryPkts=etherHistoryPkts, logEventIndex=logEventIndex, rmonNotificationGroup=rmonNotificationGroup, rmonPacketCaptureGroup=rmonPacketCaptureGroup, captureBufferPacketTime=captureBufferPacketTime, risingAlarm=risingAlarm, alarmRisingEventIndex=alarmRisingEventIndex, alarmRisingThreshold=alarmRisingThreshold, hostTopNControlIndex=hostTopNControlIndex, logEntry=logEntry, matrixControlTable=matrixControlTable, etherStatsPkts64Octets=etherStatsPkts64Octets, matrixSDErrors=matrixSDErrors)