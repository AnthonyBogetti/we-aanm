from prody import *

p1 = parsePDB("PDB1", subset='ca')
p2 = parsePDB("PDB2", subset='ca')
ens = calcAdaptiveANM(p1, p2, 100, mode=AANMMODE)
writeDCD("ens.dcd", ens)
