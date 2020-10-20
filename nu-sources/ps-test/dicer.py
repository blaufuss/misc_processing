#!/usr/bin/env python

import os
import sys
from glob import glob
import numpy as np
import pickle
from I3Tray import *
from icecube import icetray
from icecube import dataclasses 
from icecube import dataio 

#runfile = '/extra/blaufuss/icework/offline/data/viewer/Viewer_Run00127655_Subrun00000000.i3'

runfiles = glob('/extra/blaufuss/icework/offline/data/viewer/Viewer_*i3')
thelist = []

tray = I3Tray()
tray.AddModule("I3Reader",
               FilenameList = runfiles)

def extractor(frame, saver = thelist):
    omgeo = frame["I3Geometry"].omgeo
    #print omgeo
    # get pulses
    if frame.Has("OnlineL2_CleanedMuonPulses"):
        mask = frame["OnlineL2_CleanedMuonPulses"]
        pulsemap = mask.apply(frame)
    else:
        print "NO PULSES"
        return False
    hitsum = []
    for key,pulses in pulsemap:
        omg = omgeo[key]
        #print key, pulses[0].time, omg.position.x
        hitdict = {'string': key.string,
                   'om': key.om,
                   'time': pulses[0].time,
                   'charge': pulses[0].charge,
                   'x': omg.position.x,
                   'y': omg.position.y,
                   'z': omg.position.z}

        # hitsum.append([key.string, 
        #                key.om, 
        #                pulses[0].time,
        #                pulses[0].charge,
        #                omg.position.x,
        #                omg.position.y,
        #                omg.position.z])
        hitsum.append(hitdict)
    print len(pulsemap)
    #print len(hitsum)
    #print hitsum
    saver.append(hitsum)
    
tray.AddModule(extractor,"ex")

tray.Execute()
tray.Finish()

print 'done: ',len(thelist)

#for item in thelist:
#    print 'item:', len(item)

output = open('linefit_data.pkl', 'wb')
pickle.dump(thelist,output)
output.close()
