# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/utils/utils.py
# Compiled at: 2019-02-26 08:20:22
# Size of source mod 2**32: 10242 bytes
from .time import cal2et
from .time import et_to_datetime
import matplotlib.pyplot as plt, matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from bokeh.plotting import figure, output_file, output_notebook, show
from bokeh.models import HoverTool
from bokeh.models import DatetimeTickFormatter
from tempfile import mkstemp
from shutil import move
import os, glob
from os import fdopen, remove, chmod, path

def valid_url(html_file_name):
    """
    This function returns a valid URL for an HTML given a filename. 
    The filename is checked in such way that URL non valid characters
    are replaced by other characters. 
    
    This was used due to the fact that we were using the following string:
    
       '67P/CG' -> '67P-CG'
    
    as part of an URL for 2D plotting and it would not work
    
    :param html_file_name: Input filename 
    :type html_file_name: str
    :return: Corrected Input filename without URL non valid characters
    :rtype: str
    """
    for element in ('$', '_', '.', '+', '!', '*', '(', ')', '/', '\\'):
        if element in ('/', '\\', '!', '*', '$'):
            replacement = '-'
        else:
            replacement = '_'
        html_file_name = html_file_name.replace(element, replacement)

    return html_file_name


def convert_ESOCorbit2data(orbit_file, support_ker=''):
    orbit_data = []
    time_list = []
    distance_list = []
    with open(orbit_file, 'r') as (f):
        read_data = False
        for line in f:
            if read_data:
                line = line.split()
                time = cal2et((line[0]), 'CAL', support_ker=support_ker)
                distance = np.sqrt(float(line[1]) * float(line[1]) + float(line[2]) * float(line[2]) + float(line[3]) * float(line[3]))
                time_list.append(time)
                distance_list.append(distance)
            if 'META_STOP' in line:
                read_data = True
            if 'META_START' in line:
                read_data = False

    return [
     time_list, distance_list]


def convert_OEM2data():
    pass


def plot(xaxis, yaxis, xaxis_name='Date', yaxis_name='', title='', format='line', external_data=[], notebook=False, mission='', target='', date_format='TDB', plot_width=1000, plot_height=1000, fill_color=[], fill_alpha=0, background_image=False, line_width=2):
    if not isinstance(yaxis_name, list):
        yaxis_name = [
         yaxis_name]
        yaxis = [yaxis]
    else:
        if not title:
            title = '{} {}'.format(mission, yaxis_name).title().upper()
            html_file_name = 'plot_{}_{}_{}-{}.html'.format('Time', yaxis_name, mission, target)
            html_file_name = valid_url(html_file_name)
        else:
            title = title.upper()
            if ' ' in title:
                html_file_name = title.replace(' ', '_').upper()
            else:
                html_file_name = title
            html_file_name = valid_url(html_file_name)
        if xaxis_name == 'Date':
            window_dt = []
            window = xaxis
            for element in window:
                window_dt.append(et_to_datetime(element, date_format))

            x = window_dt
        else:
            x = xaxis
        y = yaxis
        if notebook:
            output_notebook()
            plot_width = 975
            plot_height = 400
        else:
            output_file(html_file_name + '.html')
            plot_width = plot_width
            plot_height = plot_height
        if xaxis_name == 'Date':
            x_axis_type = 'datetime'
        else:
            x_axis_type = 'auto'
        p = figure(title=title, plot_width=plot_width,
          plot_height=plot_height,
          x_axis_label=(xaxis_name.upper()),
          y_axis_label='',
          x_axis_type=x_axis_type)
        if xaxis_name == 'Date':
            p.xaxis.formatter = DatetimeTickFormatter(seconds=[
             '%Y-%m-%d %H:%M:%S'],
              minsec=[
             '%Y-%m-%d %H:%M:%S'],
              minutes=[
             '%Y-%m-%d %H:%M:%S'],
              hourmin=[
             '%Y-%m-%d %H:%M:%S'],
              hours=[
             '%Y-%m-%d %H:%M:%S'],
              days=[
             '%Y-%m-%d %H:%M:%S'],
              months=[
             '%Y-%m-%d %H:%M:%S'],
              years=[
             '%Y-%m-%d %H:%M:%S'])
        hover = HoverTool(tooltips=[
         (
          xaxis_name, '@x{0.000}'),
         (
          title, '@y{0.000}')],
          formatters={xaxis_name: 'numeral', 
         title: 'numeral'})
        p.add_tools(hover)
        if external_data:
            window_dt = []
            window = external_data[0]
            for element in window:
                window_dt.append(et_to_datetime(element, 'TDB'))

            x_ext = window_dt
            y_ext = external_data[1]
            if format == 'circle':
                p.circle(x_ext, y_ext, legend='External Data', size=5, color='red')
            elif format == 'line':
                p.line(x_ext, y_ext, legend='External Data', line_width=2, color='red')
        color_list = ['red', 'green', 'blue', 'orange']
        index = 0
        if background_image:
            p.image_url(url=[
             os.path.join(os.path.dirname(__file__), '../data/Mars_Viking_MDIM21_ClrMosaic_global_1024.jpg')],
              x=(-180),
              y=(-90),
              w=360,
              h=180,
              anchor='bottom_left',
              global_alpha=0.6)
    for element in y:
        if format == 'circle':
            p.line(x, element, line_width=line_width, color=(color_list[index]))
            p.circle(x, element, fill_color='white', size=8)
        if format == 'circle_only':
            p.circle(x, element, size=3, color='red')
        else:
            if format == 'line':
                p.line(x, element, legend=(yaxis_name[index].upper()), line_width=line_width,
                  color=(color_list[index]))
        index += 1

    show(p)


def plot3d(data, observer, target):
    x, y, z = [], [], []
    for element in data:
        x.append(element[0])
        y.append(element[1])
        z.append(element[2])

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    ax.plot(x, y, z, label=(observer.name + ' w.r.t. ' + target.name + ' on ' + observer.trajectory_reference_frame + ' [km]'))
    ax.legend()
    u = np.linspace(0, 2 * np.pi, 360)
    v = np.linspace(0, np.pi, 360)
    x = target.radii[0] * np.outer(np.cos(u), np.sin(v))
    y = target.radii[1] * np.outer(np.sin(u), np.sin(v))
    z = target.radii[2] * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='r')
    plt.show()


def replace(file_path, pattern, subst):
    replaced = False
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as (new_file):
        with open(file_path) as (old_file):
            for line in old_file:
                updated_line = line.replace(pattern, subst)
                new_file.write(updated_line)
                if updated_line != line:
                    replaced = True

    if replaced:
        chmod(abs_path, 420)
        if file_path.isupper():
            move(abs_path, file_path.split('.')[0] + '_LOCAL.TM')
        else:
            move(abs_path, file_path.split('.')[0] + '_local.tm')
        return True
    else:
        return False


def get_latest_kernel(kernel_type, path, pattern, dates=False, excluded_kernels=False):
    kernels = []
    kernel_path = os.path.join(path, kernel_type)
    kernels_with_path = glob.glob(kernel_path + '/' + pattern)
    if os.path.isdir(kernel_path + '/former_versions'):
        kernels_with_path += glob.glob(kernel_path + '/former_versions/' + pattern)
    for kernel in kernels_with_path:
        kernels.append(kernel.split('/')[(-1)])

    kernels.sort()
    if excluded_kernels:
        for kernel in excluded_kernels:
            if kernel in kernels:
                kernels.remove(kernel)

    if not dates:
        return kernels.pop()
    else:
        previous_kernel = ''
        kernels_date = []
        for kernel in kernels:
            if previous_kernel:
                if previous_kernel.upper().split('_V')[0] == kernel.upper().split('_V')[0]:
                    kernels_date.remove(previous_kernel)
            previous_kernel = kernel
            kernels_date.append(kernel)

        return kernels_date


def get_sc(kernel):
    if 'ROSETTA' in kernel.upper():
        return 'ROS'
    else:
        if 'VENUS-EXPRESS' in kernel.upper():
            return 'VEX'
        else:
            if 'MARS-EXPRESS' in kernel.upper():
                return 'MEX'
            else:
                if 'EXOMARS2016' in kernel.upper():
                    if 'edm' in kernel:
                        return 'em16_edm'
                    else:
                        return 'em16_tgo'
                if 'BEPICOLOMBO' in kernel.upper():
                    if 'mmo' in kernel:
                        return 'bc_mmo'
                    else:
                        return 'bc_mpo'
                if 'JUICE' in kernel.upper():
                    return 'juice'
            if 'SOLAR-ORBITER' in kernel.upper():
                return 'solo'
        if 'EXOMARSRSP' in kernel.upper():
            if '_sp_' in kernel:
                return 'emrsp_sp'
            else:
                return 'emrsp_rm'