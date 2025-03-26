#!/bin/bash
set -x
cd $WEST_SIM_ROOT || exit 1

module unload amber

cp $WEST_SIM_ROOT/common_files/top.prmtop .
cp $WEST_SIM_ROOT/bstates/bstate_ca_aligned.pdb .

# Calculate pcoord
python $WEST_SIM_ROOT/common_files/get_pcs.py 1
cat pca_coords_init.npy > $WEST_PCOORD_RETURN

cp $WEST_SIM_ROOT/common_files/top.prmtop $WEST_TRAJECTORY_RETURN
cp $WEST_STRUCT_DATA_REF $WEST_TRAJECTORY_RETURN

cp $WEST_SIM_ROOT/common_files/top.prmtop $WEST_RESTART_RETURN
cp $WEST_STRUCT_DATA_REF $WEST_RESTART_RETURN/parent.ncrst

rm top.prmtop bstate.ncrst pca_coords_init.npy
