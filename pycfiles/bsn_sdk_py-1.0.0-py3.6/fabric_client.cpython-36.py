# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\fabric_client.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 8361 bytes
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.common.api_requestor import APIRequestor
from bsn_sdk_py.client.bsn_enum import AppCaType
from bsn_sdk_py.until.bsn_logger import log_debug, log_info
from bsn_sdk_py.client.entity import RegisterUser, EnrollUser, ReqChainCode, GetTransaction, GetBlockInfo, GetLedgerInfo, EventRegister, EventQuery, EventRemove, NoTrustTrans

class FabricClient(object):
    __doc__ = '\n    统一fabric应用请求\n    '

    def __init__(self):
        pass

    def set_config(self, config: Config):
        self.config = config

    def build_req_data(self, req_body):
        """
        统一创建请求报文
        :param req_body:
        :return:
        """
        data = {'header':{'userCode':self.config.user_code, 
          'appCode':self.config.app_code}, 
         'body':req_body, 
         'mac':''}
        return data

    def common_request(self, req_url, req_data):
        res = APIRequestor().request_post(req_url, req_data)
        return res

    def register_user(self, name, secret=''):
        """
        用户注册
        :param name: 用户名
        :param secret: 用户密码
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/user/register'
        req_body = {'name':name, 
         'secret':secret}
        register_user = RegisterUser(self.config, name, secret)
        req_data = self.build_req_data(register_user.req_body())
        mac = register_user.sign()
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert register_user.verify(res_data)
        return res_data

    def enroll_user(self, name, secret):
        """
            密钥非托管模式用户证书登记
        :param name:
        :param secret:
        :return:
        """
        if not self.config.app_info['caType'] == AppCaType.AppCaType_NoTrust.value:
            raise AssertionError('只允许密钥非托管模式用户进行证书登记')
        else:
            req_url = self.config.nodeApi + '/api/fabric/v1/user/enroll'
            enroll_user_obj = EnrollUser(name, secret)
            enroll_user_obj.set_config(self.config)
            req_data = self.build_req_data(enroll_user_obj.req_body())
            mac = enroll_user_obj.sign()
            req_data['mac'] = mac
            res_data = self.common_request(req_url, req_data)
            assert enroll_user_obj.verify(res_data)
        enroll_user_obj.save_cert_to_file(res_data['body']['cert'].encode())
        return res_data

    def req_chain_code(self, chainCode, funcName, name='', args=[], transientData: dict={}):
        """
        密钥托管模式交易处理
        :param chainCode:
        :param funcName:
        :param name:
        :param args:
        :param transientData:
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/node/reqChainCode'
        req_chain_code_obj = ReqChainCode(chainCode, funcName, name, args, transientData)
        req_chain_code_obj.set_config(self.config)
        req_data = self.build_req_data(req_chain_code_obj.req_body())
        mac = req_chain_code_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert req_chain_code_obj.verify(res_data)
        return res_data

    def get_transaction(self, txId):
        """
        获取交易信息
        :param txId:
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/node/getTransaction'
        get_transaction_obj = GetTransaction(txId)
        get_transaction_obj.set_config(self.config)
        req_data = self.build_req_data(get_transaction_obj.req_body())
        log_info(req_data)
        mac = get_transaction_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        log_info(res_data)
        assert get_transaction_obj.verify(res_data)
        return res_data

    def get_block_info(self, blockNumber=0, blockHash='', txId=''):
        """
        获取块信息
        :param blockNumber:
        :param blockHash:
        :param txId:
        :return:
        """
        if not any((blockNumber, blockHash, txId)):
            raise AssertionError('blockNumber or blockHash or txId 不可同时为空')
        else:
            req_url = self.config.nodeApi + '/api/fabric/v1/node/getBlockInfo'
            get_block_info_obj = GetBlockInfo(blockNumber, blockHash, txId)
            get_block_info_obj.set_config(self.config)
            req_data = self.build_req_data(get_block_info_obj.req_body())
            mac = get_block_info_obj.sign(req_data)
            req_data['mac'] = mac
            res_data = self.common_request(req_url, req_data)
            assert get_block_info_obj.verify(res_data), '验签失败'
        return res_data

    def get_ledger_info(self):
        """
        获取最新账本信息
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/node/getLedgerInfo'
        get_ledger_info_obj = GetLedgerInfo()
        get_ledger_info_obj.set_config(self.config)
        req_data = self.build_req_data(get_ledger_info_obj.req_body())
        mac = get_ledger_info_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert get_ledger_info_obj.verify(res_data), '验签失败'
        return res_data

    def event_register(self, chainCode, eventKey, notifyUrl, attachArgs=''):
        """
        链码事件注册
        :param chainCode:
        :param eventKey:
        :param notifyUrl:
        :param attachArgs:
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/chainCode/event/register'
        event_register_obj = EventRegister(chainCode, eventKey, notifyUrl, attachArgs)
        event_register_obj.set_config(self.config)
        req_data = self.build_req_data(event_register_obj.req_body())
        mac = event_register_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert event_register_obj.verify(res_data), '验签失败'
        return res_data

    def event_query(self):
        """
        链码事件查询
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/chainCode/event/query'
        event_query_obj = EventQuery()
        event_query_obj.set_config(self.config)
        req_data = self.build_req_data(event_query_obj.req_body())
        mac = event_query_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert event_query_obj.verify(res_data), '验签失败'
        return res_data

    def event_remove(self, eventId):
        """
        链码事件注销
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/chainCode/event/remove'
        event_remove_obj = EventRemove(eventId)
        event_remove_obj.set_config(self.config)
        req_data = self.build_req_data(event_remove_obj.req_body())
        mac = event_remove_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert event_remove_obj.verify(res_data), '验签失败'
        return res_data

    def not_trust_trans(self, chainCode, funcName, name, args: list=[], transientData: dict={}):
        """
        密钥非托管模式交易
        :return:
        """
        req_url = self.config.nodeApi + '/api/fabric/v1/node/trans'
        not_trust_trans_obj = NoTrustTrans(chainCode, funcName, name, args, transientData)
        not_trust_trans_obj.set_config(self.config)
        req_data = self.build_req_data(not_trust_trans_obj.req_body())
        mac = not_trust_trans_obj.sign(req_data)
        req_data['mac'] = mac
        res_data = self.common_request(req_url, req_data)
        assert not_trust_trans_obj.verify(res_data), '验签失败'
        return res_data