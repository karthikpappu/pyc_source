# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylshvec/__init__.py
# Compiled at: 2019-10-31 12:30:10
# Size of source mod 2**32: 170 bytes
from .lshvec import LSHVec

def set_lshvec_jar_path(jar_path):
    LSHVec.set_lshvec_jar_path(jar_path)


def add_java_options(*args):
    (LSHVec.add_java_options)(*args)