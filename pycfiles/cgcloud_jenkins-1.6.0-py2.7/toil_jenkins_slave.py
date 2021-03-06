# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/jenkins/toil_jenkins_slave.py
# Compiled at: 2016-11-22 15:21:45
from StringIO import StringIO
import time, re
from fabric.operations import run, put
from bd2k.util.strings import interpolate as fmt
from cgcloud.core.apache import ApacheSoftwareBox
from cgcloud.core.mesos_box import MesosBox
from cgcloud.jenkins.cgcloud_jenkins_slave import CgcloudJenkinsSlave
from cgcloud.jenkins.jenkins_master import Jenkins
from cgcloud.core.box import fabric_task
from cgcloud.core.common_iam_policies import s3_full_policy, sdb_full_policy
from cgcloud.core.docker_box import DockerBox
from cgcloud.fabric.operations import sudo, remote_sudo_popen, remote_open
from cgcloud.lib.util import abreviated_snake_case_class_name, heredoc
hadoop_version = '2.6.2'
spark_hadoop_version = '2.6'
spark_version = '1.5.2'
install_dir = '/opt'

class ToilJenkinsSlave(CgcloudJenkinsSlave, DockerBox, MesosBox, ApacheSoftwareBox):
    """
    Jenkins slave for running the Toil build and tests on
    """

    @classmethod
    def recommended_instance_type(cls):
        return 'm3.large'

    def _list_packages_to_install(self):
        return super(ToilJenkinsSlave, self)._list_packages_to_install() + ['python-dev', 'gcc', 'make', 'libffi-dev', 'libcurl4-openssl-dev', 'slurm-llnl', 'bc'] + [ 'gridengine-' + p for p in ('common',
                                                                                                                                                                                                   'master',
                                                                                                                                                                                                   'client',
                                                                                                                                                                                                   'exec') ]

    def _get_debconf_selections(self):
        return super(ToilJenkinsSlave, self)._get_debconf_selections() + [
         'gridengine-master shared/gridenginemaster string localhost',
         'gridengine-master shared/gridenginecell string default',
         'gridengine-master shared/gridengineconfig boolean true']

    def _post_install_packages(self):
        super(ToilJenkinsSlave, self)._post_install_packages()
        self.setup_repo_host_keys()
        self.__disable_mesos_daemons()
        self.__install_parasol()
        self.__patch_distutils()
        self.__configure_gridengine()
        self.__configure_slurm()
        self.__install_yarn()
        self.__install_spark()

    @fabric_task
    def _setup_build_user(self):
        super(ToilJenkinsSlave, self)._setup_build_user()
        for prog in ('mount', 'umount'):
            sudo("echo 'jenkins ALL=(ALL) NOPASSWD: /bin/%s' >> /etc/sudoers" % prog)

    @fabric_task
    def __disable_mesos_daemons(self):
        for daemon in ('master', 'slave'):
            sudo('echo manual > /etc/init/mesos-%s.override' % daemon)

    @fabric_task
    def __install_parasol(self):
        run('git clone https://github.com/BD2KGenomics/parasol-binaries.git')
        sudo('cp parasol-binaries/* /usr/local/bin')
        run('rm -rf parasol-binaries')

    @fabric_task
    def __install_yarn(self):
        path = fmt('hadoop/common/hadoop-{hadoop_version}/hadoop-{hadoop_version}.tar.gz')
        self._install_apache_package(path, install_dir)
        with remote_open('/etc/environment', use_sudo=True) as (f):
            yarn_path = fmt('{install_dir}/hadoop')
            self._patch_etc_environment(f, env_pairs=dict(HADOOP_HOME=yarn_path))

    @fabric_task
    def __install_spark(self):
        path = fmt('spark/spark-{spark_version}/spark-{spark_version}-bin-hadoop{spark_hadoop_version}.tgz')
        self._install_apache_package(path, install_dir)
        with remote_open('/etc/environment', use_sudo=True) as (f):
            spark_home = fmt('{install_dir}/spark')
            python_path = [
             fmt('{spark_home}/python'),
             run(fmt('ls {spark_home}/python/lib/py4j-*-src.zip').strip())]
            self._patch_etc_environment(f, env_pairs=dict(SPARK_HOME=spark_home), dirs=python_path, dirs_var='PYTHONPATH')

    def _pass_role_arn(self):
        return 'arn:aws:iam::%s:role/*' % self.ctx.account

    def _get_iam_ec2_role(self):
        iam_role_name, policies = super(ToilJenkinsSlave, self)._get_iam_ec2_role()
        iam_role_name += '--' + abreviated_snake_case_class_name(ToilJenkinsSlave)
        policies.update(dict(s3_full=s3_full_policy, sdb_full=sdb_full_policy))
        return (iam_role_name, policies)

    @fabric_task
    def __patch_distutils(self):
        """
        https://hg.python.org/cpython/rev/cf70f030a744/
        https://bitbucket.org/pypa/setuptools/issues/248/exit-code-is-zero-when-upload-fails
        Fixed in 2.7.8: https://hg.python.org/cpython/raw-file/v2.7.8/Misc/NEWS
        """
        if self._remote_python_version() < (2, 7, 8):
            with remote_sudo_popen('patch -d /usr/lib/python2.7 -p2') as (patch):
                patch.write(heredoc("\n                    --- a/Lib/distutils/command/upload.py\n                    +++ b/Lib/distutils/command/upload.py\n                    @@ -10,7 +10,7 @@ import urlparse\n                     import cStringIO as StringIO\n                     from hashlib import md5\n\n                    -from distutils.errors import DistutilsOptionError\n                    +from distutils.errors import DistutilsError, DistutilsOptionError\n                     from distutils.core import PyPIRCCommand\n                     from distutils.spawn import spawn\n                     from distutils import log\n                    @@ -181,7 +181,7 @@ class upload(PyPIRCCommand):\n                                     self.announce(msg, log.INFO)\n                             except socket.error, e:\n                                 self.announce(str(e), log.ERROR)\n                    -            return\n                    +            raise\n                             except HTTPError, e:\n                                 status = e.code\n                                 reason = e.msg\n                    @@ -190,5 +190,6 @@ class upload(PyPIRCCommand):\n                                 self.announce('Server response (%s): %s' % (status, reason),\n                                               log.INFO)\n                             else:\n                    -            self.announce('Upload failed (%s): %s' % (status, reason),\n                    -                          log.ERROR)\n                    +            msg = 'Upload failed (%s): %s' % (status, reason)\n                    +            self.announce(msg, log.ERROR)\n                    +            raise DistutilsError(msg)"))

    @fabric_task
    def __configure_gridengine(self):
        """
        Configure the GridEngine daemons (master and exec) and creata a default queue. Ensure
        that the queue is updated to reflect the number of cores actually available.
        """
        ws = re.compile('\\s+')
        nl = re.compile('[\\r\\n]+')

        def qconf(opt, **kwargs):
            return qconf_dict(opt, kwargs)

        def qconf_dict(opt, d=None, file_name='qconf.tmp'):
            if d:
                s = ('\n').join((' ').join(i) for i in d.iteritems()) + '\n'
                put(remote_path=file_name, local_path=StringIO(s))
                sudo((' ').join(['qconf', opt, file_name]))
                run((' ').join(['rm', file_name]))
            else:
                return dict(tuple(ws.split(l, 1)) for l in nl.split(run('SGE_SINGLE_LINE=1 qconf ' + opt)) if l and not l.startswith('#'))

        qconf('-Auser', name=Jenkins.user, oticket='0', fshare='0', delete_time='0', default_project='NONE')
        sudo('qconf -au %s arusers' % Jenkins.user)
        sudo('qconf -as localhost')
        run('for i in `qconf -sel`; do sudo qconf -de $i ; done')
        qconf('-Ae', hostname='localhost', load_scaling='NONE', complex_values='NONE', user_lists='arusers', xuser_lists='NONE', projects='NONE', xprojects='NONE', usage_scaling='NONE', report_variables='NONE')
        qconf('-Ap', pe_name='smp', slots='999', user_lists='NONE', xuser_lists='NONE', start_proc_args='/bin/true', stop_proc_args='/bin/true', allocation_rule='$pe_slots', control_slaves='FALSE', job_is_first_task='TRUE', urgency_slots='min', accounting_summary='FALSE')
        qconf('-Aq', qname='all.q', processors='1', slots='1', hostlist='localhost', seq_no='0', load_thresholds='np_load_avg=1.75', suspend_thresholds='NONE', nsuspend='1', suspend_interval='00:05:00', priority='0', min_cpu_interval='00:05:00', qtype='BATCH INTERACTIVE', ckpt_list='NONE', pe_list='make smp', rerun='FALSE', tmpdir='/tmp', shell='/bin/bash', prolog='NONE', epilog='NONE', shell_start_mode='posix_compliant', starter_method='NONE', suspend_method='NONE', resume_method='NONE', terminate_method='NONE', notify='00:00:60', owner_list='NONE', user_lists='arusers', xuser_lists='NONE', subordinate_list='NONE', complex_values='NONE', projects='NONE', xprojects='NONE', calendar='NONE', initial_state='default', s_rt='INFINITY', h_rt='INFINITY', s_cpu='INFINITY', h_cpu='INFINITY', s_fsize='INFINITY', h_fsize='INFINITY', s_data='INFINITY', h_data='INFINITY', s_stack='INFINITY', h_stack='INFINITY', s_core='INFINITY', h_core='INFINITY', s_rss='INFINITY', h_rss='INFINITY', s_vmem='INFINITY', h_vmem='INFINITY')
        sconf = qconf('-ssconf')
        sconf.update(dict(flush_submit_sec='1', flush_finish_sec='1', schedule_interval='0:0:1'))
        qconf_dict('-Msconf', sconf)
        conf = qconf('-sconf')
        params = dict(tuple(e.split('=')) for e in conf['reporting_params'].split(' '))
        params['accounting_flush_time'] = '00:00:00'
        conf['reporting_params'] = (' ').join(('=').join(e) for e in params.iteritems())
        qconf_dict('-Mconf', conf, file_name='global')
        path = '/var/lib/gridengine/default/common/'
        self._register_init_script('gridengine-pre', heredoc('\n            description "GridEngine pre-start configuration"\n            console log\n            start on filesystem\n            pre-start script\n                echo localhost > {path}/act_qmaster ; chown sgeadmin:sgeadmin {path}/act_qmaster\n                echo localhost `hostname -f` > {path}/host_aliases\n            end script'))
        self._register_init_script('gridengine-post', heredoc('\n            description "GridEngine post-start configuration"\n            console log\n            # I would rather depend on the gridengine daemons but don\'t know how as they are\n            # started by SysV init scripts. Supposedly the \'rc\' job is run last.\n            start on started rc\n            pre-start script\n                cores=$(grep -c \'^processor\' /proc/cpuinfo)\n                qconf -mattr queue processors $cores `qselect`\n                qconf -mattr queue slots $cores `qselect`\n            end script'))
        for daemon in ('exec', 'master'):
            sudo('/etc/init.d/gridengine-%s stop' % daemon)

        sudo("killall -9 -r 'sge_.*'", warn_only=True)
        self._run_init_script('gridengine-pre')
        for daemon in ('master', 'exec'):
            sudo('/etc/init.d/gridengine-%s start' % daemon)

        self._run_init_script('gridengine-post')
        while 'execd is in unknown state' in run('qstat -f -q all.q -explain a', warn_only=True):
            time.sleep(1)

        return

    @fabric_task
    def __configure_slurm(self):
        """
        Configures SLURM in a single-node configuration with text-file accounting
        :return:
        """
        sudo('/usr/sbin/create-munge-key')
        sudo('/usr/sbin/service munge start')
        slurm_acct_file = '/var/log/slurm-llnl/slurm-acct.txt'
        slurm_conf = heredoc('\n            ClusterName=jenkins-testing\n            ControlMachine=localhost\n            SlurmUser=slurm\n            SlurmctldPort=6817\n            SlurmdPort=6818\n            StateSaveLocation=/tmp\n            SlurmdSpoolDir=/tmp/slurmd\n            SwitchType=switch/none\n            MpiDefault=none\n            SlurmctldPidFile=/var/run/slurmctld.pid\n            SlurmdPidFile=/var/run/slurmd.pid\n            ProctrackType=proctrack/pgid\n            CacheGroups=0\n            ReturnToService=0\n            SlurmctldTimeout=300\n            SlurmdTimeout=300\n            InactiveLimit=0\n            MinJobAge=300\n            KillWait=30\n            Waittime=0\n            SchedulerType=sched/backfill\n            SelectType=select/cons_res\n            FastSchedule=1\n\n            # LOGGING\n            SlurmctldDebug=3\n            SlurmdDebug=3\n            JobCompType=jobcomp/none\n\n            # ACCOUNTING\n            AccountingStorageLoc={slurm_acct_file}\n            AccountingStorageType=accounting_storage/filetxt\n            AccountingStoreJobComment=YES\n            JobAcctGatherFrequency=30\n            JobAcctGatherType=jobacct_gather/linux\n\n            # COMPUTE NODES\n            NodeName=localhost CPUs=1 State=UNKNOWN RealMemory=256\n            PartitionName=debug Nodes=localhost Default=YES MaxTime=INFINITE State=UP\n        ')
        slurm_conf_tmp = '/tmp/slurm.conf'
        slurm_conf_file = '/etc/slurm-llnl/slurm.conf'
        put(remote_path=slurm_conf_tmp, local_path=StringIO(slurm_conf))
        sudo('mkdir -p /etc/slurm-llnl')
        sudo('mv %s %s' % (slurm_conf_tmp, slurm_conf_file))
        sudo('chown root:root %s' % slurm_conf_file)
        sudo('mkdir -p /var/log/slurm-llnl')
        sudo('touch %s' % slurm_acct_file)
        sudo('chown slurm:slurm %s' % slurm_acct_file)
        sudo('chmod 644 %s' % slurm_acct_file)
        self._register_init_script('slurm-llnl-pre', heredoc('\n            description "Slurm pre-start configuration"\n            console log\n            start on filesystem\n            pre-start script\n                CPUS=$(/usr/bin/nproc)\n                MEMORY=$(cat /proc/meminfo | grep MemTotal | awk \'{{print $2, "/ 1024"}}\' | bc)\n                sed -i "s/CPUs=[0-9]\\+/CPUs=${{CPUS}}/" {slurm_conf_file}\n                sed -i "s/RealMemory=[0-9]\\+/RealMemory=${{MEMORY}}/" {slurm_conf_file}\n            end script'))
        self._run_init_script('slurm-llnl-pre')
        self._run_init_script('slurm-llnl')
        sudo('scontrol update NodeName=localhost State=Down')
        sudo('scontrol update NodeName=localhost State=Resume')

    def _docker_users(self):
        return super(ToilJenkinsSlave, self)._docker_users() + [self.default_account()]