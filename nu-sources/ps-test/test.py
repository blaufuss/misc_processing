import numpy as np
import pylab 
def detectorWeight(declination):
	dat = np.load("./all_mc.npy")
	energy= []
	area = []
	Ebins=60
	decBins = [30]
	eventsByBin = []
	index = -1
	for i in decBins:
		index += -1
		cos_cent = i   #degrees
		cos_min = np.cos((cos_cent + 5.0)*np.pi/180.0)
		cos_max = np.cos((cos_cent - 5.0)*np.pi/180.0)
		SolidAngle=2*np.pi*(cos_max - cos_min)

		#hardcoded from files used
		NumberFiles = 12*1000
		NEvents=dat["NEvents"][0]*NumberFiles

		MinEnergyLog=dat["MinLogE"][0]
		MaxEnergyLog=dat["MaxLogE"][0]
		DeltaLogE=(MaxEnergyLog-MinEnergyLog)/Ebins

		for ev in dat:
			if np.cos(ev["PrimZenith"])>cos_min and np.cos(ev["PrimZenith"])<cos_max:
                                print ev["PrimZenith"]
				energy.append(np.log10(ev["PrimEnergy"]))
				this_event = (ev["OneWeight"]*1e-4)/(ev["PrimEnergy"]*SolidAngle*NEvents*DeltaLogE*np.log(10))
				area.append(this_event)

                print len(area), len(energy)
		eff_area, logE, junk = pylab.hist(energy, bins=Ebins, weights=area, histtype="step", color='red')
                print eff_area
                print logE
		flux_bin = []
		lastbin = 0
		logE_centers = []
		bin_widths = []
                count = 0
		for Ebin in logE:
                        count = count +1
                        print lastbin,Ebin,count
			if lastbin == 0:
				lastbin = Ebin
			else:
				logE_centers.append((Ebin + lastbin)/2)
				bin_widths.append(10**Ebin - 10**lastbin)
				lastbin = Ebin
                print len(bin_widths)
		for Ebin in logE_centers:
			this_bin = (1e-8) * ((10**Ebin)**(-2))  *1e4 #* 2 * np.pi
			flux_bin.append(this_bin)

		flux_bin_arr = np.array(flux_bin)
		print len(flux_bin_arr), len(eff_area), len(bin_widths)
		ev_yr_en = flux_bin_arr * eff_area * bin_widths * 86400*365
		eventsByBin[index] = sum(ev_yr_en)

detectorWeight(100)
