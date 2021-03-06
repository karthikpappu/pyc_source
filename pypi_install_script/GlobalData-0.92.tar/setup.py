#setup.py

from distutils.core import setup
setup(
  name = 'GlobalData',         # How you named your package folder (MyLib)
  packages = ['GlobalData'],   # Chose the same as "name"
  version = '0.92',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Easy multiprocessing with GlobalData',   # Give a short description about your library
  author = 'Tami Bar',                   # Type in your name
  author_email = 'fire17@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/fire17/GlobalData',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/fire17/GlobalData/archive/v_092.tar.gz',    # I explain this later on
  keywords = ['multiprocessing', 'global', 'dynamic', "data", "communitcation", "subscribe", "events"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'glob3',
          'dill',
          'Pillow',
          'numpy',
          'scipy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6', ####CHECK
  ],
)
