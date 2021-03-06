# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/BastionPGPKey.py
# Compiled at: 2012-03-06 02:26:51
import os, commands, re, types, subprocess
pgpUserId = re.compile('User ID - ([A-Za-z0-9 ]+)\\s+\\((.+)\\)\\s+<(.+)>')
pgpKeyId = re.compile('Key ID - 0x([0-9A-F]+)')
pgpDateStamp = re.compile('Creation time - (.+)')
PGP_BOUNDARY = re.compile('^(- )*?-----(BEGIN|END) PGP (SIGNATURE|SIGNED MESSAGE)-----\\r?$').match
PGP_BEGIN_SIGNED = re.compile('^(- )*?-----BEGIN PGP SIGNED MESSAGE-----\\r?$').match
PGP_BEGIN_SIGNATURE = re.compile('^(- )*?-----BEGIN PGP SIGNATURE-----\\r?$').match
PGP_END_SIGNATURE = re.compile('^(- )*?-----END PGP SIGNATURE-----\\r?$').match

def parse_signatories(text, sigs=None):
    """
    pass it to pgpdump and pluck out a list of the (Key ID, date) pairs ...
    """
    if sigs == None:
        sigs = []
    lines = text.split('\n')
    if len(lines) < 12 or not PGP_BEGIN_SIGNED(lines[0]) or not PGP_BEGIN_SIGNATURE(lines[(-8)]) or not PGP_END_SIGNATURE(lines[(-2)]):
        sigs.reverse()
        return sigs
    else:
        lines[0] = '-----BEGIN PGP SIGNED MESSAGE-----'
        lines[-8] = '-----BEGIN PGP SIGNATURE-----'
        lines[-2] = '-----END PGP SIGNATURE-----'
        pipe = subprocess.Popen(['/usr/bin/pgpdump'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdin, stdout, stderr = pipe.stdin, pipe.stdout, pipe.stderr
        stdin.write(('\n').join(lines))
        stdin.close()
        parsed = stdout.read()
        stdout.close()
        error = stderr.read()
        if error:
            raise IOError, error
        keys = pgpKeyId.findall(parsed)
        dates = pgpDateStamp.findall(parsed)
        sigs.append((keys[0], dates[0]))
        inner = lines[3:-8]
        inner.append('')
        return parse_signatories(('\n').join(inner), sigs)


def remove_pgp_clearsign_boundary(text=''):
    """
    return raw text with PGP boundaries removed
    """
    lines = text.split('\n')
    if len(lines) < 12:
        return text
    if PGP_BEGIN_SIGNED(lines[0]) and lines[1].startswith('Hash: ') and lines[2] == '' and lines[(-1)] == '' and PGP_END_SIGNATURE(lines[(-2)]) and PGP_BEGIN_SIGNATURE(lines[(-8)]):
        if len(lines) == 12:
            return '%s\n' % lines[3]
        else:
            return ('').join(remove_pgp_clearsign_boundary(('\n').join(lines[3:-8])))
    return text


def pgp_headers(text, headers=None):
    if headers == None:
        headers = []
    lines = text.split('\n')
    if not PGP_BEGIN_SIGNED(lines[0]):
        return ('\n').join(headers)
    else:
        headers.extend(lines[0:3])
        return pgp_headers(('\n').join(lines[3:]), headers)


def pgp_trailers(text, trailers=None):
    if trailers == None:
        trailers = []
    lines = text.split('\n')
    if trailers:
        ndx = -7
    else:
        ndx = -8
    if -len(lines) > ndx or not PGP_BEGIN_SIGNATURE(lines[ndx]):
        trailers.reverse()
        return ('\n').join(trailers)
    else:
        tail = lines[ndx:]
        tail.reverse()
        trailers.extend(tail)
        return pgp_trailers(('\n').join(lines[:ndx]), trailers)


class BastionPGPKey:
    """
    an encapsulation of an OpenPGP Key Object
    this is non-persistent!

    the present implementation is a bit shite - but we only have to work on this
    one class to clean it up ...

    the 'parsed' key contains the following:

Old: Public Key Packet(tag 6)(418 bytes)
        Ver 4 - new
        Public key creation time - Mon Jul 30 01:56:25 BST 2001
        Pub alg - DSA Digital Signature Standard(pub 17)
        DSA p(1024 bits) - ...
        DSA q(160 bits) - ...
        DSA g(1023 bits) - ...
        DSA y(1021 bits) - ...
Old: User ID Packet(tag 13)(42 bytes)
        User ID - Alan Milligan (Spike) <alan@balclutha.org>
Old: Signature Packet(tag 2)(93 bytes)
        Ver 4 - new
        Sig type - Positive certification of a User ID and Public Key packet(0x13).
        Pub alg - DSA Digital Signature Standard(pub 17)
        Hash alg - SHA1(hash 2)
        Hashed Sub: signature creation time(sub 2)(4 bytes)
                Time - Tue Feb 11 16:54:50 GMT 2003
        Hashed Sub: key expiration time(sub 9)(4 bytes)
                Time - Sat Feb 10 16:54:50 GMT 2007
        Hashed Sub: preferred symmetric algorithms(sub 11)(4 bytes)
                Sym alg - AES with 128-bit key(sym 7)
                Sym alg - Twofish with 256-bit key(sym 10)
                Sym alg - CAST5(sym 3)
                Sym alg - Blowfish(sym 4)
        Hashed Sub: preferred hash algorithms(sub 21)(2 bytes)
                Hash alg - RIPEMD160(hash 3)
                Hash alg - SHA1(hash 2)
        Hashed Sub: preferred compression algorithms(sub 22)(2 bytes)
                Comp alg - ZLIB <RFC1950>(comp 2)
                Comp alg - ZIP <RFC1951>(comp 1)
        Hashed Sub: key server preferences(sub 23)(1 bytes)
                Flag - No-modify
        Sub: issuer key ID(sub 16)(8 bytes)
                Key ID - 0xADA841845252F63F
        Hash left 2 bytes - 50 2c 
        DSA r(160 bits) - ...
        DSA s(160 bits) - ...
                -> hash(160 bits)
Old: Public Subkey Packet(tag 14)(269 bytes)
        Ver 4 - new
        Public key creation time - Mon Jul 30 01:56:38 BST 2001
        Pub alg - ElGamal Encrypt-Only(pub 16)
        ElGamal p(1024 bits) - ...
        ElGamal g(5 bits) - ...
        ElGamal y(1023 bits) - ...
Old: Signature Packet(tag 2)(76 bytes)
        Ver 4 - new
        Sig type - Subkey Binding Signature(0x18).
        Pub alg - DSA Digital Signature Standard(pub 17)
        Hash alg - SHA1(hash 2)
        Hashed Sub: signature creation time(sub 2)(4 bytes)
                Time - Mon Jul 30 01:56:38 BST 2001
        Hashed Sub: key expiration time(sub 9)(4 bytes)
                Time - Tue Jul 30 01:56:38 BST 2002
        Sub: issuer key ID(sub 16)(8 bytes)
                Key ID - 0xADA841845252F63F
        Hash left 2 bytes - 98 d2 
        DSA r(156 bits) - ...
        DSA s(159 bits) - ...
                -> hash(160 bits)
Old: Public Subkey Packet(tag 14)(418 bytes)
        Ver 4 - new
        Public key creation time - Fri Mar 21 22:36:03 GMT 2003
        Pub alg - DSA Digital Signature Standard(pub 17)
        DSA p(1024 bits) - ...
        DSA q(160 bits) - ...
        DSA g(1022 bits) - ...
        DSA y(1019 bits) - ...
Old: Signature Packet(tag 2)(70 bytes)
        Ver 4 - new
        Sig type - Subkey Binding Signature(0x18).
        Pub alg - DSA Digital Signature Standard(pub 17)
        Hash alg - SHA1(hash 2)
        Hashed Sub: signature creation time(sub 2)(4 bytes)
                Time - Fri Mar 21 22:36:03 GMT 2003
        Sub: issuer key ID(sub 16)(8 bytes)
                Key ID - 0xADA841845252F63F
        Hash left 2 bytes - 30 85 
        DSA r(157 bits) - ...
        DSA s(159 bits) - ...
                -> hash(160 bits)

    """

    def __init__(self, key):
        if type(key) in types.StringTypes:
            self._v_key = key
            pipe = subprocess.Popen(['/usr/bin/pgpdump'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdin, stdout = pipe.stdin, pipe.stdout
            stdin.write(key)
            stdin.close()
            self._v_imp = stdout.read()
            stdout.close()
        else:
            self._v_imp = commands.getoutput('/usr/bin/pgpdump %s' % key)
            self._v_key = open(key, 'r').read()

    def isValid(self):
        try:
            return self.pgpKeyId() and self.pgpUserId()
        except:
            raise
            return 0

    def pgpKey(self):
        return self._v_key

    def pgpKeyId(self):
        match = pgpKeyId.search(self._v_imp)
        if match:
            return match.group(1)
        raise KeyError, 'Unrecognised!! %s' % self._v_imp

    def pgpUserId(self):
        match = pgpUserId.search(self._v_imp)
        if match:
            return match.group(1)
        raise KeyError, 'Unrecognised!!'

    def pgpNameCommentEmail(self):
        match = pgpUserId.search(self._v_imp)
        if match:
            return match.groups()
        raise KeyError, 'Unrecognised!!'