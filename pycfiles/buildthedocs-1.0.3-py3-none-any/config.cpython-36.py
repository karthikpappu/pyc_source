# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/siddis14/github/buildtest-framework/buildtest/tools/config.py
# Compiled at: 2018-10-26 17:00:06
# Size of source mod 2**32: 8534 bytes
__doc__ = '\nChecks buildtest configuration and reports any errors. Also display buildtest\nconfiguration using buildtest --show\n\n:author: Shahzeb Siddiqui (Pfizer)\n'
import os, sys, time, logging, subprocess, yaml
BUILDTEST_VERSION = '0.6.3'
BUILDTEST_ROOT = os.getenv('BUILDTEST_ROOT')
BUILDTEST_JOB_EXTENSION = [
 '.lsf', '.slurm', '.pbs']
BUILDTEST_SHELLTYPES = ['sh', 'bash', 'csh']
PYTHON_APPS = [
 'python', 'anaconda2', 'anaconda3']
MPI_APPS = ['openmpi', 'mpich', 'mvapich2', 'intel', 'impi']
BUILDTEST_CONFIG_FILE = os.path.join(os.getenv('HOME'), '.local', 'buildtest', 'config.yaml')
try:
    fd = open(BUILDTEST_CONFIG_FILE, 'r')
    config_opts = yaml.load(fd)
    config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'] = ''
    config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'] = ''
except FileNotFoundError as err_msg:
    print((f"{err_msg}"))
    raise

logID = 'buildtest'

def check_configuration():
    """
    Reports buildtest configuration and checks each BUILDTEST environment variable and check
    for module environment
    """
    ec = 0
    time.sleep(0.1)
    if not os.path.exists(BUILDTEST_ROOT):
        ec = 1
        print('ERROR:  \t BUILDTEST_ROOT: %{BUILDTEST_ROOT} does not exist')
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_CONFIGS_REPO']):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_CONFIGS_REPO: {config_opts['BUILDTEST_CONFIGS_REPO']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_R_REPO']):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_R_REPO: {config_opts['BUILDTEST_R_REPO']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_R_TESTDIR']):
        ec = 1
        print(f"ERROR: \t BUILDTEST_R_TESTDIR: {config_opts['BUILDTEST_R_TESTDIR']}  does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_PERL_REPO']):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_PERL_REPO: {config_opts['BUILDTEST_PERL_REPO']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_PERL_TESTDIR']):
        ec = 1
        print(f"ERROR: \t BUILDTEST_PERL_TESTDIR: {config_opts['BUILDTEST_PERL_TESTDIR']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_PYTHON_REPO']):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_PYTHON_REPO: {config_opts['BUILDTEST_PYTHON_REPO']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_PYTHON_TESTDIR']):
        ec = 1
        print(f"ERROR: \t BUILDTEST_PYTHON_TESTDIR: {config_opts['BUILDTEST_PYTHON_TESTDIR']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_RUBY_REPO']):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_RUBY_REPO: {config_opts['BUILDTEST_RUBY_REPO']} does not exist")
    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_RUBY_TESTDIR']):
        ec = 1
        print(f"ERROR: \t BUILDTEST_RUBY_TESTDIR: %{config_opts['BUILDTEST_RUBY_TESTDIR']} does not exist")
    time.sleep(0.1)
    for tree in config_opts['BUILDTEST_MODULE_ROOT']:
        if not os.path.exists(tree):
            ec = 1
            print(f"ERROR:  \t BUILDTEST_MODULE_ROOT: {tree} does  not exists ")

    time.sleep(0.1)
    if config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] not in ('FNS', 'HMNS'):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_MODULE_NAMING_SCHEME: {config_opts['BUILDTEST_MODULE_NAMING_SCHEME']} valid values are {('HMNS', 'FNS')}")
    time.sleep(0.1)
    if config_opts['BUILDTEST_EASYBUILD'] not in (True, False):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_EASYBUILD: {config_opts['BUILDTEST_EASYBUILD']} valid values are {(True, False)} ")
    time.sleep(0.1)
    if config_opts['BUILDTEST_CLEAN_BUILD'] not in (True, False):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_CLEAN_BUILD: {config_opts['BUILDTEST_CLEAN_BUILD']} valid values are {(True, False)} ")
    time.sleep(0.1)
    if config_opts['BUILDTEST_SHELL'] not in BUILDTEST_SHELLTYPES:
        ec = 1
        print(f"ERROR: \t BUILDTEST_SHELL: {config_opts['BUILDTEST_SHELL']} not a valid value, must be one of the following: {BUILDTEST_SHELLTYPES}")
    time.sleep(0.1)
    time.sleep(0.1)
    if config_opts['BUILDTEST_ENABLE_JOB'] not in (True, False):
        ec = 1
        print(f"ERROR:  \t BUILDTEST_ENABLE_JOB: {config_opts['BUILDTEST_ENABLE_JOB']} valid values are {(True, False)} ")
    if not os.path.exists(config_opts['BUILDTEST_JOB_TEMPLATE']):
        ec = 1
        print(f"ERROR:\t BUILDTEST_JOB_TEMPLATE: {config_opts['BUILDTEST_JOB_TEMPLATE']} does not exist")
    time.sleep(0.1)
    job_template_extension = os.path.splitext(config_opts['BUILDTEST_JOB_TEMPLATE'])[1]
    if job_template_extension not in BUILDTEST_JOB_EXTENSION:
        ec = 1
        print(f"Invalid file extension: {job_template_extension} must be one of the following extension {BUILDTEST_JOB_EXTENSION}")
    if 'BUILDTEST_PREPEND_MODULES' not in list(config_opts.keys()):
        config_opts['BUILDTEST_PREPEND_MODULES'] = []
    time.sleep(0.1)
    if ec != 0:
        print('Please fix your BUILDTEST configuration')
        sys.exit(1)
    cmd = 'module --version'
    ret = subprocess.Popen(cmd, shell=True, stdin=(subprocess.PIPE), stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
    outputmsg, errormsg = ret.communicate()
    ec = ret.returncode
    if ec != 0:
        print('module commmand not found in system')
        print(outputmsg)
        print(errormsg)
        sys.exit(1)


def show_configuration():
    """ show buildtest configuration """
    print
    print('\t buildtest configuration summary')
    print('\t (C): Configuration File,  (E): Environment Variable')
    print
    print(('BUILDTEST_ROOT' + '\t (E) =').expandtabs(50), os.getenv('BUILDTEST_ROOT'))
    for key in sorted(config_opts):
        if os.getenv(key):
            type = '(E)'
        else:
            type = '(C)'
        if key == 'BUILDTEST_MODULE_ROOT':
            tree = ''
            for mod_tree in config_opts[key]:
                tree += mod_tree + ':'

            tree = tree[:-1]
            print((key + '\t ' + type + ' =').expandtabs(50), tree)
        else:
            print((key + '\t ' + type + ' =').expandtabs(50), config_opts[key])

    sys.exit(0)