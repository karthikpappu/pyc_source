# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/novelringan.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 1991 bytes
import json, logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('NOVELRINGAN')

class NovelRinganCrawler(Crawler):
    base_url = 'https://novelringan.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1.entry-title').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('div.imgprop img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = 'Translated by novelringan.com'
        logger.info('Novel author: %s', self.novel_author)
        for a in reversed(soup.select('.bxcl ul li a')):
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id // 100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'url':self.absolute_url(a['href']), 
             'title':a.text.strip() or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        soup.select_one('#bacotan').extract()
        contents = soup.select('.entry-content p')
        body = [str(p) for p in contents if p.text.strip()]
        return '<p>' + '</p><p>'.join(body) + '</p>'