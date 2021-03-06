# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DNS-RESOLVER-MIB.py
# Compiled at: 2016-02-13 18:08:40
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ValueSizeConstraint, SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ValueSizeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection')
(DnsNameAsIndex, DnsTime, dns, DnsType, DnsOpCode, DnsClass, DnsName) = mibBuilder.importSymbols('DNS-SERVER-MIB', 'DnsNameAsIndex', 'DnsTime', 'dns', 'DnsType', 'DnsOpCode', 'DnsClass', 'DnsName')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(iso, IpAddress, Counter32, ObjectIdentity, Bits, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, NotificationType, Unsigned32, Integer32, Gauge32, ModuleIdentity, TimeTicks, MibIdentifier) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'IpAddress', 'Counter32', 'ObjectIdentity', 'Bits', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'NotificationType', 'Unsigned32', 'Integer32', 'Gauge32', 'ModuleIdentity', 'TimeTicks', 'MibIdentifier')
(TextualConvention, RowStatus, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'RowStatus', 'DisplayString')
dnsResMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 32, 2))
if mibBuilder.loadTexts:
    dnsResMIB.setLastUpdated('9401282250Z')
if mibBuilder.loadTexts:
    dnsResMIB.setOrganization('IETF DNS Working Group')
if mibBuilder.loadTexts:
    dnsResMIB.setContactInfo('       Rob Austein\n               Postal: Epilogue Technology Corporation\n                       268 Main Street, Suite 283\n                       North Reading, MA 10864\n                       US\n                  Tel: +1 617 245 0804\n                  Fax: +1 617 245 8122\n               E-Mail: sra@epilogue.com\n\n                       Jon Saperia\n               Postal: Digital Equipment Corporation\n                       110 Spit Brook Road\n                       ZKO1-3/H18\n                       Nashua, NH 03062-2698\n                       US\n                  Tel: +1 603 881 0480\n                  Fax: +1 603 881 0120\n               E-mail: saperia@zko.dec.com')
if mibBuilder.loadTexts:
    dnsResMIB.setDescription('The MIB module for entities implementing the client\n               (resolver) side of the Domain Name System (DNS)\n               protocol.')
dnsResMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1))
dnsResConfig = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1, 1))
dnsResCounter = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1, 2))
dnsResLameDelegation = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1, 3))
dnsResCache = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1, 4))
dnsResNCache = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1, 5))
dnsResOptCounter = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 1, 6))

class DnsQClass(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = '2d'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 65535)


class DnsQType(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = '2d'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 65535)


class DnsRespCode(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 15)


dnsResConfigImplementIdent = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 1), DisplayString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResConfigImplementIdent.setDescription("The implementation identification string for the\n               resolver software in use on the system, for example;\n               `RES-2.1'")
dnsResConfigService = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('recursiveOnly',
                                                                                                                                                                                     1), ('iterativeOnly',
                                                                                                                                                                                          2), ('recursiveAndIterative',
                                                                                                                                                                                               3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResConfigService.setDescription('Kind of DNS resolution service provided:\n\n               recursiveOnly(1) indicates a stub resolver.\n\n               iterativeOnly(2) indicates a normal full service\n               resolver.\n\n               recursiveAndIterative(3) indicates a full-service\n               resolver which performs a mix of recursive and iterative\n               queries.')
dnsResConfigMaxCnames = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResConfigMaxCnames.setDescription("Limit on how many CNAMEs the resolver should allow\n               before deciding that there's a CNAME loop.  Zero means\n               that resolver has no explicit CNAME limit.")
dnsResConfigSbeltTable = MibTable((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4))
if mibBuilder.loadTexts:
    dnsResConfigSbeltTable.setDescription("Table of safety belt information used by the resolver\n               when it hasn't got any better idea of where to send a\n               query, such as when the resolver is booting or is a stub\n               resolver.")
dnsResConfigSbeltEntry = MibTableRow((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1)).setIndexNames((0,
                                                                                           'DNS-RESOLVER-MIB',
                                                                                           'dnsResConfigSbeltAddr'), (0,
                                                                                                                      'DNS-RESOLVER-MIB',
                                                                                                                      'dnsResConfigSbeltSubTree'), (0,
                                                                                                                                                    'DNS-RESOLVER-MIB',
                                                                                                                                                    'dnsResConfigSbeltClass'))
if mibBuilder.loadTexts:
    dnsResConfigSbeltEntry.setDescription("An entry in the resolver's Sbelt table.\n               Rows may be created or deleted at any time by the DNS\n               resolver and by SNMP SET requests.  Whether the values\n               changed via SNMP are saved in stable storage across\n               `reset' operations is implementation-specific.")
dnsResConfigSbeltAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 1), IpAddress())
if mibBuilder.loadTexts:
    dnsResConfigSbeltAddr.setDescription('The IP address of the Sbelt name server identified by\n               this row of the table.')
dnsResConfigSbeltName = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 2), DnsName()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dnsResConfigSbeltName.setDescription('The DNS name of a Sbelt nameserver identified by this\n               row of the table.  A zero-length string indicates that\n               the name is not known by the resolver.')
dnsResConfigSbeltRecursion = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('iterative',
                                                                                                                                                                                                       1), ('recursive',
                                                                                                                                                                                                            2), ('recursiveAndIterative',
                                                                                                                                                                                                                 3)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dnsResConfigSbeltRecursion.setDescription('Kind of queries resolver will be sending to the name\n               server identified in this row of the table:\n\n               iterative(1) indicates that resolver will be directing\n               iterative queries to this name server (RD bit turned\n               off).\n\n               recursive(2) indicates that resolver will be directing\n               recursive queries to this name server (RD bit turned\n               on).\n\n               recursiveAndIterative(3) indicates that the resolver\n               will be directing both recursive and iterative queries\n               to the server identified in this row of the table.')
dnsResConfigSbeltPref = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dnsResConfigSbeltPref.setDescription('This value identifies the preference for the name server\n               identified in this row of the table.  The lower the\n               value, the more desirable the resolver considers this\n               server.')
dnsResConfigSbeltSubTree = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 5), DnsNameAsIndex())
if mibBuilder.loadTexts:
    dnsResConfigSbeltSubTree.setDescription('Queries sent to the name server identified by this row\n               of the table are limited to those for names in the name\n               subtree identified by this variable.  If no such\n               limitation applies, the value of this variable is the\n               name of the root domain (a DNS name consisting of a\n               single zero octet).')
dnsResConfigSbeltClass = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 6), DnsClass())
if mibBuilder.loadTexts:
    dnsResConfigSbeltClass.setDescription('The class of DNS queries that will be sent to the server\n               identified by this row of the table.')
dnsResConfigSbeltStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 4, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dnsResConfigSbeltStatus.setDescription('Row status column for this row of the Sbelt table.')
dnsResConfigUpTime = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 5), DnsTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResConfigUpTime.setDescription('If the resolver has a persistent state (e.g., a\n               process), this value will be the time elapsed since it\n               started.  For software without persistant state, this\n               value will be 0.')
dnsResConfigResetTime = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 6), DnsTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResConfigResetTime.setDescription("If the resolver has a persistent state (e.g., a process)\n               and supports a `reset' operation (e.g., can be told to\n               re-read configuration files), this value will be the\n               time elapsed since the last time the resolver was\n               `reset.'  For software that does not have persistence or\n               does not support a `reset' operation, this value will be\n               zero.")
dnsResConfigReset = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                      1), ('reset',
                                                                                                                                                                                           2), ('initializing',
                                                                                                                                                                                                3), ('running',
                                                                                                                                                                                                     4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResConfigReset.setDescription('Status/action object to reinitialize any persistant\n               resolver state.  When set to reset(2), any persistant\n               resolver state (such as a process) is reinitialized as if\n               the resolver had just been started.  This value will\n               never be returned by a read operation.  When read, one of\n               the following values will be returned:\n                   other(1) - resolver in some unknown state;\n                   initializing(3) - resolver (re)initializing;\n                   running(4) - resolver currently running.')
dnsResCounterByOpcodeTable = MibTable((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 3))
if mibBuilder.loadTexts:
    dnsResCounterByOpcodeTable.setDescription('Table of the current count of resolver queries and\n               answers.')
dnsResCounterByOpcodeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 3, 1)).setIndexNames((0,
                                                                                               'DNS-RESOLVER-MIB',
                                                                                               'dnsResCounterByOpcodeCode'))
if mibBuilder.loadTexts:
    dnsResCounterByOpcodeEntry.setDescription('Entry in the resolver counter table.  Entries are\n               indexed by DNS OpCode.')
dnsResCounterByOpcodeCode = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 3, 1, 1), DnsOpCode())
if mibBuilder.loadTexts:
    dnsResCounterByOpcodeCode.setDescription('The index to this table.  The OpCodes that have already\n               been defined are found in RFC-1035.')
dnsResCounterByOpcodeQueries = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 3, 1,
                                               2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterByOpcodeQueries.setDescription('Total number of queries that have sent out by the\n               resolver since initialization for the OpCode which is\n               the index to this row of the table.')
dnsResCounterByOpcodeResponses = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 3,
                                                 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterByOpcodeResponses.setDescription('Total number of responses that have been received by the\n               resolver since initialization for the OpCode which is\n               the index to this row of the table.')
dnsResCounterByRcodeTable = MibTable((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 4))
if mibBuilder.loadTexts:
    dnsResCounterByRcodeTable.setDescription('Table of the current count of responses to resolver\n               queries.')
dnsResCounterByRcodeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 4, 1)).setIndexNames((0,
                                                                                              'DNS-RESOLVER-MIB',
                                                                                              'dnsResCounterByRcodeCode'))
if mibBuilder.loadTexts:
    dnsResCounterByRcodeEntry.setDescription('Entry in the resolver response table.  Entries are\n               indexed by DNS response code.')
dnsResCounterByRcodeCode = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 4, 1, 1), DnsRespCode())
if mibBuilder.loadTexts:
    dnsResCounterByRcodeCode.setDescription('The index to this table.  The Response Codes that have\n               already been defined are found in RFC-1035.')
dnsResCounterByRcodeResponses = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 4, 1,
                                                2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterByRcodeResponses.setDescription('Number of responses the resolver has received for the\n               response code value which identifies this row of the\n               table.')
dnsResCounterNonAuthDataResps = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterNonAuthDataResps.setDescription('Number of requests made by the resolver for which a\n               non-authoritative answer (cached data) was received.')
dnsResCounterNonAuthNoDataResps = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterNonAuthNoDataResps.setDescription('Number of requests made by the resolver for which a\n               non-authoritative answer - no such data response (empty\n               answer) was received.')
dnsResCounterMartians = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterMartians.setDescription('Number of responses received which were received from\n               servers that the resolver does not think it asked.')
dnsResCounterRecdResponses = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterRecdResponses.setDescription('Number of responses received to all queries.')
dnsResCounterUnparseResps = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterUnparseResps.setDescription('Number of responses received which were unparseable.')
dnsResCounterFallbacks = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 2, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCounterFallbacks.setDescription('Number of times the resolver had to fall back to its\n               seat belt information.')
dnsResLameDelegationOverflows = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResLameDelegationOverflows.setDescription('Number of times the resolver attempted to add an entry\n               to the Lame Delegation table but was unable to for some\n               reason such as space constraints.')
dnsResLameDelegationTable = MibTable((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2))
if mibBuilder.loadTexts:
    dnsResLameDelegationTable.setDescription('Table of name servers returning lame delegations.\n\n               A lame delegation has occured when a parent zone\n               delegates authority for a child zone to a server that\n               appears not to think that it is authoritative for the\n               child zone in question.')
dnsResLameDelegationEntry = MibTableRow((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2, 1)).setIndexNames((0,
                                                                                              'DNS-RESOLVER-MIB',
                                                                                              'dnsResLameDelegationSource'), (0,
                                                                                                                              'DNS-RESOLVER-MIB',
                                                                                                                              'dnsResLameDelegationName'), (0,
                                                                                                                                                            'DNS-RESOLVER-MIB',
                                                                                                                                                            'dnsResLameDelegationClass'))
if mibBuilder.loadTexts:
    dnsResLameDelegationEntry.setDescription('Entry in lame delegation table.  Only the resolver may\n               create rows in this table.  SNMP SET requests may be used\n               to delete rows.')
dnsResLameDelegationSource = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2, 1, 1), IpAddress())
if mibBuilder.loadTexts:
    dnsResLameDelegationSource.setDescription('Source of lame delegation.')
dnsResLameDelegationName = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2, 1, 2), DnsNameAsIndex())
if mibBuilder.loadTexts:
    dnsResLameDelegationName.setDescription('DNS name for which lame delegation was received.')
dnsResLameDelegationClass = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2, 1, 3), DnsClass())
if mibBuilder.loadTexts:
    dnsResLameDelegationClass.setDescription('DNS class of received lame delegation.')
dnsResLameDelegationCounts = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResLameDelegationCounts.setDescription('How many times this lame delegation has been received.')
dnsResLameDelegationStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 3, 2, 1, 5), RowStatus()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResLameDelegationStatus.setDescription('Status column for the lame delegation table.  Since only\n               the agent (DNS resolver) creates rows in this table, the\n               only values that a manager may write to this variable\n               are active(1) and destroy(6).')
dnsResCacheStatus = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                   1), ('disabled',
                                                                                                                                                                                        2), ('clear',
                                                                                                                                                                                             3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResCacheStatus.setDescription("Status/action for the resolver's cache.\n\n               enabled(1) means that the use of the cache is allowed.\n               Query operations can return this state.\n\n               disabled(2) means that the cache is not being used.\n               Query operations can return this state.\n\n               Setting this variable to clear(3) deletes the entire\n               contents of the resolver's cache, but does not otherwise\n               change the resolver's state.  The status will retain its\n               previous value from before the clear operation (i.e.,\n               enabled(1) or disabled(2)).  The value of clear(3) can\n               NOT be returned by a query operation.")
dnsResCacheMaxTTL = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 2), DnsTime()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResCacheMaxTTL.setDescription('Maximum Time-To-Live for RRs in this cache.  If the\n               resolver does not implement a TTL ceiling, the value of\n               this field should be zero.')
dnsResCacheGoodCaches = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheGoodCaches.setDescription('Number of RRs the resolver has cached successfully.')
dnsResCacheBadCaches = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheBadCaches.setDescription("Number of RRs the resolver has refused to cache because\n               they appear to be dangerous or irrelevant.  E.g., RRs\n               with suspiciously high TTLs, unsolicited root\n               information, or that just don't appear to be relevant to\n               the question the resolver asked.")
dnsResCacheRRTable = MibTable((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5))
if mibBuilder.loadTexts:
    dnsResCacheRRTable.setDescription("This table contains information about all the resource\n               records currently in the resolver's cache.")
dnsResCacheRREntry = MibTableRow((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1)).setIndexNames((0,
                                                                                       'DNS-RESOLVER-MIB',
                                                                                       'dnsResCacheRRName'), (0,
                                                                                                              'DNS-RESOLVER-MIB',
                                                                                                              'dnsResCacheRRClass'), (0,
                                                                                                                                      'DNS-RESOLVER-MIB',
                                                                                                                                      'dnsResCacheRRType'), (0,
                                                                                                                                                             'DNS-RESOLVER-MIB',
                                                                                                                                                             'dnsResCacheRRIndex'))
if mibBuilder.loadTexts:
    dnsResCacheRREntry.setDescription("An entry in the resolvers's cache.  Rows may be created\n               only by the resolver.  SNMP SET requests may be used to\n               delete rows.")
dnsResCacheRRName = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 1), DnsNameAsIndex())
if mibBuilder.loadTexts:
    dnsResCacheRRName.setDescription('Owner name of the Resource Record in the cache which is\n               identified in this row of the table.  As described in\n               RFC-1034, the owner of the record is the domain name\n               were the RR is found.')
dnsResCacheRRClass = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 2), DnsClass())
if mibBuilder.loadTexts:
    dnsResCacheRRClass.setDescription('DNS class of the Resource Record in the cache which is\n               identified in this row of the table.')
dnsResCacheRRType = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 3), DnsType())
if mibBuilder.loadTexts:
    dnsResCacheRRType.setDescription('DNS type of the Resource Record in the cache which is\n               identified in this row of the table.')
dnsResCacheRRTTL = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 4), DnsTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheRRTTL.setDescription('Time-To-Live of RR in DNS cache.  This is the initial\n               TTL value which was received with the RR when it was\n               originally received.')
dnsResCacheRRElapsedTTL = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 5), DnsTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheRRElapsedTTL.setDescription('Elapsed seconds since RR was received.')
dnsResCacheRRSource = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 6), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheRRSource.setDescription('Host from which RR was received, 0.0.0.0 if unknown.')
dnsResCacheRRData = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 7), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheRRData.setDescription('RDATA portion of a cached RR.  The value is in the\n               format defined for the particular DNS class and type of\n               the resource record.')
dnsResCacheRRStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 8), RowStatus()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResCacheRRStatus.setDescription('Status column for the resolver cache table.  Since only\n               the agent (DNS resolver) creates rows in this table, the\n               only values that a manager may write to this variable\n               are active(1) and destroy(6).')
dnsResCacheRRIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 9), Integer32())
if mibBuilder.loadTexts:
    dnsResCacheRRIndex.setDescription('A value which makes entries in the table unique when the\n               other index values (dnsResCacheRRName,\n               dnsResCacheRRClass, and dnsResCacheRRType) do not\n               provide a unique index.')
dnsResCacheRRPrettyName = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 4, 5, 1, 10), DnsName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResCacheRRPrettyName.setDescription('Name of the RR at this row in the table.  This is\n               identical to the dnsResCacheRRName variable, except that\n               character case is preserved in this variable, per DNS\n               conventions.')
dnsResNCacheStatus = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                    1), ('disabled',
                                                                                                                                                                                         2), ('clear',
                                                                                                                                                                                              3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResNCacheStatus.setDescription("Status/action for the resolver's negative response\n               cache.\n\n               enabled(1) means that the use of the negative response\n               cache is allowed.  Query operations can return this\n               state.\n\n               disabled(2) means that the negative response cache is\n               not being used.  Query operations can return this state.\n\n               Setting this variable to clear(3) deletes the entire\n               contents of the resolver's negative response cache.  The\n               status will retain its previous value from before the\n               clear operation (i.e., enabled(1) or disabled(2)).  The\n               value of clear(3) can NOT be returned by a query\n               operation.")
dnsResNCacheMaxTTL = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 2), DnsTime()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResNCacheMaxTTL.setDescription('Maximum Time-To-Live for cached authoritative errors.\n               If the resolver does not implement a TTL ceiling, the\n               value of this field should be zero.')
dnsResNCacheGoodNCaches = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheGoodNCaches.setDescription('Number of authoritative errors the resolver has cached\n               successfully.')
dnsResNCacheBadNCaches = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheBadNCaches.setDescription('Number of authoritative errors the resolver would have\n               liked to cache but was unable to because the appropriate\n               SOA RR was not supplied or looked suspicious.')
dnsResNCacheErrTable = MibTable((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5))
if mibBuilder.loadTexts:
    dnsResNCacheErrTable.setDescription("The resolver's negative response cache.  This table\n               contains information about authoritative errors that\n               have been cached by the resolver.")
dnsResNCacheErrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1)).setIndexNames((0,
                                                                                         'DNS-RESOLVER-MIB',
                                                                                         'dnsResNCacheErrQName'), (0,
                                                                                                                   'DNS-RESOLVER-MIB',
                                                                                                                   'dnsResNCacheErrQClass'), (0,
                                                                                                                                              'DNS-RESOLVER-MIB',
                                                                                                                                              'dnsResNCacheErrQType'), (0,
                                                                                                                                                                        'DNS-RESOLVER-MIB',
                                                                                                                                                                        'dnsResNCacheErrIndex'))
if mibBuilder.loadTexts:
    dnsResNCacheErrEntry.setDescription("An entry in the resolver's negative response cache\n               table.  Only the resolver can create rows.  SNMP SET\n               requests may be used to delete rows.")
dnsResNCacheErrQName = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 1), DnsNameAsIndex())
if mibBuilder.loadTexts:
    dnsResNCacheErrQName.setDescription('QNAME associated with a cached authoritative error.')
dnsResNCacheErrQClass = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 2), DnsQClass())
if mibBuilder.loadTexts:
    dnsResNCacheErrQClass.setDescription('DNS QCLASS associated with a cached authoritative\n               error.')
dnsResNCacheErrQType = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 3), DnsQType())
if mibBuilder.loadTexts:
    dnsResNCacheErrQType.setDescription('DNS QTYPE associated with a cached authoritative error.')
dnsResNCacheErrTTL = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 4), DnsTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheErrTTL.setDescription('Time-To-Live of a cached authoritative error at the time\n               of the error, it should not be decremented by the number\n               of seconds since it was received.  This should be the\n               TTL as copied from the MINIMUM field of the SOA that\n               accompanied the authoritative error, or a smaller value\n               if the resolver implements a ceiling on negative\n               response cache TTLs.')
dnsResNCacheErrElapsedTTL = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 5), DnsTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheErrElapsedTTL.setDescription('Elapsed seconds since authoritative error was received.')
dnsResNCacheErrSource = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 6), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheErrSource.setDescription('Host which sent the authoritative error, 0.0.0.0 if\n               unknown.')
dnsResNCacheErrCode = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('nonexistantName',
                                                                                                                                                                                                1), ('noData',
                                                                                                                                                                                                     2), ('other',
                                                                                                                                                                                                          3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheErrCode.setDescription('The authoritative error that has been cached:\n\n               nonexistantName(1) indicates an authoritative name error\n               (RCODE = 3).\n\n               noData(2) indicates an authoritative response with no\n               error (RCODE = 0) and no relevant data.\n\n               other(3) indicates some other cached authoritative\n               error.  At present, no such errors are known to exist.')
dnsResNCacheErrStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 8), RowStatus()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dnsResNCacheErrStatus.setDescription('Status column for the resolver negative response cache\n               table.  Since only the agent (DNS resolver) creates rows\n               in this table, the only values that a manager may write\n               to this variable are active(1) and destroy(6).')
dnsResNCacheErrIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 9), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheErrIndex.setDescription('A value which makes entries in the table unique when the\n               other index values (dnsResNCacheErrQName,\n               dnsResNCacheErrQClass, and dnsResNCacheErrQType) do not\n               provide a unique index.')
dnsResNCacheErrPrettyName = MibTableColumn((1, 3, 6, 1, 2, 1, 32, 2, 1, 5, 5, 1, 10), DnsName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResNCacheErrPrettyName.setDescription('QNAME associated with this row in the table.  This is\n               identical to the dnsResNCacheErrQName variable, except\n               that character case is preserved in this variable, per\n               DNS conventions.')
dnsResOptCounterReferals = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 6, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResOptCounterReferals.setDescription('Number of responses which were received from servers\n               redirecting query to another server.')
dnsResOptCounterRetrans = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 6, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResOptCounterRetrans.setDescription('Number requests retransmitted for all reasons.')
dnsResOptCounterNoResponses = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 6, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResOptCounterNoResponses.setDescription('Number of queries that were retransmitted because of no\n               response.')
dnsResOptCounterRootRetrans = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 6, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResOptCounterRootRetrans.setDescription('Number of queries that were retransmitted that were to\n               root servers.')
dnsResOptCounterInternals = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 6, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResOptCounterInternals.setDescription('Number of requests internally generated by the\n               resolver.')
dnsResOptCounterInternalTimeOuts = MibScalar((1, 3, 6, 1, 2, 1, 32, 2, 1, 6, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dnsResOptCounterInternalTimeOuts.setDescription('Number of requests internally generated which timed\n               out.')
dnsResMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 2))
dnsResConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 32, 2, 2, 1)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResConfigImplementIdent'), ('DNS-RESOLVER-MIB', 'dnsResConfigService'), ('DNS-RESOLVER-MIB', 'dnsResConfigMaxCnames'), ('DNS-RESOLVER-MIB', 'dnsResConfigSbeltName'), ('DNS-RESOLVER-MIB', 'dnsResConfigSbeltRecursion'), ('DNS-RESOLVER-MIB', 'dnsResConfigSbeltPref'), ('DNS-RESOLVER-MIB', 'dnsResConfigSbeltStatus'), ('DNS-RESOLVER-MIB', 'dnsResConfigUpTime'), ('DNS-RESOLVER-MIB', 'dnsResConfigResetTime'), ('DNS-RESOLVER-MIB', 'dnsResConfigReset')))
if mibBuilder.loadTexts:
    dnsResConfigGroup.setDescription('A collection of objects providing basic configuration\n               information for a DNS resolver implementation.')
dnsResCounterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 32, 2, 2, 2)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResCounterByOpcodeQueries'), ('DNS-RESOLVER-MIB', 'dnsResCounterByOpcodeResponses'), ('DNS-RESOLVER-MIB', 'dnsResCounterByRcodeResponses'), ('DNS-RESOLVER-MIB', 'dnsResCounterNonAuthDataResps'), ('DNS-RESOLVER-MIB', 'dnsResCounterNonAuthNoDataResps'), ('DNS-RESOLVER-MIB', 'dnsResCounterMartians'), ('DNS-RESOLVER-MIB', 'dnsResCounterRecdResponses'), ('DNS-RESOLVER-MIB', 'dnsResCounterUnparseResps'), ('DNS-RESOLVER-MIB', 'dnsResCounterFallbacks')))
if mibBuilder.loadTexts:
    dnsResCounterGroup.setDescription('A collection of objects providing basic instrumentation\n               of a DNS resolver implementation.')
dnsResLameDelegationGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 32, 2, 2, 3)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResLameDelegationOverflows'), ('DNS-RESOLVER-MIB', 'dnsResLameDelegationCounts'), ('DNS-RESOLVER-MIB', 'dnsResLameDelegationStatus')))
if mibBuilder.loadTexts:
    dnsResLameDelegationGroup.setDescription("A collection of objects providing instrumentation of\n               `lame delegation' failures.")
dnsResCacheGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 32, 2, 2, 4)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResCacheStatus'), ('DNS-RESOLVER-MIB', 'dnsResCacheMaxTTL'), ('DNS-RESOLVER-MIB', 'dnsResCacheGoodCaches'), ('DNS-RESOLVER-MIB', 'dnsResCacheBadCaches'), ('DNS-RESOLVER-MIB', 'dnsResCacheRRTTL'), ('DNS-RESOLVER-MIB', 'dnsResCacheRRElapsedTTL'), ('DNS-RESOLVER-MIB', 'dnsResCacheRRSource'), ('DNS-RESOLVER-MIB', 'dnsResCacheRRData'), ('DNS-RESOLVER-MIB', 'dnsResCacheRRStatus'), ('DNS-RESOLVER-MIB', 'dnsResCacheRRPrettyName')))
if mibBuilder.loadTexts:
    dnsResCacheGroup.setDescription("A collection of objects providing access to and control\n               of a DNS resolver's cache.")
dnsResNCacheGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 32, 2, 2, 5)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResNCacheStatus'), ('DNS-RESOLVER-MIB', 'dnsResNCacheMaxTTL'), ('DNS-RESOLVER-MIB', 'dnsResNCacheGoodNCaches'), ('DNS-RESOLVER-MIB', 'dnsResNCacheBadNCaches'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrTTL'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrElapsedTTL'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrSource'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrCode'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrStatus'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrIndex'), ('DNS-RESOLVER-MIB', 'dnsResNCacheErrPrettyName')))
if mibBuilder.loadTexts:
    dnsResNCacheGroup.setDescription("A collection of objects providing access to and control\n               of a DNS resolver's negative response cache.")
dnsResOptCounterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 32, 2, 2, 6)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResOptCounterReferals'), ('DNS-RESOLVER-MIB', 'dnsResOptCounterRetrans'), ('DNS-RESOLVER-MIB', 'dnsResOptCounterNoResponses'), ('DNS-RESOLVER-MIB', 'dnsResOptCounterRootRetrans'), ('DNS-RESOLVER-MIB', 'dnsResOptCounterInternals'), ('DNS-RESOLVER-MIB', 'dnsResOptCounterInternalTimeOuts')))
if mibBuilder.loadTexts:
    dnsResOptCounterGroup.setDescription('A collection of objects providing further\n               instrumentation applicable to many but not all DNS\n               resolvers.')
dnsResMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 32, 2, 3))
dnsResMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 32, 2, 3, 1)).setObjects(*(('DNS-RESOLVER-MIB', 'dnsResConfigGroup'), ('DNS-RESOLVER-MIB', 'dnsResCounterGroup'), ('DNS-RESOLVER-MIB', 'dnsResCacheGroup'), ('DNS-RESOLVER-MIB', 'dnsResNCacheGroup'), ('DNS-RESOLVER-MIB', 'dnsResLameDelegationGroup'), ('DNS-RESOLVER-MIB', 'dnsResOptCounterGroup')))
if mibBuilder.loadTexts:
    dnsResMIBCompliance.setDescription('The compliance statement for agents implementing the DNS\n               resolver MIB extensions.')
mibBuilder.exportSymbols('DNS-RESOLVER-MIB', dnsResNCacheErrStatus=dnsResNCacheErrStatus, dnsResCounterByOpcodeCode=dnsResCounterByOpcodeCode, dnsResCacheBadCaches=dnsResCacheBadCaches, dnsResLameDelegationStatus=dnsResLameDelegationStatus, dnsResConfigSbeltStatus=dnsResConfigSbeltStatus, dnsResNCacheErrTTL=dnsResNCacheErrTTL, dnsResOptCounterInternalTimeOuts=dnsResOptCounterInternalTimeOuts, dnsResCounterMartians=dnsResCounterMartians, dnsResCacheRRSource=dnsResCacheRRSource, dnsResNCacheStatus=dnsResNCacheStatus, dnsResCounter=dnsResCounter, dnsResConfigSbeltAddr=dnsResConfigSbeltAddr, dnsResConfigImplementIdent=dnsResConfigImplementIdent, dnsResOptCounterRetrans=dnsResOptCounterRetrans, dnsResConfigService=dnsResConfigService, dnsResCounterByRcodeEntry=dnsResCounterByRcodeEntry, dnsResNCacheErrQClass=dnsResNCacheErrQClass, dnsResNCacheGroup=dnsResNCacheGroup, dnsResNCacheErrQType=dnsResNCacheErrQType, dnsResLameDelegationGroup=dnsResLameDelegationGroup, dnsResCounterByRcodeCode=dnsResCounterByRcodeCode, dnsResMIB=dnsResMIB, dnsResCacheRRTTL=dnsResCacheRRTTL, dnsResNCacheMaxTTL=dnsResNCacheMaxTTL, dnsResOptCounterRootRetrans=dnsResOptCounterRootRetrans, dnsResOptCounterGroup=dnsResOptCounterGroup, dnsResNCacheErrQName=dnsResNCacheErrQName, dnsResLameDelegationSource=dnsResLameDelegationSource, dnsResCounterFallbacks=dnsResCounterFallbacks, dnsResConfigSbeltEntry=dnsResConfigSbeltEntry, dnsResCacheRRType=dnsResCacheRRType, dnsResConfigResetTime=dnsResConfigResetTime, dnsResCacheRRName=dnsResCacheRRName, dnsResConfigMaxCnames=dnsResConfigMaxCnames, dnsResCache=dnsResCache, dnsResCounterByRcodeResponses=dnsResCounterByRcodeResponses, dnsResLameDelegationName=dnsResLameDelegationName, dnsResLameDelegationEntry=dnsResLameDelegationEntry, PYSNMP_MODULE_ID=dnsResMIB, dnsResCounterGroup=dnsResCounterGroup, dnsResCounterByOpcodeQueries=dnsResCounterByOpcodeQueries, dnsResLameDelegationTable=dnsResLameDelegationTable, dnsResConfigSbeltSubTree=dnsResConfigSbeltSubTree, dnsResCacheMaxTTL=dnsResCacheMaxTTL, DnsQClass=DnsQClass, dnsResCacheRREntry=dnsResCacheRREntry, dnsResCounterNonAuthNoDataResps=dnsResCounterNonAuthNoDataResps, dnsResMIBCompliance=dnsResMIBCompliance, dnsResNCacheErrCode=dnsResNCacheErrCode, dnsResNCacheErrIndex=dnsResNCacheErrIndex, dnsResMIBCompliances=dnsResMIBCompliances, dnsResCounterByOpcodeResponses=dnsResCounterByOpcodeResponses, dnsResCacheGroup=dnsResCacheGroup, dnsResCacheRRStatus=dnsResCacheRRStatus, dnsResConfigSbeltClass=dnsResConfigSbeltClass, dnsResConfigUpTime=dnsResConfigUpTime, dnsResCounterRecdResponses=dnsResCounterRecdResponses, dnsResCounterByOpcodeEntry=dnsResCounterByOpcodeEntry, dnsResCounterByRcodeTable=dnsResCounterByRcodeTable, dnsResCacheRRData=dnsResCacheRRData, dnsResConfigSbeltName=dnsResConfigSbeltName, dnsResNCacheErrTable=dnsResNCacheErrTable, dnsResConfigGroup=dnsResConfigGroup, dnsResCacheRRClass=dnsResCacheRRClass, DnsQType=DnsQType, dnsResMIBGroups=dnsResMIBGroups, dnsResConfig=dnsResConfig, DnsRespCode=DnsRespCode, dnsResLameDelegation=dnsResLameDelegation, dnsResNCacheGoodNCaches=dnsResNCacheGoodNCaches, dnsResCacheRRIndex=dnsResCacheRRIndex, dnsResCacheRRPrettyName=dnsResCacheRRPrettyName, dnsResCacheRRElapsedTTL=dnsResCacheRRElapsedTTL, dnsResNCache=dnsResNCache, dnsResCacheGoodCaches=dnsResCacheGoodCaches, dnsResOptCounterNoResponses=dnsResOptCounterNoResponses, dnsResCacheStatus=dnsResCacheStatus, dnsResNCacheBadNCaches=dnsResNCacheBadNCaches, dnsResOptCounterInternals=dnsResOptCounterInternals, dnsResMIBObjects=dnsResMIBObjects, dnsResLameDelegationOverflows=dnsResLameDelegationOverflows, dnsResConfigSbeltRecursion=dnsResConfigSbeltRecursion, dnsResConfigReset=dnsResConfigReset, dnsResCacheRRTable=dnsResCacheRRTable, dnsResOptCounterReferals=dnsResOptCounterReferals, dnsResConfigSbeltTable=dnsResConfigSbeltTable, dnsResNCacheErrPrettyName=dnsResNCacheErrPrettyName, dnsResNCacheErrEntry=dnsResNCacheErrEntry, dnsResLameDelegationClass=dnsResLameDelegationClass, dnsResConfigSbeltPref=dnsResConfigSbeltPref, dnsResLameDelegationCounts=dnsResLameDelegationCounts, dnsResNCacheErrElapsedTTL=dnsResNCacheErrElapsedTTL, dnsResCounterUnparseResps=dnsResCounterUnparseResps, dnsResNCacheErrSource=dnsResNCacheErrSource, dnsResOptCounter=dnsResOptCounter, dnsResCounterByOpcodeTable=dnsResCounterByOpcodeTable, dnsResCounterNonAuthDataResps=dnsResCounterNonAuthDataResps)