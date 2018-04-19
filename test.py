import cv2
from matplotlib import pyplot as plt
from pylab import figure, show
import numpy as np
from matplotlib import colors
from matplotlib import cm

test = cv2.imread("satellite.jpg")
hsv = cv2.cvtColor(test, cv2.COLOR_BGR2HSV)

chans = cv2.split(hsv)

cols = ("b", "g", "r")
plt.figure()
plt.title("'Flattened' Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
features = []
 
# loop over the image channels
#for (chan, color) in zip(chans, cols):
  # create a histogram for the current channel and
  # concatenate the resulting histograms for each
  # channel
hist = cv2.calcHist([chans[0]], [0], None, [256], [0, 256])
features.extend(hist)
 
  # plot the histogram
plt.plot(hist)
plt.xlim([0, 256])

plt.show()
'''
fig = figure()
ax = fig.add_subplot(111)
Ntotal = 1000
N, bins, patches = ax.hist(cv2.calcHist([chans[0]], [0], None, [256], [0, 256]), 20)

fracs = N.astype(float) / N.max()

norm = colors.Normalize(vmin=fracs.min(), vmax=fracs.max())

for thisfrac, thispatch in zip(fracs, patches):
	color = cm.jet(norm(thisfrac))
	thispatch.set_facecolor(color)

show()
'''