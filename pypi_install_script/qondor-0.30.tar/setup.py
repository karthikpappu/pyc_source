from setuptools import setup

setup(
    name          = 'qondor',
    version       = '0.30',
    license       = 'BSD 3-Clause License',
    description   = 'Description text',
    url           = 'https://github.com/tklijnsma/qondor.git',
    download_url  = 'https://github.com/tklijnsma/qondor/archive/v0_30.tar.gz',
    author        = 'Thomas Klijnsma',
    author_email  = 'tklijnsm@gmail.com',
    packages      = ['qondor'],
    zip_safe      = False,
    scripts       = [
        'bin/qondor-submit',
        'bin/qondor-sleepuntil'
        ],
    )
