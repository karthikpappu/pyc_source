# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/pyrev/project.py
# Compiled at: 2017-02-20 23:06:00
# Size of source mod 2**32: 37386 bytes
"""
Core functionalities for pyrev = Py:Re:VIEW.

Note to developers:
Though some functions starts with "_" (_log_debug()) and some do not,
any functions may change in the future anyway.
You're be warned! X-(
sorry.
"""
import os, re, shutil, yaml
from functools import reduce
import traceback
r_chap = re.compile('^(?P<level>=+)(?P<column>[column]?)(?P<sp>\\s*)(?P<title>.+)$')
r_re = re.compile('^(.+.re)$')
from logging import getLogger, NullHandler
local_logger = getLogger(__name__)
local_logger.addHandler(NullHandler())

def _verify_filename(source_dir, filename, logger=None):
    """
    Checks if a given file is appropriate to use in drivers.
    Returns an absolute path for the filename. None otherwise.
    """
    logger = logger or local_logger
    abs_path = os.path.abspath(os.path.join(source_dir, filename))
    if source_dir not in abs_path:
        logger.info('"{}" does not point to file in dir "{}".'.format(filename, source_dir))
        return
    if not os.path.exists(abs_path):
        logger.info('"{}" does not exist in "{}".'.format(filename, source_dir))
        return
    if os.path.islink(abs_path):
        logger.info('"{}" is a symlink.'.format(filename))
        return
    logger.debug('"{}" is verified as safe'.format(abs_path))
    return abs_path


def _verify_re_filename(source_dir, filename, logger=local_logger):
    """
    In addition to _is_appropriate_file(), checks if the file name
    looks like a Re:VIEW file (i.e. if the extension is ".re").
    """
    m = r_re.match(filename)
    if not m:
        logger.debug('{} does not look like .re file'.format(filename))
        return
    return _verify_filename(source_dir, filename)


def _is_appropriate_file(source_dir, filename):
    return _verify_filename(source_dir, filename) is not None


def _is_appropriate_re_file(source_dir, filename):
    return _verify_re_filename(source_dir, filename) is not None


def _split_path_into_dirs(path):
    """
    a/b/c/d.txt -> ['a', 'b', 'c', 'd.txt']
    """
    drive, path_and_file = os.path.splitdrive(path)
    dirs = []
    while True:
        path, _dir = os.path.split(path)
        if _dir:
            dirs.append(_dir)
        else:
            if path:
                dirs.append(path)
            break

    dirs.reverse()
    return dirs


class ProjectImage(object):
    __doc__ = '\n    Right now this class supports two types of image structures.\n    1. images/chap1-image1.png\n    2. images/chap1/image1.png\n    '

    def __init__(self, rel_path, parent_filename, image_dir):
        self.parent_filename = parent_filename
        parent_head, parent_tail = os.path.splitext(parent_filename)
        self.parent_id = parent_head
        self.parent_tail = parent_tail
        self.rel_path = rel_path
        self.image_dir = image_dir
        parts = _split_path_into_dirs(self.rel_path)
        assert (len(parts) == 2 or len(parts) == 3) and parts[0] == self.image_dir, 'rel_path: "{}", image_dir: "{}"'.format(self.rel_path, self.image_dir)
        if len(parts) == 3:
            assert parts[1] == self.parent_id
            head, tail = os.path.splitext(parts[2])
            self.id = head
        else:
            head, tail = os.path.splitext(parts[1])
            assert head.startswith('{}-'.format(self.parent_id))
            self.id = head[len(self.parent_id) + 1:]
        assert self.id
        self.tail = tail

    def __str__(self):
        return '{} (parent: {})'.format(self.rel_path, self.parent_filename)


class ReVIEWProject(object):
    __doc__ = '\n    Represents a whole Re:VIEW project in a single directory,\n    which should contain config.yml, catalog.yml, etc.\n    '
    RELATED_FILES = set(['config.yml', 'config.yaml',
     'catalog.yml', 'catalog.yaml',
     'CHAPS', 'PREDEF', 'POSTDEF', 'PART'])
    BM_TITLE = 'title'
    BM_LEVEL = 'level'
    BM_SOURCE_FILE_NAME = 'source_file_name'
    BM_SOURCE_CHAP_INDEX = 'source_chap_index'
    BM_SP = 'sp'
    BM_IS_COLUMN = 'is_column'

    @staticmethod
    def instantiate(source_dir, **kwargs):
        driver = ReVIEWProject(source_dir, logger=kwargs.get('logger'))
        if driver.init(**kwargs):
            return driver
        else:
            return

    def __init__(self, source_dir, logger=None):
        self.source_dir = os.path.normpath(source_dir)
        self.logger = logger or local_logger
        self._reset()

    def _reset(self):
        self.config_file = None
        self.catalog_file = None
        self._catalog_files = []
        self.source_filenames = []
        self.predef_filenames = []
        self.postdef_filenames = []
        self.draft_filenames = []
        self.parts = None
        self.chaps = None
        self.image_dir = None
        self.images = {}
        self.unmappable_images = []
        self.title = ''
        self.author = ''
        self.description = ''
        self.coverimage = ''
        self.pdf_num_pages = 0
        self.bookmarks = None
        self.chap_to_bookmark = None
        self.ready = False

    def init(self, config_file=None, catalog_file=None, logger=None, **kwargs):
        """
        Initializes this instance.
        Returns True when successful.
        Returns False otherwise, where this instance will not be usable.

        config_file: a filename of a review config file.
        catalog_file: a filename of a review catalog file.
        """
        logger = kwargs.get('logger') or self.logger
        logger.debug('ReVIEWProject.init()')
        if config_file:
            logger.debug('config_file is specified ("{}"). Try pasing it.'.format(config_file))
            if not self._try_parse_config_file(config_file):
                logger.error('Failed to parse config file "{}"'.format(config_file))
                return False
        else:
            logger.debug('config_file is not specified. Find suitable one.')
            if not self._find_and_parse_config_file():
                logger.info('Failed to find config.yml or relevant.')
                return False
            assert self.bookname is not None
            if not self.config_file is not None:
                raise AssertionError
        if catalog_file:
            logger.debug('catalog_file is specified ("{}"). Try parsing it.'.format(catalog_file))
            if not self._try_parse_catalog_file(catalog_file):
                logger.error('Failed to parse catalog file "{}"'.format(catalog_file))
                return False
        else:
            logger.debug('catalog_file is not specified. Find suitable one(s).')
            if not self._recognize_catalog_files():
                logger.info('Failed to find config.yml or relevant.')
                return False
            if self.parts is None and self.chaps is None:
                self.logger.warn('Failed to recognize book structure in {}.'.format(self.source_dir))
                return False
            if not self.parts:
                if not self.parts:
                    self.logger.info('No chapter found.')
            self._recognize_draft_files()
            self.image_dir = kwargs.get('image_dir', 'images')
            self.image_dir_path = os.path.normpath('{}/{}'.format(self.source_dir, self.image_dir))
            self.images = {}
            if os.path.isdir(self.image_dir_path):
                self._recognize_image_files()
            else:
                self.logger.info('"{}"({}) is not a directory'.format(self.image_dir, self.image_dir_path))
        self._log_debug()
        self.ready = True
        return True

    def _find_and_parse_config_file(self, logger=None):
        logger = logger or self.logger
        candidates = ['config.yml', 'config.yaml',
         'sample.yml', 'sample.yaml']
        for candidate in candidates:
            if self._try_parse_config_file(candidate):
                logger.debug('"{}" is used as Re:VIEW config file.'.format(candidate))
                return True

        return False

    def _try_parse_config_file(self, candidate, logger=None):
        """
        Try parsing a given config file (e.g. config.yml) and
        check if it is really an appropriate config for Re:VIEW.
        If it looks appropriate, set up member variables too.

        Returns True if parsing the file is successful.
        Returns False otherwise.
        """
        logger = logger or self.logger
        candidate_path = os.path.normpath(os.path.join(self.source_dir, candidate))
        if not os.path.isfile(candidate_path):
            logger.error('Did not find config_file "{}".'.format(candidate))
            return False
        if self.source_dir not in candidate_path:
            logger.error('"{}" is not in source_dir'.format(candidate))
            return False
        try:
            with open(candidate_path) as (f):
                yaml_data = yaml.safe_load(f)
            if 'bookname' in yaml_data:
                self.bookname = yaml_data['bookname']
                self.yaml_data = yaml_data
                self.title = yaml_data.get('booktitle', '')
                self.author = yaml_data.get('aut')
                self.description = yaml_data.get('description', '')
                self.coverimage = yaml_data.get('coverimage', '')
                self.config_file = candidate
                return True
        except Exception as e:
            logger.error('Error during parsing {}: {}'.format(candidate, e))
            for line in traceback.format_exc().rstrip().split('\n'):
                logger.error(line)

        return False

    def _try_parse_catalog_file(self, catalog_file, logger=None):
        """
        Try parsing a single catalog file, which must be in new format
        (so called "catalog yaml"), not older format
        (with PART/CHAPS/PREDEF/POSTDEF).

        Returns True if parsing the file is successful.
        Returns False otherwise.
        """
        logger = logger or self.logger
        catalog_yml_path = _verify_filename(self.source_dir, catalog_file, logger=logger)
        if not catalog_yml_path:
            return False
        logger.debug('catalog_yml path: "{}"'.format(catalog_yml_path))
        with open(catalog_yml_path) as (f):
            yaml_data = yaml.load(f)
        if 'CHAPS' not in yaml_data or type(yaml_data['CHAPS']) is not list or len(yaml_data['CHAPS']) == 0:
            logger.info('CHAPS elem is not appropriate.')
            return False
        predef_filenames = []
        source_filenames = []
        postdef_filenames = []
        source_filenames = []
        parts = None
        chaps = None
        try:
            if yaml_data.get('PREDEF'):
                for filename in [x.strip() for x in yaml_data['PREDEF']]:
                    if not _is_appropriate_file(self.source_dir, filename):
                        logger.info('Ignoring "{}" because the file looks inappropriate (not available, invalid, etc'.format(filename))
                        continue
                    predef_filenames.append(filename)
                    source_filenames.append(filename)

        except:
            logger.waring('Failed to parse PREDEF. Ignoring..')

        chap = yaml_data['CHAPS'][0]
        if type(chap) is dict:
            logger.debug('Considered to be chaps-with-part structure.')
            chaps = None
            parts = []
            for part_content in yaml_data['CHAPS']:
                if len(part_content) != 1:
                    logger.info('Malformed PART content: "{}"'.format(part_content))
                    return False
                part_title, part_chaps = next(iter(part_content.items()))
                if type(part_title) is not str and type(part_title) is not str:
                    logger.info('Malformed PART title: "{}"'.format(part_title))
                    return False
                if not reduce(lambda x, y: x and (type(y) is str or type(y) is str) and _is_appropriate_re_file(self.source_dir, y), part_chaps, True):
                    logger.info('Malformed chaps exist in PART: {}'.format(part_chaps))
                    return False
                parts.append((part_title, part_chaps))
                for filename in part_chaps:
                    source_filenames.append(filename)

        else:
            logger.debug('Considered to be plain chaps without part.')
            chaps = []
            parts = None
        try:
            for filename in [x.strip() for x in yaml_data['CHAPS']]:
                if not _is_appropriate_re_file(self.source_dir, filename):
                    logger.debug('Ignoring {}'.format(filename))
                    continue
                chaps.append(filename)
                source_filenames.append(filename)

        except:
            logger.error('Failed to parse CHAPS. Exitting')
            return False

        try:
            if yaml_data.get('POSTDEF'):
                for filename in [x.strip() for x in yaml_data['POSTDEF']]:
                    if not _is_appropriate_file(self.source_dir, filename):
                        logger.debug('Ignoring {}'.format(filename))
                        continue
                    postdef_filenames.append(filename)
                    source_filenames.append(filename)

        except:
            logger.waring('Failed to parse POSTDEF. Ignoring..')

        self.predef_filenames = predef_filenames
        self.parts = parts
        self.chaps = chaps
        self.postdef_filenames = postdef_filenames
        self.source_filenames = source_filenames
        self.catalog_file = catalog_file
        self._catalog_files.append(catalog_file)
        return True

    def _recognize_catalog_files(self, logger=None):
        """
        Scans new and legacy catalog files to detect a project structure.
        New projects with catalog.yml/catalog.yaml will be prioritized.
        """
        logger = logger or self.logger
        if self._recognize_new_catalog_files(logger=logger):
            return True
        return self._recognize_legacy_catalog_files(logger=logger)

    def _recognize_new_catalog_files(self, logger=None):
        logger = logger or self.logger
        for candidate in ['catalog.yml', 'config.yaml']:
            if self._try_parse_catalog_file(candidate, logger):
                return True

    def _recognize_legacy_catalog_files(self, logger=None):
        """
        Tries recognizing old catalog files (CHAPS, PREDEF, POSTDEF, PART)
        which has been used before Re:VIEW version 1.3.
        """
        logger = logger or self.logger
        chaps_path = _verify_filename(self.source_dir, 'CHAPS', logger)
        if not chaps_path:
            self.logger.error('No valid CHAPS file is available.')
            return False
        self._catalog_files.append('CHAPS')
        catalog_files = []
        predef_filenames = []
        source_filenames = []
        postdef_filenames = []
        source_filenames = []
        parts = None
        chaps = None
        if _is_appropriate_file(self.source_dir, 'PREDEF'):
            catalog_files.append('PREDEF')
            predef_path = os.path.join(self.source_dir, 'PREDEF')
            for line in open(predef_path):
                filename = line.rstrip()
                if not filename:
                    continue
                if not _is_appropriate_file(self.source_dir, filename):
                    logger.debug('Ignore {}'.format(filename))
                    continue
                predef_filenames.append(filename)
                source_filenames.append(filename)

        part_titles = None
        part_path = _verify_filename(self.source_dir, 'PART')
        if part_path:
            logger.debug('Valid PART file exists ({})'.format(part_path))
            part_titles = self._detect_parts(file(part_path))
            logger.debug('part_titles: {}'.format(part_titles))
        if part_titles:
            logger.debug('Valid part information found.')
            parts = []
            current_part = 0
            chaps = None
            part_chaps = []
            for line in open(chaps_path):
                filename = line.rstrip()
                if not filename:
                    if current_part < len(part_titles):
                        parts.append((part_titles[current_part], part_chaps))
                        current_part += 1
                        part_chaps = []
                    else:
                        continue
                        if not _is_appropriate_re_file(self.source_dir, filename):
                            logger.debug('Ignore {}'.format(filename))
                            continue
                        part_chaps.append(filename)
                        source_filenames.append(filename)

            parts.append((part_titles[current_part], part_chaps))
        else:
            logger.debug('No valid part information found.')
            parts = None
            chaps = []
            for line in open(chaps_path):
                filename = line.rstrip()
                if not filename:
                    continue
                if not _is_appropriate_re_file(self.source_dir, filename):
                    logger.debug('Ignore {}'.format(filename))
                    continue
                chaps.append(filename)
                source_filenames.append(filename)

        if _is_appropriate_file(self.source_dir, 'POSTDEF'):
            catalog_files.append('POSTDEF')
            postdef_path = os.path.join(self.source_dir, 'POSTDEF')
            for line in open(postdef_path):
                filename = line.rstrip()
                if not filename:
                    continue
                if not _is_appropriate_file(self.source_dir, filename):
                    logger.debug('Ignore {}'.format(filename))
                    continue
                postdef_filenames.append(filename)
                source_filenames.append(filename)

        self.predef_filenames = predef_filenames
        self.parts = parts
        self.chaps = chaps
        self.postdef_filenames = postdef_filenames
        self.source_filenames = source_filenames
        self.catalog_file = None
        self._catalog_files += catalog_files
        return True

    def _detect_parts(self, part_content):
        part_titles = []
        for line in part_content:
            part_titles.append(line.rstrip())

        return part_titles

    def _recognize_draft_files(self):
        logger = self.logger
        for re_file in [x for x in os.listdir(self.source_dir) if x.endswith('.re')]:
            if re_file not in self.source_filenames:
                self.draft_filenames.append(re_file)
                continue

        return True

    def parse_source_files(self, logger=None):
        """
        Parses all Re:VIEW files and prepare internal structure.
        """
        logger = logger or self.logger
        if self.parts is None and self.chaps is None:
            logger.error('No chaps/parts information is available.')
            return
        logger.debug('parse_source_files()')
        self.bookmarks = []
        self.chap_to_bookmark = {}
        for filename in self.predef_filenames:
            self.parse_single_source_file(filename, 0)

        if self.parts:
            for part in self.parts:
                part_title, part_chaps = part
                self._append_bookmark({self.BM_LEVEL: 1,  self.BM_TITLE: part_title.strip(), 
                 self.BM_SOURCE_FILE_NAME: None, 
                 self.BM_SOURCE_CHAP_INDEX: None})
                for chap in part_chaps:
                    self.parse_single_source_file(chap, 1)

        else:
            for chap in self.chaps:
                self.parse_single_source_file(chap, 0)

        for filename in self.postdef_filenames:
            self.parse_single_source_file(filename, 0)

        return True

    def parse_single_source_file(self, filename, base_level):
        """
        Parses a single source (.re) file.
        Returns a ParseResult object.
        The object may be from "parse_result" argument (if not None),
        or newly created one (if None)

        This may raises Exceptions when the file looks broken and cannot
        recover the failure.
        """
        f = open(os.path.normpath('{}/{}'.format(self.source_dir, filename)), encoding='utf-8-sig')
        chap_index = 0
        for line in f:
            line = line.rstrip()
            m = r_chap.match(line)
            if m:
                level = len(m.group('level'))
                title = m.group('title')
                if level == 1:
                    new_bookmark = {self.BM_LEVEL: base_level + level,  self.BM_TITLE: title.strip(), 
                     self.BM_SOURCE_FILE_NAME: filename, 
                     self.BM_SOURCE_CHAP_INDEX: chap_index}
                    chap_index += 1
                else:
                    new_bookmark = {self.BM_LEVEL: base_level + level,  self.BM_TITLE: title.strip(), 
                     self.BM_SOURCE_FILE_NAME: filename, 
                     self.BM_SOURCE_CHAP_INDEX: None}
                self.bookmarks.append(new_bookmark)
                continue

    def _append_bookmark(self, bookmark):
        self.bookmarks.append(bookmark)
        bm_source_file_name = bookmark.get(self.BM_SOURCE_FILE_NAME)
        bm_chap_index = bookmark.get(self.BM_SOURCE_CHAP_INDEX)
        if bm_source_file_name:
            if bm_chap_index is not None:
                key = (
                 bm_source_file_name, bm_chap_index)
                self.chap_to_bookmark[key] = bookmark

    def remove_tempfiles(self, logger=None):
        """
        Removes possible tempfiles from the project.
        """
        logger = logger or self.logger
        logger.debug('ReVIEWProject.remove_tempfiles()')
        bookname = self.bookname or 'book'
        temp_dirs = [x.format(bookname) for x in ['{}', '{}-pdf', '{}-epub', '{}-log']]
        for temp_dir in temp_dirs:
            dir_path = os.path.join(self.source_dir, temp_dir)
            shutil.rmtree(dir_path, ignore_errors=True)

    def has_part(self):
        if self.parts:
            return True
        else:
            return False

    def has_source(self, re_file):
        return re_file in self.all_filenames()

    def get_images_for_source(self, re_file):
        return self.images.get(re_file, [])

    def all_filenames(self):
        """
        Returns all possible .re files that can be source of output.
        Note draft should come after self.source_filenames.
        """
        return self.source_filenames + self.draft_filenames

    def _recognize_image_files(self):
        if not os.path.isdir(self.image_dir_path):
            self.logger.debug('No image_dir ("{}")'.format(self.image_dir_path))
            return
        parent_filenames = sorted(self.all_filenames())
        image_filenames = sorted(os.listdir(self.image_dir_path))
        i_parents = 0
        i_images = 0
        while i_parents < len(parent_filenames) and i_images < len(image_filenames):
            parent_filename = parent_filenames[i_parents]
            parent_id, _ = os.path.splitext(parent_filename)
            image_filename = image_filenames[i_images]
            rel_path = '{}/{}'.format(self.image_dir, image_filename)
            abs_path = os.path.normpath('{}/{}'.format(self.image_dir_path, image_filename))
            head, tail = os.path.splitext(image_filename)
            if os.path.isdir(abs_path):
                if parent_id == image_filename:
                    for image_filename2 in os.listdir(abs_path):
                        rel_path2 = '{}/{}'.format(rel_path, image_filename2)
                        pi = ProjectImage(rel_path=rel_path2, parent_filename=parent_filename, image_dir=self.image_dir)
                        lst = self.images.setdefault(parent_filename, [])
                        lst.append(pi)

                    i_images += 1
                    i_parents += 1
                else:
                    if parent_id < image_filename:
                        self.images.setdefault(parent_filename, [])
                        i_parents += 1
                    else:
                        self.unmappable_images.append(image_filename)
                        i_images += 1
            elif head.startswith('{}-'.format(parent_id)):
                pi = ProjectImage(rel_path=rel_path, parent_filename=parent_filename, image_dir=self.image_dir)
                lst = self.images.setdefault(parent_filename, [])
                lst.append(pi)
                i_images += 1
            elif parent_id < head:
                self.images.setdefault(parent_filename, [])
                i_parents += 1
            else:
                self.unmappable_images.append(image_filename)
                i_images += 1

    def _get_debug_info(self):
        lst = []
        lst.append('config_file: "{}"'.format(self.config_file))
        if self.catalog_file:
            lst.append('catalog_file: "{}"'.format(self.catalog_file))
        else:
            if self._catalog_files:
                lst.append('catalog_files: {}'.format(self._catalog_files))
            else:
                lst.append('No catalog file.')
            lst.append('source_filenames(len: {}): {}'.format(len(self.source_filenames), self.source_filenames))
            lst.append('predef_filenames(len: {}): {}'.format(len(self.predef_filenames), self.predef_filenames))
            lst.append('postdef_filenames(len: {}): {}'.format(len(self.postdef_filenames), self.postdef_filenames))
            if self.parts:
                lst.append('parts: {}'.format(self.parts))
            else:
                if self.chaps:
                    lst.append('chaps: {}'.format(self.chaps))
                else:
                    lst.append('No parts or chaps')
        return lst

    def _log_debug(self, logger=None):
        logger = logger or self.logger
        for line in self._get_debug_info():
            logger.debug(line)

    def _format_bookmark(self, bookmark):
        return '{} "{}" (source: {}, index: {}'.format('=' * bookmark.get(self.BM_LEVEL, 10), bookmark[self.BM_TITLE], bookmark.get(self.BM_SOURCE_FILE_NAME), bookmark.get(self.BM_SOURCE_CHAP_INDEX))

    def _log_bookmarks(self, logger=None):
        if not logger:
            logger = self.logger
        if self.bookmarks:
            logger.debug('Bookmarks:')
            for i, bookmark in enumerate(self.bookmarks):
                logger.debug(' {}:{}'.format(i, self._format_bookmark(bookmark)))

        else:
            logger.debug('No bookmark')
        if self.chap_to_bookmark:
            logger.debug('chap_to_bookmark:')
            for key in sorted(self.chap_to_bookmark.keys()):
                bookmark = self.chap_to_bookmark[key]
                self.logger.debug(' {}: "{}"'.format(key, bookmark[self.BM_TITLE]))

    @classmethod
    def _look_for_base(cls, base_dir, depth, func):
        files = os.listdir(base_dir)
        if func(files):
            return base_dir
        if depth == 0:
            return
        if depth > 0:
            depth = depth - 1
        for filename in files:
            next_path = os.path.join(base_dir, filename)
            if os.path.isdir(next_path):
                ret = cls._look_for_base(next_path, depth, func)
                if ret:
                    return ret
                continue

    @classmethod
    def _look_for_related_files(cls, base_dir, depth):
        func = lambda files: bool(set(files) & cls.RELATED_FILES)
        return cls._look_for_base(base_dir, depth, func)

    @classmethod
    def _look_for_re_files(cls, base_dir, depth):
        func = lambda files: bool([f for f in files if f.endswith('.re')])
        return cls._look_for_base(base_dir, depth, func)

    @classmethod
    def guess_source_dir(cls, base_dir, depth=-1):
        """
        Tries to find Re:VIEW's source directory (source_dir) under "base_dir".
        Returns the path when successful.
        Returns None on failure.

        If depth is set 0 or positive, this function will
        traverse directories until that depth.
        0 means no traverse. 1 means directories in the
        root will be traversed.
        Negative value means no limit for the search depth.

        For example if a project has a following structure:

         project
         |-- README.md
         `-- article
             |-- catalog.yml
             |-- config.yml
             |-- images
             |   `-- cover.jpg
             |-- layouts
             |   `-- layout.erb
             |-- sty
             |   `-- reviewmacro.sty
             |-- style.css
             `-- review_article.re

        .. this function should receive a path to the project and
        return "(path-to-the-project)/article/".
        When depth is set to 0, this will fail to find the directory instead.
        """
        return cls._look_for_related_files(base_dir, depth) or cls._look_for_re_files(base_dir, depth)