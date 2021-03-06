from setuptools import setup, find_packages


setup(
    name='xjpath',
    description='JSON like structure data lookup library. A fast alternative to XPath and JsonPath.',
    version='0.2.0',
    author='Volodymyr Burenin',
    author_email='vburenin@gmail.net',
    maintainer='Volodymyr Burenin',
    maintainer_email='vburenin@gmail.com',
    packages=find_packages(".", exclude=("test_*",)),
    install_requires=[],
    tests_require=['nose', 'nosexcover'],
    test_suite='nose.collector',
    extras_require={
        'test': ['nose', 'nosexcover'],
    },
    url='https://github.com/vburenin/xjpath',
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 ],
)
