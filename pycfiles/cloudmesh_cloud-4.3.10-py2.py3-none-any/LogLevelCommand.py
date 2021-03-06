# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/LogLevelCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand, ShellPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.LogUtil import LogUtil
LOGGER = LogUtil.get_logger()

class LogLevelCommand(PluginCommand, CloudPluginCommand, ShellPluginCommand):
    topics = {'loglevel': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command loglevel')

    @command
    def do_loglevel(self, args, arguments):
        """
        ::

            Usage:
                loglevel set MODE [--cloud=CLOUD]
                loglevel get [--cloud=CLOUD]
                loglevel save [--cloud=CLOUD]

            Arguments:
                MODE    log level mode [DEBUG/INFO/WARNING/CRITICAL/ERROR]

            Options:
                --cloud=CLOUD    the name of the cloud

        Description:
            loglevel command sets the default logging level
            for a cloud.

        Examples:
            loglevel set DEBUG --cloud=kilo
                sets the default log level to DEBUG for kilo.

            loglevel get --cloud=kilo
                retreives the default log level for kilo cloud.

            loglevel save --cloud=kilo
                saves the log level preference to the db & yaml file.

        """
        cloud = arguments['--cloud'] or Default.cloud
        LOGGER.info('Cloud: ' + cloud + ', Arguments: ' + str(arguments))
        if arguments['set']:
            try:
                log_level = arguments['MODE']
                response = LogUtil.set_level(log_level=log_level, cloudname=cloud)
                if response is not None:
                    Console.ok(response)
            except Exception as ex:
                Console.error(ex.message)

        elif arguments['get']:
            try:
                log_level = LogUtil.get_level(cloudname=cloud)
                Console.ok('Current Log Level = ' + log_level + '. Ok.')
            except Exception as ex:
                Console.error(ex.message)

        elif arguments['save']:
            LogUtil.save(cloudname=cloud)
        return