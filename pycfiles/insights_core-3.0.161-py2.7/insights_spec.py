# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/insights_spec.py
# Compiled at: 2020-03-25 13:10:41
from __future__ import absolute_import
import os, errno, shlex, logging, six
from subprocess import Popen, PIPE, STDOUT
from tempfile import NamedTemporaryFile
from insights.util import mangle
from .constants import InsightsConstants as constants
from .utilities import determine_hostname, systemd_notify
logger = logging.getLogger(__name__)

class InsightsSpec(object):
    """
    A spec loaded from the uploader.json
    """

    def __init__(self, config, spec, exclude, parent_pid=None):
        self.config = config
        self.regex = False
        self.exclude = None
        if exclude and isinstance(exclude, dict):
            if 'regex' in exclude and exclude['regex']:
                logger.debug('Using regular expression matching in remove.conf.')
                self.regex = True
                self.exclude = exclude['regex']
        else:
            self.exclude = exclude
        self.pattern = spec['pattern'] if spec['pattern'] else None
        self.parent_pid = parent_pid
        return


class InsightsCommand(InsightsSpec):
    """
    A command spec
    """

    def __init__(self, config, spec, exclude, mountpoint, parent_pid=None):
        InsightsSpec.__init__(self, config, spec, exclude, parent_pid)
        self.command = spec['command'].replace('{CONTAINER_MOUNT_POINT}', mountpoint)
        self.archive_path = mangle.mangle_command(self.command)
        self.is_hostname = spec.get('symbolic_name') == 'hostname'
        if not six.PY3:
            self.command = self.command.encode('utf-8', 'ignore')

    def get_output(self):
        """
        Execute a command through system shell. First checks to see if
        the requested command is executable. Returns (returncode, stdout, 0)
        """
        systemd_notify(self.parent_pid)
        if self.is_hostname:
            return determine_hostname()
        timeout_command = 'timeout -s KILL %s %s' % (
         self.config.cmd_timeout, self.command)
        cmd_env = {'LC_ALL': 'C', 'PATH': '/sbin:/bin:/usr/sbin:/usr/bin', 
           'PYTHONPATH': os.getenv('PYTHONPATH')}
        args = shlex.split(timeout_command)
        if set.intersection(set(args), constants.command_blacklist):
            raise RuntimeError('Command Blacklist: ' + self.command)
        try:
            logger.debug('Executing: %s', args)
            proc0 = Popen(args, shell=False, stdout=PIPE, stderr=STDOUT, bufsize=-1, env=cmd_env, close_fds=True)
        except OSError as err:
            if err.errno == errno.ENOENT:
                logger.debug('Command %s not found', self.command)
                return
            raise err

        dirty = False
        cmd = 'sed -rf ' + constants.default_sed_file
        sedcmd = Popen(shlex.split(cmd), stdin=proc0.stdout, stdout=PIPE)
        proc0.stdout.close()
        proc0 = sedcmd
        if self.exclude is not None:
            exclude_file = NamedTemporaryFile()
            exclude_file.write(('\n').join(self.exclude).encode('utf-8'))
            exclude_file.flush()
            if self.regex:
                cmd = 'grep -E -v -f %s' % exclude_file.name
            else:
                cmd = 'grep -F -v -f %s' % exclude_file.name
            proc1 = Popen(shlex.split(cmd), stdin=proc0.stdout, stdout=PIPE)
            proc0.stdout.close()
            stderr = None
            if self.pattern is None or len(self.pattern) == 0:
                stdout, stderr = proc1.communicate()
            logger.debug('Proc1 Status: %s', proc1.returncode)
            logger.debug('Proc1 stderr: %s', stderr)
            proc0 = proc1
            dirty = True
        if self.pattern is not None and len(self.pattern):
            pattern_file = NamedTemporaryFile()
            pattern_file.write(('\n').join(self.pattern).encode('utf-8'))
            pattern_file.flush()
            cmd = 'grep -F -f %s' % pattern_file.name
            proc2 = Popen(shlex.split(cmd), stdin=proc0.stdout, stdout=PIPE)
            proc0.stdout.close()
            stdout, stderr = proc2.communicate()
            logger.debug('Proc2 Status: %s', proc2.returncode)
            logger.debug('Proc2 stderr: %s', stderr)
            proc0 = proc2
            dirty = True
        if not dirty:
            stdout, stderr = proc0.communicate()
        if proc0.returncode == 126 or proc0.returncode == 127:
            stdout = (
             'Could not find cmd: %s', self.command)
        logger.debug('Proc0 Status: %s', proc0.returncode)
        logger.debug('Proc0 stderr: %s', stderr)
        return stdout.decode('utf-8', 'ignore').strip()


class InsightsFile(InsightsSpec):
    """
    A file spec
    """

    def __init__(self, spec, exclude, mountpoint, parent_pid=None):
        InsightsSpec.__init__(self, None, spec, exclude, parent_pid)
        self.real_path = os.path.join(mountpoint, spec['file'].lstrip('/'))
        self.archive_path = spec['file']
        return

    def get_output(self):
        """
        Get file content, selecting only lines we are interested in
        """
        systemd_notify(self.parent_pid)
        if not os.path.isfile(self.real_path):
            logger.debug('File %s does not exist', self.real_path)
            return
        else:
            cmd = []
            cmd.append('sed')
            cmd.append('-rf')
            cmd.append(constants.default_sed_file)
            cmd.append(self.real_path)
            sedcmd = Popen(cmd, stdout=PIPE)
            if self.exclude is not None:
                exclude_file = NamedTemporaryFile()
                exclude_file.write(('\n').join(self.exclude).encode('utf-8'))
                exclude_file.flush()
                if self.regex:
                    cmd = 'grep -E -v -f %s' % exclude_file.name
                else:
                    cmd = 'grep -F -v -f %s' % exclude_file.name
                args = shlex.split(cmd)
                proc = Popen(args, stdin=sedcmd.stdout, stdout=PIPE)
                sedcmd.stdout.close()
                stdin = proc.stdout
                if self.pattern is None:
                    output = proc.communicate()[0]
                else:
                    sedcmd = proc
            if self.pattern is not None:
                pattern_file = NamedTemporaryFile()
                pattern_file.write(('\n').join(self.pattern).encode('utf-8'))
                pattern_file.flush()
                cmd = 'grep -F -f %s' % pattern_file.name
                args = shlex.split(cmd)
                proc1 = Popen(args, stdin=sedcmd.stdout, stdout=PIPE)
                sedcmd.stdout.close()
                if self.exclude is not None:
                    stdin.close()
                output = proc1.communicate()[0]
            if self.pattern is None and self.exclude is None:
                output = sedcmd.communicate()[0]
            return output.decode('utf-8', 'ignore').strip()