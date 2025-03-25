import os
import numpy as np

from westpa import WESTSystem
from westpa.core.binning import VoronoiBinMapper

from rmsd import RMSD

pcoord_dtype = np.float32
centers_file = "/titan/anthony/WE-ECO/adenylate_kinase/enm_validation/we_voronoi_newrmsd/centers/centers.npy"

def dfunc(p, centers):
#    n_atoms = 214
#    n_frames = 6
#    if p.shape[0] > n_atoms*3:
#        d = np.empty((n_frames,centers.shape[0]))
#        p = p.reshape(n_frames,n_atoms*3)
#        for idx, i in enumerate(p):
#            d_frame = np.empty((centers.shape[0]))                                      
#            for idx2, c in enumerate(centers):
#                aligned_i, T = superpose(i.reshape(n_atoms,3), c.reshape(n_atoms,3))
#                d_frame[idx2] = calcRMSD(aligned_i, c.reshape(n_atoms,3))
#            d[idx] = d_frame
#    else:
#        # then we are initializing...
#        d = np.empty((centers.shape[0]))
#        for idx, c in enumerate(centers):
#            d[idx] = RMSD(p.reshape(n_atoms,3), c.reshape(n_atoms,3))*10
#
#    return d.astype(pcoord_dtype)
    return 0

class System(WESTSystem):

    def initialize(self):

        rc = self.rc.config['west', 'system']

        self.pcoord_ndim = 214*3
        self.pcoord_len = 11
        self.pcoord_dtype = pcoord_dtype
        self.target_count = rc.get('target_count')
        self.nbins = rc.get('nbins')

        centers = np.load(centers_file)

        self.bin_mapper = VoronoiBinMapper(dfunc, centers)
        self.bin_target_counts = np.zeros((self.bin_mapper.nbins,), dtype=np.int_)
        self.bin_target_counts[...] = self.target_count
