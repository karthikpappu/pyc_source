# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cryptop/cryptop.py
# Compiled at: 2017-12-06 19:43:51
# Size of source mod 2**32: 8619 bytes
import curses, os, sys, re, shutil, configparser, json, pkg_resources, locale, requests, requests_cache
BASEDIR = os.path.join(os.path.expanduser('~'), '.cryptop')
DATAFILE = os.path.join(BASEDIR, 'wallet.json')
CONFFILE = os.path.join(BASEDIR, 'config.ini')
CONFIG = configparser.ConfigParser()
COIN_FORMAT = re.compile('[A-Z]{2,5},\\d{0,}\\.?\\d{0,}')
SORT_FNS = {'coin':lambda item: item[0], 
 'price':lambda item: float(item[1][0]), 
 'held':lambda item: float(item[2]), 
 'val':lambda item: float(item[1][0]) * float(item[2])}
SORTS = list(SORT_FNS.keys())
COLUMN = SORTS.index('val')
ORDER = True
KEY_ESCAPE = 27
KEY_ZERO = 48
KEY_A = 65
KEY_Q = 81
KEY_R = 82
KEY_S = 83
KEY_C = 67
KEY_a = 97
KEY_q = 113
KEY_r = 114
KEY_s = 115
KEY_c = 99

def read_configuration(confpath):
    """Read the configuration file at given path."""
    global CONFIG
    if not os.path.isfile(confpath):
        defaultconf = pkg_resources.resource_filename(__name__, 'config.ini')
        shutil.copyfile(defaultconf, CONFFILE)
    CONFIG.read(confpath)
    return CONFIG


def if_coin(coin, url='https://www.cryptocompare.com/api/data/coinlist/'):
    """Check if coin exists"""
    return coin in requests.get(url).json()['Data']


def get_price(coin, curr=None):
    """Get the data on coins"""
    curr = curr or CONFIG['api'].get('currency', 'USD')
    fmt = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}'
    try:
        r = requests.get(fmt.format(coin, curr))
    except requests.exceptions.RequestException:
        sys.exit('Could not complete request')

    try:
        data_raw = r.json()['RAW']
        return [(data_raw[c][curr]['PRICE'], data_raw[c][curr]['HIGH24HOUR'], data_raw[c][curr]['LOW24HOUR']) for c in coin.split(',') if c in data_raw.keys()]
    except:
        sys.exit('Could not parse data')


def get_theme_colors():
    """ Returns curses colors according to the config"""

    def get_curses_color(name_or_value):
        try:
            return getattr(curses, 'COLOR_' + name_or_value.upper())
        except AttributeError:
            return int(name_or_value)

    theme_config = CONFIG['theme']
    return (
     get_curses_color(theme_config.get('text', 'yellow')),
     get_curses_color(theme_config.get('banner', 'yellow')),
     get_curses_color(theme_config.get('banner_text', 'black')),
     get_curses_color(theme_config.get('background', -1)))


def conf_scr():
    """Configure the screen and colors/etc"""
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    text, banner, banner_text, background = get_theme_colors()
    curses.init_pair(2, text, background)
    curses.init_pair(3, banner_text, banner)
    curses.halfdelay(10)


def str_formatter(coin, val, held):
    """Prepare the coin strings as per ini length/decimal place values"""
    max_length = CONFIG['theme'].getint('field_length', 13)
    dec_place = CONFIG['theme'].getint('dec_places', 2)
    avg_length = CONFIG['theme'].getint('dec_places', 2) + 10
    held_str = '{:>{},.8f}'.format(float(held), max_length)
    val_str = '{:>{},.{}f}'.format(float(held) * val[0], max_length, dec_place)
    return '  {:<5} {:>{}}  {} {:>{}} {:>{}} {:>{}}'.format(coin, locale.currency((val[0]), grouping=True)[:max_length], avg_length, held_str[:max_length], locale.currency((float(held) * val[0]), grouping=True)[:max_length], avg_length, locale.currency((val[1]), grouping=True)[:max_length], avg_length, locale.currency((val[2]), grouping=True)[:max_length], avg_length)


def write_scr(stdscr, wallet, y, x):
    """Write text and formatting to screen"""
    global COLUMN
    global ORDER
    first_pad = '{:>{}}'.format('', CONFIG['theme'].getint('dec_places', 2) + 10 - 3)
    second_pad = ' ' * (CONFIG['theme'].getint('field_length', 13) - 2)
    third_pad = ' ' * (CONFIG['theme'].getint('field_length', 13) - 3)
    if y >= 1:
        stdscr.addnstr(0, 0, 'cryptop v0.2.0', x, curses.color_pair(2))
    if y >= 2:
        header = '  COIN{}PRICE{}HELD {}VAL{}HIGH {}LOW  '.format(first_pad, second_pad, third_pad, first_pad, first_pad)
        stdscr.addnstr(1, 0, header, x, curses.color_pair(3))
    total = 0
    coinl = list(wallet.keys())
    heldl = list(wallet.values())
    if coinl:
        coinvl = get_price(','.join(coinl))
        if y > 3:
            s = sorted((list(zip(coinl, coinvl, heldl))), key=(SORT_FNS[SORTS[COLUMN]]), reverse=ORDER)
            coinl = list(x[0] for x in s)
            coinvl = list(x[1] for x in s)
            heldl = list(x[2] for x in s)
            for coin, val, held in zip(coinl, coinvl, heldl):
                if coinl.index(coin) + 2 < y:
                    stdscr.addnstr(coinl.index(coin) + 2, 0, str_formatter(coin, val, held), x, curses.color_pair(2))
                total += float(held) * val[0]

    if y > len(coinl) + 3:
        stdscr.addnstr(y - 2, 0, 'Total Holdings: {:10}    '.format(locale.currency(total, grouping=True)), x, curses.color_pair(3))
        stdscr.addnstr(y - 1, 0, '[A] Add/update coin [R] Remove coin [S] Sort [C] Cycle sort [0\\Q]Exit', x, curses.color_pair(2))


def read_wallet():
    """ Reads the wallet data from its json file """
    try:
        with open(DATAFILE, 'r') as (f):
            return json.load(f)
    except (FileNotFoundError, ValueError):
        write_wallet({})
        return {}


def write_wallet(wallet):
    """ Write wallet data to its json file """
    with open(DATAFILE, 'w') as (f):
        json.dump(wallet, f)


def get_string(stdscr, prompt):
    """Requests and string from the user"""
    curses.echo()
    stdscr.clear()
    stdscr.addnstr(0, 0, prompt, -1, curses.color_pair(2))
    curses.curs_set(1)
    stdscr.refresh()
    in_str = stdscr.getstr(1, 0, 20).decode()
    curses.noecho()
    curses.curs_set(0)
    stdscr.clear()
    curses.halfdelay(10)
    return in_str


def add_coin(coin_amount, wallet):
    """ Add a coin and its amount to the wallet """
    coin_amount = coin_amount.upper()
    if not COIN_FORMAT.match(coin_amount):
        return wallet
    coin, amount = coin_amount.split(',')
    if not if_coin(coin):
        return wallet
    else:
        if not amount:
            amount = '0'
        wallet[coin] = amount
        return wallet


def remove_coin(coin, wallet):
    """ Remove a coin and its amount from the wallet """
    if coin:
        coin = coin.upper()
        wallet.pop(coin, None)
    return wallet


def mainc(stdscr):
    global COLUMN
    global ORDER
    inp = 0
    wallet = read_wallet()
    y, x = stdscr.getmaxyx()
    conf_scr()
    stdscr.bkgd(' ', curses.color_pair(2))
    stdscr.clear()
    while inp not in {KEY_ZERO, KEY_ESCAPE, KEY_Q, KEY_q}:
        while True:
            try:
                write_scr(stdscr, wallet, y, x)
            except curses.error:
                pass

            inp = stdscr.getch()
            if inp != curses.KEY_RESIZE:
                break
            stdscr.erase()
            y, x = stdscr.getmaxyx()

        if inp in {KEY_a, KEY_A}:
            if y > 2:
                data = get_string(stdscr, 'Enter in format Symbol,Amount e.g. BTC,10')
                wallet = add_coin(data, wallet)
                write_wallet(wallet)
        if inp in {KEY_r, KEY_R}:
            if y > 2:
                data = get_string(stdscr, 'Enter the symbol of coin to be removed, e.g. BTC')
                wallet = remove_coin(data, wallet)
                write_wallet(wallet)
        if inp in {KEY_s, KEY_S}:
            if y > 2:
                ORDER = not ORDER
        if inp in {KEY_c, KEY_C} and y > 2:
            COLUMN = (COLUMN + 1) % len(SORTS)


def main():
    global CONFIG
    if os.path.isfile(BASEDIR):
        sys.exit('Please remove your old configuration file at {}'.format(BASEDIR))
    os.makedirs(BASEDIR, exist_ok=True)
    CONFIG = read_configuration(CONFFILE)
    locale.setlocale(locale.LC_MONETARY, CONFIG['locale'].get('monetary', ''))
    requests_cache.install_cache(cache_name='api_cache', backend='memory', expire_after=(int(CONFIG['api'].get('cache', 10))))
    curses.wrapper(mainc)


if __name__ == '__main__':
    main()