# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/libs/defaults.py
# Compiled at: 2019-11-14 03:54:14
# Size of source mod 2**32: 4504 bytes
xpath_transform_ext = '"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"'
AUTHOR_PATTERN = [
 '作者[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]',
 '编辑[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]',
 '文[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]',
 '原创[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]',
 '撰文[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]',
 '来源[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：|<]',
 '网[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：|<]',
 '社[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：|<]',
 '责编[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]',
 '责任编辑[：|:| |丨|/]\\s*([一-龥a-zA-Z]{2,20})[^一-龥|:|：]']
DATETIME_PATTERN = [
 '(\\d{4}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{4}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{4}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[0-1]?[0-9]:[0-5]?[0-9])',
 '(\\d{4}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[2][0-3]:[0-5]?[0-9])',
 '(\\d{4}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[1-24]\\d时[0-60]\\d分)([1-24]\\d时)',
 '(\\d{2}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{2}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{2}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[0-1]?[0-9]:[0-5]?[0-9])',
 '(\\d{2}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[2][0-3]:[0-5]?[0-9])',
 '(\\d{2}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2}\\s*?[1-24]\\d时[0-60]\\d分)([1-24]\\d时)',
 '(\\d{4}年\\d{1,2}月\\d{1,2}日\\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{4}年\\d{1,2}月\\d{1,2}日\\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{4}年\\d{1,2}月\\d{1,2}日\\s*?[0-1]?[0-9]:[0-5]?[0-9])',
 '(\\d{4}年\\d{1,2}月\\d{1,2}日\\s*?[2][0-3]:[0-5]?[0-9])',
 '(\\d{4}年\\d{1,2}月\\d{1,2}日\\s*?[1-24]\\d时[0-60]\\d分)([1-24]\\d时)',
 '(\\d{2}年\\d{1,2}月\\d{1,2}日\\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{2}年\\d{1,2}月\\d{1,2}日\\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{2}年\\d{1,2}月\\d{1,2}日\\s*?[0-1]?[0-9]:[0-5]?[0-9])',
 '(\\d{2}年\\d{1,2}月\\d{1,2}日\\s*?[2][0-3]:[0-5]?[0-9])',
 '(\\d{2}年\\d{1,2}月\\d{1,2}日\\s*?[1-24]\\d时[0-60]\\d分)([1-24]\\d时)',
 '(\\d{1,2}月\\d{1,2}日\\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{1,2}月\\d{1,2}日\\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])',
 '(\\d{1,2}月\\d{1,2}日\\s*?[0-1]?[0-9]:[0-5]?[0-9])',
 '(\\d{1,2}月\\d{1,2}日\\s*?[2][0-3]:[0-5]?[0-9])',
 '(\\d{1,2}月\\d{1,2}日\\s*?[1-24]\\d时[0-60]\\d分)([1-24]\\d时)',
 '(\\d{4}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2})',
 '(\\d{2}[-|/|.]\\d{1,2}[-|/|.]\\d{1,2})',
 '(\\d{4}年\\d{1,2}月\\d{1,2}日)',
 '(\\d{2}年\\d{1,2}月\\d{1,2}日)',
 '(\\d{1,2}月\\d{1,2}日)',
 '(\\d{1,2}-\\d{1,2})']
DATETIME_PATTERN_XPATH = [
 "//*[contains(@class,'date')]/text()",
 "//*[contains(@class,'time')]/text()"]
LIST_PATTERN_RE = [
 '<div|ul.*>(<li.*?>.*?<a.*?>.+?</a>.*<p.*?>.+?</p></li>)</div|ul>']
LIST_PATTERN_XPATH = [
 "//div[@class]//a[@target='_blank' and @href]/..",
 "//ul[@class]/li/a[@target='_blank' and @href]/..",
 "//div/ul[@class]/li/a[@href!='']/..",
 '//div[@class]/a']
TITLE_PATTERN_XPATH = [
 '//a/@title',
 '//a/text()[.!=""]',
 f'//*[contains(translate(@class, {xpath_transform_ext}), "title")]/text()[.!=""]']
TITLE_HTAG_XPATH = '//h1//text() | //h2//text() | //h3//text() | //h4//text()'
TITLE_SPLIT_CHAR_PATTERN = '[-_|]'
TITLE_JSON_KEYS = [
 'title']
URL_PATTERN_XPATH = [
 '//a/@href',
 f'//*[contains(translate(@class, {xpath_transform_ext}), "url")]/@href[.!=""]',
 f'//*[contains(translate(@class, {xpath_transform_ext}), "path")]/@href[.!=""]',
 f'//*[contains(translate(@class, {xpath_transform_ext}), "href")]/@href[.!=""]']
URL_JSON_KEYS = [
 'url',
 'href']
URL_PATTERN = [
 '<a .*?href="(.*?)".*?>']
USELESS_TAG = [
 'style', 'script', 'link', 'video', 'iframe', 'source', 'picture', 'header']
TAGS_CAN_BE_REMOVE_IF_EMPTY = [
 'section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']
USELESS_ATTR = [
 'share', 'contribution', 'copyright', 'disclaimer', 'recommend', 'related', 'footer', 'comment',
 'social', 'submeta']