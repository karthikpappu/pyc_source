# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/IANA-LANGUAGE-MIB.py
# Compiled at: 2016-02-13 18:15:55
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, ValueRangeConstraint, ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'ValueRangeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ConstraintsIntersection')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(Integer32, mib_2, Counter64, IpAddress, TimeTicks, Counter32, Unsigned32, Bits, MibIdentifier, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, ModuleIdentity, ObjectIdentity, NotificationType) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'mib-2', 'Counter64', 'IpAddress', 'TimeTicks', 'Counter32', 'Unsigned32', 'Bits', 'MibIdentifier', 'iso', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'ModuleIdentity', 'ObjectIdentity', 'NotificationType')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
ianaLanguages = ModuleIdentity((1, 3, 6, 1, 2, 1, 73)).setRevisions(('2000-05-10 00:00',
                                                                     '1999-09-09 09:00'))
if mibBuilder.loadTexts:
    ianaLanguages.setLastUpdated('200005100000Z')
if mibBuilder.loadTexts:
    ianaLanguages.setOrganization('IANA')
if mibBuilder.loadTexts:
    ianaLanguages.setContactInfo('Internet Assigned Numbers Authority (IANA)\n\n            Postal: ICANN\n                    4676 Admiralty Way, Suite 330\n                    Marina del Rey, CA 90292\n\n            Tel:    +1 310 823 9358 x20\n            E-Mail: iana&iana.org')
if mibBuilder.loadTexts:
    ianaLanguages.setDescription("The MIB module registers object identifier values for\n            well-known programming and scripting languages. Every\n            language registration MUST describe the format used\n            when transferring scripts written in this language.\n\n            Any additions or changes to the contents of this MIB\n            module require Designated Expert Review as defined in\n            the Guidelines for Writing IANA Considerations Section\n            document. The Designated Expert will be selected by\n            the IESG Area Director of the OPS Area.\n\n            Note, this module does not have to register all possible\n            languages since languages are identified by object\n            identifier values. It is therefore possible to registered \n            languages in private OID trees. The references given below are not\n            normative with regard to the language version. Other\n            references might be better suited to describe some newer \n            versions of this language. The references are only\n            provided as `a pointer into the right direction'.")
ianaLangJavaByteCode = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 1))
if mibBuilder.loadTexts:
    ianaLangJavaByteCode.setDescription('Java byte code to be processed by a Java virtual machine.\n            A script written in Java byte code is transferred by using\n            the Java archive file format (JAR).')
ianaLangTcl = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 2))
if mibBuilder.loadTexts:
    ianaLangTcl.setDescription('The Tool Command Language (Tcl). A script written in the\n            Tcl language is transferred in Tcl source code format.')
ianaLangPerl = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 3))
if mibBuilder.loadTexts:
    ianaLangPerl.setDescription('The Perl language. A script written in the Perl language\n            is transferred in Perl source code format.')
ianaLangScheme = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 4))
if mibBuilder.loadTexts:
    ianaLangScheme.setDescription('The Scheme language. A script written in the Scheme\n            language is transferred in Scheme source code format.')
ianaLangSRSL = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 5))
if mibBuilder.loadTexts:
    ianaLangSRSL.setDescription('The SNMP Script Language defined by SNMP Research. A\n            script written in the SNMP Script Language is transferred\n            in the SNMP Script Language source code format.')
ianaLangPSL = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 6))
if mibBuilder.loadTexts:
    ianaLangPSL.setDescription('The Patrol Script Language defined by BMC Software. A script\n            written in the Patrol Script Language is transferred in the\n            Patrol Script Language source code format.')
ianaLangSMSL = ObjectIdentity((1, 3, 6, 1, 2, 1, 73, 7))
if mibBuilder.loadTexts:
    ianaLangSMSL.setDescription('The Systems Management Scripting Language. A script written\n            in the SMSL language is transferred in the SMSL source code\n            format.')
mibBuilder.exportSymbols('IANA-LANGUAGE-MIB', ianaLangScheme=ianaLangScheme, ianaLangJavaByteCode=ianaLangJavaByteCode, ianaLangPerl=ianaLangPerl, ianaLanguages=ianaLanguages, ianaLangTcl=ianaLangTcl, PYSNMP_MODULE_ID=ianaLanguages, ianaLangPSL=ianaLangPSL, ianaLangSMSL=ianaLangSMSL, ianaLangSRSL=ianaLangSRSL)