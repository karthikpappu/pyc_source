# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dir2html/copy_files.py
# Compiled at: 2018-11-21 04:57:05
# Size of source mod 2**32: 122 bytes
import shutil

def copy_files(files, destination_folder):
    for f in files:
        shutil.copy(f, destination_folder)