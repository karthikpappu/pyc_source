# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/backend/daemonrpc.py
# Compiled at: 2016-01-06 16:54:44
# Size of source mod 2**32: 2649 bytes
import requests, json, logging, time
from .backend import *
from .. import config
logger = logging.getLogger(config.APP_NAME)

class DaemonRPC(Backend):
    SUPPORTED_CHAINS = [
     'BTC', 'XTN', 'DOGE', 'LTC', 'XLT', 'XDT']

    def __init__(self, chain, host, port, user, password, ssl):
        self.chain = chain
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl
        self.url = 'http' + ('s' if self.ssl else '') + '://' + self.user + ':' + self.password + '@' + self.host + ':' + self.port
        self.headers = {'content-type': 'application/json'}

    def _rpc(self, command, args=[]):
        while True:
            try:
                payload = {'method': command, 
                 'params': args, 
                 'jsonrpc': '2.0', 
                 'id': 0}
                response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()
                if 'error' in response and response['error'] != None and response['error']['code'] == -28:
                    logger.warning('The rpc server is syncing. Retrying in 5 seconds')
                    time.sleep(5)
                else:
                    return response
            except Exception as e:
                logger.error('Unable to connect. Retrying in 5 seconds...')
                time.sleep(5)

    def getChainCode(self):
        responseh = self._rpc('help')['result']
        response = self._rpc('getinfo')
        tn = response['result']['testnet']
        if responseh.find('litecoin') != -1:
            if bool(tn):
                return 'XLT'
            else:
                return 'LTC'
        else:
            if responseh.find('bitcoin') != -1:
                if bool(tn):
                    return 'XTN'
                else:
                    return 'BTC'
            elif responseh.find('dogecoin') != -1:
                if bool(tn):
                    return 'XDT'
                return 'DOGE'
        return 'UNK'

    def connect(self):
        try:
            code = self.getChainCode()
            if code == self.chain:
                return True
            else:
                logger.critical('Using rpc of wrong chain (%s <> %s)', code, self.chain)
                return False
        except:
            return False

    def getLastBlockHeight(self):
        response = self._rpc('getblockcount')
        return int(response['result'])

    def getBlockHash(self, index):
        response = self._rpc('getblockhash', [index])
        return response['result']

    def getBlockByHash(self, bhash):
        response = self._rpc('getblock', [bhash])
        return response['result']

    def broadcastTransaction(self, transaction):
        response = self._rpc('sendrawtransaction', [transaction])
        return response['result']

    def getTransaction(self, txid):
        response = self._rpc('getrawtransaction', [txid])
        return response['result']