# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\romanticlb.py
# Compiled at: 2020-05-04 20:07:05
# Size of source mod 2**32: 3757 bytes
import logging, re
from bs4 import BeautifulSoup
from utils.crawler import Crawler
logger = logging.getLogger('ROMANTIC_LOVE_BOOKS')
ajaxchapter_url = 'https://www.romanticlovebooks.com/home/index/ajaxchapter'

class RomanticLBCrawler(Crawler):
    base_url = [
     'https://m.romanticlovebooks.com/',
     'https://www.romanticlovebooks.com/']

    def initialize(self):
        self.home_url = 'https://www.romanticlovebooks.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        url = self.novel_url.replace('https://m.romanticlovebooks', 'https://www.romanticlovebooks')
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        self.novel_title = soup.select_one('body > div > div.rt > h1').text.strip()
        self.novel_cover = self.absolute_url(soup.select_one('body > div > div.lf > img')['src'])
        for info in soup.select('body > div > div.msg > *'):
            text = info.text.strip()
            if text.lower().startswith('author'):
                self.novel_author = text
                break
        else:
            chap_id = 0
            for a in soup.select('body > div.mulu ul')[(-1)].select('li a'):
                vol_id = chap_id // 100 + 1
                if vol_id > len(self.volumes):
                    self.volumes.append({'id':vol_id, 
                     'title':'Volume %d' % vol_id})
                chap_id += 1
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'title':a['title'], 
                 'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one('#content')
        body = self.extract_contents(contents)
        return '<p>' + '</p><p>'.join(body) + '</p>'