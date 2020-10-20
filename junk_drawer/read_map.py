import healpy as hp
import numpy as np

fitsFile = 'https://gracedb.ligo.org/api/superevents/S190930t/files/bayestar.fits.gz,0'

probs = hp.read_map(fitsFile)
print(probs)
