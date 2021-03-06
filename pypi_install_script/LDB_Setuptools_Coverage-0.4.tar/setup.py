# Copyright 2016 Alex Orange
# 
# This file is part of LDB Setuptools Coverage.
# 
# LDB Setuptools Coverage is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LDB Setuptools Coverage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with LDB Setuptools Coverage.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(name="Dummy_test_pass",
      namespace_packages=['ns_pkg'],
      packages=['my_pkg', 'ns_pkg', 'ns_pkg.pkg'],
      test_suite='test',
     )
