# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/spoon.py
# Compiled at: 2006-11-19 22:31:08
import sys, StringIO, warnings, zlib
from threading import RLock, Semaphore
import ber
DICT_TAG = ber.Tag(ber.APPLICATION, 1, container=True)
PYOBJ_TAG = ber.Tag(ber.APPLICATION, 2, container=True)
PYOBJ_REF_TAG = ber.Tag(ber.APPLICATION, 3)
LAZY_DICT_TAG = ber.Tag(ber.APPLICATION, 4, container=True)
STRING_BUFF_TAG = ber.Tag(ber.APPLICATION, 5, container=True)
PYOBJZ_TAG = ber.Tag(ber.APPLICATION, 6)
SPOONLINKMSG_TAG = ber.Tag(ber.APPLICATION, 7, container=True)
SPOONNETMSG_TAG = ber.Tag(ber.APPLICATION, 8, container=True)

class serialprop(object):
    """
    When used like a property in a Serial class, it will act as 
    a flag to the serializer that only properties that are of type C{serialprop} or C{lazyprop} 
    are to be serialized. 
    
    Any subclass of this will be treated the same way, so if you need your property to behave like
    a customizable property, then subclass away.
    """
    __module__ = __name__

    def __init__(self, value=None):
        self.initVal = value
        self.valDict = {}
        self.lock = RLock()

    def __get__(self, obj, Type=None):
        obj._spoon_meta.proplock.acquire()
        try:
            return obj._spoon_meta.propdict.setdefault(self, self.initVal)
        finally:
            obj._spoon_meta.proplock.release()

    def __set__(self, obj, value):
        obj._spoon_meta.proplock.acquire()
        try:
            obj._spoon_meta.propdict[self] = value
        finally:
            obj._spoon_meta.proplock.release()

    def __del__(self, obj):
        self.lock.acquire()
        try:
            del obj._spoon_meta.propdict[self]
        finally:
            self.lock.release()


class lazyprop(property):
    """
    When used like a property in a Serial class, it will act as 
    a flag to the serializer that only properties that are of type C{serialprop} or C{lazyprop} 
    are to be serialized. 
    
    Any subclass of this will be treated the same way, so if you need your property to behave like
    a customizable property, then subclass away.
    
    lazyprop indicates that on decoding, the object will have to explicitly decode all of the 
    properties marked with lazyprop.  lazyprop and serialprop may be mixed together in a class, 
    and all serialprops will be decoded.
    """
    __module__ = __name__

    def __init__(self, value=None):
        self.initVal = value
        self.valDict = {}

    def __get__(self, obj, Type=None):
        lazydata = getattr(obj, '_spoon_lazydata', None)
        if lazydata is not None and lazydata.closed != True:
            obj.decode_lazy()
        obj._spoon_meta.proplock.acquire()
        try:
            return obj._spoon_meta.propdict.setdefault(self, self.initVal)
        finally:
            obj._spoon_meta.proplock.release()
        return

    def __set__(self, obj, value):
        obj._spoon_meta.proplock.acquire()
        try:
            obj._spoon_meta.propdict[self] = value
        finally:
            obj._spoon_meta.proplock.release()

    def __del__(self, obj):
        obj._spoon_meta.proplock.acquire()
        try:
            del obj._spoon_meta.propdict[self]
        finally:
            obj._spoon_meta.proplock.release()


class SpoonData(object):
    __module__ = __name__

    def __init__(self):
        self.proplock = Semaphore()
        self.decodelock = Semaphore()
        self.propdict = {}


class SerialMeta(type):
    __module__ = __name__

    def __init__(cls, name, bases, dict):
        super(SerialMeta, cls).__init__(name, bases, dict)
        tmpList = [ k for (k, v) in dict.iteritems() if serialprop in type(v).__mro__ ]
        if len(tmpList) > 0:
            setattr(cls, '_spoon_attrs', tmpList)
        tmpList = [ k for (k, v) in dict.iteritems() if lazyprop in type(v).__mro__ ]
        if len(tmpList) > 0:
            setattr(cls, '_spoon_lazyattrs', tmpList)


class Serial(object):
    __module__ = __name__
    __metaclass__ = SerialMeta

    def __new__(cls, *args, **kwargs):
        newobj = super(Serial, cls).__new__(cls, *args, **kwargs)
        newobj._spoon_meta = SpoonData()
        return newobj

    def post_deserialize(self):
        """
        Called after an object is received over the network, instead of the
        normal C{__init__} method.
        """
        pass

    def pre_serialize(self):
        """
        Called right before this object's attributes are encoded into a stream
        for network travel.
        """
        pass

    def decode_lazy(self):
        """
        Decode all of the attributes marked as lazy that have not yet been decoded.
        @return: Number of attributes decoded.
        @warning: Some sort of instance level locking should be done 
        """
        if self._spoon_lazydata.closed:
            return 0
        self._spoon_meta.decodelock.acquire()
        try:
            b = ber.BERStream(self._spoon_lazydata)
            attrs = b.next()
            for (k, v) in attrs.iteritems():
                setattr(self, k, v)

            self._spoon_lazydata.close()
            return len(attrs)
        finally:
            self._spoon_meta.decodelock.release()


class Memoizer(object):
    """
    Used as a substitute for the file object when serializing Serial objects,
    so reference cycles are caught and handled.
    """
    __module__ = __name__

    def __init__(self, fd):
        self.fd = fd
        self.memo = {}

    def write(self, data):
        self.fd.write(data)

    def read(self, n):
        return self.fd.read(n)

    def __getattr__(self, name):
        return getattr(self._fd, name)


class StringIOWrap(object):
    """
    Stupid wrapper around StringIO because it isn't a new style class. GRR!
    
    I'm only implementing the methods that actually make sense for StringIOs and that we actually use.
    """
    __module__ = __name__

    def __init__(self, sio=None):
        if sio == None:
            self.sio = StringIO.StringIO()
        else:
            self.sio = sio
        return

    def __iter__(self):
        return self.sio.__iter__()

    def next(self):
        return self.sio.next()

    def getvalue(self):
        return self.sio.getvalue()

    def write(self, data):
        return self.sio.write(data)

    def read(self, cnt):
        return self.sio.read(cnt)

    def close(self):
        return self.sio.close()

    def seek(self, pos):
        return self.sio.seek(pos)

    def tell(self):
        return self.sio.tell()

    def get_len(self):
        return self.sio.len

    def get_closed(self):
        return self.sio.closed

    len = property(fget=get_len)
    closed = property(fget=get_closed)


class LazyDict(dict):
    __module__ = __name__


@ber.encoder(StringIOWrap)
def encode_stringio(fd, item):
    tmpfd = StringIO.StringIO()
    strio_pos = item.tell()
    b = ber.BERStream(tmpfd)
    b.add(item.tell())
    ber.Tag.from_tag(ber.BYTES_TYPE, item.len).write(tmpfd)
    tmpfd.write(item.getvalue())
    ber.Tag.from_tag(STRING_BUFF_TAG, tmpfd.len).write(fd)
    fd.write(tmpfd.getvalue())


@ber.decoder(STRING_BUFF_TAG)
def decode_stringio(fd, tag):
    out = StringIOWrap()
    b = ber.BERStream(fd)
    seek_pos = b.next()
    out.write(b.next())
    out.seek(seek_pos)
    return out


@ber.encoder(LazyDict)
def encode_lazydict(fd, item):
    tmpfd = StringIO.StringIO()
    b = ber.BERStream(tmpfd)
    for (key, value) in item.iteritems():
        b.add((key, value))

    ber.Tag.from_tag(LAZY_DICT_TAG, tmpfd.len).write(fd)
    fd.write(tmpfd.getvalue())
    tmpfd.close()


@ber.decoder(LAZY_DICT_TAG)
def decode_lazydict(fd, tag):
    """
    Decoding a lazy dict will just result in returning the entire object as a string.
    """
    tmpfd = StringIOWrap()
    ber.Tag.from_tag(DICT_TAG, tag.size).write(tmpfd)
    count = 0
    while count < tag.size:
        data = fd.read(tag.size - count)
        count += len(data)
        tmpfd.write(data)

    tmpfd.seek(0)
    return tmpfd


@ber.encoder(dict)
def encode_dict(fd, item):
    ber.Tag.from_tag(DICT_TAG, None).write(fd)
    b = ber.BERStream(fd)
    for (key, value) in item.iteritems():
        b.add((key, value))

    b._add_eof()
    return


@ber.decoder(DICT_TAG)
def decode_dict(fd, tag):
    out = {}
    b = ber.BERStream(fd, tag.size)
    while b.has_next():
        (key, value) = b.next()
        out[key] = value

    return out


@ber.zencoder(Serial)
def encode_pyobjz(fd, obj):
    tmpfd = StringIO.StringIO()
    encode_pyobj(tmpfd, obj, True)
    data = zlib.compress(tmpfd.getvalue())
    tmpfd.close()
    ber.Tag.from_tag(PYOBJZ_TAG, len(data)).write(fd)
    fd.write(data)


@ber.decoder(PYOBJZ_TAG)
def decode_pyobjz(fd, tag):
    data = zlib.decompress(fd.read(tag.size))
    tmpfd = StringIO.StringIO(data)
    return decode_pyobj(tmpfd, ber.Tag.from_tag(PYOBJ_TAG, len(data)))


@ber.encoder(Serial)
def encode_pyobj(fd, obj, omittag=False):
    obj.pre_serialize()
    attrlist = getattr(obj, '_spoon_attrs', None)
    lazyattrlist = getattr(obj, '_spoon_lazyattrs', None)
    if attrlist is None and lazyattrlist is None:
        attrlist = [ a for a in dir(obj) if a[0] != '_' if '__call__' not in dir(getattr(obj, a, None)) ]
    objectlazydata = getattr(obj, '_spoon_lazydata', None)
    attrdict = {}
    if attrlist is not None:
        for a in attrlist:
            if not ber.BERStream.can_encode(getattr(obj, a, None)):
                warnings.warn("Can't encode attribute %s of %s(type: %s" % (a, type(obj).__name__, repr(type(getattr(obj, a, None)))), RuntimeWarning)
                continue
            attrdict[a] = getattr(obj, a, None)

    if objectlazydata is not None and not objectlazydata.closed:
        attrdict['_spoon_lazydata'] = objectlazydata
    lazydict = LazyDict()
    if lazyattrlist is not None and objectlazydata is None:
        for a in lazyattrlist:
            lazydict[a] = getattr(obj, a, None)

    if getattr(fd, 'memo', None) is None:
        fd = Memoizer(fd)
    ref = str(id(obj))
    if ref in fd.memo:
        ber.Tag.from_tag(PYOBJ_REF_TAG, len(ref)).write(fd)
        fd.write(ref)
        return
    fd.memo[ref] = obj
    if not omittag:
        ber.Tag.from_tag(PYOBJ_TAG, None).write(fd)
    b = ber.BERStream(fd)
    b.add(ref)
    b.add(type(obj).__name__)
    b.add(type(obj).__module__)
    b.add(attrdict)
    b.add(lazydict)
    b._add_eof()
    return


@ber.decoder(PYOBJ_TAG)
def decode_pyobj(fd, tag):
    if getattr(fd, 'memo', None) is None:
        fd = Memoizer(fd)
    b = ber.BERStream(fd, tag.size)
    ref = b.next()
    typename = b.next()
    modulename = b.next()
    module = sys.modules.get(modulename, None)
    if module is None:
        raise ber.BERException('Unable to find module %r' % (modulename,))
    cls = getattr(module, typename, None)
    if cls is None:
        raise ber.BERException('Unable to find class %r in module %r' % (typename, modulename))
    obj = cls.__new__(cls)
    fd.memo[ref] = obj
    setlazydata = False
    attrs = b.next()
    for (k, v) in attrs.iteritems():
        setattr(obj, k, v)
        if k == '_spoon_lazydata':
            setlazydata = True

    lazydata = b.next()
    if setlazydata is False:
        setattr(obj, '_spoon_lazydata', lazydata)
    if b.has_next():
        pass
    obj.post_deserialize()
    return obj


@ber.decoder(PYOBJ_REF_TAG)
def decode_pyobj_ref(fd, tag):
    print 'decode-ref'
    if getattr(fd, 'memo', None) is None:
        raise ber.BERException('Python object reference outside of object cycle == impossible?')
    ref = fd.read(tag.size)
    obj = fd.memo.get(ref, None)
    if obj is None:
        raise ber.BERException('Python object reference to nonexistent entity')
    return obj