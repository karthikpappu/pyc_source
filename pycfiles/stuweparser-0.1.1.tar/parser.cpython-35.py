# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trybnetic/Documents/projects/stuweparser/stuweparser/parser.py
# Compiled at: 2017-11-02 19:34:26
# Size of source mod 2**32: 1958 bytes
"""
parser.py provides functionality to parse the websites of `my-stuwe.de
<https://www.my-stuwe.de/>`_
"""
from collections import namedtuple
from bs4 import BeautifulSoup

def parse_current_day(html):
    """
    Parses a html string for the current day

    - **parameters**, **types**, **return** and **return types**::
        :param html: a html string from a website
        :type html: string
        :return: the current day
        :rtype: string
    """
    parser = BeautifulSoup(html, 'html.parser')
    day = parser.find_all('span', class_='speiseplan2-wochentag')[0].string
    return day


def parse_current_date(html):
    """
    Parses a html string for the current date

    - **parameters**, **types**, **return** and **return types**::
        :param html: a html string from a website
        :type html: string
        :return: the current date
        :rtype: string
    """
    parser = BeautifulSoup(html, 'html.parser')
    date = parser.find_all('span', class_='speiseplan2-datum')[0].string
    return date


def parse_menues(html):
    """
    Parses a html string for the current day

    - **parameters**, **types**, **return** and **return types**::
        :param html: a html string from a website
        :type html: string
        :return: a list of the menues of the day
        :rtype: list of collections.namedtuple
    """
    parser = BeautifulSoup(html, 'html.parser')
    table = parser.table.find_all('tr')
    table.pop(0)
    menues = []
    menue_tuple = namedtuple('Menue', 'name food student_price guest_price')
    for row in table:
        col = row.find_all('td')
        menue = menue_tuple(name=col[0].string, food=col[1].string, student_price=col[2].string, guest_price=col[3].string)
        menues.append(menue)

    return menues