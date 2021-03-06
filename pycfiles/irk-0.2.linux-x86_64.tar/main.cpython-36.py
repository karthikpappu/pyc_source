# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/main.py
# Compiled at: 2018-06-21 19:13:53
# Size of source mod 2**32: 1809 bytes
import click
from irk.util.storage.database import load_installed_database
from .commands.update import update as update_impl
from .commands.install import install as install_impl
from .commands.remove import remove as remove_impl
from .util.version import VERSION_STRING, COPYRIGHT

@click.group(invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, help='Print version information')
def main(version):
    if version:
        print(f"version {VERSION_STRING}\n{COPYRIGHT}")
        exit(0)


@main.command()
def update():
    update_impl()


@main.command()
@click.option('--dry-run/--no-dry-run', help='Print commands/actions to be ran')
@click.option('-r', '--resolver', default=None, type=str, help='Use this resolver specifically')
@click.option('-e', '--exclude-resolver', type=str, multiple=True, help='Do not use this installer (can be specified multiple times)')
@click.option('--reinstall', is_flag=True, help='Reinstall packages (often upgrades them)')
@click.argument('name')
def install(dry_run, resolver, exclude_resolver, reinstall, name):
    load_installed_database()
    exit(install_impl(name, resolver, dry_run, exclude_resolver, reinstall))


@main.command()
@click.option('--dry-run/--no-dry-run', help='Print commands/actions to be ran')
@click.option('-r', '--resolver', default=None, type=str, help='Use this resolver specifically')
@click.option('-f', '--force', default=False, is_flag=True, help="Force removal, even if we don't think we installed the package")
@click.argument('name')
def remove(dry_run, resolver, force, name):
    load_installed_database()
    exit(remove_impl(name, resolver, dry_run, force))