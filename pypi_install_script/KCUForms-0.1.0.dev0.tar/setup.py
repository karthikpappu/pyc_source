import re
from collections import OrderedDict
import io

from setuptools import setup, find_packages

# read the contents of project README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "README.md"), "rt", encoding="utf-8") as fd:
    readme = fd.read()

with io.open("src/kcuforms/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

reqs = [
    'flask_restful==0.3.7',
    'six==1.12.0'
]

setup(
    name="KCUForms",
    version=version,
    url="https://github.com/DeeeFOX/kcuforms",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://github.com/DeeeFOX/kcuforms"),
            ("Code", "https://github.com/DeeeFOX/kcuforms/tree/master/src/kcuforms"),
            ("Issue tracker", "https://github.com/DeeeFOX/kcuforms/issues"),
        )
    ),
    license="BSD",
    maintainer="KCUForms team",
    maintainer_email="dennias.chiu@gmail.com",
    author="deefox",
    author_email="602716933@qq.com",
    description=(
        "A flexible forms validation and rendering library for Python"
        " web development"
        " that inherited and learned from WTForms."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=reqs
)
