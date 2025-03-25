import os
import math
import numpy as np

from westpa import WESTSystem
from westpa.core.binning import VoronoiBinMapper

from prody import *

pcoord_dtype = np.float32
centers_file = "WSR/centers/center_coords_pca.npy"

def dfunc(p, centers):
    n_frames = NFRAMES
    if p.shape[0] == n_frames:
        # it's a run...
        d = np.empty((n_frames,centers.shape[0]))
        for idx, i in enumerate(p):
            d_frame = np.empty((centers.shape[0]))                                      
            for idx2, c in enumerate(centers):
                d_frame[idx2] = math.dist(i,c)
            d[idx] = d_frame
    else:
        # then we are initializing.
        d = np.empty((centers.shape[0]))
        for idx, c in enumerate(centers):
            d[idx] = math.dist(p, c)

    return d.astype(pcoord_dtype)

class System(WESTSystem):

    def initialize(self):

        rc = self.rc.config['west', 'system']

        self.pcoord_ndim = NPCS
        self.pcoord_len = NFRAMES
        self.pcoord_dtype = pcoord_dtype
        self.target_count = rc.get('target_count')
        self.nbins = rc.get('nbins')

        centers = np.load(centers_file)

        self.bin_mapper = VoronoiBinMapper(dfunc, centers)
        self.bin_target_counts = np.zeros((self.bin_mapper.nbins,), dtype=np.int_)
        self.bin_target_counts[...] = self.target_count
