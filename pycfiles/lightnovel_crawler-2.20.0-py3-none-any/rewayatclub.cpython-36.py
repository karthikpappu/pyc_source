# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/rewayatclub.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 2794 bytes
import logging, re
from concurrent import futures
from ..utils.crawler import Crawler
logger = logging.getLogger('REWAYAT_CLUB')

class RewayatClubCrawler(Crawler):
    base_url = 'https://rewayat.club/'

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.is_rtl = True
        self.novel_title = soup.select_one('h1.card-header').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.card-body .align-middle img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = soup.select_one('.card-body table td a[href*="/user/"]').text.strip()
        logger.info('Novel author: %s', self.novel_author)
        page_count = len(soup.select('.card-footer select.custom-select option'))
        logger.info('Total pages: %d', page_count)
        logger.info('Getting chapters...')
        futures_to_check = {self.executor.submit(self.download_chapter_list, i + 1):str(i) for i in range(page_count)}
        temp_chapters = dict()
        for future in futures.as_completed(futures_to_check):
            page = int(futures_to_check[future])
            temp_chapters[page] = future.result()

        logger.info('Building sorted chapter list...')
        volumes = set()
        for page in sorted(temp_chapters.keys()):
            for chap in temp_chapters[page]:
                chap['id'] = 1 + len(self.chapters)
                chap['volume'] = 1 + len(self.chapters) // 100
                volumes.add(chap['volume'])
                self.chapters.append(chap)

        self.volumes = [{'id': x} for x in volumes]

    def download_chapter_list(self, page_no):
        chapter_url = self.novel_url + '?page=%d' % page_no
        logger.info('Visiting %s', chapter_url)
        soup = self.get_soup(chapter_url)
        chapters = []
        for a in soup.select('.card a[href*="/novel/"]'):
            chapters.append({'url':self.absolute_url(a['href']), 
             'title':a.select_one('div p').text.strip()})

        return chapters

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        paras = soup.select('.card .card-body p')
        paras = [str(p) for p in paras if p.text.strip()]
        return ''.join(paras)