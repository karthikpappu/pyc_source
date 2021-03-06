# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/env.py
# Compiled at: 2017-03-20 03:08:12
import os
from fabric.api import *
from fabric.main import list_commands
from fabric.utils import _AttributeDict
ez_env = _AttributeDict({'debug': None, 
   'group': None, 
   'roles': None, 
   'cloud': None, 
   'cc': {'cloud_class': None, 
          'processor': None, 
          'connection': None, 
          'sleep_time': None, 
          'config': None, 
          'actions': {}}, 
   'cloud_processor': None, 
   'cloud_class': None, 
   'cloud_handler': None, 
   'cloud_hold_recyle': 3, 
   'debug': None})

def _pssh(file):
    """
    Parse pssh-like file
    :param file:
    """
    file = os.path.realpath(os.path.expanduser(file))
    with open(file, 'r') as (fp):
        buffer = fp.read()
    host_list = buffer.strip('\n').split('\n')
    machines = []
    for addr in host_list[:]:
        addr.strip()
        if addr.find('#') == -1:
            machines.append(addr)

    return machines


def bind_hosts(curr, routes=None):
    """
    bind hosts from file
    :param curr:
    :param routes:
    :return:
    """
    if not routes:
        current_path = './config/fabric'
        files = os.listdir(current_path)
        routes = {}
        for f in files:
            if f.endswith('conf'):
                k = f.rsplit('.')[0]
                v = os.path.join(current_path, f)
                if k == 'online':
                    k = 'ol'
                routes[k] = v
                continue

    ez_env.group = curr
    ez_env.roles = {}
    for k, v in routes.items():
        if k == curr:
            env.hosts = _pssh(v)
            env.use_ssh_config = True
        if k == 'online':
            k = 'ol'
        ez_env.roles[k] = _pssh(v)
        env.roledefs[k] = ez_env.roles[k]


def bind_cloud(cloud_options, cloud_class=None):
    ez_env.cloud = cloud_options
    if cloud_class:
        ez_env.cc['cloud_class'] = cloud_class


def debug(flag=None):
    """
    get or set debug flag
    :param flag:
    :return:
    """
    if flag is not None:
        ez_env.debug = flag
    return ez_env.debug


def help():
    commands = list_commands(None, 'nested')
    support_type = [
     'cmd', 'cloud', 'classic', 'config', 'io', 'py', 'git']
    ignore = ['Dumper', 'Loader', 'bind_cloud', 'bind_hosts', 'dump',
     'dump_codes']
    origin = ['Available commands:']
    print commands
    return
    for c in commands_buff:
        compare = c.strip()
        print compare
        if compare in ignore:
            continue
        if compare in origin:
            print c
            continue

    return