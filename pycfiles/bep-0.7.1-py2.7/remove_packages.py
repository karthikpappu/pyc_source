# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/cmds/remove_packages.py
# Compiled at: 2015-11-21 14:39:40
from Bep.core.release_info import name
from Bep.core import utils
from Bep import package
command_and_items_to_process_when_multiple_items = {}

def remove_cmd(args, additional_args, lang_dir_name, pkg_type, noise, install_dirs, pkgs_and_branches_on, pkgs_and_branches_off, everything_already_installed, **kwargs):
    """ Removes specified packages.

    Parameters
    ----------
    args:  a class inst of the argparse namespace with the arguments parsed to use during the install.
    additional_args:  list of additional args parsed from the the argparse arguments.
    lang_dir_name:  name of lang_version dir for package to remove.
    pkg_type:  str of pkg_type to remove.
    noise:  noise class inst with the verbosity level for the amount of output to deliver to stdout.
    install_dirs:  dict of install locations for installed pkgs and install logs.
    pkgs_and_branches_on:  dict of all packages and branches currently turned on for this lang_version
        and pkg_type. eg. {'ipython': ['master']}
    pkgs_and_branches_off:  dict of all packages and branches currently turned off for this lang_version
        and pkg_type.
    everything_already_installed:  dict of all installed packages by lang_version, pkg_type, pkg_name,
        and branches installed for that hierarchy.
    """

    def remove_pkg_branches(which_pkgs_and_branches_to_remove, branches_type):
        any_pkg_off_removed = False
        for pkg_to_remove, branches in which_pkgs_and_branches_to_remove.items():
            for branch_to_remove in branches:
                if branches_type == 'off':
                    branch_to_remove = ('.__{0}').format(branch_to_remove)
                pkg_inst.remove(pkg_to_remove, branch_to_remove, noise)
                any_pkg_off_removed = True

        return any_pkg_off_removed

    if 'all' in args:
        utils.when_not_quiet_mode(utils.status(('\t\tRemoving {0} {1} packages').format(lang_dir_name, pkg_type)), noise.quiet)
        pkg_inst = package.create_pkg_inst(lang_dir_name, pkg_type, install_dirs)
        any_pkg_on_removed = remove_pkg_branches(pkgs_and_branches_on, branches_type='on')
        any_pkg_off_removed = remove_pkg_branches(pkgs_and_branches_off, branches_type='off')
        if any_pkg_on_removed or any_pkg_off_removed:
            return True
        return False
    else:

        def how_to_remove_branches(pkg_to_remove, all_installed_for_pkg):
            any_how_to_displayed = False
            for quad_tuple in all_installed_for_pkg:
                lang_installed, pkg_type_installed, pkg_name_installed, branch_installed = quad_tuple
                if lang_installed == lang_dir_name and pkg_type_installed == pkg_type:
                    if branch_installed.startswith('.__'):
                        branch_installed = branch_installed.lstrip('.__')
                    remove_cue = ('Remove {0} [{1}] {2} with:').format(pkg_to_remove, branch_installed, lang_installed)
                    remove_cmd = ('{0} -l {1} remove {2} {3} --branch={4}').format(name, lang_installed, pkg_type_installed, pkg_name_installed, branch_installed)
                    command_and_items_to_process_when_multiple_items[remove_cue] = remove_cmd
                    any_how_to_displayed = True

            if any_how_to_displayed:
                return command_and_items_to_process_when_multiple_items
            else:
                return False

        def remove_branch(lang_arg, pkg_to_remove, branch_to_remove):
            pkg_inst = package.create_pkg_inst(lang_arg, pkg_type, install_dirs)
            lang_cmd = pkg_inst.lang_cmd
            if lang_dir_name == lang_cmd:

                def _remove(which_pkgs_and_branches_to_remove, branches_type, branch_to_remove=branch_to_remove):
                    if pkg_to_remove in which_pkgs_and_branches_to_remove:
                        branches_installed = which_pkgs_and_branches_to_remove[pkg_to_remove]
                        if branch_to_remove in branches_installed:
                            utils.when_not_quiet_mode(utils.status(('\tRemoving {0} [{1}] {2} {3}').format(pkg_to_remove, branch_to_remove, lang_dir_name, pkg_type)), noise.quiet)
                            if branches_type == 'off':
                                branch_to_remove = ('.__{0}').format(branch_to_remove)
                            pkg_inst.remove(pkg_to_remove, branch_to_remove, noise)
                            return True
                    else:
                        return False

                a_pkg_on_was_processed = _remove(pkgs_and_branches_on, branches_type='on')
                a_pkg_off_was_processed = _remove(pkgs_and_branches_off, branches_type='off')
                if a_pkg_on_was_processed or a_pkg_off_was_processed:
                    return True
                return False

        pkg_was_processed_or_displayed = utils.package_processor(args, additional_args, pkg_type, how_to_func=how_to_remove_branches, processing_func=remove_branch, process_str='remove', everything_already_installed=everything_already_installed)
        return pkg_was_processed_or_displayed