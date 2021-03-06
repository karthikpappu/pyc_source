# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/commands/subscription/subscription_role.py
# Compiled at: 2017-03-01 08:38:06
__author__ = 'UShareSoft'
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from uforgecli.utils import org_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from uforgecli.utils.uforgecli_utils import *
from uforge.objects import uforge
from uforgecli.utils import uforgecli_utils
import pyxb, shlex

class Subscription_Roles(Cmd, CoreGlobal):
    """Manage subscription profile roles"""
    cmd_name = 'role'

    def __init__(self):
        super(Subscription_Roles, self).__init__()

    def arg_add(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' add', add_help=True, description='Add roles to a subscription profile')
        mandatory = doParser.add_argument_group('mandatory arguments')
        optional = doParser.add_argument_group('optional arguments')
        mandatory.add_argument('--name', dest='name', required=True, help='The name of the subscription profile')
        mandatory.add_argument('--roles', dest='roles', nargs='+', required=True, help='The roles to add to the subscription profile')
        optional.add_argument('--org', dest='org', required=False, help='The organization name. If no organization is provided, then the default organization is used.')
        optional.add_argument('--allusers', dest='allusers', action='store_true', required=False, help='if set, all existing active users of that subscription profile benefit from the role addition.')
        return doParser

    def do_add(self, args):
        try:
            doParser = self.arg_add()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            printer.out('Getting subscription profile with name [' + doArgs.name + ']...')
            org = org_utils.org_get(self.api, doArgs.org)
            subscriptions = self.api.Orgs(org.dbId).Subscriptions().Getall(Search=None)
            exist = False
            for item in subscriptions.subscriptionProfiles.subscriptionProfile:
                if item.name == doArgs.name:
                    exist = True
                    all_roles = roles()
                    all_roles.roles = pyxb.BIND()
                    for r in item.roles.role:
                        already_role = role()
                        already_role.name = r.name
                        all_roles.roles.append(already_role)

                    for nr in doArgs.roles:
                        new_role = role()
                        new_role.name = nr
                        all_roles.roles.append(new_role)
                        printer.out('Added role ' + new_role.name)

                    self.api.Orgs(org.dbId).Subscriptions(item.dbId).Roles.Update(Allusers=doArgs.allusers, body=all_roles)
                    printer.out('Some roles added for subscription profile [' + doArgs.name + ']...', printer.OK)

            if not exist:
                printer.out("Subscription profile requested don't exist in [" + org.name + ']')
            return 0
        except ArgumentParserError, e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_add()
        except Exception, e:
            return handle_uforge_exception(e)

        return

    def help_add(self):
        doParser = self.arg_add()
        doParser.print_help()

    def arg_remove(self):
        doParser = ArgumentParser(prog=self.cmd_name + ' remove', add_help=True, description='Remove one or several roles from a subscription profile')
        mandatory = doParser.add_argument_group('mandatory arguments')
        optional = doParser.add_argument_group('optional arguments')
        mandatory.add_argument('--name', dest='name', required=True, help='the name of the subscription profile')
        mandatory.add_argument('--roles', dest='roles', nargs='+', required=True, help='the roles to add to the subscription profile')
        optional.add_argument('--org', dest='org', required=False, help='the organization name. If no organization is provided, then the default organization is used.')
        optional.add_argument('--allusers', dest='allusers', action='store_true', required=False, help='if set, all existing active users of that subscription profile benefit from the role deletion.')
        return doParser

    def do_remove(self, args):
        try:
            doParser = self.arg_remove()
            doArgs = doParser.parse_args(shlex.split(args))
            if not doArgs:
                return 2
            printer.out('Getting subscription profile with name [' + doArgs.name + ']...')
            org = org_utils.org_get(self.api, doArgs.org)
            subscriptions = self.api.Orgs(org.dbId).Subscriptions().Getall(Search=None)
            exist = False
            for item in subscriptions.subscriptionProfiles.subscriptionProfile:
                if item.name == doArgs.name:
                    exist = True
                    all_roles = roles()
                    all_roles.roles = pyxb.BIND()
                    for r in item.roles.role:
                        if r.name not in doArgs.roles:
                            already_role = role()
                            already_role.name = r.name
                            all_roles.roles.append(already_role)
                        else:
                            printer.out('Removed ' + r.name + ' role.')

                    self.api.Orgs(org.dbId).Subscriptions(item.dbId).Roles.Update(Allusers=doArgs.allusers, body=all_roles)
                    printer.out('Somes roles removed from subscription profile [' + doArgs.name + ']...', printer.OK)

            if not exist:
                printer.out("Subscription profile requested don't exist in [" + org.name + ']')
            return 0
        except ArgumentParserError, e:
            printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)
            self.help_remove()
        except Exception, e:
            return handle_uforge_exception(e)

        return

    def help_remove(self):
        doParser = self.arg_remove()
        doParser.print_help()