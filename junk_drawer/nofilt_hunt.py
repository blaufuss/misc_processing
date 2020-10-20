#!/usr/bin/env python

"""
It's got what plants crave. It's got electrolytes.
"""

import sys, os, glob, time
from os.path import expandvars

from icecube import icetray, dataclasses, dataio
import I3Tray

print 'start',time.asctime()

infiles = glob.glob('/data/exp/IceCube/2016/filtered/PFFilt/0726/PFFilt_PhysicsFiltering_Run00128272*.tar.bz2')
print infiles

day = 'test'
outfile = 'Fail_' + day + '.i3'
print 'out: ', outfile
infiles.sort()

##print infiles

tray = I3Tray.I3Tray()



tray.AddModule("I3Reader", "reader", filenameList=infiles)
def find_filt_fail(frame):
    if frame.Has('UNFILTERED_EVENT'):
        print frame
        return True
    else:
        return False

tray.AddModule(find_filt_fail,"fail",Streams=[icetray.I3Frame.Physics])
tray.AddModule("I3Writer","wrat",filename = outfile)
tray.AddModule("TrashCan", "YesWeCan")

tray.Execute()
tray.Finish()
print 'end',time.asctime()
