# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jake/CRAPtion/craption/utils.py
# Compiled at: 2018-05-18 03:22:54
# Size of source mod 2**32: 1248 bytes
import craption.settings, datetime, os, pkg_resources, pyperclip, random, re, subprocess, sys, tempfile, time

def set_clipboard(data):
    pyperclip.copy(data)


def screenshot():
    path = tempfile.mktemp('.png')
    if sys.platform.startswith('linux'):
        run(['scrot', '-s', path])
    else:
        run(['screencapture', '-ix', path])
    return path


def get_filename():
    conf = craption.settings.get_conf()
    filename = conf['file']['name']
    now = time.time()
    for match in re.finditer('{r(\\d+)}', filename):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        random_string = ''.join([random.choice(chars) for _ in range(int(match.group(1)))])
        filename = filename.replace(match.group(0), random_string)

    filename = filename.replace('{u}', str(int(now)))
    filename = filename.replace('{d}', datetime.datetime.fromtimestamp(now).strftime(conf['file']['datetime_format']))
    return filename + '.png'


def install():
    craption.settings.write_template()
    exit(0)


def run(args):
    devnull = open(os.devnull, 'wb')
    p = subprocess.Popen(args, stdout=devnull, stderr=devnull)
    p.wait()