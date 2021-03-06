
from setuptools import setup, find_namespace_packages


setup(
    name='qtoggleserver-paradox',
    version='1.3.3',
    description='Control your Paradox alarm with qToggleServer',
    author='Calin Crisan',
    author_email='ccrisan@gmail.com',
    license='Apache 2.0',

    packages=find_namespace_packages(),

    install_requires=[
        'paradox-alarm-interface==2.1.0',
        'pyserial>=3.4',
        'pyserial-asyncio>=0.4',
        'requests'
    ]
)
