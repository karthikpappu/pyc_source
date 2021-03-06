# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\plugins\export.py
# Compiled at: 2019-01-06 19:47:42
# Size of source mod 2**32: 9996 bytes
import datetime, io, sys
from django.db.models import BooleanField, NullBooleanField
from django.http import HttpResponse
from django.template import loader
from django.utils import six
from django.utils.encoding import force_text, smart_text, escape_uri_path
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.xmlutils import SimplerXMLGenerator
from future.utils import iteritems
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.util import json
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.views.list import ALL_VAR
try:
    import xlwt
    has_xlwt = True
except:
    has_xlwt = False

try:
    import xlsxwriter
    has_xlsxwriter = True
except:
    has_xlsxwriter = False

class ExportMenuPlugin(BaseAdminPlugin):
    list_export = ('xlsx', 'xls', 'csv', 'xml', 'json')
    export_names = {'xlsx':'Excel 2007',  'xls':'Excel',  'csv':'CSV',  'xml':'XML', 
     'json':'JSON'}

    def init_request(self, *args, **kwargs):
        self.list_export = [f for f in self.list_export if f != 'xlsx' or has_xlsxwriter if f != 'xls' or has_xlwt]

    def block_top_toolbar(self, context, nodes):
        if self.list_export:
            context.update({'show_export_all':self.admin_view.paginator.count > self.admin_view.list_per_page and ALL_VAR not in self.admin_view.request.GET, 
             'form_params':self.admin_view.get_form_params({'_do_': 'export'}, ('export_type', )), 
             'export_types':[{'type':et,  'name':self.export_names[et]} for et in self.list_export]})
            nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.exports.html', context=(get_context_dict(context))))


class ExportPlugin(BaseAdminPlugin):
    export_mimes = {'xlsx':'application/vnd.ms-excel', 
     'xls':'application/vnd.ms-excel', 
     'csv':'text/csv',  'xml':'application/xhtml+xml', 
     'json':'application/json'}

    def init_request(self, *args, **kwargs):
        return self.request.GET.get('_do_') == 'export'

    def _format_value(self, o):
        if o.field is None and getattr(o.attr, 'boolean', False) or o.field and isinstance(o.field, (BooleanField, NullBooleanField)):
            value = o.value
        else:
            if str(o.text).startswith("<span class='text-muted'>"):
                value = escape(str(o.text)[25:-7])
            else:
                value = escape(str(o.text))
        return value

    def _get_objects(self, context):
        headers = [c for c in context['result_headers'].cells if c.export]
        rows = context['results']
        return [dict([(force_text(headers[i].text), self._format_value(o)) for i, o in enumerate(filter(lambda c: getattr(c, 'export', False), r.cells))]) for r in rows]

    def _get_datas(self, context):
        rows = context['results']
        new_rows = [[self._format_value(o) for o in filter(lambda c: getattr(c, 'export', False), r.cells)] for r in rows]
        new_rows.insert(0, [force_text(c.text) for c in context['result_headers'].cells if c.export])
        return new_rows

    def get_xlsx_export(self, context):
        datas = self._get_datas(context)
        output = io.BytesIO()
        export_header = self.request.GET.get('export_xlsx_header', 'off') == 'on'
        model_name = self.opts.verbose_name
        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet('%s %s' % (_('Sheet'), force_text(model_name)))
        styles = {'datetime':book.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'}),  'date':book.add_format({'num_format': 'yyyy-mm-dd'}), 
         'time':book.add_format({'num_format': 'hh:mm:ss'}), 
         'header':book.add_format({'font':'name Times New Roman', 
          'color':'red',  'bold':'on',  'num_format':'#,##0.00'}), 
         'default':book.add_format()}
        if not export_header:
            datas = datas[1:]
        for rowx, row in enumerate(datas):
            for colx, value in enumerate(row):
                if export_header:
                    if rowx == 0:
                        cell_style = styles['header']
                else:
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    else:
                        if isinstance(value, datetime.date):
                            cell_style = styles['date']
                        else:
                            if isinstance(value, datetime.time):
                                cell_style = styles['time']
                            else:
                                cell_style = styles['default']
                sheet.write(rowx, colx, value, cell_style)

        book.close()
        output.seek(0)
        return output.getvalue()

    def get_xls_export(self, context):
        datas = self._get_datas(context)
        output = io.BytesIO()
        export_header = self.request.GET.get('export_xls_header', 'off') == 'on'
        model_name = self.opts.verbose_name
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('%s %s' % (_('Sheet'), force_text(model_name)))
        styles = {'datetime':xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),  'date':xlwt.easyxf(num_format_str='yyyy-mm-dd'), 
         'time':xlwt.easyxf(num_format_str='hh:mm:ss'), 
         'header':xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00'), 
         'default':xlwt.Style.default_style}
        if not export_header:
            datas = datas[1:]
        for rowx, row in enumerate(datas):
            for colx, value in enumerate(row):
                if export_header:
                    if rowx == 0:
                        cell_style = styles['header']
                else:
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    else:
                        if isinstance(value, datetime.date):
                            cell_style = styles['date']
                        else:
                            if isinstance(value, datetime.time):
                                cell_style = styles['time']
                            else:
                                cell_style = styles['default']
                sheet.write(rowx, colx, value, style=cell_style)

        book.save(output)
        output.seek(0)
        return output.getvalue()

    def _format_csv_text(self, t):
        if isinstance(t, bool):
            if t:
                return _('Yes')
            return _('No')
        else:
            t = t.replace('"', '""').replace(',', '\\,')
            cls_str = str if six.PY3 else basestring
            if isinstance(t, cls_str):
                t = '"%s"' % t
            return t

    def get_csv_export(self, context):
        datas = self._get_datas(context)
        stream = []
        if self.request.GET.get('export_csv_header', 'off') != 'on':
            datas = datas[1:]
        for row in datas:
            stream.append(','.join(map(self._format_csv_text, row)))

        return '\r\n'.join(stream)

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement('row', {})
                self._to_xml(xml, item)
                xml.endElement('row')

        else:
            if isinstance(data, dict):
                for key, value in iteritems(data):
                    key = key.replace(' ', '_')
                    xml.startElement(key, {})
                    self._to_xml(xml, value)
                    xml.endElement(key)

            else:
                xml.characters(smart_text(data))

    def get_xml_export(self, context):
        results = self._get_objects(context)
        stream = io.StringIO()
        xml = SimplerXMLGenerator(stream, 'utf-8')
        xml.startDocument()
        xml.startElement('objects', {})
        self._to_xml(xml, results)
        xml.endElement('objects')
        xml.endDocument()
        return stream.getvalue().split('\n')[1]

    def get_json_export(self, context):
        results = self._get_objects(context)
        return json.dumps({'objects': results}, ensure_ascii=False, indent=(self.request.GET.get('export_json_format', 'off') == 'on' and 4 or None))

    def get_response(self, response, context, *args, **kwargs):
        file_type = self.request.GET.get('export_type', 'csv')
        response = HttpResponse(content_type=('%s; charset=UTF-8' % self.export_mimes[file_type]))
        file_name = self.opts.verbose_name.replace(' ', '_')
        response['Content-Disposition'] = "attachment; filename*=utf-8''{0}.{1}".format(escape_uri_path(file_name), file_type)
        response.write(getattr(self, 'get_%s_export' % file_type)(context))
        return response

    def get_result_list(self, __):
        if self.request.GET.get('all', 'off') == 'on':
            self.admin_view.list_per_page = sys.maxsize
        return __()

    def result_header(self, item, field_name, row):
        item.export = not item.attr or field_name == '__str__' or getattr(item.attr, 'allow_export', True)
        return item

    def result_item(self, item, obj, field_name, row):
        item.export = item.field or field_name == '__str__' or getattr(item.attr, 'allow_export', True)
        return item


site.register_plugin(ExportMenuPlugin, ListAdminView)
site.register_plugin(ExportPlugin, ListAdminView)