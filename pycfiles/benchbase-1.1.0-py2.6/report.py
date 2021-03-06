# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/report.py
# Compiled at: 2011-09-20 05:19:26
import os, logging
from math import ceil
from bencher import Bencher
from sar import Sar
from util import str2id, render_template, gnuplot, generate_html

class Report(object):
    """Report rendering"""

    def __init__(self, db, options):
        self.db = db
        self.options = options
        self.height = options.chart_height
        self.width = options.chart_width
        self.period = options.period

    def buildReport(self, bid):
        output_dir = self.options.output
        if not os.access(output_dir, os.W_OK):
            os.mkdir(output_dir, 509)
        bencher = Bencher.getBencherForBid(self.db, self.options, bid)
        info = bencher.getInfo(bid)
        period = self.period
        def_period = int(ceil(info['duration'] / float(self.width))) * 30
        bars = 4
        plot_type = 'linespoints'
        plot_type_avg = 'lines'
        if period is None:
            if info['generator'].lower() == 'funkload':
                cycle_duration = float(info['extra']['duration'])
                period = int(ceil(cycle_duration / 4.0))
                plot_type = 'impulses'
                plot_type_avg = 'points'
            else:
                period = def_period
        if 2 * period < def_period:
            bars = 2
        params = {'dbpath': self.options.database, 'output_dir': output_dir, 'start': info['start'][11:19], 
           'end': info['end'], 
           'bid': bid, 
           'ravg': self.options.runningavg, 
           'width': self.width, 
           'height': self.height, 
           'period': period, 
           'duration': info['duration'], 
           'bars': bars, 
           'plot_type': plot_type, 
           'plot_type_avg': plot_type_avg}
        for sample in [info['all_samples']] + info['samples']:
            name = sample['name']
            data = bencher.getIntervalInfo(bid, info['start_stamp'], period, name)
            data_path = os.path.join(output_dir, str2id(name) + '.data')
            f = open(data_path, 'w')
            for row in data:
                row = [ str(i) for i in row ]
                f.write((' ').join(row) + '\n')

            f.close()
            params['data'] = os.path.basename(data_path)
            params['filter'] = " AND lb = '%s' " % name
            params['title'] = 'Sample: ' + sample['title']
            params['filename'] = str2id(name)
            if name.lower() == 'all':
                params['filter'] = ''
                params['title'] = 'All'
            script = render_template('sample-gplot.mako', **params)
            script_path = os.path.join(output_dir, str2id(name) + '.gplot')
            f = open(script_path, 'w')
            f.write(script)
            f.close()
            gnuplot(script_path)

        sar = Sar(self.db, self.options)
        info.update(sar.getInfo(bid))
        for host in info['sar'].keys():
            params['host'] = host
            params['filter'] = " AND host = '%s'" % host
            script = render_template('sar-gplot.mako', **params)
            script_path = os.path.join(output_dir, 'sar-%s.gplot' % host)
            script_path.replace(' ', '-')
            f = open(script_path, 'w')
            f.write(script)
            f.close()
            gnuplot(script_path)

        report = render_template('report.mako', **info)
        rst_path = os.path.join(output_dir, 'index.rst')
        f = open(rst_path, 'w')
        f.write(report)
        f.close()
        html_path = os.path.join(output_dir, 'index.html')
        generate_html(rst_path, html_path, output_dir)
        logging.info('Report generated: ' + html_path)
        return