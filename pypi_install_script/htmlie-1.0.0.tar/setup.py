from setuptools import setup, find_packages


setup(
    name="htmlie",
    version="1.0.0",
    description="HTMLie is a command line HTML Parser.",
    url="https://github.com/gaojiuli/htmlie",
    author="Jiuli Gao",
    author_email="gaojiuli@gmail.com",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["html = htmlie:main"]},
    install_requires=("pyquery", "httpie"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development",
        "Topic :: System :: Networking",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
