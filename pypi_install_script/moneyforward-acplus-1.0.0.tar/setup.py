# coding: utf-8

"""
    マネーフォワードクラウド会計Plus API

    マネーフォワードクラウド会計PlusのAPI  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: api.acplus.support@moneyforward.co.jp
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "moneyforward-acplus"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="マネーフォワードクラウド会計Plus API",
    author="OTA2000",
    author_email="yasuhiroota26@gmail.com",
    url="https://github.com/moneyforward-api-client/acplus-python",
    keywords=["OpenAPI", "OpenAPI-Generator", "マネーフォワードクラウド会計Plus API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    マネーフォワードクラウド会計PlusのAPI
    """
)
