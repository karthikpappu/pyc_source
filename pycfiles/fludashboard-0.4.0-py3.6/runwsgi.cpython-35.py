# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /storage/Marcelo/codes/FluVigilanciaBR/fludashboard/fludashboard/runwsgi.py
# Compiled at: 2017-10-24 05:01:50
# Size of source mod 2**32: 189 bytes
import os
if __name__ == '__main__':
    path_root = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_root, 'runwsgi.sh')
    os.system('bash %s' % path_file)