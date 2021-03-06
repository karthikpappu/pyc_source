# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/aegis_model/util/aux_functions.py
# Compiled at: 2020-01-27 21:51:56
# Size of source mod 2**32: 1679 bytes
import datetime, math
from requests import get
from wows_stats.util.ansi_code import AnsiEscapeCode

def check_ip():
    """
    Get external API from REST call
    :return: external ip address of current host
    """
    try:
        ip = get('https://api.ipify.org').text
        print('External ip: {}{}{}'.format(AnsiEscapeCode.BLUE, ip, AnsiEscapeCode.ENDC))
        return ip
    except Exception:
        raise


def check_date():
    """
    Get current date
    :return: current date in "%Y-%m-%d" format
    """
    return datetime.datetime.now().date().strftime('%Y-%m-%d')


def max_hundred(x):
    return int(x / 100) * 100


def greatest_common_divisor(x, y):
    if x == 0 or y == 0:
        return 0
    else:
        if x == y:
            return x
        else:
            negate = False
            if not x > 0 > y:
                if x < 0 < y:
                    negate = True
            else:
                x = abs(x)
                y = abs(y)
                if x > y:
                    r = greatest_common_divisor(x - y, y)
                else:
                    r = greatest_common_divisor(y - x, x)
            if negate:
                r = -r
        return r


def least_common_factor_with_limit(x, y, limit=1000):
    f = greatest_common_divisor(x, y)
    factor = 1
    for i in range(1, min(int(math.sqrt(f)), limit) + 1):
        if f % i == 0:
            factor = i

    return factor


def list_to_url_params(list):
    return ','.join(str(item) for item in list)


def generate_date_list_of_ten_days(date):
    date_format = '%Y-%m-%d'
    date_range = 10
    date_list = list()
    for day in range(date_range):
        date_list.append((date - datetime.timedelta(days=day)).strftime(format=date_format))

    return date_list


if __name__ == '__main__':
    x = greatest_common_divisor(288, 108)
    print(x)