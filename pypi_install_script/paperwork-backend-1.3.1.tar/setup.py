#!/usr/bin/env python3

import os
import sys

from setuptools import setup, find_packages

if os.name == "nt":
    extra_deps = []
else:
    extra_deps = [
        "python-Levenshtein",
    ]

quiet = '--quiet' in sys.argv or '-q' in sys.argv

try:
    with open("paperwork_backend/_version.py", "r") as file_descriptor:
        version = file_descriptor.read().strip()
        version = version.split(" ")[2][1:-1]
    if not quiet:
        print("Paperwork-backend version: {}".format(version))
    if "-" in version:
        version = version.split("-")[0]
except FileNotFoundError:
    print("ERROR: _version.py file is missing")
    print("ERROR: Please run 'make version' first")
    sys.exit(1)

setup(
    name="paperwork-backend",
    version=version,
    description=(
        "Paperwork's backend"
    ),
    long_description="""Paperwork is a GUI to make papers searchable.

This is the backend part of Paperwork. It manages:
- The work directory / Access to the documents
- Indexing
- Searching
- Suggestions
- Import
- Export

There is no GUI here. The GUI is
<https://gitlab.gnome.org/World/OpenPaperwork/paperwork>.
    """,
    keywords="documents",
    url=(
        "https://gitlab.gnome.org/World/OpenPaperwork/paperwork/tree/master/"
        "paperwork-backend"
    ),
    download_url=(
        "https://gitlab.gnome.org/World/OpenPaperwork/paperwork/-"
        "/archive/{}/paperwork-{}.tar.gz".format(version, version)
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        ("License :: OSI Approved ::"
         " GNU General Public License v3 or later (GPLv3+)"),
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Indexing",
    ],
    license="GPLv3+",
    author="Jerome Flesch",
    author_email="jflesch@openpaper.work",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'paperwork-shell = paperwork_backend.shell_cmd:main',
        ],
    },
    zip_safe=True,
    install_requires=[
        "distro",
        "natsort",
        "Pillow",
        "pycountry",
        "pyocr",
        "simplebayes",
        "termcolor",  # used by paperwork-chkdeps
        "Whoosh",
        # paperwork-shell chkdeps take care of all the dependencies that can't
        # be handled here. Mainly, dependencies using gobject introspection
        # (libpoppler, etc)
    ] + extra_deps
)

if quiet:
    sys.exit(0)

print("============================================================")
print("============================================================")
print("||                       IMPORTANT                        ||")
print("|| Please run 'paperwork-shell chkdeps paperwork_backend' ||")
print("||            to find any missing dependency              ||")
print("============================================================")
print("============================================================")
