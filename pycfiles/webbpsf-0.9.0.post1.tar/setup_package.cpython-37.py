# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: astropy_helpers/sphinx/setup_package.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 292 bytes


def get_package_data():
    return {'astropy_helpers.sphinx': [
                                'local/*.inv',
                                'themes/bootstrap-astropy/*.*',
                                'themes/bootstrap-astropy/static/*.*']}