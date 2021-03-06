# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc2511.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1_modules import rfc2315
from pyasn1_modules.rfc2459 import *
MAX = float('inf')
id_pkix = univ.ObjectIdentifier('1.3.6.1.5.5.7')
id_pkip = univ.ObjectIdentifier('1.3.6.1.5.5.7.5')
id_regCtrl = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1')
id_regCtrl_regToken = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1.1')
id_regCtrl_authenticator = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1.2')
id_regCtrl_pkiPublicationInfo = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1.3')
id_regCtrl_pkiArchiveOptions = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1.4')
id_regCtrl_oldCertID = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1.5')
id_regCtrl_protocolEncrKey = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.1.6')
id_regInfo = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.2')
id_regInfo_utf8Pairs = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.2.1')
id_regInfo_certReq = univ.ObjectIdentifier('1.3.6.1.5.5.7.5.2.2')

class GeneralName(univ.OctetString):
    __module__ = __name__


class UTF8Pairs(char.UTF8String):
    __module__ = __name__


class ProtocolEncrKey(SubjectPublicKeyInfo):
    __module__ = __name__


class CertId(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('issuer', GeneralName()), namedtype.NamedType('serialNumber', univ.Integer()))


class OldCertId(CertId):
    __module__ = __name__


class KeyGenParameters(univ.OctetString):
    __module__ = __name__


class EncryptedValue(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('intendedAlg', AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.OptionalNamedType('symmAlg', AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.OptionalNamedType('encSymmKey', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))), namedtype.OptionalNamedType('keyAlg', AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))), namedtype.OptionalNamedType('valueHint', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))), namedtype.NamedType('encValue', univ.BitString()))


class EncryptedKey(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('encryptedValue', EncryptedValue()), namedtype.NamedType('envelopedData', rfc2315.EnvelopedData().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))))


class PKIArchiveOptions(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('encryptedPrivKey', EncryptedKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('keyGenParameters', KeyGenParameters().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('archiveRemGenPrivKey', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))


class SinglePubInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('pubMethod', univ.Integer(namedValues=namedval.NamedValues(('dontCare',
                                                                                                                         0), ('x500',
                                                                                                                              1), ('web',
                                                                                                                                   2), ('ldap',
                                                                                                                                        3)))), namedtype.OptionalNamedType('pubLocation', GeneralName()))


class PKIPublicationInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('action', univ.Integer(namedValues=namedval.NamedValues(('dontPublish',
                                                                                                                      0), ('pleasePublish',
                                                                                                                           1)))), namedtype.OptionalNamedType('pubInfos', univ.SequenceOf(componentType=SinglePubInfo()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))))


class Authenticator(char.UTF8String):
    __module__ = __name__


class RegToken(char.UTF8String):
    __module__ = __name__


class SubsequentMessage(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('encrCert', 0), ('challengeResp', 1))


class POPOPrivKey(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('thisMessage', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('subsequentMessage', SubsequentMessage().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('dhMAC', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))


class PBMParameter(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('salt', univ.OctetString()), namedtype.NamedType('owf', AlgorithmIdentifier()), namedtype.NamedType('iterationCount', univ.Integer()), namedtype.NamedType('mac', AlgorithmIdentifier()))


class PKMACValue(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('algId', AlgorithmIdentifier()), namedtype.NamedType('value', univ.BitString()))


class POPOSigningKeyInput(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('authInfo', univ.Choice(componentType=namedtype.NamedTypes(namedtype.NamedType('sender', GeneralName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('publicKeyMAC', PKMACValue())))), namedtype.NamedType('publicKey', SubjectPublicKeyInfo()))


class POPOSigningKey(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('poposkInput', POPOSigningKeyInput().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('algorithmIdentifier', AlgorithmIdentifier()), namedtype.NamedType('signature', univ.BitString()))


class ProofOfPossession(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('raVerified', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('signature', POPOSigningKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.NamedType('keyEncipherment', POPOPrivKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))), namedtype.NamedType('keyAgreement', POPOPrivKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))))


class Controls(univ.SequenceOf):
    __module__ = __name__
    componentType = AttributeTypeAndValue()
    sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)


class OptionalValidity(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('notBefore', Time().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('notAfter', Time().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))


class CertTemplate(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('version', Version().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('serialNumber', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('signingAlg', AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))), namedtype.OptionalNamedType('issuer', Name().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))), namedtype.OptionalNamedType('validity', OptionalValidity().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))), namedtype.OptionalNamedType('subject', Name().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5))), namedtype.OptionalNamedType('publicKey', SubjectPublicKeyInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6))), namedtype.OptionalNamedType('issuerUID', UniqueIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))), namedtype.OptionalNamedType('subjectUID', UniqueIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))), namedtype.OptionalNamedType('extensions', Extensions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 9))))


class CertRequest(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('certReqId', univ.Integer()), namedtype.NamedType('certTemplate', CertTemplate()), namedtype.OptionalNamedType('controls', Controls()))


class CertReq(CertRequest):
    __module__ = __name__


class CertReqMsg(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('certReq', CertRequest()), namedtype.OptionalNamedType('pop', ProofOfPossession()), namedtype.OptionalNamedType('regInfo', univ.SequenceOf(componentType=AttributeTypeAndValue()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))))


class CertReqMessages(univ.SequenceOf):
    __module__ = __name__
    componentType = CertReqMsg()
    sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)