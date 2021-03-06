# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/vis/plot.py
# Compiled at: 2019-10-29 08:43:48
# Size of source mod 2**32: 4567 bytes
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ..utils.itis import is_str, is_seq
plt.rcParams['axes.unicode_minus'] = False
plt.tick_params(top='off', right='off')
marks = ['o', 'x']

def draw_line(y_data, x_data=None, figsize=None, show_value=False, legends=None, title=None, x_label=None, y_label=None, x_ticklabels=None, y_ticklabels=None, x_tick_rotation=0, y_tick_rotation=0, x_line_values=None, y_line_values=None, marker='o', linestyle='-', linewidth=2, color='r', save_path=None):
    y_data = np.array(y_data)
    if not y_data.ndim <= 2:
        raise AssertionError
    else:
        cnt = y_data.shape[0]
        if x_data is not None:
            x_data = np.array(x_data)
            assert x_data.shape == y_data.shape
        else:
            x_data = np.array([i for i in range(y_data.shape[1])] * cnt).reshape(y_data.shape)
        if y_data.ndim == 1:
            y_data = y_data[None, :]
            x_data = x_data[None, :]
        if not figsize is None:
            if not (isinstance(figsize, tuple) and len(figsize) == 2):
                raise AssertionError
        if not legends is None:
            if not (is_seq(legends) and len(legends) == cnt):
                raise AssertionError
        if is_str(color):
            color = [
             color] * cnt
        else:
            if is_seq(color):
                color = list(color)[:cnt]
                if len(color) < cnt:
                    color = color + [color[(-1)]] * (cnt - len(color))
            else:
                color = [
                 'r'] * cnt
    for i in range(cnt):
        marker = marker if marker is not None else marks[(i % len(marks))]
        plt.plot((x_data[i, :]),
          (y_data[i, :]), linestyle=linestyle, linewidth=linewidth, color=(color[i]), marker=marker,
          label=(None if legends is None else legends[i]))
        if show_value:
            for a, b in zip(x_data[i, :], y_data[i, :]):
                plt.annotate(('%.3f' % b), xy=(a, b), xytext=(-20, 10), textcoords='offset points')

    if title is not None:
        plt.title(title)
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    if x_ticklabels is not None:
        plt.gca().set_xticklabels(x_ticklabels)
        if x_tick_rotation > 0:
            for tick in plt.gca().get_xticklabels():
                tick.set_rotation(x_tick_rotation)

    if y_ticklabels is not None:
        plt.gca().set_yticklabels(y_ticklabels)
        if y_tick_rotation > 0:
            for tick in plt.gca().get_yticklabels():
                tick.set_rotation(y_tick_rotation)

    if x_line_values is not None:
        if not is_seq(x_line_values):
            x_line_values = [
             x_line_values]
        for x in x_line_values:
            plt.axvline(x=x, ymax=(np.max(y_data)), linestyle='--')

    if y_line_values is not None:
        if not is_seq(y_line_values):
            y_line_values = [
             y_line_values]
        for y in y_line_values:
            plt.axhline(y=y, linestyle='--')

    if legends is not None:
        plt.legend()
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()


def draw_bar(data_list, show_value=True, legends=None, title=None, x_ticklabels=None, y_ticklabels=None, x_tick_rotation=0, y_tick_rotation=0, alpha=0.9, save_path=None):
    if not (len(data_list) > 0 and is_seq(data_list[0])):
        raise AssertionError
    else:
        if not legends is None:
            if not (is_seq(legends) and len(legends) == len(data_list)):
                raise AssertionError
            else:
                width = 1 / len(data_list)
                for ix, data in enumerate(data_list):
                    plt.bar((list(range(len(data)))), data, width=width, label=(legends[ix]), alpha=alpha, tick_label=x_ticklabels)
                    if show_value:
                        for i in range(len(data)):
                            plt.text(i, (data[i]), ('%.3f' % data[i]), ha='center', va='bottom', fontsize=11)

                if x_ticklabels is not None:
                    if x_tick_rotation > 0:
                        for tick in plt.gca().get_xticklabels():
                            tick.set_rotation(x_tick_rotation)

                if y_ticklabels is not None:
                    plt.gca().set_yticklabels(y_ticklabels)
                    if y_tick_rotation > 0:
                        for tick in plt.gca().get_yticklabels():
                            tick.set_rotation(y_tick_rotation)

        else:
            if legends is not None:
                plt.legend()
            if title is not None:
                plt.title(title)
        if save_path is not None:
            plt.savefig(save_path)
    plt.show()