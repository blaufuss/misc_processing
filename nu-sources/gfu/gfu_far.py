###!/usr/bin/env python

##import numpy as np

#dat = np.load("./gfu_2015_exp.npy")
dat = np.load("./gfu_2017_exp.npy")
#total_livetime = 31473046.0
total_livetime = 29652698

# e_edges = [np.percentile(dat["logE"], 0.0),
#          np.percentile(dat["logE"], 10.0),
#          np.percentile(dat["logE"], 20.0),
#          np.percentile(dat["logE"], 30.0),
#          np.percentile(dat["logE"], 40.0),
#          np.percentile(dat["logE"], 50.0),
#          np.percentile(dat["logE"], 60.0),
#          np.percentile(dat["logE"], 70.0),
#          np.percentile(dat["logE"], 80.0),
#          np.percentile(dat["logE"], 90.0)
#]

#e_bins = np.digitize(dat["logE"],e_edges)

zen_bins = 12
e_bins = 100

(counts, xedges, yedges, Image) = plt.hist2d(np.cos(dat["zenith"]),
                                             dat["logE"],
                                             [zen_bins,e_bins])

# lets go over the counts histo and sum all entries with 
esum_counts_f = np.zeros((zen_bins,e_bins))
# flip so that most energetic bins are first
counts_flip = np.fliplr(counts)

for z_bin in range(0,zen_bins):
    #in each zenith bin, make a cumm. sum of all higher E events
    esum_counts_f[z_bin] = np.cumsum(counts_flip[z_bin])

# now flip back to correct E ordering
esum_counts = np.fliplr(esum_counts_f)

#plot em
X, Y = np.meshgrid(xedges[:], yedges[:])

plt.clf()
plt.pcolormesh(X,Y,esum_counts.T/total_livetime)
plt.colorbar()
plt.axis([X.min(),X.max(),Y.min(),Y.max()])
plt.show()

ml_dict = {'livetime': total_livetime,
	   'zen_edges' : xedges,
	   'energy_edges' : yedges,
	   'bin_counts' : esum_counts}

