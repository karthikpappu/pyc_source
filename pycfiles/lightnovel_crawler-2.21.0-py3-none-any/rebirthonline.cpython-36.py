# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/rebirthonline.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3522 bytes
import logging, re
from bs4 import BeautifulSoup
from ..utils.crawler import Crawler
logger = logging.getLogger('REBIRTH_ONLINE')
book_url = 'https://www.rebirth.online/novel/%s'

class RebirthOnlineCrawler(Crawler):
    base_url = 'https://www.rebirth.online/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        self.novel_id = self.novel_url.split('rebirth.online/novel/')[1].split('/')[0]
        logger.info('Novel Id: %s', self.novel_id)
        self.novel_url = book_url % self.novel_id
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h2.entry-title a').text
        logger.info('Novel title: %s', self.novel_title)
        translator = soup.find('h3', {'class': 'section-title'}).findNext('p').text
        author = soup.find('h3', {'class': 'section-title'}).findNext('p').findNext('p').text
        self.novel_author = 'Author : %s, Translator: %s' % (
         author, translator)
        logger.info('Novel author: %s', self.novel_author)
        self.novel_cover = None
        logger.info('Novel cover: %s', self.novel_cover)
        last_vol = -1
        volume = {'id':0,  'title':'Volume 1'}
        for item in soup.find('div', {'class': 'table_of_content'}).findAll('ul'):
            vol = volume.copy()
            vol['id'] += 1
            vol['title'] = 'Book %s' % vol['id']
            volume = vol
            self.volumes.append(volume)
            for li in item.findAll('li'):
                chap_id = len(self.chapters) + 1
                a = li.select_one('a')
                self.chapters.append({'id':chap_id, 
                 'volume':vol['id'], 
                 'url':self.absolute_url(a['href']), 
                 'title':a.text.strip() or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        self.blacklist_patterns = [
         '^translat(ed by|or)',
         '(volume|chapter) .?\\d+']
        if len(soup.findAll('br')) > 10:
            contents = soup.find('br').parent
        else:
            remove = [
             'http://www.rebirth.online', 'support Content Creators', 'content-copying bots',
             "Firefox Reader's Mode", 'content-stealing websites', 'rebirthonlineworld@gmail.com',
             'PayPal\xa0or\xa0Patreon', 'available for\xa0Patreons', 'Join us on Discord', 'enjoy this novel']
            contents = soup.find('div', {'class': 'obstruction'}).select('p')
            for content in contents:
                for item in remove:
                    if item in content.text:
                        content.decompose()

            tmp = ''
            for content in contents:
                tmp = tmp + '<p>' + content.text + '</p>'
                contents = BeautifulSoup(tmp, 'lxml')

        return str(contents)