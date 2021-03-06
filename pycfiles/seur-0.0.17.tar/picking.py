# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/resteve/virtualenv/nan38mifarma/python-seur/seur/picking.py
# Compiled at: 2017-01-24 17:20:15
from seur.api import API
from xml.dom.minidom import parseString
import os, datetime, genshi, genshi.template
loader = genshi.template.TemplateLoader(os.path.join(os.path.dirname(__file__), 'template'), auto_reload=True)

class Picking(API):
    """
    Picking API
    """
    __slots__ = ()

    def create(self, data):
        """
        Create a picking using the given data

        :param data: Dictionary of values
        :return: reference (str), label (pdf), error (str)
        """
        reference = None
        label = None
        error = None
        if self.context.get('pdf'):
            tmpl = loader.load('picking_send_pdf.xml')
        else:
            tmpl = loader.load('picking_send.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'vat': self.vat, 
           'franchise': self.franchise, 
           'seurid': self.seurid, 
           'ci': self.ci, 
           'ccc': self.ccc, 
           'servicio': data.get('servicio', '1'), 
           'product': data.get('product', '2'), 
           'total_bultos': data.get('total_bultos', 1), 
           'total_kilos': data.get('total_kilos', '1'), 
           'peso_bulto': data.get('peso_bulto', '1'), 
           'observaciones': data.get('observaciones', ''), 
           'referencia_expedicion': data.get('referencia_expedicion', ''), 
           'ref_bulto': data.get('ref_bulto', ''), 
           'clave_portes': data.get('clave_portes', 'F'), 
           'clave_reembolso': data.get('clave_reembolso', 'F'), 
           'valor_reembolso': data.get('valor_reembolso', ''), 
           'cliente_nombre': data.get('cliente_nombre', ''), 
           'cliente_direccion': data.get('cliente_direccion', ''), 
           'cliente_tipovia': data.get('cliente_tipovia', 'CL'), 
           'cliente_tnumvia': data.get('cliente_tnumvia', 'N'), 
           'cliente_numvia': data.get('cliente_numvia', '.'), 
           'cliente_escalera': data.get('cliente_escalera', '.'), 
           'cliente_piso': data.get('cliente_piso', '.'), 
           'cliente_puerta': data.get('cliente_puerta', ''), 
           'cliente_poblacion': data.get('cliente_poblacion', ''), 
           'cliente_cpostal': data.get('cliente_cpostal', ''), 
           'cliente_pais': data.get('cliente_pais', ''), 
           'cliente_email': data.get('cliente_email', ''), 
           'cliente_telefono': data.get('cliente_telefono', ''), 
           'cliente_atencion': data.get('cliente_atencion', ''), 
           'aviso_preaviso': data.get('aviso_preaviso', 'N'), 
           'aviso_reparto': data.get('aviso_reparto', 'N'), 
           'aviso_email': data.get('aviso_email', 'N'), 
           'aviso_sms': data.get('aviso_sms', 'N'), 
           'id_mercancia': data.get('id_mercancia', '')}
        if not self.context.get('pdf'):
            vals['printer'] = self.context.get('printer', 'ZEBRA')
            vals['printer_model'] = self.context.get('printer_model', 'LP2844-Z')
            vals['ecb_code'] = self.context.get('ecb_code', '2C')
        url = 'http://cit.seur.com/CIT-war/services/ImprimirECBWebService'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return (reference, label, 'timed out')
        else:
            dom = parseString(result)
            mensaje = dom.getElementsByTagName('mensaje')
            if mensaje:
                if mensaje[0].firstChild.data != 'OK':
                    error = '%s - %s' % (vals['ref_bulto'], mensaje[0].firstChild.data)
                    return (
                     reference, label, error)
            ecb = dom.getElementsByTagName('ECB')
            if ecb:
                reference = ecb[0].childNodes[0].firstChild.data
            if self.context.get('pdf'):
                pdf = dom.getElementsByTagName('PDF')
                if pdf:
                    label = pdf[0].firstChild.data
            else:
                traza = dom.getElementsByTagName('traza')
                if traza:
                    label = traza[0].firstChild.data
            return (
             reference, label, error)

    def info(self, data):
        """
        Picking info using the given data

        :param data: Dictionary of values
        :return: info dict
        """
        tmpl = loader.load('picking_info.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'expedicion': data.get('expedicion', 'S'), 
           'reference': data.get('reference'), 
           'service': data.get('service', '0'), 
           'public': data.get('public', 'N')}
        url = 'https://ws.seur.com/webseur/services/WSConsultaExpediciones'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return
        dom = parseString(result)
        info = dom.getElementsByTagName('out')
        return info[0].firstChild.data

    def list(self, data):
        """
        Picking list using the given data

        :param data: Dictionary of values
        :return: list dict
        """
        tmpl = loader.load('picking_list.xml')
        t = datetime.datetime.now()
        today = '%s-%s-%s' % (t.day, t.month, t.year)
        vals = {'username': self.username, 
           'password': self.password, 
           'ccc': self.ccc, 
           'expedicion': data.get('expedicion', 'S'), 
           'date_from': data.get('from', today), 
           'date_to': data.get('to', today), 
           'service': data.get('service', '0'), 
           'public': data.get('public', 'N')}
        url = 'https://ws.seur.com/webseur/services/WSConsultaExpediciones'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return
        dom = parseString(result)
        info = dom.getElementsByTagName('out')
        return info[0].firstChild.data

    def label(self, data):
        """
        Get label picking using reference

        :param data: Dictionary of values
        :return: string
        """
        if self.context.get('pdf'):
            tmpl = loader.load('picking_label_pdf.xml')
        else:
            tmpl = loader.load('picking_label.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'vat': self.vat, 
           'franchise': self.franchise, 
           'seurid': self.seurid, 
           'ci': self.ci, 
           'ccc': self.ccc, 
           'servicio': data.get('servicio', '1'), 
           'product': data.get('product', '2'), 
           'total_bultos': data.get('total_bultos', 1), 
           'total_kilos': data.get('total_kilos', '1'), 
           'peso_bulto': data.get('peso_bulto', '1'), 
           'observaciones': data.get('observaciones', ''), 
           'referencia_expedicion': data.get('referencia_expedicion', ''), 
           'ref_bulto': data.get('ref_bulto', ''), 
           'clave_portes': data.get('clave_portes', 'F'), 
           'clave_reembolso': data.get('clave_reembolso', 'F'), 
           'valor_reembolso': data.get('valor_reembolso', ''), 
           'cliente_nombre': data.get('cliente_nombre', ''), 
           'cliente_direccion': data.get('cliente_direccion', ''), 
           'cliente_tipovia': data.get('cliente_tipovia', 'CL'), 
           'cliente_tnumvia': data.get('cliente_tnumvia', 'N'), 
           'cliente_numvia': data.get('cliente_numvia', '.'), 
           'cliente_escalera': data.get('cliente_escalera', '.'), 
           'cliente_piso': data.get('cliente_piso', '.'), 
           'cliente_puerta': data.get('cliente_puerta', ''), 
           'cliente_poblacion': data.get('cliente_poblacion', ''), 
           'cliente_cpostal': data.get('cliente_cpostal', ''), 
           'cliente_pais': data.get('cliente_pais', ''), 
           'cliente_email': data.get('cliente_email', ''), 
           'cliente_telefono': data.get('cliente_telefono', ''), 
           'cliente_atencion': data.get('cliente_atencion', ''), 
           'id_mercancia': data.get('id_mercancia', '')}
        if not self.context.get('pdf'):
            vals['printer'] = self.context.get('printer', 'ZEBRA')
            vals['printer_model'] = self.context.get('printer_model', 'LP2844-Z')
            vals['ecb_code'] = self.context.get('ecb_code', '2C')
        url = 'http://cit.seur.com/CIT-war/services/ImprimirECBWebService'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return
        dom = parseString(result)
        if self.context.get('pdf'):
            pdf = dom.getElementsByTagName('PDF')
            if pdf:
                return pdf[0].firstChild.data
        else:
            traza = dom.getElementsByTagName('traza')
            if traza:
                return traza[0].firstChild.data

    def manifiesto(self, data):
        """
        Get Manifiesto

        :param data: Dictionary of values
        :return: string
        """
        tmpl = loader.load('manifiesto.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'vat': self.vat, 
           'franchise': self.franchise, 
           'seurid': self.seurid, 
           'ci': self.ci, 
           'ccc': self.ccc}
        if data.get('date'):
            vals['date'] = data.get('date')
        else:
            d = datetime.datetime.now()
            vals['date'] = '%s-%s-%s' % (d.year, d.strftime('%m'), d.strftime('%d'))
        url = 'http://cit.seur.com/CIT-war/services/DetalleBultoPDFWebService'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return
        else:
            dom = parseString(result)
            pdf = dom.getElementsByTagName('ns1:out')
            if pdf:
                return pdf[0].firstChild.data
            return

    def city(self, city):
        """
        Get Seur values from city

        :param city: string
        :return: dict
        """
        tmpl = loader.load('city.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'city': city.upper()}
        url = 'https://ws.seur.com/WSEcatalogoPublicos/servlet/XFireServlet/WSServiciosWebPublicos'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return []
        dom = parseString(result)
        info = dom.getElementsByTagName('out')
        data = info[0].firstChild.data
        dom2 = parseString(data.encode('utf-8'))
        registros = dom2.getElementsByTagName('REGISTROS')
        total = registros[0].childNodes.length
        values = []
        for i in range(1, total + 1):
            reg_name = 'REG%s' % i
            reg = registros[0].getElementsByTagName(reg_name)[0]
            vals = {}
            for r in reg.childNodes:
                vals[r.nodeName] = r.firstChild.data

            values.append(vals)

        return values

    def zip(self, zip):
        """
        Get Seur values from zip

        :param zip: string
        :return: list dict
        """
        tmpl = loader.load('zip.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'zip': zip}
        url = 'https://ws.seur.com/WSEcatalogoPublicos/servlet/XFireServlet/WSServiciosWebPublicos'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return []
        dom = parseString(result)
        info = dom.getElementsByTagName('ns1:out')
        data = info[0].firstChild.data
        dom2 = parseString(data.encode('utf-8'))
        registros = dom2.getElementsByTagName('REGISTROS')
        total = registros[0].childNodes.length
        values = []
        for i in range(1, total + 1):
            reg_name = 'REG%s' % i
            reg = registros[0].getElementsByTagName(reg_name)[0]
            vals = {}
            for r in reg.childNodes:
                vals[r.nodeName] = r.firstChild.data

            values.append(vals)

        return values