# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/enum/passpol.py
# Compiled at: 2016-12-29 01:49:52
import sys, codecs, logging
from impacket.nt_errors import STATUS_MORE_ENTRIES
from impacket.dcerpc.v5 import transport, samr
from impacket.dcerpc.v5.rpcrt import DCERPCException
from time import strftime, gmtime

class PassPolDump:
    KNOWN_PROTOCOLS = {'139/SMB': ('ncacn_np:%s[\\pipe\\samr]', 139), 
       '445/SMB': ('ncacn_np:%s[\\pipe\\samr]', 445)}

    def __init__(self, connection):
        self.logger = connection.logger
        self.addr = connection.host
        self.protocol = connection.args.smb_port
        self.username = connection.username
        self.password = connection.password
        self.domain = connection.domain
        self.hash = connection.hash
        self.lmhash = ''
        self.nthash = ''
        self.aesKey = None
        self.doKerberos = False
        if self.hash is not None:
            self.lmhash, self.nthash = self.hash.split(':')
        if self.password is None:
            self.password = ''
        return

    def enum(self):
        entries = []
        protodef = PassPolDump.KNOWN_PROTOCOLS[('{}/SMB').format(self.protocol)]
        port = protodef[1]
        logging.info('Trying protocol %s...' % self.protocol)
        rpctransport = transport.SMBTransport(self.addr, port, '\\samr', self.username, self.password, self.domain, self.lmhash, self.nthash, self.aesKey, doKerberos=self.doKerberos)
        dce = rpctransport.get_dce_rpc()
        dce.connect()
        dce.bind(samr.MSRPC_UUID_SAMR)
        resp = samr.hSamrConnect(dce)
        serverHandle = resp['ServerHandle']
        resp = samr.hSamrEnumerateDomainsInSamServer(dce, serverHandle)
        domains = resp['Buffer']['Buffer']
        resp = samr.hSamrLookupDomainInSamServer(dce, serverHandle, domains[0]['Name'])
        resp = samr.hSamrOpenDomain(dce, serverHandle=serverHandle, domainId=resp['DomainId'])
        domainHandle = resp['DomainHandle']
        self.logger.success('Dumping password policy')
        self.get_pass_pol(self.addr, rpctransport, dce, domainHandle)

    def convert(self, low, high, no_zero):
        if low == 0 and hex(high) == '-0x80000000':
            return 'Not Set'
        if low == 0 and high == 0:
            return 'None'
        if no_zero:
            if low != 0:
                high = 0 - (high + 1)
            else:
                high = 0 - high
            low = 0 - low
        tmp = low + high * 4294967296
        tmp *= 1e-07
        try:
            minutes = int(strftime('%M', gmtime(tmp)))
        except ValueError as e:
            return 'BAD TIME:'

        hours = int(strftime('%H', gmtime(tmp)))
        days = int(strftime('%j', gmtime(tmp))) - 1
        time = ''
        if days > 1:
            time = str(days) + ' days '
        elif days == 1:
            time = str(days) + ' day '
        if hours > 1:
            time += str(hours) + ' hours '
        elif hours == 1:
            time = str(days) + ' hour '
        if minutes > 1:
            time += str(minutes) + ' minutes'
        elif minutes == 1:
            time = str(days) + ' minute '
        return time

    def get_pass_pol(self, host, rpctransport, dce, domainHandle):
        resp = samr.hSamrQueryInformationDomain(dce, domainHandle, samr.DOMAIN_INFORMATION_CLASS.DomainPasswordInformation)
        min_pass_len = resp['Buffer']['Password']['MinPasswordLength']
        pass_hst_len = resp['Buffer']['Password']['PasswordHistoryLength']
        self.logger.highlight(('Minimum password length: {}').format(min_pass_len))
        self.logger.highlight(('Password history length: {}').format(pass_hst_len))
        max_pass_age = self.convert(resp['Buffer']['Password']['MaxPasswordAge']['LowPart'], resp['Buffer']['Password']['MaxPasswordAge']['HighPart'], 1)
        min_pass_age = self.convert(resp['Buffer']['Password']['MinPasswordAge']['LowPart'], resp['Buffer']['Password']['MinPasswordAge']['HighPart'], 1)
        self.logger.highlight(('Maximum password age: {}').format(max_pass_age))
        self.logger.highlight(('Minimum password age: {}').format(min_pass_age))
        resp = samr.hSamrQueryInformationDomain2(dce, domainHandle, samr.DOMAIN_INFORMATION_CLASS.DomainLockoutInformation)
        lock_threshold = int(resp['Buffer']['Lockout']['LockoutThreshold'])
        self.logger.highlight(('Account lockout threshold: {}').format(lock_threshold))
        lock_duration = None
        if lock_threshold != 0:
            lock_duration = int(resp['Buffer']['Lockout']['LockoutDuration']) / -600000000
        self.logger.highlight(('Account lockout duration: {}').format(lock_duration))
        return