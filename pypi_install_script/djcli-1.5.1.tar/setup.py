from setuptools import setup


setup(
    name='djcli',
    version='1.5.1',
    setup_requires='setupmeta',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/djcli',
    include_package_data=True,
    license='MIT',
    keywords='django cli',
    python_requires='>=3',
    install_requires=['cli2', 'tabulate'],
    extras_require={
        'test': ['django', 'pytest', 'pytest-cov', 'pytest-django'],
    },
    entry_points={
        'console_scripts': [
            'djcli = djcli:console_script',
        ],
    },
)
