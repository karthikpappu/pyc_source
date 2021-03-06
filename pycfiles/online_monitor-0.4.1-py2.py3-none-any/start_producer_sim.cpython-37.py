# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/start_producer_sim.py
# Compiled at: 2015-11-30 03:47:55
# Size of source mod 2**32: 366 bytes
import online_monitor.utils as utils
from online_monitor.utils.producer_sim_manager import ProducerSimManager

def main():
    args = utils.parse_arguments()
    utils.setup_logging(args.log)
    cm = ProducerSimManager(args.config_file)
    cm.start()


if __name__ == '__main__':
    main()