# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_pdf/kotti_pdf/views/edit.py
# Compiled at: 2017-05-11 21:30:45
"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""
from pyramid.view import view_config
from kotti.views.edit.content import FileEditForm, FileAddForm
from kotti_pdf import _
from kotti_pdf.resources import PDF

@view_config(name=PDF.type_info.add_view, permission=PDF.type_info.add_permission, renderer='kotti:templates/edit/node.pt')
class PDFAddForm(FileAddForm):
    item_type = _('PDF')
    item_class = PDF


@view_config(name='edit', context=PDF, permission='edit', renderer='kotti:templates/edit/node.pt')
class PDFEditForm(FileEditForm):
    pass