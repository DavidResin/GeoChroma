import glob, os, cv2, math, time
import numpy as np
import colorsys as cs

# Processes all images in the given folder and writes the best images, best colors, coordinates for the best images and counts of images in respective files, the latter 2 to be used in the dataviz
def tile(n_tiles=8, input_dir='.', output_dir='.', size=64, stretch=False):
	canvas = np.zeros((size * n_tiles, size * n_tiles, 3), dtype="uint8")
	means = np.zeros((size * n_tiles, size * n_tiles, 3), dtype="uint8")
	scores = np.zeros((n_tiles, n_tiles))
	counts = np.zeros((n_tiles, n_tiles))
	data = []

	os.chdir(input_dir)

	start = time.time()
	
	for ext in ["*.png", "*.jpg"]:
		for fname in glob.glob(ext):
			img, score, color = process_image(fname)

			b, g, r = color

			h, s, v = cs.rgb_to_hsv(r / 256, g / 256, b / 256)

			xVal = h
			yVal = s

			x = math.floor(n_tiles * xVal)
			y = math.floor(n_tiles * yVal)

			if img is not None and (scores[x, y] == 0 or scores[x, y] > score):
				scores[x, y] = score

				xPos = size * x
				yPos = size * y

				img_bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

				img_proc = img

				img_proc = cv2.resize(img_proc, (size, size))

				canvas[xPos:xPos + size, yPos:yPos + size, :] = img_proc
				means[xPos:xPos + size, yPos:yPos + size, :] = color
				counts[x, y] = counts[x, y] + 1

				lat, lon, _ = tuple(fname.split('_'))

				data.append(['\'' + str(x) + '_' + str(y) + '\'', str(lat), str(lon)])

	os.chdir('../../' + output_dir)

	for i in range(n_tiles):
		for j in range(n_tiles):
			temp = canvas[i * size:(i+1) * size, j * size:(j+1) * size]
			cv2.imwrite('slices/slice_' + str(i) + '_' + str(j) + '.jpg', temp)


	end = time.time()
	print("time : " + str(end - start))

	t = time.localtime()[:6]

	cv2.imwrite('tiles_' + '_'.join(str(i) for i in t) + '.jpg', canvas)
	cv2.imwrite('means_' + '_'.join(str(i) for i in t) + '.jpg', means)

	np.savetxt("temp.txt", counts.tolist(), header="values = [[", footer="]];", delimiter=", ", newline="],\n[", fmt="%s", comments="")
	np.savetxt("coor.txt", [i for i in reversed(data)], header="values = [[", footer="]];", delimiter=", ", newline="],\n[", fmt="%s", comments="")

# Function for processing a given image by path, returns the cut image with a score and an average
def process_image(path, n_cuts=16):
	try:
		img_raw = cv2.imread(path)
	except:
		return None, 0, (0, 0, 0)

	img_proc = img_raw

	h, w, c = img_proc.shape
	short = min(h, w)
	img_crop = cv2.resize(img_proc[:short, :short], (128, 128))

	global_avg = np.mean(img_crop, (0, 1))
	
	score = sum([np.std(img_crop[:, :, i]) for i in range(3)])
	return img_proc, score, tuple(global_avg)

tile(n_tiles=32, input_dir="maps/small", output_dir="outputs", size=32)
