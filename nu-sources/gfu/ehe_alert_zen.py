###!/usr/bin/env python

##import numpy as np

#dat = np.load("./gfu_2017_exp.npy")
#dat = np.load("./gfu_2017_exp_te.npy")
#dat = np.load("Online.MuEx.138037352sec.npy")
dat = np.load("Online.TruncatedEnergy.138037352sec.npy")


#zen_bins = 12
#e_bins = 100

#(counts, xedges, yedges, Image) = plt.hist2d(np.cos(dat["zenith"]),
#                                             dat["logE"],
#                                             [zen_bins,e_bins])

min_dec_sin = np.sin(np.deg2rad(0.72))
max_dec_sin = np.sin(np.deg2rad(10.72))

in_bin_energy = []
in_bin_higher = []
for event in dat:
    ev_sindec = np.sin(event["dec"])
    if ((ev_sindec > min_dec_sin) and (ev_sindec < max_dec_sin)):
	 if (event["logE"] > 0):
          	in_bin_energy.append(event["logE"])
          	#if (event["logE"] >= np.log10(53100)):
          	if (event["logE"] >= np.log10(2.3099E5)): #TE
            		in_bin_higher.append(event["logE"])
