# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/MDconvert/meme2tamo.py
# Compiled at: 2019-04-23 02:08:32
import sys, re, os, math, time, string, tempfile, glob
from TAMO import MotifTools
from TAMO.MD import AlignAce, Meme
from TAMO.util import Arith
from TAMO.seq import Fasta
from TAMO import MotifMetrics
probefile = None
PROBESET = None

def main():
    fsa_fcn = up_and_no_N
    parse()
    for filename in sys.argv[1:]:
        root = filename.split('.')[0]
        ext = filename.split('.')[(-1)]
        tamoname = '%s.t%s' % (root, ext)
        print '#Looking for "%s.*%s"' % (root, ext)
        files = glob.glob('%s.*%s' % (root, ext))
        files = [ f for f in files if f != tamoname ]
        print '%-18s  --> %s' % ((' ').join(files), tamoname)
        sys.stdout.flush()
        memefiles2tamo(files, tamoname)
        try:
            pass
        except:
            print 'Error: Could not convert %s [[ %s ]]' % (
             filename, (' ').join(files))


def parse():
    global PROBESET
    global probefile
    try:
        idx = sys.argv.index('-genome')
        del sys.argv[idx]
        probefile = sys.argv[idx]
        del sys.argv[idx]
        PROBESET = MotifMetrics.ProbeSet(probefile)
        PROBESET.factor = 0.7
    except:
        pass


def memefiles2tamo(files, tamoname):
    global PROBESET
    motifs = []
    for filename in files:
        print '>>>SDFSD>F ', filename
        if re.search('\\.ace$', filename):
            mdobject = AlignAce.AlignAce(filename)
            if not mdobject.fastafile:
                mdobject.fastafile = filename.replace('.ace', '.fsa')
        elif re.search('\\.meme.*$', filename):
            mdobject = Meme.Meme(filename)
            if not mdobject.fastafile:
                mdobject.fastafile = re.sub('\\..\\.meme', '.meme', filename).replace('.meme', '.fsa')
        motifs.extend(mdobject.motifs)

    print mdobject.fastafile
    fsaname = Fasta.find(mdobject.fastafile)
    fsaD = Fasta.load(fsaname)
    probes = fsaD.keys()
    if not probefile:
        PROBESET = MotifMetrics.ProbeSet('YEAST')
    for key, seq in fsaD.items():
        PROBESET.probes[key] = seq

    for motif in motifs:
        if motif.pvalue == 1:
            motif.pvalue = PROBESET.p_value(motif, probes, 'v')
        if motif.church == 1:
            motif.church = PROBESET.church(motif, probes, 'v')
        if motif.E_site == None:
            motif.E_site = PROBESET.E_sitef(motif, probes, 3, 'v')
        if motif.ROC_auc == None:
            motif.ROC_auc = PROBESET.ROC_AUC(motif, probes, 'v')
        if motif.MNCP == None:
            motif.MNCP = PROBESET.MNCP(motif, probes, 'v')
        if motif.frac == None:
            motif.frac = PROBESET.frac(motif, probes, 'v', 0.7)
        if re.search('\\.meme$', filename):
            motif.MAP = -math.log(motif.evalue) / math.log(10)
        if 1 and motif.CRA == None:
            try:
                CRA, Cfrac = PROBESET.cons_ROC_AUC(motif, probes, 'v', tuple='YES')
                motif.CRA = CRA
                motif.Cfrac = Cfrac
            except:
                pass

    if re.search('\\.meme$', filename):
        mdobject.motifs.sort(lambda x, y: cmp(x.pvalue, y.pvalue))
    else:
        mdobject.motifs.sort(lambda x, y: cmp(x.church, y.church))
    MotifTools.save_motifs(motifs, tamoname)
    return


def find_fsa(name, pathhint='../'):
    exists = os.path.exists
    root = re.sub('\\.\\w*$', '', name)
    smroot = re.sub('_.$', '', root)
    if re.search('\\.fsa$', name):
        if exists(name):
            return name
        if exists(pathhint + name):
            return pathhint + name
    else:
        if exists(root + '.fsa'):
            return root + '.fsa'
        if exists(pathhint + root + '.fsa'):
            return pathhint + root + '.fsa'
        if exists(smroot + '.fsa'):
            return smroot + '.fsa'
        if exists(pathhint + smroot + '.fsa'):
            return pathhint + smroot + '.fsa'
    print '## ! Could not find fsa file for %s' % name
    return


def up_and_no_N(name):
    root = re.sub('_N.ace', '', name)
    ans = '../%s.fsa' % root
    return ans


if __name__ == '__main__':
    main()