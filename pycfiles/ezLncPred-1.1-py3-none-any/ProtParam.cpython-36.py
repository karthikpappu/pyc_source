# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/PredLnc_GFStack/src/get_features_module/ProtParam.py
# Compiled at: 2019-12-04 10:19:56
# Size of source mod 2**32: 1065 bytes
import sys, re
from Bio.Seq import Seq
from .ORF import ExtractORF
from Bio.SeqUtils import ProtParam
import numpy as np

def mRNA_translate(mRNA):
    return Seq(mRNA).translate()


def protein_param(putative_seqprot):
    return (
     putative_seqprot.instability_index(), putative_seqprot.isoelectric_point(), putative_seqprot.gravy(), putative_seqprot.molecular_weight())


def param(seq):
    strinfoAmbiguous = re.compile('X|B|Z|J|U', re.I)
    ptU = re.compile('U', re.I)
    seqRNA = ptU.sub('T', str(seq).strip())
    seqRNA = seqRNA.upper()
    CDS_size1, CDS_integrity, seqCDS = ExtractORF(seqRNA).longest_ORF(start=['ATG'], stop=['TAA', 'TAG', 'TGA'])
    seqprot = mRNA_translate(seqCDS)
    pep_len = len(seqprot.strip('*'))
    newseqprot = strinfoAmbiguous.sub('', str(seqprot))
    protparam_obj = ProtParam.ProteinAnalysis(str(newseqprot.strip('*')))
    if pep_len > 0:
        Instability_index, PI, Gravy, Mw = protein_param(protparam_obj)
        pI_Mw = np.log10(float(Mw) / PI + 1)
    else:
        Instability_index = 0.0
        PI = 0.0
        Gravy = 0.0
        Mw = 0.0
        pI_Mw = 0.0
    return (
     Instability_index, PI, Gravy, Mw, pI_Mw)