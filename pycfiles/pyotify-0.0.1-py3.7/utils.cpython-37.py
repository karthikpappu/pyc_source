# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyotify\utils.py
# Compiled at: 2020-02-21 17:48:56
# Size of source mod 2**32: 739 bytes
import time, base64

def normalize_scope(scope):
    return ' '.join(sorted(scope.split()))


def is_token_expired(token, offset=60):
    return token['expires_at'] - int(time.time()) < offset


def get_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')
    return {'Authorization': f"Basic {auth_header}"}


def add_custom_values_to_token(token, scope=None):
    token['expires_at'] = token['expires_in'] + int(time.time())
    if scope:
        token['scope'] = scope
    return token


def encode_image(image):
    with open(image, 'rb') as (f):
        enc_str = base64.b64encode(f.read())
    return enc_str