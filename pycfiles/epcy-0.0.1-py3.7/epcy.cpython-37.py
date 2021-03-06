# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/epcy.py
# Compiled at: 2020-03-19 17:41:06
# Size of source mod 2**32: 2735 bytes
import argparse
from .argparser.pred import *
from .argparser.pred_rna import *
from .argparser.profile import *
from .argparser.profile_rna import *
from .argparser.qc import *
from .argparser.kal2mat import *
from .argparser.explore import *
from tools.pred import main_pred
from tools.pred_rna import main_pred_rna
from tools.profile import main_profile
from tools.profile_rna import main_profile_rna
from tools.qc import main_qc
from tools.kal2mat import main_kal2mat
from tools.explore import main_explore

def main():
    argparser = argparse.ArgumentParser(prog='PROG')
    subparsers = argparser.add_subparsers(help='sub-command help')
    pred = subparsers.add_parser('pred',
      help='Compute predictive capability of each normalized features (Generic case).')
    pred.set_defaults(func=main_pred)
    get_argparser_pred(pred)
    pred_rna = subparsers.add_parser('pred_rna',
      help='Compute predictive capability of each genes/transcripts expression.')
    pred_rna.set_defaults(func=main_pred_rna)
    get_argparser_pred_rna(pred_rna)
    profile = subparsers.add_parser('profile',
      help='Plot profile of a list of features.')
    profile.set_defaults(func=main_profile)
    get_argparser_profile(profile)
    profile_rna = subparsers.add_parser('profile_rna',
      help='Plot profile of a list of genes/transcipts.')
    profile_rna.set_defaults(func=main_profile_rna)
    get_argparser_profile_rna(profile_rna)
    qc = subparsers.add_parser('qc',
      help='Plot quality conrol gaph.')
    qc.set_defaults(func=main_qc)
    get_argparser_qc(qc)
    kal2mat = subparsers.add_parser('kal2mat',
      help='Build and save matrix expression from kallisto quantification h5 files.')
    kal2mat.set_defaults(func=main_kal2mat)
    get_argparser_kal2mat(kal2mat)
    explore = subparsers.add_parser('explore',
      help='Create figures to explore subgroup_predicted.xls.')
    explore.set_defaults(func=main_explore)
    get_argparser_explore(explore)
    args = argparser.parse_args()
    args.func(args, argparser)