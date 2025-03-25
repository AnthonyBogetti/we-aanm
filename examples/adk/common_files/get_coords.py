import mdtraj as md
import numpy as np
import sys

init = sys.argv[1]

if float(init) > 0:
    print("initializing")
    conf = md.load("bstate.ncrst", top="4ake.prmtop")
    sel = conf.topology.select("name CA")
    print(np.ravel(conf.xyz[:,sel,:].shape))
    np.save("init_coords.npy", np.ravel(conf.xyz[:,sel,:]))
else:
    traj = md.load("comb.dcd", top="4ake.prmtop")
    sel = traj.topology.select("name CA")
    np.save("seg_coords.npy", np.ravel(traj.xyz[:,sel,:]))
