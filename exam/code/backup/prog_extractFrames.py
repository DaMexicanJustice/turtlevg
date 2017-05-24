import cv2
import sys
import os

def extractFrames(platform, file):
	vidcap = cv2.VideoCapture(file)
	success, image = vidcap.read()
	
	count = 0
	success = True
	
	subdir = "./" + platform + "/"
	
	if not os.path.exists(subdir):
		os.makedirs(subdir)

	while True:
		success, image = vidcap.read()
		if(success == False):
			break
		print("Frame " + str(count))
		cv2.imwrite(subdir + "frame%d.jpg" % count, image)
		count += 1
		

if __name__ == "__main__":
	args = sys.argv

	if(len(args) < 3):
		print("Usage:\n\tpython " + args[0] + " [platform] [videofile]\n")
		print("Example:\n\tpython " + args[0] + " xbox samplevideo.mp4\n")
	else:
		print("Ok")
		extractFrames(args[1], args[2])
