# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DOCS-IETF-BPI2-MIB.py
# Compiled at: 2016-02-13 18:09:31
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ValueSizeConstraint, SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ValueSizeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection')
(ifIndex,) = mibBuilder.importSymbols('IF-MIB', 'ifIndex')
(InetAddress, InetAddressType) = mibBuilder.importSymbols('INET-ADDRESS-MIB', 'InetAddress', 'InetAddressType')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ModuleCompliance, ObjectGroup, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'ObjectGroup', 'NotificationGroup')
(Counter32, MibIdentifier, TimeTicks, NotificationType, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, iso, mib_2, IpAddress, Unsigned32, Counter64, Integer32, Bits, ObjectIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'Counter32', 'MibIdentifier', 'TimeTicks', 'NotificationType', 'ModuleIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'iso', 'mib-2', 'IpAddress', 'Unsigned32', 'Counter64', 'Integer32', 'Bits', 'ObjectIdentity')
(DateAndTime, TruthValue, StorageType, DisplayString, MacAddress, RowStatus, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DateAndTime', 'TruthValue', 'StorageType', 'DisplayString', 'MacAddress', 'RowStatus', 'TextualConvention')
docsIetfBpi2MIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 9999)).setRevisions(('2004-09-07 17:00',))
if mibBuilder.loadTexts:
    docsIetfBpi2MIB.setLastUpdated('200409071700Z')
if mibBuilder.loadTexts:
    docsIetfBpi2MIB.setOrganization('IETF IP over Cable Data Network (IPCDN)\n                          Working Group')
if mibBuilder.loadTexts:
    docsIetfBpi2MIB.setContactInfo('---------------------------------------\n                       Stuart M. Green\n                       Postal:\n                       ADC Telecommunications, Inc.\n                       Mailstop 1641\n                       8 Technology Drive\n                       Westborough, MA  01581\n                       U.S.A.\n                       Tel:    +1 508 870 2554\n                       E-mail: stuart.green@adc.com\n                       ---------------------------------------\n                       Kaz Ozawa\n                       Cable Modem & Network Dept.\n                       Server & Network Div.\n                       TOSHIBA CORPORATION\n                       Digital Media Network Company\n                       1-1, Shibaura 1-Chome\n                       Minato-ku, Tokyo 105-8001\n                       Japan\n                       Phone: +81-3-3457-2726\n                       FAX: +81-3-5444-9359\n                       Email: Kazuyoshi.Ozawa@toshiba.co.jp\n                       ---------------------------------------\n                       Alexander Katsnelson\n                       Postal:\n                       Cable Television Laboratories, Inc.\n                       858 Coal Creek Circle\n                       Louisville, CO 80027- 9750\n                       U.S.A.\n                       Tel:    +1 303 661 9100\n                       Fax:    +1 303 661 9199\n                       E-mail: a.katsnelson@cablelabs.com\n                       ---------------------------------------\n                       Eduardo Cardona\n                       Postal:\n                       Cable Television Laboratories, Inc.\n                       858 Coal Creek Circle\n                       Louisville, CO 80027- 9750\n                       U.S.A.\n                       Tel:    +1 303 661 9100\n                       Fax:    +1 303 661 9199\n                       E-mail: e.cardona@cablelabs.com\n                       ---------------------------------------\n\n               IETF IPCDN Working Group\n               General Discussion: ipcdn@ietf.org\n               Subscribe: http://www.ietf.org/mailman/listinfo/ipcdn.\n               Archive: ftp://ftp.ietf.org/ietf-mail-archive/ipcdn.\n               Co-chairs: Richard Woundy, rwoundy@cisco.com\n                          Jean-Francois Mule, jfm@cablelabs.com')
if mibBuilder.loadTexts:
    docsIetfBpi2MIB.setDescription('This is the MIB module for the DOCSIS Baseline\n                 Privacy Plus Interface (BPI+) at cable modems (CMs)\n                 and cable modem termination systems (CMTSs).\n\n                 Copyright (C) The Internet Society (2004). This\n                 version of this MIB module is part of RFC XXXX; see\n                 the RFC itself for full legal notices.')

class DocsX509ASN1DEREncodedCertificate(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 4096)


class DocsSAId(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(1, 16383)


class DocsSAIdOrZero(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ConstraintsUnion(ValueRangeConstraint(0, 0), ValueRangeConstraint(1, 16383))


class DocsBpkmSAType(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3))
    namedValues = NamedValues(('none', 0), ('primary', 1), ('static', 2), ('dynamic',
                                                                           3))


class DocsBpkmDataEncryptAlg(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5))
    namedValues = NamedValues(('none', 0), ('des56CbcMode', 1), ('des40CbcMode', 2), ('t3Des128CbcMode',
                                                                                      3), ('aes128CbcMode',
                                                                                           4), ('aes256CbcMode',
                                                                                                5))


class DocsBpkmDataAuthentAlg(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(0, 1))
    namedValues = NamedValues(('none', 0), ('hmacSha196', 1))


docsIetfBpi2MIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1))
docsIetfBpi2CmObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 1))
docsIetfBpi2CmBaseTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1))
if mibBuilder.loadTexts:
    docsIetfBpi2CmBaseTable.setDescription('This table describes the basic and authorization\n            related Baseline Privacy Plus attributes of each CM MAC\n            interface.')
docsIetfBpi2CmBaseEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmBaseEntry.setDescription('Each entry contains objects describing attributes of\n            one CM MAC interface. An entry in this table exists for\n            each ifEntry with an ifType of docsCableMaclayer(127).')
docsIetfBpi2CmPrivacyEnable = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 1), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmPrivacyEnable.setDescription('This object identifies whether this CM is\n            provisioned to run Baseline Privacy Plus.')
docsIetfBpi2CmPublicKey = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 524))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmPublicKey.setDescription('The value of this object is a DER-encoded\n            RSAPublicKey ASN.1 type string, as defined in the RSA\n            Encryption Standard (PKCS #1), corresponding to the\n            public key of the CM.')
docsIetfBpi2CmAuthState = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('start', 1), ('authWait', 2), ('authorized', 3), ('reauthWait', 4), ('authRejectWait', 5), ('silent', 6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthState.setDescription('The value of this object is the state of the CM\n            authorization FSM.  The start state indicates that FSM is\n            in its initial state.')
docsIetfBpi2CmAuthKeySequenceNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthKeySequenceNumber.setDescription('The value of this object is the most recent\n            authorization key sequence number for this FSM.')
docsIetfBpi2CmAuthExpiresOld = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 5), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthExpiresOld.setDescription('The value of this object is the actual clock time for\n            expiration of the immediate predecessor of the most recent\n            authorization key for this FSM.  If this FSM has only one\n            authorization key, then the value is the time of activation\n            of this FSM.')
docsIetfBpi2CmAuthExpiresNew = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 6), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthExpiresNew.setDescription('The value of this object is the actual clock time for\n            expiration of the most recent authorization key for this\n            FSM.')
docsIetfBpi2CmAuthReset = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 7), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthReset.setDescription("Setting this object to 'true' generates a Reauthorize\n            event in the authorization FSM. Reading this object always\n            returns FALSE.\n            This object is for testing purposes only and therefore it\n            does not require to be associated with a last reset\n            object.")
docsIetfBpi2CmAuthGraceTime = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 6047999))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthGraceTime.setDescription('The value of this object is the grace time for an\n            authorization key in seconds.  A CM is expected to start\n            trying to get a new authorization key beginning\n            AuthGraceTime seconds before the most recent authorization\n            key actually expires.')
docsIetfBpi2CmTEKGraceTime = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 302399))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKGraceTime.setDescription('The value of this object is the grace time for\n            the TEK in seconds.  The CM is expected to start trying to\n            acquire a new TEK beginning TEK GraceTime seconds before\n            the expiration of the most recent TEK.')
docsIetfBpi2CmAuthWaitTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 30))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthWaitTimeout.setDescription('The value of this object is the Authorize Wait\n            Timeout in second.')
docsIetfBpi2CmReauthWaitTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 30))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmReauthWaitTimeout.setDescription('The value of this object is the Reauthorize Wait\n            Timeout in seconds.')
docsIetfBpi2CmOpWaitTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 10))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmOpWaitTimeout.setDescription('The value of this object is the Operational Wait\n            Timeout in seconds.')
docsIetfBpi2CmRekeyWaitTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 10))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmRekeyWaitTimeout.setDescription('The value of this object is the Rekey Wait Timeout\n            in seconds.')
docsIetfBpi2CmAuthRejectWaitTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 600))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthRejectWaitTimeout.setDescription('The value of this object is the Authorization Reject\n            Wait Timeout in seconds.')
docsIetfBpi2CmSAMapWaitTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 10))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmSAMapWaitTimeout.setDescription('The value of this object is the retransmission\n            interval, in seconds, of SA Map Requests from the MAP Wait\n            state.')
docsIetfBpi2CmSAMapMaxRetries = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 10))).setUnits('count').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmSAMapMaxRetries.setDescription('The value of this object is the maximum number of\n            Map Request retries allowed.')
docsIetfBpi2CmAuthentInfos = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthentInfos.setDescription('The value of this object is the count of times the CM\n            has transmitted an Authentication Information message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmAuthRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 18), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthRequests.setDescription('The value of this object is the count of times the CM\n            has transmitted an Authorization Request message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmAuthReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 19), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthReplies.setDescription('The value of this object is the count of times the CM\n            has received an Authorization Reply message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmAuthRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 20), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthRejects.setDescription('The value of this object is the count of times the CM\n            has received an Authorization Reject message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmAuthInvalids = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 21), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthInvalids.setDescription('The value of this object is the count of times the CM\n            has received an Authorization Invalid message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmAuthRejectErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 22), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 8, 11))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('unauthorizedCm', 3), ('unauthorizedSaid', 4), ('permanentAuthorizationFailure', 8), ('timeOfDayNotAcquired', 11)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthRejectErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in most recent Authorization\n            Reject message received by the CM.  This has value\n            unknown(2) if the last Error-Code value was 0, and none(1)\n            if no Authorization Reject message has been received since\n            reboot.')
docsIetfBpi2CmAuthRejectErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 23), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthRejectErrorString.setDescription('The value of this object is the text string in\n            most recent Authorization Reject message received by the\n            CM.  This is a zero length string if no Authorization\n            Reject message has been received since reboot.')
docsIetfBpi2CmAuthInvalidErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 24), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 5, 6, 7))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('unauthorizedCm', 3), ('unsolicited', 5), ('invalidKeySequence', 6), ('keyRequestAuthenticationFailure', 7)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthInvalidErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in most recent Authorization\n            Invalid message received by the CM.  This has value\n            unknown(2) if the last Error-Code value was 0, and none(1)\n            if no Authorization Invalid message has been received since\n            reboot.')
docsIetfBpi2CmAuthInvalidErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 1, 1, 25), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmAuthInvalidErrorString.setDescription('The value of this object is the text string in\n            most recent Authorization Invalid message received by the\n            CM. This is a zero length string if no Authorization\n            Invalid message has been received since reboot.')
docsIetfBpi2CmTEKTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2))
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKTable.setDescription('This table describes the attributes of each CM\n            Traffic Encryption Key (TEK) association. The CM maintains\n            (no more than) one TEK association per SAID per CM MAC\n            interface.')
docsIetfBpi2CmTEKEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKSAId'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKEntry.setDescription('Each entry contains objects describing the TEK\n            association attributes of one SAID. The CM MUST create one\n            entry per SAID, regardless of whether the SAID was obtained\n            from a Registration Response message, from an Authorization\n            Reply message, or from any dynamic SAID establishment\n            mechanisms.')
docsIetfBpi2CmTEKSAId = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 1), DocsSAId())
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKSAId.setDescription('The value of this object is the DOCSIS Security\n            Association ID (SAID).')
docsIetfBpi2CmTEKSAType = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 2), DocsBpkmSAType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKSAType.setDescription('The value of this object is the type of security\n            association.')
docsIetfBpi2CmTEKDataEncryptAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 3), DocsBpkmDataEncryptAlg()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKDataEncryptAlg.setDescription('The value of this object is the data encryption\n            algorithm for this SAID.')
docsIetfBpi2CmTEKDataAuthentAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 4), DocsBpkmDataAuthentAlg()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKDataAuthentAlg.setDescription('The value of this object is the data authentication\n            algorithm for this SAID.')
docsIetfBpi2CmTEKState = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('start', 1), ('opWait', 2), ('opReauthWait', 3), ('operational', 4), ('rekeyWait', 5), ('rekeyReauthWait', 6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKState.setDescription('The value of this object is the state of the\n            indicated TEK FSM.  The start(1) state indicates that FSM\n            is in its initial state.')
docsIetfBpi2CmTEKKeySequenceNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKKeySequenceNumber.setDescription('The value of this object is the most recent TEK\n            key sequence number for this TEK FSM.')
docsIetfBpi2CmTEKExpiresOld = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 7), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKExpiresOld.setDescription('The value of this object is the actual clock time for\n            expiration of the immediate predecessor of the most recent\n            TEK for this FSM.  If this FSM has only one TEK, then the\n            value is the time of activation of this FSM.')
docsIetfBpi2CmTEKExpiresNew = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 8), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKExpiresNew.setDescription('The value of this object is the actual clock time for\n            expiration of the most recent TEK for this FSM.')
docsIetfBpi2CmTEKKeyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKKeyRequests.setDescription('The value of this object is the count of times the CM\n            has transmitted a Key Request message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmTEKKeyReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKKeyReplies.setDescription('The value of this object is the count of times the CM\n            has received a Key Reply message, including a message whose\n            authentication failed.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmTEKKeyRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKKeyRejects.setDescription('The value of this object is the count of times the CM\n            has received a Key Reject message, including a message\n            whose authentication failed.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmTEKInvalids = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKInvalids.setDescription('The value of this object is the count of times the CM\n            has received a TEK Invalid message, including a message\n            whose authentication failed.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmTEKAuthPends = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKAuthPends.setDescription('The value of this object is the count of times an\n            Authorization Pending (Auth Pend) event occurred in this\n            FSM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmTEKKeyRejectErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 4))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('unauthorizedSaid', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKKeyRejectErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in most recent Key Reject\n            message received by the CM. This has value unknown(2) if\n            the last Error-Code value was 0, and none(1) if no Key\n            Reject message has been received since registration.')
docsIetfBpi2CmTEKKeyRejectErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 15), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKKeyRejectErrorString.setDescription('The value of this object is the text string in\n            most recent Key Reject message received by the CM. This is\n            a zero length string if no Key Reject message has been\n            received since registration.')
docsIetfBpi2CmTEKInvalidErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 16), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 6))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('invalidKeySequence', 6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKInvalidErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in most recent TEK Invalid\n            message received by the CM.  This has value unknown(2) if\n            the last Error-Code value was 0, and none(1) if no TEK\n            Invalid message has been received since registration.')
docsIetfBpi2CmTEKInvalidErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 2, 1, 17), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmTEKInvalidErrorString.setDescription('The value of this object is the text string in\n            most recent TEK Invalid message received by the CM. This is\n            a zero length string if no TEK Invalid message has been\n            received since registration.')
docsIetfBpi2CmMulticastObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3))
docsIetfBpi2CmIpMulticastMapTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1))
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastMapTable.setDescription('This table maps multicast IP addresses to SAIDs per\n            CM MAC Interface.\n            It is intended to map multicast IP addresses associated\n            with SA MAP Request messages.')
docsIetfBpi2CmIpMulticastMapEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastMapEntry.setDescription('Each entry contains objects describing the mapping of\n            one multicast IP address to one SAID, as well as\n            associated state, message counters, and error information.\n\n            An entry may be removed from this table upon the reception\n            of an SA Map Reject.')
docsIetfBpi2CmIpMulticastIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastIndex.setDescription('The index of this row.')
docsIetfBpi2CmIpMulticastAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 2), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastAddressType.setDescription('The type of internet address for\n            docsIetfBpi2CmIpMulticastAddress.')
docsIetfBpi2CmIpMulticastAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 3), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastAddress.setDescription('This object represents the IP multicast address\n            to be mapped. The type of this address is determined by\n            the value of the docsIetfBpi2CmIpMulticastAddressType object.')
docsIetfBpi2CmIpMulticastSAId = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 4), DocsSAIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAId.setDescription('This object represents the SAID to which the IP\n            multicast address has been mapped.  If no SA Map Reply has\n            been received for the IP address, this object should have\n            the value 0.')
docsIetfBpi2CmIpMulticastSAMapState = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('start', 1), ('mapWait', 2), ('mapped', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAMapState.setDescription('The value of this object is the state of the SA\n            Mapping FSM for this IP.')
docsIetfBpi2CmIpMulticastSAMapRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAMapRequests.setDescription('The value of this object is the count of times the\n            CM has transmitted an SA Map Request message for this IP.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmIpMulticastSAMapReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAMapReplies.setDescription('The value of this object is the count of times the\n            CM has received an SA Map Reply message for this IP.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmIpMulticastSAMapRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAMapRejects.setDescription('The value of this object is the count of times the\n            CM has received an SA MAP Reject message for this IP.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmIpMulticastSAMapRejectErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 9, 10))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('noAuthForRequestedDSFlow', 9), ('dsFlowNotMappedToSA', 10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAMapRejectErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in the most recent SA Map\n            Reject message sent in response to an SA Map Request for\n            This IP.  It has the value none(1) if no SA MAP Reject\n            message has been received since entry creation.')
docsIetfBpi2CmIpMulticastSAMapRejectErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 3, 1, 1, 10), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmIpMulticastSAMapRejectErrorString.setDescription('The value of this object is the text string in\n            the most recent SA Map Reject message sent in response to\n            an SA Map Request for this IP.  It is a zero length string\n            if no SA Map Reject message has been received since entry\n            creation.')
docsIetfBpi2CmCertObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 1, 4))
docsIetfBpi2CmDeviceCertTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 1, 4, 1))
if mibBuilder.loadTexts:
    docsIetfBpi2CmDeviceCertTable.setDescription('This table describes the Baseline Privacy Plus\n            device certificates for each CM MAC interface.')
docsIetfBpi2CmDeviceCertEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 1, 4, 1, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmDeviceCertEntry.setDescription('Each entry contains the device certificates of\n            one CM MAC interface.  An entry in this table exists for\n            each ifEntry with an ifType of docsCableMaclayer(127).')
docsIetfBpi2CmDeviceCmCert = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 4, 1, 1, 1), DocsX509ASN1DEREncodedCertificate()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmDeviceCmCert.setDescription("The X509 DER-encoded cable modem certificate.\n            Note:  This object can be set only when the value is the\n            zero-length OCTET STRING, otherwise an error\n            'inconsistentValue' is returned.  Once the object\n            contains  the certificate, its access MUST be read-only\n            and persists after re-initialization of the\n            managed system.")
docsIetfBpi2CmDeviceManufCert = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 4, 1, 1, 2), DocsX509ASN1DEREncodedCertificate()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmDeviceManufCert.setDescription('The X509 DER-encoded manufacturer certificate which\n            signed the cable modem certificate.')
docsIetfBpi2CmCryptoSuiteTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 1, 5))
if mibBuilder.loadTexts:
    docsIetfBpi2CmCryptoSuiteTable.setDescription('This table describes the Baseline Privacy Plus\n            cryptographic suite capabilities for each CM MAC\n            interface.')
docsIetfBpi2CmCryptoSuiteEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 1, 5, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmCryptoSuiteIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmCryptoSuiteEntry.setDescription('Each entry contains a cryptographic suite pair\n            which this CM MAC supports.')
docsIetfBpi2CmCryptoSuiteIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 5, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 1000)))
if mibBuilder.loadTexts:
    docsIetfBpi2CmCryptoSuiteIndex.setDescription('The index for a cryptographic suite row.')
docsIetfBpi2CmCryptoSuiteDataEncryptAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 5, 1, 2), DocsBpkmDataEncryptAlg()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmCryptoSuiteDataEncryptAlg.setDescription('The value of this object is the data encryption\n            algorithm for this cryptographic suite capability.')
docsIetfBpi2CmCryptoSuiteDataAuthentAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 1, 5, 1, 3), DocsBpkmDataAuthentAlg()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmCryptoSuiteDataAuthentAlg.setDescription('The value of this object is the data authentication\n            algorithm for this cryptographic suite capability.')
docsIetfBpi2CmtsObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 2))
docsIetfBpi2CmtsBaseTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsBaseTable.setDescription('This table describes the basic Baseline Privacy\n            attributes of each CMTS MAC interface.')
docsIetfBpi2CmtsBaseEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsBaseEntry.setDescription('Each entry contains objects describing attributes of\n            one CMTS MAC interface.  An entry in this table exists for\n            each ifEntry with an ifType of docsCableMaclayer(127).')
docsIetfBpi2CmtsDefaultAuthLifetime = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 6048000)).clone(604800)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsDefaultAuthLifetime.setDescription('The value of this object is the default lifetime, in\n            seconds, the CMTS assigns to a new authorization key.\n            This object value persist after re-initialization of the\n            managed system.')
docsIetfBpi2CmtsDefaultTEKLifetime = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 604800)).clone(43200)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsDefaultTEKLifetime.setDescription('The value of this object is the default lifetime, in\n            seconds, the CMTS assigns to a new Traffic Encryption Key\n            (TEK).\n            This object value persist after re-initialization of the\n            managed system.')
docsIetfBpi2CmtsDefaultSelfSignedManufCertTrust = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('trusted', 1), ('untrusted', 2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsDefaultSelfSignedManufCertTrust.setDescription('This object determines the default trust of\n            self-signed  manufacturer certificate entries, contained\n            in docsIetfBpi2CmtsCACertTable, created after setting this\n            object.\n            This object needs not to persist after re-initialization\n             of the managed system.')
docsIetfBpi2CmtsCheckCertValidityPeriods = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 4), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCheckCertValidityPeriods.setDescription("Setting this object to 'true' causes all chained and\n            root certificates in the chain to have their validity\n            periods checked against the current time of day, when\n            the CMTS receives an Authorization Request from the\n            CM.\n            A 'false' setting causes all certificates in the chain\n            not to have their validity periods checked against the\n            current time of day.\n            This object needs not to persist after re-initialization\n             of the managed system.")
docsIetfBpi2CmtsAuthentInfos = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthentInfos.setDescription('The value of this object is the count of times the\n            CMTS has received an Authentication Information message\n            from any CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthRequests.setDescription('The value of this object is the count of times the\n            CMTS has received an Authorization Request message from any\n            CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthReplies.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an Authorization Reply message to any\n            CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthRejects.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an Authorization Reject message to any\n            CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthInvalids = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthInvalids.setDescription('The value of this object is the count of times\n            the CMTS has transmitted an Authorization Invalid message\n            to any CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsSAMapRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsSAMapRequests.setDescription('The value of this object is the count of times the\n            CMTS has received an SA Map Request message from any CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsSAMapReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsSAMapReplies.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an SA Map Reply message to any CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsSAMapRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 1, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsSAMapRejects.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an SA Map Reject message to any CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthTable.setDescription('This table describes the attributes of each CM\n            authorization association. The CMTS maintains one\n            authorization association with each Baseline Privacy-\n            enabled CM, registered on each CMTS MAC interface,\n            regardless of whether the CM is authorized or rejected.')
docsIetfBpi2CmtsAuthEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmMacAddress'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthEntry.setDescription('Each entry contains objects describing attributes of\n            one authorization association. The CMTS MUST create one\n            entry per CM per MAC interface, based on the receipt of an\n            Authorization Request message, and MUST not delete the\n            entry until the CM loses registration.')
docsIetfBpi2CmtsAuthCmMacAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 1), MacAddress())
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmMacAddress.setDescription('The value of this object is the physical address of\n            the CM to which the authorization association applies.')
docsIetfBpi2CmtsAuthCmBpiVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1))).clone(namedValues=NamedValues(('bpi', 0), ('bpiPlus', 1)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmBpiVersion.setDescription("The value of this object is the version of Baseline\n            Privacy for which this CM has registered. The value\n            'bpiplus' represents the value of BPI-Version Attribute of\n            the Baseline Privacy Key Management BPKM attribute\n            BPI-Version (1). The value 'bpi' is used to represent the\n            CM registered using DOCSIS 1.0 Baseline Privacy.")
docsIetfBpi2CmtsAuthCmPublicKey = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 524))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmPublicKey.setDescription('The value of this object is a DER-encoded\n            RSAPublicKey ASN.1 type string, as defined in the RSA\n            Encryption Standard (PKCS #1), corresponding to the\n            public key of the CM.  This is the zero-length OCTET\n            STRING if the CMTS does not retain the public key.')
docsIetfBpi2CmtsAuthCmKeySequenceNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmKeySequenceNumber.setDescription('The value of this object is the most recent\n            authorization key sequence number for this CM.')
docsIetfBpi2CmtsAuthCmExpiresOld = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 5), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmExpiresOld.setDescription('The value of this object is the actual clock time\n            for expiration of the immediate predecessor of the most\n            recent authorization key for this FSM. If this FSM has only\n            one authorization key, then the value is the time of\n            activation of this FSM.\n            Note: This object has no meaning for CMs running in BPI\n            mode, therefore this object is not instantiated for entries\n            associated to those CMs.')
docsIetfBpi2CmtsAuthCmExpiresNew = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 6), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmExpiresNew.setDescription('The value of this object is the actual clock\n            time for expiration of the most recent authorization key\n            for this FSM.')
docsIetfBpi2CmtsAuthCmLifetime = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 6048000))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmLifetime.setDescription('The value of this object is the lifetime, in seconds,\n            the CMTS assigns to an authorization key for this CM.')
docsIetfBpi2CmtsAuthCmReset = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noResetRequested', 1), ('invalidateAuth', 2), ('sendAuthInvalid', 3), ('invalidateTeks', 4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmReset.setDescription("Setting this object to invalidateAuth(2) causes the\n            CMTS to invalidate the current CM authorization key(s), but\n            not to transmit an Authorization Invalid message nor to\n            invalidate the primary SAID's TEKs.  Setting this object to\n            sendAuthInvalid(3) causes the CMTS to invalidate the\n            current CM authorization key(s), and to transmit an\n            Authorization Invalid message to the CM, but not to\n            invalidate the primary SAID's TEKs.  Setting this object to\n            invalidateTeks(4) causes the CMTS to invalidate the current\n            CM authorization key(s), to transmit an Authorization\n            Invalid message to the CM, and to invalidate the TEKs\n            associated with this CM's primary SAID.\n            For BPI mode, substitute all of the CM's unicast\n            TEK(s) for the primary SAID's TEKs in the previous\n            paragraph.\n            Reading this object returns the most recently set\n            value of this object, or returns noResetRequested(1) if the\n            object has not been set since entry creation.")
docsIetfBpi2CmtsAuthCmInfos = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmInfos.setDescription('The value of this object is the count of times the\n            CMTS has received an Authentication Information message\n            from this CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthCmRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmRequests.setDescription('The value of this object is the count of times the\n            CMTS has received an Authorization Request message from\n            this CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthCmReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmReplies.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an Authorization Reply message to this\n            CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthCmRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmRejects.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an Authorization Reject message to\n            this CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthCmInvalids = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCmInvalids.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an Authorization Invalid message to\n            this CM.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsAuthRejectErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 8, 11))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('unauthorizedCm', 3), ('unauthorizedSaid', 4), ('permanentAuthorizationFailure', 8), ('timeOfDayNotAcquired', 11)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthRejectErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in most recent Authorization\n            Reject message transmitted to the CM.  This has value\n            unknown(2) if the last Error-Code value was 0, and none(1)\n            if no Authorization Reject message has been transmitted to\n            the CM, since entry creation.')
docsIetfBpi2CmtsAuthRejectErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 15), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthRejectErrorString.setDescription('The value of this object is the text string in\n            most recent Authorization Reject message transmitted to the\n            CM.  This is a zero length string if no Authorization\n            Reject message has been transmitted to the CM, since entry\n            creation.')
docsIetfBpi2CmtsAuthInvalidErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 16), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 5, 6, 7))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('unauthorizedCm', 3), ('unsolicited', 5), ('invalidKeySequence', 6), ('keyRequestAuthenticationFailure', 7)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthInvalidErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in most recent Authorization\n            Invalid message transmitted to the CM.  This has value\n            unknown(2) if the last Error-Code value was 0, and none(1)\n            if no Authorization Invalid message has been transmitted to\n            the CM since entry creation.')
docsIetfBpi2CmtsAuthInvalidErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 17), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthInvalidErrorString.setDescription('The value of this object is the text string in\n            most recent Authorization Invalid message transmitted to\n            the CM.  This is a zero length string if no Authorization\n            Invalid message has been transmitted to the CM since entry\n            creation.')
docsIetfBpi2CmtsAuthPrimarySAId = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 18), DocsSAIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthPrimarySAId.setDescription('The value of this object is the Primary Security\n            Association identifier.  For BPI mode, the value must be\n            any unicast SID.')
docsIetfBpi2CmtsAuthBpkmCmCertValid = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 19), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(('unknown', 0), ('validCmChained', 1), ('validCmTrusted', 2), ('invalidCmUntrusted', 3), ('invalidCAUntrusted', 4), ('invalidCmOther', 5), ('invalidCAOther', 6), ('invalidCmRevoked', 7), ('invalidCARevoked', 8)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthBpkmCmCertValid.setDescription("Contains the reason why a CM's certificate is deemed\n            valid or invalid.\n            Return unknown(0) if the CM is running BPI mode.\n            ValidCmChained(1) means the certificate is valid\n               because it chains to a valid certificate.\n            ValidCmTrusted(2) means the certificate is valid\n               because it has been provisioned (in the\n               docsIetfBpi2CmtsProvisionedCmCert table) to be trusted.\n            InvalidCmUntrusted(3) means the certificate is invalid\n                 because it has been provisioned (in the\n                 docsIetfBpi2CmtsProvisionedCmCert table) to be untrusted.\n            InvalidCAUntrusted(4) means the certificate is invalid\n                 because it chains to an untrusted certificate.\n            InvalidCmOther(5) and InvalidCAOther(6) refer to\n                 errors in parsing, validity periods, etc, which are\n                 attributable to the CM certificate or its chain\n                 respectively; additional information may be found\n                 in docsIetfBpi2AuthRejectErrorString for these types\n                 of errors.\n            InvalidCmRevoked(7) means the certificate is\n               invalid as it was marked as revoked. \n            InvalidCARevoked(8) means the CA certificate is\n               invalid as it was marked as revoked.")
docsIetfBpi2CmtsAuthBpkmCmCert = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 20), DocsX509ASN1DEREncodedCertificate()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthBpkmCmCert.setDescription('The X509 CM Certificate sent as part of a BPKM\n            Authorization Request.\n            Note: The zero-length OCTET STRING must be returned if the\n            Entire certificate is not retained in the CMTS.')
docsIetfBpi2CmtsAuthCACertIndexPtr = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 2, 1, 21), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsAuthCACertIndexPtr.setDescription('A row index into docsIetfBpi2CmtsCACertTable.\n                  Returns the index in docsIetfBpi2CmtsCACertTable which\n                  CA certificate this CM is chained to.  A value of\n                  0 means it could not be found or not applicable.')
docsIetfBpi2CmtsTEKTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKTable.setDescription('This table describes the attributes of each\n            Traffic Encryption Key (TEK) association. The CMTS\n            Maintains one TEK association per SAID on each CMTS MAC\n            interface.')
docsIetfBpi2CmtsTEKEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKSAId'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKEntry.setDescription('Each entry contains objects describing attributes of\n            one TEK association on a particular CMTS MAC interface. The\n            CMTS MUST create one entry per SAID per MAC interface,\n            based on the receipt of a Key Request message, and MUST not\n            delete the entry before the CM authorization for the SAID\n            permanently expires.')
docsIetfBpi2CmtsTEKSAId = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 1), DocsSAId())
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKSAId.setDescription('The value of this object is the DOCSIS Security\n            Association ID (SAID).')
docsIetfBpi2CmtsTEKSAType = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 2), DocsBpkmSAType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKSAType.setDescription("The value of this object is the type of security\n            association.  'dynamic' does not apply to CMs running in\n            BPI mode.  Unicast BPI TEKs must utilize the 'primary'\n            encoding and multicast BPI TEKs must utilize the 'static'\n            encoding.")
docsIetfBpi2CmtsTEKDataEncryptAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 3), DocsBpkmDataEncryptAlg()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKDataEncryptAlg.setDescription('The value of this object is the data encryption\n            algorithm for this SAID.')
docsIetfBpi2CmtsTEKDataAuthentAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 4), DocsBpkmDataAuthentAlg()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKDataAuthentAlg.setDescription('The value of this object is the data authentication\n            algorithm for this SAID.')
docsIetfBpi2CmtsTEKLifetime = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 604800))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKLifetime.setDescription('The value of this object is the lifetime, in\n            seconds, the CMTS assigns to keys for this TEK\n            association.')
docsIetfBpi2CmtsTEKKeySequenceNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 15))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKKeySequenceNumber.setDescription('The value of this object is the most recent TEK\n            key sequence number for this SAID.')
docsIetfBpi2CmtsTEKExpiresOld = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 7), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKExpiresOld.setDescription('The value of this object is the actual clock time\n            for expiration of the immediate predecessor of the most\n            recent TEK for this FSM. If this FSM has only one TEK, then\n            the value is the time of activation of this FSM.')
docsIetfBpi2CmtsTEKExpiresNew = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 8), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKExpiresNew.setDescription('The value of this object is the actual clock time\n            for expiration of the most recent TEK for this FSM.')
docsIetfBpi2CmtsTEKReset = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 9), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKReset.setDescription("Setting this object to 'true' causes the CMTS to\n            invalidate all currently active TEK(s) and to generate new\n            TEK(s) for the associated SAID; the CMTS MAY also generate\n            unsolicited TEK Invalid message(s), to optimize the TEK\n            synchronization between the CMTS and the CM(s). Reading\n            this object always returns FALSE.")
docsIetfBpi2CmtsKeyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsKeyRequests.setDescription('The value of this object is the count of times the\n            CMTS has received a Key Request message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsKeyReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsKeyReplies.setDescription('The value of this object is the count of times the\n            CMTS has transmitted a Key Reply message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsKeyRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsKeyRejects.setDescription('The value of this object is the count of times the\n            CMTS has transmitted a Key Reject message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsTEKInvalids = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKInvalids.setDescription('The value of this object is the count of times the\n            CMTS has transmitted a TEK Invalid message.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsKeyRejectErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 4))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('unauthorizedSaid', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsKeyRejectErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in the most recent Key Reject\n            message sent in response to a Key Request for this SAID.\n            This has value unknown(2) if the last Error-Code value\n            was 0, and none(1) if no Key Reject message has been\n            received since registration.')
docsIetfBpi2CmtsKeyRejectErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 15), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsKeyRejectErrorString.setDescription('The value of this object is the text string in\n            the most recent Key Reject message sent in response to a\n            Key Request for this SAID. This is a zero length string if\n            no Key Reject message has been received since\n            registration.')
docsIetfBpi2CmtsTEKInvalidErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 16), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 6))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('invalidKeySequence', 6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKInvalidErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in the most recent TEK\n            Invalid message sent in association with this SAID.  This\n            has value unknown(2) if the last Error-Code value was 0,\n            and none(1) if no TEK Invalid message has been received\n            since registration.')
docsIetfBpi2CmtsTEKInvalidErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 3, 1, 17), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsTEKInvalidErrorString.setDescription('The value of this object is the text string in\n            the most recent TEK Invalid message sent in association\n            with this SAID.  This is a zero length string if no TEK\n            Invalid message has been received since registration.')
docsIetfBpi2CmtsMulticastObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4))
docsIetfBpi2CmtsIpMulticastMapTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastMapTable.setDescription('This table maps multicast IP addresses to SAIDs.\n            If a multicast IP address is mapped by multiple rows\n            in the table, the row with the lowest\n            docsIetfBpi2CmtsIpMulticastIndex must be utilized for the\n            mapping.')
docsIetfBpi2CmtsIpMulticastMapEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastMapEntry.setDescription('Each entry contains objects describing the mapping of\n            a set of multicast IP address and mask to one SAID\n            associated to a CMTS MAC Interface, as well as associated\n            message\n            counters and error information.')
docsIetfBpi2CmtsIpMulticastIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastIndex.setDescription("The index of this row.\n            Conceptual rows having the value 'permanent' need not allow\n            write-access to any columnar objects in the row.")
docsIetfBpi2CmtsIpMulticastAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 2), InetAddressType().clone('ipv4')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastAddressType.setDescription('The type of internet address for\n            docsIetfBpi2CmtsIpMulticastAddress\n            and docsIetfBpi2CmtsIpMulticastMask.')
docsIetfBpi2CmtsIpMulticastAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 3), InetAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastAddress.setDescription('This object represents the IP multicast address\n            to be mapped, in conjunction with\n            docsIetfBpi2CmtsIpMulticastMask. The type of this address is\n            determined by the value of the object\n            docsIetfBpi2CmtsIpMulticastAddressType.')
docsIetfBpi2CmtsIpMulticastMask = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 4), InetAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastMask.setDescription("This object represents the IP multicast address mask\n            for this row.\n            An IP multicast address matches this row if the logical\n            AND of the address with docsIetfBpi2CmtsIpMulticastMask is\n            identical to the logical AND of\n            docsIetfBpi2CmtsIpMulticastAddr with\n            docsIetfBpi2CmtsIpMulticastMask. The type of this address is\n            determined by the value of the object\n            docsIetfBpi2CmtsIpMulticastAddressType.\n             Note: For IPv6 this object needs not to represent a\n             contiguous netmask, e.g. to associate an SAID to a\n             multicast group matching 'any' multicast scope. The TC\n             InetAddressPrefixLength is not used because it only\n             represents contiguous netmask.")
docsIetfBpi2CmtsIpMulticastSAId = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 5), DocsSAIdOrZero()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAId.setDescription('This object represents the multicast SAID to be\n            used in this IP multicast address mapping entry.')
docsIetfBpi2CmtsIpMulticastSAType = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 6), DocsBpkmSAType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAType.setDescription("The value of this object is the type of security\n            association.  'dynamic' does not apply to CMs running in\n            BPI mode.  Unicast BPI TEKs must utilize the 'primary'\n            encoding and multicast BPI TEKs must utilize the 'static'\n            encoding.  SNMP created entries set this object by default\n            to 'static' if not set at row creation.")
docsIetfBpi2CmtsIpMulticastDataEncryptAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 7), DocsBpkmDataEncryptAlg().clone('des56CbcMode')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastDataEncryptAlg.setDescription('The value of this object is the data encryption\n            algorithm for this IP.')
docsIetfBpi2CmtsIpMulticastDataAuthentAlg = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 8), DocsBpkmDataAuthentAlg().clone('none')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastDataAuthentAlg.setDescription('The value of this object is the data authentication\n            algorithm for this IP.')
docsIetfBpi2CmtsIpMulticastSAMapRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAMapRequests.setDescription('The value of this object is the count of times the\n            CMTS has received an SA Map Request message for this IP.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsIpMulticastSAMapReplies = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAMapReplies.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an SA Map Reply message for this IP.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsIpMulticastSAMapRejects = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAMapRejects.setDescription('The value of this object is the count of times the\n            CMTS has transmitted an SA Map Reject message for this IP.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, and at other\n            times as indicated by the value of\n            ifCounterDiscontinuityTime.')
docsIetfBpi2CmtsIpMulticastSAMapRejectErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 9, 10))).clone(namedValues=NamedValues(('none', 1), ('unknown', 2), ('noAuthForRequestedDSFlow', 9), ('dsFlowNotMappedToSA', 10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAMapRejectErrorCode.setDescription('The value of this object is the enumerated\n            description of the Error-Code in the most recent SA Map\n            Reject message sent in response to a SA Map Request for\n            This IP.  It has value unknown(2) if the last Error-Code\n            Value was 0, and none(1) if no SA MAP Reject message has\n            been received since entry creation.')
docsIetfBpi2CmtsIpMulticastSAMapRejectErrorString = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 13), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 128))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastSAMapRejectErrorString.setDescription('The value of this object is the text string in\n            the most recent SA Map Reject message sent in response to\n            an SA Map Request for this IP.  It is a zero length string\n            if no SA Map Reject message has been received since entry\n            creation.')
docsIetfBpi2CmtsIpMulticastMapControl = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 14), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastMapControl.setDescription('This object controls and reflects the IP multicast\n            address mapping entry.  There is no restriction on the\n            ability to change values in this row while the row is\n            active.\n            A created row can be set to active only after the\n            Corresponding instances of docsIetfBpi2CmtsIpMulticastAddress,\n            docsIetfBpi2CmtsIpMulticastMask, docsIetfBpi2CmtsIpMulticastSAId\n            and docsIetfBpi2CmtsIpMulticastSAType have all been set.')
docsIetfBpi2CmtsIpMulticastMapStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 1, 1, 15), StorageType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsIpMulticastMapStorageType.setDescription("The storage type for this conceptual row.\n            Conceptual rows having the value 'permanent' need not allow\n            write-access to any columnar objects in the row.")
docsIetfBpi2CmtsMulticastAuthTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 2))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsMulticastAuthTable.setDescription('This table describes the multicast SAID\n            authorization for each CM on each CMTS MAC interface.')
docsIetfBpi2CmtsMulticastAuthEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 2, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsMulticastAuthSAId'), (0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsMulticastAuthCmMacAddress'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsMulticastAuthEntry.setDescription('Each entry contains objects describing the key\n            authorization of one cable modem for one multicast SAID\n            for one CMTS MAC interface.\n            Row entries persist after re-initialization of\n            the managed system.')
docsIetfBpi2CmtsMulticastAuthSAId = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 2, 1, 1), DocsSAId())
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsMulticastAuthSAId.setDescription('This object represents the multicast SAID for\n            authorization.')
docsIetfBpi2CmtsMulticastAuthCmMacAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 2, 1, 2), MacAddress())
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsMulticastAuthCmMacAddress.setDescription('This object represents the MAC address of the CM\n            to which the multicast SAID authorization applies.')
docsIetfBpi2CmtsMulticastAuthControl = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 4, 2, 1, 3), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsMulticastAuthControl.setDescription('The status of this conceptual row for the\n            authorization of  multicast SAIDs to CMs. ')
docsIetfBpi2CmtsCertObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5))
docsIetfBpi2CmtsProvisionedCmCertTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCertTable.setDescription('A table of CM certificate trust entries provisioned\n            to the CMTS.  The trust object for a certificate in this\n            table has an overriding effect on the validity object of a\n            certificate in the authorization table, as long as the\n            entire contents of the two certificates are identical.')
docsIetfBpi2CmtsProvisionedCmCertEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1, 1)).setIndexNames((0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsProvisionedCmCertMacAddress'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCertEntry.setDescription("An entry in the CMTS's provisioned CM certificate\n            table.  Row entries persist after re-initialization of\n            the managed system.")
docsIetfBpi2CmtsProvisionedCmCertMacAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1, 1, 1), MacAddress())
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCertMacAddress.setDescription('The index of this row.')
docsIetfBpi2CmtsProvisionedCmCertTrust = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('trusted', 1), ('untrusted', 2))).clone('untrusted')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCertTrust.setDescription('Trust state for the provisioned CM certificate entry.\n            Note: Setting this object need only override the validity\n            of CM certificates sent in future authorization requests;\n            instantaneous effect need not occur.')
docsIetfBpi2CmtsProvisionedCmCertSource = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('snmp', 1), ('configurationFile', 2), ('externalDatabase', 3), ('other', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCertSource.setDescription('This object indicates how the certificate reached the\n            CMTS.  Other(4) means is originated from a source not\n            identified above.')
docsIetfBpi2CmtsProvisionedCmCertStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCertStatus.setDescription("The status of this conceptual row. Values in this row\n            cannot be changed while the row is 'active'.")
docsIetfBpi2CmtsProvisionedCmCert = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 1, 1, 5), DocsX509ASN1DEREncodedCertificate()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsProvisionedCmCert.setDescription('An X509 DER-encoded Certificate Authority\n            certificate.\n            Note: The zero-length OCTET STRING must be returned, on\n            reads, if the entire certificate is not retained in the\n            CMTS.')
docsIetfBpi2CmtsCACertTable = MibTable((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertTable.setDescription('The table of known Certificate Authority certificates\n            acquired by this device.')
docsIetfBpi2CmtsCACertEntry = MibTableRow((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1)).setIndexNames((0, 'DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertIndex'))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertEntry.setDescription("A row in the Certificate Authority certificate\n            table.  Row entries with trust status 'trusted',\n            'untrusted', or 'root' persist after re-initialization\n             of the managed system.")
docsIetfBpi2CmtsCACertIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertIndex.setDescription('The index for this row.')
docsIetfBpi2CmtsCACertSubject = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertSubject.setDescription("The subject name exactly as it is encoded in the\n            X509 certificate.\n            The organizationName portion of the certificate's subject\n            name must be present.  All other fields are optional.  Any\n            optional field present must be pre pended with <CR>\n            (carriage return, U+000D) <LF> (line feed, U+000A).\n            Ordering of fields present must conform to:\n            organizationName <CR> <LF>\n            countryName <CR> <LF>\n            stateOrProvinceName <CR> <LF>\n            localityName <CR> <LF>\n            organizationalUnitName <CR> <LF>\n            organizationalUnitName=<Manufacturing Location> <CR> <LF>\n            commonName")
docsIetfBpi2CmtsCACertIssuer = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 3), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertIssuer.setDescription("The issuer name exactly as it is encoded in the\n            X509 certificate.\n            The commonName portion of the certificate's issuer\n            name must be present.  All other fields are optional.  Any\n            optional field present must be pre pended with <CR>\n            (carriage return, U+000D) <LF> (line feed, U+000A).\n            Ordering of fields present must conform to:\n\n            CommonName <CR><LF>\n            countryName <CR><LF>\n            stateOrProvinceName <CR><LF>\n            localityName <CR><LF>\n            organizationName <CR><LF>\n            organizationalUnitName <CR><LF>\n            organizationalUnitName=<Manufacturing Location>")
docsIetfBpi2CmtsCACertSerialNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertSerialNumber.setDescription("This CA certificate's serial number represented as\n            an octet string.")
docsIetfBpi2CmtsCACertTrust = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('trusted', 1), ('untrusted', 2), ('chained', 3), ('root', 4))).clone('chained')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertTrust.setDescription('This object controls the trust status of this\n            certificate.  Root certificates must be given root(4)\n            trust; manufacturer certificates must not be given root(4)\n            trust.  Trust on root certificates must not change.\n            Note: Setting this object need only affect the validity of\n            CM certificates sent in future authorization requests;\n            instantaneous effect need not occur.')
docsIetfBpi2CmtsCACertSource = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('snmp', 1), ('configurationFile', 2), ('externalDatabase', 3), ('other', 4), ('authentInfo', 5), ('compiledIntoCode', 6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertSource.setDescription('This object indicates how the certificate reached\n            the CMTS.  Other(4) means it originated from a source not\n            identified above.')
docsIetfBpi2CmtsCACertStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertStatus.setDescription("The status of this conceptual row. An attempt\n            to set writable columnar values while this row is active\n            behaves as follows:\n            - Sets to the object docsIetfBpi2CmtsCACertTrust are allowed.\n            - Sets to the object docsIetfBpi2CmtsCACert will return an\n              error inconsistentValue'.\n            A newly create entry cannot be set to active until the\n            value of docsIetfBpi2CmtsCACert is being set.")
docsIetfBpi2CmtsCACert = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 8), DocsX509ASN1DEREncodedCertificate()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACert.setDescription('An X509 DER-encoded Certificate Authority\n            certificate.\n            To help identify certificates, either this object or\n            docsIetfBpi2CmtsCACertThumbprint must be returned by a CMTS for\n            self-signed CA certificates.\n\n            Note: The zero-length OCTET STRING must be returned, on\n            reads, if the entire certificate is not retained in the\n            CMTS.')
docsIetfBpi2CmtsCACertThumbprint = MibTableColumn((1, 3, 6, 1, 2, 1, 9999, 1, 2, 5, 2, 1, 9), OctetString().subtype(subtypeSpec=ValueSizeConstraint(20, 20)).setFixedLength(20)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCACertThumbprint.setDescription('The SHA-1 hash of a CA certificate.\n            To help identify certificates, either this object or\n            docsIetfBpi2CmtsCACert must be returned by a CMTS for\n            self-signed CA certificates.\n\n            Note: The zero-length OCTET STRING must be returned, on\n            reads, if the CA certificate thumb print is not retained\n            in the CMTS.')
docsIetfBpi2CodeDownloadControl = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 1, 4))
docsIetfBpi2CodeDownloadStatusCode = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))).clone(namedValues=NamedValues(('configFileCvcVerified', 1), ('configFileCvcRejected', 2), ('snmpCvcVerified', 3), ('snmpCvcRejected', 4), ('codeFileVerified', 5), ('codeFileRejected', 6), ('other', 7)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeDownloadStatusCode.setDescription('The value indicates the result of the latest config\n            file CVC verification, SNMP CVC verification, or code file\n            verification.')
docsIetfBpi2CodeDownloadStatusString = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeDownloadStatusString.setDescription('The value of this object indicates the additional\n            information to the status code.  The value will include\n            the error code and error description which will be defined\n            separately.')
docsIetfBpi2CodeMfgOrgName = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 3), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeMfgOrgName.setDescription("The value of this object is the device manufacturer's\n            organizationName.")
docsIetfBpi2CodeMfgCodeAccessStart = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 4), DateAndTime().subtype(subtypeSpec=ValueSizeConstraint(11, 11)).setFixedLength(11)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeMfgCodeAccessStart.setDescription("The value of this object is the device manufacturer's\n            current codeAccessStart value. This value always be\n            referenced to Greenwich Mean Time (GMT) and the value\n            format must contain TimeZone information (fields 8-10).")
docsIetfBpi2CodeMfgCvcAccessStart = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 5), DateAndTime().subtype(subtypeSpec=ValueSizeConstraint(11, 11)).setFixedLength(11)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeMfgCvcAccessStart.setDescription("The value of this object is the device manufacturer's\n            current cvcAccessStart value. This value always be\n            referenced to Greenwich Mean Time (GMT) and the value\n            format must contain TimeZone information (fields 8-10).")
docsIetfBpi2CodeCoSignerOrgName = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 6), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeCoSignerOrgName.setDescription("The value of this object is the Co-Signer's\n            organizationName.  The value is a zero length string if\n            the co-signer is not specified.")
docsIetfBpi2CodeCoSignerCodeAccessStart = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 7), DateAndTime().subtype(subtypeSpec=ValueSizeConstraint(11, 11)).setFixedLength(11)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeCoSignerCodeAccessStart.setDescription("The value of this object is the Co-Signer's current\n            codeAccessStart value. This value always be referenced to\n            Greenwich Mean Time (GMT) and the value format must contain\n            TimeZone information (fields 8-10).\n            If docsIetfBpi2CodeCoSignerOrgName is a zero\n            length string, the value of this object is meaningless.")
docsIetfBpi2CodeCoSignerCvcAccessStart = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 8), DateAndTime().subtype(subtypeSpec=ValueSizeConstraint(11, 11)).setFixedLength(11)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeCoSignerCvcAccessStart.setDescription("The value of this object is the Co-Signer's current\n            cvcAccessStart value. This value always be referenced to\n            Greenwich Mean Time (GMT) and the value format must contain\n            TimeZone information (fields 8-10).\n            If docsIetfBpi2CodeCoSignerOrgName is a zero\n            length string, the value of this object is meaningless.")
docsIetfBpi2CodeCvcUpdate = MibScalar((1, 3, 6, 1, 2, 1, 9999, 1, 4, 9), DocsX509ASN1DEREncodedCertificate()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    docsIetfBpi2CodeCvcUpdate.setDescription('Setting a CVC to this object triggers the device\n            to verify the CVC and update the cvcAccessStart values,\n            then the content of this object is discarded..\n            If the device is not enabled to upgrade codefiles, or\n            the CVC verification fails, the CVC will be rejected.\n            Reading this object always returns the zero-length OCTET\n            STRING.')
docsIetfBpi2Notification = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 0))
docsIetfBpi2Conformance = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 2))
docsIetfBpi2Compliances = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 2, 1))
docsIetfBpi2Groups = MibIdentifier((1, 3, 6, 1, 2, 1, 9999, 2, 2))
docsIetfBpi2CmCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 9999, 2, 1, 1)).setObjects(*(('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmGroup'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeDownloadGroup')))
if mibBuilder.loadTexts:
    docsIetfBpi2CmCompliance.setDescription('This is the compliance statement for CMs which\n            implement the DOCSIS Baseline Privacy Interface Plus.')
docsIetfBpi2CmtsCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 9999, 2, 1, 2)).setObjects(*(('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsGroup'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeDownloadGroup')))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsCompliance.setDescription('This is the compliance statement for CMTSs which\n            implement the DOCSIS Baseline Privacy Interface Plus.')
docsIetfBpi2CmGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 9999, 2, 2, 1)).setObjects(*(('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmPrivacyEnable'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmPublicKey'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthState'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthKeySequenceNumber'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthExpiresOld'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthExpiresNew'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthReset'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthGraceTime'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKGraceTime'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthWaitTimeout'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmReauthWaitTimeout'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmOpWaitTimeout'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmRekeyWaitTimeout'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthRejectWaitTimeout'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmSAMapWaitTimeout'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmSAMapMaxRetries'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthentInfos'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthInvalids'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthRejectErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthRejectErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthInvalidErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmAuthInvalidErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKSAType'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKDataEncryptAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKDataAuthentAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKState'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKKeySequenceNumber'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKExpiresOld'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKExpiresNew'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKKeyRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKKeyReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKKeyRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKInvalids'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKAuthPends'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKKeyRejectErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKKeyRejectErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKInvalidErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmTEKInvalidErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastAddressType'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastAddress'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAId'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAMapState'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAMapRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAMapReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAMapRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAMapRejectErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmIpMulticastSAMapRejectErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmDeviceCmCert'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmDeviceManufCert'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmCryptoSuiteDataEncryptAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmCryptoSuiteDataAuthentAlg')))
if mibBuilder.loadTexts:
    docsIetfBpi2CmGroup.setDescription('This collection of objects provides CM BPI+ status\n            and control.')
docsIetfBpi2CmtsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 9999, 2, 2, 2)).setObjects(*(('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsDefaultAuthLifetime'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsDefaultTEKLifetime'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsDefaultSelfSignedManufCertTrust'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCheckCertValidityPeriods'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthentInfos'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthInvalids'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsSAMapRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsSAMapReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsSAMapRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmBpiVersion'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmPublicKey'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmKeySequenceNumber'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmExpiresOld'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmExpiresNew'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmLifetime'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmReset'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmInfos'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCmInvalids'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthRejectErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthRejectErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthInvalidErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthInvalidErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthPrimarySAId'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthBpkmCmCertValid'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthBpkmCmCert'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsAuthCACertIndexPtr'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKSAType'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKDataEncryptAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKDataAuthentAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKLifetime'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKKeySequenceNumber'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKExpiresOld'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKExpiresNew'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKReset'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsKeyRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsKeyReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsKeyRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKInvalids'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsKeyRejectErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsKeyRejectErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKInvalidErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsTEKInvalidErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastAddressType'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastAddress'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastMask'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAId'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAType'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastDataEncryptAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastDataAuthentAlg'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAMapRequests'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAMapReplies'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAMapRejects'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAMapRejectErrorCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastSAMapRejectErrorString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastMapControl'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsIpMulticastMapStorageType'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsMulticastAuthControl'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsProvisionedCmCertTrust'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsProvisionedCmCertSource'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsProvisionedCmCertStatus'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsProvisionedCmCert'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertSubject'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertIssuer'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertSerialNumber'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertTrust'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertSource'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertStatus'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACert'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CmtsCACertThumbprint')))
if mibBuilder.loadTexts:
    docsIetfBpi2CmtsGroup.setDescription('This collection of objects provides CMTS BPI+ status\n            and control.')
docsIetfBpi2CodeDownloadGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 9999, 2, 2, 3)).setObjects(*(('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeDownloadStatusCode'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeDownloadStatusString'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeMfgOrgName'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeMfgCodeAccessStart'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeMfgCvcAccessStart'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeCoSignerOrgName'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeCoSignerCodeAccessStart'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeCoSignerCvcAccessStart'), ('DOCS-IETF-BPI2-MIB', 'docsIetfBpi2CodeCvcUpdate')))
if mibBuilder.loadTexts:
    docsIetfBpi2CodeDownloadGroup.setDescription('This collection of objects provide authenticated\n            software\n            download support.')
mibBuilder.exportSymbols('DOCS-IETF-BPI2-MIB', docsIetfBpi2CmtsSAMapRejects=docsIetfBpi2CmtsSAMapRejects, docsIetfBpi2CmAuthState=docsIetfBpi2CmAuthState, docsIetfBpi2CmtsIpMulticastSAType=docsIetfBpi2CmtsIpMulticastSAType, docsIetfBpi2CmIpMulticastSAMapRequests=docsIetfBpi2CmIpMulticastSAMapRequests, docsIetfBpi2CmCompliance=docsIetfBpi2CmCompliance, docsIetfBpi2CmtsAuthCmReset=docsIetfBpi2CmtsAuthCmReset, docsIetfBpi2CmtsAuthCmInvalids=docsIetfBpi2CmtsAuthCmInvalids, docsIetfBpi2CmtsMulticastObjects=docsIetfBpi2CmtsMulticastObjects, docsIetfBpi2CmtsMulticastAuthSAId=docsIetfBpi2CmtsMulticastAuthSAId, docsIetfBpi2CodeMfgCodeAccessStart=docsIetfBpi2CodeMfgCodeAccessStart, docsIetfBpi2CmCryptoSuiteDataEncryptAlg=docsIetfBpi2CmCryptoSuiteDataEncryptAlg, docsIetfBpi2CmtsTEKSAType=docsIetfBpi2CmtsTEKSAType, docsIetfBpi2CmtsAuthCACertIndexPtr=docsIetfBpi2CmtsAuthCACertIndexPtr, docsIetfBpi2CmtsKeyReplies=docsIetfBpi2CmtsKeyReplies, DocsBpkmDataEncryptAlg=DocsBpkmDataEncryptAlg, docsIetfBpi2CodeCoSignerCvcAccessStart=docsIetfBpi2CodeCoSignerCvcAccessStart, docsIetfBpi2Notification=docsIetfBpi2Notification, docsIetfBpi2CmtsAuthRejectErrorString=docsIetfBpi2CmtsAuthRejectErrorString, docsIetfBpi2Compliances=docsIetfBpi2Compliances, docsIetfBpi2CmIpMulticastAddress=docsIetfBpi2CmIpMulticastAddress, docsIetfBpi2CmtsAuthCmExpiresNew=docsIetfBpi2CmtsAuthCmExpiresNew, docsIetfBpi2CmtsTEKSAId=docsIetfBpi2CmtsTEKSAId, docsIetfBpi2CodeDownloadStatusCode=docsIetfBpi2CodeDownloadStatusCode, docsIetfBpi2CmtsAuthEntry=docsIetfBpi2CmtsAuthEntry, docsIetfBpi2CodeCoSignerOrgName=docsIetfBpi2CodeCoSignerOrgName, docsIetfBpi2CmtsCACertThumbprint=docsIetfBpi2CmtsCACertThumbprint, docsIetfBpi2CmtsKeyRequests=docsIetfBpi2CmtsKeyRequests, docsIetfBpi2CmtsTEKLifetime=docsIetfBpi2CmtsTEKLifetime, docsIetfBpi2CmtsCACertIndex=docsIetfBpi2CmtsCACertIndex, docsIetfBpi2CmtsGroup=docsIetfBpi2CmtsGroup, docsIetfBpi2CmtsAuthCmRejects=docsIetfBpi2CmtsAuthCmRejects, docsIetfBpi2CmtsBaseTable=docsIetfBpi2CmtsBaseTable, docsIetfBpi2CmtsIpMulticastMapControl=docsIetfBpi2CmtsIpMulticastMapControl, docsIetfBpi2CmtsCACertTrust=docsIetfBpi2CmtsCACertTrust, docsIetfBpi2CmtsIpMulticastDataEncryptAlg=docsIetfBpi2CmtsIpMulticastDataEncryptAlg, docsIetfBpi2CmtsIpMulticastDataAuthentAlg=docsIetfBpi2CmtsIpMulticastDataAuthentAlg, docsIetfBpi2CmtsTEKDataAuthentAlg=docsIetfBpi2CmtsTEKDataAuthentAlg, docsIetfBpi2CmCryptoSuiteIndex=docsIetfBpi2CmCryptoSuiteIndex, docsIetfBpi2CmBaseEntry=docsIetfBpi2CmBaseEntry, docsIetfBpi2CmtsTEKInvalidErrorString=docsIetfBpi2CmtsTEKInvalidErrorString, docsIetfBpi2CmCryptoSuiteEntry=docsIetfBpi2CmCryptoSuiteEntry, docsIetfBpi2CmtsAuthReplies=docsIetfBpi2CmtsAuthReplies, docsIetfBpi2CmtsCACertEntry=docsIetfBpi2CmtsCACertEntry, docsIetfBpi2CmtsAuthCmRequests=docsIetfBpi2CmtsAuthCmRequests, docsIetfBpi2CmtsProvisionedCmCertTrust=docsIetfBpi2CmtsProvisionedCmCertTrust, docsIetfBpi2CmTEKKeyRequests=docsIetfBpi2CmTEKKeyRequests, docsIetfBpi2CmAuthRejectErrorString=docsIetfBpi2CmAuthRejectErrorString, docsIetfBpi2CmRekeyWaitTimeout=docsIetfBpi2CmRekeyWaitTimeout, docsIetfBpi2CmAuthGraceTime=docsIetfBpi2CmAuthGraceTime, docsIetfBpi2CmReauthWaitTimeout=docsIetfBpi2CmReauthWaitTimeout, docsIetfBpi2CmtsAuthCmPublicKey=docsIetfBpi2CmtsAuthCmPublicKey, docsIetfBpi2CmtsAuthCmReplies=docsIetfBpi2CmtsAuthCmReplies, docsIetfBpi2CmIpMulticastMapTable=docsIetfBpi2CmIpMulticastMapTable, docsIetfBpi2CmCryptoSuiteDataAuthentAlg=docsIetfBpi2CmCryptoSuiteDataAuthentAlg, docsIetfBpi2CmTEKState=docsIetfBpi2CmTEKState, docsIetfBpi2CmSAMapWaitTimeout=docsIetfBpi2CmSAMapWaitTimeout, docsIetfBpi2CmtsAuthRejectErrorCode=docsIetfBpi2CmtsAuthRejectErrorCode, docsIetfBpi2CmtsMulticastAuthCmMacAddress=docsIetfBpi2CmtsMulticastAuthCmMacAddress, docsIetfBpi2CmDeviceCertEntry=docsIetfBpi2CmDeviceCertEntry, docsIetfBpi2CmtsTEKTable=docsIetfBpi2CmtsTEKTable, docsIetfBpi2CmtsIpMulticastAddress=docsIetfBpi2CmtsIpMulticastAddress, docsIetfBpi2CmtsKeyRejectErrorCode=docsIetfBpi2CmtsKeyRejectErrorCode, docsIetfBpi2CmtsCertObjects=docsIetfBpi2CmtsCertObjects, docsIetfBpi2CodeDownloadControl=docsIetfBpi2CodeDownloadControl, docsIetfBpi2CmtsAuthTable=docsIetfBpi2CmtsAuthTable, docsIetfBpi2CmIpMulticastSAMapRejectErrorString=docsIetfBpi2CmIpMulticastSAMapRejectErrorString, docsIetfBpi2CmtsKeyRejects=docsIetfBpi2CmtsKeyRejects, docsIetfBpi2CmIpMulticastIndex=docsIetfBpi2CmIpMulticastIndex, docsIetfBpi2CmTEKSAType=docsIetfBpi2CmTEKSAType, docsIetfBpi2CmtsIpMulticastMapEntry=docsIetfBpi2CmtsIpMulticastMapEntry, docsIetfBpi2CmIpMulticastSAId=docsIetfBpi2CmIpMulticastSAId, docsIetfBpi2CmAuthRejects=docsIetfBpi2CmAuthRejects, docsIetfBpi2CmAuthentInfos=docsIetfBpi2CmAuthentInfos, docsIetfBpi2CmtsMulticastAuthEntry=docsIetfBpi2CmtsMulticastAuthEntry, docsIetfBpi2CmtsTEKInvalids=docsIetfBpi2CmtsTEKInvalids, docsIetfBpi2CmtsAuthBpkmCmCert=docsIetfBpi2CmtsAuthBpkmCmCert, docsIetfBpi2CmTEKEntry=docsIetfBpi2CmTEKEntry, docsIetfBpi2CmtsCACert=docsIetfBpi2CmtsCACert, docsIetfBpi2CmtsDefaultSelfSignedManufCertTrust=docsIetfBpi2CmtsDefaultSelfSignedManufCertTrust, docsIetfBpi2Groups=docsIetfBpi2Groups, docsIetfBpi2CmtsTEKKeySequenceNumber=docsIetfBpi2CmtsTEKKeySequenceNumber, DocsSAIdOrZero=DocsSAIdOrZero, docsIetfBpi2CodeMfgOrgName=docsIetfBpi2CodeMfgOrgName, docsIetfBpi2CodeCvcUpdate=docsIetfBpi2CodeCvcUpdate, docsIetfBpi2CmAuthRejectErrorCode=docsIetfBpi2CmAuthRejectErrorCode, docsIetfBpi2CodeDownloadStatusString=docsIetfBpi2CodeDownloadStatusString, docsIetfBpi2CmBaseTable=docsIetfBpi2CmBaseTable, docsIetfBpi2CmAuthReplies=docsIetfBpi2CmAuthReplies, docsIetfBpi2CmAuthExpiresOld=docsIetfBpi2CmAuthExpiresOld, docsIetfBpi2CmTEKDataAuthentAlg=docsIetfBpi2CmTEKDataAuthentAlg, PYSNMP_MODULE_ID=docsIetfBpi2MIB, docsIetfBpi2Conformance=docsIetfBpi2Conformance, docsIetfBpi2CmAuthExpiresNew=docsIetfBpi2CmAuthExpiresNew, docsIetfBpi2CmtsCompliance=docsIetfBpi2CmtsCompliance, docsIetfBpi2CmDeviceManufCert=docsIetfBpi2CmDeviceManufCert, docsIetfBpi2CmtsSAMapRequests=docsIetfBpi2CmtsSAMapRequests, docsIetfBpi2CmTEKAuthPends=docsIetfBpi2CmTEKAuthPends, docsIetfBpi2CmtsProvisionedCmCertStatus=docsIetfBpi2CmtsProvisionedCmCertStatus, DocsSAId=DocsSAId, docsIetfBpi2CmSAMapMaxRetries=docsIetfBpi2CmSAMapMaxRetries, docsIetfBpi2MIBObjects=docsIetfBpi2MIBObjects, docsIetfBpi2CmtsKeyRejectErrorString=docsIetfBpi2CmtsKeyRejectErrorString, docsIetfBpi2CmObjects=docsIetfBpi2CmObjects, docsIetfBpi2CmIpMulticastSAMapReplies=docsIetfBpi2CmIpMulticastSAMapReplies, docsIetfBpi2CmTEKInvalidErrorString=docsIetfBpi2CmTEKInvalidErrorString, docsIetfBpi2CodeDownloadGroup=docsIetfBpi2CodeDownloadGroup, docsIetfBpi2CmGroup=docsIetfBpi2CmGroup, docsIetfBpi2CmPublicKey=docsIetfBpi2CmPublicKey, docsIetfBpi2CmtsProvisionedCmCertTable=docsIetfBpi2CmtsProvisionedCmCertTable, docsIetfBpi2CmAuthRejectWaitTimeout=docsIetfBpi2CmAuthRejectWaitTimeout, docsIetfBpi2CmtsBaseEntry=docsIetfBpi2CmtsBaseEntry, docsIetfBpi2CmtsAuthCmLifetime=docsIetfBpi2CmtsAuthCmLifetime, docsIetfBpi2CmtsIpMulticastSAMapRequests=docsIetfBpi2CmtsIpMulticastSAMapRequests, docsIetfBpi2CmIpMulticastSAMapState=docsIetfBpi2CmIpMulticastSAMapState, docsIetfBpi2CmAuthInvalids=docsIetfBpi2CmAuthInvalids, docsIetfBpi2CmTEKKeyRejectErrorString=docsIetfBpi2CmTEKKeyRejectErrorString, docsIetfBpi2CmIpMulticastSAMapRejectErrorCode=docsIetfBpi2CmIpMulticastSAMapRejectErrorCode, docsIetfBpi2CmtsCACertStatus=docsIetfBpi2CmtsCACertStatus, docsIetfBpi2CmtsIpMulticastSAMapReplies=docsIetfBpi2CmtsIpMulticastSAMapReplies, docsIetfBpi2CmtsIpMulticastMapStorageType=docsIetfBpi2CmtsIpMulticastMapStorageType, docsIetfBpi2CmOpWaitTimeout=docsIetfBpi2CmOpWaitTimeout, docsIetfBpi2CmtsAuthCmKeySequenceNumber=docsIetfBpi2CmtsAuthCmKeySequenceNumber, docsIetfBpi2CmtsCACertTable=docsIetfBpi2CmtsCACertTable, DocsX509ASN1DEREncodedCertificate=DocsX509ASN1DEREncodedCertificate, docsIetfBpi2CmtsTEKEntry=docsIetfBpi2CmtsTEKEntry, docsIetfBpi2CmtsCACertSource=docsIetfBpi2CmtsCACertSource, docsIetfBpi2CmTEKDataEncryptAlg=docsIetfBpi2CmTEKDataEncryptAlg, docsIetfBpi2CmtsTEKExpiresNew=docsIetfBpi2CmtsTEKExpiresNew, DocsBpkmSAType=DocsBpkmSAType, docsIetfBpi2CmtsTEKDataEncryptAlg=docsIetfBpi2CmtsTEKDataEncryptAlg, docsIetfBpi2CmDeviceCmCert=docsIetfBpi2CmDeviceCmCert, docsIetfBpi2CmIpMulticastAddressType=docsIetfBpi2CmIpMulticastAddressType, docsIetfBpi2CmtsCheckCertValidityPeriods=docsIetfBpi2CmtsCheckCertValidityPeriods, docsIetfBpi2CmTEKSAId=docsIetfBpi2CmTEKSAId, docsIetfBpi2CmtsDefaultTEKLifetime=docsIetfBpi2CmtsDefaultTEKLifetime, docsIetfBpi2CmTEKTable=docsIetfBpi2CmTEKTable, docsIetfBpi2CmTEKExpiresNew=docsIetfBpi2CmTEKExpiresNew, docsIetfBpi2CmtsAuthCmExpiresOld=docsIetfBpi2CmtsAuthCmExpiresOld, docsIetfBpi2CmtsObjects=docsIetfBpi2CmtsObjects, docsIetfBpi2CmtsProvisionedCmCertEntry=docsIetfBpi2CmtsProvisionedCmCertEntry, docsIetfBpi2CmTEKGraceTime=docsIetfBpi2CmTEKGraceTime, docsIetfBpi2CmtsTEKInvalidErrorCode=docsIetfBpi2CmtsTEKInvalidErrorCode, docsIetfBpi2CmtsIpMulticastSAMapRejects=docsIetfBpi2CmtsIpMulticastSAMapRejects, docsIetfBpi2CmtsAuthCmMacAddress=docsIetfBpi2CmtsAuthCmMacAddress, docsIetfBpi2CmtsIpMulticastSAMapRejectErrorString=docsIetfBpi2CmtsIpMulticastSAMapRejectErrorString, docsIetfBpi2CmAuthWaitTimeout=docsIetfBpi2CmAuthWaitTimeout, docsIetfBpi2CmTEKKeyRejects=docsIetfBpi2CmTEKKeyRejects, docsIetfBpi2CmtsAuthBpkmCmCertValid=docsIetfBpi2CmtsAuthBpkmCmCertValid, docsIetfBpi2CmDeviceCertTable=docsIetfBpi2CmDeviceCertTable, docsIetfBpi2CmAuthInvalidErrorString=docsIetfBpi2CmAuthInvalidErrorString, docsIetfBpi2CmtsIpMulticastMapTable=docsIetfBpi2CmtsIpMulticastMapTable, docsIetfBpi2CmtsDefaultAuthLifetime=docsIetfBpi2CmtsDefaultAuthLifetime, docsIetfBpi2CmtsCACertSerialNumber=docsIetfBpi2CmtsCACertSerialNumber, docsIetfBpi2CmtsAuthRejects=docsIetfBpi2CmtsAuthRejects, docsIetfBpi2CmIpMulticastMapEntry=docsIetfBpi2CmIpMulticastMapEntry, docsIetfBpi2CmTEKKeySequenceNumber=docsIetfBpi2CmTEKKeySequenceNumber, docsIetfBpi2CmMulticastObjects=docsIetfBpi2CmMulticastObjects, docsIetfBpi2CmCertObjects=docsIetfBpi2CmCertObjects, docsIetfBpi2CmtsTEKReset=docsIetfBpi2CmtsTEKReset, docsIetfBpi2CmAuthReset=docsIetfBpi2CmAuthReset, docsIetfBpi2CmtsIpMulticastSAMapRejectErrorCode=docsIetfBpi2CmtsIpMulticastSAMapRejectErrorCode, docsIetfBpi2CmtsAuthPrimarySAId=docsIetfBpi2CmtsAuthPrimarySAId, docsIetfBpi2CmTEKKeyReplies=docsIetfBpi2CmTEKKeyReplies, docsIetfBpi2CmtsProvisionedCmCertMacAddress=docsIetfBpi2CmtsProvisionedCmCertMacAddress, docsIetfBpi2CmtsAuthCmInfos=docsIetfBpi2CmtsAuthCmInfos, docsIetfBpi2CmtsTEKExpiresOld=docsIetfBpi2CmtsTEKExpiresOld, docsIetfBpi2CmtsSAMapReplies=docsIetfBpi2CmtsSAMapReplies, docsIetfBpi2CmtsProvisionedCmCertSource=docsIetfBpi2CmtsProvisionedCmCertSource, docsIetfBpi2CmtsAuthInvalidErrorCode=docsIetfBpi2CmtsAuthInvalidErrorCode, docsIetfBpi2CmCryptoSuiteTable=docsIetfBpi2CmCryptoSuiteTable, DocsBpkmDataAuthentAlg=DocsBpkmDataAuthentAlg, docsIetfBpi2CmPrivacyEnable=docsIetfBpi2CmPrivacyEnable, docsIetfBpi2CmtsIpMulticastMask=docsIetfBpi2CmtsIpMulticastMask, docsIetfBpi2CmtsCACertIssuer=docsIetfBpi2CmtsCACertIssuer, docsIetfBpi2CmtsAuthInvalidErrorString=docsIetfBpi2CmtsAuthInvalidErrorString, docsIetfBpi2CmtsIpMulticastAddressType=docsIetfBpi2CmtsIpMulticastAddressType, docsIetfBpi2CodeCoSignerCodeAccessStart=docsIetfBpi2CodeCoSignerCodeAccessStart, docsIetfBpi2CmtsCACertSubject=docsIetfBpi2CmtsCACertSubject, docsIetfBpi2CmtsAuthCmBpiVersion=docsIetfBpi2CmtsAuthCmBpiVersion, docsIetfBpi2CmIpMulticastSAMapRejects=docsIetfBpi2CmIpMulticastSAMapRejects, docsIetfBpi2CmTEKInvalids=docsIetfBpi2CmTEKInvalids, docsIetfBpi2CmTEKInvalidErrorCode=docsIetfBpi2CmTEKInvalidErrorCode, docsIetfBpi2CmtsIpMulticastSAId=docsIetfBpi2CmtsIpMulticastSAId, docsIetfBpi2CodeMfgCvcAccessStart=docsIetfBpi2CodeMfgCvcAccessStart, docsIetfBpi2CmtsAuthRequests=docsIetfBpi2CmtsAuthRequests, docsIetfBpi2CmtsIpMulticastIndex=docsIetfBpi2CmtsIpMulticastIndex, docsIetfBpi2CmtsMulticastAuthControl=docsIetfBpi2CmtsMulticastAuthControl, docsIetfBpi2CmtsAuthInvalids=docsIetfBpi2CmtsAuthInvalids, docsIetfBpi2MIB=docsIetfBpi2MIB, docsIetfBpi2CmTEKExpiresOld=docsIetfBpi2CmTEKExpiresOld, docsIetfBpi2CmAuthInvalidErrorCode=docsIetfBpi2CmAuthInvalidErrorCode, docsIetfBpi2CmtsProvisionedCmCert=docsIetfBpi2CmtsProvisionedCmCert, docsIetfBpi2CmTEKKeyRejectErrorCode=docsIetfBpi2CmTEKKeyRejectErrorCode, docsIetfBpi2CmAuthKeySequenceNumber=docsIetfBpi2CmAuthKeySequenceNumber, docsIetfBpi2CmtsMulticastAuthTable=docsIetfBpi2CmtsMulticastAuthTable, docsIetfBpi2CmtsAuthentInfos=docsIetfBpi2CmtsAuthentInfos, docsIetfBpi2CmAuthRequests=docsIetfBpi2CmAuthRequests)