# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/summary.py
# Compiled at: 2016-09-09 23:03:24
"""
A stand-alone script to print summary statistics about a data file.
Runs without arguments - GUI dialogs are used to select the
chain and info files.
"""
import os
from argparse import ArgumentParser as arg_parser
from prettytable import PrettyTable as pt
import data_loader
from plot_options import default
import superplot.statslib.point as stats, superplot.statslib.one_dim as one_dim

def _summary(name, param, posterior, chi_sq):
    """
    Find summary statistics for a single parameter.
    
    :param name: Name of parameter
    :type name: string
    :param param: Data column of parameter
    :type param:
    :param posterior:
    :type posterior:
    :param chi_sq:
    :type chi_sq:
    
    :returns: List of summary statistics for a particular parameter
    :rtype: list
    """
    bestfit = stats.best_fit(chi_sq, param)
    post_mean = stats.posterior_mean(posterior, param)
    pdf_data = one_dim.posterior_pdf(param, posterior, nbins=default('nbins'), bin_limits=default('bin_limits'))
    lower_credible_region = one_dim.credible_region(pdf_data.pdf, pdf_data.bin_centers, alpha=default('alpha')[1], region='lower')
    upper_credible_region = one_dim.credible_region(pdf_data.pdf, pdf_data.bin_centers, alpha=default('alpha')[1], region='upper')
    summary = [
     name,
     bestfit,
     post_mean,
     lower_credible_region,
     upper_credible_region]
    return summary


def _summary_table(labels, data, names=None, datafile=None, infofile=None):
    """
    Summarize multiple parameters in a table.
    
    :returns: Table of summary statistics for particular parameters
    :rtype: string
    """
    if names is None:
        names = labels.values()
    beta_percent = 100.0 * (1.0 - default('alpha')[1])
    credible_name = '%.2g%% credible region' % beta_percent
    headings = [
     'Name',
     'best-fit',
     'posterior mean',
     credible_name,
     '']
    param_table = pt(headings)
    param_table.align = 'l'
    param_table.float_format = '4.2'
    posterior = data[0]
    chi_sq = data[1]
    for key, name in labels.iteritems():
        if name in names:
            param = data[key]
            param_table.add_row(_summary(name, param, posterior, chi_sq))

    min_chi_sq = data[1].min()
    p_value = stats.p_value(data[1], default('dof'))
    bestfit_table = pt(header=False)
    bestfit_table.align = 'l'
    bestfit_table.float_format = '4.2'
    bestfit_table.add_row(['File', datafile])
    bestfit_table.add_row(['Info-file', infofile])
    bestfit_table.add_row(['Minimum chi-squared', min_chi_sq])
    bestfit_table.add_row(['p-value', p_value])
    return bestfit_table.get_string() + '\n\n' + param_table.get_string()


def main():
    parser = arg_parser(description='Superplot summary tool', conflict_handler='resolve')
    parser.add_argument('--data_file', '-d', help='Chain file to summarise', type=str, required=True)
    parser.add_argument('--info_file', '-i', help='Info file to summarise', type=str, default=None, required=False)
    args = vars(parser.parse_args())
    datafile = os.path.abspath(args['data_file'])
    infofile = args['info_file']
    if infofile:
        infofile = os.path.abspath(infofile)
    labels, data = data_loader.load(infofile, datafile)
    summary_table = _summary_table(labels, data, datafile=datafile, infofile=infofile)
    return summary_table


if __name__ == '__main__':
    print main()