r'''
simple proxy pool + proxy validation
'''
# pylint: disable=invalid-name
from pathlib import Path

import os
import re

from setuptools import setup, find_packages

# https://stackoverflow.com/questions/49689880/proper-way-to-parse-requirements-file-after-pip-upgrade-to-pip-10-x-x
# try:  # for pip >= 10
    # from pip._internal.req import parse_requirements
    # from pip._internal.download import PipSession
# except ImportError:  # for pip <= 9.0.3
    # from pip.req import parse_requirements
    # from pip.download import PipSession

name = """zz-test"""
description = ' '.join(name.split('-')) + ' playground'
# dir_name, *_ = find_packages()
dir_name = '_'.join(name.split('-'))
curr_dir = Path(__file__).absolute().parent.__str__()
# curr_dir = Path(__file__).parent.__str__()


def read_requirements_file(*args):
    ''' paths, filename'''
    # filepath = Path(*args)
    print(*args)
    filepath = os.path.join(*args)

    try:
        # lines = filepath.read_text('utf-8').split('\n')
        # lines = open(filepath.__str__(), encoding='utf-8', errors='ignore')
        lines = open(filepath, encoding='utf-8', errors='ignore')
    except Exception as exc:
        print(exc)
        return None

    # strip '#'
    lines = [elm.split('#', 1)[0].strip() for elm in lines]

    # remove empty lines
    return filter(None, lines)

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


# _ = open(f'{dir_name}/__init__.py').read()
_ = Path(f'{dir_name}/__init__.py').read_text(encoding='utf-8')
version, *_ = re.findall(r"__version__\W*=\W*'([^']+)'", _)
targz = 'v_' + version.replace('.', '') + '.tar.gz'
# install_requires = [*read_requirements_file(curr_dir, 'requirements.txt')]  # noqa
# install_requires = []
# requriements =

# does not work
# parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())
# install_requires = [str(requirement.req) for requirement in requriements]

# install_requires = [
    # 'requests',
    # 'aiohttp',
    # 'httpx',
    # 'multidict',
    # 'async_timeout',
    # 'html2text',
    # 'loguru',
    # 'tqdm',
    # 'pyperclip',
# ]

install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
# reqs = [str(ir.req) for ir in install_reqs]

README_rst = f'{curr_dir}/README.md'
long_description = open(README_rst, encoding='utf-8').read() if Path(README_rst).exists() else ''

setup(
    name=name,
    packages=find_packages(),
    # packages=['simple_pp'],
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['machine translation', 'free', 'scraping', ],
    author="mikeee",
    url=f'http://github.com/ffreemt/{name}',
    download_url='https://github.com/ffreemt/yeekit-tr-free/archive/' + targz,
    # install_requires=install_requires,
    install_requires=install_reqs,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
)
