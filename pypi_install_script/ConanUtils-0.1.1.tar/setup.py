from distutils.core import setup

setup(
    name='ConanUtils',
    version='0.1.1',
    packages=['conanutils', 'conanutils.common'],
    package_data={'conanutils': ['templates/*.template']},
    license='MIT',
    long_description="additional Toolbox for conan.io C/C++ package manager",
    url="https://github.com/Av3m/conantools",
    author="Av3m",
    author_email="7688354+Av3m@users.noreply.github.com",
    download_url="https://github.com/Av3m/conantools/archive/0.1.0.zip",
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[],
    keywords=['conan', 'packages', 'uploader', 'config']
)
