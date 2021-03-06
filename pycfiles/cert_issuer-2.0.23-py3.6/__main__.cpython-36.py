# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/__main__.py
# Compiled at: 2018-12-05 14:02:34
# Size of source mod 2**32: 544 bytes
import os.path, sys
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if __package__ is None:
    if not hasattr(sys, 'frozen'):
        path = os.path.realpath(os.path.abspath(__file__))
        sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

def cert_issuer_main(args=None):
    from cert_issuer import config
    parsed_config = config.get_config()
    from cert_issuer import issue_certificates
    issue_certificates.main(parsed_config)


if __name__ == '__main__':
    cert_issuer_main()