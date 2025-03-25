#!/bin/bash

cp ../west.h5 .
#wedap -h5 west.h5 -dt evolution -X pcoord -Xi 0 --xlabel "nmp-core distance" --xlim 15 40 --bins 10
#wedap -h5 west.h5 -dt evolution -X pcoord -Xi 1 --xlabel "lid-core distance" --xlim 15 40 --bins 10
wedap -h5 west.h5 -dt average -X pcoord -Xi 0 -Y pcoord -Yi 1 --xlabel "nmp-core distance" --ylabel "lid-core distance" --xlim 15 26 --ylim 15 38 --bins 20 20
