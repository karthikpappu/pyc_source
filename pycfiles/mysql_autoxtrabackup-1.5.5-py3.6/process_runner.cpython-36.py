# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/process_runner/process_runner.py
# Compiled at: 2020-03-24 02:41:06
# Size of source mod 2**32: 5523 bytes
import datetime, logging, re, subprocess, shlex
from subprocess import PIPE, STDOUT
from general_conf.generalops import GeneralClass
from general_conf import path_config
logger = logging.getLogger(__name__)

class ProcessHandler(GeneralClass):
    __doc__ = '\n    Class to run a command with real-time logging for process\n\n    centralizes logic for subprocess calls, and is available to all other classes (Prepare, Backup, etc)\n    '

    def __init__(self, config=path_config.config_path_file):
        self.conf = config
        GeneralClass.__init__(self, self.conf)
        self._xtrabackup_history_log = [['command', 'xtrabackup_function', 'start time', 'end time', 'duration', 'exit code']]

    @property
    def xtrabackup_history_log(self):
        return self._xtrabackup_history_log

    def run_command(self, command):
        """
        executes a prepared command, enables real-time console & log output.

        This function should eventually be used for all subprocess calls.

        :param command: bash command to be executed
        :type command: str
        :return: True if success, False if failure
        :rtype: bool
        """
        filtered_command = re.sub("--password='?\\w+'?", "--password='*'", command)
        logger.info('SUBPROCESS STARTING: {}'.format(filtered_command))
        subprocess_args = self.command_to_args(command_str=command)
        cmd_start = datetime.datetime.now()
        with subprocess.Popen(subprocess_args, stdout=PIPE, stderr=STDOUT) as (process):
            for line in process.stdout:
                logger.debug('[{}:{}] {}'.format(subprocess_args[0], process.pid, line.decode('utf-8').strip('\n')))

        logger.info('SUBPROCESS {} COMPLETED with exit code: {}'.format(subprocess_args[0], process.returncode))
        cmd_end = datetime.datetime.now()
        self.summarize_process(subprocess_args, cmd_start, cmd_end, process.returncode)
        if process.returncode == 0:
            return True
        else:
            return False

    @staticmethod
    def command_to_args(command_str):
        """
        convert a string bash command to an arguments list, to use with subprocess

        Most autoxtrabackup code creates a string command, e.g. "xtrabackup --prepare --target-dir..."
        If we run a string command with subprocess.Popen, we require shell=True.
        shell=True has security considerations (below), and we run autoxtrabackup with privileges (!).
        https://docs.python.org/3/library/subprocess.html#security-considerations
        So, convert to an args list and call Popen without shell=True.

        :param command_str: string command to execute as a subprocess
        :type command_str: str
        :return: list of args to pass to subprocess.Popen.
        :rtype: list
        """
        if isinstance(command_str, list):
            args = command_str
        else:
            if isinstance(command_str, str):
                args = shlex.split(command_str)
            else:
                raise TypeError
        logger.debug('subprocess args are: {}'.format(args))
        return args

    @staticmethod
    def represent_duration(start_time, end_time):
        duration_delta = end_time - start_time
        seconds = int(duration_delta.seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
        if hours > 0:
            return '%dh%dm%ds' % (hours, minutes, seconds)
        else:
            if minutes > 0:
                return '%dm%ds' % (minutes, seconds)
            return '%ds' % (seconds,)

    def summarize_process(self, args, cmd_start, cmd_end, return_code):
        cmd_root = args[0].split('/')[-1:][0]
        xtrabackup_function = None
        if cmd_root == 'xtrabackup':
            if '--backup' in args:
                xtrabackup_function = 'backup'
            elif '--prepare' in args and '--apply-log-only' not in args:
                xtrabackup_function = 'prepare'
            elif '--prepare' in args:
                if '--apply-log-only' in args:
                    xtrabackup_function = 'prepare/apply-log-only'
        if not xtrabackup_function:
            for arg in args:
                if re.search('(--decrypt)=?[\\w]*', arg):
                    xtrabackup_function = 'decrypt'
                else:
                    if re.search('(--decompress)=?[\\w]*', arg):
                        xtrabackup_function = 'decompress'

        if cmd_root != 'pigz':
            self._xtrabackup_history_log.append([cmd_root,
             xtrabackup_function,
             cmd_start.strftime('%Y-%m-%d %H:%M:%S'),
             cmd_end.strftime('%Y-%m-%d %H:%M:%S'),
             self.represent_duration(cmd_start, cmd_end),
             return_code])
        return True


ProcessRunner = ProcessHandler()