from setuptools import setup, Extension

setup(name='partialCopy',
      version='0.6.1',
      description='A tool to copy big data to multiple smaller disks ',
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",

      author='Mohamed El-Kalioby',
      author_email='mkalioby@mkalioby.com',
      url='https://github.com/mkalioby/partialCopy',
      packages=['partialCopy'],
      keywords = ['admin','utils', 'notification'],
      data_files=[('/usr/local/bin/',['pcp'])],
	  python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
]
     )
