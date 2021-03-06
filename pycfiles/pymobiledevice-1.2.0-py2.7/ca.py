# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/ca.py
# Compiled at: 2019-02-24 18:45:28
"""
How to create a CA certificate with Python.

WARNING: This sample only demonstrates how to use the objects and methods,
         not how to create a safe and correct certificate.

Copyright (c) 2004 Open Source Applications Foundation.
Authors: Heikki Toivonen
         Mathieu RENARD
"""
from M2Crypto import RSA, X509, EVP, m2, BIO
from M2Crypto.RSA import load_pub_key_bio
from pyasn1.type import univ
from pyasn1.codec.der import encoder as der_encoder
from pyasn1.codec.der import decoder as der_decoder
import struct, base64
from pprint import *

def convertPKCS1toPKCS8pubKey(bitsdata):
    pubkey_pkcs1_b64 = ('').join(bitsdata.split('\n')[1:-2])
    pubkey_pkcs1, restOfInput = der_decoder.decode(base64.b64decode(pubkey_pkcs1_b64))
    bitstring = univ.Sequence()
    bitstring.setComponentByPosition(0, univ.Integer(pubkey_pkcs1[0]))
    bitstring.setComponentByPosition(1, univ.Integer(pubkey_pkcs1[1]))
    bitstring = der_encoder.encode(bitstring)
    try:
        bitstring = ('').join([ ('00000000' + bin(ord(x))[2:])[-8:] for x in list(bitstring) ])
    except:
        bitstring = ('').join([ ('00000000' + bin(x)[2:])[-8:] for x in list(bitstring) ])

    bitstring = univ.BitString("'%s'B" % bitstring)
    pubkeyid = univ.Sequence()
    pubkeyid.setComponentByPosition(0, univ.ObjectIdentifier('1.2.840.113549.1.1.1'))
    pubkeyid.setComponentByPosition(1, univ.Null(''))
    pubkey_seq = univ.Sequence()
    pubkey_seq.setComponentByPosition(0, pubkeyid)
    pubkey_seq.setComponentByPosition(1, bitstring)
    base64.MAXBINSIZE = 48
    res = '-----BEGIN PUBLIC KEY-----\n'
    res += base64.encodestring(der_encoder.encode(pubkey_seq))
    res += '-----END PUBLIC KEY-----\n'
    return res


def generateRSAKey():
    return RSA.gen_key(2048, m2.RSA_F4)


def makePKey(key):
    pkey = EVP.PKey()
    pkey.assign_rsa(key)
    return pkey


def makeRequest(pkey, cn):
    req = X509.Request()
    req.set_version(2)
    req.set_pubkey(pkey)
    name = X509.X509_Name()
    name.CN = cn
    req.set_subject_name(name)
    ext1 = X509.new_extension('subjectAltName', 'DNS:foobar.example.com')
    ext2 = X509.new_extension('nsComment', 'Hello there')
    extstack = X509.X509_Extension_Stack()
    extstack.push(ext1)
    extstack.push(ext2)
    assert extstack[1].get_name() == 'nsComment'
    req.add_extensions(extstack)
    return req


def makeCert(req, caPkey):
    pkey = req.get_pubkey()
    if not req.verify(pkey):
        raise ValueError('Error verifying request')
    sub = req.get_subject()
    cert = X509.X509()
    cert.set_serial_number(1)
    cert.set_version(2)
    cert.set_subject(sub)
    issuer = X509.X509_Name()
    issuer.CN = 'The Issuer Monkey'
    issuer.O = 'The Organization Otherwise Known as My CA, Inc.'
    cert.set_issuer(issuer)
    cert.set_pubkey(pkey)
    notBefore = m2.x509_get_not_before(cert.x509)
    notAfter = m2.x509_get_not_after(cert.x509)
    m2.x509_gmtime_adj(notBefore, 0)
    days = 30
    m2.x509_gmtime_adj(notAfter, 86400 * days)
    cert.add_ext(X509.new_extension('subjectAltName', 'DNS:foobar.example.com'))
    ext = X509.new_extension('nsComment', 'M2Crypto generated certificate')
    ext.set_critical(0)
    cert.add_ext(ext)
    cert.sign(caPkey, 'sha1')
    assert cert.get_ext('subjectAltName').get_name() == 'subjectAltName'
    assert cert.get_ext_at(0).get_name() == 'subjectAltName'
    assert cert.get_ext_at(0).get_value() == 'DNS:foobar.example.com'
    return cert


def ca():
    key = generateRSAKey()
    pkey = makePKey(key)
    req = makeRequest(pkey)
    cert = makeCert(req, pkey)
    return (cert, pkey)


def ca_do_everything(DevicePublicKey):
    rsa = generateRSAKey()
    privateKey = makePKey(rsa)
    req = makeRequest(privateKey, 'The Issuer Monkey')
    cert = makeCert(req, privateKey)
    rsa2 = load_pub_key_bio(BIO.MemoryBuffer(convertPKCS1toPKCS8pubKey(DevicePublicKey)))
    pkey2 = EVP.PKey()
    pkey2.assign_rsa(rsa2)
    req = makeRequest(pkey2, 'Device')
    cert2 = makeCert(req, privateKey)
    return (cert.as_pem(), privateKey.as_pem(None), cert2.as_pem())


if __name__ == '__main__':
    rsa = generateRSAKey()
    pkey = makePKey(rsa)
    print pkey.as_pem(None)
    req = makeRequest(pkey, 'The Issuer Monkey')
    cert = makeCert(req, pkey)
    print cert.as_text()
    cert.save_pem('my_ca_cert.pem')
    rsa.save_key('my_key.pem', None)