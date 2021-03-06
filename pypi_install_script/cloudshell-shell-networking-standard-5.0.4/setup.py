import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cloudshell-shell-networking-standard",
    url="http://www.qualisystems.com/",
    author="Quali",
    author_email="info@quali.com",
    packages=find_packages(),
    install_requires=required,
    tests_require=required_for_tests,
    python_requires=(
        ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, <4"
    ),
    test_suite="nose.collector",
    version=version_from_file,
    description="QualiSystems Shells Networking Standard Package",
    include_package_data=True,
)
