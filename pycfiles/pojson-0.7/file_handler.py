# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pojen/file_handler.py
# Compiled at: 2016-08-26 17:24:53
import os
sep = os.path.sep

def read(path):
    to_read = open(path, 'r')
    content = to_read.read()
    to_read.close()
    return content


def save(path, content):
    to_write = open(path, 'w+')
    to_write.write(content)
    to_write.close()


def create_folder_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def file_exsits(path):
    return os.path.exists(path)