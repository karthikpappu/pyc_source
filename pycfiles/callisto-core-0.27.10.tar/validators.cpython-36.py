# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/reporting/validators.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 5666 bytes
import logging, re
from six.moves.urllib.parse import parse_qs, urlsplit
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.forms import URLField
logger = logging.getLogger(__name__)

def _clean_url(url):
    url_field = URLField()
    return url_field.clean(url.strip())


def _get_url_parts(url):
    url = _clean_url(url)
    return urlsplit(url)


def _get_initial_path(url_parts):
    return url_parts[2].strip('/').split('/')[0].lower()


def email_validation_function(value):
    validator = EmailValidator()
    validator(value)
    return value


def phone_validation_function(value):
    if sum(map(str.isdigit, value)) != 10:
        raise ValidationError('Invalid phone number, must be 10 numbers long')
    phone = ''
    for number in re.findall('\\d+', value):
        phone = phone + number

    return phone


def instagram_validation_function(value):
    instagram_re = 'https?:\\/\\/(www\\.)?instagram\\.com\\/([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\\.(?!\\.))){0,28}(?:[A-Za-z0-9_]))?)'
    instagram_url = re.match(instagram_re, value)
    if instagram_url:
        instagram_url = instagram_url.group(0)
        return instagram_url
    raise ValidationError('Invalid instagram account URL.')


generic_twitter_urls = [
 'i',
 'following',
 'followers',
 'who_to_follow',
 'settings',
 'search',
 'tos',
 'privacy',
 'about']

def twitter_validation_function(value):
    path = None
    try:
        url_parts = _get_url_parts(value)
        domain = url_parts[1]
        if not (domain == 'twitter.com' or domain == 'www.twitter.com' or domain == 'mobile.twitter.com'):
            return
        path = _get_initial_path(url_parts)
    except ValidationError:
        if value.startswith('@'):
            path = value[1:]

    if not path or path == '' or len(path) > 15 or path in generic_twitter_urls:
        return
    else:
        return path


generic_fb_urls = [
 'messages',
 'hashtag',
 'events',
 'pages',
 'groups',
 'bookmarks',
 'lists',
 'developers',
 'topic',
 'help',
 'privacy',
 'campaign',
 'policies',
 'support',
 'settings',
 'games',
 'people']

def facebook_validation_function(url):
    try:
        url_parts = _get_url_parts(url)
        domain = url_parts[1]
        if not (domain == 'facebook.com' or domain.endswith('.facebook.com')):
            return
        else:
            path = _get_initial_path(url_parts)
            if path == 'profile.php':
                path = parse_qs(url_parts[3]).get('id')[0]
            if path == 'people':
                path = url_parts[2].strip('/').split('/')[2].lower()
            if not path or path == '' or path.endswith('.php') or path in generic_fb_urls:
                return
            return path
    except ValidationError:
        return


def perp_identifiers():
    return {'email':{'label':'WHAT IS THEIR TWITTER HANDLE?', 
      'id':'email', 
      'validation_function':email_validation_function, 
      'example':'', 
      'unique_prefix':'email'}, 
     'twitter':{'label':'WHAT IS THEIR TWITTER HANDLE?', 
      'id':'twitter', 
      'validation_function':twitter_validation_function, 
      'example':'http://www.twitter.com/perpetratorname or @perpetratorname', 
      'unique_prefix':'twitter'}, 
     'facebook':{'label':'WHAT IS THEIR FACEBOOK URL?', 
      'id':'facebook', 
      'validation_function':facebook_validation_function, 
      'example':'http://www.facebook.com/perpetratorname', 
      'unique_prefix':''}, 
     'phone':{'label':'WHAT IS THEIR MOBILE NUMBER?', 
      'id':'phone', 
      'validation_function':phone_validation_function, 
      'example':'(xxx) xxx xxxx', 
      'unique_prefix':'phone'}, 
     'instagram':{'label':'WHAT IS THEIR INSTAGRAM?', 
      'id':'instagram', 
      'validation_function':instagram_validation_function, 
      'example':'http://www.instagram.com/perpetratorname', 
      'unique_prefix':'instagram'}}


def join_list_with_or(lst):
    if len(lst) < 2:
        return lst[0]
    else:
        all_but_last = ', '.join(lst[:-1])
        last = lst[(-1)]
        return ' or '.join([all_but_last, last])


class Validators(object):

    def __init__(self, validator):
        self.validator = validator

    def invalid(self):
        return 'Please enter a valid ' + self.validator['id']

    def titled(self):
        return "Perpetrator's " + self.validator['id']

    def examples(self):
        return 'ex. ' + self.validator['example']