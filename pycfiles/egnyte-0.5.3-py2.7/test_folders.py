# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/tests/test_folders.py
# Compiled at: 2017-03-15 09:46:43
from __future__ import unicode_literals
from egnyte import exc
from egnyte.tests.config import EgnyteTestCase
FOLDER_NAME = b'Iñtërnâtiônàlizætiøν☃ test'
DESTINATION_FOLDER_NAME = b'destination'
SUB_FOLDER_NAME = b'subfolder'
FILE_IN_FOLDER_NAME = b'test.txt'
FILE_CONTENT = b'TEST FILE CONTENT'

class TestFolders(EgnyteTestCase):

    def setUp(self):
        super(TestFolders, self).setUp()
        self.folder = self.root_folder.folder(FOLDER_NAME)
        self.destination = self.root_folder.folder(DESTINATION_FOLDER_NAME)
        self.file = self.folder.file(FILE_IN_FOLDER_NAME)

    def test_folder_create(self):
        self.folder.create()
        self.assertIsNone(self.folder.check())
        with self.assertRaises(exc.InsufficientPermissions):
            self.folder.create(False)

    def test_folder_recreate(self):
        self.folder.create()
        self.assertIsNone(self.folder.check())
        self.folder.create()
        self.assertIsNone(self.folder.check())

    def test_folder_cannot_recreate(self):
        self.folder.create()
        self.assertIsNone(self.folder.check())
        with self.assertRaises(exc.InsufficientPermissions):
            self.folder.create(False)

    def test_folder_delete(self):
        self.folder.create()
        self.assertIsNone(self.folder.check())
        self.folder.delete()
        with self.assertRaises(exc.NotFound):
            self.folder.check()

    def test_folder_move(self):
        self.folder.create()
        moved = self.folder.move(self.destination.path)
        self.assertEqual(moved.path, self.destination.path, b'Moved folder path should be identical')
        with self.assertRaises(exc.NotFound):
            self.folder.check()

    def test_folder_copy(self):
        self.folder.create()
        copied = self.folder.copy(self.destination.path)
        self.assertEqual(copied.path, self.destination.path, b'Copied folder path should be identical')
        self.assertIsNone(self.folder.check())
        self.assertIsNone(self.destination.check())

    def test_folder_list(self):
        self.folder.create()
        subfolder = self.folder.folder(SUB_FOLDER_NAME).create()
        _file = self.folder.file(FILE_IN_FOLDER_NAME)
        _file.upload(FILE_CONTENT)
        self.folder.list()
        folders_list = self.folder.folders
        self.assertEqual(1, len(folders_list), b'There should be one subfolder')
        self.assertEqual(folders_list[0]._url, subfolder._url, b'Subfolder URLs should be identical')
        files_list = self.folder.files
        self.assertEqual(1, len(files_list), b'There should be one file')
        self.assertEqual(files_list[0]._url, _file._url, b'File URLs should be identical')