#!/usr/bin/env python

"""
It's got what plants crave. It's got electrolytes.
"""

import sys, os, glob, time
from os.path import expandvars

from icecube import icetray, dataclasses, dataio
import I3Tray

print 'start',time.asctime()

indir = sys.argv[1]
print 'InDir: ', indir
infiles = glob.glob(indir + '/PFFilt_Phy*.i3')
print infiles

filterMask = sys.argv[2]
print 'filterMask: ', filterMask

outfile = 'Found_' + filterMask + '.i3'
print 'out: ', outfile
infiles.sort()

##print infiles

tray = I3Tray.I3Tray()



tray.AddModule("I3Reader", "reader", filenameList=infiles)

def find_filt(frame):
    if frame.Has('QFilterMask'):
        fm = frame["QFilterMask"]
        hese_fr = fm[filterMask]
        #hese_fr = fm["EHEAlertFilter_15"]
        #print "HESE",hese_fr.condition_passed
        if hese_fr.condition_passed:
            print frame
            return True
        else:
            return False
    else:
        return False

tray.AddModule(find_filt,"foinf",Streams=[icetray.I3Frame.Physics])
tray.AddModule("I3Writer","wrat",filename = outfile)
tray.AddModule("TrashCan", "YesWeCan")

tray.Execute()
tray.Finish()
print 'end',time.asctime()

