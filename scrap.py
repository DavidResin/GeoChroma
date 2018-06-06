def convert_coordinate(deg=0, min=0, sec=0):
	return deg + min / 60 + sec / 3600

from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import cv2, time

# need to run "export PATH=$PATH:"" first

# Setting up the scrapper
profile = webdriver.FirefoxProfile()
driver = webdriver.Firefox(firefox_profile=profile)
driver.get("https://coast.noaa.gov/dataviewer/#/imagery/search/")
driver.find_element_by_class_name('basemap2').click()

#maxLon = convert_coordinate(47, 48)
#minLon = convert_coordinate(45, 49)
#minLat = convert_coordinate(5, 57)
#maxLat = convert_coordinate(10, 29)

# Setting boundaries and conditions
maxLon = convert_coordinate(41, 1)
minLon = convert_coordinate(36, 8)
minLat = convert_coordinate(-109, 2)
maxLat = convert_coordinate(101, 0)

textbox = driver.find_element_by_id('location-search-input')

time.sleep(2)

canvas = driver.find_element_by_tag_name("canvas")

delta = 0.1
start_x = minLat
start_y = minLon
end_x = maxLat
end_y = maxLon
x = start_x
y = start_y

geolocator = Nominatim()

# GOing through the whole area
while x < end_x:
	while y < end_y:
		loc = geolocator.reverse(str(y) + ',' + str(x)).address.split(', ')
		
		if (loc[-2] == 'Colorado' or loc[-3] == 'Colorado'):
			textbox = driver.find_element_by_id('location-search-input')
			textbox.send_keys(str(x) + ',' + str(y) + ',' + str(x + delta) + ',' + str(y + delta))
			textbox.send_keys(Keys.RETURN)
			time.sleep(2.5)

			driver.save_screenshot("canvas.png")

			im = cv2.imread('canvas.png')
			im = im[220:540, 300:550]

			cv2.imwrite('maps/' + str(x) + '_' + str(y) + '_' + loc[-3] + '.png', im)

		y = round(y + delta, 1)

	x = round(x + delta, 1)
	y = start_y
