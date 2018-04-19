import glob, os, cv2, math, time
import numpy as np
import colorsys as cs


def tile(n_tiles=8, input_dir='.', output_dir='.', size=64, stretch=False):
	canvas = np.zeros((size * n_tiles, size * n_tiles, 3), dtype="uint8")
	means = np.zeros((size * n_tiles, size * n_tiles, 3), dtype="uint8")
	scores = np.zeros((n_tiles, n_tiles))

	os.chdir(input_dir)
	i = 0

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

				#cleanly convert color for image location

				#display stacks of images to check validity of scoring system

				#smaller tiles, more images

				#timestamps + parameters in file name

				#database for image data

				#calculate standard deviation?

				#time taken per image

				#adjust value on images!!!!

				#show means

	os.chdir('../' + output_dir)

	end = time.time()
	print("time : " + str(end - start))

	t = time.localtime()[:6]

	cv2.imwrite('tiles_' + '_'.join(str(i) for i in t) + '.jpg', canvas)
	cv2.imwrite('means_' + '_'.join(str(i) for i in t) + '.jpg', means)

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
	'''	
	indices, _ = zip(*np.ndenumerate(np.zeros((n_cuts, n_cuts))))
	cuts = [math.floor(short * (i / n_cuts)) for i in range(n_cuts + 1)]

	local_avgs = [[np.mean(img_proc[cuts[x]:cuts[x + 1], cuts[y]:cuts[y + 1], i]) for i in range(c)] for x, y in indices]

	score = sum([np.linalg.norm(global_avg - avg) for avg in local_avgs]) / n_cuts**2
	'''
	score = sum([np.std(img_crop[:, :, i]) for i in range(3)])
	return img_proc, score, tuple(global_avg)


def temp():
	start = time.time()
	path = 'inputs/37.jpg'
	process_image(path)
	end = time.time()
	print("tiles : " + str(end - start))


	start = time.time()

	img_proc = cv2.imread(path) 

	h, w, c = img_proc.shape
	short = min(h, w)
	img_crop = img_proc[:short, :short]

	global_avg = np.mean(img_crop, (0, 1))
	score = np.std(img_crop)

	end = time.time()

	print("std : " + str(end - start))



tile(n_tiles=32, input_dir="inputs", output_dir="outputs", size=32)
