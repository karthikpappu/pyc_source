# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/interface.py
# Compiled at: 2020-02-01 09:41:35
# Size of source mod 2**32: 2414 bytes
from argparse import ArgumentParser

class Interface:
    __doc__ = 'A wrapper for the command line interface\n    '

    def __init__(self):
        """Creates a parser and parses arguments
        """
        parser = ArgumentParser(description='Picharsso', prog='picharsso')
        commands = parser.add_subparsers(dest='command')
        p_config = commands.add_parser('config', help='show config path')
        p_art = commands.add_parser('art', help='transform image to text art')
        p_art_sub = p_art.add_subparsers(dest='art')
        p_art_helper = ArgumentParser(add_help=False)
        p_art_helper.add_argument('image', type=str, help='path to image')
        p_art_helper.add_argument('-c', '--color', action='store_true', help='keep color', default=False)
        p_art_helper.add_argument('-W', '--width', nargs='?', type=int, help='width of output in characters, flags to fit terminal', metavar='width', default=False)
        p_art_helper.add_argument('-H', '--height', nargs='?', type=int, help='height of output in characters, flags to fit terminal', metavar='height', default=False)
        p_art_helper.add_argument('-o', '--output-type', choices=['ansi', 'html'], default=(self.configuration.output_type), help='type of output')
        p_art_helper.add_argument('-f', '--output-file', type=str, help='path to output file')
        p_art_helper.add_argument('-q', '--quiet', action='store_true', help='disable console output')
        p_ascii = p_art_sub.add_parser('ascii', help='apply ASCII', parents=[p_art_helper])
        p_ascii.add_argument('-s', '--charset', type=int, help='choice of charset (options available in config)', choices=(range(len(self.configuration.charsets))), default=(self.configuration.charset))
        p_ascii.add_argument('-n', '--negative', action='store_true', help='reverse grayscale')
        p_braille = p_art_sub.add_parser('braille', help='apply Braille', parents=[p_art_helper])
        p_braille.add_argument('-t', '--threshold', type=int, help='threshold pixel intensity', default=(self.configuration.threshold), metavar='threshold')
        self.args = parser.parse_args()
        if self.args.command is None:
            parser.print_help()
            exit()
        if self.args.command == 'art':
            if self.args.art is None:
                p_art.print_help()
                exit()