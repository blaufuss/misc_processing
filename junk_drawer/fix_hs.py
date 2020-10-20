#!/usr/bin/env python

from I3Tray import *

from icecube import icetray, dataclasses, dataio

files = ['Run00119946.i3.bz2']

tray = I3Tray()

tray.Add(dataio.I3Reader, "reader", filenamelist = files)

def fix_hits(frame):
    if frame.Has('SplitInIcePulses'):
        hit2 = dataclasses.I3RecoPulseSeriesMap.from_frame(frame, 'SplitInIcePulses')
        frame['RealSplitInIcePulses'] = hit2



tray.Add(fix_hits,'fixer')
tray.AddModule( "I3Writer", "EventWriter", filename='test.i3')
tray.Execute()

