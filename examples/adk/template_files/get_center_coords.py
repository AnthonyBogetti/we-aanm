import mdtraj as md
import numpy as np

center_coords = np.zeros((NBINS,NATOMS*3))

traj = md.load("ens.dcd", top="top.pdb")

traj.save_pdb("ens.pdb")

for idx, frame in enumerate(traj):
    sel = frame.topology.select("name CA")
    center_coords[idx] = np.ravel(frame.xyz[:,sel,:])

np.save("centers.npy", center_coords)
