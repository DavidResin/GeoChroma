import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import itemfreq

img = cv2.imread('satellite.jpg')

average_color = [img[:, :, i].mean for i in range(img.shape[-1])]

arr = np.float32(img)
pixels = arr.reshape((-1, 3))

n_colors = 5
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
flags = cv2.KMEANS_RANDOM_CENTERS
_, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

palette = np.uint8(centroids)
quantized = palette[labels.flatten()]
quantized = quantized.reshape(img.shape)

dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]

res = np.zeros((200, 200, 3), np.uint8)


res[:, :100] = average_color

for i in range(n_colors):
	res[40 * i:40 * i + 20, 100:] = tuple(dominant_color)

cv2.imshow("test", res)
cv2.waitKey(0)