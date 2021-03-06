# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aede/simulator.py
# Compiled at: 2017-03-03 04:47:10
import numpy as np, scipy.stats as stats
from functools import partial

class LocalAncestrySimulator(object):

    def __init__(self, gen_map, pipeline, name=None):
        self.name = name
        self.gen_map = gen_map
        self.pipeline = pipeline

    def run(self, *args, **kwargs):
        return self.pipeline(self.gen_map, *args, **kwargs)

    def __str__(self):
        return self.name


def morgan_to_index(pos_morgan, gen_map):
    """
    Convert an array of position in morgans into an array of index thanks to the
    genetic map
    """
    return [ np.searchsorted(gen_map, p) + 1 for p in pos_morgan ]


def jumps_builder(gen_map, lambd):
    max_cm = gen_map[(-1)]
    jumps = np.cumsum(stats.expon.rvs(scale=1 / float(lambd), size=1000))
    return morgan_to_index(jumps[(jumps <= max_cm)], gen_map)


jumps_6 = partial(jumps_builder, lambd=6)

def cluster_builder(jumps, gen_map, a_beta, b_beta):
    alpha = stats.beta.rvs(a_beta, b_beta)
    clusters_by_region = stats.bernoulli.rvs(alpha, size=len(jumps) + 1)
    clusters_by_snp = np.repeat(clusters_by_region, np.ediff1d([0] + jumps + [len(gen_map)]))
    return clusters_by_snp


cluster_default = partial(cluster_builder, a_beta=0.2, b_beta=0.1)

def pipeline_hapmix(gen_map, pop_1, pop_2, jumps_builder, cluster_builder):
    h_adm = []
    jump_adm = []
    snp_cluster_adm = []
    for h_1, h_2 in zip(pop_1, pop_2):
        choices = [h_1, h_2]
        jumps = jumps_builder(gen_map)
        snp_cluster = cluster_builder(jumps, gen_map)
        h_adm.append(np.array([ choices[cluster][j] for j, cluster in enumerate(snp_cluster) ]))
        jumps_pos = np.zeros(len(h_1))
        jumps_pos[jumps] = 1
        jump_adm.append(jumps_pos)
        snp_cluster_adm.append(snp_cluster)

    return (np.array(h_adm), np.array(jump_adm), np.array(snp_cluster_adm))