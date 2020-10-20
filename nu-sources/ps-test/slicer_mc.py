import tables
import numpy as np

import sys
inputfile = str(sys.argv[1])
outputfile = str(sys.argv[2])
print 'input:', inputfile
print 'output:',outputfile

from utils.coords import local2eq
print("IC86")

deg5 = np.radians(5.)

pull = lambda X: (79. - 86.7 * X + 38.45 * X**2 - 8.673 * X**3
                  + 1.056 * X**4 - 0.0658 * X**5 + 0.00165 * X**6)



hdf = tables.openFile(inputfile)

f = hdf.root

data = f.SplineMPEParaboloidFitParams.cols
pbf_status = ((data.err1[:] >= 0)&(data.err2[:] >= 0))
paraboloid_sigma = np.sqrt(data.err1[:]**2 + data.err2[:]**2) / np.sqrt(2)

print("\t\t{0:7.2%} Paraboloid OK".format(
    np.sum(pbf_status, dtype=np.float) / len(pbf_status)))

arr = np.empty((np.sum(pbf_status), ), dtype=[("MinZen", np.float),
                                              ("MaxZen", np.float),
                                              ("NEvents", np.int),
                                              ("MinLogE", np.float),
                                              ("MaxLogE",np.float),
                                              ("PrimZenith",np.float),
                                              ("PrimEnergy", np.float),
                                              ("OneWeight", np.float)])


data = f.I3MCWeightDict.cols
arr["MinZen"] = data.MinZenith[:][pbf_status]
arr["MaxZen"] = data.MaxZenith[:][pbf_status]
arr["NEvents"] = data.NEvents[:][pbf_status]
arr["MinLogE"] = data.MinEnergyLog[:][pbf_status]
arr["MaxLogE"] = data.MaxEnergyLog[:][pbf_status]
arr["PrimZenith"] = data.PrimaryNeutrinoZenith[:][pbf_status]
arr["PrimEnergy"] = data.PrimaryNeutrinoEnergy[:][pbf_status]
arr["OneWeight"] = data.OneWeight[:][pbf_status]

hdf.close()

print("\t{0:6d} events".format(len(arr)))
np.save(outputfile, arr)

