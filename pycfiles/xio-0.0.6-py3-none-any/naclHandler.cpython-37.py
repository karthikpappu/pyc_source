# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/lib/crypto/naclHandler.py
# Compiled at: 2018-12-07 08:05:33
# Size of source mod 2**32: 2525 bytes
from .common import *
import nacl.utils
from nacl.public import PrivateKey, PublicKey, SealedBox, Box
from nacl.signing import SigningKey
import nacl.hash, time

class NaclEncryptionHandler:

    def __init__(self, naclpriv, naclpub):
        self._naclpriv = naclpriv.to_curve25519_private_key()
        self._naclpub = naclpub.to_curve25519_public_key()
        self.private = self._naclpriv.encode(nacl.encoding.HexEncoder)
        self.public = self._naclpub.encode(nacl.encoding.HexEncoder)

    def encrypt(self, message, dst_public_key=None):
        publicKey = PublicKey(decode_hex(dst_public_key)) if dst_public_key else self._naclpub
        sealed_box = SealedBox(publicKey)
        encrypted = sealed_box.encrypt(str_to_bytes(message))
        return encode_hex(encrypted)

    def decrypt(self, message):
        unseal_box = SealedBox(self._naclpriv)
        message = unseal_box.decrypt(decode_hex(message))
        return message


class NaclHandler:

    def __init__(self, private=None, seed=None):
        if private:
            self._naclpriv = SigningKey(decode_hex(private))
        else:
            if seed:
                seed = decode_hex(nacl.hash.sha256(str_to_bytes(seed)))
                self._naclpriv = SigningKey(seed)
            else:
                self._naclpriv = SigningKey.generate()
        self._naclpub = self._naclpriv.verify_key
        self.private = self._naclpriv.encode(nacl.encoding.HexEncoder)
        self.public = self._naclpub.encode(nacl.encoding.HexEncoder)
        self.encryption = NaclEncryptionHandler(self._naclpriv, self._naclpub)

    def sign(self, message):
        signingKey = self._naclpriv
        signed = signingKey.sign(str_to_bytes(message))
        verify_key = signingKey.verify_key
        verify_key_hex = verify_key.encode(encoder=(nacl.encoding.HexEncoder))
        sig = (
         str_to_bytes(verify_key_hex), str_to_bytes(encode_hex(signed)))
        sig = (b'-').join(sig)
        sig = encode_hex(sig)
        assert self.verify(message, sig)
        return sig

    @staticmethod
    def verify(message, sig):
        verify_key_hex, signed = str_to_bytes(decode_hex(sig)).split(b'-')
        verifyKey = nacl.signing.VerifyKey((str_to_bytes(verify_key_hex)), encoder=(nacl.encoding.HexEncoder))
        unsigned = verifyKey.verify(decode_hex(signed))
        assert str_to_bytes(message) == unsigned
        return True