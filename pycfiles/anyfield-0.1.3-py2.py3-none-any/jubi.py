# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/jubi.py
# Compiled at: 2018-04-27 06:35:44
from anyex.btcbox import btcbox

class jubi(btcbox):

    def describe(self):
        return self.deep_extend(super(jubi, self).describe(), {'id': 'jubi', 
           'name': 'jubi.com', 
           'countries': 'CN', 
           'rateLimit': 1500, 
           'version': 'v1', 
           'has': {'CORS': False, 
                   'fetchTickers': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766581-9d397d9a-5edd-11e7-8fb9-5d8236c0e692.jpg', 
                    'api': 'https://www.jubi.com/api', 
                    'www': 'https://www.jubi.com', 
                    'doc': 'https://www.jubi.com/help/api.html'}})

    def fetch_markets(self):
        markets = self.publicGetAllticker()
        keys = list(markets.keys())
        result = []
        for p in range(0, len(keys)):
            id = keys[p]
            base = id.upper()
            quote = 'CNY'
            symbol = base + '/' + quote
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            result.append({'id': id, 
               'symbol': symbol, 
               'base': base, 
               'quote': quote, 
               'info': id})

        return result