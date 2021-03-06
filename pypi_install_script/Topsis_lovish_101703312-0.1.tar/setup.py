from distutils.core import setup
setup(
  name = 'Topsis_lovish_101703312',         # How you named your package folder (MyLib)
  packages = ['Topsis_lovish_101703312'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library has got the implementation of topsis approach',   # Give a short description about your library
  author = 'Lovish Jindal',                   # Type in your name
  author_email = 'lovishjindal2503@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/lovishjindal2503/TOPSIS_project1/tree/master/Topsis_lovish_101703312',   # Provide either the link to your github or to your website
  keywords = ['topsis', 'lovish', '101703312'],   # Keywords that define your package best
  install_requires=[
          'numpy'
      ],
  include_package_data = True,
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