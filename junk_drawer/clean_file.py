#!/usr/bin/env python

"""
It's got what plants crave. It's got electrolytes.
"""

import sys, os, glob, time
from os.path import expandvars

from icecube import icetray, dataclasses, dataio
import I3Tray

print('start',time.asctime())

infile = sys.argv[1]
print('Infile: ',infile)
outfile = sys.argv[2]
print('Outfile: ',outfile)

tray = I3Tray.I3Tray()


tray.AddModule("I3Reader", "reader", filenameList=[infile])
tray.AddModule("I3Writer","wrat",filename = outfile)
tray.AddModule("TrashCan", "YesWeCan")

tray.Execute()
tray.Finish()
print('end',time.asctime())

