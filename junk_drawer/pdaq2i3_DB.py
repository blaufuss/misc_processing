#!/usr/bin/env python
from I3Tray import *

from os.path import expandvars
from glob import glob

load("libicetray")
load("libdataclasses")
load("libphys-services")
load("libfilecontainer")
load("libjebclasses")
load("libpayload-parsing")
load("libdaq-decode")
load("libdaqreader")
load("libdaqdispatch")
load("libjebserver")
load("libjebcontrol")
load("libI3Db")

workspace = expandvars("$I3_WORK")

mb_id_file = workspace + "/phys-services/resources/mainboard_ids.xml"

tray = I3Tray()

tray.AddService("I3XMLOMKey2MBIDFactory","omkey2mbid")(
   ("infile",mb_id_file),
   )

tray.AddService("I3DummyWatchdogServiceFactory","dog")

tray.AddService("I3PayloadParsingEventDecoderFactory","evtdecode")(
   ("year",2007),
   ("flasherdataid","Flasher"),
   )
file_list = glob("/icework/blaufuss/data/2007/DebugData/Run109675/physics_*")
file_list.sort()
print file_list

tray.AddService("I3DAQEventServiceFactory","daqevents")(
   ("files",file_list),
   )

dbserver = "dbs2.icecube.wisc.edu"

tray.AddService("I3DbGeometryServiceFactory","geometry")(
    ("host",dbserver),
    )

tray.AddService("I3DbCalibrationServiceFactory","calibration")(
    ("host",dbserver),
    )

tray.AddService("I3DbDetectorStatusServiceFactory","status")(
    ("host",dbserver),
    )

	
tray.AddModule("I3JEBMuxer","muxme")

#tray.AddModule("Dump","Dump")

tray.AddModule("I3MultiWriter","write")(
   ("filename","./Run_109675_%04u.i3"),
   ("sizelimit",1000000000),
   )

tray.AddModule("TrashCan","trash")

tray.Execute()
tray.Finish()

