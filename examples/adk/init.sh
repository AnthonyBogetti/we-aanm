#!/bin/bash

read -p "Full (f), partial (p) or clean (c) initialization? " choice

case $choice in
  f) CHOICE=1 && echo "Performing a full initialization." ;;
  p) CHOICE=2 && echo "Performing a partial initialization." ;;
  c) CHOICE=3 && echo "Just cleaning." ;;
  *) echo "Unrecognized selection: $choice" && exit;;
esac

if [[ $CHOICE -eq  1 ]]; then

    read -p "RMSD (r) or PCA (p) for distance? " choice
    
    case $choice in
      r) METHOD=1 && echo "Distance will be from RMSD." ;;
      p) METHOD=2 && echo "Distance will be from PCA." ;;
      *) echo "Unrecognized selection: $choice" && exit;;
    esac

fi

# Set up simulation environment
source env.sh

# Clean up from previous/ failed runs
rm -rf traj_segs seg_logs istates west.h5 voronoi.* west.log west-* west_zmq* __pycache__ get_pcoord.*
mkdir seg_logs traj_segs istates

if [[ $CHOICE -eq 3 ]]; then
    rm -rf system.py west.cfg executable.py centers westpa_scripts/get_pcoord.sh westpa_scripts/runseg.sh
    exit 0
fi	

if [[ $CHOICE -eq  1 ]]; then

    TCOUNT=8
    NFRAMES=11
    NPCS=10 # optional
    WSR=$WEST_SIM_ROOT
    PDB1="1ake.amber.pdb"
    PDB2="4ake.amber.pdb"
    AUX1CMD="angle aux1 :115-125@CA :90-100@CA :35-55@CA out disang.dat"
    AUX2CMD="angle aux2 :179-185@CA :115-125@CA :125-153@CA out disang.dat"
    
    rm -rf system.py west.cfg executable.py centers westpa_scripts/get_pcoord.sh westpa_scripts/runseg.sh
    mkdir centers
    
    sed -e "s/PDB1/${PDB1}/g" -e "s/PDB2/${PDB2}/g" template_files/aanm.py > centers/aanm.py
    cp common_files/$PDB1 centers
    cp common_files/$PDB2 centers
    cd centers
    cat $PDB1 | grep "CA" > top.pdb
    python aanm.py &> aanm.log
    sed -e "s/AUX1CMD/${AUX1CMD}/g" -e "s/AUX2CMD/${AUX2CMD}/g" ../template_files/disang.in > disang.in
    cpptraj -i disang.in
    NBINS=$(tail aanm.log | grep "cycle" | awk {'print $3'})
    NBINS=$((2 * $NBINS + 1))
    NATOMS=$(cat top.pdb | wc | awk {'print $1'})
    
    if [[ $METHOD -eq  1 ]]; then
        sed -e "s/NBINS/${NBINS}/g" -e "s/NATOMS/${NATOMS}/g" ../template_files/get_center_coords.py > get_center_coords.py
        python get_center_coords.py
        cd ../
        sed -e "s/NATOMS/${NATOMS}/g" -e "s/NFRAMES/${NFRAMES}/g" -e "s|WSR|${WSR}|g" template_files/system.py > system.py
	cp template_files/get_coords.py common_files
	cp template_files/get_pcoord.sh westpa_scripts
	sed -e "s/AUX1CMD/${AUX1CMD}/g" -e "s/AUX2CMD/${AUX2CMD}/g" template_files/runseg.sh > westpa_scripts/runseg.sh
	chmod +x westpa_scripts/runseg.sh

    elif [[ $METHOD -eq  2 ]]; then
	cp ../template_files/align.in .
	cpptraj -i align.in
        cat $PDB1 | grep "CA" > pdb1_ca.pdb
        cat $PDB2 | grep "CA" > pdb2_ca.pdb
	sed -e "s/NPCS/${NPCS}/g" ../template_files/pca.py > pca.py
	python pca.py
	cd ../
	sed -e "s/NPCS/${NPCS}/g" -e "s/NFRAMES/${NFRAMES}/g" template_files/get_pcs.py > common_files/get_pcs.py
        sed -e "s/NPCS/${NPCS}/g" -e "s/NFRAMES/${NFRAMES}/g" -e "s|WSR|${WSR}|g" template_files/system_pca.py > system.py
	cp template_files/get_pcoord_pca.sh westpa_scripts/get_pcoord.sh
	sed -e "s/AUX1CMD/${AUX1CMD}/g" -e "s/AUX2CMD/${AUX2CMD}/g" template_files/runseg_pca.sh > westpa_scripts/runseg.sh
	chmod +x westpa_scripts/runseg.sh

    fi

    sed -e "s/NBINS/${NBINS}/g" -e "s/TCOUNT/${TCOUNT}/g" template_files/west.cfg > west.cfg
    cp template_files/executable.py .

fi

# Set pointer to bstate and tstate
BSTATE_ARGS="--bstate-file $WEST_SIM_ROOT/bstates/bstates.txt"
#TSTATE_ARGS="--tstate-file $WEST_SIM_ROOT/tstate.file"

# Run w_init
w_init \
  $BSTATE_ARGS \
  $TSTATE_ARGS \
  --segs-per-state 5 \
  --work-manager=threads "$@"
