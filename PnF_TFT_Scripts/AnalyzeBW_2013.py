#!/usr/bin/env python

#  Updated 2013 filter tuneup. 
#    Major newness:  SuperDST for all events, limited I3DAQData.  No more SDST in filter tags.
#

import sys
import math, glob

from icecube import icetray, dataclasses, dataio,  gulliver
#bring in the filter pairs from shared definition file.
from icecube.filterscripts import filter_globals

# Set the streams to the new list for 2013.
allStreams = filter_globals.filter_streams + filter_globals.sdst_streams
daqdataStreams = []## filter_globals.filters_keeping_allraw
daqdataStreams2 = [] ##['IceTopSTA3_13','IceTopSTA5_13','IceTop_InFill_STA3_13','InIceSMT_IceTopCoincidence_13','EHEFilter_13','FilterMinBias_13']
frtStream = 'FixedRateFilter_13'
sdstStreams = filter_globals.sdst_streams

filelist = glob.glob('/scratch/blaufuss/data/pass3_check/new_wfd/Level2pass3_PhysicsFiltering_Run00127998_Subrun00000000_0000000?.i3.gz')
#filelist = glob.glob('/scratch/blaufuss/data/pass3_check/orig/Level2pass2_IC86.2016_data_Run00127998_Subrun00000000_0000000?.i3.gz')

filelist.sort()
print 'Infiles:',filelist
##
## Day frac that this data represents:
##
#day_frac = 216.0        # Run121585_0-3
day_frac = 62.72       # Run127998_0-09


gzip_frac = 12.00     ## <- just the "filter extras", recos, FilterMasks, etc, derated a bit
                       ## since I measured them in isolation and bzip2 optimal there
dst_gzip_frac = 3.42 ## factor applies to 4 SuperDST objects, right now with I3EventHeader and SuperDST
daq_gzip_frac = 1.53 ## compression ratio of I3DAQData+I3DAQDataTrimmed


fmk = filter_globals.qfilter_mask


#TODO: include regular DST foo
dst_keys = (filter_globals.smalltriggerhierarchy,
            filter_globals.eventheader,
            filter_globals.superdst,
            filter_globals.qfilter_mask,
            filter_globals.dst,
            filter_globals.dstheader,
            'I3DST13Reco_InIceSplit0') ##since it gets remapped from filter_globals.dstreco
daq_keys = (filter_globals.rawdaqdata,
            filter_globals.seatbeltdata)

file_ignore = ()
#file_ignore = ('PFContinuity','DrivingTime','PassedConventional','PassedAnyFilter','PassedKeepSuperDSTOnly', 'I3EventHeader')
#('PassedConventional','PassedAnyFilter', 'PassedSuperDST',
#               filter_globals.qtriggerhierarchy)

filter_passing_events = dict([(name,0) for name in allStreams])
filter_overlap_events = dict([(name,0) for name in allStreams])
filter_passing_bytes = dict([(name,0.0) for name in allStreams])

sec_per_day = 60.0 * 60.0 * 24.0

nframes = 0
file_size = 0
dst_file_size = 0
daq_file_size = 0
for file in filelist:
    openfile = dataio.I3File(file)
    while openfile.more():
      frame = openfile.pop_frame()
      if frame.Stop==icetray.I3Frame.DAQ:
        nframes += 1
        ####
        frame_size = 0
        dst_frame_size = 0
        daq_frame_size = 0
        file_size += frame_size + dst_frame_size + daq_frame_size
        dst_file_size += dst_frame_size/dst_gzip_frac
        frame_accounted = False

        if not nframes%10000:
            print'Mark : ',nframes


        ####
        ####  Take a look at the contents of the std FilterMask
        ####    These are the few events selecting to keep I3DAQData
        # Using the presence of the bool: PassedAnyFilter as tag
        if frame.Has(fmk):
            filt_mask = frame.Get(fmk)
	    #print filt_mask
        else:
            print 'YIKES no QFilterMask'
            continue
        # Quick sping thru mask, see how many filters passing.
        #print "Assign blame"
        npass = 0
        #Check the FRT first
        if filt_mask[frtStream].prescale_passed:
            npass = 1
        else:
            for key in filt_mask.keys():
                if key in daqdataStreams2:
                    if filt_mask[key].prescale_passed:
                        npass += 1
        #print 'Num Filters selected this event:', npass
        if npass > 0:
            bw_charge = float(frame_size)/(npass*gzip_frac) + float(daq_frame_size)/(npass*daq_gzip_frac)
            frame_accounted = True
         # Now loop over the fm again, and assign blame.
        if filt_mask[frtStream].prescale_passed:
            filter_passing_events[frtStream] += 1
            filter_passing_bytes[frtStream] += bw_charge
            print 'FRT event', npass
        for key in filt_mask.keys():
            if key in daqdataStreams2:
                if filt_mask[key].prescale_passed:
                    filter_passing_events[key] += 1
                    filter_passing_bytes[key] += bw_charge
                    if npass > 1:
                        filter_overlap_events[key] +=1

        ####
        ####  Now repeated for Super DST events (majority)
        ####
        # Quick sping thru mask, see how many filters passing.
        npass_dst = 0
        for key in filt_mask.keys():
            if key not in daqdataStreams:
                if key not in sdstStreams:
                    if filt_mask[key].prescale_passed:
                        npass_dst += 1
        #print 'Num Filters selected this event:', npass_dst
        if npass_dst > 0:
            bw_charge = float(frame_size)/(npass_dst*gzip_frac) + float(daq_frame_size)/(npass_dst*daq_gzip_frac)
        # Now loop over the fm again, and assign blame.
        for key in filt_mask.keys():
            if key not in daqdataStreams:
                if key not in sdstStreams:
                    if filt_mask[key].prescale_passed:
                        filter_passing_events[key] += 1
                        if npass_dst > 1:
                            filter_overlap_events[key] +=1
                        if not frame_accounted:
                            filter_passing_bytes[key] += bw_charge

        # now count SDST
        for key in filt_mask.keys():
            if key in sdstStreams:
                if filt_mask[key].prescale_passed:
                    filter_passing_events[key] += 1
                    # No charge for BW


print 'NFrames proceesed = ', nframes
print 'Total file size: ', file_size, ' DST file size:', dst_file_size
print filter_passing_events
print filter_passing_bytes
end_sum =0.0
for key in filter_passing_bytes.keys():
    end_sum += filter_passing_bytes[key]
print 'end sum:', end_sum
##
## Pretty print city
##
for key in filter_passing_events.keys():
    if key in daqdataStreams:
        mykey = key + ' **I3DAQDATA'
    else:
        mykey = key
    this_rate = filter_passing_events[key]/sec_per_day*day_frac
    overlap_rate = filter_overlap_events[key]/sec_per_day*day_frac
    if filter_passing_events[key] > 0:
        overlap_frac = float(filter_overlap_events[key])/float(filter_passing_events[key])*100.00
    else:
        overlap_frac = 0.0
    print 'Rate for ', mykey.ljust(30), ' is %7.2f Hz, with overlap %7.2f Hz ( %7.2f pct) ' %(this_rate,overlap_rate,overlap_frac)

print 'This data is said to be from %7.2f fraction of day.' %day_frac
