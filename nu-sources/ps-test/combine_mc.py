#! /usr/bin/python

import numpy as np

dat0 = np.load("./MC/Merged_11069_downgoing_Part0000_001000files.npy")
dat1 = np.load("./MC/Merged_11069_downgoing_Part0001_001000files.npy")
dat2 = np.load("./MC/Merged_11069_downgoing_Part0002_001000files.npy")
dat3 = np.load("./MC/Merged_11069_downgoing_Part0003_001000files.npy")
dat4 = np.load("./MC/Merged_11069_downgoing_Part0004_001000files.npy")
dat5 = np.load("./MC/Merged_11069_downgoing_Part0005_001000files.npy")

dat10 = np.load("./MC/Merged_11069_upgoing_Part0000_001000files.npy")
dat11 = np.load("./MC/Merged_11069_upgoing_Part0001_001000files.npy")
dat12 = np.load("./MC/Merged_11069_upgoing_Part0002_001000files.npy")
dat13 = np.load("./MC/Merged_11069_upgoing_Part0003_001000files.npy")
dat14 = np.load("./MC/Merged_11069_upgoing_Part0004_001000files.npy")
dat15 = np.load("./MC/Merged_11069_upgoing_Part0005_001000files.npy")

dat = np.append(dat0,dat1,axis=0)
dat = np.append(dat,dat2,axis=0)
dat = np.append(dat,dat3,axis=0)
dat = np.append(dat,dat4,axis=0)
dat = np.append(dat,dat5,axis=0)
dat = np.append(dat,dat10,axis=0)
dat = np.append(dat,dat11,axis=0)
dat = np.append(dat,dat12,axis=0)
dat = np.append(dat,dat13,axis=0)
dat = np.append(dat,dat14,axis=0)
dat = np.append(dat,dat15,axis=0)

np.save("./all_mc.npy", dat)

