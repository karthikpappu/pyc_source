# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/gatk/base_recalibrator.py
# Compiled at: 2019-11-15 09:07:24
""" MultiQC submodule to parse output from GATK BaseRecalibrator """
import logging
from collections import namedtuple
from multiqc.plots import linegraph
log = logging.getLogger(__name__)
RecalTableType = namedtuple('RecalTableType', ('pre_recalibration post_recalibration').split())
recal_table_type = RecalTableType(0, 1)

class BaseRecalibratorMixin:

    def parse_gatk_base_recalibrator(self):
        """ Find GATK BaseRecalibrator logs and parse their data """
        report_table_headers = {'#:GATKTable:Arguments:Recalibration argument collection values used in this run': 'arguments', 
           '#:GATKTable:Quantized:Quality quantization map': 'quality_quantization_map', 
           '#:GATKTable:RecalTable0:': 'recal_table_0', 
           '#:GATKTable:RecalTable1:': 'recal_table_1', 
           '#:GATKTable:RecalTable2:': 'recal_table_2'}
        samples_kept = {rt_type:set() for rt_type in recal_table_type}
        self.gatk_base_recalibrator = {recal_type:{table_name:{} for table_name in report_table_headers.values()} for recal_type in recal_table_type}
        for f in self.find_log_files('gatk/base_recalibrator', filehandles=True):
            parsed_data = self.parse_report(f['f'].readlines(), report_table_headers)
            rt_type = determine_recal_table_type(parsed_data)
            if len(parsed_data) > 0:
                if f['s_name'] in samples_kept[rt_type]:
                    log.debug(('Duplicate sample name found! Overwriting: {}').format(f['s_name']))
                else:
                    samples_kept[rt_type].add(f['s_name'])
                self.add_data_source(f, section='base_recalibrator')
                for table_name, sample_tables in parsed_data.items():
                    self.gatk_base_recalibrator[rt_type][table_name][f['s_name']] = sample_tables

        for rt_type in recal_table_type:
            for table_name, sample_tables in self.gatk_base_recalibrator[rt_type].items():
                self.gatk_base_recalibrator[rt_type][table_name] = self.ignore_samples(sample_tables)

        n_reports_found = sum([ len(samples_kept[rt_type]) for rt_type in recal_table_type ])
        if n_reports_found > 0:
            log.info(('Found {} BaseRecalibrator reports').format(n_reports_found))
            self.add_quality_score_vs_no_of_observations_section()
        return n_reports_found

    def add_quality_score_vs_no_of_observations_section(self):
        """ Add a section for the quality score vs number of observations line plot """
        sample_data = []
        data_labels = []
        for rt_type_name, rt_type in recal_table_type._asdict().items():
            sample_tables = self.gatk_base_recalibrator[rt_type]['quality_quantization_map']
            if len(sample_tables) == 0:
                continue
            count_data = {}
            pct_data = {}
            for sample, table in sample_tables.items():
                count_data[sample] = {}
                pct_data[sample] = {}
                sample_y_sum = sum(int(y) for y in table['Count'])
                for x, y in zip(table['QualityScore'], table['Count']):
                    count_data[sample][int(x)] = int(y)
                    try:
                        pct_data[sample][int(x)] = float(y) / sample_y_sum
                    except ZeroDivisionError:
                        pct_data[sample][int(x)] = 0

            sample_data.append(count_data)
            sample_data.append(pct_data)
            data_labels.append({'name': ('{} Count').format(rt_type_name.capitalize().replace('_', '-')), 
               'ylab': 'Count'})
            data_labels.append({'name': ('{} Percent').format(rt_type_name.capitalize().replace('_', '-')), 
               'ylab': 'Percent'})

        plot = linegraph.plot(sample_data, pconfig={'title': 'Observed Quality Score Counts', 
           'id': 'gatk-base-recalibrator-quality-scores-plot', 
           'xlab': 'Observed Quality Score', 
           'ylab': 'Count', 
           'xDecimals': False, 
           'data_labels': data_labels})
        self.add_section(name='Observed Quality Scores', anchor='gatk-base-recalibrator-quality-scores', description='This plot shows the distribution of base quality scores in each sample before and after base quality score recalibration (BQSR). Applying BQSR should broaden the distribution of base quality scores.', helptext="For more information see [the Broad's description of BQSR](https://gatkforums.broadinstitute.org/gatk/discussion/44/base-quality-score-recalibration-bqsr).", plot=plot)


def determine_recal_table_type(parsed_data):
    arguments = dict(zip(parsed_data['arguments']['Argument'], parsed_data['arguments']['Value']))
    if arguments['recalibration_report'] == 'null':
        return recal_table_type.pre_recalibration
    else:
        return recal_table_type.post_recalibration