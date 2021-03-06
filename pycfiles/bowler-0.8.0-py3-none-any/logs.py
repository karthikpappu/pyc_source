# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/logs.py
# Compiled at: 2014-09-28 15:41:32
__doc__ = '\nThis module is the logs command of bowl.\n\nCreated on 14 March 2014\n@author: Charlie Lewis\n'
import docker, os
from bowl.cli_opts import list

class Object(object):
    pass


class logs(object):
    """
    This class is responsible for the logs command of the cli.
    """

    @classmethod
    def main(self, args):
        directory = args.metadata_path
        directory = os.path.expanduser(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        list_args = Object()
        list_args.metadata_path = args.metadata_path
        list_args.z = True
        list_a = list.list.main(list_args)
        for container in list_a:
            if args.CONTAINER in container:
                host = container.split(',')[1]
                cont = container.split(',')[0]
                try:
                    c = docker.Client(base_url='tcp://' + host + ':2375', version='1.12', timeout=2)
                    output = c.logs(cont)
                    if not args.z:
                        print output
                    return output
                except:
                    if not args.z:
                        print 'unable to get logs for container ' + cont
                    return False