import cv2
import sys
from prog_isolate import read, create_mask, create_mask_rgb, find_contours
from prog_compare import compare
import os
import pprint
from prog_plot import plot_results_bar, prepare_for_plotting

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
	
def compare_against_v2(source_crop, platform):
	comparables = [f for f in os.listdir(platform) if os.path.isfile(os.path.join(platform, f))]
	
	smallest = ("unknown", 99999)
	
	for item in comparables:	
		diff = compare(
			source_crop,
			cv2.imread(
				platform + "/" + item
			)
		)
		if(diff < smallest[1]):
			smallest = (item, diff)

	return smallest

def try_detect(image_file, lower, upper, path, masktype, erode=0, dilate=0):
	platform_mask = masktype(image_file, lower, upper, erode, dilate)
	platform_contours = find_contours(platform_mask, 50) # prev was 1
	platform_best_match = ("Unknown", 99999)
	
	verygoodfit = 100
	
	for item in platform_contours:
		my_crop = get_crop(item, image_file)
		tmpres = compare_against_v2(my_crop, path )

		if(tmpres[1] < platform_best_match[1]):
			platform_best_match = (tmpres[0], tmpres[1])
		if tmpres[1] < verygoodfit:
			print("Found a good fit, moving on to next.")
			break
	
	
	return platform_best_match

if __name__ == "__main__":
	args = sys.argv

	if(len(args) < 2):
		print("error")
		exit()
		
	
	image_file = cv2.imread(args[1])
	
	pp = pprint.PrettyPrinter(indent=4)
	
	results = {}
	print("Calculating...")
	results["Xbox 360"] = try_detect(image_file, (20,50,50), (100,255,255), "./realxbox", create_mask, 2, 2)[1]
	results["PS4"] = try_detect(image_file, (200,200,200), (255,255,255), "./realps", create_mask_rgb, 0, 2)[1]
	results["Nintendo GCN"] = try_detect( image_file, (45,45,100), (211,211,224), "./realgc", create_mask_rgb, 0, 2 )[1]
	results["Nintendo DS"] = try_detect( image_file, (0,0,0), (40,40,40), "./realds", create_mask_rgb, 0, 3 )[1]
	results["Nintendo Wii U"] = try_detect( image_file, (180,180,180), (255,255,255), "./realwiiu", create_mask_rgb)[1]
	plot_results_bar( prepare_for_plotting(results), args[1] )
