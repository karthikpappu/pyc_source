# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/transposer/script/console_script.py
# Compiled at: 2015-01-24 11:00:02
import argparse, transposer

def parse_args():
    parser = argparse.ArgumentParser(description='command line args to assist with development')
    parser.add_argument('-i', '--in', dest='file_in', default=None, required=True, help='file from which to read input data')
    parser.add_argument('-o', '--out', dest='file_out', default=None, help='file to which results should be written')
    parser.add_argument('-d', '--delimiter', dest='delimiter', default=',', help='the type of delmiter to read and write with' + "defaults to ','")
    return parser.parse_args()


def main():
    args = parse_args()
    transposer.transpose(i=args.file_in, o=args.file_out, d=args.delimiter)