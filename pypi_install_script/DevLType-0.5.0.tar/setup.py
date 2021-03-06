import os
import re
import shutil
from sys import argv

from setuptools import setup, find_packages, Command

def get_version():
    with open("DevLType/__init__.py", encoding="utf-8") as f:
        return re.findall(r"__version__ = \"(.+)\"", f.read())[0]

setup(
    name="DevLType",
    version=get_version(),
    description="MyType",
    long_description=" ",
    url="https://github.com/devladityanugraha",
    author_email="adityanugraha5405@gmail.com",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    python_requires="~=3.4",
    packages=find_packages()
)
