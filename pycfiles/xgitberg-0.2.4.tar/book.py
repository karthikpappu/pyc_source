# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/book.py
# Compiled at: 2016-03-02 11:52:08
import logging, os, shutil, github3, sh
from re import sub
import unicodedata
from .fetch import BookFetcher
from .make import NewFilesHandler, LocalRepo
from .push import GithubRepo
from .util.catalog import BookMetadata
from . import config

class Book:
    """ An index card tells you where a book lives
        `book_id` is PG's unique book id
        `remote_path` is where it lives on PG servers
        `local_path` is where it should be stored locally
    """

    def __init__(self, book_id, repo_name=None, library_path='./library'):
        if repo_name and not book_id:
            self.repo_name = repo_name
            book_id = repo_name.split('_')[(-1)]
        self.book_id = str(book_id)
        self.github_repo = GithubRepo(self)
        try:
            self.library_path = config.data.get('library_path', library_path)
        except:
            self.library_path = library_path

    def parse_book_metadata(self, rdf_library=None):
        if not rdf_library:
            self.meta = BookMetadata(self, rdf_library=config.data.get('rdf_library', ''))
        else:
            self.meta = BookMetadata(self, rdf_library=rdf_library)
        self.format_title()

    @property
    def remote_path(self):
        """ turns an ebook_id into a path on PG's server(s)
            4443  -> 4/4/4/4443/ """
        path_parts = list(self.book_id[:-1])
        path_parts.append(self.book_id)
        return os.path.join(*path_parts) + '/'

    @property
    def local_path(self):
        path_parts = [self.library_path, self.book_id]
        return os.path.join(*path_parts)

    def fetch(self):
        fetcher = BookFetcher(self)
        fetcher.fetch()

    def make(self):
        local_repo = LocalRepo(self)
        logging.debug('preparing to add all git files')
        local_repo.add_all_files()
        local_repo.commit('Initial import from Project Gutenberg')
        file_handler = NewFilesHandler(self)
        file_handler.add_new_files()
        local_repo.add_all_files()
        local_repo.commit('Adds Readme, contributing and license files to book repo')

    def push(self):
        self.github_repo.create_and_push()
        return self.github_repo.repo

    def repo(self):
        if self.repo_name:
            return self.github_repo.github.repository('GITenberg', repo_name)

    def all(self):
        try:
            try:
                self.fetch()
                self.make()
                self.push()
                print ('{0} {1} added').format(self.book_id, self.meta._repo)
            except sh.ErrorReturnCode_12:
                logging.error(('{0} {1} timeout').format(self.book_id, self.meta._repo))
            except sh.ErrorReturnCode_23:
                logging.error(('{0} {1} notfound').format(self.book_id, self.meta._repo))
            except github3.GitHubError as e:
                logging.error(('{0} {1} already').format(self.book_id, self.meta._repo))
            except sh.ErrorReturnCode_1:
                logging.error(('{0} {1} nopush').format(self.book_id, self.meta._repo))

        finally:
            self.remove()

    def remove(self):
        shutil.rmtree(self.local_path)

    def format_title(self):
        """ Takes a string and sanitizes it for Github's url name format """
        _title = unicodedata.normalize('NFD', unicode(self.meta.title))
        out = []
        ok = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM- ',"
        for ch in _title:
            if ch in ok:
                out.append(ch)
            elif unicodedata.category(ch)[0] == 'L':
                out.append(hex(ord(ch)))
            elif ch in '\r\n\t':
                out.append('-')

        _title = sub("[ ',-]+", '-', ('').join(out))
        title_length = 99 - len(str(self.book_id)) - 1
        if len(_title) > title_length:
            repo_title = ('{0}__{1}').format(_title[:title_length], self.book_id)
        else:
            repo_title = ('{0}_{1}').format(_title[:title_length], self.book_id)
        self.meta.metadata['_repo'] = repo_title
        return repo_title