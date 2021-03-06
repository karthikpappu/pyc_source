# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/enum/uac.py
# Compiled at: 2016-12-29 01:49:52
from cme.remoteoperations import RemoteOperations
from impacket.dcerpc.v5 import rrp

class UAC:

    def __init__(self, connection):
        self.logger = connection.logger
        self.smbconnection = connection.conn
        self.doKerb = False

    def enum(self):
        remoteOps = RemoteOperations(self.smbconnection, self.doKerb)
        remoteOps.enableRegistry()
        ans = rrp.hOpenLocalMachine(remoteOps._RemoteOperations__rrp)
        regHandle = ans['phKey']
        ans = rrp.hBaseRegOpenKey(remoteOps._RemoteOperations__rrp, regHandle, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System')
        keyHandle = ans['phkResult']
        dataType, uac_value = rrp.hBaseRegQueryValue(remoteOps._RemoteOperations__rrp, keyHandle, 'EnableLUA')
        self.logger.success('Enumerating UAC status')
        if uac_value == 1:
            self.logger.highlight('1 - UAC Enabled')
        elif uac_value == 0:
            self.logger.highlight('0 - UAC Disabled')
        rrp.hBaseRegCloseKey(remoteOps._RemoteOperations__rrp, keyHandle)
        remoteOps.finish()