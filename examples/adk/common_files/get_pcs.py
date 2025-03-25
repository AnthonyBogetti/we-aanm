import math
import mdtraj as md
import numpy as np
import sys

from prody import *

init = sys.argv[1]

if float(init) > 0:

    print("initializing")

    top = parsePDB("centers/top.pdb")
    dcd = parseDCD("centers/ens_aligned.dcd")
    dcd.setAtoms(top)
    dcd.setCoords(top)
    ens = Ensemble(dcd)
    ens.iterpose()
    
    pca = PCA("ADK aANM")
    pca.buildCovariance(ens)
    pca.calcModes()

    bs = parsePDB("bstates/bstate_ca_aligned.pdb", sel="ca")

    ens_bs = Ensemble(bs)

    pca_coords = []

    for i in np.arange(0,10):
        pca_coords.append(calcProjection(ens_bs, pca[i]))
    
    np.save("pca_coords_init.npy", np.array(pca_coords).reshape(-1))

elif float(init) < 0:
    centers = np.load("center_coords.npy")
    p = np.load("pca_coords.npy")
    n_frames = 11
    d = np.empty((n_frames))                                         
    for idx, i in enumerate(p):
        d_frame = np.empty((centers.shape[0]))                                      
        for idx2, c in enumerate(centers):
            d_frame[idx2] = math.dist(i,c)
        d[idx] = np.argmin(d_frame)
    np.savetxt("center_id.txt", d)

else:

    top = parsePDB("top.pdb")
    dcd = parseDCD("ens_aligned.dcd")
    dcd.setAtoms(top)
    dcd.setCoords(top)
    ens = Ensemble(dcd)
    ens.iterpose()
    
    pca = PCA("ADK aANM")
    pca.buildCovariance(ens)
    pca.calcModes()

    seg = parsePDB("top.pdb")
    traj = parseDCD("comb_ca_aligned.dcd")
    traj.setAtoms(seg)
    traj.setCoords(seg)
    ens_traj = Ensemble(traj)

    pca_coords = []

    for i in np.arange(0,10):
        pca_coords.append(calcProjection(ens_traj, pca[i]))
    
    np.save("pca_coords.npy", np.array(pca_coords).reshape(-1))
