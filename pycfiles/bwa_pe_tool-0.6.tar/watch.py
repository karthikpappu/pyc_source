# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/watch.py
# Compiled at: 2017-09-14 01:02:46
__doc__ = 'A Binary Watch Presentation'
from __future__ import print_function
import sys, time
__version__ = '1.0.5'
__author__ = 'hellflame'
__url__ = 'https://github.com/hellflame/binary_clock/tree/v' + __version__
__all__ = [
 'glimpse', 'loop_watch']
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
COLORS = ['\x1b[01;34m{}\x1b[00m', '\x1b[01;34m{}\x1b[00m',
 '\x1b[01;35m{}\x1b[00m', '\x1b[01;35m{}\x1b[00m',
 '\x1b[01;31m{}\x1b[00m',
 '\x1b[01;36m{}\x1b[00m', '\x1b[01;36m{}\x1b[00m',
 '\x1b[01;32m{}\x1b[00m', '\x1b[01;32m{}\x1b[00m',
 '\x1b[01;33m{}\x1b[00m', '\x1b[01;33m{}\x1b[00m']
THEMES = {'raw': None, 
   'smallBox': ('□', '■'), 
   'bigBox': ('▢', '▩'), 
   'boxSimple': ('-', '▣'), 
   'boxBlank': (' ', '▣'), 
   'circleSimple': ('-', '◉'), 
   'circleBlank': (' ', '◉'), 
   'rhombusSimple': ('-', '◈'), 
   'rhombusBlank': (' ', '◈'), 
   'plusSimple': ('-', '+'), 
   'plusBlank': (' ', '+')}

def transpose(n):
    """
    convert decimal to binary matrix (transposition), at most 4 bits deep ( because 9 < 15 )
    `numpy` seems not always available, or it will be much easier to do so using `numpy.concatenate`

    progress like:
        n => bin(n) => [[0, 1, ...], [1, 1, ...], [1, 0, ...], [0, 0, ... ]]
    eg:
        n = '17'
    =>  ['0001', '0111'] 
    =>  [[0, 0], [0, 1], [0, 1], [1, 1]]

    if print in the console, it may look like this:
    from:
        0 0 0 1
        0 1 1 1
    to:
        0 0
        0 1
        0 1
        1 1

    :param n: str (decimal int value)
    :return: list of 4 lists
    """
    tmp = [ ('{:0>4}').format(('{:b}').format(int(s))) for s in n ]
    return [ [ tmp[index][i] for index in range(len(tmp)) ] for i in range(4) ]


def theme_print(theme, text, color=False):
    """
    print transposed text in the console

    :param theme: str
    :param text: list of 4 lists
    :param color: bool
    :return: None
    """
    if color:
        if len(text[0]) == 11:
            for line in text:
                if THEMES.get(theme):
                    print((' ').join([ COLORS[i].format(THEMES[theme][int(x)]) for i, x in enumerate(line) ]))
                else:
                    print((' ').join([ COLORS[i] for i, x in enumerate(line) ]))

        else:
            for line in text:
                if THEMES.get(theme):
                    print((' ').join([ COLORS[(i + 5)].format(THEMES[theme][int(x)]) for i, x in enumerate(line) ]))
                else:
                    print((' ').join([ COLORS[(i + 5)].format(x) for i, x in enumerate(line) ]))

    else:
        for line in text:
            if THEMES.get(theme):
                print((' ').join([ THEMES[theme][int(x)] for x in line ]))
            else:
                print((' ').join(line))


def glimpse(theme='boxSimple', full=False, hint=False, color=False, universal=False, timezone=None):
    """
    show a glimpse of localtime

    :param theme: print style choice
    :param full: set True to print full length date time string
    :param hint: set True to print human-readable date time or else, programmer-readable date time
    :param color: set True to print colorful columns, more easy to read
    :param universal: set True to print utc time
    :param timezone: set Time zone

    :type theme: str
    :type full: bool
    :type hint: bool
    :type color: bool
    :type universal: bool
    :type timezone: None
    :return: None
    """
    if timezone is None:
        if universal:
            t = time.gmtime()
        else:
            t = time.localtime()
    else:
        t = time.gmtime(time.time() + int(timezone) * 3600)
    if theme == 'basic':
        if full:
            if hint:
                print(('{} | Month : {:>2}').format(('       ').join(('{:b}').format(t.tm_mon).rjust(4)), t.tm_mon))
                print(('{} |   Day : {:>2}').format(('     ').join(('{:b}').format(t.tm_mday).rjust(5)), t.tm_mday))
                print(('{} |  Week : {:>2}').format(('       ').join(('{:b}').format(t.tm_wday + 1).rjust(4)), t.tm_wday + 1))
            else:
                print(('{}').format(('       ').join(('{:b}').format(t.tm_mon).rjust(4))))
                print(('{}').format(('     ').join(('{:b}').format(t.tm_mday).rjust(5))))
                print(('{}').format(('       ').join(('{:b}').format(t.tm_wday + 1).rjust(4))))
        if hint:
            print(('{} |  Hour : {:>2}').format(('     ').join(('{:b}').format(t.tm_hour).rjust(5)), t.tm_hour))
            print(('  {}   |   Min : {:>2}').format(('   ').join(('{:b}').format(t.tm_min).rjust(6)), t.tm_min))
            print(('  {}   |   Sec : {:>2}').format(('   ').join(('{:b}').format(t.tm_sec).rjust(6)), t.tm_sec))
        else:
            print(('{}').format(('     ').join(('{:b}').format(t.tm_hour).rjust(5))))
            print(('  {}   ').format(('   ').join(('{:b}').format(t.tm_min).rjust(6))))
            print(('  {}   ').format(('   ').join(('{:b}').format(t.tm_sec).rjust(6))))
    elif theme in THEMES:
        if full:
            raw = ('{month:0>2}{day:0>2}{week}{hour:0>2}{min:0>2}{sec:0>2}').format(month=t.tm_mon, day=t.tm_mday, week=t.tm_wday + 1, hour=t.tm_hour, min=t.tm_min, sec=t.tm_sec)
            result = transpose(raw)
            if hint:
                theme_print(theme, result, color)
                print('_' * 21)
                print('M M D D W h h m m s s')
                print((' ').join(raw))
            else:
                theme_print(theme, result, color)
        else:
            raw = ('{hour:0>2}{min:0>2}{sec:0>2}').format(hour=t.tm_hour, min=t.tm_min, sec=t.tm_sec)
            result = transpose(raw)
            if hint:
                theme_print(theme, result, color)
                print('___________')
                print('h h m m s s')
                print((' ').join(raw))
            else:
                theme_print(theme, result, color)
    return


def loop_watch(theme='basic', full=True, hint=True, color=False, universal=False, timezone=None):
    """
    start watch click, control-C to stop, 
    this basically just keep calling `glimpse` 

    :param theme: print style choice
    :param full: set True to print full length date time string
    :param hint: set True to print human-readable date time or else, programmer-readable date time
    :param color: set True to print colorful columns, more easy to read
    :param universal: set True to print utc time
    :param timezone: set Time zone

    :type theme: str
    :type full: bool
    :type hint: bool
    :type color: bool
    :type universal: bool
    :type timezone: None
    :return: None
    """
    try:
        while True:
            glimpse(theme, full, hint, color, universal, timezone)
            if theme == 'basic':
                if full:
                    sys.stdout.write('\x1b[F\x1b[F\x1b[F\x1b[F\x1b[F\x1b[F')
                else:
                    sys.stdout.write('\x1b[F\x1b[F\x1b[F')
            elif theme in THEMES:
                if hint:
                    sys.stdout.write('\x1b[F' * 7)
                else:
                    sys.stdout.write('\x1b[F\x1b[F\x1b[F\x1b[F')
            time.sleep(0.05)

    except KeyboardInterrupt:
        if theme == 'basic':
            if full:
                sys.stdout.write('\n\n\n\n\n\n')
            else:
                sys.stdout.write('\n\n\n')
        elif theme in THEMES:
            if hint:
                sys.stdout.write('\n\n\n\n\n\n\n')
            else:
                sys.stdout.write('\n\n\n\n')


def terminal():
    """
    command line entry
    """
    import argparse

    def available_themes(s):
        if s not in THEMES and not s == 'basic':
            raise argparse.ArgumentTypeError(('`{}` is not a supported theme.\n`basic / {}` are available').format(s, (' / ').join(THEMES.keys())))
        return s

    parser = argparse.ArgumentParser(description=__doc__, epilog='More Info, visit ' + __url__)
    parser.add_argument('--hint', action='store_true', help='show easy read time outputs')
    parser.add_argument('-nc', '--no-color', action='store_true', help='supress color output')
    parser.add_argument('-g', '--glimpse', action='store_true', help='show only one moment time')
    parser.add_argument('-f', '--full', action='store_true', help='output Month, Day, Week')
    parser.add_argument('-l', '--list-theme', action='store_true', help='list available themes')
    parser.add_argument('-v', '--version', action='store_true', help='display version info')
    parser.add_argument('-u', '--universal', action='store_true', help='use utc time instead of localtime')
    parser.add_argument('-z', '--zone', help='set timezone', type=int)
    parser.add_argument('-t', '--theme', default='boxSimple', type=available_themes, help='choose output theme, default `boxSimple`.')
    args = parser.parse_args()
    if args.list_theme:
        print('These are available themes:\nbasic')
        print(('\n').join(THEMES.keys()))
    elif args.version:
        print('binary watch version: ' + __version__)
    elif args.glimpse:
        glimpse(args.theme, full=args.full, hint=args.hint, color=not args.no_color, universal=args.universal, timezone=args.zone)
    else:
        loop_watch(args.theme, full=args.full, hint=args.hint, color=not args.no_color, universal=args.universal, timezone=args.zone)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        import unittest, random

        class TransTest(unittest.TestCase):
            """transpose test cases"""

            def random_gen(self, length):
                target = ('').join([ random.choice('0123456789') for _ in range(length) ])
                rand_choice = random.choice(range(length))
                self.assertListEqual(list(('{:0>4}').format(('{:b}').format(int(target[rand_choice])))), [ transpose(target)[i][rand_choice] for i in range(4) ])

            def test_simple(self):
                self.assertListEqual([['0', '0'], ['0', '1'], ['0', '1'], ['1', '1']], transpose('17'))

            def test_complex(self):
                self.random_gen(1)
                self.random_gen(3)
                self.random_gen(50)
                self.random_gen(100)
                self.random_gen(200)

            def test_empty(self):
                self.assertListEqual([[], [], [], []], transpose(''))

            def test_very_long(self):
                self.random_gen(1048576)

            def test_keep_always(self):
                target = ('').join([ random.choice('0123456789') for _ in range(100) ])
                self.assertListEqual(transpose(target), transpose(target))

            def test_level1_depth(self):
                self.assertEqual(len(transpose(('').join([ random.choice('0123456789') for _ in range(100)
                                                         ]))), 4)

            def test_level2_depth(self):
                self.assertEqual(len(transpose(('').join([ random.choice('0123456789') for _ in range(100)
                                                         ]))[0]), 100)


        unittest.main()
    else:
        terminal()