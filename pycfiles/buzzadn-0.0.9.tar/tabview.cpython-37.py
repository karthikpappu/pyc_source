# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/tabview.py
# Compiled at: 2020-05-03 14:22:19
# Size of source mod 2**32: 55369 bytes
__doc__ = ' tabview.py -- View a tab-delimited file in a spreadsheet-like display.\n\n  Scott Hansen <firecat four one five three at gmail dot com>\n  Based on code contributed by A.M. Kuchling <amk at amk dot ca>\n\n'
import _curses, csv, curses, curses.ascii, io, locale, os, re, string, sys, unicodedata
from collections import Counter
from curses.textpad import Textbox
from operator import itemgetter
from subprocess import PIPE, Popen
from textwrap import wrap
import numpy as np, pandas as pd
from pandas import option_context

def colorama_data(lines, conc_data):
    """
    take a list of strings for printing, and add ansi colors
    """
    from colorama import Back, Fore, Style, init
    regex = re.compile('^\\s*([0-9]+)')
    if not conc_data:
        return lines
    lines_to_print = []
    init(autoreset=True)
    for line in lines:
        s = re.search(regex, line)
        if not s:
            continue
        num = s.group(1)
        gotnums = conc_data.get(int(num), {})
        highstr = ''
        if gotnums:
            for sty, col in gotnums.items():
                if col.upper() in ('DIM', 'NORMAL', 'BRIGHT', 'RESET_ALL'):
                    thing_to_color = Style
                elif sty == 'Back':
                    thing_to_color = Back
                else:
                    thing_to_color = Fore
                highstr += getattr(thing_to_color, col.upper())

        highstr += line + Style.RESET_ALL
        lines_to_print.append(highstr)

    return '\n'.join(lines_to_print)


def KEY_CTRL(key):
    return curses.ascii.ctrl(key)


def addstr(*args):
    scr, args = args[0], args[1:]
    return (scr.addstr)(*args)


def insstr(*args):
    scr, args = args[0], args[1:]
    return (scr.insstr)(*args)


class ReloadException(Exception):

    def __init__(self, start_pos, column_width, column_gap, column_widths, search_str):
        self.start_pos = start_pos
        self.column_width_mode = column_width
        self.column_gap = column_gap
        self.column_widths = column_widths
        self.search_str = search_str


class QuitException(Exception):
    pass


class MaybeTruncatedString(str):

    def __new__(self, s, width, trunc_char, trunc_left=False, background=False, colgap=False):
        self.original = s
        if len(s) > width:
            if trunc_left:
                s = s[-width:]
                s = trunc_char + s
            else:
                s = s[:width - 1]
                s += trunc_char
        if background:
            s += ' ' * colgap
        return str.__new__(self, s)


class Viewer(object):
    """Viewer"""

    def __init__(self, *args, **kwargs):
        os.unsetenv('LINES')
        os.unsetenv('COLUMNS')
        self.scr = args[0]
        self.data = args[1]['data']
        self.header_offset_orig = 4
        self.align_right = kwargs.get('align_right', False)
        self.trunc_left = kwargs.get('trunc_left', False)
        self.df = kwargs.get('df', False)
        self.reference = kwargs.get('reference', False)
        self.header = args[1]['header']
        self.index = args[1].get('index', False)
        self.index_depth = kwargs.get('index_depth')
        self.prev_key = False
        self.background = False
        self.header_offset = self.header_offset_orig
        self.num_data_columns = len(self.header)
        if len(self.data) > 1:
            del (any((self._is_num(cell) for cell in self.header)) or self.data)[0]
            self.header_offset = self.header_offset_orig
        else:
            self.header_offset = self.header_offset_orig - 1
        self._init_double_width(kwargs.get('double_width'))
        self.column_width_mode = kwargs.get('column_width')
        self.column_gap = kwargs.get('column_gap')
        self._init_column_widths(kwargs.get('column_width'), kwargs.get('column_widths'))
        try:
            kwargs.get('trunc_char').encode(sys.stdout.encoding or )
            self.trunc_char = kwargs.get('trunc_char')
        except (UnicodeDecodeError, UnicodeError):
            self.trunc_char = '>'

        self.x, self.y = (0, 0)
        self.win_x, self.win_y = (0, 0)
        self.max_y, self.max_x = (0, 0)
        self.num_columns = 0
        self.vis_columns = 0
        self.init_search = self.search_str = kwargs.get('search_str')
        self._search_win_open = 0
        self.modifier = str()
        self.define_keys()
        self.colours = kwargs.get('colours')
        self.colourdict = self._make_colour_dict()
        self.resize()
        self.display()
        try:
            self.goto_y(kwargs.get('start_pos')[0])
        except TypeError:
            self.goto_y(kwargs.get('start_pos'))

        try:
            self.goto_x(kwargs.get('start_pos')[1])
        except (IndexError, TypeError):
            pass

    def show_info(self):
        """Display data information in a pop-up window
        """
        fn = self.info
        yp = self.y + self.win_y
        xp = self.x + self.win_x
        location = self.location_string(yp, xp)

        def sizeof_fmt(num, suffix='B'):
            for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
                if abs(num) < 1024.0:
                    return '{:3.1f}{}{}'.format(num, unit, suffix)
                num /= 1024.0

            return '{:.1f}{}{}'.format(num, 'Yi', suffix)

        size = sizeof_fmt(sys.getsizeof(self.data))
        rows_cols = str((len(self.data), self.num_data_columns))
        info = [
         (
          'Filename/Data Info:', fn),
         (
          'Current Location:', location),
         (
          'Total Rows/Columns:', rows_cols),
         (
          'Data Size:', size)]
        display = '\n\n'.join(['{:<20}{:<}'.format(i, j) for i, j in info])
        TextBox((self.scr), data=display)()
        self.resize()

    def _is_num(self, cell):
        try:
            float(cell)
            return True
        except ValueError:
            return False

    def _init_double_width(self, dw):
        """Initialize self._cell_len to determine if double width characters
        are taken into account when calculating cell widths.

        """
        self.double_width = dw
        if self.double_width is False:
            self.double_width = len(self.data) * self.num_data_columns < 65000
        elif self.double_width is True:
            self._cell_len = self._Viewer__cell_len_dw
        else:
            self._cell_len = len

    def _make_colour_dict(self):
        """
        make a dictionary to get initialised colour pairs
        """
        if not self.colours:
            return {}
        import curses
        colours = [
         'reset',
         'black',
         'red',
         'green',
         'yellow',
         'blue',
         'magenta',
         'cyan',
         'white']
        dct = {}
        i = 1
        for c in colours:
            for d in colours:
                e = getattr(curses, 'COLOR_' + c.upper(), -1)
                f = getattr(curses, 'COLOR_' + d.upper(), -1)
                curses.init_pair(i, e, f)
                dct[(c, d)] = i
                i += 1

        return dct

    def _init_column_widths(self, cw, cws):
        """Initialize column widths

        Args: - cw: column_width mode
                cws: list of column widths

        """
        if not cws:
            self._get_column_widths(cw)
        else:
            self.column_width = cws

    def column_xw(self, x, index=False):
        """Return the position and width of the requested column"""
        scw = self.column_width
        sid = self.index_depth
        indbits = scw[:sid] if x > sid else scw[:x]
        cols = indbits + scw[self.win_x:self.win_x + x][sid:]
        xp = sum(cols) + x * self.column_gap
        w = max(0, min(self.max_x - xp, scw[(self.win_x + x)]))
        if isinstance(scw, list):
            if index:
                w = max(0, min(self.max_x - xp, scw[x]))
            else:
                w = max(0, min(self.max_x - xp, scw[(x + self.win_x)]))
        return (
         xp, w)

    def quit(self):
        raise QuitException

    def reload(self):
        start_pos = (
         self.y + self.win_y + 1, self.x + self.win_x + 1)
        raise ReloadException(start_pos, self.column_width_mode, self.column_gap, self.column_width, self.search_str)

    def consume_modifier(self, default=1):
        m = int(self.modifier) if len(self.modifier) else default
        self.modifier = str()
        return m

    def down(self):
        m = self.consume_modifier()
        yp = self.y + self.win_y
        self.goto_y(yp + 1 + m)

    def up(self):
        m = self.consume_modifier()
        yp = self.y + self.win_y
        self.goto_y(yp + 1 - m)

    def left(self):
        m = self.consume_modifier()
        xp = self.x + self.win_x
        self.goto_x(xp + 1 - m)

    def right(self):
        m = self.consume_modifier()
        xp = self.x + self.win_x
        self.goto_x(xp + 1 + m)

    def page_down(self):
        m = self.consume_modifier()
        row_shift = (self.max_y - self.header_offset) * m
        end = len(self.data) - 1
        if self.win_y <= end - row_shift:
            new_win_y = self.win_y + row_shift
            if new_win_y + self.y > end:
                self.y = end - new_win_y
            self.win_y = new_win_y
        else:
            self.y = end - self.win_y

    def page_up(self):
        m = self.consume_modifier()
        row_shift = (self.max_y - self.header_offset) * m
        if self.win_y == 0:
            self.y = 0
        elif self.win_y < row_shift:
            self.win_y = 0
        else:
            self.win_y = self.win_y - row_shift

    def page_right(self):
        for _ in range(self.consume_modifier()):
            end = self.num_data_columns - 1
            if self.win_x <= end - self.num_columns:
                cols = self.num_columns_fwd(self.win_x + self.x)
                new_win_x = self.win_x + cols
                if new_win_x + self.x > end:
                    self.x = end - new_win_x
                self.win_x = new_win_x
                self.recalculate_layout()
            else:
                self.x = end - self.win_x
                break

    def page_left(self):
        for _ in range(self.consume_modifier()):
            if self.win_x == 0:
                self.x = 0
                break
            cols = self.num_columns_rev(self.win_x + self.x)
            if self.win_x < cols:
                self.win_x = 0
                self.recalculate_layout()
            else:
                self.win_x = self.win_x - cols
                self.recalculate_layout()

    def mark(self):
        self.save_y, self.save_x = self.y + self.win_y, self.x + self.win_x

    def goto_mark(self):
        if hasattr(self, 'save_y'):
            self.goto_yx(self.save_y + 1, self.save_x + 1)

    def home(self):
        self.goto_y(1)

    def goto_y(self, y):
        y = max(min(len(self.data), y), 1)
        if self.win_y < y <= self.win_y + (self.max_y - self.header_offset - self._search_win_open):
            self.y = y - 1 - self.win_y
        elif y <= self.win_y:
            self.y = 0
            self.win_y = y - 1
        else:
            self.win_y = y - (self.max_y - self.header_offset - self._search_win_open)
            self.y = self.max_y - self.header_offset - self._search_win_open - 1

    def goto_row(self):
        m = self.consume_modifier(len(self.data))
        self.goto_y(m)

    def goto_x(self, x):
        x = max(min(self.num_data_columns, x), 1)
        if self.win_x < x <= self.win_x + self.num_columns:
            self.x = x - 1 - self.win_x
        elif x <= self.win_x:
            self.x = 0
            self.win_x = x - 1
            self.recalculate_layout()
        else:
            cols = self.num_columns_rev(x - 1)
            self.win_x = x - cols
            self.x = cols - 1
            self.recalculate_layout()

    def goto_col(self):
        m = self.consume_modifier()
        self.goto_x(m)

    def goto_yx(self, y, x):
        self.goto_y(y)
        self.goto_x(x)

    def line_home(self):
        self.goto_x(1)

    def line_end(self):
        end = len(self.data[(self.y + self.win_y)])
        self.goto_x(end)

    def find_match_line(self, concordance, filename, s, predict):
        """
        Get the concordance line related to a cell
        """
        import pandas as pd
        conc = pd.DataFrame(concordance).astype(object)
        conc = conc[(conc['file'] == filename)]
        conc = conc[(conc['s'].astype(int) == int(s))]
        conc = conc[(conc['match'].str.strip() == predict)]
        try:
            return conc.index[0]
        except IndexError:
            return

    def show_cell(self):
        """Display current cell in a pop-up window"""
        yp = self.y + self.win_y
        xp = self.x + self.win_x
        is_conc = all((i in self.df.columns for i in ('left', 'match', 'right')))
        if not is_conc:
            filename = self.data[self.y][0]
            s = self.data[self.y][1]
            col_name = self.header[xp]
            target = col_name if col_name in self.reference.columns else 'w'
            query = self.data[self.y][self.x]
            word = self.data[self.y][3]
            show = ['w'] + [target] if target != 'w' else ['w']
            predict = query if show == ['w'] else '{}/{}'.format(word, query)
            outshow = ['file', 's', 'left', 'match', 'right']
            if target not in outshow:
                outshow.append(target)
            matches = getattr(self.df.just, target)(query,
              exact_match=True, case=False, regex=False)
            concordance = matches.conc(show=show, reference=(self.reference))
            match_line = self.find_match_line(concordance, filename, s, predict)
            outshow = [i for i in outshow if i in concordance.columns]
            concordance = concordance[outshow]
            with option_context('display.max_colwidth', -1):
                text = concordance.to_string()
            cursor_line_pos = 0
            if not text:
                return
            TextBox((self.scr),
              data=text,
              title=(self.location_string(yp, xp)),
              cursor_line_pos=cursor_line_pos,
              match_line=match_line)()
            self.resize()

    def _search_validator(self, ch):
        """Fix Enter and backspace for textbox.

        Used as an aux function for the textpad.edit method

        """
        if ch == curses.ascii.NL:
            return curses.ascii.BEL
            if ch == 127:
                self.search_str = self.textpad.gather().strip().lower()[:-1]
                return 8
        elif 0 < ch < 256:
            c = chr(ch)
            if c in string.printable:
                res = self.textpad.gather().strip().lower()
                self.search_str = res + chr(ch)
                self.search_results(look_in_cur=True)
                self.display()
        return ch

    def search(self):
        """Open search window, get input and set the search string."""
        if self.init_search is not None:
            return
        scr2 = curses.newwin(3, self.max_x, self.max_y - 3, 0)
        scr3 = scr2.derwin(1, self.max_x - 12, 1, 9)
        scr2.box()
        scr2.move(1, 1)
        addstr(scr2, 'Search: ')
        scr2.refresh()
        curses.curs_set(1)
        self._search_win_open = 3
        self.textpad = Textbox(scr3, insert_mode=True)
        self.search_str = self.textpad.edit(self._search_validator)
        self.search_str = self.search_str.lower().strip()
        try:
            curses.curs_set(0)
        except _curses.error:
            pass

        if self.search_str:
            self.init_search = None
        self._search_win_open = 0

    def search_results(self, rev=False, look_in_cur=False):
        """Given self.search_str or self.init_search, find next result after
        current position and reposition the cursor there.

        Args: rev - True/False search backward if true
              look_in_cur - True/False start search in current cell

        """
        if not self.search_str:
            if not self.init_search:
                return
            else:
                self.search_str = self.search_str or 
                yp, xp = self.y + self.win_y, self.x + self.win_x
                if rev is True:
                    data, yp, xp = self._reverse_data(self.data, yp, xp)
                else:
                    data = self.data
            if look_in_cur is False:
                if xp < len(data[0]) - 1:
                    xp += 1
        elif xp >= len(data[0]) - 1 and yp < len(data) - 1:
            yp += 1
            xp = 0
        else:
            yp = xp = 0
        search_order = [self._search_cur_line_r,
         self._search_next_line_to_end,
         self._search_next_line_from_beg,
         self._search_cur_line_l]
        for search in search_order:
            y, x, res = search(data, yp, xp)
            if res is True:
                yp, xp = y, x
                break

        if rev is True:
            self.data, yp, xp = self._reverse_data(data, yp, xp)
        if res is True:
            self.goto_yx(yp + 1, xp + 1)

    def search_results_prev(self, rev=False, look_in_cur=False):
        """Search backwards"""
        self.search_results(rev=True, look_in_cur=look_in_cur)

    def _reverse_yp_xp(self, data, yp, xp):
        return (
         len(data) - 1 - yp, len(data[0]) - 1 - xp)

    def _reverse_data(self, data, yp, xp):
        yp, xp = self._reverse_yp_xp(data, yp, xp)
        data.reverse()
        for idx, i in enumerate(data):
            i.reverse()
            data[idx] = i

        return (data, yp, xp)

    def _search_cur_line_r(self, data, yp, xp):
        """Current line first, from yp,xp to the right """
        res = False
        for x, item in enumerate(data[yp][xp:]):
            if self.search_str in str(item).lower():
                xp += x
                res = True
                break

        return (
         yp, xp, res)

    def _search_cur_line_l(self, data, yp, xp):
        """Last, search from beginning of current line to current position"""
        res = x = False
        for x, item in enumerate(data[yp][:xp]):
            if self.search_str in str(item).lower():
                res = True
                break

        return (
         yp, x, res)

    def _search_next_line_to_end(self, data, yp, xp):
        """ Search from next line to the end """
        res = done = False
        for y, line in enumerate(data[yp + 1:]):
            for x, item in enumerate(line):
                if self.search_str in str(item).lower():
                    done = True
                    break

            if done is True:
                res = True
                yp, xp = yp + 1 + y, x
                break

        return (
         yp, xp, res)

    def _search_next_line_from_beg(self, data, yp, xp):
        """Search from beginning to line before current."""
        res = done = y = x = False
        for y, line in enumerate(data[:yp]):
            for x, item in enumerate(line):
                if self.search_str in str(item).lower():
                    done = True
                    break

            if done is True:
                res = True
                yp, xp = y, x
                break

        return (
         yp, xp, res)

    def help(self):
        help_txt = readme()
        idx = help_txt.index('Keybindings:\n')
        help_txt = [i.replace('**', '') for i in help_txt[idx:] if '===' not in i]
        TextBox((self.scr), data=(''.join(help_txt)), title='Help')()
        self.resize()

    def toggle_header(self):
        if self.header_offset == self.header_offset_orig:
            self.header_offset = self.header_offset - 2
            self.data.insert(0, self.header)
            self.y = self.y + 2
        elif len(self.data) == 1:
            return
        else:
            self.header_offset = self.header_offset_orig
            del self.data[self.data.index(self.header)]
            if self.y > 0:
                self.y = self.y - 2
            elif self.win_y > 0:
                self.up()
                self.down()
                self.y = self.y - 2

    def column_gap_down(self):
        self.column_gap = max(0, self.column_gap - 1)
        self.recalculate_layout()

    def column_gap_up(self):
        self.column_gap += 1
        self.recalculate_layout()

    def column_width_all_down(self):
        self.column_width = [max(1, self.column_width[i] - max(1, int(self.column_width[i] * 0.2))) for i in range(0, self.num_data_columns)]
        self.recalculate_layout()

    def column_width_all_up(self):
        self.column_width = [max(1, self.column_width[i] + max(1, int(self.column_width[i] * 0.2))) for i in range(0, self.num_data_columns)]
        self.recalculate_layout()

    def column_width_down(self):
        xp = self.x + self.win_x
        self.column_width[xp] -= max(1, int(self.column_width[xp] * 0.2))
        self.recalculate_layout()

    def column_width_up(self):
        xp = self.x + self.win_x
        self.column_width[xp] += max(1, int(self.column_width[xp] * 0.2))
        self.recalculate_layout()

    def sort_by_column_numeric(self):
        xp = self.x + self.win_x
        self.data = sorted((self.data),
          key=(lambda x: self.float_string_key(itemgetter(xp)(x))))

    def sort_by_column_numeric_reverse(self):
        xp = self.x + self.win_x
        self.data = sorted((self.data),
          key=(lambda x: self.float_string_key(itemgetter(xp)(x))),
          reverse=True)

    def sort_by_column(self):
        xp = self.x + self.win_x
        self.data = sorted((self.data), key=(itemgetter(xp)))

    def sort_by_column_reverse(self):
        xp = self.x + self.win_x
        self.data = sorted((self.data), key=(itemgetter(xp)), reverse=True)

    def sort_by_column_natural(self):
        xp = self.x + self.win_x
        self.data = sorted((self.data),
          key=(lambda i:         if i[xp].isdigit():
int(i[xp]) # Avoid dead code: i[xp]))

    def sort_by_column_natural_reverse(self):
        xp = self.x + self.win_x
        self.data = sorted((self.data),
          key=(lambda i:         if i[xp].isdigit():
int(i[xp]) # Avoid dead code: i[xp]),
          reverse=True)

    def float_string_key(self, value):
        """Sort by data type first and by floating point value second,
        if possible. Used for numeric sorting

        """
        try:
            value = float(value)
        except ValueError:
            pass

        return (
         repr(type(value)), value)

    def toggle_column_width(self):
        """Toggle column width mode between 'mode' and 'max' or set fixed
        column width mode if self.modifier is set.

        """
        try:
            self.column_width_mode = min(int(self.modifier), self.max_x)
            self.modifier = str()
        except ValueError:
            if self.column_width_mode == 'mode':
                self.column_width_mode = 'max'
            else:
                self.column_width_mode = 'mode'

        self._get_column_widths(self.column_width_mode)
        self.recalculate_layout()

    def set_current_column_width(self):
        xs = self.win_x + self.x
        if len(self.modifier):
            width = int(self.modifier)
            self.modifier = str()
        else:
            width = 0
            for y in range(0, len(self.data)):
                width = max(width, self._cell_len(self.data[y][xs]))

            width = min(250, width)
        self.column_width[xs] = width
        self.recalculate_layout()

    def yank_cell(self):
        yp = self.y + self.win_y
        xp = self.x + self.win_x
        s = self.data[yp][xp]
        try:
            os.environ['DISPLAY']
        except KeyError:
            return
        else:
            for cmd in (['xclip', '-selection', 'clipboard'], ['xsel', '-i']):
                try:
                    Popen(cmd, stdin=PIPE, universal_newlines=True).communicate(input=s)
                except IOError:
                    pass

    def define_keys(self):
        self.keys = {'j': self.down, 
         'k': self.up, 
         'h': self.left, 
         'l': self.right, 
         'J': self.page_down, 
         'K': self.page_up, 
         'm': self.mark, 
         "'": self.goto_mark, 
         'L': self.page_right, 
         'H': self.page_left, 
         'q': self.quit, 
         'Q': self.quit, 
         '$': self.line_end, 
         '^': self.line_home, 
         'g': self.home, 
         'G': self.goto_row, 
         '|': self.goto_col, 
         '\n': self.show_cell, 
         '/': self.search, 
         'n': self.search_results, 
         'p': self.search_results_prev, 
         't': self.toggle_header, 
         '-': self.column_gap_down, 
         '+': self.column_gap_up, 
         '<': self.column_width_all_down, 
         '>': self.column_width_all_up, 
         ',': self.column_width_down, 
         '.': self.column_width_up, 
         'a': self.sort_by_column_natural, 
         'A': self.sort_by_column_natural_reverse, 
         '#': self.sort_by_column_numeric, 
         '@': self.sort_by_column_numeric_reverse, 
         's': self.sort_by_column, 
         'S': self.sort_by_column_reverse, 
         'y': self.yank_cell, 
         'r': self.reload, 
         'c': self.toggle_column_width, 
         'C': self.set_current_column_width, 
         ']': self.skip_to_row_change, 
         '[': self.skip_to_row_change_reverse, 
         '}': self.skip_to_col_change, 
         '{': self.skip_to_col_change_reverse, 
         '?': self.help, 
         curses.KEY_F1: self.help, 
         curses.KEY_UP: self.up, 
         curses.KEY_DOWN: self.down, 
         curses.KEY_LEFT: self.left, 
         curses.KEY_RIGHT: self.right, 
         curses.KEY_HOME: self.line_home, 
         curses.KEY_END: self.line_end, 
         curses.KEY_PPAGE: self.page_up, 
         curses.KEY_NPAGE: self.page_down, 
         curses.KEY_IC: self.mark, 
         curses.KEY_DC: self.goto_mark, 
         curses.KEY_ENTER: self.show_cell, 
         KEY_CTRL('a'): self.line_home, 
         KEY_CTRL('e'): self.line_end, 
         KEY_CTRL('l'): self.scr.redrawwin, 
         KEY_CTRL('g'): self.show_info}

    def run(self):
        while True:
            self.display()
            self.handle_keys()

    def handle_keys(self):
        """Determine what method to call for each keypress.

        """
        c = self.scr.getch()
        self.prev_key = c
        if c == curses.KEY_RESIZE:
            self.resize()
            return
        if 0 < c < 256:
            c = chr(c)
        else:
            try:
                found_digit = c.isdigit()
            except AttributeError:
                found_digit = False

            if not found_digit or len(self.modifier) > 0 or c not in self.keys:
                self.handle_modifier(c)
            elif c in self.keys:
                self.keys[c]()
            else:
                self.modifier = str()

    def handle_modifier(self, mod):
        """Append digits as a key modifier, clear the modifier if not
        a digit.

        Args:
            mod: potential modifier string
        """
        self.modifier += mod
        if not self.modifier.isdigit():
            self.modifier = str()

    def resize(self):
        """Handle terminal resizing"""
        resize = self.max_x == 0 or 
        if resize is True:
            self.recalculate_layout()
            curses.resizeterm(self.max_y, self.max_x)

    def num_columns_fwd(self, x):
        """Count number of fully visible columns starting at x,
        going forward.

        """
        width = cols = 0
        while x + cols < self.num_data_columns and width + self.column_width[(x + cols)] <= self.max_x:
            width += self.column_width[(x + cols)] + self.column_gap
            cols += 1

        return max(1, cols)

    def num_columns_rev(self, x):
        """Count number of fully visible columns starting at x,
        going reverse.

        """
        width = cols = 0
        while x - cols >= 0 and width + self.column_width[(x - cols)] <= self.max_x:
            width += self.column_width[(x - cols)] + self.column_gap
            cols += 1

        return max(1, cols)

    def recalculate_layout(self):
        """Recalulate the screen layout and cursor position"""
        self.max_y, self.max_x = self.scr.getmaxyx()
        self.vis_columns = self.num_columns = self.num_columns_fwd(self.win_x)
        if self.win_x + self.num_columns < self.num_data_columns:
            xc, wc = self.column_xw(self.num_columns)
            if wc > len(self.trunc_char):
                self.vis_columns += 1
        if self.x >= self.num_columns:
            self.goto_x(self.win_x + self.x + 1)
        if self.y >= self.max_y - self.header_offset:
            self.goto_y(self.win_y + self.y + 1)

    def location_string(self, yp, xp):
        """Create (y,x) col_label string. Max 30% of screen width. (y,x) is
        padded to the max possible length it could be. Label string gets
        trunc_char appended if it's longer than the allowed width.
        """
        yx_str = ' ({},{}) '
        label_str = '{},{}'
        max_y = str(len(self.data))
        max_x = str(len(self.data[0]))
        max_yx = yx_str.format(max_y, max_x)
        y_cord = max((self.index), key=len) if self.index else '-'
        max_label = label_str.format(y_cord, max((self.header), key=len))
        if self.header_offset != self.header_offset_orig:
            label = ''
            max_width = min(int(self.max_x * 0.3), len(max_yx))
        else:
            y_cord = self.index[yp] if self.index else '-'
            label = label_str.format(y_cord, self.header[xp])
            max_width = min(int(self.max_x * 0.3), len(max_yx + max_label))
        yx = yx_str.format(yp + 1, xp + 1)
        pad = ' ' * (max_width - len(yx) - len(label))
        every = '{}{}{}'.format(yx, label, pad)
        if len(every) > max_width:
            every = every[:max_width - 1] + self.trunc_char
        return every

    def display(self):
        """Refresh the current display"""
        yp = self.y + self.win_y
        xp = self.x + self.win_x
        if isinstance(self.index_depth, int):
            if self.x < self.index_depth:
                xp = self.x
        self.scr.move(0, 0)
        self.scr.clrtoeol()
        info = self.location_string(yp, xp)
        addstr(self.scr, info, curses.A_REVERSE)
        wc = self.max_x - len(info) - 2
        s = self.cellstr(yp, xp, wc, True)
        addstr(self.scr, '  ' + s, curses.A_NORMAL)
        if self.header_offset == self.header_offset_orig:
            self.scr.move(2, 0)
            self.scr.clrtoeol()
            for x in range(0, self.vis_columns - self.index_depth):
                is_index = isinstance(self.index_depth, int) and x < self.index_depth
                align_right = self.align_right[x] if isinstance(self.align_right, list) else self.align_right
                xc, wc = self.column_xw(x, index=is_index)
                if is_index:
                    s = self.hdrstr(x, wc, align_right)
                else:
                    s = self.hdrstr(x + self.win_x, wc, align_right)
                addstr(self.scr, 2, xc, s, curses.A_BOLD)

        self.scr.hline(3, 0, ord('-'), self.max_x)
        for y in range(0, self.max_y - self.header_offset - self._search_win_open):
            yc = y + self.header_offset
            self.scr.move(yc, 0)
            self.scr.clrtoeol()
            for x in range(0, self.vis_columns - self.index_depth):
                self.background = False
                back = False
                bold = isinstance(self.index_depth, int) and x < self.index_depth
                selected = x == self.x and y == self.y
                align_right = self.align_right[x] if isinstance(self.align_right, list) else self.align_right
                trunc_left = self.trunc_left[x] if isinstance(self.trunc_left, list) else self.trunc_left
                if selected:
                    attr = curses.A_REVERSE
                elif bold:
                    attr = curses.A_BOLD
                else:
                    attr = curses.A_NORMAL
                if self.colours:
                    colour_data = self.colours.get(int(y), {})
                    fore = colour_data.get('Fore', 'reset')
                    back = colour_data.get('Back', 'reset')
                    t = self.colourdict.get((fore, back), False)
                    if t is not False:
                        attr = curses.color_pair(t)
                else:
                    xc, wc = self.column_xw(x, index=bold)
                    if bold:
                        s = self.cellstr((y + self.win_y),
                          x, wc, align_right, trunc_left=trunc_left)
                    else:
                        s = self.cellstr((y + self.win_y),
                          (x + self.win_x),
                          wc,
                          align_right,
                          trunc_left=trunc_left)
                if back != 'default':
                    self.background = back
                if y > 0 and bold and s.original == self.cellstr(y + self.win_y - 1, x + self.win_x, wc, align_right).original:
                    if not selected:
                        s = ''
                if yc == self.max_y - 1:
                    if x == self.vis_columns - 1:
                        insstr(self.scr, yc, xc, s, attr)
                    else:
                        addstr(self.scr, yc, xc, s, attr)
                    if bold and self.index_depth - 1 == x:
                        try:
                            self.scr.vline(2, xc + wc + 1, ord('|'), self.max_y - 1)
                            self.scr.vline(2, xc + wc + 2, ord(' '), self.max_y - 1)
                        except:
                            pass

        self.scr.refresh()

    def strpad(self, s, width, align_right, trunc_left=False):
        """pads cell content, left or right, depending on self.align_right"""
        if width < 1:
            return str()
        else:
            if '\n' in str(s):
                s = str(s).replace('\n', '\\n')
            extra_wide = len([c for c in s if unicodedata.east_asian_width(c) == 'W'])
            if align_right:
                s = str(s).rjust(width + extra_wide, ' ')
            else:
                s = str(s).ljust(width + extra_wide, ' ')
        return MaybeTruncatedString(s,
          width,
          (self.trunc_char),
          trunc_left=trunc_left,
          background=(self.background),
          colgap=(self.column_gap))

    def hdrstr(self, x, width, align_right):
        """
        Format the content of the requested header for display
        """
        if len(self.header) <= x:
            s = ''
        else:
            s = self.header[x]
        return self.strpad(s, width, align_right)

    def cellstr(self, y, x, width, align_right, trunc_left=False):
        """
        Format the content of the requested cell for display
        """
        if len(self.data) <= y or len(self.data[y]) <= x:
            s = ''
        else:
            s = self.data[y][x]
        return self.strpad(s, width, align_right, trunc_left=trunc_left)

    def _get_column_widths(self, width):
        """Compute column width array

        Args: width - 'max', 'mode', or an integer value
        Returns: [len of col 1, len of col 2, ....]

        """
        if width == 'max':
            self.column_width = self._get_column_widths_max(self.data)
        elif width == 'mode':
            self.column_width = self._get_column_widths_mode(self.data)
        else:
            try:
                width = int(width)
            except (TypeError, ValueError):
                width = 25

            self.column_width = [width for i in range(0, self.num_data_columns)]

    @staticmethod
    def __cell_len_dw(s):
        """Return the number of character cells a string will take
        (double-width aware). Defined as self._cell_len in __init__

        """
        len = 0
        for c in s:
            w = 2 if unicodedata.east_asian_width(c) == 'W' else 1
            len += w

        return len

    def _mode_len(self, x):
        """Compute arithmetic mode (most common value) of the length of each item
        in an iterator.

            Args: x - iterator (list, tuple, etc)
            Returns: mode - int.

        """
        lens = [self._cell_len(i) for i in x]
        m = Counter(lens).most_common()
        try:
            mode = m[0][0] or 
        except IndexError:
            mode = 0

        max_len = max(lens) or 
        diff = abs(mode - max_len)
        if diff > self.column_gap * 2:
            if diff / max_len > 0.1:
                return max(max(1, self.column_gap), mode)
        return max(max(1, self.column_gap), max_len)

    def _get_column_widths_mode(self, d):
        """Given a list of lists, return a list of the variable column width
        for each column using the arithmetic mode.

        Args: d - list of lists with x columns
        Returns: list of ints [len_1, len_2...len_x]

        """
        d = zip(*d)
        return [self._mode_len(i) for i in d]

    def _get_column_widths_max(self, d):
        """Given a list of lists, return a list of the variable column width
        for each column using the max length.

        Args: d - list of lists with x columns
        Returns: list of ints [len_1, len_2...len_x]

        """
        d = zip(*d)
        return [max(1, min(250, max(set((self._cell_len(j) for j in i))))) for i in d]

    def _skip_to_value_change(self, x_inc, y_inc):
        m = self.consume_modifier()
        for _ in range(m):
            x = self.win_x + self.x
            y = self.win_y + self.y
            v = self.data[y][x]
            y += y_inc
            x += x_inc
            while y >= 0 and y < len(self.data) and x >= 0 and x < self.num_data_columns and self.data[y][x] == v:
                y += y_inc
                x += x_inc

            self.goto_yx(y + 1, x + 1)

    def skip_to_row_change(self):
        self._skip_to_value_change(0, 1)

    def skip_to_row_change_reverse(self):
        self._skip_to_value_change(0, -1)

    def skip_to_col_change(self):
        self._skip_to_value_change(1, 0)

    def skip_to_col_change_reverse(self):
        self._skip_to_value_change(-1, 0)


class TextBox(object):
    """TextBox"""

    def __init__(self, scr, data='', title='', cursor_line_pos=0, match_line=-1):
        self._running = False
        self.scr = scr
        self.data = data
        self.title = title
        self.match_line = match_line + 1 if match_line is not None else -1
        self.cursor_line_pos = cursor_line_pos
        self.tdata = []
        self.hid_rows = 0
        self.hid_cols = 0
        self.setup_handlers()

    def __call__(self):
        self.run()

    def setup_handlers(self):
        self.handlers = {'\n': self.close, 
         curses.KEY_ENTER: self.close, 
         'q': self.close, 
         curses.KEY_RESIZE: self.close, 
         curses.KEY_DOWN: self.scroll_down, 
         curses.KEY_LEFT: self.scroll_left, 
         curses.KEY_RIGHT: self.scroll_right, 
         'j': self.scroll_down, 
         curses.KEY_UP: self.scroll_up, 
         'k': self.scroll_up}

    def _calculate_layout(self):
        """Setup popup window and format data. """
        self.scr.touchwin()
        self.term_rows, self.term_cols = self.scr.getmaxyx()
        self.box_height = self.term_rows - int(self.term_rows / 2)
        self.win = curses.newwin(int(self.term_rows / 2), self.term_cols, self.box_height, 0)
        try:
            curses.curs_set(False)
        except _curses.error:
            pass

        s = self.data.splitlines()
        self.longest_row = max((len(i) for i in s))
        s = [wrap(i, (self.term_cols - 3), subsequent_indent=' ') or  for i in s]
        self.tdata = [i for j in s for i in j]
        self.nlines = min(len(self.tdata), self.box_height - 3)
        self.scr.refresh()

    def run(self):
        self._running = True
        self._calculate_layout()
        while self._running:
            self.display()
            c = self.scr.getch()
            self.handle_key(c)

    def handle_key(self, key):
        if 0 < key < 256:
            key = chr(key)
        try:
            self.handlers[key]()
        except KeyError:
            pass

    def close(self):
        self._running = False

    def scroll_down(self):
        if self.box_height - 3 + self.hid_rows <= len(self.tdata):
            self.hid_rows += 1
            self.match_line -= 1
        self.hid_rows = min(len(self.tdata), self.hid_rows)

    def scroll_up(self):
        orig = self.hid_rows
        self.hid_rows -= 1
        self.hid_rows = max(0, self.hid_rows)
        if orig != self.hid_rows:
            self.match_line += 1

    def scroll_left(self):
        self.hid_cols -= 1
        self.hid_cols = max(0, self.hid_cols)

    def scroll_right(self):
        self.hid_cols += 1
        self.hid_cols = self.longest_row

    def move_to_starting_pos(self):
        self.hid_rows += self.cursor_line_pos
        for i in range(self.cursor_line_pos):
            self.scroll_down()

    def display(self):
        self.win.erase()
        addstr(self.win, 1, 1, self.title[:self.term_cols - 3], curses.A_STANDOUT)
        num_hidden = self.hid_rows
        visible_rows = self.tdata[num_hidden:self.hid_rows + self.nlines]
        if -1 < self.match_line < len(visible_rows):
            start = visible_rows[:self.match_line]
            match = visible_rows[self.match_line]
            end = visible_rows[self.match_line + 1:]
            addstr(self.win, 2, 1, '\n '.join(start))
            addstr(self.win, 2 + len(start), 1, match, curses.A_REVERSE)
            addstr(self.win, 2 + len(start) + 1, 1, '\n '.join(end))
        else:
            addstr(self.win, 2, 1, '\n '.join(visible_rows))
        self.win.box()
        self.win.refresh()


def csv_sniff(data, enc):
    """Given a list, sniff the dialect of the data and return it.

    Args:
        data - list like ["col1,col2,col3"]
        enc - python encoding value ('utf_8','latin-1','cp870', etc)
    Returns:
        csv.dialect.delimiter

    """
    data = data.decode(enc)
    dialect = csv.Sniffer().sniff(data)
    return dialect.delimiter


def process_data(data, enc=None, delim=None, **kwargs):
    """Given a data input, determine the input type and process data accordingly.

    Returns a dictionary containing two entries: 'header', which corresponds to
    the header row, and 'data', which corresponds to the data rows.
    """
    if isinstance(data.index, pd.MultiIndex):
        index = []
        for item in list(data.index):
            if isinstance(item, tuple):
                item = [str(i) for i in item]
                item = ' '.join(item)
            index.append(item)

    else:
        index = [str(i) for i in list(data.index)]
    size = len(data.index.names)
    try:
        data = data.reset_index()
    except ValueError:
        data.index.names = ['__%s__' % str(x) for x in data.index.names]
        data = data.reset_index()
        fixed = [n.strip('_') for n in data.columns[:size]] + list(data.columns[size:])
        data.columns = fixed

    header = [str(i) for i in data.columns]
    try:
        unicode_convert = np.vectorize(str)
        data = unicode_convert(data.values)
    except:
        np_codec = detect_encoding(data.select_dtypes(include=['object']).values.ravel().tolist())
        unicode_convert = np.vectorize(lambda x: np_decode(x, np_codec))
        data = unicode_convert(data.values)

    data[np.where(data == 'nan')] = ''
    return {'data':data.tolist(), 
     'header':header,  'index':index}


def np_decode(inp_str, codec):
    """String decoding function for numpy arrays.
    """
    try:
        return str(inp_str)
    except:
        return inp_str.decode(codec)


def py2_list_to_unicode(data):
    """Convert strings/int to unicode for python 2

    """
    enc = detect_encoding()
    csv_data = []
    for row in data:
        r = []
        for x in row:
            try:
                r.append(str(x, enc))
            except TypeError:
                r.append(str(x))

        csv_data.append(r)

    return csv_data


def pad_data(d):
    """Pad data rows to the length of the longest row.

        Args: d - list of lists

    """
    max_len = set((len(i) for i in d))
    if len(max_len) == 1:
        return d
    max_len = max(max_len)
    return [i + [''] * (max_len - len(i)) for i in d]


def readme():
    path = os.path.dirname(os.path.realpath(__file__))
    fn = os.path.join(path, 'README.rst')
    with open(fn, 'rb') as (f):
        h = f.readlines()
        return [i.decode('utf-8') for i in h]


def detect_encoding(data=None):
    """Return the default system encoding. If data is passed, try
    to decode the data with the default system encoding or from a short
    list of encoding types to test.

    Args:
        data - list of lists
    Returns:
        enc - system encoding

    """
    enc_list = [
     'utf-8', 'latin-1', 'iso8859-1', 'iso8859-2', 'utf-16', 'cp720']
    code = locale.getpreferredencoding(False)
    if data is None:
        return code
    if code.lower() not in enc_list:
        enc_list.insert(0, code.lower())
    for c in enc_list:
        try:
            for line in data:
                line.decode(c)

        except (UnicodeDecodeError, UnicodeError, AttributeError):
            continue

        return c

    print('Encoding not detected. Please pass encoding value manually')


def main(stdscr, *args, **kwargs):
    try:
        curses.use_default_colors()
    except (AttributeError, _curses.error):
        pass

    try:
        curses.curs_set(False)
    except (AttributeError, _curses.error):
        pass

    Viewer(stdscr, *args, **kwargs).run()


def get_index_depth(data, freeze):
    if freeze:
        return freeze
    try:
        import pandas as pd
        if isinstance(data, (pd.DataFrame, pd.Series)):
            if isinstance(data.index, pd.MultiIndex):
                return len(data.index.levels)
            return 1
    except ImportError:
        return 1
    else:
        return False


def view(data, enc=None, start_pos=(0, 0), column_width=20, column_gap=2, colours=False, trunc_char='…', column_widths=None, search_str=None, persist=False, trunc_left=False, double_width=False, delimiter=None, orient='columns', align_right=False, df=False, **kwargs):
    """The curses.wrapper passes stdscr as the first argument to main +
    passes to main any other arguments passed to wrapper. Initializes
    and then puts screen back in a normal state after closing or
    exceptions.

    Args:
        data: dataframe-like object
        enc: encoding for file/data
        start_pos: initial file position. Either a single integer for just y
            (row) position, or tuple/list (y,x)
        column_width: 'max' (max width for the column),
                      'mode' (uses arithmetic mode to compute width), or
                      int x (x characters wide). Default is 'mode'
        column_gap: gap between columns
        column_widths: list of widths for each column [len1, len2, lenxxx...]
        trunc_char: character to indicate continuation of too-long columns
        search_str: string to search for
        double_width: boolean indicating whether double-width characters
                      should be handled (defaults to False for large files)
        delimiter: CSV delimiter. Typically needed only if the automatic
                   delimiter detection doesn't work. None => automatic

    """
    lc_all = None
    stdscr = curses.initscr()
    try:
        buf = None
        while True:
            try:
                if isinstance(data, str):
                    with open(data, 'rb') as (fd):
                        new_data = fd.readlines()
                elif isinstance(data, (io.IOBase, io.FileIO)):
                    new_data = data.readlines()
                else:
                    new_data = data
                index_depth = get_index_depth(new_data, kwargs.pop('freeze', False))
                buf = process_data(new_data, enc, delimiter, orient=orient)
                (curses.wrapper)(
 main,
 buf, start_pos=start_pos, 
                 column_width=column_width, 
                 column_gap=column_gap, 
                 trunc_char=trunc_char, 
                 column_widths=column_widths, 
                 search_str=search_str, 
                 double_width=double_width, 
                 align_right=align_right, 
                 index_depth=index_depth, 
                 colours=colours, 
                 trunc_left=trunc_left, 
                 df=df, **kwargs)
            except (QuitException, KeyboardInterrupt):
                return 0
            except ReloadException as e:
                try:
                    start_pos = e.start_pos
                    column_width = e.column_width_mode
                    column_gap = e.column_gap
                    column_widths = e.column_widths
                    search_str = e.search_str
                    continue
                finally:
                    e = None
                    del e

    finally:
        if lc_all is not None:
            locale.setlocale(locale.LC_ALL, lc_all)
        if persist:
            pad_content = []
            try:
                height, width = stdscr.getmaxyx()
            except:
                stdscr = curses.initscr()
                height, width = stdscr.getmaxyx()

            for x in range(height):
                cont = stdscr.instr(x, 0).decode('utf-8')
                if x < 3:
                    cont = cont.replace('-', '─')
                pad_content.append(cont)

            out = '\n'.join(pad_content)
            if colours:
                out = colorama_data(pad_content, colours)
            print(out.replace('|', '│'))