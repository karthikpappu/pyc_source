# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/ssh_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7693 bytes
from base64 import b64encode
from select import select
from airflow import configuration
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SSHOperator(BaseOperator):
    """SSHOperator"""
    template_fields = ('command', 'remote_host')
    template_ext = ('.sh', )

    @apply_defaults
    def __init__(self, ssh_hook=None, ssh_conn_id=None, remote_host=None, command=None, timeout=10, do_xcom_push=False, environment=None, *args, **kwargs):
        (super(SSHOperator, self).__init__)(*args, **kwargs)
        self.ssh_hook = ssh_hook
        self.ssh_conn_id = ssh_conn_id
        self.remote_host = remote_host
        self.command = command
        self.timeout = timeout
        self.environment = environment
        self.do_xcom_push = do_xcom_push

    def execute(self, context):
        try:
            if self.ssh_conn_id:
                if self.ssh_hook:
                    if isinstance(self.ssh_hook, SSHHook):
                        self.log.info('ssh_conn_id is ignored when ssh_hook is provided.')
                else:
                    self.log.info('ssh_hook is not provided or invalid. Trying ssh_conn_id to create SSHHook.')
                    self.ssh_hook = SSHHook(ssh_conn_id=(self.ssh_conn_id), timeout=(self.timeout))
            else:
                if not self.ssh_hook:
                    raise AirflowException('Cannot operate without ssh_hook or ssh_conn_id.')
                if self.remote_host is not None:
                    self.log.info('remote_host is provided explicitly. It will replace the remote_host which was defined in ssh_hook or predefined in connection of ssh_conn_id.')
                    self.ssh_hook.remote_host = self.remote_host
                raise self.command or AirflowException('SSH command not specified. Aborting.')
            with self.ssh_hook.get_conn() as (ssh_client):
                get_pty = False
                if self.command.startswith('sudo'):
                    get_pty = True
                stdin, stdout, stderr = ssh_client.exec_command(command=(self.command), get_pty=get_pty,
                  timeout=(self.timeout),
                  environment=(self.environment))
                channel = stdout.channel
                stdin.close()
                channel.shutdown_write()
                agg_stdout = ''
                agg_stderr = ''
                stdout_buffer_length = len(stdout.channel.in_buffer)
                if stdout_buffer_length > 0:
                    agg_stdout += stdout.channel.recv(stdout_buffer_length)
                while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
                    readq, _, _ = select([channel], [], [], self.timeout)
                    for c in readq:
                        if c.recv_ready():
                            line = stdout.channel.recv(len(c.in_buffer))
                            line = line
                            agg_stdout += line
                            self.log.info(line.decode('utf-8').strip('\n'))
                        if c.recv_stderr_ready():
                            line = stderr.channel.recv_stderr(len(c.in_stderr_buffer))
                            line = line
                            agg_stderr += line
                            self.log.warning(line.decode('utf-8').strip('\n'))

                    if stdout.channel.exit_status_ready() and not stderr.channel.recv_stderr_ready() and not stdout.channel.recv_ready():
                        stdout.channel.shutdown_read()
                        stdout.channel.close()
                        break

                stdout.close()
                stderr.close()
                exit_status = stdout.channel.recv_exit_status()
                if exit_status == 0:
                    if self.do_xcom_push:
                        enable_pickling = configuration.conf.getboolean('core', 'enable_xcom_pickling')
                        if enable_pickling:
                            return agg_stdout
                        else:
                            return b64encode(agg_stdout).decode('utf-8')
                else:
                    error_msg = agg_stderr.decode('utf-8')
                    raise AirflowException('error running cmd: {0}, error: {1}'.format(self.command, error_msg))
        except Exception as e:
            raise AirflowException('SSH operator error: {0}'.format(str(e)))

        return True

    def tunnel(self):
        ssh_client = self.ssh_hook.get_conn()
        ssh_client.get_transport()