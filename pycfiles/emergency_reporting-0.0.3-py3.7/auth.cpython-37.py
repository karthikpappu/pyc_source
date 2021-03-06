# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emergency_reporting/auth.py
# Compiled at: 2020-05-02 18:50:45
# Size of source mod 2**32: 2694 bytes
import requests, re, datetime
from urllib.parse import urljoin
from .util import BASE_URL
from .excpetion import AuthException
import logging

class Token:

    def __init__(self, access_token, refresh_token, life, received_at):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.life = life
        self.recevied_at = received_at

    def age(self):
        age = datetime.datetime.utcnow() - self.recevied_at
        print(age.seconds)
        return age.seconds

    def token_too_old(self):
        if self.age() > self.life * 0.9:
            return True
        return False


class Auth:

    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.base_url = BASE_URL
        self.code = None
        self.token = None
        self.primary_key = None

    def _get_auth_code(self):
        path = 'auth/Authorize.php'
        data = {'username':self.username, 
         'password':self.password, 
         'client_id':self.client_id, 
         'response_type':'code', 
         'state':'xyz'}
        headers = {'Ocp-Apim-Subscription-Key': self.primary_key}
        r = requests.post((urljoin(self.base_url, path)), data=data, headers=headers)
        if r.ok:
            try:
                self.code = re.search(b'code=(.*)&', r.content).group(1)
            except AttributeError:
                logging.error(r.content)
                logging.error(str(r.status_code))
                raise AuthException

        else:
            logging.error(r.content)
            logging.error(str(r.status_code))
            raise AuthException

    def _get_token(self):
        path = 'authtoken/Token.php'
        data = {'grant_type':'authorization_code', 
         'code':self.code, 
         'client_id':self.client_id, 
         'client_secret':self.client_secret, 
         'redirect_uri':'https://google.com'}
        headers = {'Ocp-Apim-Subscription-Key': self.primary_key}
        r = requests.post((urljoin(self.base_url, path)), data=data, headers=headers)
        self.auth_time = datetime.datetime.utcnow()
        self.token = Token((r.json()['access_token']),
          (r.json()['refresh_token']),
          life=(r.json()['expires_in']),
          received_at=(datetime.datetime.utcnow()))

    def get_token(self):
        self._get_auth_code()
        self._get_token()