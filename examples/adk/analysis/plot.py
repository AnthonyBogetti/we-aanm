import wedap
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16, 'axes.linewidth': 1.5, 'figure.figsize': (5,5)})

data_options = {"h5" : "west.h5",
                "Xname" : "nmp",
                "Yname" : "lid",
#                "Xindex" : 0,
#                "Yindex" : 0,
                "data_type" : "average",
#                "p_max" : 10,
                "bins" : 50,
                "cbar_label" : "-ln(P)",
                "xlabel" : "nmp-core angle",
                "ylabel" : "lid-core angle",
                "xlim" : (40,85),
                "ylim" : (90,165),
#                "cmap" : "jet_r",
                }


plot = wedap.H5_Plot(**data_options)
plot.plot()

Xc = np.loadtxt("../centers/disang.dat", skiprows=1, usecols=1)
Yc = np.loadtxt("../centers/disang.dat", skiprows=1, usecols=2)

#Xr1 = np.loadtxt("reppath1.dat", skiprows=1, usecols=1)
#Yr1 = np.loadtxt("reppath1.dat", skiprows=1, usecols=2)
#
#Xr2 = np.loadtxt("reppath2.dat", skiprows=1, usecols=1)
#Yr2 = np.loadtxt("reppath2.dat", skiprows=1, usecols=2)

plt.scatter(Xc, Yc, color="grey", marker="o", s=100, zorder=3)
#plt.plot(Xr1[::2], Yr1[::2], color="red", linewidth=1.5, zorder=3)
#plt.plot(Xr2[::2], Yr2[::2], color="dodgerblue", linewidth=1.5, zorder=3)

plt.savefig("hist.pdf")
