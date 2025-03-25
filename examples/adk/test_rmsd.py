import numpy as np
from prody import *

centers = np.load("centers/centers.npy")

c1 = centers[0].reshape((214,3))
c2 = centers[10].reshape((214,3))

print(calcRMSD(c2, c1))

aligned_c2, T = superpose(c2, c1)

print(T)

print(calcRMSD(aligned_c2, c1))
