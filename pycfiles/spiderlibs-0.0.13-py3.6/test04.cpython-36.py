# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spiderlib\test04.py
# Compiled at: 2020-03-26 07:21:19
# Size of source mod 2**32: 1569 bytes
import requests, json
url = 'http://192.168.1.90:86/node?_format=hal_json'
headers = {'Content-Type': 'application/hal+json'}
data = {'_links':{'type':{'href': 'http://192.168.1.90:86/rest/type/node/article'}, 
  'http://192.168.1.90:86/rest/relation/node/article/field_tags':{'href': 'http://192.168.1.90:86/taxonomy/term/1?_format=hal_json'}}, 
 'type':{'target_id': 'article'}, 
 'title':{'value': '复活节前复工？纽约市长说别信特朗普虚幻的希望'}, 
 'body':{'value': '\n他在接受福克斯记者采访时解释称，复活节对他来说是特殊的日子，“到时候所有的教堂都塞满了人不是很好吗？”\n\n特朗普的愿望首先遭到民主党人批评，拜登称“特朗普应该闭上嘴，听听专家怎么说”。\n\n而23日特朗普还称，“交通事故造成的死亡更多，但没人要求大家都别开车了。”\n\n美专家：数百万人或因解封死亡\n\n值得注意的是，特朗普在23日的白宫新冠肺炎新闻发布会上说，他支持美国恢复正常生活。\n\n他说：“美国将再次并很快恢复正常，很快。”\n\n据《每日邮报》报道，23日，美国一位健康专家警告说，如果特朗普总统解除对美国的封锁，新冠肺炎将“广泛、迅速、可怕地扩散，数百万人可能会死亡”。    \n    '}}
resp = requests.post(url=url, auth=('root', 'admin'), headers=headers, data=(json.dumps(data)))
print(resp)
print(resp.text)