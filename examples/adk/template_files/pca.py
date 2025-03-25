from prody import *
import numpy as np
import matplotlib.pyplot as plt

spike = parsePDB("top.pdb")

dcd = parseDCD("ens_aligned.dcd")
dcd.setAtoms(spike)
dcd.setCoords(spike)
ens = Ensemble(dcd)
ens.iterpose()

pca = PCA("ADK aANM")
pca.buildCovariance(ens)
pca.calcModes()

num_confs = calcProjection(ens, pca[0]).shape[0]

pca_coords = []

for i in np.arange(0,NPCS):
    pca_coords.append(calcProjection(ens, pca[i]))

np.save("center_coords_pca.npy", np.column_stack(pca_coords).reshape(num_confs,-1))
