# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/ext/columnsizer.py
# Compiled at: 2008-02-07 14:10:42
"""columnsizer -- a mixin to handle column resizing for list controls

This mixin provides the capabibility to resize columns in a
report-mode list control.  Integer flags are used for each column to
indicate whether the column should be a fixed size or a width
proportional to te length of the largest item in the column.  It also
tries (with only some success) to avoid using a horizontal scrollbar
if at all possible.
"""
import wx, logging

class ColumnSizerMixin(object):
    """Enhancement to ListCtrl to handle column resizing.

    Resizes columns to a fixed size or based on the size of the
    contents, but constrains the whole width to the visible area of
    the list.  Theoretically there won't be any horizontal scrollbars,
    but this doesnt' yet work on GTK, at least.
    """

    def __init__(self, *args, **kw):
        self._resize_flags = None
        self._resize_dirty = True
        self._last_size = None
        self.Bind(wx.EVT_SIZE, self.OnSize)
        return

    def OnSize(self, evt):
        logging.debug('OnSize recieved event: %s' % evt.GetSize())
        if self._last_size is None or self._last_size != evt.GetSize():
            self._resize_dirty = True
            self._last_size = evt.GetSize()
            wx.CallAfter(self.resizeColumnsIfDirty)
        evt.Skip()
        return

    def resizeColumnsIfDirty(self):
        if self._resize_dirty:
            self._resizeColumns()

    def resizeColumns(self, flags=[]):
        try:
            self._resize_dirty = True
            self._resizeColumns(flags)
        except wx._core.PyDeadObjectError:
            logging.debug('Caught dead object error for %s' % self)

    def _resizeColumns(self, flags=[]):
        """Resize each column according to the flag.

        For each column, the respective flag indicates the following:

        0: smallest width that fits the entire string
        1: smallest width, and keep this column fixed width if possible
        >1: maximum size
        <0: absolute value is the minimum size
        """
        if not self._resize_dirty:
            return
        self.Freeze()
        if self._resize_flags is None or len(flags) > 0:
            copy = list(flags)
            if len(copy) < self.GetColumnCount():
                copy.extend([0] * (self.GetColumnCount() - len(copy)))
            self._resize_flags = tuple(copy)
            logging.debug('Resetting flags to %s' % str(self._resize_flags))
        flags = self._resize_flags
        fixed_width = 0
        total_width = 0
        num_fixed = 0
        for col in range(self.GetColumnCount()):
            self.SetColumnWidth(col, wx.LIST_AUTOSIZE)
            flag = flags[col]
            if flag > 1:
                after = self.GetColumnWidth(col)
                if after > flag:
                    self.SetColumnWidth(col, flag)
            elif flag < 0:
                after = self.GetColumnWidth(col)
                if after < -flag:
                    self.SetColumnWidth(col, -flag)
            after = self.GetColumnWidth(col)
            total_width += after
            if flag == 1:
                num_fixed += 1
                fixed_width += after

        (w, h) = self.GetClientSizeTuple()
        logging.debug('Client width = %d, fixed_width = %d' % (w, fixed_width))
        w -= fixed_width
        for col in range(self.GetColumnCount()):
            before = self.GetColumnWidth(col)
            logging.debug('Col %d: flag=%d before=%d' % (col, flags[col], before))
            if flags[col] != 1:
                self.SetColumnWidth(col, before * w / total_width)

        self.Thaw()
        self._resize_dirty = False
        return