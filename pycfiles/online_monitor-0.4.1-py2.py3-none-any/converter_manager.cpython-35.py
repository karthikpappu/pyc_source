# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/converter/converter_manager.py
# Compiled at: 2015-10-27 08:51:54
# Size of source mod 2**32: 1972 bytes
import logging, time, psutil, sys
from online_monitor.converter.transceiver import Transceiver
from online_monitor.utils import utils

class ConverterManager(object):

    def __init__(self, configuration, loglevel='INFO'):
        utils.setup_logging(loglevel)
        logging.info('Initialize converter mananager with configuration in %s', configuration)
        self.configuration = utils.parse_config_file(configuration)

    def _info_output(self, process_infos):
        info_str = 'INFO: Sytem CPU usage: %1.1f' % psutil.cpu_percent()
        for process_info in process_infos:
            info_str += ', %s CPU usage: %1.1f ' % (process_info[0], process_info[1].cpu_percent())

        info_str += '\r'
        sys.stdout.write(info_str)
        sys.stdout.flush()

    def start(self):
        if not self.configuration['converter']:
            raise RuntimeError('Cannot find any converters defined in the configuration')
        logging.info('Starting %d converters', len(self.configuration['converter']))
        converters, process_infos = [], []
        for converter_name, converter_settings in self.configuration['converter'].items():
            converter_settings['name'] = converter_name
            converter = utils.load_converter(converter_settings['data_type'], base_class_type=Transceiver, *(), **converter_settings)
            converter.start()
            process_infos.append((converter_name, psutil.Process(converter.ident)))
            converters.append(converter)

        try:
            while True:
                self._info_output(process_infos)
                time.sleep(1)

        except KeyboardInterrupt:
            logging.info('CRTL-C pressed, shutting down %d converters', len(self.configuration['converter']))
            for converter in converters:
                converter.shutdown()

        for converter in converters:
            converter.join()

        logging.info('Close converter manager')