# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/transform/encrypt_common.py
# Compiled at: 2016-03-08 18:12:41
from zope.component import getGlobalSiteManager, ComponentLookupError
from zope.interface import implementer
from .interfaces import IEncrypter, IEncrypterClass
_gsm = getGlobalSiteManager()

@implementer(IEncrypter)
class CommonEncrypter(object):
    name = ''
    attributes = ()

    def __init__(self, **kw):
        kwargs = {}
        for i in self.attributes:
            if i in kw:
                kwargs[i] = kw[i]

        self._signature = '.e%s$' % self.name
        self._init_encryption(**kwargs)
        self.register()

    def _init_encryption(self, **kw):
        pass

    def encrypt(self, data, no_cipher_name=False):
        if no_cipher_name:
            sig = '.e$'
        else:
            sig = self._signature
        return sig + self._encrypt(data)

    def decrypt(self, data):
        if data.startswith(self._signature):
            return self._decrypt(data[len(self._signature):])
        else:
            if data.startswith('.e$'):
                return self._decrypt(data[3:])
            return data

    def register(self):
        try:
            if _gsm.getUtility(IEncrypterClass) is self.__class__:
                _gsm.registerUtility(self)
            _gsm.registerUtility(self, name=self.name)
        except ComponentLookupError:
            pass

    @classmethod
    def register_class(self, default=False):
        _gsm.registerUtility(self, IEncrypterClass, name=self.name)
        if default:
            _gsm.registerUtility(self, IEncrypterClass)


def encrypt(data, no_cipher_name=False):
    try:
        return _gsm.getUtility(IEncrypter).encrypt(data, no_cipher_name=no_cipher_name)
    except ComponentLookupError:
        return data


def get_encryption_signature(data):
    if data.startswith('.e'):
        return data[2:data.find('$')]
    else:
        return
        return


def decrypt(data):
    sig = get_encryption_signature(data).decode()
    if sig is not None:
        return _gsm.getUtility(IEncrypter, sig).decrypt(data)
    else:
        return data
        return


def init(**kw):
    for name, cls in _gsm.getUtilitiesFor(IEncrypterClass):
        if name:
            try:
                utility = _gsm.getUtility(IEncrypter, name=name)
                _gsm.unregisterUtility(utility)
            except ComponentLookupError:
                pass

            cls(**kw).register()