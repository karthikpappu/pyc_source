# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelfull.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 4343 bytes
import re, logging
from concurrent import futures
from utils.crawler import Crawler
logger = logging.getLogger('NOVEL_FULL')
search_url = 'http://novelfull.com/search?keyword=%s'

class NovelFullCrawler(Crawler):
    base_url = 'http://novelfull.com/'

    def search_novel(self, query):
        """Gets a list of (title, url) matching the given query"""
        query = query.strip().lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for div in soup.select('#list-page .archive .list-truyen > .row'):
            a = div.select_one('.truyen-title a')
            info = div.select_one('.text-info a .chapter-text')
            results.append({'title':a.text.strip(), 
             'url':self.absolute_url(a['href']), 
             'info':info.text.strip() if info else ''})

        return results

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        image = soup.select_one('.info-holder .book img')
        self.novel_title = image['alt']
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(image['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        authors = []
        for a in soup.select('.info-holder .info a'):
            if a['href'].startswith('/author/'):
                authors.append(a.text.strip())

        self.novel_author = ', '.join(authors)
        logger.info('Novel author: %s', self.novel_author)
        pagination_link = soup.select_one('#list-chapter .pagination .last a')
        page_count = int(pagination_link['data-page']) if pagination_link else 0
        logger.info('Chapter list pages: %d' % page_count)
        logger.info('Getting chapters...')
        futures_to_check = {self.executor.submit(self.download_chapter_list, i + 1):str(i) for i in range(page_count + 1)}
        [x.result() for x in futures.as_completed(futures_to_check)]
        logger.info('Sorting chapters...')
        self.chapters.sort(key=(lambda x: x['id']))
        logger.info('Adding volumes...')
        mini = self.chapters[0]['volume']
        maxi = self.chapters[(-1)]['volume']
        for i in range(mini, maxi + 1):
            self.volumes.append({'id':i, 
             'title':'Volume %d' % i, 
             'volume':str(i)})

    def download_chapter_list(self, page):
        """Download list of chapters and volumes."""
        url = self.novel_url.split('?')[0].strip('/')
        url += '?page=%d&per-page=50' % page
        soup = self.get_soup(url)
        for a in soup.select('ul.list-chapter li a'):
            title = a['title'].strip()
            chapter_id = len(self.chapters) + 1
            match = re.findall('ch(apter)? (\\d+)', title, re.IGNORECASE)
            if len(match) == 1:
                chapter_id = int(match[0][1])
            volume_id = 1 + (chapter_id - 1) // 100
            match = re.findall('(book|vol|volume) (\\d+)', title, re.IGNORECASE)
            if len(match) == 1:
                volume_id = int(match[0][1])
            data = {'title':title, 
             'id':chapter_id, 
             'volume':volume_id, 
             'url':self.absolute_url(a['href'])}
            self.chapters.append(data)

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('div#chapter-content')
        for ads in content.findAll('div', {'align': 'left'}):
            ads.decompose()

        for ads in content.findAll('div', {'align': 'center'}):
            ads.decompose()

        self.clean_contents(content)
        return str(content)