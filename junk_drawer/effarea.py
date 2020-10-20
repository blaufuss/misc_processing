import pylab
#from loot.plotting import *
import numpy
import tables

#nugen  = tables.openFile( "Level3_nugen_numu_ic40_Dataset001882_00001000Files.hdf5" )
nugen  = tables.openFile( "nugen_numu_e-1_2082_files=999.hdf5")
#nugen  = tables.openFile( "nugen_numu_e-2_2326_files=4999.hdf5")


ndir_cut=5
ldir_cut=175
bayes_cut=26
rlogl_cut=8
para_cut=5

cut= ( ( nugen.root.I3MCTree.cols.MaxPrimary.Zenith[:] >= numpy.pi/2 ) * 
      ( nugen.root.MPEFitFitParams.cols.rlogl[:] <= rlogl_cut )  * 
      ( nugen.root.PSSigma.cols.value[:] <= numpy.radians(para_cut) ) *
      ( nugen.root.MPEFitCuts.cols.Ndir[:] >= ndir_cut ) *
      ( nugen.root.MPEFitCuts.cols.Ldir[:] >= ldir_cut ) * 
      ( (nugen.root.SPEFit32BayesianFitParams.cols.logl[:]-nugen.root.SPEFit32FitParams.cols.logl[:]) > bayes_cut) 
      )      

#cut= ( nugen.root.SPEFit32FitParams.cols.rlogl[:] <=7.5 )

OneWeight = nugen.root.I3MCWeightDict.cols.OneWeight[:][cut]
Energy    = nugen.root.I3MCTree.cols.MaxPrimary.Energy[:][cut]
Zenith    = nugen.root.I3MCTree.cols.MaxPrimary.Zenith[:][cut]

Nevents   = nugen.root.I3MCWeightDict.cols.NEvents[0]*1000. #1000 files
MinLogEnergy = nugen.root.I3MCWeightDict.cols.MinEnergyLog[0]
MaxLogEnergy = nugen.root.I3MCWeightDict.cols.MaxEnergyLog[0]
LogEnergyStep = 0.20
EnergyBins=(MaxLogEnergy-MinLogEnergy)/LogEnergyStep
print EnergyBins

MinCosZenith = -1
MaxCosZenith = 0
CosZenithStep = 0.2

SolidAngle = CosZenithStep

Aeff= OneWeight * numpy.log(10) / Energy / Nevents / SolidAngle / LogEnergyStep / 1e4


linestyles = [ dict(ls='steps-' ,c='k'),
              dict(ls='steps--',c='k'),
              dict(ls='steps-.',c='k'),
              dict(ls='steps:' ,c='k'),
              dict(ls='steps-' ,c='grey'),
              dict(ls='steps--',c='grey'),
              dict(ls='steps:' ,c='grey'),               
              ]


i=0

ymin= 1e-4


for CosZenith in numpy.arange ( MaxCosZenith-CosZenithStep, MinCosZenith-CosZenithStep, -CosZenithStep):
   print CosZenith, i 

   y,x= numpy.histogram( numpy.log10(Energy),
                         weights=Aeff * ( numpy.cos(Zenith) > CosZenith ) * ( numpy.cos(Zenith) < CosZenith + CosZenithStep),
                         bins=EnergyBins,
                         )
   x=10**(numpy.array(x))
   y[y<ymin]=ymin

   pylab.loglog(x,numpy.append([ymin],y),label=(r"$%1.1f < Cos(\theta) < %+1.1f$"%(CosZenith,CosZenith+CosZenithStep)),**linestyles[i])
   i+=1

pylab.xlabel(r"$E_\nu\ \ [GeV]$")
pylab.ylabel(r"$A_{eff}\ \ [m^2]$")
pylab.legend(loc=4)
pylab.savefig("Aeff.png")
pylab.savefig("Aeff.eps")
pylab.show()
