from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.readlines()

with open('package_readme.rst') as file:
    long_description = file.read()

setup(
    name='stacktask',

    version='0.1.3',
    description='An admin task workflow service for openstack.',
    long_description=long_description,
    url='https://github.com/catalyst/stacktask',
    author='Adrian Turjak',
    author_email='adriant@catalyst.net.nz',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python :: 2.7',
        'Environment :: OpenStack',
    ],

    keywords='openstack keystone users tasks registration workflow',
    packages=find_packages(),
    package_data={
        'stacktask': [
            'api/v*/templates/*.txt',
            'notifications/templates/*.txt',
            'notifications/*/templates/*.txt']},
    install_requires=required,
    entry_points={
        'console_scripts': [
            'stacktask-api = stacktask:management_command',
        ],
    }
)
