#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.backends.backend_agg

dat = np.load("./IC86_exp_all.npy")
ra = dat["ra"]*180/np.pi - 180.0
dec = dat["dec"]*180/np.pi

hist, xedges, yedges =  np.histogram2d(dec, ra, bins=[40,80],
                                    range=[[-90,90],[-180,180]])

fig = plt.figure(figsize=(10, 5))  
ax = fig.add_subplot(111,projection='mollweide')

ax.set_xlabel('RA')
ax.set_ylabel('DEC')
ax.set_xticklabels(np.arange(30,331,30))

X,Y = np.meshgrid(np.radians(yedges),np.radians(xedges))
image = ax.pcolormesh(X,Y,hist)
ax.grid(True)
cb = fig.colorbar(image, orientation='vertical')

fig.show()
#canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
#fig.canvas.print_figure("image.png")


#h = plt.contourf(xedges[0:101],yedges[0:100],h)

#fig = plt.figure(figsize=(10, 5))

#ax = fig.add_subplot(111, projection="mollweide")
#ax.grid(True)
#ax.contourf(xedges[0:100],yedges[0:100],h)

