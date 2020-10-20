#!/usr/bin/env python
from I3Tray import *

from os.path import expandvars
from optparse import OptionParser
import numpy
import pylab
from icecube import icetray, dataclasses, dataio

###
#  Use the optparse module to parse options from the command line
###
parser = OptionParser()

parser.add_option("-i","--i3file",
                  dest="i3file", default=expandvars("$I3_PORTS/test-data/sim/GCD.i3.gz"),
                  help="I3File which contains the GCD.")

parser.add_option("-p","--plot_path",
                  dest="plot_path", default=expandvars("$HOME/"),
                  help="Path to store the plots.")

(options, args) = parser.parse_args()

###
# Get the GCD file
###
gcdI3File = dataio.I3File(options.i3file)

###
# Loop over the frames until you find one with the geometry
###
frame = gcdI3File.pop_frame()
while not frame.Has("I3Geometry"): frame = gcdI3File.pop_frame()

###
# Now you have a frame with the geometry in it.
# We want to get the map of I3OMGeo objects because
# these contain the positions of the DOMs
###
omgeomap = frame.Get("I3Geometry").omgeo

###
# Define convenience strings showing the strings that
# were deployed for the various seasons
###
ic2006 = ",29,30,38,39,40,49,50,59,"
ic2007 = ",58,67,66,74,73,65,72,78,48,57,47,46,56,"
ic2008 = ",63,64,55,71,70,76,77,75,69,60,68,61,62,52,44,53,54,45,"
ic2009 = ",2,3,4,5,6,10,11,12,13,17,18,19,20,26,27,28,36,37,"

for element in omgeomap:
    i3omgeo = element.data()
    omkey = element.key()
    
    if(omkey.GetOM() == 1):
        x = i3omgeo.position.X
        y = i3omgeo.position.Y
        string = omkey.GetString()

        if omkey.GetString() == 21 :
            print "string 21 is at (%3.2fm,%3.2fm)" % (x,y)

        c = "black"
        if string == 21 : c = "orange"
        if ic2006.count(","+str(s)+",") : c = "green"
        if ic2007.count(","+str(s)+","): c = "red"
        if ic2008.count(","+str(s)+",") : c = "blue"
        if ic2009.count(","+str(s)+",") : c = "magenta"
        if string < 0 : c = "pink"

        if c == "black" : continue

        if string > 0 :
            pylab.plot([x],[y],marker="o",color=c)
            pylab.text(x + 5*I3Units.m,y + 5*I3Units.m,"%d" % s)
        else:
            pylab.plot([x],[y],marker="o",color=c, markersize = 5)

pylab.xlim(-650*I3Units.m,650*I3Units.m)
pylab.ylim(-650*I3Units.m,650*I3Units.m)

###
# Plot the DeepCore string
###
x = 113.21
y = -60.4
pylab.plot([x],[y],marker="o",color="magenta")
pylab.text(x + 5*I3Units.m,y + 5*I3Units.m,"83")

###
# Now we have the plot.  Let's make it pretty by
# adding titles and save it.
###
pylab.title("IceCube String Positions")
pylab.xlabel("x(m)")
pylab.ylabel("y(m)")
pylab.savefig(options.plot_path + "/string_postions.png")
