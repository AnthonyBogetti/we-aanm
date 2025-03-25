import numpy
  
def load_auxdata(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/nmp']
    auxgroup2 = iter_group['auxdata/lid']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset
