# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/buty_phyl/scripts/OTU.filter.py
# Compiled at: 2019-04-12 20:57:52
# Size of source mod 2**32: 3694 bytes
import os
from Bio import SeqIO
import argparse, glob, pandas as pd, numpy as np
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-t', help='file name of your otu_table',
  type=str,
  default='a.otu.table',
  metavar='a.otu.table')
parser.add_argument('-s', help='file name of your otu_seq',
  type=str,
  default='a.otu.fasta',
  metavar='a.otu.fasta')
parser.add_argument('-r', help='results_dir',
  type=str,
  default='Filtered_OTU',
  metavar='Filtered_OTU')
parser.add_argument('-top', help='number of top OTUs',
  type=int,
  default=5000,
  metavar=5000)
args = parser.parse_args()
try:
    os.mkdir(args.r)
except OSError:
    pass

def Maxabu(Abus):
    Abumax = 0
    for number in Abus:
        Abumax = max(Abumax, int(number.replace('\r', '').replace('\n', '')))

    return Abumax


def biomTOcsv(otutablefile):
    os.system('biom convert -i ' + otutablefile + ' -o ' + otutablefile + '.otu_table.temp.txt --to-tsv')
    os.system('sed 1d ' + otutablefile + '.otu_table.temp.txt > ' + otutablefile + '.otu_table.txt')
    os.system('rm -rf ' + otutablefile + '.otu_table.temp.txt')
    return otutablefile + '.otu_table.txt'


def Tableinput(otutablefile, topnumber):
    filenames, fileextensions = os.path.splitext(otutablefile)
    if fileextensions == '.biom':
        otutablefile = biomTOcsv(otutablefile)
    OTUtable = dict()
    OTUtop = []
    rootofutb, otutable = os.path.split(otutablefile)
    OTU_table = pd.read_csv(otutablefile, sep='\t', index_col=0)
    OTU_table_new = OTU_table.div(OTU_table.sum(axis=0, numeric_only=True), axis=1)
    OTU_table_new.to_csv((os.path.join(args.r, otutable + '.abu.table')), sep='\t', header=True)
    Abus = OTU_table_new.max(axis=1, numeric_only=True).tolist()
    i = 0
    for OTUs in OTU_table_new.index:
        OTUtable.setdefault(OTUs, Abus[i])
        i += 1

    Abus.sort(reverse=True)
    f1 = open(os.path.join(args.r, otutable + '.max.abu'), 'w')
    for OTUs in OTUtable:
        try:
            if OTUtable[OTUs] >= Abus[(topnumber - 1)]:
                f1.write(str(OTUs) + '\t' + str(OTUtable[OTUs]) + '\n')
                OTUtop.append(str(OTUs))
        except IndexError:
            f1.write(str(OTUs) + '\t' + str(OTUtable[OTUs]) + '\n')
            OTUtop.append(str(OTUs))

    f1.close()
    return OTUtop


def Tableoutput(OTUtop, otuseqfile):
    rootofus, otuseq = os.path.split(otuseqfile)
    f1 = open(os.path.join(args.r, otuseq + '.filter'), 'w')
    Write = 0
    for record in SeqIO.parse(open(otuseqfile, 'r'), 'fasta'):
        if str(record.id) in OTUtop:
            Write = 1
            f1.write('>' + str(record.id) + '\n' + str(str(record.seq)) + '\n')

    f1.close()
    if Write == 0:
        print('WRANING: please make sure the OTU IDs/names in OTU table and OTU seqs are the same!!!\n')
        print('If you see this warning, please check your input files, delete the result folder and re-run the scripts.')


Tableoutput(Tableinput(args.t, args.top), args.s)