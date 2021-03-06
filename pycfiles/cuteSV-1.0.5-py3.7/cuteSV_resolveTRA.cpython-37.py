# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuteSV/cuteSV_resolveTRA.py
# Compiled at: 2020-04-17 02:18:29
# Size of source mod 2**32: 6903 bytes
import sys, numpy as np

def resolution_TRA(path, chr_1, chr_2, read_count, overlap_size, max_cluster_bias, bam_path, action, hom, het):
    semi_tra_cluster = list()
    semi_tra_cluster.append([0, 0, '', 'N'])
    candidate_single_SV = list()
    file = open(path, 'r')
    for line in file:
        seq = line.strip('\n').split('\t')
        if seq[1] != chr_1:
            continue
        if seq[4] != chr_2:
            continue
        pos_1 = int(seq[3])
        pos_2 = int(seq[5])
        read_id = seq[6]
        BND_type = seq[2]
        if pos_1 - semi_tra_cluster[(-1)][0] > max_cluster_bias or BND_type != semi_tra_cluster[(-1)][3]:
            if len(semi_tra_cluster) >= read_count:
                generate_semi_tra_cluster(semi_tra_cluster, chr_1, chr_2, read_count, overlap_size, max_cluster_bias, candidate_single_SV, bam_path, action, hom, het)
            semi_tra_cluster = []
            semi_tra_cluster.append([pos_1, pos_2, read_id, BND_type])
        else:
            semi_tra_cluster.append([pos_1, pos_2, read_id, BND_type])

    if len(semi_tra_cluster) >= read_count:
        generate_semi_tra_cluster(semi_tra_cluster, chr_1, chr_2, read_count, overlap_size, max_cluster_bias, candidate_single_SV, bam_path, action, hom, het)
    file.close()
    return candidate_single_SV


def generate_semi_tra_cluster(semi_tra_cluster, chr_1, chr_2, read_count, overlap_size, max_cluster_bias, candidate_single_SV, bam_path, action, hom, het):
    BND_type = semi_tra_cluster[0][3]
    semi_tra_cluster = sorted(semi_tra_cluster, key=(lambda x: x[1]))
    read_tag = dict()
    temp = list()
    last_len = 0
    temp.append([0, 0, set()])
    for element in semi_tra_cluster:
        if element[1] - last_len > max_cluster_bias:
            temp.append([element[0], element[1], {element[2]}])
            last_len = element[1]
        else:
            temp[(-1)][0] += element[0]
            temp[(-1)][1] += element[1]
            temp[(-1)][2].add(element[2])
            last_len = element[1]
        if element[2] not in read_tag:
            read_tag[element[2]] = 0

    if len(read_tag) < read_count:
        return
        temp = sorted(temp, key=(lambda x: -len(x[2])))
        if len(temp[1][2]) >= 0.5 * read_count:
            if len(temp[0][2]) + len(temp[1][2]) >= len(semi_tra_cluster) * overlap_size:
                BND_pos_1 = '%s:%s' % (chr_2, int(temp[0][1] / len(temp[0][2])))
                BND_pos_2 = '%s:%s' % (chr_2, int(temp[1][1] / len(temp[1][2])))
                if BND_type == 'A':
                    TRA_1 = 'N[%s[' % BND_pos_1
                    TRA_2 = 'N[%s[' % BND_pos_2
                else:
                    if BND_type == 'B':
                        TRA_1 = 'N]%s]' % BND_pos_1
                        TRA_2 = 'N]%s]' % BND_pos_2
                    else:
                        if BND_type == 'C':
                            TRA_1 = '[%s[N' % BND_pos_1
                            TRA_2 = '[%s[N' % BND_pos_2
                        else:
                            if BND_type == 'D':
                                TRA_1 = ']%s]N' % BND_pos_1
                                TRA_2 = ']%s]N' % BND_pos_2
                            else:
                                return
                if action:
                    DV, DR, GT = call_gt(bam_path, int(temp[0][0] / len(temp[0][2])), int(temp[0][1] / len(temp[0][2])), chr_1, chr_2, temp[0][2], max_cluster_bias, hom, het)
                else:
                    DR = '.'
                    GT = './.'
                candidate_single_SV.append([chr_1,
                 TRA_1,
                 str(int(temp[0][0] / len(temp[0][2]))),
                 chr_2,
                 str(int(temp[0][1] / len(temp[0][2]))),
                 str(len(temp[0][2])),
                 str(DR),
                 str(GT)])
                if action:
                    DV, DR, GT = call_gt(bam_path, int(temp[1][0] / len(temp[1][2])), int(temp[1][1] / len(temp[1][2])), chr_1, chr_2, temp[1][2], max_cluster_bias, hom, het)
                else:
                    DR = '.'
                    GT = './.'
                candidate_single_SV.append([chr_1,
                 TRA_2,
                 str(int(temp[1][0] / len(temp[1][2]))),
                 chr_2,
                 str(int(temp[1][1] / len(temp[1][2]))),
                 str(len(temp[1][2])),
                 str(DR),
                 str(GT)])
    elif len(temp[0][2]) >= len(semi_tra_cluster) * overlap_size:
        BND_pos = '%s:%s' % (chr_2, int(temp[0][1] / len(temp[0][2])))
        if BND_type == 'A':
            TRA = 'N[%s[' % BND_pos
        else:
            if BND_type == 'B':
                TRA = 'N]%s]' % BND_pos
            else:
                if BND_type == 'C':
                    TRA = '[%s[N' % BND_pos
                else:
                    if BND_type == 'D':
                        TRA = ']%s]N' % BND_pos
                    else:
                        return
        if action:
            DV, DR, GT = call_gt(bam_path, int(temp[0][0] / len(temp[0][2])), int(temp[0][1] / len(temp[0][2])), chr_1, chr_2, temp[0][2], max_cluster_bias, hom, het)
        else:
            DR = '.'
            GT = './.'
        candidate_single_SV.append([chr_1,
         TRA,
         str(int(temp[0][0] / len(temp[0][2]))),
         chr_2,
         str(int(temp[0][1] / len(temp[0][2]))),
         str(len(temp[0][2])),
         str(DR),
         str(GT)])


def run_tra(args):
    return resolution_TRA(*args)


def count_coverage(chr, s, e, f, read_count):
    for i in f.fetch(chr, s, e):
        if i.flag not in (0, 16):
            continue
        if i.reference_start < s and i.reference_end > e:
            read_count.add(i.query_name)


def assign_gt(a, b, hom, het):
    if b == 0:
        return '1/1'
        if a * 1.0 / b < het:
            return '0/0'
    else:
        if a * 1.0 / b >= het:
            if a * 1.0 / b < hom:
                return '0/1'
        if a * 1.0 / b >= hom and a * 1.0 / b < 1.0:
            return '1/1'
    return '1/1'


def call_gt(bam_path, pos_1, pos_2, chr_1, chr_2, read_id_list, max_cluster_bias, hom, het):
    import pysam
    bamfile = pysam.AlignmentFile(bam_path)
    querydata = set()
    search_start = max(int(pos_1) - max_cluster_bias, 0)
    search_end = min(int(pos_1) + max_cluster_bias, bamfile.get_reference_length(chr_1))
    count_coverage(chr_1, search_start, search_end, bamfile, querydata)
    search_start = max(int(pos_2) - max_cluster_bias, 0)
    search_end = min(int(pos_2) + max_cluster_bias, bamfile.get_reference_length(chr_2))
    count_coverage(chr_2, search_start, search_end, bamfile, querydata)
    bamfile.close()
    DR = 0
    for query in querydata:
        if query not in read_id_list:
            DR += 1

    return (
     len(read_id_list), DR, assign_gt(len(read_id_list), DR + len(read_id_list), hom, het))