# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "django",
]

setup(
    name="django-force-disable-permissions-admin",
    version="0.2.0",
    description="Force disable permissions in admin site.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django admin extentions", "django force disable permissions admin"],
    install_requires=requires,
    packages=find_packages(".", exclude=["force_disable_permissions_example", "force_disable_permissions_example.migrations", "force_disable_permissions_demo"]),
    py_modules=["force_disable_permissions"],
    zip_safe=False,
    include_package_data=True,
)