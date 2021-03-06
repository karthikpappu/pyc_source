# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sunatservice/debitnote.py
# Compiled at: 2020-01-09 18:05:03
# Size of source mod 2**32: 26049 bytes
from lxml import etree
import json
from xml.dom import minidom

class Debitnote:

    def fillDocument(self, XMLpath, fileName, data):
        tree = etree.parse(XMLpath + '/XMLdocuments/1_unfilled/UNFILLED-debit-note.XML')
        XMLFileContents = etree.tostring((tree.getroot()), pretty_print=True, xml_declaration=True, encoding='UTF-8', standalone='yes')
        data = json.dumps(data, indent=4)
        data = json.loads(data)
        DebitNoteNode = tree.getroot()
        documentID = str(data['serie']) + '-' + str(data['numero'])
        ID = DebitNoteNode.find(self.getInvoiceNameSpace('cbc') + 'ID')
        ID.text = documentID
        IssueDate = DebitNoteNode.find(self.getInvoiceNameSpace('cbc') + 'IssueDate')
        IssueDate.text = data['fechaEmision']
        IssueTime = DebitNoteNode.find(self.getInvoiceNameSpace('cbc') + 'IssueTime')
        IssueTime.text = data['horaEmision']
        Note = DebitNoteNode.find(self.getInvoiceNameSpace('cbc') + 'Note')
        Note.text = self.precioALiteral(data['totalVentaGravada'])
        Note.set('languageLocaleID', '1000')
        DocumentCurrencyCode = DebitNoteNode.find(self.getInvoiceNameSpace('cbc') + 'DocumentCurrencyCode')
        DocumentCurrencyCode.text = data['tipoMoneda']
        for DiscrepancyResponse in DebitNoteNode.findall(self.getInvoiceNameSpace('cac') + 'DiscrepancyResponse'):
            ReferenceID = DiscrepancyResponse.find(self.getInvoiceNameSpace('cbc') + 'ReferenceID')
            ReferenceID.text = data['documentoOrigen']
            ResponseCode = DiscrepancyResponse.find(self.getInvoiceNameSpace('cbc') + 'ResponseCode')
            ResponseCode.text = data['notaDiscrepanciaCode']
            Description = DiscrepancyResponse.find(self.getInvoiceNameSpace('cbc') + 'Description')
            Description.text = etree.CDATA(data['notaDescripcion'])

        for BillingReference in DebitNoteNode.findall(self.getInvoiceNameSpace('cac') + 'BillingReference'):
            for InvoiceDocumentReference in BillingReference.findall(self.getInvoiceNameSpace('cac') + 'InvoiceDocumentReference'):
                ID = InvoiceDocumentReference.find(self.getInvoiceNameSpace('cbc') + 'ID')
                ID.text = documentID
                DocumentTypeCode = InvoiceDocumentReference.find(self.getInvoiceNameSpace('cbc') + 'DocumentTypeCode')
                DocumentTypeCode.text = data['documentoOrigenTipo']

        for Signature in DebitNoteNode.iter(self.getInvoiceNameSpace('cac') + 'Signature'):
            ID = Signature.find(self.getInvoiceNameSpace('cbc') + 'ID')
            ID.text = 'S' + documentID
            SignatoryParty = Signature.find(self.getInvoiceNameSpace('cac') + 'SignatoryParty')
            PartyIdentification = SignatoryParty.find(self.getInvoiceNameSpace('cac') + 'PartyIdentification')
            ID = PartyIdentification.find(self.getInvoiceNameSpace('cbc') + 'ID')
            ID.text = data['emisor']['nro']
            PartyName = SignatoryParty.find(self.getInvoiceNameSpace('cac') + 'PartyName')
            Name = PartyName.find(self.getInvoiceNameSpace('cbc') + 'Name')
            Name.text = etree.CDATA(data['emisor']['nombre'])
            DigitalSignatureAttachment = Signature.find(self.getInvoiceNameSpace('cac') + 'DigitalSignatureAttachment')
            ExternalReference = DigitalSignatureAttachment.find(self.getInvoiceNameSpace('cac') + 'ExternalReference')
            URI = ExternalReference.find(self.getInvoiceNameSpace('cbc') + 'URI')
            URI.text = '#S' + documentID

        for AccountingSupplierParty in DebitNoteNode.findall(self.getInvoiceNameSpace('cac') + 'AccountingSupplierParty'):
            Party = AccountingSupplierParty.find(self.getInvoiceNameSpace('cac') + 'Party')
            PartyIdentification = Party.find(self.getInvoiceNameSpace('cac') + 'PartyIdentification')
            ID = PartyIdentification.find(self.getInvoiceNameSpace('cbc') + 'ID')
            ID.text = data['emisor']['nro']
            ID.set('schemeID', str(data['emisor']['tipo_documento']))
            ID.set('schemeName', str('SUNAT:Identificador de Documento de Identidad'))
            ID.set('schemeAgencyName', str('PE:SUNAT'))
            PartyName = Party.find(self.getInvoiceNameSpace('cac') + 'PartyName')
            Name = PartyName.find(self.getInvoiceNameSpace('cbc') + 'Name')
            Name.text = etree.CDATA(data['emisor']['nombre'])
            PartyLegalEntity = Party.find(self.getInvoiceNameSpace('cac') + 'PartyLegalEntity')
            RegistrationName = PartyLegalEntity.find(self.getInvoiceNameSpace('cbc') + 'RegistrationName')
            RegistrationName.text = etree.CDATA(data['emisor']['nombre'])
            RegistrationAddress = PartyLegalEntity.find(self.getInvoiceNameSpace('cac') + 'RegistrationAddress')
            AddressTypeCode = RegistrationAddress.find(self.getInvoiceNameSpace('cbc') + 'AddressTypeCode')
            AddressTypeCode.text = str(data['emisor']['ubigeo'])

        for AccountingCustomerParty in DebitNoteNode.findall(self.getInvoiceNameSpace('cac') + 'AccountingCustomerParty'):
            Party = AccountingCustomerParty.find(self.getInvoiceNameSpace('cac') + 'Party')
            PartyIdentification = Party.find(self.getInvoiceNameSpace('cac') + 'PartyIdentification')
            ID = PartyIdentification.find(self.getInvoiceNameSpace('cbc') + 'ID')
            ID.text = data['receptor']['nro']
            ID.set('schemeID', str(data['receptor']['tipo_documento']))
            PartyLegalEntity = Party.find(self.getInvoiceNameSpace('cac') + 'PartyLegalEntity')
            RegistrationName = PartyLegalEntity.find(self.getInvoiceNameSpace('cbc') + 'RegistrationName')
            RegistrationName.text = etree.CDATA(data['receptor']['nombre'])

        tagTaxTotalAdded = False
        tributos = data['tributos']
        for tributo_name in tributos:
            tributo = tributos[str(tributo_name)]
            for tributo_item_percent_differenced in tributo:
                tribute_details = self.getTributeDetails(tributo_item_percent_differenced['codigo'])
                if tagTaxTotalAdded == False:
                    TaxTotal = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxTotal')
                    TaxAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxAmount')
                    TaxAmount.text = format(float(tributo_item_percent_differenced['sumatoria']), '.2f')
                    TaxAmount.set('currencyID', data['tipoMoneda'])
                    TaxTotal.append(TaxAmount)
                TaxSubtotal = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxSubtotal')
                TaxableAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxableAmount')
                TaxableAmount.text = format(float(tributo_item_percent_differenced['total_venta']), '.2f')
                TaxableAmount.set('currencyID', data['tipoMoneda'])
                TaxSubtotal.append(TaxableAmount)
                TaxAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxAmount')
                TaxAmount.text = format(float(tributo_item_percent_differenced['sumatoria']), '.2f')
                TaxAmount.set('currencyID', data['tipoMoneda'])
                TaxSubtotal.append(TaxAmount)
                if str(tributo_item_percent_differenced['codigo']) != '7152':
                    Percent = etree.Element(self.getInvoiceNameSpace('cbc') + 'Percent')
                    Percent.text = str(tributo_item_percent_differenced['porcentaje'])
                    TaxSubtotal.append(Percent)
                TaxCategory = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxCategory')
                ID = etree.Element(self.getInvoiceNameSpace('cbc') + 'ID')
                ID.text = tribute_details['category_code']
                ID.set('schemeID', 'UN/ECE 5153')
                ID.set('schemeAgencyID', '6')
                TaxCategory.append(ID)
                TaxScheme = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxScheme')
                ID = etree.Element(self.getInvoiceNameSpace('cbc') + 'ID')
                ID.text = tributo_item_percent_differenced['codigo']
                ID.set('schemeID', 'UN/ECE 5153')
                ID.set('schemeAgencyID', '6')
                TaxScheme.append(ID)
                Name = etree.Element(self.getInvoiceNameSpace('cbc') + 'Name')
                Name.text = str(tribute_details['name']).strip()
                TaxScheme.append(Name)
                TaxTypeCode = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxTypeCode')
                TaxTypeCode.text = tribute_details['name_code']
                TaxScheme.append(TaxTypeCode)
                TaxCategory.append(TaxScheme)
                TaxSubtotal.append(TaxCategory)
                TaxTotal.append(TaxSubtotal)
                if tagTaxTotalAdded == False:
                    DebitNoteNode.append(TaxTotal)
                    tagTaxTotalAdded = True

        RequestedMonetaryTotal = etree.Element(self.getInvoiceNameSpace('cac') + 'RequestedMonetaryTotal')
        PayableAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'PayableAmount')
        PayableAmount.text = format(float(data['totalVentaGravada']), '.2f')
        PayableAmount.set('currencyID', data['tipoMoneda'])
        RequestedMonetaryTotal.append(PayableAmount)
        DebitNoteNode.append(RequestedMonetaryTotal)
        index = 0
        items = data['items']
        for item in items:
            DebitNoteLine = etree.Element(self.getInvoiceNameSpace('cac') + 'DebitNoteLine')
            ID = etree.Element(self.getInvoiceNameSpace('cbc') + 'ID')
            ID.text = str(index + 1)
            DebitNoteLine.append(ID)
            DebitedQuantity = etree.Element(self.getInvoiceNameSpace('cbc') + 'DebitedQuantity')
            DebitedQuantity.text = item['cantidad']
            DebitedQuantity.set('unitCode', item['medidaCantidad'])
            DebitedQuantity.set('unitCodeListID', 'UN/ECE rec 20')
            DebitedQuantity.set('unitCodeListAgencyName', 'United Nations Economic Commission for Europe')
            DebitNoteLine.append(DebitedQuantity)
            LineExtensionAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'LineExtensionAmount')
            LineExtensionAmount.text = format(float(item['subTotalVenta']), '.2f')
            LineExtensionAmount.set('currencyID', data['tipoMoneda'])
            DebitNoteLine.append(LineExtensionAmount)
            PricingReference = etree.Element(self.getInvoiceNameSpace('cac') + 'PricingReference')
            AlternativeConditionPrice = etree.Element(self.getInvoiceNameSpace('cac') + 'AlternativeConditionPrice')
            PriceAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'PriceAmount')
            PriceAmount.text = format(float(item['totalVenta']) / float(item['cantidad']), '.2f')
            PriceAmount.set('currencyID', data['tipoMoneda'])
            AlternativeConditionPrice.append(PriceAmount)
            PriceTypeCode = etree.Element(self.getInvoiceNameSpace('cbc') + 'PriceTypeCode')
            PriceTypeCode.text = item['tipoPrecioVentaUnitario']
            PriceTypeCode.set('listName', 'Tipo de Precio')
            PriceTypeCode.set('listAgencyName', 'PE:SUNAT')
            PriceTypeCode.set('listURI', 'urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo16')
            AlternativeConditionPrice.append(PriceTypeCode)
            PricingReference.append(AlternativeConditionPrice)
            DebitNoteLine.append(PricingReference)
            tributos = item['tributos']
            tagTaxTotalAdded = False
            for tributo in tributos:
                trubuteDetails = self.getTributeDetails(tributo['codigo'])
                if tagTaxTotalAdded == False:
                    TaxTotal = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxTotal')
                    TaxAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxAmount')
                    TaxAmount.text = format(float(tributo['montoAfectacionTributo']), '.2f')
                    TaxAmount.set('currencyID', data['tipoMoneda'])
                    TaxTotal.append(TaxAmount)
                TaxSubtotal = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxSubtotal')
                if str(tributo['codigo']) != '7152':
                    TaxableAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxableAmount')
                    TaxableAmount.text = format(float(tributo['total_venta']), '.2f')
                    TaxableAmount.set('currencyID', data['tipoMoneda'])
                    TaxSubtotal.append(TaxableAmount)
                TaxAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxAmount')
                TaxAmount.text = format(float(tributo['montoAfectacionTributo']), '.2f')
                TaxAmount.set('currencyID', data['tipoMoneda'])
                TaxSubtotal.append(TaxAmount)
                if str(tributo['codigo']) == '7152':
                    BaseUnitMeasure = etree.Element(self.getInvoiceNameSpace('cbc') + 'BaseUnitMeasure')
                    BaseUnitMeasure.text = format(float(item['cantidad']), '.0f')
                    BaseUnitMeasure.set('unitCode', item['medidaCantidad'])
                    TaxSubtotal.append(BaseUnitMeasure)
                TaxCategory = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxCategory')
                if str(tributo['codigo']) != '7152':
                    ID = etree.Element(self.getInvoiceNameSpace('cbc') + 'ID')
                    ID.text = trubuteDetails['category_code']
                    ID.set('schemeID', 'UN/ECE 5153')
                    ID.set('schemeAgencyID', '6')
                    TaxCategory.append(ID)
                if str(tributo['codigo']) == '7152':
                    PerUnitAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'PerUnitAmount')
                    PerUnitAmount.text = format(float(tributo['porcentaje']), '.2f')
                    PerUnitAmount.set('currencyID', data['tipoMoneda'])
                    TaxCategory.append(PerUnitAmount)
                if str(tributo['codigo']) != '7152':
                    Percent = etree.Element(self.getInvoiceNameSpace('cbc') + 'Percent')
                    Percent.text = str(tributo['porcentaje'])
                    TaxCategory.append(Percent)
                if tributo['codigo'] == '2000':
                    TaxExemptionReasonCode = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxExemptionReasonCode')
                    TaxExemptionReasonCode.text = str(tributo['tipoAfectacionTributoIGV'])
                    TaxExemptionReasonCode.set('listAgencyName', 'PE:SUNAT')
                    TaxExemptionReasonCode.set('listName', 'SUNAT:Codigo de Tipo de Afectación del IGV')
                    TaxExemptionReasonCode.set('listURI', 'urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo07')
                    TaxCategory.append(TaxExemptionReasonCode)
                    TierRange = etree.Element(self.getInvoiceNameSpace('cbc') + 'TierRange')
                    TierRange.text = str(tributo['sistemaCalculoISC'])
                    TaxCategory.append(TierRange)
                else:
                    TaxExemptionReasonCode = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxExemptionReasonCode')
                    TaxExemptionReasonCode.text = str(tributo['tipoAfectacionTributoIGV'])
                    TaxExemptionReasonCode.set('listAgencyName', 'PE:SUNAT')
                    TaxExemptionReasonCode.set('listName', 'SUNAT:Codigo de Tipo de Afectación del IGV')
                    TaxExemptionReasonCode.set('listURI', 'urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo07')
                    TaxCategory.append(TaxExemptionReasonCode)
                TaxScheme = etree.Element(self.getInvoiceNameSpace('cac') + 'TaxScheme')
                ID = etree.Element(self.getInvoiceNameSpace('cbc') + 'ID')
                ID.text = tributo['codigo']
                ID.set('schemeID', 'UN/ECE 5153')
                ID.set('schemeName', 'Tax Scheme Identifier')
                ID.set('schemeAgencyName', 'United Nations Economic Commission for Europe')
                TaxScheme.append(ID)
                Name = etree.Element(self.getInvoiceNameSpace('cbc') + 'Name')
                Name.text = str(trubuteDetails['name']).strip()
                TaxScheme.append(Name)
                TaxTypeCode = etree.Element(self.getInvoiceNameSpace('cbc') + 'TaxTypeCode')
                TaxTypeCode.text = trubuteDetails['name_code']
                TaxScheme.append(TaxTypeCode)
                TaxCategory.append(TaxScheme)
                TaxSubtotal.append(TaxCategory)
                TaxTotal.append(TaxSubtotal)
                if tagTaxTotalAdded == False:
                    DebitNoteLine.append(TaxTotal)
                    tagTaxTotalAdded = True

            Item = etree.Element(self.getInvoiceNameSpace('cac') + 'Item')
            Description = etree.Element(self.getInvoiceNameSpace('cbc') + 'Description')
            Description.text = etree.CDATA(item['descripcion'])
            Item.append(Description)
            SellersItemIdentification = etree.Element(self.getInvoiceNameSpace('cac') + 'SellersItemIdentification')
            ID = etree.Element(self.getInvoiceNameSpace('cbc') + 'ID')
            ID.text = item['id']
            SellersItemIdentification.append(ID)
            Item.append(SellersItemIdentification)
            CommodityClassification = etree.Element(self.getInvoiceNameSpace('cac') + 'CommodityClassification')
            ItemClassificationCode = etree.Element(self.getInvoiceNameSpace('cbc') + 'ItemClassificationCode')
            ItemClassificationCode.text = item['clasificacionProductoServicioCodigo']
            CommodityClassification.append(ItemClassificationCode)
            Item.append(CommodityClassification)
            DebitNoteLine.append(Item)
            Price = etree.Element(self.getInvoiceNameSpace('cac') + 'Price')
            PriceAmount = etree.Element(self.getInvoiceNameSpace('cbc') + 'PriceAmount')
            PriceAmount.text = format(float(item['precioUnidad']), '.2f')
            PriceAmount.set('currencyID', data['tipoMoneda'])
            Price.append(PriceAmount)
            DebitNoteLine.append(Price)
            DebitNoteNode.append(DebitNoteLine)
            index = index + 1

        tree.write(XMLpath + '/XMLdocuments/2_unsigned/' + fileName + '.XML')
        self.prettyXMLSave(XMLpath + '/XMLdocuments/2_unsigned/' + fileName + '.XML')
        return XMLpath + '/XMLdocuments/2_unsigned/' + fileName + '.XML'

    def prettyXMLSave(self, pathFile):
        tree = etree.parse(pathFile)
        xmlstr = minidom.parseString(etree.tostring(tree.getroot())).toprettyxml(indent='   ')
        with open(pathFile, 'w') as (f):
            f.write(xmlstr)

    def getPriceAmount(self, price_unit, taxes):
        taxes_amount = float(0)
        for tax in taxes:
            tax_amount = float(price_unit * (tax['porcentaje'] / 100))
            taxes_amount = taxes_amount + tax_amount

        price_amount = price_unit + taxes_amount
        return price_amount

    def getTaxAmount(self, tributo):
        taxAmount = float(tributo['IGV']['sumatoria']) + float(tributo['inafecto']['sumatoria']) + float(tributo['exonerado']['sumatoria']) + float(tributo['exportacion']['sumatoria']) + float(tributo['other']['sumatoria'])
        return str(taxAmount)

    def getGlobalTaxableAmountIGV(self, tributo):
        taxAmount = float(tributo['IGV']['total_venta']) + float(tributo['inafecto']['total_venta']) + float(tributo['exonerado']['total_venta']) + float(tributo['exportacion']['total_venta']) + float(tributo['other']['total_venta'])
        return str(taxAmount)

    def getTributeDetails(self, codigo):
        response = {}
        if codigo == '1000':
            response['name'] = 'IGV'
            response['name_code'] = 'VAT'
            response['category_code'] = 'S'
        if codigo == '2000':
            response['name'] = 'ISC'
            response['name_code'] = 'EXC'
            response['category_code'] = 'S'
        if codigo == '7152':
            response['name'] = 'ICBPER'
            response['name_code'] = 'OTH'
            response['category_code'] = 'S'
        if codigo == '9995':
            response['name'] = 'EXPORTACION'
            response['name_code'] = 'FRE'
            response['category_code'] = 'G'
        if codigo == '9996':
            response['name'] = 'GRATUITO'
            response['name_code'] = 'FRE'
            response['category_code'] = 'Z'
        if codigo == '9997':
            response['name'] = 'EXONERADO'
            response['name_code'] = 'VAT'
            response['category_code'] = 'E'
        if codigo == '9998':
            response['name'] = 'INA'
            response['name_code'] = 'FRE'
            response['category_code'] = 'O'
        if codigo == '9999':
            response['name'] = 'OTROS CONCEPTOS DE PAGO'
            response['name_code'] = 'OTH'
            response['category_code'] = 'S'
        return response

    def getInvoiceNameSpace(self, namespace):
        if namespace == 'sac':
            return '{urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1}'
        else:
            if namespace == 'cbc':
                return '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}'
            if namespace == 'ext':
                return '{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}'
            if namespace == 'cac':
                return '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}'

    def precioALiteral(self, numero):
        indicador = [('', ''), ('MIL', 'MIL'), ('MILLON', 'MILLONES'), ('MIL', 'MIL'), ('BILLON', 'BILLONES')]
        entero = int(numero)
        decimal = int(round((numero - entero) * 100))
        contador = 0
        numero_letras = ''
        while entero > 0:
            a = entero % 1000
            if contador == 0:
                en_letras = self.convierte_cifra(a, 1).strip()
            else:
                en_letras = self.convierte_cifra(a, 0).strip()
            if a == 0:
                numero_letras = en_letras + ' ' + numero_letras
            else:
                if a == 1:
                    if contador in (1, 3):
                        numero_letras = indicador[contador][0] + ' ' + numero_letras
                    else:
                        numero_letras = en_letras + ' ' + indicador[contador][0] + ' ' + numero_letras
                else:
                    numero_letras = en_letras + ' ' + indicador[contador][1] + ' ' + numero_letras
            numero_letras = numero_letras.strip()
            contador = contador + 1
            entero = int(entero / 1000)

        numero_letras = numero_letras + ' Y ' + str(decimal) + '/100 SOLES'
        return numero_letras

    def convierte_cifra(self, numero, sw):
        lista_centana = [
         '', ('CIEN', 'CIENTO'), 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS', 'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS']
        lista_decena = ['', ('DIEZ', 'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE', 'DIECISEIS', 'DIECISIETE', 'DIECIOCHO',
 'DIECINUEVE'),
         ('VEINTE', 'VEINTI'), ('TREINTA', 'TREINTA Y '), ('CUARENTA', 'CUARENTA Y '),
         ('CINCUENTA', 'CINCUENTA Y '), ('SESENTA', 'SESENTA Y '),
         ('SETENTA', 'SETENTA Y '), ('OCHENTA', 'OCHENTA Y '),
         ('NOVENTA', 'NOVENTA Y ')]
        lista_unidad = [
         '', ('UN', 'UNO'), 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE']
        centena = int(numero / 100)
        decena = int((numero - centena * 100) / 10)
        unidad = int(numero - (centena * 100 + decena * 10))
        texto_centena = ''
        texto_decena = ''
        texto_unidad = ''
        texto_centena = lista_centana[centena]
        if centena == 1:
            if decena + unidad != 0:
                texto_centena = texto_centena[1]
            else:
                texto_centena = texto_centena[0]
        else:
            texto_decena = lista_decena[decena]
            if decena == 1:
                texto_decena = texto_decena[unidad]
            elif decena > 1:
                if unidad != 0:
                    texto_decena = texto_decena[1]
                else:
                    texto_decena = texto_decena[0]
        if decena != 1:
            texto_unidad = lista_unidad[unidad]
            if unidad == 1:
                texto_unidad = texto_unidad[sw]
        return '%s %s %s' % (texto_centena, texto_decena, texto_unidad)