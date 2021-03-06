# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/john/pycharm_workspace/sop/unified_platform/libs/unified/shawty/models.py
# Compiled at: 2012-11-12 17:50:13
"""
Contains all models for working with Shawty in django_shawty.
The ShawtyURL model contains the functionality used to retrieve and store shortened URLs.
"""
import simplejson
from django.db import models
from django.core.cache import cache
from django.conf import settings
import requests
SHAWTY_CACHE_KEY_PREFIX = 'shawty-long-url-'
SHAWTY_SETTING_REQUEST_URL = 'SHAWTY_REQUEST_URL'
SHAWTY_SETTING_USE_DB = 'SHAWTY_USE_DB'
SHAWTY_SETTING_USE_CACHE = 'SHAWTY_USE_CACHING'
SHAWTY_SETTING_CACHE_EXPIRE = 'SHAWTY_CACHE_EXPIRE'

class ShawtyURL(models.Model):
    long_url = models.CharField(max_length=4095, null=False, blank=False, verbose_name='Long URL', help_text='The long URL that was shortened by Shawty')
    short_url = models.CharField(max_length=4095, null=False, blank=False, verbose_name='Short URL', help_text='The short URL corresponding to the long URL')
    short_url_id = models.CharField(max_length=32, null=False, blank=False, verbose_name='Short URL ID', help_text='The short URL ID (everything after /)')
    created_date = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='Created Date', help_text='The date/time this short url was created')
    modified_date = models.DateTimeField(auto_now=True, null=False, blank=False, verbose_name='Modified Date', help_text='The date/time this short url was modified')

    @classmethod
    def get_short_urls(cls, long_urls):
        """
        Gets the short URLs for the given list of long URLs
        @param cls: The ShawtyURL model class
        @param long_urls: A python list of long URLs to get short URLs for, or string of single URL
        @return: A dict of {long_url:short_url} for all the given long urls
        """
        if isinstance(long_urls, basestring):
            long_urls = [
             long_urls]
        output_dict = {}
        if getattr(settings, SHAWTY_SETTING_USE_CACHE):
            for url in long_urls:
                short_url = cache.get(SHAWTY_CACHE_KEY_PREFIX + url)
                if short_url:
                    output_dict[url] = short_url
                    long_urls.remove(url)

        if not long_urls:
            return cls.return_short_urls(output_dict)
        if getattr(settings, SHAWTY_SETTING_USE_DB):
            shawty_urls = cls.objects.filter(long_url__in=long_urls)
            for shawty_url in shawty_urls:
                output_dict[shawty_url.long_url] = shawty_url.short_url
                long_urls.remove(shawty_url.long_url)

        if not long_urls:
            return cls.return_short_urls(output_dict)
        output_dict.update(cls.holla_at_shawty(long_urls))
        return cls.return_short_urls(output_dict)

    @classmethod
    def holla_at_shawty(cls, long_urls):
        """
        Calls the Shawty server and retrieves the output dictionary from Shawty,
        returning it.
        @param cls: The ShawtyURL model class
        @param long_urls: The list of long urls for shawty to shorten
        @return: A dict of {long_url: short_url} for all long_urls
        """
        request_url = getattr(settings, SHAWTY_SETTING_REQUEST_URL)
        if not request_url:
            raise Exception('SHAWTY_REQUEST_URL is not defined in settings! Must be full URL with protocol. Example: http://www.shawty.com')
        response = requests.get(request_url, params={'shorten': simplejson.dumps(long_urls)})
        if not response.ok:
            raise Exception(('Response from Shawty server returned {code}. Cannot shorten URLs.').format(code=response.status_code))
        return response.json

    @classmethod
    def return_short_urls(cls, shortened_url_dict):
        """
        Method called before returning shortened URLs, will cache/store in DB
        if that is specified by config
        @param cls: The ShawtyURL class
        @param shortened_url_dict: A dict containing {long_url:short_url) for all short urls
        @return: Returns the short_url_dict after it has been processed
        """
        if getattr(settings, SHAWTY_SETTING_USE_CACHE):
            cache_expire = getattr(settings, SHAWTY_SETTING_CACHE_EXPIRE, 2592000)
            for long_url, short_url in shortened_url_dict.iteritems():
                cache.set(SHAWTY_CACHE_KEY_PREFIX + long_url, short_url, cache_expire)

        if getattr(settings, SHAWTY_SETTING_USE_DB):
            for long_url, short_url in shortened_url_dict.iteritems():
                short_url_id = short_url.rpartition('/')[2]
                ShawtyURL.objects.get_or_create(long_url=long_url, short_url=short_url, short_url_id=short_url_id)

        return shortened_url_dict

    class Meta:
        verbose_name = 'Shawty URL'
        verbose_name_plural = 'Shawty URLs'