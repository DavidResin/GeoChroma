import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import itemfreq
from math import *

cut = 32

values = []
img = cv2.imread('desert.jpg')
recolor_rgb = img.copy()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
recolor = hsv.copy()

h, w = img.shape[:2]

for i in range(cut):
	for j in range(cut):
		aH, bH = floor(h * (i / cut)), floor(h * ((i + 1) / cut))

		aW, bW = floor(w * (j / cut)), floor(w * ((j + 1) / cut))

		average_color = [hsv[aH:bH, aW:bW, i].mean() for i in range(img.shape[-1])]
		values.append(average_color)

		temp = np.zeros((bH - aH, bW - aW, 2))
		temp[:, :, 0].fill(average_color[0])
		temp[:, :, 1].fill(average_color[1])

		recolor[aH:bH, aW:bW, 0:2] = temp

		average_rgb = [img[aH:bH, aW:bW, i].mean() for i in range(img.shape[-1])]

		temp = np.zeros((bH - aH, bW - aW, 3))
		temp[:, :, 0].fill(average_rgb[0])
		temp[:, :, 1].fill(average_rgb[1])
		temp[:, :, 2].fill(average_rgb[2])

		recolor_rgb[aH:bH, aW:bW, :] = temp

average_color = [hsv[:, :, i].mean() for i in range(img.shape[-1])]		

x = np.arange(len(values))
series = list(map(list, list(zip(*values))))

for i in range(len(series)):
	plt.plot(x, series[i])

plt.show()

cv2.imshow("recolor", recolor)
cv2.waitKey(0)
cv2.imshow("recolor", recolor_rgb)
cv2.waitKey(0)