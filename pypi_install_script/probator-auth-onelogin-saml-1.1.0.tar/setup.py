import os
from codecs import open

import setuptools


path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(path, 'README.md')) as fd:
    long_desc = fd.read()

setuptools.setup(
    name='probator-auth-onelogin-saml',
    use_scm_version=True,
    python_requires='~=3.7',

    entry_points={
        'probator.plugins.auth': [
            'auth_onelogin_saml = probator_auth_onelogin_saml:OneLoginSAMLAuth',
        ],

        'probator.plugins.commands': [
            'import-saml = probator_auth_onelogin_saml.commands:ImportSAML'
        ]
    },

    packages=setuptools.find_packages(),
    setup_requires=['setuptools_scm'],
    install_requires=[
        'probator~=1.0',
        'python3-saml~=1.4',
        'flask',
    ],
    extras_require={
        'dev': [],
        'test': [],
    },

    # Metadata for the project
    description='OneLogin SAML based user authentication',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/bunjiboys/probator-auth-onelogin-saml/',
    author='Asbjorn Kjaer',
    author_email='bunjiboys+probator@gmail.com',
    license='License :: OSI Approved :: Apache Software License',
    classifiers=[
        # Current project status
        'Development Status :: 4 - Beta',

        # Audience
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',

        # License information
        'License :: OSI Approved :: Apache Software License',

        # Supported python versions
        'Programming Language :: Python :: 3.7',

        # Frameworks used
        'Framework :: Flask',
        'Framework :: Sphinx',

        # Supported OS's
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',

        # Extra metadata
        'Environment :: Console',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    keywords='cloud security',
)
