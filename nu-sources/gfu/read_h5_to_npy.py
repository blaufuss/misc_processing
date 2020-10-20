#!/usr/bin/env python
import tables
import numpy as np
from utils.coords import local2eq
print("IC86")

#hdf = tables.openFile("Data.2015_258_31473046s_gfu.h5")
hdf = tables.openFile("./2017/Data.2015.29652698sec.h5")

f = hdf.root

data = f.OnlineL2_SplineMPE.cols
data2 = f.GFU_BDT_Score_Up.cols

gfu_status = ((data.zenith[:] < np.pi)) #|(data2.value[:] > 0.1))

print("\t\t{0:7.2%} GFU OK".format(
    np.sum(gfu_status, dtype=np.float) / len(gfu_status)))

arr = np.empty((np.sum(gfu_status), ), dtype=[("run", np.int),
                                              ("event", np.int),
                                              ("ra", np.float),
                                              ("dec", np.float),
                                              ("azimuth",np.float),
                                              ("zenith",np.float),
                                              ("logE", np.float),
                                              ("time", np.float)])

arr["run"] = f.I3EventHeader.cols.Run[:][gfu_status]
arr["event"] = f.I3EventHeader.cols.Event[:][gfu_status]
#arr["time"] = f.I3EventHeader.cols.time_start_mjd_day[:][gfu_status] + \
#              f.I3EventHeader.cols.time_start_mjd_sec[:][gfu_status]/(24.0*60.0*60.0)
arr["time"] = f.I3EventHeader.cols.time_start_mjd[:][gfu_status]

data = f.OnlineL2_SplineMPE.cols
zen = data.zenith[:][gfu_status]
phi = data.azimuth[:][gfu_status]
arr["azimuth"] = data.azimuth[:][gfu_status]
arr["zenith"] = data.zenith[:][gfu_status]

arr["ra"], arr["dec"] = local2eq(zen, phi, arr["time"])

data = f.OnlineL2_BestFit_MuEx.cols
arr["logE"] = np.log10(data.energy[:][gfu_status])

hdf.close()

print("\t{0:6d} events".format(len(arr)))
#np.save("gfu_2015_exp.npy", arr)
np.save("gfu_2017_exp.npy", arr)

