import cv2
import sys

def read(path, switch_channels=True):
	image = cv2.imread(path)
	if switch_channels:
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return image

def create_mask_rgb(image, lower, upper, erode_iterator=0, dilate_iterator=0):
	nothsv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	mask = cv2.inRange(nothsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=erode_iterator)
	mask = cv2.dilate(mask, None, iterations=dilate_iterator)
	return mask
	
def create_mask(image, lower, upper, erode_iterator=0, dilate_iterator=0):
	hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=erode_iterator)
	mask = cv2.dilate(mask, None, iterations=dilate_iterator)
	return mask

def find_contours(frame, area):
	arr = []
	cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	for c in cnts:
		if cv2.contourArea(c) >= area:
			(x,y,w,h) = cv2.boundingRect(c)
			arr.append((x,y,w,h))
			
	return arr

if __name__ == "__main__":
	args = sys.argv
	
	if(len(args) < 2):
		print("Usage: python " + args[0] + "(file)")
		exit()

	image_path = args[1]
	img = read(image_path) # reads and converts BGR -> RGB
	
	# For PS4
	w_mask = create_mask_rgb(img, (200,200,200), (255,255,255), 0, 2)
	
	# For XBOX360
	#g_mask = create_mask(img, (30,50,50), (70,255,255
	
	# For DS
	#b_mask = create_mask_rgb(img, (0,0,0), (40,40,40), 0, 3)
	
	#Assign desired mask to this variable to be used as the reference going forward
	mask = w_mask
	
	cv2.imwrite("test.jpg", mask)

	the_contours = find_contours(mask, 50)

	idx = 0
	for item in the_contours:
		idx += 1
		(x,y,w,h) = item
		print(str(x) + ":" + str(y) + ":" + str(w) + ":" + str(h))
		crop_tmp = img[y:y+h, x:x+w]
		crop_tmp = cv2.cvtColor(crop_tmp, cv2.COLOR_BGR2RGB)
		crop_tmp50x50 = cv2.resize(crop_tmp, (50,50), interpolation=cv2.INTER_AREA)
		cv2.imwrite("crop" + str(idx) + ".jpg", crop_tmp50x50)
