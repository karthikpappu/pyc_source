# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/input_preprocess/coords_extract.py
# Compiled at: 2019-09-30 06:40:20
# Size of source mod 2**32: 2528 bytes
import argparse, os
from tqdm import tqdm
import numpy as np
from prody import *
from multiprocessing import Pool
import cluster_drug_discovery.input_preprocess.feature_extraction as fte
import cluster_drug_discovery.input_preprocess.point as pt
from cluster_drug_discovery.methods import kmeans, dbscan, agglomerative

class CoordinatesExtractor(fte.FeatureExtractor):

    def __init__(self, files, residues, cpus):
        self.residues = residues
        self.files = files
        self.cpus = cpus
        fte.FeatureExtractor.__init__(self, files)

    def _retrieve_coords(self):
        print('Retrieve coordinates from pdb files...')
        proc_pool = Pool(self.cpus)
        all_files_coordinates, info_samples = zip(*list(tqdm((proc_pool.imap(self._retrieve_pdb_coords, self.files)), total=(len(self.files)))))
        proc_pool.close()
        proc_pool.join()
        all_files_coordinates = np.array([e for sample in all_files_coordinates for e in sample])
        info_samples = np.array([e for sample in info_samples for e in sample])
        return (all_files_coordinates, info_samples)

    def _retrieve_pdb_coords(self, f):
        all_files_coordinates = []
        info_samples = []
        traj = f[:-4].rsplit('_', 1)[1]
        epoch = os.path.basename(os.path.dirname(f))
        model = 1
        while True:
            try:
                atoms = parsePDB(f, model=model)
            except prody.proteins.pdbfile.PDBParseError:
                break

            coordinates = []
            for res in self.residues:
                residue_specified = atoms.select('resname {}'.format(res))
                for atom in residue_specified:
                    coordinates.extend(atom.getCoords())

            all_files_coordinates.append(coordinates)
            info_samples.append(pt.Point(coordinates, epoch, traj, model))
            model += 1

        return (
         all_files_coordinates, info_samples)


def add_args(parser):
    parser.add_argument('files', nargs='+', help='cluster algorithm to use')
    parser.add_argument('--residues', nargs='+', help='residue name of the ligand to use', default=[])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract coordinate sof ligand along pdb simulation')
    add_args(parser)
    args = parser.parse_args()
    extraction = CoordinatesExtractor(args.files, args.residues)
    X = extraction.retrieve_coords()
    cluster = kmeans.KmeansAlg(X, nclust=3)
    cluster.analyze()