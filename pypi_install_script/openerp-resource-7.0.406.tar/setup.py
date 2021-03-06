#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Replacement (unofficial) `setup.py` for the `resource` module.
Automatically generated by `openerpdist`. See http://noteed.com/openerpdist/.
"""

import setuptools

setuptools.setup(
    name = "openerp-resource",
    version = "7.0.406",
    description = "Resource",
    long_description = 
"""

Module for resource management.
===============================

A resource represent something that can be scheduled (a developer on a task or a
work center on manufacturing orders). This module manages a resource calendar
associated to every resource. It also manages the leaves of every resource.
    
""",
    url = "http://www.openerp.com",
    author = "OpenERP SA",
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
        'openerp.addons.resource': ".",
    },
    packages = ["openerp.addons.resource","openerp.addons.resource.faces"],
    package_data = {
        'openerp.addons.resource': ["i18n/*.po*","resource_demo.xml","resource_view.xml","images/resource_leaves_calendar.jpeg","images/resource_leaves_form.jpeg","i18n/hr.po","i18n/da.po","i18n/sl.po","i18n/es_MX.po","i18n/ru.po","i18n/cs.po","i18n/fi.po","i18n/pt_BR.po","i18n/bg.po","i18n/es_VE.po","i18n/ja.po","i18n/ro.po","i18n/es.po","i18n/mn.po","i18n/it.po","i18n/nl.po","i18n/sv.po","i18n/es_EC.po","i18n/bs.po","i18n/tr.po","i18n/de.po","i18n/et.po","i18n/lt.po","i18n/hu.po","i18n/vi.po","i18n/gl.po","i18n/mk.po","i18n/ca.po","i18n/fr.po","i18n/zh_CN.po","i18n/pl.po","i18n/he.po","i18n/ar.po","i18n/pt.po","i18n/es_CR.po","test/resource.yml","test/duplicate_resource.yml","security/ir.model.access.csv","security/ir.model.access.csv","resource_view.xml","resource_demo.xml"],
    },
    install_requires = ["openerp-process"],
    tests_require = ["unittest2"],
)
