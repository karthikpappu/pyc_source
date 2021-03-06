# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/extend/dingding_robot.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: dingding_robot.py\n@create at: 2017-10-24 10:57\n\n这一行开始写关于本文件的说明与解释\n'
import json
from crwy.spider import BaseSpider
from crwy.exceptions import CrwyExtendException

class DingDingRobot(BaseSpider):

    def __init__(self, access_token=None, api_url='https://oapi.dingtalk.com/robot/send?access_token='):
        super(DingDingRobot, self).__init__()
        if not api_url:
            raise CrwyExtendException('access_token unset.')
        self.api_url = api_url
        self.header = {'Content-Type': 'application/json'}
        self.access_token = access_token
        self.html_downloader.session.headers = self.header

    def send_text(self, content, at_mobiles=list(), is_at_all=False):
        try:
            data = {'text': {'content': content}, 
               'msgtype': 'text', 
               'at': {'isAtAll': is_at_all, 
                      'atMobiles': at_mobiles}}
            res = self.html_downloader.download(self.api_url + self.access_token, method='POST', data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

    def send_markdown(self, title, content, at_mobiles=list(), is_at_all=False):
        try:
            data = {'msgtype': 'markdown', 
               'markdown': {'title': title, 
                            'text': content}, 
               'at': {'atMobiles': at_mobiles, 
                      'isAtAll': is_at_all}}
            res = self.html_downloader.download(self.api_url + self.access_token, method='POST', data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

    def send_action_card(self, title, content, hide_avatar='0', btn_oriengtation='0', single_title='阅读全文', single_url='#'):
        try:
            data = {'actionCard': {'title': title, 
                              'text': content, 
                              'hideAvatar': hide_avatar, 
                              'btnOrientation': btn_oriengtation, 
                              'singleTitle': single_title, 
                              'singleURL': single_url}, 
               'msgtype': 'actionCard'}
            res = self.html_downloader.download(self.api_url + self.access_token, method='POST', data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

    def send_feed_card(self, links):
        """

        :param links: array[{'title':'', 'messageURL':'', 'picURL':''}]
        :return:
        """
        try:
            data = {'feedCard': {'links': links}, 
               'msgtype': 'feedCard'}
            res = self.html_downloader.download(self.api_url + self.access_token, method='POST', data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)