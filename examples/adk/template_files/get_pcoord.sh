#!/bin/bash
set -x
cd $WEST_SIM_ROOT || exit 1

module unload amber

cp $WEST_SIM_ROOT/common_files/4ake.prmtop .
cp $WEST_SIM_ROOT/bstates/bstate.ncrst .

# Calculate pcoord
python $WEST_SIM_ROOT/common_files/get_coords.py 1
cat init_coords.npy > $WEST_PCOORD_RETURN

cp $WEST_SIM_ROOT/common_files/4ake.prmtop $WEST_TRAJECTORY_RETURN
cp $WEST_STRUCT_DATA_REF $WEST_TRAJECTORY_RETURN

cp $WEST_SIM_ROOT/common_files/4ake.prmtop $WEST_RESTART_RETURN
cp $WEST_STRUCT_DATA_REF $WEST_RESTART_RETURN/parent.ncrst

rm 4ake.prmtop bstate.ncrst init_coords.npy
