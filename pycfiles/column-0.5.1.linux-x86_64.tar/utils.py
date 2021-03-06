# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/utils.py
# Compiled at: 2017-08-02 01:06:09
import ConfigParser, os
from ansible import cli
from ansible.parsing import dataloader
from ansible.parsing import vault
ANSIBLE_CFG = os.path.join(os.sep, 'etc', 'ansible', 'ansible.cfg')
VAULT_PWD_FILE = os.path.join(os.sep, 'etc', 'column', 'vault_pass.txt')
DEFAULTS = {'vault_password_file': VAULT_PWD_FILE}

def _get_vault_password_file():
    if os.path.exists(ANSIBLE_CFG):
        cfg = ConfigParser.ConfigParser(DEFAULTS)
        cfg.read(ANSIBLE_CFG)
        return cfg.get('defaults', 'vault_password_file')


def vault_decrypt(value):
    vault_password = cli.CLI.read_vault_password_file(_get_vault_password_file(), dataloader.DataLoader())
    this_vault = vault.VaultLib(vault_password)
    return this_vault.decrypt(value)


def vault_encrypt(value):
    vault_password = cli.CLI.read_vault_password_file(_get_vault_password_file(), dataloader.DataLoader())
    this_vault = vault.VaultLib(vault_password)
    return this_vault.encrypt(value)