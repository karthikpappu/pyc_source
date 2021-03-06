# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caspredict/crisprcas.py
# Compiled at: 2020-04-15 17:23:15
# Size of source mod 2**32: 7136 bytes
import logging, re, pandas as pd

class CRISPRCas(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

    def crisprcas(self):

        def dist(x, y, ss, co):
            if co:
                return min(y[0] - x[1], x[0] - y[1])
                if ss > 0:
                    if y[0] > x[1]:
                        return min(y[0] - x[1], x[0] + ss - y[1])
                    return min(x[0] - y[1], y[0] + ss - x[1])
            else:
                if y[0] > x[1]:
                    return y[0] - x[1]
                return x[0] - y[1]

        def dist_ll(x, ll, ss, co):
            return [dist(x, y, ss, co) for y in ll]

        if not self.any_crispr:
            self.crisprsall = []
        if self.any_crispr:
            if not self.any_operon:
                crispr = pd.read_csv((self.out + 'crisprs_all.tab'), sep='\t')
                self.crisprsall = crispr
        if self.any_operon:
            if self.any_crispr:
                logging.info('Connecting Cas operons and CRISPR arrays')
                cas = self.preddf
                cas = cas[(~cas['Prediction'].isin(['False']))]
                cas_1 = cas[(~cas['Prediction'].isin(['False', 'Ambiguous', 'Partial']))]
                crispr = pd.read_csv((self.out + 'crisprs_all.tab'), sep='\t')
                self.crisprsall = crispr
                dicts = []
                for contig in set(cas['Contig']):
                    cas_sub = cas[(cas['Contig'] == contig)]
                    crispr_sub = crispr[(crispr['Contig'] == contig)]
                    for operon in set(cas_sub['Operon']):
                        cas_operon = cas_sub[(cas_sub['Operon'] == operon)]
                        if self.circular:
                            seq_size = self.len_dict[list(cas_operon['Contig'])[0]]
                            circ_op = operon in self.circ_operons
                        else:
                            seq_size = 0
                            circ_op = False
                        dists = dist_ll((int(cas_operon['Start']), int(cas_operon['End'])), zip(crispr_sub['Start'], crispr_sub['End']), seq_size, circ_op)
                        crispr_operon = crispr_sub[[x <= self.crispr_cas_dist for x in dists]]
                        if len(crispr_operon) > 0:
                            outdict = {'Contig':list(cas_operon['Contig'])[0],  'Operon':list(cas_operon['Operon'])[0], 
                             'Operon_Pos':[
                              list(cas_operon['Start'])[0], list(cas_operon['End'])[0]], 
                             'CRISPRs':list(crispr_operon['CRISPR']), 
                             'Distances':[0 if x < 0 else x for x in dists if x <= self.crispr_cas_dist], 
                             'Prediction_Cas':list(cas_operon['Prediction'])[0], 
                             'Prediction_CRISPRs':list(crispr_operon['Prediction']), 
                             'Subtype_Cas':list(cas_operon['Best_type'])[0], 
                             'Subtype_CRISPRs':list(crispr_operon['Subtype'])}
                            dicts.append(outdict)

                else:
                    if len(dicts) > 0:
                        crispr_cas = pd.DataFrame(dicts, columns=(dicts[0].keys()))
                        self.orphan_cas = cas_1[cas_1['Operon'].isin(set(cas_1['Operon']).difference(set(crispr_cas['Operon'])))]
                        self.orphan_crispr = crispr[crispr['CRISPR'].isin(set(crispr['CRISPR']).difference(set([x for x in crispr_cas['CRISPRs'] for x in x])))]
                        pred_lst = []
                        for index, row in crispr_cas.iterrows():
                            Prediction_CRISPR = row['Prediction_CRISPRs'][row['Distances'].index(min(row['Distances']))]
                            Prediction_Cas = row['Prediction_Cas']
                            Best_Cas = row['Subtype_Cas']
                            if Prediction_Cas == Prediction_CRISPR:
                                Prediction = Prediction_Cas
                            else:
                                if Prediction_Cas == 'Ambiguous':
                                    if Prediction_CRISPR in Best_Cas:
                                        Prediction = Prediction_CRISPR
                                    else:
                                        if re.sub('-.*$', '', Prediction_CRISPR) in [re.sub('-.*$', '', x) for x in Best_Cas]:
                                            Prediction = re.sub('-.*$', '', Prediction_CRISPR)
                                        else:
                                            Prediction = 'Unknown'
                                else:
                                    if Prediction_Cas not in ('False', 'Partial'):
                                        Prediction = Prediction_Cas
                                    else:
                                        if Best_Cas == Prediction_CRISPR:
                                            Prediction = Best_Cas + '(Partial)'
                                        else:
                                            if re.sub('-.*$', '', Best_Cas) == re.sub('-.*$', '', Prediction_CRISPR):
                                                Prediction = re.sub('-.*$', '', Prediction_CRISPR) + '(Partial)'
                                            else:
                                                Prediction = 'Unknown'
                            pred_lst.append(Prediction)
                        else:
                            crispr_cas['Prediction'] = pred_lst
                            self.crispr_cas = crispr_cas[['Contig', 'Operon', 'Operon_Pos', 'Prediction', 'CRISPRs', 'Distances', 'Prediction_Cas', 'Prediction_CRISPRs']]

                if len(dicts) > 0:
                    crispr_cas_good = self.crispr_cas[(~self.crispr_cas['Prediction'].str.contains('Unknown|Partial'))]
                    crispr_cas_put = self.crispr_cas[self.crispr_cas['Prediction'].str.contains('Unknown|Partial')]
                    if len(crispr_cas_good) > 0:
                        crispr_cas_good.to_csv((self.out + 'CRISPR_Cas.tab'), sep='\t', index=False)
                    if len(crispr_cas_put) > 0:
                        crispr_cas_put.to_csv((self.out + 'CRISPR_Cas_putative.tab'), sep='\t', index=False)
                    if len(self.orphan_cas) > 0:
                        self.orphan_cas.to_csv((self.out + 'cas_operons_orphan.tab'), sep='\t', index=False)
                    if len(self.orphan_crispr) > 0:
                        self.orphan_crispr.to_csv((self.out + 'crisprs_orphan.tab'), sep='\t', index=False)