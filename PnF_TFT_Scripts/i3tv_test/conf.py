#
#  $Id$
#  
#  Copyright (C) 2007
#  Troy D. Straszheim  <troy@icecube.umd.edu>
#  and the IceCube Collaboration <http://www.icecube.wisc.edu>
#  
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#  
import os
import re
from os.path import join, getsize

print "Reading conf.py"

channel_description = "South Pole IceCube Event Viewer Channel"
port = 26227
sleep_seconds = 4
physics_stride = 1

#spool_dir = "/mnt/data/pnflocal2/i3tv/spool"
spool_dir = "/home/blaufuss/i3tv_test/test"
physics_re = "I3TV_PhysicsFiltering.*\\.i3$"

print "Using files from spool_dir: ", spool_dir
def get_next_file():
	for spath, ldir, ffiles in os.walk(spool_dir):
		lfiles = []
		for thefile in ffiles:
			if re.match(physics_re, thefile):
				lfiles.append(thefile)	
		lfiles.sort()
		#print "Path to files :",spath
		#print "Sorted files:",lfiles
		#print "Length of filelist:",len(lfiles)
		file_to_use = spath + "/" + lfiles[-1]
		toremove = lfiles[0:-1]
	#print "to remove:",len(toremove),toremove

	print "Cleaning older files, found ",len(toremove)
	for oldfile in toremove:
		rmcm = "rm " + spath + "/" + oldfile
		#print "will run", rmcm
		os.system(rmcm)
	print "File going to server: ", file_to_use
	return file_to_use 


