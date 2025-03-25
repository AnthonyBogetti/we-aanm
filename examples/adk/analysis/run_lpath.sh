#!/bin/bash

# assign source and target states using the phi/psi angles from WE simulations
#lpath discretize -we -W ./west.h5 --assign-arguments="--config-from-file --scheme ANGLES -W west.h5"

# extract all successful pathways connecting source and target states
# also extract the cluster labels for matching in the next step
lpath extract -we -W ./west.h5 -A ./ANALYSIS/ANGLES/assign.h5 -ss 0 -ts 1 -p -aa --stride 2

# perform matching with condensing repeat pairs
# uses the cluster labels as states through reassign_custom
lpath match -we -op succ_traj/reassigned.pickle --condense 2
