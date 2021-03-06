# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/webpage/table.py
# Compiled at: 2011-11-24 14:18:10
import os, types, sys, copy, pypoly
from pypoly.content.webpage import Content, ContentType, ContentProperties

class Header(list, Content):
    """
    Handle all header data for the table.

    :since: 0.1
    """

    def append(self, cells):
        """
        Append the cells as a new row to the table header

        :since: 0.1

        :param cells: list of cells or strings to append
        :type cells: List
        """
        tmp_cells = []
        for cell in cells:
            if Cell in type(cell).__bases__:
                tmp_cells.append(cell)
            else:
                tmp_cell = LabelCell()
                tmp_cell.value = cell
                tmp_cells.append(tmp_cell)

        list.append(self, tmp_cells)


class Footer(list, Content):
    """
    Handle all footer data for the table.
    """

    def append(self, cells):
        """
        Append the cells as a new row to the table footer

        :since: 0.1
        :param cells: list of cells or strings to append
        :type cells: List
        """
        tmp_cells = []
        for cell in cells:
            if Cell in type(cell).__bases__:
                tmp_cells.append(cell)
            else:
                tmp_cell = LabelCell()
                tmp_cell.value = cell
                tmp_cells.append(tmp_cell)

        list.append(self, tmp_cells)


class Table(list, Content):
    """
    Create a table.

    Example::

        page = Webpage()

        # create table
        table = Table()
        table.cols.append(TextCell())
        table.cols.append(TextCell())

        # add two rows to the header
        table.header.append(['Test Label11', 'Test Label12'])
        table.header.append(['Test Label21', TextCell(value = 'Test Label22')])

        # add two rows to the footer
        table.footer.append(['Test Label11', 'Test Label12'])
        table.footer.append(['Test Label21', TextCell(value = 'Test Label22')])

        # add two data rows
        table.append(['Cell11', 'Cell12'])
        table.append([LabelCell(value = 'Cell21'), 'Cell22'])

        page.append(table)

    :since: 0.1

    :todo: add checks for header and footer
    """
    type = ContentType('table')

    def __init__(self, *args, **options):
        self.title = ''
        self._caption = None
        Content.__init__(self, *args, **options)
        self.cols = []
        self.header = Header()
        self.footer = Footer()
        self.id = 'table_' + self._name
        self.template = pypoly.template.load_web('webpage', 'table', 'table')
        return

    def get_caption(self):
        if self._caption == None or self._caption == '':
            return self.title
        else:
            return self._caption
            return

    def set_caption(self, value):
        self._caption = value

    caption = property(get_caption, set_caption)

    def append(self, cells):
        tmp_cells = []
        index = 0
        for cell in cells:
            if Cell in type(cell).__bases__:
                tmp_cell = cell
            else:
                tmp_cell = copy.copy(self.cols[index])
                tmp_cell.value = cell
            if tmp_cell.colspan != None and tmp_cell.colspan > 1:
                index = index + tmp_cell.colspan
            else:
                index = index + 1
            tmp_cells.append(tmp_cell)

        list.append(self, tmp_cells)
        return

    def get_childs(self, level=1):
        """
        Returns all child items.

        :param level: Get child elements recursively
        :type level: Integer
        :return: List of child elements
        :rtype: List
        """
        if level == 0:
            return []
        else:
            if level != None:
                level = level - 1
            items = []
            for row in self:
                for item in row:
                    func = getattr(item, 'get_childs', None)
                    if func == None or callable(func) == False:
                        continue
                    items.append(item)
                    items = items + item.get_childs(level=level)

            return items

    def generate(self, **options):
        return self.template.generate(table=self)


class Cell(Content):
    """
    This is the parent Column class

    :since: 0.1
    """
    colspan = None
    rowspan = None
    type = ContentType('table.cell')

    def __init__(self, *args, **options):
        """
        Set all defaults
        """
        if 'value' in options:
            self._value = options['value']
        else:
            self._value = None
        self.colspan = None
        self.rowspan = None
        Content.__init__(self, *args, **options)
        return

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value

    value = property(_get_value, _set_value)

    def get_childs(self, level=1):
        """
        Returns all child items.

        :param level: Get child elements recursively
        :type level: Integer
        :return: List of child elements
        :rtype: List
        """
        if level == 0:
            return []
        else:
            if level != None:
                level = level - 1
            func = getattr(self._value, 'get_childs', None)
            if func == None or callable(func) == False:
                return []
            return [self._value] + self._value.get_childs(level=level)

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'table', 'cell')
        return tpl.generate(cell=self)


class ContentCell(Cell):
    """
    Use this column if you want to display a Label

    :since: 0.1
    """
    type = ContentType('table.cell.content')

    def __init__(self, *args, **options):
        Cell.__init__(self, *args, **options)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value

    value = property(_get_value, _set_value)


class LabelCell(Cell):
    """
    Use this column if you want to display a Label

    :since: 0.1
    """
    type = ContentType('table.cell.label')

    def __init__(self, *args, **options):
        Cell.__init__(self, *args, **options)


class LinkCell(Cell):
    """
    Use this cell if you want to display a Link

    :since: 0.1
    """
    url = None
    type = ContentType('table.cell.link')

    def __init__(self, *args, **options):
        self.url = None
        Cell.__init__(self, *args, **options)
        return


class TextCell(Cell):
    """
    Use this column if you want to display text

    :since: 0.1
    """
    type = ContentType('table.cell.text')

    def __init__(self, *args, **options):
        Cell.__init__(self, *args, **options)


class DateCell(Cell):
    """
    Use this column if you want to display a date

    :since: 0.1
    """
    type = ContentType('table.cell.date')

    def __init__(self, *args, **options):
        Cell.__init__(self, *args, **options)


class MoneyCell(Cell):
    """
    Use this Column for money values

    :since: 0.1
    """
    currency = ''
    highlight_both = False
    highlight_neg = False
    highlight_pos = False
    type = ContentType('table.cell.money')

    def __init__(self, *args, **options):
        """
        Set all defaults
        """
        self.currency = ''
        self.highlight_both = False
        self.highlight_neg = False
        self.highlight_pos = False
        Cell.__init__(self, *args, **options)