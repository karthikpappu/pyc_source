from setuptools import setup, find_packages

version = '1.1.0'

tests_require = [
    'ftw.builder',
    'ftw.testing',
    'ftw.testbrowser',
    'plone.app.contenttypes',
    'plone.app.testing',
    'plone.testing',
]

extras_require = {
    'tests': tests_require,
}


setup(
    name='ftw.gopip',
    version=version,
    description='Speed up getObjPositionInParent index in Plone',
    long_description=open('README.rst').read(),

    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='ftw gopip getObjPositionInParent',
    author='4teamwork AG',
    author_email='mailto:info@4teamwork.ch',
    url='https://github.com/4teamwork/ftw.gopip',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ftw'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Plone',
        'ftw.profilehook',
        'plone.api',
        'setuptools',
    ],

    tests_require=tests_require,
    extras_require=extras_require,

    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
