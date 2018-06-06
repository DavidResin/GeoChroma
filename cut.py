import glob, os, cv2, math, time
import numpy as np
import colorsys as cs

cut_y = 6
cut_x = 4
size = 32
step = 0.1

count = 0

os.chdir('maps')

for fname in glob.glob('*png'):
	x, y, rest = tuple(fname.split('_'))

	x = float(x)
	y = float(y)

	img = cv2.imread(fname)

	h, w = img.shape[:2]

	for i in range(cut_x):
		for j in range(cut_y):
			temp = img[round(h * j / cut_y):round(h * (j + 1) / cut_y), round(w * i / cut_x):round(w * (i + 1) / cut_x)]
			temp = cv2.resize(temp, (size, size))
			count += 1
			cv2.imwrite('small/' + str(round(x + step * i / cut_x, 2)) + '_' + str(round(y + step * j / cut_y, 2)) + '_' + rest, temp)