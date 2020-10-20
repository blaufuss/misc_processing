#! /usr/bin/env python
import numpy as np
#from matplotlib import pylab, mlab, pyplot
#plt = pyplot

from icecube.realtime_gfu import muon_alerts

import glob
files = glob.glob('SplineMPEfast.details.IC86*.npy')
files.sort()

print files

dat_temp = []
for file in files:
    from_every_file = np.load(file)
    #print len(from_every_file)
    dat_temp.append(from_every_file)
dat = np.concatenate(dat_temp)
print 'Total events:',len(dat)

good_e = []
zen_cut = np.radians(82.)
n_nan = 0 
events = []
for ev in dat:
    if not np.isnan(ev['logTruncated']):
        good_e.append(ev['logTruncated'])

    else:
        n_nan +=1
    cut = muon_alerts.is_alert(zen=ev['zen'],
                               dec=ev['dec'],
                               bdt_up = ev['BDT_Up'],
                               track_len = ev['lengthInDet'],
                               logTruncatedE = ev['logTruncated'],
                               qtot = ev['QtotIC'])
    if (cut['gold'] or cut['bronze']):
        truncated = 10**ev['logTruncated']
        signess = muon_alerts.signalness(ev['zen'], ev['dec'], ev['QtotIC'], truncated)[0]
        yr_rate = muon_alerts.yearly_rate(ev['zen'], ev['dec'], ev['QtotIC'], truncated)[0]
        nu_energy = muon_alerts.neutrino_energy(truncated)
        this_ev = dict(
            gold = cut['gold'],
            bronze = cut['bronze'],
            cos_zen = np.cos(ev['zen']),
            signs = signess,
            rate = yr_rate,
            rate_scale = yr_rate*(28.2/26.2))
        events.append(this_ev)
        if cut['gold']:
            print 'GOLD',cut, ev['dec'],signess, yr_rate, yr_rate*(9.9/7.8), nu_energy
        else:
            print 'BRONZE',cut, ev['dec'],signess, yr_rate, yr_rate*(28.2/26.2), nu_energy

names = ['gold','bronze','cos_zen','signs','rate','rate_scale']
formats = ['b','b','f8','f8','f8','f8']
values = []

for event in events:
    value = tuple(event[name] for name in names)
    values.append(value)
array = np.array(values, dtype = dict(names=names, formats = formats))
print array

np.save('gfu_far_bronze.npy', array)

            
print n_nan
#plt.hist(good_e,bins = 30)


