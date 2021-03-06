# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/ldap/ldaphasher.py
# Compiled at: 2007-12-02 16:26:55
import base64, string, md5, sha
from random import choice

class LDAPPasswordHasher(object):
    __module__ = __name__

    def __init__(self, password):
        self.password = password

    def hash(self, algo='SHA'):
        salt = ''
        password = self.password
        if algo == 'CLEARTEXT':
            return self.password
        if 'SHA' in algo:
            module = sha
        elif 'MD5' or 'crypt' in algo:
            module = md5
        else:
            raise 'unsupported encryption'
        if algo == 'SSHA' or algo == 'SMD5':
            for i in range(0, 4):
                salt += choice(string.ascii_letters + string.digits)

            password += salt
        if algo == 'crypt':
            for i in range(0, 8):
                salt += choice(string.ascii_letters + string.digits)

            hashed = self.md5crypt(password, salt)
            return '{%s}%s' % (algo, hashed)
        return ('{%s}%s' % (algo, base64.encodestring(module.new(str(password)).digest() + salt))).rstrip()

    def md5crypt(self, password, salt, magic='$1$'):
        m = md5.new()
        m.update(password + magic + salt)
        mixin = md5.md5(password + salt + password).digest()
        for i in range(0, len(password)):
            m.update(mixin[(i % 16)])

        i = len(password)
        while i:
            if i & 1:
                m.update('\x00')
            else:
                m.update(password[0])
            i >>= 1

        final = m.digest()
        for i in range(1000):
            m2 = md5.md5()
            if i & 1:
                m2.update(password)
            else:
                m2.update(final)
            if i % 3:
                m2.update(salt)
            if i % 7:
                m2.update(password)
            if i & 1:
                m2.update(final)
            else:
                m2.update(password)
            final = m2.digest()

        itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        rearranged = ''
        for (a, b, c) in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
            v = ord(final[a]) << 16 | ord(final[b]) << 8 | ord(final[c])
            for i in range(4):
                rearranged += itoa64[(v & 63)]
                v >>= 6

        v = ord(final[11])
        for i in range(2):
            rearranged += itoa64[(v & 63)]
            v >>= 6

        return magic + salt + '$' + rearranged


from salamoia.tests import *
runDocTests()