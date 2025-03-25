import h5py
import numpy

# this is your main simulation h5 file
westh5 = h5py.File("west.h5", "a")

n_iter = westh5["summary"][:].shape[0]

# loop though all iterations and copy one at a time into the main h5file
for i in range(1,n_iter):
    print("iteration %s"%i)

    # this is the location and name of the new data from your w_crawl h5 file
    nmp_string = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/nmp'
    lid_string = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/lid'

    # this is the destination in the west h5 file to place your new data,
    # you can change the name if you want but make sure to put it in auxdata
    destination_string = 'iterations/iter_'+str(i).zfill(8)+'/pcoord'

    nmp_data = westh5[nmp_string]
    lid_data = westh5[lid_string]
    pcoord_data = westh5[destination_string]


    comb_data = []
    for idx, val in enumerate(nmp_data):
        new_data = numpy.column_stack((val, lid_data[idx]))
        comb_data.append(new_data)

    comb_arr = numpy.array(comb_data)

    del westh5[destination_string]
    dset = westh5.create_dataset(destination_string, data=comb_arr)

# close the files (to avoid data corruption)
westh5.close()
