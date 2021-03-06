from setuptools import setup

setup(
    name='schatz',
    version='1.0.8',
    license='Apache 2.0',
    maintainer='Egor Litvinenko',
    maintainer_email='e.v.litvinenko.1@gmail.com',
    packages=['schatz', 'schatz.adapter'],
    description='Schatz integration package for Python 3',
    install_requires=[
        'requests',
        'SQLAlchemy',
        'schatz-sqlalchemy-clickhouse',
    ]
)