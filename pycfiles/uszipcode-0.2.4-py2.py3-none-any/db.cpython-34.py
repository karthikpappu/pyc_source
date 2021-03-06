# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/db.py
# Compiled at: 2019-05-20 14:28:07
# Size of source mod 2**32: 3083 bytes
"""
The dataset for ``uszipcode`` is from multiple source, and integrated by Sanhe Hu.

- 2012-01-22 federal governmanet zipcode data from
  http://federalgovernmentzipcodes.us/
- 2010 zcta2010 population, wage, houseunit, land, water area data from
  from http://proximityone.com/cen2010_zcta_dp.htm
- 2015-10-01 geometry google map geocoding data from http://maps.google.com
"""
from __future__ import print_function
import requests
from pathlib_mate import PathCls as Path
try:
    from .pkg.atomicwrites import atomic_write
    from .pkg.sqlalchemy_mate import engine_creator
except:
    from uszipcode.pkg.atomicwrites import atomic_write
    from uszipcode.pkg.sqlalchemy_mate import engine_creator

db_file_dir = Path.home().append_parts('.uszipcode')
db_file_dir.mkdir(exist_ok=True)
simple_db_file_path = db_file_dir.append_parts('simple_db.sqlite')
db_file_path = db_file_dir.append_parts('db.sqlite')

def is_simple_db_file_exists():
    if simple_db_file_path.exists():
        if simple_db_file_path.size >= 5000000:
            return True
    return False


def is_db_file_exists():
    if db_file_path.exists():
        if db_file_path.size >= 100000000:
            return True
    return False


def connect_to_simple_zipcode_db():
    return engine_creator.create_sqlite(path=simple_db_file_path.abspath)


def connect_to_zipcode_db():
    return engine_creator.create_sqlite(path=db_file_path.abspath)


def download_simple_db_file():
    simple_db_file_download_url = 'https://datahub.io/machu-gwu/uszipcode-0.2.0-simple_db/r/simple_db.sqlite'
    if not is_simple_db_file_exists():
        print('Start downloading data for simple zipcode database, total size 9MB ...')
        response = requests.get(simple_db_file_download_url, stream=True)
        chunk_size = 1048576
        counter = 0
        with atomic_write(simple_db_file_path.abspath, mode='wb', overwrite=True) as (f):
            for chunk in response.iter_content(chunk_size):
                if not chunk:
                    break
                f.write(chunk)
                counter += 1
                print('  %s MB finished ...' % counter)

        print('  Complete!')


def download_db_file():
    db_file_download_url = 'https://datahub.io/machu-gwu/uszipcode-0.2.0-db/r/db.sqlite'
    if not is_db_file_exists():
        print('Start downloading data for rich info zipcode database, total size 450+MB ...')
        response = requests.get(db_file_download_url, stream=True)
        chunk_size = 10485760
        counter = 0
        with atomic_write(db_file_path.abspath, mode='wb', overwrite=True) as (f):
            for chunk in response.iter_content(chunk_size):
                if not chunk:
                    break
                f.write(chunk)
                counter += 10
                print('  %s MB finished ...' % counter)

        print('  Complete!')


if __name__ == '__main__':
    pass