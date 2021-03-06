from distutils.core import setup
setup(
  name = 'hes',
  packages = ['hes'],
  version = '0.5',
  description = 'A cute calculator',
  author = 'Cagatay CALI',
  author_email = 'cagataycali@icloud.com',
  url = 'https://github.com/cagataycali/hes',
  download_url = 'https://github.com/cagataycali/hes/archive/0.5.tar.gz',
  keywords = ['cute', 'calculator'],
  classifiers = [],
  entry_points='''
        [console_scripts]
        hes=hes:cli
    ''',
)
