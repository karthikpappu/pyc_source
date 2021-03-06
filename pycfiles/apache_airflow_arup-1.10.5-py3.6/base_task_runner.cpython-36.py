# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/task/task_runner/base_task_runner.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6711 bytes
from __future__ import unicode_literals
import getpass, os, subprocess, threading
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow import configuration as conf
from airflow.utils.configuration import tmp_configuration_copy
PYTHONPATH_VAR = 'PYTHONPATH'

class BaseTaskRunner(LoggingMixin):
    __doc__ = '\n    Runs Airflow task instances by invoking the `airflow run` command with raw\n    mode enabled in a subprocess.\n    '

    def __init__(self, local_task_job):
        super(BaseTaskRunner, self).__init__(local_task_job.task_instance)
        self._task_instance = local_task_job.task_instance
        popen_prepend = []
        if self._task_instance.run_as_user:
            self.run_as_user = self._task_instance.run_as_user
        else:
            try:
                self.run_as_user = conf.get('core', 'default_impersonation')
            except conf.AirflowConfigException:
                self.run_as_user = None

        self.log.debug('Planning to run as the %s user', self.run_as_user)
        if self.run_as_user and self.run_as_user != getpass.getuser():
            cfg_path = tmp_configuration_copy(chmod=384, include_env=True,
              include_cmds=True)
            subprocess.call([
             'sudo', 'chown', self.run_as_user, cfg_path],
              close_fds=True)
            pythonpath_value = os.environ.get(PYTHONPATH_VAR, '')
            popen_prepend = ['sudo', '-E', '-H', '-u', self.run_as_user]
            if pythonpath_value:
                popen_prepend.append('{}={}'.format(PYTHONPATH_VAR, pythonpath_value))
        else:
            cfg_path = tmp_configuration_copy(chmod=384, include_env=False,
              include_cmds=False)
        self._cfg_path = cfg_path
        self._command = popen_prepend + self._task_instance.command_as_list(raw=True,
          pickle_id=(local_task_job.pickle_id),
          mark_success=(local_task_job.mark_success),
          job_id=(local_task_job.id),
          pool=(local_task_job.pool),
          cfg_path=cfg_path)
        self.process = None

    def _read_task_logs(self, stream):
        while True:
            line = stream.readline()
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            if len(line) == 0:
                break
            self.log.info('Job %s: Subtask %s %s', self._task_instance.job_id, self._task_instance.task_id, line.rstrip('\n'))

    def run_command(self, run_with=None, join_args=False):
        """
        Run the task command.

        :param run_with: list of tokens to run the task command with e.g. ``['bash', '-c']``
        :type run_with: list
        :param join_args: whether to concatenate the list of command tokens e.g. ``['airflow', 'run']`` vs
            ``['airflow run']``
        :param join_args: bool
        :return: the process that was run
        :rtype: subprocess.Popen
        """
        run_with = run_with or []
        cmd = [' '.join(self._command)] if join_args else self._command
        full_cmd = run_with + cmd
        self.log.info('Running: %s', full_cmd)
        proc = subprocess.Popen(full_cmd,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT),
          universal_newlines=True,
          close_fds=True,
          env=(os.environ.copy()),
          preexec_fn=(os.setsid))
        log_reader = threading.Thread(target=(self._read_task_logs),
          args=(
         proc.stdout,))
        log_reader.daemon = True
        log_reader.start()
        return proc

    def start(self):
        """
        Start running the task instance in a subprocess.
        """
        raise NotImplementedError()

    def return_code(self):
        """
        :return: The return code associated with running the task instance or
            None if the task is not yet done.
        :rtype: int
        """
        raise NotImplementedError()

    def terminate(self):
        """
        Kill the running task instance.
        """
        raise NotImplementedError()

    def on_finish(self):
        """
        A callback that should be called when this is done running.
        """
        if self._cfg_path:
            if os.path.isfile(self._cfg_path):
                if self.run_as_user:
                    subprocess.call(['sudo', 'rm', self._cfg_path], close_fds=True)
                else:
                    os.remove(self._cfg_path)