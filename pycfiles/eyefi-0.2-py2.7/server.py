# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/server.py
# Compiled at: 2010-11-28 13:32:31
import os, cgi, hashlib, binascii, struct, tarfile, random, datetime, cStringIO as StringIO
from xml.etree import ElementTree as ET
import SOAPpy
from twisted.python import log
from twisted.web import soap, server
from twisted.internet import reactor, defer

def checksum(data):
    data += '\x00' * (-len(data) % 512)
    s = ''
    for i in range(0, len(data), 512):
        a = sum(struct.unpack('<256H', data[i:i + 512]))
        while a >> 16:
            a = (a >> 16) + (a & 65535)

        s += struct.pack('<H', a ^ 65535)

    return s


class EyeFiServer(soap.SOAPPublisher):

    def __init__(self, cards, actions):
        soap.SOAPPublisher.__init__(self)
        self.cards = cards
        self.actions = actions
        reactor.callLater(0, log.msg, 'eyefi server configured and running with cards', cards, 'and actions', actions)

    def render(self, request):
        if request.postpath == ['upload']:
            headers = request.requestHeaders
            content_type = headers.getRawHeaders('content-type')[0]
            typ, pdict = cgi.parse_header(content_type)
            form = cgi.parse_multipart(request.content, pdict)
            data = form['SOAPENVELOPE'][0]
        else:
            form = None
            data = request.content.read()
        p, header, body, attrs = SOAPpy.parseSOAPRPC(data, 1, 1, 1)
        methodName, args, kwargs, ns = (p._name, p._aslist, p._asdict, p._ns)
        if callable(args):
            args = args()
        if callable(kwargs):
            kwargs = kwargs()
        if form:
            kwargs['form'] = form
            args.insert(0, form)
        function = self.lookupFunction(methodName)
        if not function:
            self._methodNotFound(request, methodName)
            return server.NOT_DONE_YET
        else:
            if hasattr(function, 'useKeywords'):
                keywords = {}
                for k, v in kwargs.items():
                    keywords[str(k)] = v

                d = defer.maybeDeferred(function, **keywords)
            else:
                d = defer.maybeDeferred(function, *args)
            d.addCallback(self._gotResult, request, methodName)
            d.addErrback(self._gotError, request, methodName)
            return server.NOT_DONE_YET

    def _gotResult(self, result, request, methodName):
        response = SOAPpy.buildSOAP(kw={'%sResponse' % methodName: result}, encoding=self.encoding)
        self._sendResponse(request, response)

    def soap_StartSession(self, transfermode, macaddress, cnonce, transfermodetimestamp):
        log.msg('StartSession', macaddress)
        m = hashlib.md5()
        m.update(binascii.unhexlify(macaddress + cnonce + self.cards[macaddress]['uploadkey']))
        credential = m.hexdigest()
        snonce = '%x' % random.getrandbits(128)
        self.cards[macaddress]['snonce'] = snonce
        return {'credential': credential, 'snonce': snonce, 
           'transfermode': transfermode, 
           'transfermodetimestamp': transfermodetimestamp, 
           'upsyncallowed': 'false'}

    soap_StartSession.useKeywords = True

    def soap_GetPhotoStatus(self, macaddress, credential, filesignature, flags, filesize, filename):
        log.msg('GetPhotoStatus', macaddress, filename)
        m = hashlib.md5()
        m.update(binascii.unhexlify(macaddress + self.cards[macaddress]['uploadkey'] + self.cards[macaddress]['snonce']))
        want = m.hexdigest()
        assert credential == want, (credential, want)
        return {'fileid': 1, 'offset': 0}

    soap_GetPhotoStatus.useKeywords = True

    def soap_UploadPhoto(self, form, macaddress, encryption, filename, flags, filesize, filesignature, fileid):
        m = hashlib.md5()
        m.update(checksum(form['FILENAME'][0]) + binascii.unhexlify(self.cards[macaddress]['uploadkey']))
        got = m.hexdigest()
        want = form['INTEGRITYDIGEST'][0]
        if not got == want:
            log.msg('upload verification failed', macaddress, got, want)
            return {'success': 'false'}
        else:
            tar = StringIO.StringIO(form['FILENAME'][0])
            names = self.unpack_tar(macaddress, tar)
            reactor.callLater(0, self.run_actions, macaddress, names)
            log.msg('successful upload', macaddress, names)
            return {'success': 'true'}

    soap_UploadPhoto.useKeywords = True

    def unpack_tar(self, macaddress, tar):
        tarfi = tarfile.open(fileobj=tar)
        output = os.path.expanduser(self.cards[macaddress]['folder'])
        if self.cards[macaddress]['date_folders']:
            dat = datetime.datetime.now()
            dat = dat.strftime(self.cards[macaddress]['date_format'])
            output = os.path.join(output, dat)
            if not os.access(output, os.R_OK):
                os.mkdir(output)
        tarfi.extractall(output)
        names = [ os.path.join(output, name) for name in tarfi.getnames()
                ]
        return names

    def run_actions(self, macaddress, names):
        d = defer.succeed((self.cards[macaddress], names))
        for action in self.actions[macaddress]:
            d.addCallback(action)

        d.addCallback(lambda _: log.msg('actions completed on', names))
        d.addErrback(log.msg, 'actions failed on', names)

    def soap_MarkLastPhotoInRoll(self, macaddress, mergedelta):
        log.msg('MarkLastPhotoInRoll', macaddress, mergedelta)
        return {}

    soap_MarkLastPhotoInRoll.useKeywords = True


def build_site(cfg, cards, actions):
    from twisted.web import server, resource
    root = resource.Resource()
    api = resource.Resource()
    root.putChild('api', api)
    soap = resource.Resource()
    api.putChild('soap', soap)
    eyefilm = resource.Resource()
    soap.putChild('eyefilm', eyefilm)
    v1 = EyeFiServer(cards, actions)
    eyefilm.putChild('v1', v1)
    site = server.Site(root)
    return site