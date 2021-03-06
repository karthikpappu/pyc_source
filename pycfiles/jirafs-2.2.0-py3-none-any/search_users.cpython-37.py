# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/search_users.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 1414 bytes
from __future__ import print_function
import json
from prettytable import PrettyTable
from jirafs import utils
from jirafs.plugin import CommandResult, DirectOutputCommandPlugin
from jirafs.ticketfolder import TicketFolder

class Command(DirectOutputCommandPlugin):
    __doc__ = 'Search for users matching the specified search term'
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'
    AUTOMATICALLY_INSTANTIATE_FOLDER = False

    def main(self, args, jira, path, parser, **kwargs):
        search_term = ' '.join(args.terms)
        try:
            tf = TicketFolder(path, jira)
            jira_client = tf.jira
        except IOError:
            jira_client = jira(utils.get_default_jira_server())

        users = jira_client.search_users(search_term)
        if args.json:
            print(json.dumps([u.raw for u in users]))
            return
        else:
            return users or CommandResult('No matching users were found', return_code=1)
        table = PrettyTable(['Name', 'Username', 'Email Address', 'Time Zone'])
        table.align = 'l'
        for user in users:
            table.add_row([
             user.displayName, user.name, user.emailAddress, user.timeZone])

        return CommandResult(table)

    def add_arguments(self, parser):
        parser.add_argument('terms', nargs='*')
        parser.add_argument('--json', default=False, action='store_true')