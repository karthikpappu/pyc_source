# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:04:23 2020

@author: DELL
"""

from distutils.core import setup
setup(
  name = 'outliers_aditri',         # How you named your package folder (MyLib)
  packages = ['outliers_aditri'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Finding outliers in a dataset in python',   # Give a short description about your library
  author = 'Aditri Sinha',                   # Type in your name
  author_email = 'asinha_be17@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/aditrisinha/outliers_aditri',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['python', 'outliers', 'aditri'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)