# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/UCD-SNMP-MIB.py
# Compiled at: 2016-02-13 18:32:22
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ValueRangeConstraint', 'ConstraintsUnion')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Gauge32, MibIdentifier, Opaque, Integer32, NotificationType, Bits, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter32, Counter64, enterprises, ObjectIdentity, iso, IpAddress, ModuleIdentity, Unsigned32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'MibIdentifier', 'Opaque', 'Integer32', 'NotificationType', 'Bits', 'TimeTicks', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter32', 'Counter64', 'enterprises', 'ObjectIdentity', 'iso', 'IpAddress', 'ModuleIdentity', 'Unsigned32')
(TextualConvention, DisplayString, TruthValue) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString', 'TruthValue')
ucdavis = ModuleIdentity((1, 3, 6, 1, 4, 1, 2021)).setRevisions(('2011-05-14 00:00',
                                                                 '2009-01-19 00:00',
                                                                 '2006-11-22 00:00',
                                                                 '2004-04-07 00:00',
                                                                 '2002-09-05 00:00',
                                                                 '2001-09-20 00:00',
                                                                 '2001-01-17 00:00',
                                                                 '1999-12-09 00:00'))
if mibBuilder.loadTexts:
    ucdavis.setLastUpdated('200901190000Z')
if mibBuilder.loadTexts:
    ucdavis.setOrganization('University of California, Davis')
if mibBuilder.loadTexts:
    ucdavis.setContactInfo('This mib is no longer being maintained by the University of\n\t California and is now in life-support-mode and being\n\t maintained by the net-snmp project.  The best place to write\n\t for public questions about the net-snmp-coders mailing list\n\t at net-snmp-coders@lists.sourceforge.net.\n\n         postal:   Wes Hardaker\n                   P.O. Box 382\n                   Davis CA  95617\n\n         email:    net-snmp-coders@lists.sourceforge.net\n        ')
if mibBuilder.loadTexts:
    ucdavis.setDescription('This file defines the private UCD SNMP MIB extensions.')
ucdInternal = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 12))
ucdExperimental = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 13))
ucdSnmpAgent = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250))
hpux9 = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 1))
sunos4 = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 2))
solaris = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 3))
osf = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 4))
ultrix = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 5))
hpux10 = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 6))
netbsd1 = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 7))
freebsd = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 8))
irix = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 9))
linux = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 10))
bsdi = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 11))
openbsd = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 12))
win32 = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 13))
hpux11 = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 14))
aix = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 15))
macosx = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 16))
dragonfly = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 17))
unknown = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 250, 255))

class Float(Opaque, TextualConvention):
    __module__ = __name__
    subtypeSpec = Opaque.subtypeSpec + ValueSizeConstraint(7, 7)
    fixedLength = 7


class UCDErrorFlag(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(0, 1))
    namedValues = NamedValues(('noError', 0), ('error', 1))


class UCDErrorFix(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(0, 1))
    namedValues = NamedValues(('noError', 0), ('runFix', 1))


prTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 2))
if mibBuilder.loadTexts:
    prTable.setDescription("A table containing information on running\n\t programs/daemons configured for monitoring in the\n\t snmpd.conf file of the agent.  Processes violating the\n\t number of running processes required by the agent's\n\t configuration file are flagged with numerical and\n\t textual errors.")
prEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 2, 1)).setIndexNames((0, 'UCD-SNMP-MIB',
                                                                     'prIndex'))
if mibBuilder.loadTexts:
    prEntry.setDescription('An entry containing a process and its statistics.')
prIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prIndex.setDescription('Reference Index for each observed process.')
prNames = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prNames.setDescription("The process name we're counting/checking on.")
prMin = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prMin.setDescription('The minimum number of processes that should be\n\t running.  An error flag is generated if the number of\n\t running processes is < the minimum.')
prMax = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prMax.setDescription('The maximum number of processes that should be\n\t running.  An error flag is generated if the number of\n\t running processes is > the maximum.')
prCount = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prCount.setDescription('The number of current processes running with the name\n\t in question.')
prErrorFlag = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prErrorFlag.setDescription('A Error flag to indicate trouble with a process.  It\n\t goes to 1 if there is an error, 0 if no error.')
prErrMessage = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prErrMessage.setDescription('An error message describing the problem (if one exists).')
prErrFix = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 102), UCDErrorFix()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    prErrFix.setDescription('Setting this to one will try to fix the problem if\n\t the agent has been configured with a script to call\n\t to attempt to fix problems automatically using remote\n\t snmp operations.')
prErrFixCmd = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 2, 1, 103), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    prErrFixCmd.setDescription('The command that gets run when the prErrFix column is \n\t set to 1.')
extTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 8))
if mibBuilder.loadTexts:
    extTable.setDescription("A table of extensible commands returning output and\n\t result codes.  These commands are configured via the\n\t agent's snmpd.conf file.")
extEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 8, 1)).setIndexNames((0, 'UCD-SNMP-MIB',
                                                                      'extIndex'))
if mibBuilder.loadTexts:
    extEntry.setDescription('An entry containing an extensible script/program and its output.')
extIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    extIndex.setDescription('Reference Index for extensible scripts.  Simply an\n\t integer row number.')
extNames = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    extNames.setDescription('A Short, one name description of the extensible command.')
extCommand = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 3), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    extCommand.setDescription('The command line to be executed.')
extResult = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 100), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    extResult.setDescription('The result code (exit status) from the executed command.')
extOutput = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    extOutput.setDescription('The first line of output of the executed command.')
extErrFix = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 102), UCDErrorFix()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    extErrFix.setDescription('Setting this to one will try to fix the problem if\n\t the agent has been configured with a script to call\n\t to attempt to fix problems automatically using remote\n\t snmp operations.')
extErrFixCmd = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 8, 1, 103), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    extErrFixCmd.setDescription('The command that gets run when the extErrFix column is \n\t set to 1.')
memory = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 4))
memIndex = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memIndex.setDescription('Bogus Index.  This should always return the integer 0.')
memErrorName = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memErrorName.setDescription("Bogus Name. This should always return the string 'swap'.")
memTotalSwap = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 3), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memTotalSwap.setDescription('The total amount of swap space configured for this host.')
memAvailSwap = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 4), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memAvailSwap.setDescription('The amount of swap space currently unused or available.')
memTotalReal = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 5), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memTotalReal.setDescription('The total amount of real/physical memory installed\n         on this host.')
memAvailReal = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 6), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memAvailReal.setDescription('The amount of real/physical memory currently unused\n         or available.')
memTotalSwapTXT = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 7), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memTotalSwapTXT.setDescription('The total amount of swap space or virtual memory allocated\n         for text pages on this host.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not distinguish text\n         pages from other uses of swap space or virtual memory.')
memAvailSwapTXT = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 8), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memAvailSwapTXT.setDescription("The amount of swap space or virtual memory currently\n         being used by text pages on this host.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not distinguish text\n         pages from other uses of swap space or virtual memory.\n\n         Note that (despite the name), this value reports the\n         amount used, rather than the amount free or available\n         for use.  For clarity, this object is being deprecated\n         in favour of 'memUsedSwapTXT(16).")
memTotalRealTXT = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 9), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memTotalRealTXT.setDescription('The total amount of real/physical memory allocated\n         for text pages on this host.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not distinguish text\n         pages from other uses of physical memory.')
memAvailRealTXT = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 10), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memAvailRealTXT.setDescription("The amount of real/physical memory currently being\n         used by text pages on this host.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not distinguish text\n         pages from other uses of physical memory.\n\n         Note that (despite the name), this value reports the\n         amount used, rather than the amount free or available\n         for use.  For clarity, this object is being deprecated\n         in favour of 'memUsedRealTXT(17).")
memTotalFree = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 11), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memTotalFree.setDescription('The total amount of memory free or available for use on\n         this host.  This value typically covers both real memory\n         and swap space or virtual memory.')
memMinimumSwap = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 12), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memMinimumSwap.setDescription("The minimum amount of swap space expected to be kept\n         free or available during normal operation of this host.\n\n         If this value (as reported by 'memAvailSwap(4)') falls\n         below the specified level, then 'memSwapError(100)' will\n         be set to 1 and an error message made available via\n         'memSwapErrorMsg(101)'.")
memShared = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 13), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memShared.setDescription('The total amount of real or virtual memory currently\n         allocated for use as shared memory.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not explicitly identify\n         memory as specifically reserved for this purpose.')
memBuffer = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 14), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memBuffer.setDescription('The total amount of real or virtual memory currently\n         allocated for use as memory buffers.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not explicitly identify\n         memory as specifically reserved for this purpose.')
memCached = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 15), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memCached.setDescription('The total amount of real or virtual memory currently\n         allocated for use as cached memory.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not explicitly identify\n         memory as specifically reserved for this purpose.')
memUsedSwapTXT = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 16), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memUsedSwapTXT.setDescription('The amount of swap space or virtual memory currently\n         being used by text pages on this host.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not distinguish text\n         pages from other uses of swap space or virtual memory.')
memUsedRealTXT = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 17), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memUsedRealTXT.setDescription('The amount of real/physical memory currently being\n         used by text pages on this host.\n\n         This object will not be implemented on hosts where the\n         underlying operating system does not distinguish text\n         pages from other uses of physical memory.')
memSwapError = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memSwapError.setDescription("Indicates whether the amount of available swap space\n         (as reported by 'memAvailSwap(4)'), is less than the\n         desired minimum (specified by 'memMinimumSwap(12)').")
memSwapErrorMsg = MibScalar((1, 3, 6, 1, 4, 1, 2021, 4, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    memSwapErrorMsg.setDescription("Describes whether the amount of available swap space\n         (as reported by 'memAvailSwap(4)'), is less than the\n         desired minimum (specified by 'memMinimumSwap(12)').")
dskTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 9))
if mibBuilder.loadTexts:
    dskTable.setDescription('Disk watching information.  Partions to be watched\n\t are configured by the snmpd.conf file of the agent.')
dskEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 9, 1)).setIndexNames((0, 'UCD-SNMP-MIB',
                                                                      'dskIndex'))
if mibBuilder.loadTexts:
    dskEntry.setDescription('An entry containing a disk and its statistics.')
dskIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskIndex.setDescription('Integer reference number (row number) for the disk mib.')
dskPath = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskPath.setDescription('Path where the disk is mounted.')
dskDevice = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 3), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskDevice.setDescription('Path of the device for the partition')
dskMinimum = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskMinimum.setDescription("Minimum space required on the disk (in kBytes) before the\n         errors are triggered.  Either this or dskMinPercent is\n         configured via the agent's snmpd.conf file.")
dskMinPercent = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskMinPercent.setDescription("Percentage of minimum space required on the disk before the\n         errors are triggered.  Either this or dskMinimum is\n         configured via the agent's snmpd.conf file.")
dskTotal = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskTotal.setDescription('Total size of the disk/partion (kBytes).\n\t For large disks (>2Tb), this value will\n\t latch at INT32_MAX (2147483647).')
dskAvail = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskAvail.setDescription('Available space on the disk.\n\t For large lightly-used disks (>2Tb), this\n\t value will latch at INT32_MAX (2147483647).')
dskUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 8), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskUsed.setDescription('Used space on the disk.\n\t For large heavily-used disks (>2Tb), this\n\t value will latch at INT32_MAX (2147483647).')
dskPercent = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 9), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskPercent.setDescription('Percentage of space used on disk')
dskPercentNode = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 10), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskPercentNode.setDescription('Percentage of inodes used on disk')
dskTotalLow = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 11), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskTotalLow.setDescription('Total size of the disk/partion (kBytes).\n\tTogether with dskTotalHigh composes 64-bit number.')
dskTotalHigh = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 12), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskTotalHigh.setDescription('Total size of the disk/partion (kBytes).\n\tTogether with dskTotalLow composes 64-bit number.')
dskAvailLow = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 13), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskAvailLow.setDescription('Available space on the disk (kBytes).\n\tTogether with dskAvailHigh composes 64-bit number.')
dskAvailHigh = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 14), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskAvailHigh.setDescription('Available space on the disk (kBytes).\n\tTogether with dskAvailLow composes 64-bit number.')
dskUsedLow = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 15), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskUsedLow.setDescription('Used space on the disk (kBytes).\n\tTogether with dskUsedHigh composes 64-bit number.')
dskUsedHigh = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 16), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskUsedHigh.setDescription('Used space on the disk (kBytes).\n\tTogether with dskUsedLow composes 64-bit number.')
dskErrorFlag = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskErrorFlag.setDescription('Error flag signaling that the disk or partition is under\n\t the minimum required space configured for it.')
dskErrorMsg = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 9, 1, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dskErrorMsg.setDescription('A text description providing a warning and the space left\n\t on the disk.')
laTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 10))
if mibBuilder.loadTexts:
    laTable.setDescription('Load average information.')
laEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 10, 1)).setIndexNames((0, 'UCD-SNMP-MIB',
                                                                      'laIndex'))
if mibBuilder.loadTexts:
    laEntry.setDescription('An entry containing a load average and its values.')
laIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laIndex.setDescription('reference index/row number for each observed loadave.')
laNames = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laNames.setDescription("The list of loadave names we're watching.")
laLoad = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 3), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laLoad.setDescription('The 1,5 and 15 minute load averages (one per row).')
laConfig = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 4), DisplayString()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    laConfig.setDescription('The watch point for load-averages to signal an\n\t error.  If the load averages rises above this value,\n\t the laErrorFlag below is set.')
laLoadInt = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 5), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laLoadInt.setDescription('The 1,5 and 15 minute load averages as an integer.\n\t This is computed by taking the floating point\n\t loadaverage value and multiplying by 100, then\n\t converting the value to an integer.')
laLoadFloat = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 6), Float()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laLoadFloat.setDescription('The 1,5 and 15 minute load averages as an opaquely\n\t wrapped floating point number.')
laErrorFlag = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laErrorFlag.setDescription('A Error flag to indicate the load-average has crossed\n\t its threshold value defined in the snmpd.conf file.\n\t It is set to 1 if the threshold is crossed, 0 otherwise.')
laErrMessage = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 10, 1, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    laErrMessage.setDescription('An error message describing the load-average and its\n\t surpased watch-point value.')
version = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 100))
versionIndex = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    versionIndex.setDescription('Index to mib (always 0)')
versionTag = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    versionTag.setDescription('CVS tag keyword')
versionDate = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 3), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    versionDate.setDescription('Date string from RCS keyword')
versionCDate = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 4), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    versionCDate.setDescription('Date string from ctime() ')
versionIdent = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 5), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    versionIdent.setDescription('Id string from RCS keyword')
versionConfigureOptions = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 6), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    versionConfigureOptions.setDescription('Options passed to the configure script when this agent was built.')
versionClearCache = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 10), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    versionClearCache.setDescription('Set to 1 to clear the exec cache, if enabled')
versionUpdateConfig = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 11), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    versionUpdateConfig.setDescription('Set to 1 to read-read the config file(s).')
versionRestartAgent = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 12), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    versionRestartAgent.setDescription('Set to 1 to restart the agent.')
versionSavePersistentData = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 13), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    versionSavePersistentData.setDescription("Set to 1 to force the agent to save it's persistent data immediately.")
versionDoDebugging = MibScalar((1, 3, 6, 1, 4, 1, 2021, 100, 20), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    versionDoDebugging.setDescription('Set to 1 to turn debugging statements on in the agent or 0\n\t to turn it off.')
snmperrs = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 101))
snmperrIndex = MibScalar((1, 3, 6, 1, 4, 1, 2021, 101, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmperrIndex.setDescription('Bogus Index for snmperrs (always 0).')
snmperrNames = MibScalar((1, 3, 6, 1, 4, 1, 2021, 101, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmperrNames.setDescription('snmp')
snmperrErrorFlag = MibScalar((1, 3, 6, 1, 4, 1, 2021, 101, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmperrErrorFlag.setDescription('A Error flag to indicate trouble with the agent.  It\n\t goes to 1 if there is an error, 0 if no error.')
snmperrErrMessage = MibScalar((1, 3, 6, 1, 4, 1, 2021, 101, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmperrErrMessage.setDescription('An error message describing the problem (if one exists).')
mrTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 102))
if mibBuilder.loadTexts:
    mrTable.setDescription("A table displaying all the oid's registered by mib modules in\n\t the agent.  Since the agent is modular in nature, this lists\n\t each module's OID it is responsible for and the name of the module")
mrEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 102, 1)).setIndexNames((1, 'UCD-SNMP-MIB',
                                                                       'mrIndex'))
if mibBuilder.loadTexts:
    mrEntry.setDescription('An entry containing a registered mib oid.')
mrIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 102, 1, 1), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    mrIndex.setDescription('The registry slot of a mibmodule.')
mrModuleName = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 102, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    mrModuleName.setDescription('The module name that registered this OID.')
systemStats = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 11))
ssIndex = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssIndex.setDescription('Bogus Index.  This should always return the integer 1.')
ssErrorName = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssErrorName.setDescription("Bogus Name. This should always return the string 'systemStats'.")
ssSwapIn = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 3), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssSwapIn.setDescription('The average amount of memory swapped in from disk,\n         calculated over the last minute.')
ssSwapOut = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 4), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssSwapOut.setDescription('The average amount of memory swapped out to disk,\n         calculated over the last minute.')
ssIOSent = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 5), Integer32()).setUnits('blocks/s').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssIOSent.setDescription("The average amount of data written to disk or other\n         block device, calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssIORawSent(57)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssIOReceive = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 6), Integer32()).setUnits('blocks/s').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssIOReceive.setDescription("The average amount of data read from disk or other\n         block device, calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssIORawReceived(58)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssSysInterrupts = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 7), Integer32()).setUnits('interrupts/s').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssSysInterrupts.setDescription("The average rate of interrupts processed (including\n         the clock) calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssRawInterrupts(59)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssSysContext = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 8), Integer32()).setUnits('switches/s').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssSysContext.setDescription("The average rate of context switches,\n         calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssRawContext(60)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssCpuUser = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 9), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuUser.setDescription("The percentage of CPU time spent processing\n         user-level code, calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssCpuRawUser(50)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssCpuSystem = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 10), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuSystem.setDescription("The percentage of CPU time spent processing\n         system-level code, calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssCpuRawSystem(52)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssCpuIdle = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 11), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuIdle.setDescription("The percentage of processor time spent idle,\n         calculated over the last minute.\n       \n\t This object has been deprecated in favour of\n         'ssCpuRawIdle(53)', which can be used to calculate\n         the same metric, but over any desired time period.")
ssCpuRawUser = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 50), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawUser.setDescription("The number of 'ticks' (typically 1/100s) spent\n         processing user-level code.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawNice = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 51), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawNice.setDescription("The number of 'ticks' (typically 1/100s) spent\n         processing reduced-priority code.\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawSystem = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 52), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawSystem.setDescription("The number of 'ticks' (typically 1/100s) spent\n         processing system-level code.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).\n\n         This object may sometimes be implemented as the\n         combination of the 'ssCpuRawWait(54)' and\n         'ssCpuRawKernel(55)' counters, so care must be\n         taken when summing the overall raw counters.")
ssCpuRawIdle = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 53), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawIdle.setDescription("The number of 'ticks' (typically 1/100s) spent\n         idle.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawWait = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 54), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawWait.setDescription("The number of 'ticks' (typically 1/100s) spent\n         waiting for IO.\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.  This time may also be\n         included within the 'ssCpuRawSystem(52)' counter.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawKernel = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 55), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawKernel.setDescription("The number of 'ticks' (typically 1/100s) spent\n         processing kernel-level code.\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.  This time may also be\n         included within the 'ssCpuRawSystem(52)' counter.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawInterrupt = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 56), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawInterrupt.setDescription("The number of 'ticks' (typically 1/100s) spent\n         processing hardware interrupts.\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssIORawSent = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 57), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssIORawSent.setDescription('Number of blocks sent to a block device')
ssIORawReceived = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 58), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssIORawReceived.setDescription('Number of blocks received from a block device')
ssRawInterrupts = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 59), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssRawInterrupts.setDescription('Number of interrupts processed')
ssRawContexts = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 60), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssRawContexts.setDescription('Number of context switches')
ssCpuRawSoftIRQ = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 61), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawSoftIRQ.setDescription("The number of 'ticks' (typically 1/100s) spent\n         processing software interrupts.\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssRawSwapIn = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 62), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssRawSwapIn.setDescription('Number of blocks swapped in')
ssRawSwapOut = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 63), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssRawSwapOut.setDescription('Number of blocks swapped out')
ssCpuRawSteal = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 64), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawSteal.setDescription("The number of 'ticks' (typically 1/100s) spent\n         by the hypervisor code to run other VMs even\n         though the CPU in the current VM had something runnable.\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawGuest = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 65), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawGuest.setDescription("The number of 'ticks' (typically 1/100s) spent\n         by the CPU to run a virtual CPU (guest).\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ssCpuRawGuestNice = MibScalar((1, 3, 6, 1, 4, 1, 2021, 11, 66), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ssCpuRawGuestNice.setDescription("The number of 'ticks' (typically 1/100s) spent\n         by the CPU to run a niced virtual CPU (guest).\n\n         This object will not be implemented on hosts where\n         the underlying operating system does not measure\n         this particular CPU metric.\n\n         On a multi-processor system, the 'ssCpuRaw*'\n         counters are cumulative over all CPUs, so their\n         sum will typically be N*100 (for N processors).")
ucdTraps = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 251))
ucdStart = NotificationType((1, 3, 6, 1, 4, 1, 2021, 251, 1)).setObjects(*())
if mibBuilder.loadTexts:
    ucdStart.setDescription('This trap could in principle be sent when the agent start')
ucdShutdown = NotificationType((1, 3, 6, 1, 4, 1, 2021, 251, 2)).setObjects(*())
if mibBuilder.loadTexts:
    ucdShutdown.setDescription('This trap is sent when the agent terminates')
fileTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 15))
if mibBuilder.loadTexts:
    fileTable.setDescription('Table of monitored files.')
fileEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 15, 1)).setIndexNames((0, 'UCD-SNMP-MIB',
                                                                        'fileIndex'))
if mibBuilder.loadTexts:
    fileEntry.setDescription('Entry of file')
fileIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 15, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fileIndex.setDescription('Index of file')
fileName = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 15, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fileName.setDescription('Filename')
fileSize = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 15, 1, 3), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fileSize.setDescription('Size of file (kB)')
fileMax = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 15, 1, 4), Integer32()).setUnits('kB').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fileMax.setDescription('Limit of filesize (kB)')
fileErrorFlag = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 15, 1, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fileErrorFlag.setDescription('Limit exceeded flag')
fileErrorMsg = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 15, 1, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fileErrorMsg.setDescription('Filesize error message')
logMatch = MibIdentifier((1, 3, 6, 1, 4, 1, 2021, 16))
logMatchMaxEntries = MibScalar((1, 3, 6, 1, 4, 1, 2021, 16, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchMaxEntries.setDescription('The maximum number of logmatch entries\n\t\tthis snmpd daemon can support.')
logMatchTable = MibTable((1, 3, 6, 1, 4, 1, 2021, 16, 2))
if mibBuilder.loadTexts:
    logMatchTable.setDescription('Table of monitored files.')
logMatchEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1)).setIndexNames((0, 'UCD-SNMP-MIB',
                                                                               'logMatchIndex'))
if mibBuilder.loadTexts:
    logMatchEntry.setDescription('Entry of file')
logMatchIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchIndex.setDescription('Index of logmatch')
logMatchName = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 2), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchName.setDescription('logmatch instance name')
logMatchFilename = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 3), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchFilename.setDescription('filename to be logmatched')
logMatchRegEx = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 4), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchRegEx.setDescription('regular expression')
logMatchGlobalCounter = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchGlobalCounter.setDescription('global count of matches')
logMatchGlobalCount = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchGlobalCount.setDescription('Description.')
logMatchCurrentCounter = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchCurrentCounter.setDescription('Regex match counter. This counter will\n\t\tbe reset with each logfile rotation.')
logMatchCurrentCount = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 8), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchCurrentCount.setDescription('Description.')
logMatchCounter = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchCounter.setDescription('Regex match counter. This counter will\n\t\tbe reset with each read')
logMatchCount = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 10), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchCount.setDescription('Description.')
logMatchCycle = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 11), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchCycle.setDescription('time between updates (if not queried) in seconds')
logMatchErrorFlag = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 100), UCDErrorFlag()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchErrorFlag.setDescription('errorflag: is this line configured correctly?')
logMatchRegExCompilation = MibTableColumn((1, 3, 6, 1, 4, 1, 2021, 16, 2, 1, 101), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    logMatchRegExCompilation.setDescription('message of regex precompilation')
mibBuilder.exportSymbols('UCD-SNMP-MIB', ucdavis=ucdavis, versionClearCache=versionClearCache, fileName=fileName, memTotalSwapTXT=memTotalSwapTXT, snmperrIndex=snmperrIndex, logMatchCounter=logMatchCounter, logMatchCycle=logMatchCycle, dskAvailHigh=dskAvailHigh, logMatchCurrentCount=logMatchCurrentCount, extNames=extNames, snmperrErrorFlag=snmperrErrorFlag, extResult=extResult, ucdInternal=ucdInternal, ssSysContext=ssSysContext, ssRawInterrupts=ssRawInterrupts, logMatchMaxEntries=logMatchMaxEntries, ssIORawSent=ssIORawSent, prErrFix=prErrFix, laConfig=laConfig, versionCDate=versionCDate, versionRestartAgent=versionRestartAgent, irix=irix, memIndex=memIndex, memTotalSwap=memTotalSwap, ssCpuRawNice=ssCpuRawNice, laLoadFloat=laLoadFloat, ucdShutdown=ucdShutdown, memShared=memShared, memCached=memCached, PYSNMP_MODULE_ID=ucdavis, memSwapErrorMsg=memSwapErrorMsg, snmperrErrMessage=snmperrErrMessage, logMatchErrorFlag=logMatchErrorFlag, memUsedRealTXT=memUsedRealTXT, mrEntry=mrEntry, dskUsedHigh=dskUsedHigh, extErrFixCmd=extErrFixCmd, version=version, dskPath=dskPath, dskErrorFlag=dskErrorFlag, UCDErrorFix=UCDErrorFix, ssIOReceive=ssIOReceive, ssCpuUser=ssCpuUser, extIndex=extIndex, extEntry=extEntry, versionSavePersistentData=versionSavePersistentData, mrModuleName=mrModuleName, ssErrorName=ssErrorName, memUsedSwapTXT=memUsedSwapTXT, ssCpuRawGuestNice=ssCpuRawGuestNice, versionDoDebugging=versionDoDebugging, dragonfly=dragonfly, memMinimumSwap=memMinimumSwap, ucdExperimental=ucdExperimental, ssIOSent=ssIOSent, logMatchTable=logMatchTable, prErrFixCmd=prErrFixCmd, laNames=laNames, dskEntry=dskEntry, dskAvail=dskAvail, snmperrs=snmperrs, versionUpdateConfig=versionUpdateConfig, versionConfigureOptions=versionConfigureOptions, fileEntry=fileEntry, ssSwapIn=ssSwapIn, logMatchCurrentCounter=logMatchCurrentCounter, ssIndex=ssIndex, prErrorFlag=prErrorFlag, memTotalReal=memTotalReal, fileTable=fileTable, memSwapError=memSwapError, dskUsed=dskUsed, ssSwapOut=ssSwapOut, memBuffer=memBuffer, macosx=macosx, extErrFix=extErrFix, dskUsedLow=dskUsedLow, memAvailRealTXT=memAvailRealTXT, versionIndex=versionIndex, versionIdent=versionIdent, ssCpuRawKernel=ssCpuRawKernel, ssCpuRawSystem=ssCpuRawSystem, laIndex=laIndex, osf=osf, prEntry=prEntry, laLoadInt=laLoadInt, ssCpuRawInterrupt=ssCpuRawInterrupt, snmperrNames=snmperrNames, UCDErrorFlag=UCDErrorFlag, dskDevice=dskDevice, memAvailSwapTXT=memAvailSwapTXT, logMatchRegEx=logMatchRegEx, sunos4=sunos4, logMatchIndex=logMatchIndex, dskMinPercent=dskMinPercent, hpux10=hpux10, ssCpuRawIdle=ssCpuRawIdle, prTable=prTable, dskIndex=dskIndex, versionDate=versionDate, dskMinimum=dskMinimum, laErrMessage=laErrMessage, laErrorFlag=laErrorFlag, ssCpuRawSoftIRQ=ssCpuRawSoftIRQ, freebsd=freebsd, ssRawSwapIn=ssRawSwapIn, logMatchGlobalCount=logMatchGlobalCount, openbsd=openbsd, solaris=solaris, dskTotal=dskTotal, ucdTraps=ucdTraps, ssRawContexts=ssRawContexts, ssIORawReceived=ssIORawReceived, ssRawSwapOut=ssRawSwapOut, prIndex=prIndex, fileErrorMsg=fileErrorMsg, fileMax=fileMax, hpux9=hpux9, netbsd1=netbsd1, linux=linux, prMax=prMax, prErrMessage=prErrMessage, dskTotalHigh=dskTotalHigh, ssCpuRawSteal=ssCpuRawSteal, logMatchCount=logMatchCount, fileIndex=fileIndex, aix=aix, versionTag=versionTag, logMatchEntry=logMatchEntry, extOutput=extOutput, laTable=laTable, ssCpuRawGuest=ssCpuRawGuest, ssCpuRawUser=ssCpuRawUser, extCommand=extCommand, ssCpuSystem=ssCpuSystem, ssCpuRawWait=ssCpuRawWait, memAvailReal=memAvailReal, mrTable=mrTable, logMatchFilename=logMatchFilename, mrIndex=mrIndex, fileErrorFlag=fileErrorFlag, logMatchName=logMatchName, systemStats=systemStats, memTotalRealTXT=memTotalRealTXT, dskAvailLow=dskAvailLow, Float=Float, logMatchRegExCompilation=logMatchRegExCompilation, extTable=extTable, prNames=prNames, prMin=prMin, memory=memory, dskErrorMsg=dskErrorMsg, laEntry=laEntry, ucdStart=ucdStart, ucdSnmpAgent=ucdSnmpAgent, dskPercentNode=dskPercentNode, logMatchGlobalCounter=logMatchGlobalCounter, logMatch=logMatch, dskTable=dskTable, memErrorName=memErrorName, laLoad=laLoad, prCount=prCount, win32=win32, fileSize=fileSize, bsdi=bsdi, dskTotalLow=dskTotalLow, unknown=unknown, hpux11=hpux11, memTotalFree=memTotalFree, dskPercent=dskPercent, ssCpuIdle=ssCpuIdle, ultrix=ultrix, memAvailSwap=memAvailSwap, ssSysInterrupts=ssSysInterrupts)