import cv2
import matplotlib.pyplot as plt
from time import sleep
import numpy as np
import sys
from prog_isolate import read, create_mask, create_mask_rgb, find_contours
from prog_compare import compare
import os

def printimage(img):
	while True:
		cv2.imshow("aa",img)
		k = cv2.waitKey(0)
		if k == 27:
			cv2.destroyAllWindows()
			break

def get_crop(item, image):
	(x,y,w,h) = item

	crop_tmp = image[y:y+h, x:x+w]
	crop_tmp50x50 = cv2.resize(crop_tmp, (50,50), interpolation=cv2.INTER_AREA)
	return crop_tmp50x50

def compare_against(source_crop, platform):
	comparables = [f for f in os.listdir(platform) if os.path.isfile(os.path.join(platform, f))]
	
	res = []
	
	reference = cv2.imread("./realxbox/crop46.jpg")
	
	#smallest = {"name": "Unknown", "value": 1000000}
	smallest_name = "unknown"
	smallest_value = 99999
	
	for item in comparables:
		diff = compare(
			source_crop,
			cv2.imread(
				platform + "/" + item
			)
		)
		#print("diff is " + str(diff))
		if(diff < smallest_value):
			smallest_value = diff
			smallest_name = item
		

	return (smallest_name, smallest_value)

if __name__ == "__main__":
	args = sys.argv

	if(len(args) < 2):
		print("error")
		exit()
		
	
	image_file = cv2.imread(args[1])
	############ xbox
	xbox_mask = create_mask(image_file, (30,50,50), (90,255,255), 2, 2) #prev was 20-100
	xbox_contours = find_contours(xbox_mask, 50) # prev was 1
	xbox_best_match = ("Unknown", 99999)
	
	for item in xbox_contours:
		my_crop = get_crop(item, image_file)
		tmpres = compare_against(my_crop, "./realxbox" )
		print(tmpres)
		if(tmpres[1] < xbox_best_match[1]):
			xbox_best_match = (tmpres[0], tmpres[1])
	
	############# ps4
	ps4_mask = create_mask_rgb(image_file, (200,200,200), (255,255,255), 0, 2)
	ps4_contours = find_contours(ps4_mask, 50)
	ps4_best_match = ("Unknown", 99999)
	
	for item in ps4_contours:
		my_crop = get_crop(item, image_file)
		tmpres = compare_against(my_crop, "./realps")
		print(tmpres)
		if(tmpres[1] < ps4_best_match[1]):
			ps4_best_match = (tmpres[0], tmpres[1])
	
	print("XBOX best match")
	print(xbox_best_match)
	print("PS4 best match")
	print(ps4_best_match)