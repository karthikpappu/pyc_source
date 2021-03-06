# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/cli/nas_init.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 2992 bytes
import argparse, os, sys

def add_subparser(subparsers):
    subparser_name = 'nas-init'
    function_to_call = main
    subparser = subparsers.add_parser(subparser_name,
      help='Tool to init a neural architecture search package or a neural architecture search problem folder.')
    subparser.add_argument('--new-pckg', type=str, help='Name of the new neural architecture package to create.')
    subparser.add_argument('--new-pb', type=str, help='Name of the new neural architecture search folder to create.')
    subparser.set_defaults(func=function_to_call)


def main(new_pckg, new_pb, *args, **kwargs):
    pb_files = [
     '__init__.py',
     'problem.py',
     'load_data.py',
     'preprocessing.py',
     'structure.py']
    if new_pckg is not None:
        path = new_pckg
        try:
            os.mkdir(path)
        except OSError:
            print('Creation of the directory %s failed' % path)
        else:
            print('Successfully created the directory %s ' % path)
            with open(os.path.join(path, 'setup.py'), 'w') as (fp):
                fp.write(f"from setuptools import setup\n\nsetup(\n    name='{new_pckg}',\n    packages=['{new_pckg}'],\n    install_requires=[]\n)")
        path = os.path.join(path, new_pckg)
        try:
            os.mkdir(path)
        except OSError:
            print('Creation of the directory %s failed' % path)
        else:
            print('Successfully created the directory %s ' % path)
            with open(os.path.join(path, '__init__.py'), 'w') as (fp):
                pass
            path = '/'.join(path.split('/')[:-1])
            os.chdir(path)
            cmd = f"{sys.executable} {'setup.py'} install"
            os.system(cmd)
        if new_pb is not None:
            os.chdir(new_pckg)
            path = os.path.join(os.getcwd(), new_pb)
            try:
                os.mkdir(path)
            except OSError:
                print('Creation of the directory %s failed' % path)
            else:
                print('Successfully created the directory %s ' % path)
                for fname in pb_files:
                    file_path = os.path.join(path, fname)
                    with open(file_path, 'w') as (fp):
                        print(f"create file: {file_path}")
                        if fname == 'problem.py':
                            fp.write('from deephyper.benchmark import NaProblem\n')

    elif new_pb is not None:
        path = os.path.join(os.getcwd(), new_pb)
        try:
            os.mkdir(path)
        except OSError:
            print('Creation of the directory %s failed' % path)
        else:
            print('Successfully created the directory %s ' % path)
            for fname in pb_files:
                file_path = os.path.join(path, fname)
                with open(file_path, 'w') as (fp):
                    print(f"create file: {file_path}")