#! /usr/bin/python

import numpy as np
import pylab

energy= []
area = []

dat = np.load("EHE.GFU.outer_join.npy")

Ebins=20
#cos_cent = 30.0   #degrees
#cos_min = np.cos((cos_cent + 5.0)*np.pi/180.0)
#cos_max = np.cos((cos_cent - 5.0)*np.pi/180.0)
sin_min = 0.0
sin_max = 1.0
SolidAngle=2*np.pi*(sin_max - sin_min)
print "Sin(zen) range: [%f: %f]"%(sin_min,sin_max)

#hardcoded from files used
#NumberFiles = 12*1000
#NEvents=dat["NEvents"][0]*NumberFiles
NEvents = 1

#MinEnergyLog=dat["MinLogE"][0]
#MaxEnergyLog=dat["MaxLogE"][0]
MinEnergyLog=2.0
MaxEnergyLog=9.0
DeltaLogE=(MaxEnergyLog-MinEnergyLog)/Ebins


for ev in dat:
    if np.sin(ev["trueDec"])>sin_min and np.sin(ev["trueDec"])<sin_max and ev["tight"]==True:
        #print (ev["PrimZenith"])

        energy.append(np.log10(ev["trueEGFU"]))
        this_event = (ev["owGFU"]*1e-4)/(ev["trueEGFU"]*SolidAngle*NEvents*DeltaLogE*np.log(10))
        area.append(this_event)

print len(area)
pylab.clf()

eff_area, logE, junk = pylab.hist(energy, bins=Ebins, weights=area, histtype="step",
                                  color='red')
pylab.ylabel("Aeff [m^2]")
pylab.xlabel("log10(E/Gev)")
pylab.semilogy()
pylab.ylim(0.01,1000)
#pylab.text(4.0, 0.02, "Cos(zen):[%f,%f]"%(cos_min,cos_max))
pylab.show()

# print len(eff_area)
# print len(logE)

# flux_bin = []
# lastbin = 0
# logE_centers = []
# bin_widths = []
# for Ebin in logE:
#    if lastbin == 0:
#       lastbin = Ebin
#    else:
#       logE_centers.append((Ebin + lastbin)/2)
#       bin_widths.append(10**Ebin - 10**lastbin)
#       lastbin = Ebin

# ## convolve with Spectrum:  F(E) = 1*10E-8  * (E**-2)  [GeV/(cm*s)]
# ##    in PS units:          F(E) = 1*10E-11  * (E**-2)  [TeV/(cm*s)]

# print 'log_centers: ', logE_centers
# print 'bin_widths: ', bin_widths
# for Ebin in logE_centers:
#    print "E bin: ", (10**Ebin)
#    this_bin = (1e-8) * ((10**Ebin)**(-2))  *1e4 #* 2 * np.pi
#    flux_bin.append(this_bin)
   
# print flux_bin
# print "Flux bins: ", len(flux_bin)

# flux_bin_arr = np.array(flux_bin)

# ev_yr_en = flux_bin_arr * eff_area * bin_widths * 86400*365

# print len(eff_area),len(flux_bin_arr),len(bin_widths)
# print "Total events expect: ", sum(ev_yr_en)
   
# pylab.clf()
# pylab.plot(logE_centers, ev_yr_en)
# pylab.ylabel("Number of events/yr")
# pylab.xlabel("log10(E/Gev)")

# pylab.text(4.0, 0.002, "Total at 1e-8 normalization: %f"%(sum(ev_yr_en)))
# pylab.show()



