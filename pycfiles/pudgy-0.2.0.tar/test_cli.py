# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_cli.py
# Compiled at: 2006-03-14 17:35:23
__doc__ = 'Pudge Command Line Interface Tests'
import getopt, pudge.cli as cli
from pudge.generator import Generator

def test_bad_arguments():
    command = cli.PudgeCommand('pudge', ['-XX'])
    try:
        command.parse_arguments()
    except getopt.GetoptError, e:
        pass
    else:
        assert 0, 'PudgeCommand.parse_arguments() should have raised an exception.'


def test_usage():
    command = cli.PudgeCommand('pudge', ['-h'])
    call = command.parse_arguments()
    assert not isinstance(call, Generator)


def test_short_args():
    args = [
     '-f', '-x', '-d', '/test/dest', '-t', '/test/templates', '-m', 'pudge']
    command = cli.PudgeCommand('pudge', args)
    call = command.parse_arguments()
    assert isinstance(call, Generator)
    assert call.force
    assert call.xhtml
    assert call.dest == '/test/dest'
    assert call.template_dir == '/test/templates'
    assert call.modules == ['pudge']


def test_long_args():
    args = [
     '--force', '--xhtml', '--dest=/test/dest', '--templates=/test/templates', '--modules=pudge']
    command = cli.PudgeCommand('pudge', args)
    call = command.parse_arguments()
    assert isinstance(call, Generator)
    assert call.force
    assert call.xhtml
    assert call.dest == '/test/dest'
    assert call.template_dir == '/test/templates'
    assert call.modules == ['pudge']