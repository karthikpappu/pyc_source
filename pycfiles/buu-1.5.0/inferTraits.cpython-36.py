# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/buty_phyl/scripts/inferTraits.py
# Compiled at: 2018-12-22 17:37:51
# Size of source mod 2**32: 5996 bytes
import argparse, os, random, math, csv, re, sys, pandas as pd, numpy as np
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SearchIO
from Bio import Phylo
from functools import reduce
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-t', help='file name of your tree',
  type=str,
  default='16S.nwk',
  metavar='16S.nwk')
parser.add_argument('-n', help='file name of your tree node names',
  type=str,
  default='16S.format.name',
  metavar='16S.format.name')
parser.add_argument('-rd', help='the reference data of gene traits',
  type=str,
  default='Data.txt',
  metavar='Data.txt')
parser.add_argument('-r', help='results_dir',
  type=str,
  default='Bayers_model',
  metavar='Bayers_model')
parser.add_argument('-tag', help='the name of traits',
  type=str,
  default='',
  metavar='pathogen')
args = parser.parse_args()
try:
    os.mkdir(args.r)
except OSError:
    pass

def read_table(filename, reverse=0):
    table = {}
    f = open(filename, 'r')
    lines = [x.rstrip('\n').split() for x in f]
    if reverse:
        lines = [(v, k) for k, v in lines]
    for k, v in lines:
        table[k] = v

    f.close()
    return table


def assign_internal_names(tree):
    names = {}
    for idx, clade in enumerate(tree.find_clades()):
        if clade.name:
            old_name = clade.name
            clade.name = '%d_%s' % (idx, clade.name)
        else:
            old_name = None
            clade.name = str(idx)
        if old_name:
            names[old_name] = clade.name

    return names


def mismatch(c, chars):
    return len([x for x in chars if c not in x])


def pars(chars):
    if not chars:
        return set()
    else:
        all_chars = set(reduce(lambda a, b: a.union(b), chars))
        scores = [(c, mismatch(c, chars)) for c in all_chars]
        min_score = min(scores, key=(lambda x: x[1]))[1]
        return set([x[0] for x in scores if not x[1] > min_score])


def down_pass(clade, data, anno):
    for x in clade.clades:
        down_pass(x, data, anno)

    if clade.name in anno:
        data[clade.name] = set(anno[clade.name])
        return
    if clade.is_terminal():
        return
    chars = pars([data[x.name] for x in clade.clades if x.name in data])
    if chars:
        data[clade.name] = chars


def up_pass(parent_chars, clade, data, anno):
    if clade.name in anno:
        data[clade.name] = set(anno[clade.name])
        if clade.is_terminal():
            return
    else:
        if clade.name in data:
            data[clade.name] = pars([data[clade.name], parent_chars])
        else:
            data[clade.name] = parent_chars
    for x in clade.clades:
        up_pass(data[clade.name], x, data, anno)


workingDir, filename = os.path.split(args.t)
treefile = args.t
nodenamefile = args.n
annotationfile = args.rd
anno = read_table(annotationfile)
nodename = read_table(nodenamefile, 1)
tree = Phylo.read(treefile, 'newick')
internal_names = assign_internal_names(tree)
anno = dict([(internal_names[nodename[k]], v) for k, v in anno.items()])
data = {}
down_pass(tree.clade, data, anno)
up_pass(set(), tree.clade, data, anno)
leaves = [(x, data[x]) for x in data.keys() if '_' in x]
old_names = dict([(v, k) for k, v in nodename.items()])
new_names = dict([(v, k) for k, v in internal_names.items()])
missing = []
f1 = open(os.path.join(args.r, filename + '.infertraits' + args.tag + '.txt'), 'w')
for k, v in leaves:
    if new_names[k] in old_names:
        if k not in anno:
            f1.write(old_names[new_names[k]] + '\t' + str(np.mean(list(map(int, list(v))))) + '\n')
    else:
        missing += [new_names[k]]

f1.close()