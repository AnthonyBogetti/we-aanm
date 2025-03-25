from prody import *

c = parsePDB("PDB1", subset='ca')
o = parsePDB("PDB2", subset='ca')
ens = calcAdaptiveANM(o, c, 100, f=0.1, mode=AANM_ALTERNATING)
writeDCD("ens.dcd", ens)
