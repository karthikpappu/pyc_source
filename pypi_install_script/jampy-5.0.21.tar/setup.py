from setuptools import setup, find_packages
import re

package = "jampy"

def find_version(package):
    version_file = open(package + "/__init__.py").read()
    rex = r'__version__\s*=\s*"([^"]+)"'
    return re.search(rex, version_file).group(1)

def read_docstring(package):
    main_file = open(package + "/jam_axi_rms.py").read()
    rex = r'def jam_axi_rms\([\W\w]+\):\n\s*"""([\W\w]+?)"""'
    docstring = re.search(rex, main_file).group(1)
    return docstring.replace("\n    ", "\n")

setup(name=package,
      version=find_version(package),
      description="JamPy: Jeans Anisotropic Models of Galactic Dynamics",
      long_description=open(package + "/README.rst").read()
                       + read_docstring(package)
                       + "\n\nLicense\n-------\n\n"
                       + open(package + "/LICENSE.txt").read()
                       + open(package + "/CHANGELOG.rst").read(),
      url="http://purl.org/cappellari/software",
      author="Michele Cappellari",
      author_email="michele.cappellari@physics.ox.ac.uk",
      license="Other/Proprietary License",
      packages=find_packages(),
      package_data={"": ["*.rst", "*.txt", "*/*.txt"]},
      install_requires=["numpy", "scipy", "matplotlib", "plotbin"],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3"],
      zip_safe=True)
