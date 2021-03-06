#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Replacement (unofficial) `setup.py` for the `l10n_be` module.
Automatically generated by `openerpdist`. See http://noteed.com/openerpdist/.
"""

import setuptools

setuptools.setup(
    name = "openerp-l10n-be",
    version = "7.0.406",
    description = "Belgium - Accounting",
    long_description = 
"""

This is the base module to manage the accounting chart for Belgium in OpenERP.
==============================================================================

After installing this module, the Configuration wizard for accounting is launched.
    * We have the account templates which can be helpful to generate Charts of Accounts.
    * On that particular wizard, you will be asked to pass the name of the company,
      the chart template to follow, the no. of digits to generate, the code for your
      account and bank account, currency to create journals.

Thus, the pure copy of Chart Template is generated.

Wizards provided by this module:
--------------------------------
    * Partner VAT Intra: Enlist the partners with their related VAT and invoiced
      amounts. Prepares an XML file format.
      
        **Path to access :** Invoicing/Reporting/Legal Reports/Belgium Statements/Partner VAT Intra
    * Periodical VAT Declaration: Prepares an XML file for Vat Declaration of
      the Main company of the User currently Logged in.
      
        **Path to access :** Invoicing/Reporting/Legal Reports/Belgium Statements/Periodical VAT Declaration
    * Annual Listing Of VAT-Subjected Customers: Prepares an XML file for Vat
      Declaration of the Main company of the User currently Logged in Based on
      Fiscal year.
      
        **Path to access :** Invoicing/Reporting/Legal Reports/Belgium Statements/Annual Listing Of VAT-Subjected Customers

    
""",
    url = "",
    author = "Noviat & OpenERP SA",
    author_email = "TODO",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    license = "AGPL-3",
    package_dir = {
        'openerp.addons.l10n_be': ".",
    },
    packages = ["openerp.addons.l10n_be","openerp.addons.l10n_be.wizard"],
    package_data = {
        'openerp.addons.l10n_be': ["i18n/*.po*","account_tax_code_template.xml","fiscal_templates.xml","l10n_be_sequence.xml","pcmn3.csv","pcmn.csv","account_demo.xml","account_chart_template.xml","account_fiscal_position_tax_template.xml","account_financial_report.xml","account_tax_template.xml","account_pcmn_belgium.xml","account_chart_template.yml","images/2_l10n_be_chart.jpeg","images/1_config_chart_l10n_be.jpeg","static/src/img/icon.png","i18n/ko_KO.po","i18n/id.po","i18n/hr.po","i18n/da.po","i18n/sl.po","i18n/es_MX.po","i18n/ru.po","i18n/zh_TW.po","i18n/en_GB.po","i18n/cs.po","i18n/sq.po","i18n/fi.po","i18n/pt_BR.po","i18n/ko.po","i18n/bg.po","i18n/es_VE.po","i18n/tlh.po","i18n/ja.po","i18n/ro.po","i18n/es_AR.po","i18n/sr@latin.po","i18n/es.po","i18n/it.po","i18n/nl.po","i18n/sv.po","i18n/uk.po","i18n/bs.po","i18n/tr.po","i18n/znd_ZND.po","i18n/de.po","i18n/et.po","i18n/lt.po","i18n/hu.po","i18n/vi.po","i18n/gl.po","i18n/mk.po","i18n/ca.po","i18n/fr.po","i18n/zh_CN.po","i18n/pl.po","i18n/nl_BE.po","i18n/ar.po","i18n/pt.po","i18n/es_CR.po","security/ir.model.access.csv","wizard/account_wizard.xml","wizard/l10n_be_partner_vat_listing.rml","wizard/l10n_be_partner_vat_listing.xml","wizard/l10n_be_vat_intra_view.xml","wizard/l10n_be_account_vat_declaration_view.xml","wizard/l10n_be_vat_intra_print.rml","i18n_extra/nl_BE.po","account_financial_report.xml","account_pcmn_belgium.xml","account_tax_code_template.xml","account_chart_template.xml","account_chart_template.yml","account_tax_template.xml","wizard/l10n_be_account_vat_declaration_view.xml","wizard/l10n_be_vat_intra_view.xml","wizard/l10n_be_partner_vat_listing.xml","wizard/account_wizard.xml","l10n_be_sequence.xml","fiscal_templates.xml","account_fiscal_position_tax_template.xml","security/ir.model.access.csv"],
    },
    install_requires = ["openerp-account","openerp-base-vat","openerp-base-iban","openerp-account-chart","openerp-l10n-be-coda"],
    tests_require = ["unittest2"],
)
