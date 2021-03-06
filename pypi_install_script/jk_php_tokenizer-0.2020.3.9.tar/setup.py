################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
	],
	description = "This python module is a tokenizer for configuration files written in PHP.",
	download_url = "https://github.com/jkpubsrc/python-module-jk-php-tokenizer/tarball/0.2020.3.9",
	include_package_data = False,
	install_requires = [
		"jk_utils",
	],
	keywords = [
		"tokenizing",
		"tokenizer",
		"php",
	],
	license = "Apache 2.0",
	name = "jk_php_tokenizer",
	packages = [
		"jk_php_tokenizer",
	],
	url = "https://github.com/jkpubsrc/python-module-jk-php-tokenizer",
	version = "0.2020.3.9",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
