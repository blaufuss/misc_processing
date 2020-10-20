#! /usr/bin/python

import numpy as np
import pylab

energy= []
area = []

dat = np.load("all_mc.npy")

Ebins=60
cos_min = -0.2
cos_max = -0.1
SolidAngle=2*np.pi*(cos_max - cos_min)
print "Cos(zen) range: [%f: %f]"%(cos_min,cos_max)

#hardcoded from files used
NumberFiles = 12*1000
NEvents=dat["NEvents"][0]*NumberFiles

MinEnergyLog=dat["MinLogE"][0]
MaxEnergyLog=dat["MaxLogE"][0]
DeltaLogE=(MaxEnergyLog-MinEnergyLog)/Ebins


for ev in dat:
    if np.cos(ev["PrimZenith"])>cos_min and np.cos(ev["PrimZenith"])<cos_max:

        energy.append(np.log10(ev["PrimEnergy"]))
        this_event = (ev["OneWeight"]*1e-4)/(ev["PrimEnergy"]*SolidAngle*NEvents*DeltaLogE*np.log(10))
        area.append(this_event)

pylab.clf()

eff_area, logE, junk = pylab.hist(energy, bins=Ebins, weights=area, histtype="step",
                                  color='red')
pylab.ylabel("Aeff [m^2]")
pylab.xlabel("log10(E/Gev)")
pylab.semilogy()
pylab.ylim(0.01,1000)
pylab.text(4.0, 0.05, "Cos(zen):[%f,%f]"%(cos_min,cos_max))

print eff_area
print logE

pylab.show()
