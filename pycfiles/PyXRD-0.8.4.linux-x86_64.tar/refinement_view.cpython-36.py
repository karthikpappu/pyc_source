# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/views/refinement_view.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 3541 bytes
from pkg_resources import resource_filename
from math import isnan
from mvc.adapters.gtk_support.widgets.threaded_task_box import ThreadedTaskBox
from pyxrd.generic.views import DialogView
from pyxrd.generic.utils import not_none

class RefinementView(DialogView):
    title = 'Refine Phase Parameters'
    subview_builder = resource_filename(__name__, 'glade/refinement.glade')
    subview_toplevel = 'refine_params'
    modal = True
    refine_status_builder = resource_filename(__name__, 'glade/refine_status.glade')
    refine_status_toplevel = 'tbl_refine_info'
    refine_status_container = 'refine_status_box'
    refine_spin_container = 'refine_spin_box'
    refine_spin_box = None
    refine_method_builder = resource_filename(__name__, 'glade/refine_method.glade')
    refine_method_toplevel = 'tbl_refine_method'
    refine_method_container = 'refine_method_box'

    def __init__(self, *args, **kwargs):
        (super(RefinementView, self).__init__)(*args, **kwargs)
        self._builder.add_from_file(self.refine_status_builder)
        self._add_child_view(self[self.refine_status_toplevel], self[self.refine_status_container])
        self._builder.add_from_file(self.refine_method_builder)
        self._add_child_view(self[self.refine_method_toplevel], self[self.refine_method_container])
        self.refine_spin_box = ThreadedTaskBox()
        self._add_child_view(self.refine_spin_box, self[self.refine_spin_container])
        self.hide_refinement_info()

    def connect_cancel_request(self, callback):
        return self.refine_spin_box.connect('cancelrequested', callback)

    def show_refinement_info(self):
        self['hbox_actions'].set_sensitive(False)
        self['btn_auto_restrict'].set_sensitive(False)
        self[self.refine_method_toplevel].set_sensitive(False)
        self['refinables'].set_visible(False)
        self['refinables'].set_no_show_all(True)
        self[self.refine_status_toplevel].show_all()

    def hide_refinement_info(self):
        self[self.refine_status_toplevel].hide()
        self['hbox_actions'].set_sensitive(True)
        self['btn_auto_restrict'].set_sensitive(True)
        self[self.refine_method_toplevel].set_sensitive(True)
        self['refinables'].set_visible(True)
        self['refinables'].set_no_show_all(False)

    def update_refinement_info(self, current_rp=None, message=None, server_status=None):
        if not isnan(current_rp):
            self['current_residual'].set_text('%.2f' % current_rp)
        self['message'].set_text(not_none(message, ''))
        self.update_server_status(server_status)

    def update_server_status(self, server_status):
        color, title, descr = server_status
        self['lbl_server_status'].set_markup('<span foreground="%s">%s</span>' % (color, title))
        self['lbl_server_status'].set_property('tooltip-text', descr)
        self['lbl_server_status'].set_property('tooltip-text', descr)
        self['lbl_server_status'].set_tooltip_text(descr)

    def update_refinement_status(self, status):
        self.refine_spin_box.set_status(status)

    def start_spinner(self):
        self.refine_spin_box.start()

    def stop_spinner(self):
        self.refine_spin_box.stop()