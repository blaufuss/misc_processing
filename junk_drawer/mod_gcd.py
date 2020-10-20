#! /usr/bin/python

from icecube import icetray, dataclasses, dataio

oldfile = dataio.I3File("GeoCalibDetectorStatus_IC79.55380_correctedgeo.i3")

frame_g = oldfile.pop_frame()  #G
frame_c = oldfile.pop_frame()  #C
frame_d = oldfile.pop_frame()  #D

geo = frame_g.Get("I3Geometry")
cal = frame_c.Get("I3Calibration")
ds = frame_d.Get("I3DetectorStatus")

geo.startTime = dataclasses.I3Time(2009,0)
print geo.startTime
geo.endTime = dataclasses.I3Time(2012,0)
print geo.endTime

new_file = dataio.I3File("./new_gcd.i3",dataio.I3File.Mode.Writing)
frame_g.Delete("I3Geometry")
frame_g.Put("I3Geometry",geo)

new_file.push(frame_g)


new_file.close()
