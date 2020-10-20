#!/usr/bin/env python    

from I3Tray import *
import os.path,os,glob,stat,time

load("libdataio")
load("libphys-services")
load("libpayload-parsing")
load("libdaq-decode")
load("libjebclasses")
load("libI3Db")
load("libicepick")
#load("libtwr-decode")
load("libDOMcalibrator")
load("libFeatureExtractor")
load("liblinefit")
load("libDomTools")
load("liblilliput")
load("libgulliver")
load("libgulliver-modules")


dbserver = "dbs.sps.icecube.southpole.usap.gov"
oldfilename=""

def run_tray(filename,outfile):
	tray=I3Tray()

	tray.AddService("I3ReaderServiceFactory","reader")(
		("Filename",filename),
		("SkipKeys",["I3DST"]),
		("OmitGeometry",True),
		("OmitCalibration",True),
		("OmitStatus",True),
		("SkipMissingDrivingTime",True),
		)

	tray.AddService("I3DbOMKey2MBIDFactory","omkey2mbid")(
	    ("host",dbserver),
	    ("username","i3omdbro"),
	    ("database","I3OmDb"),
	    )

	tray.AddService("I3DbGeometryServiceFactory","geometry")(
	    ("host",dbserver),
	    ("username","i3omdbro"),
	    ("database","I3OmDb"),
	    ("CompleteGeometry",False),
	    )

	tray.AddService("I3DbCalibrationServiceFactory","calibration")(
	    ("host",dbserver),
	    ("username","i3omdbro"),
	    ("database","I3OmDb"),
	    )

	tray.AddService("I3DbDetectorStatusServiceFactory","status")(
	    ("host",dbserver),
	    ("username","i3omdbro"),
	    ("database","I3OmDb"),
	    )

	tray.AddService("I3PayloadParsingEventDecoderFactory","i3eventdecode")(
	    ("cpudataid","Beacon"),
	    ("specialdataid","SyncPulseMap"),
	    ("specialdataoms",[OMKey(0,91),
	                       OMKey(0,92)]),
	    )

	# Services to do Gulliver reconstruction
	tray.AddService("I3SimpleParametrizationFactory","SimpleTrack")(
		( "StepX", 20*I3Units.m ),                                   # ! 20m step size
		( "StepY", 20*I3Units.m ),                                   # ! 20m step size
		( "StepZ", 20*I3Units.m ),                                   # ! 20m step size
		( "StepZenith",  0.1 * I3Units.radian ),                     # ! 0.1 radian step size in zenith
		( "StepAzimuth", 0.2 * I3Units.radian ),                     # ! 0.2 radian step size in azimuth
		( "StepT", 0. ),                                             # Default
		( "StepLinE", 0. ),                                          # Default
		( "StepLogE", 0. ),                                          # Default
		( "StepL", 0. ),                                             # Default
		( "BoundsX", [ -2000 * I3Units.m,                            # ! Set bounds to +-2000m
				2000 * I3Units.m ] ),
		( "BoundsY", [ -2000 * I3Units.m,                            # ! Set bounds to +-2000m
				2000 * I3Units.m] ),
		( "BoundsZ", [ -2000 * I3Units.m,                            # ! Set bounds to +-2000m
				2000 * I3Units.m ] ),
		( "BoundsZenith", [ 0., 0. ] ),                              # Default
		( "BoundsAzimuth", [ 0., 0. ] ),                             # Default
		( "BoundsT", [ 0., 0. ] ),                                   # Default
		( "BoundsE", [ 0., 0. ] ),                                   # Default
		( "BoundsL", [ 0., 0. ] ),                                   # Default
		)

	# Define he gulliver minimization sevice to use
	tray.AddService( "I3GulliverMinuitFactory", "Minuit" )(
		( "Algorithm", "SIMPLEX" ),                                  # Default
		( "Tolerance", 0.1 ),                                        # Default
		( "MaxIterations", 10000 ),                                  # Default
		( "MinuitPrintLevel", -2 ),                                  # Default
		( "MinuitStrategy", 2 ),                                     # Default
		( "FlatnessCheck", True ),                                   # Default
		)

	# Use convoluted pandel as the PDF for the likelihood
	tray.AddService("I3GulliverIPDFPandelFactory","Pandel")(
		( "InputReadout", "TWCleanPulseSeries" ),                    # ! Name of pulses to use
		( "Likelihood", "SPE1st" ),                                  # Default
		( "PEProb", "GConvolute" ),                                  # Default
		( "IceModel", 2 ),                                           # Default
		( "IceFile", "" ),                                           # Default
		( "AbsorptionLength", 98.0 * I3Units.m ),                    # Default
		( "JitterTime", 15.0 * I3Units.ns ),                         # Default
		( "NoiseProbability", 1.0*I3Units.hertz * 10.0*I3Units.ns )  # ! Added a little noise term
		)

	tray.AddService( "I3BasicSeedServiceFactory", "LineFitSeed")(
		( "FirstGuesses", ["IcLinefit"] ),                           # ! Use linefit first guess
		( "InputReadout", "TWCleanPulseSeries" ),                    # ! Use pulses for vertex correction
		( "TimeShiftType", "TFirst" ),                               # ! Use TFirst for vertex correction
		( "SpeedPolice", True ),                                     # Default
		( "MaxMeanTimeResidual", 1000.0 * I3Units.ns ),              # Default
		( "AddAlternatives", "None" )                                # Default
		)

	tray.AddModule("I3Muxer","muxer")

	tray.AddModule("I3IcePickModule<I3FrameObjectFilter>","icepick")(
	    ("discardevents",True),
	    ("displaywarning",True),
	    ("frameobjectkey","I3DAQData"),
	    )

	tray.AddModule("I3FrameBufferDecode","bufferdecode")(
	    ("bufferid","I3DAQData"),
	    )
	tray.AddModule("I3DOMLaunchCleaning","4_BadDomCleaning")( 
 	    ("InIceInput","InIceRawData"), 
 	    ("IceTopInput","IceTopRawData"), 
 	    ("InIceOutput","CleanInIceRawData"), 
	    ("IceTopOutput","CleanIceTopRawData"), 
	    ("FirstLaunchCleaning",True),
 	    ("CleanedKeys",[OMKey(38,59),# Blackberry 
          	          OMKey(6,11)  # Discworld - Meteor DOM
                 	  ]) 
	    )
	tray.AddModule("I3LCCleaning","6_InIceLCClean")(
		("InIceInput","CleanInIceRawData"), 
		("InIceOutput","HLCInIceRawData") 
		)
	tray.AddModule("Delete","delete")(
		("Keys",["InIceRawData"])
		)
	tray.AddModule("Rename","rename")(
		("Keys",["HLCInIceRawData","InIceRawData"])
		)
	 
	tray.AddModule("I3IcePickModule<I3NLaunchFilter>","nlaunchfilter")(
	    ("DiscardEvents",True),
	    ("MinNLaunch",200),
	    )

	tray.AddModule("I3DOMcalibrator","calibrate-inice")(
	    ("FADCTimeOffset",-15)
 	    )
 	
 	tray.AddModule("I3FeatureExtractor","features")(
 	    ("MaxNumHits",0),
 	    ("FastFirstPeak",3),
 	    )
 	
 	tray.AddModule("I3TimeWindowCleaning<I3RecoHit>","timewindow")(
 	    ("InputResponse","InitialHitSeriesReco"),
 	    ("OutputResponse","TWCleanICHits"),
 	    ("TimeWindow",6000)
 	    )

	tray.AddModule("I3TimeWindowCleaning<I3RecoPulse>","timewindwoPulses")(
		("InputResponse","InitialPulseSeriesReco"),
		("OutputResponse","TWCleanPulseSeries"),
		("TimeWindow",6000)
		)
 	
 	tray.AddModule("I3LineFit","ic_linefit_twclean")(
 	    ("Name","IcLinefit"),
 	    ("InputRecoHits","TWCleanICHits")
 	    )

	# Iterative llh fit with on Sobol iteration
	tray.AddModule( "I3IterativeFitter", "TrackLlhFit" ) (
		( "RandomService", "SOBOL" ),                                # ! Name of randomizer service
		( "NIterations", 1 ),                                        # ! Nunmber of iterations
		( "SeedService", "LineFitSeed" ),                            # ! Name of seed service
		( "Parametrization", "SimpleTrack" ),                        # ! Name of track parametrization service
		( "LogLikelihood", "Pandel" ),                               # ! Name of likelihood service
		( "CosZenithRange", [ -1, 1 ] ),                             # ! Default
		( "Minimizer", "Minuit" )                                    # ! Name of minimizer service
		)

	tray.AddModule("Keep","keep")(
	     ("keys",["I3Geometry",
	              'DrivingTime',
	              'I3EventHeader',
		      'CleanInIceRawData',
	              'IceTopRawData',
		      "TWCleanICHits",
		      "IcLinefit",
		      "TrackLlhFit",
	              ])
	     )                             

	tray.AddModule("I3Writer","writer")(
		("Filename",outfile),
                ("streams", ["Geometry", "Physics"]),
		)

	tray.AddModule("TrashCan","can")

	tray.Execute()
	tray.Finish()
	del tray



while 1:
	latesttime=0
	#for file in glob.glob("/mnt/data/pnflocal2/PFRaw_PhysicsTrig_*.meta.xml"):
	for file in glob.glob("/mnt/data/cnv/PFRaw_PhysicsTrig_*.i3"):
		try:
			mtime=os.stat(file)[stat.ST_MTIME]
			if mtime>latesttime:
				latesttime=mtime
				#newfilename=file.replace("meta.xml","i3")
				#os.system("ln "  + file + " /mnt/data/pnflocal2/")
				tmpfile = file
				newfilename = file.replace("cnv","pnflocal2")
		except:
			print "filesystem error"
	if newfilename!=oldfilename:
		os.system("ln "  + tmpfile + " /mnt/data/pnflocal2/")
 		newoutfiletmp = newfilename.replace("PFRaw","I3TV")
 		newoutfile = newoutfiletmp.replace("pnflocal2","pnflocal2/i3tv")
		try:
			run_tray(newfilename,newoutfile)
			os.system("mv " + newoutfile + " /mnt/data/pnflocal2/i3tv/spool/")
			os.system("rm " + newfilename)
		except:
			print "IceTray Encountered an Exeption"
			sys.exit()
		oldfilename=newfilename #don't retry an exception
	else:
		print "no new file found sleeping 30sec"
		time.sleep(30)


