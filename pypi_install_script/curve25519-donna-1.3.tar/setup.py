#! /usr/bin/python

from subprocess import Popen, PIPE
from distutils.core import setup, Extension

version = "1.3" # from git rev 28772f37a4b8a57ab9439b9e79b19f9abee686da

ext_modules = [Extension("curve25519._curve25519",
                         ["python-src/curve25519/curve25519module.c",
                          "curve25519-donna.c"],
                         )]

short_description="Python wrapper for the Curve25519 cryptographic library"
long_description="""\
Curve25519 is a fast elliptic-curve key-agreement protocol, in which two
parties Alice and Bob each generate a (public,private) keypair, exchange
public keys, and can then compute the same shared key. Specifically, Alice
computes F(Aprivate, Bpublic), Bob computes F(Bprivate, Apublic), and both
get the same value (and nobody else can guess that shared value, even if they
know Apublic and Bpublic).

This is a Python wrapper for the portable 'curve25519-donna' implementation
of this algorithm, written by Adam Langley, hosted at
http://code.google.com/p/curve25519-donna/
"""

setup(name="curve25519-donna",
      version=version,
      description=short_description,
      long_description=long_description,
      author="Adam Langley",
      author_email="agl@imperialviolet.org",
      url="http://code.google.com/p/curve25519-donna/",
      maintainer="Brian Warner",
      maintainer_email="warner-pycurve25519-donna@lothar.com",
      license="BSD",
      packages=["curve25519", "curve25519.test"],
      package_dir={"curve25519": "python-src/curve25519"},
      ext_modules=ext_modules,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
      ],
      )
