# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/client.py
# Compiled at: 2017-02-27 23:23:39
import bz2, glob, imp, json, logging, logging.config, os, signal, sys, tarfile, time
from datetime import datetime
import centinel
from centinel.backend import get_meta
from centinel.primitives.tcpdump import Tcpdump
from experiment import ExperimentList
from centinel.vpn.cli import get_external_ip
loaded_modules = set()
tds = []

def signal_handler(signal, frame):
    logging.warn('Interrupt signal received.')
    if len(tds) > 0:
        logging.warn('Stopping TCP dump...')
        for td in tds:
            td.stop()
            td.delete()

    logging.warn('Exiting...')
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)

class Client:

    def __init__(self, config, vpn_provider=None):
        self.config = config
        self.experiments = self.load_experiments()
        self._meta = None
        self.vpn_provider = vpn_provider
        return

    def setup_logging(self):
        log_config = {'version': 1, 'formatters': {'error': {'format': self.config['log']['log_format']}, 'debug': {'format': self.config['log']['log_format']}}, 'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'debug', 
                                    'level': self.config['log']['log_level']}, 
                        'file': {'class': 'logging.FileHandler', 'filename': self.config['log']['log_file'], 
                                 'formatter': 'error', 
                                 'level': self.config['log']['log_level']}}, 
           'root': {'handlers': ('console', 'file'), 'level': self.config['log']['log_level']}}
        logging.config.dictConfig(log_config)
        logging.debug('Finished setting up logging.')

    def get_result_file(self, name, start_time):
        result_file = '%s-%s.json.bz2' % (name, start_time)
        return os.path.join(self.config['dirs']['results_dir'], result_file)

    def get_input_file(self, experiment_name):
        input_file = '%s' % experiment_name
        return os.path.join(self.config['dirs']['data_dir'], input_file)

    def load_input_file(self, name):
        input_file = self.get_input_file(name)
        if not os.path.isfile(input_file):
            logging.error('Input file not found %s' % input_file)
            return
        else:
            try:
                input_file_handle = open(input_file)
            except Exception as exp:
                logging.exception('Can not read from %s: %s' % (input_file, str(exp)))
                return

            logging.debug('Input file %s loaded.' % name)
            return input_file_handle

    def load_experiments(self):
        """This function will return the list of experiments.
        """
        logging.debug('Loading experiments.')
        exp_dir = self.config['dirs']['experiments_dir']
        for path in glob.glob(os.path.join(exp_dir, '[!_]*.py')):
            name, ext = os.path.splitext(os.path.basename(path))
            try:
                if name in loaded_modules:
                    continue
                imp.load_source(name, path)
                loaded_modules.add(name)
                logging.debug('Loaded experiment "%s(%s)".' % (name, path))
            except Exception as exception:
                logging.exception('Failed to load experiment %s: %s' % (
                 name, exception))

        logging.debug('Finished loading experiments.')
        return ExperimentList.experiments

    def has_experiments_to_run(self):
        sched_filename = os.path.join(self.config['dirs']['experiments_dir'], 'scheduler.info')
        sched_info = {}
        if os.path.exists(sched_filename):
            with open(sched_filename, 'r') as (file_p):
                sched_info = json.load(file_p)
        for name in sched_info:
            run_next = sched_info[name]['last_run']
            run_next += sched_info[name]['frequency']
            if run_next <= time.time():
                logging.debug('Client has experiment(s) to run (%s).' % name)
                return True

        logging.debug('Client has no experiments to run.')
        return False

    def get_meta(self):
        """we only want to get the meta information (our normalized IP) once,
        so we are going to do lazy instantiation to improve performance

        """
        if self._meta is None:
            external_ip = get_external_ip()
            if external_ip:
                self._meta = get_meta(self.config, external_ip)
            else:
                raise Exception('Unable to get public IP')
            if 'custom_meta' in self.config:
                self._meta['custom_meta'] = self.config['custom_meta']
        return self._meta

    def run(self, data_dir=None):
        """
        Note: this function will check the experiments directory for a
        special file, scheduler.info, that details how often each
        experiment should be run and the last time the experiment was
        run. If the time since the experiment was run is shorter than
        the scheduled interval in seconds, then the experiment will
        not be run.

        :param data_dir:
        :return:
        """
        if data_dir:
            centinel_home = data_dir
            self.config['dirs']['results_dir'] = os.path.join(centinel_home, 'results')
        logging.info('Centinel started.')
        if not os.path.exists(self.config['dirs']['results_dir']):
            logging.warn('Creating results directory in %s' % self.config['dirs']['results_dir'])
            os.makedirs(self.config['dirs']['results_dir'])
        logging.debug('Results directory: %s' % self.config['dirs']['results_dir'])
        sched_filename = os.path.join(self.config['dirs']['experiments_dir'], 'scheduler.info')
        logging.debug('Loading scheduler file.')
        sched_info = {}
        if os.path.exists(sched_filename):
            with open(sched_filename, 'r') as (file_p):
                try:
                    sched_info = json.load(file_p)
                except Exception as exp:
                    logging.error('Failed to load the scheduler: %s' % str(exp))
                    return

        logging.debug('Scheduler file loaded.')
        logging.debug('Processing the experiment schedule.')
        for name in sched_info:
            run_next = sched_info[name]['last_run']
            run_next += sched_info[name]['frequency']
            if run_next > time.time():
                run_next_str = datetime.fromtimestamp(long(run_next))
                logging.debug('Skipping %s, it will be run on or after %s.' % (
                 name, run_next_str))
                continue
            if 'python_exps' not in sched_info[name]:
                self.run_exp(name=name)
            else:
                exps = sched_info[name]['python_exps'].items()
                for python_exp, exp_config in exps:
                    logging.debug('Running %s.' % python_exp)
                    self.run_exp(name=python_exp, exp_config=exp_config, schedule_name=name)
                    logging.debug('Finished running %s.' % python_exp)

            sched_info[name]['last_run'] = time.time()

        logging.debug('Updating timeout values in scheduler.')
        with open(sched_filename, 'w') as (file_p):
            json.dump(sched_info, file_p, indent=2, separators=(',', ': '))
        self.consolidate_results()
        logging.info('Finished running experiments. Look in %s for results.' % self.config['dirs']['results_dir'])

    def run_exp(self, name, exp_config=None, schedule_name=None):
        if name[-3:] == '.py':
            name = name[:-3]
        if name not in self.experiments:
            logging.error('Experiment file %s not found! Skipping.' % name)
        else:
            exp_class = self.experiments[name]
            results = {'meta': {}}
            try:
                logging.debug('Getting metadata for experiment...')
                meta = self.get_meta()
                results['meta'] = meta
            except Exception as exception:
                logging.exception('Error fetching metadata for %s: %s' % (
                 name, exception))
                results['meta_exception'] = str(exception)

            if schedule_name is not None:
                results['meta']['schedule_name'] = schedule_name
            else:
                results['meta']['schedule_name'] = name
            start_time = datetime.now()
            results['meta']['client_time'] = start_time.isoformat()
            results['meta']['centinel_version'] = centinel.__version__
            if self.vpn_provider:
                results['meta']['vpn_provider'] = self.vpn_provider
            input_files = {}
            if exp_config is not None:
                if 'input_files' in exp_config and exp_config['input_files'] is not None:
                    for filename in exp_config['input_files']:
                        file_handle = self.load_input_file(filename)
                        if file_handle is not None:
                            input_files[filename] = file_handle

                if 'params' in exp_config and exp_config['params'] is not None:
                    exp_class.params = exp_config['params']
            if len(input_files) == 0:
                if exp_class.input_files is not None:
                    for filename in exp_class.input_files:
                        file_handle = self.load_input_file(filename)
                        if file_handle is not None:
                            input_files[filename] = file_handle

                else:
                    filename = '%s.txt' % name
                    file_handle = self.load_input_file(filename)
                    if file_handle is not None:
                        input_files[filename] = file_handle
            try:
                logging.debug('Initializing the experiment class for %s' % name)
                global_constants = {'experiments_dir': self.config['dirs']['experiments_dir'], 'results_dir': self.config['dirs']['results_dir'], 
                   'data_dir': self.config['dirs']['data_dir']}
                exp_class.global_constants = global_constants
                exp = exp_class(input_files)
            except Exception as exception:
                logging.exception('Error initializing %s: %s' % (name, exception))
                results['init_exception'] = str(exception)
                return

            exp.global_constants = global_constants
            run_tcpdump = True
            if self.config['results']['record_pcaps'] is False:
                logging.info('Your configuration has disabled pcap recording, tcpdump will not start.')
                run_tcpdump = False
                exp.record_pcaps = False
            if run_tcpdump and os.geteuid() != 0:
                logging.info('Centinel is not running as root, tcpdump will not start.')
                run_tcpdump = False
            if run_tcpdump and exp_class.overrides_tcpdump:
                logging.info('Experiment overrides tcpdump recording.')
                run_tcpdump = False
            tcpdump_started = False
            try:
                if run_tcpdump:
                    td = Tcpdump()
                    tds.append(td)
                    td.start()
                    tcpdump_started = True
                    logging.info('tcpdump started...')
                    time.sleep(2)
            except Exception as exp:
                logging.exception('Failed to run tcpdump: %s' % (exp,))

            try:
                exp.run()
            except Exception as exception:
                logging.exception('Error running %s: %s' % (name, exception))
                results['runtime_exception'] = str(exception)
            except KeyboardInterrupt:
                logging.warn('Keyboard interrupt received, stopping experiment...')

            results_dir = self.config['dirs']['results_dir']
            if exp.external_results is not None:
                logging.debug('Writing external files for %s' % name)
                for fname, fcontents in exp.external_results.items():
                    external_file_name = 'external_%s-%s-%s.bz2' % (
                     name,
                     start_time.strftime('%Y-%m-%dT%H%M%S.%f'),
                     fname)
                    external_file_path = os.path.join(results_dir, external_file_name)
                    try:
                        with open(external_file_path, 'w:bz2') as (file_p):
                            data = bz2.compress(fcontents)
                            file_p.write(data)
                            logging.debug('External file %s written successfully' % fname)
                    except Exception as exp:
                        logging.exception('Failed to write external file:%s' % exp)

                logging.debug('Finished writing external files for %s' % name)
            if tcpdump_started:
                logging.info('Waiting for tcpdump to process packets...')
                time.sleep(5)
                td.stop()
                logging.info('tcpdump stopped.')
                bz2_successful = False
                data = None
                try:
                    pcap_file_name = 'pcap_%s-%s.pcap.bz2' % (
                     name, start_time.strftime('%Y-%m-%dT%H%M%S.%f'))
                    pcap_file_path = os.path.join(results_dir, pcap_file_name)
                    with open(pcap_file_path, 'wb') as (pcap_bz2):
                        with open(td.pcap_filename(), 'rb') as (pcap):
                            compressor = bz2.BZ2Compressor()
                            compressed_size_so_far = 0
                            for pcap_data in iter(lambda : pcap.read(10240), ''):
                                compressed_chunk = compressor.compress(pcap_data)
                                pcap_bz2.write(compressed_chunk)
                                if len(compressed_chunk):
                                    compressed_size_so_far += len(compressed_chunk)

                            compressed_chunk = compressor.flush()
                            pcap_bz2.write(compressed_chunk)
                            if len(compressed_chunk):
                                compressed_size_so_far += len(compressed_chunk)
                            uncompressed_size = os.path.getsize(td.pcap_filename())
                            compression_ratio = 100 * (float(compressed_size_so_far) / float(uncompressed_size))
                            logging.debug('pcap BZ2 compression: compressed/uncompressed (ratio): %d/%d (%.1f%%)' % (
                             compressed_size_so_far, uncompressed_size, compression_ratio))
                    logging.info('Saved pcap to %s.' % pcap_file_path)
                    bz2_successful = True
                except Exception as exception:
                    logging.exception('Failed to compress and write pcap file: %s' % exception)

                if not bz2_successful:
                    logging.info('Writing pcap file uncompressed')
                    try:
                        pcap_file_name = 'pcap_%s-%s.pcap' % (
                         name, start_time.strftime('%Y-%m-%dT%H%M%S.%f'))
                        pcap_file_path = os.path.join(results_dir, pcap_file_name)
                        with open(pcap_file_path, 'wb') as (pcap_out):
                            with open(td.pcap_filename(), 'rb') as (pcap):
                                for pcap_data in iter(lambda : pcap.read(10240), ''):
                                    pcap_out.write(pcap_data)

                        logging.info('Saved pcap to %s.' % pcap_file_path)
                    except Exception as exception:
                        logging.exception('Failed to write pcap file: %s' % exception)

                logging.debug('Removing pcap data from memory')
                td.delete()
                del data
                del td
            logging.debug('Closing input files for %s' % name)
            if type(input_files) is dict:
                for file_name, file_handle in input_files.items():
                    try:
                        file_handle.close()
                    except AttributeError:
                        logging.warning('Closing %s failed' % file_name)

            logging.debug('Input files closed for %s' % name)
            logging.debug('Storing results for %s' % name)
            try:
                results[name] = exp.results
            except Exception as exception:
                logging.exception('Error storing results for %s: %s' % (
                 name, exception))
                if 'results_exception' not in results:
                    results['results_exception'] = {}
                results['results_exception'][name] = str(exception)

            end_time = datetime.now()
            time_taken = end_time - start_time
            results['meta']['time_taken'] = time_taken.total_seconds()
            logging.info('%s took %s to finish.' % (name, time_taken))
            logging.debug('Saving %s results to file' % name)
            try:
                result_file_path = self.get_result_file(name, start_time.strftime('%Y-%m-%dT%H%M%S.%f'))
                result_file = bz2.BZ2File(result_file_path, 'w')
                json.dump(results, result_file, indent=2, separators=(',', ': '), ensure_ascii=False)
                result_file.close()
                del results
                del result_file
            except Exception as exception:
                logging.exception('Error saving results for %s to file: %s' % (
                 name, exception))

            logging.debug('Done saving %s results to file' % name)
        return

    def consolidate_results(self):
        result_files = [ path for path in glob.glob(os.path.join(self.config['dirs']['results_dir'], '*.json.bz2'))
                       ]
        if len(result_files) >= self.config['results']['files_per_archive']:
            logging.info('Compressing and archiving results.')
            files_archived = 0
            archive_count = 0
            tar_file = None
            files_per_archive = self.config['results']['files_per_archive']
            results_dir = self.config['dirs']['results_dir']
            for path in result_files:
                if files_archived % files_per_archive == 0:
                    archive_count += 1
                    archive_filename = 'results-%s_%d.tar.bz2' % (
                     datetime.now().strftime('%Y-%m-%dT%H%M%S.%f'), archive_count)
                    archive_file_path = os.path.join(results_dir, archive_filename)
                    logging.info('Creating new archive %s' % archive_file_path)
                    if tar_file:
                        tar_file.close()
                    tar_file = tarfile.open(archive_file_path, 'w:bz2')
                tar_file.add(path, arcname=os.path.basename(path))
                os.remove(path)
                files_archived += 1

            if tar_file:
                tar_file.close()
        return