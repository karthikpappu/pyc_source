"""Setup configuration."""
import setuptools


with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="addonupdater",
    version="0.1.2",
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="",
    long_description=LONG,
    install_requires=['click', 'PyGithub>=1.43.5', 'repoupdater==0.2.3'],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/addonupdater",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'addonupdater = addonupdater.cli:cli'
        ]
    }
)
