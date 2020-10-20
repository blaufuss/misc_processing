#! /usr/bin/python

import pylab, numpy

from eff_area_n02_n01 import *

flux_bin = []
lastbin = 0
logE_centers = []
bin_widths = []
for Ebin in energy_bins:
   if lastbin == 0:
      lastbin = Ebin
   else:
      logE_centers.append((Ebin + lastbin)/2)
      bin_widths.append(10**Ebin - 10**lastbin)
      lastbin = Ebin

pylab.clf()
pylab.plot(logE_centers, eff_area, color='blue')
pylab.ylabel("Aeff [m^2]")
pylab.xlabel("log10(E/Gev)")
pylab.semilogy()
pylab.show()

print 'log_centers: ', logE_centers
print 'bin_widths: ', bin_widths
      
print "LogE bins: ", len(logE_centers)

for Ebin in logE_centers:
   print "E bin: ", (10**Ebin)
   this_bin = (1e-8) * ((10**Ebin)**(-2))  *1e4 #* 2 * numpy.pi
   flux_bin.append(this_bin)
   
print flux_bin
print "Flux bins: ", len(flux_bin)

flux_bin_arr = numpy.array(flux_bin)

ev_yr_en = flux_bin_arr * eff_area * bin_widths * 86400*365

print "Total events expect: ", sum(ev_yr_en)
   
pylab.clf()
pylab.plot(logE_centers, ev_yr_en)
pylab.show()
