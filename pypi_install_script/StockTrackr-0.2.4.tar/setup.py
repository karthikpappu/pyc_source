import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StockTrackr",
    version="0.2.4",
    author="Jack Walsh",
    author_email="jwalshdev@gmail.com",
    description="A basic stock data puller/monitor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwalshdev/StockTrackr",
    download_url="https://github.com/jwalshdev/StockTrackr/archive/0.2.3.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
