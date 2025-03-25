#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

# Link files here
ln -sv $WEST_SIM_ROOT/common_files/4ake.prmtop .

# Change random seed
if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.ncrst ./parent.ncrst
  ln -sv $WEST_PARENT_DATA_REF/seg.pdb ./parent.pdb
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF ./parent.ncrst
  ln -sv $WEST_SIM_ROOT/bstates/bstate.pdb ./parent.pdb
fi

module load amber

while ! grep -q "Final Performance Info" seg.log; do
    # Run the dynamics with OpenMM
    pmemd.cuda -O -i md.in -o seg.log -p 4ake.prmtop -c parent.ncrst -r seg.ncrst -x seg.nc
done

# Autoimage parent+segment trajectory and calculate auxdata while we're at it
COMMAND="         parm 4ake.prmtop\n" 
COMMAND="$COMMAND trajin parent.ncrst\n"
COMMAND="$COMMAND trajin seg.nc\n"
COMMAND="$COMMAND autoimage\n"
COMMAND="$COMMAND angle nmp-core :115-125@CA :90-100@CA :35-55@CA out disang.dat\n"
COMMAND="$COMMAND angle lid-core :179-185@CA :115-125@CA :125-153@CA out disang.dat\n"
COMMAND="$COMMAND trajout comb.dcd\n"
COMMAND="$COMMAND go"

echo -e "$COMMAND" | cpptraj

module unload amber

# Calculate pcoord(s) and save
python $WEST_SIM_ROOT/common_files/get_coords.py 0
cat seg_coords.npy > $WEST_PCOORD_RETURN

# Save auxdata
cat disang.dat | tail -n +2 | awk {'print $2'} > $WEST_NMP_RETURN
cat disang.dat | tail -n +2 | awk {'print $3'} > $WEST_LID_RETURN

# Save segmnet trajectory to HDF5 file
cp 4ake.prmtop $WEST_TRAJECTORY_RETURN
cp seg.nc $WEST_TRAJECTORY_RETURN

cp 4ake.prmtop $WEST_RESTART_RETURN
cp seg.ncrst $WEST_RESTART_RETURN/parent.ncrst

cp seg.log $WEST_LOG_RETURN

# Clean up
rm -f md.in 4ake.prmtop seg.nc comb.nc mdinfo run_coords.npy
