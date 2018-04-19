import numpy as np
import pylab as plt
import cv2

def rect(x, y, w, h, c):
	ax = plt.gca()
	polygon = plt.Rectangle((x, y), w, h, color=c)
	ax.add_patch(polygon)

def hsv_fill(x, y, cmap=plt.get_cmap("hsv")):
	plt.plot(x, y, lw=0)
	plt.axis('off');

	dx = x[1] - x[0]
	N = float(x.size)

	for n, (x, y) in enumerate(zip(x, y)):
		color = cmap(n / N)
		rect(x, 0, dx, y, color)

test = cv2.imread("satellite.jpg")
hsv = cv2.cvtColor(test, cv2.COLOR_BGR2HSV)

chans = cv2.split(hsv)

hist = cv2.calcHist([chans[0]], [0], None, [256], [0, 256])

x = np.linspace(0, 256, 256)
y = hist
hsv_fill(x, y)
plt.show()