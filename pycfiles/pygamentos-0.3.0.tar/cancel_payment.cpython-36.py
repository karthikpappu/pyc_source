# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Documentos/projetos/pypayments/pygamento/cancel_payment.py
# Compiled at: 2020-02-28 18:11:57
# Size of source mod 2**32: 774 bytes
import requests, json

def cancel_payment(**kwargs):
    if kwargs.get('gateway') == 'Ebanx':
        item = {'integration_key':kwargs.get('key'),  'hash':kwargs.get('hash')}
        send = requests.post((kwargs.get('url')['cancel']), data=item)
        r = send.json()
        return r
    if kwargs.get('gateway') == 'PicPay':
        headers = {'content-type':'application/json',  'x-picpay-token':kwargs.get('key')}
        payload = {'authorizationId': kwargs.get('authorization_id')}
        send = requests.post(('https://appws.picpay.com/ecommerce/public/payments/{}/cancellations'.format(kwargs.get('payment_code'))), data=(json.dumps(payload)), headers=headers)
        r = send.json()
        return r