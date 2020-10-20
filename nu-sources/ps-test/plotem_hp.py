#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.backends.backend_agg

import healpy as hp

NSIDE = 32

dat = np.load("./IC86_exp_all.npy")
#ra = dat["ra"]*180/np.pi - 180.0
#dec = dat["dec"]*180/np.pi

skymap = np.zeros(hp.nside2npix(NSIDE))

#bin the data
for ev in dat:
    if np.abs(ev["dec"]) < 85*np.pi/180.0:
        # shift dec to 0-180 instead of -90,90
        binnum = hp.ang2pix(NSIDE, (ev["dec"]+np.pi/2.0), ev["ra"])
        #print binnum
        skymap[binnum] += 1


hp.mollview(skymap, title="I3 IC86 2011 skymap")
