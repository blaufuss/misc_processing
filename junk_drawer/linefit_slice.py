#!/usr/bin/env python

"""
It's got what plants crave. It's got electrolytes.
"""

import sys, os, glob, time
from os.path import expandvars

from icecube import icetray, dataclasses, dataio
import numpy as np

print 'start',time.asctime()

indir = sys.argv[1]
print 'InFile: ', indir
infiles = indir
print infiles

outfile = sys.argv[2]
print 'out: ', outfile

##print infiles


lf_events=[]

src = dataio.I3File(indir)

while src.more():
    frame=src.pop_physics()
    if 'PoleMuonLinefit' in frame:
        lf = frame['PoleMuonLinefit']
        qf = frame['QFilterMask']
        if qf['MuonFilter_13'].prescale_passed:
            muonfilt = True
        else:
            muonfilt = False

        if qf['VEF_13'].prescale_passed:
            veffilt = True
        else:
            veffilt = False
            
        #print lf.dir.azimuth, lf.dir.zenith, lf.fit_status
        this_ev = dict(
            azi=lf.dir.azimuth,
            zen=lf.dir.zenith,
            fitstat=lf.fit_status_string,
            mufilt = muonfilt,
            veffilt = veffilt
            )
        if lf.fit_status == dataclasses.I3Particle.OK:
            lf_events.append(this_ev)
        else:
            
            print 'BAD FIT!'
            
#dt=np.dtype([('fitstat',np.str),('azi',np.float),('zen',np.float)])
#lf_values = [tuple(each.values()) for each in lf_events]
#print lf_values
#array = np.array(lf_values,dtype=dt)
names=['azi','zen','fitstat','mufilt','veffilt']
formats=['f8','f8','S8', 'b', 'b']
dtype = dict(names=names, formats=formats)
values = []
for lf_ev in lf_events:
    value = tuple(lf_ev[name] for name in names)
    values.append(value)
array = np.array(values, dtype=dtype)

print array
np.save(outfile,array)
