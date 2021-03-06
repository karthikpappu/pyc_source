#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #########################################################################
# Copyright (c) 2018, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2018. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

import os

try:
    from setuptools import find_packages, setup
except AttributeError:
    from setuptools import find_packages, setup

NAME = 'OASYS1-APS-Extensions'
VERSION = '1.0.63'
ISRELEASED = True

DESCRIPTION = 'ShadowOui/SRW extension for the APS'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Luca Rebuffi'
AUTHOR_EMAIL = 'lrebuffi@anl.gov'
URL = 'https://github.com/oasys-aps-kit/OASYS1-APS-Extensions'
DOWNLOAD_URL = 'https://github.com/oasys-aps-kit/OASYS1-APS-Extensions'
LICENSE = 'GPLv3'

KEYWORDS = (
    'raytracing',
    'simulator',
    'oasys1',
)

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
)

SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    'setuptools',
    'scikit-image'
)

PACKAGES = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests'))

PACKAGE_DATA = {
    "orangecontrib.aps.oasys.widgets.extension":["icons/*.png", "icons/*.jpg", "misc/*.png"],
    "orangecontrib.aps.syned.widgets.extension":["icons/*.png", "icons/*.jpg", "misc/*.png"],
    "orangecontrib.aps.shadow.widgets.extension":["icons/*.png", "icons/*.jpg", "misc/*.png"],
    "orangecontrib.aps.srw.widgets.extension":["icons/*.png", "icons/*.jpg", "misc/*.png"],
}

NAMESPACE_PACAKGES = ["orangecontrib",
                      "orangecontrib.aps",
                      "orangecontrib.aps.oasys",
                      "orangecontrib.aps.syned",
                      "orangecontrib.aps.shadow",
                      "orangecontrib.aps.srw",
                      "orangecontrib.aps.oasys.widgets",
                      "orangecontrib.aps.syned.widgets",
                      "orangecontrib.aps.shadow.widgets",
                      "orangecontrib.aps.srw.widgets",
                      ]

ENTRY_POINTS = {
    'oasys.addons' : ("Oasys APS Extension = orangecontrib.aps.oasys",
                      "SYNED APS Extension = orangecontrib.aps.syned",
                      "Shadow APS Extension = orangecontrib.aps.shadow",
                      "SRW APS Extension = orangecontrib.aps.srw",
                      ),
    'oasys.widgets' : (
        "Oasys APS Extension = orangecontrib.aps.oasys.widgets.extension",
        "SYNED APS Extension = orangecontrib.aps.syned.widgets.extension",
        "Shadow APS Extension = orangecontrib.aps.shadow.widgets.extension",
        "SRW APS Extension = orangecontrib.aps.srw.widgets.extension",
    ),
    'oasys.menus' : ("apsshadowmenu = orangecontrib.aps.shadow.menu",)
}

if __name__ == '__main__':
    try:
        import PyMca5, PyQt4

        raise NotImplementedError("This version of APS ShadowOui doesn't work with Oasys1 beta.\nPlease install OASYS1 final release: http://www.elettra.eu/oasys.html")
    except:
        setup(
              name = NAME,
              version = VERSION,
              description = DESCRIPTION,
              long_description = LONG_DESCRIPTION,
              author = AUTHOR,
              author_email = AUTHOR_EMAIL,
              url = URL,
              download_url = DOWNLOAD_URL,
              license = LICENSE,
              keywords = KEYWORDS,
              classifiers = CLASSIFIERS,
              packages = PACKAGES,
              package_data = PACKAGE_DATA,
              #          py_modules = PY_MODULES,
              setup_requires = SETUP_REQUIRES,
              install_requires = INSTALL_REQUIRES,
              #extras_require = EXTRAS_REQUIRE,
              #dependency_links = DEPENDENCY_LINKS,
              entry_points = ENTRY_POINTS,
              namespace_packages=NAMESPACE_PACAKGES,
              include_package_data = True,
              zip_safe = False,
              )
