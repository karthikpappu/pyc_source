# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tagbase\gutentag\blast.py
# Compiled at: 2009-07-13 23:06:10
from django.conf import settings
import os, sys, threading, subprocess, log

def makeNewDB(inputFile, seqtype, out):
    """
    Makes new blast database
    Returns retcode 
    """
    if seqtype == 'protein':
        st = 'T'
    else:
        st = 'F'
    command = '%s -i "%s" -p %s -n "%s" ' % (settings.FORMATDB, inputFile, st, out)
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        (stdout_value, stderr_error) = proc.communicate()
        retcode = proc.returncode
        log.debug('stderr_error: %s' % stderr_error)
        if retcode < 0:
            log.debug('Child was terminated by signal: %s' % retcode)
        else:
            log.debug('Child returned: %s' % retcode)
            return retcode
    except Exception, e:
        log.debug('Exception in blast: %s' % str(e))


def runShellCmd(command, seq):
    try:
        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout_value, stderr_value) = proc.communicate(seq)
        retcode = proc.returncode
        log.debug('stderr: %s' % stderr_value)
        if retcode < 0:
            log.debug('Child was terminated by signal: %s' % retcode)
        else:
            log.debug('Child returned: %s' % retcode)
            print 'Child returned %s', retcode
            return (retcode, stdout_value)
    except Exception, e:
        log.debug('Exception in blast: %s' % str(e))


def runBlastAll(db, program, seq):
    command = '%s -d "%s" -p %s ' % (settings.BLASTALL, db, program)
    log.debug('command: %s' % command)
    (retcode, stdout_value) = runShellCmd(command, seq)
    return stdout_value


def runBlastcl3(program, seq):
    command = '%s -p %s -d swissprot -v 50 -b 10     -u human[organism] -m 7' % (settings.BLASTCL3, program)
    log.debug('command: %s' % command)
    (retcode, stdout_value) = runShellCmd(command, seq)
    return (retcode, stdout_value)


def runBlastcl3CDD(seq):
    command = '%s -p blastp -d cdd ' % settings.BLASTCL3
    log.debug('command: %s' % command)
    (retcode, stdout_value) = runShellCmd(command, seq)
    return (retcode, stdout_value)