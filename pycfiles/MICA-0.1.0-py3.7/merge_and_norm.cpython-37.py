# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/MICA/bin/merge_and_norm.py
# Compiled at: 2019-10-04 13:04:58
# Size of source mod 2**32: 1568 bytes
import argparse
from MICA.bin import utils

def main():
    """Handles arguments and calls the driver function"""
    head_description = 'Merges a set of matrices into one'
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter), description=head_description)
    parser.add_argument('-i', '--mi-slices', nargs='+', metavar='STR', required=True, help='List of matrices')
    parser.add_argument('-o', '--proj-name', metavar='STR', required=True, help='Project name used for previous steps')
    parser.add_argument('-m', '--metric', metavar='STR', required=True, help='Metric used in calculation')
    args = parser.parse_args()
    merge_and_norm(args.mi_slices, args.proj_name, args.metric.lower())


def merge_and_norm(mat_files, project_name, method):
    """Merges matrices, and normalizes numeric data when distance metric is mutual information.

    Calls on utility functions to merge distance metrics that were calculated in between slices.
    Normalizes the resulting merged matrix when the data that was originally calculated was a
    measure of mutual information.

    Args:
        mat_files  (str[]): list of sliced files comparing slices
        project_name (str): name of project/original output name
        method       (str): metric used for calculating distance
    """
    utils.merge_dist_mats(mat_files, project_name, method)
    dist_file = project_name + '_dist.h5'
    if method == 'mi':
        utils.norm_mi_mat(dist_file, project_name)


if __name__ == '__main__':
    main()