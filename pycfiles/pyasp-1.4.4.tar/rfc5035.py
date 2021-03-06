# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5035.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc2634
from pyasn1_modules import rfc4055
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5280
ContentType = rfc5652.ContentType
IssuerAndSerialNumber = rfc5652.IssuerAndSerialNumber
SubjectKeyIdentifier = rfc5652.SubjectKeyIdentifier
AlgorithmIdentifier = rfc5280.AlgorithmIdentifier
PolicyInformation = rfc5280.PolicyInformation
GeneralNames = rfc5280.GeneralNames
CertificateSerialNumber = rfc5280.CertificateSerialNumber
id_aa_signingCertificate = rfc2634.id_aa_signingCertificate
id_aa_signingCertificateV2 = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.47')
Hash = rfc2634.Hash
IssuerSerial = rfc2634.IssuerSerial
ESSCertID = rfc2634.ESSCertID
SigningCertificate = rfc2634.SigningCertificate
sha256AlgId = AlgorithmIdentifier()
sha256AlgId['algorithm'] = rfc4055.id_sha256
sha256AlgId['parameters'] = der_encode(univ.OctetString(''))

class ESSCertIDv2(univ.Sequence):
    __module__ = __name__


ESSCertIDv2.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('hashAlgorithm', sha256AlgId), namedtype.NamedType('certHash', Hash()), namedtype.OptionalNamedType('issuerSerial', IssuerSerial()))

class SigningCertificateV2(univ.Sequence):
    __module__ = __name__


SigningCertificateV2.componentType = namedtype.NamedTypes(namedtype.NamedType('certs', univ.SequenceOf(componentType=ESSCertIDv2())), namedtype.OptionalNamedType('policies', univ.SequenceOf(componentType=PolicyInformation())))
id_aa_mlExpandHistory = rfc2634.id_aa_mlExpandHistory
ub_ml_expansion_history = rfc2634.ub_ml_expansion_history
EntityIdentifier = rfc2634.EntityIdentifier
MLReceiptPolicy = rfc2634.MLReceiptPolicy
MLData = rfc2634.MLData
MLExpansionHistory = rfc2634.MLExpansionHistory
id_aa_securityLabel = rfc2634.id_aa_securityLabel
ub_privacy_mark_length = rfc2634.ub_privacy_mark_length
ub_security_categories = rfc2634.ub_security_categories
ub_integer_options = rfc2634.ub_integer_options
ESSPrivacyMark = rfc2634.ESSPrivacyMark
SecurityClassification = rfc2634.SecurityClassification
SecurityPolicyIdentifier = rfc2634.SecurityPolicyIdentifier
SecurityCategory = rfc2634.SecurityCategory
SecurityCategories = rfc2634.SecurityCategories
ESSSecurityLabel = rfc2634.ESSSecurityLabel
id_aa_equivalentLabels = rfc2634.id_aa_equivalentLabels
EquivalentLabels = rfc2634.EquivalentLabels
id_aa_contentIdentifier = rfc2634.id_aa_contentIdentifier
ContentIdentifier = rfc2634.ContentIdentifier
id_aa_contentReference = rfc2634.id_aa_contentReference
ContentReference = rfc2634.ContentReference
id_aa_msgSigDigest = rfc2634.id_aa_msgSigDigest
MsgSigDigest = rfc2634.MsgSigDigest
id_aa_contentHint = rfc2634.id_aa_contentHint
ContentHints = rfc2634.ContentHints
AllOrFirstTier = rfc2634.AllOrFirstTier
ReceiptsFrom = rfc2634.ReceiptsFrom
id_aa_receiptRequest = rfc2634.id_aa_receiptRequest
ub_receiptsTo = rfc2634.ub_receiptsTo
ReceiptRequest = rfc2634.ReceiptRequest
ESSVersion = rfc2634.ESSVersion
id_ct_receipt = rfc2634.id_ct_receipt
Receipt = rfc2634.Receipt
ub_receiptsTo = rfc2634.ub_receiptsTo
ReceiptRequest = rfc2634.ReceiptRequest
_cmsAttributesMapUpdate = {id_aa_signingCertificateV2: SigningCertificateV2()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)
_cmsContentTypesMapUpdate = {id_ct_receipt: Receipt()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)