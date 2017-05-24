import cv2
import sys
import os
import math
import numpy as np

tolerance = 32

#cv2.resize(crop_tmp, (50,50), interpolation=cv2.INTER_AREA)

def oldcompare(firstpic, secondpic):
	sum = 0
	
	copyfirstpic = firstpic/tolerance
	copysecondpic = secondpic/tolerance
	
	for y in range (50):
		for x in range (50):
			pxa = copyfirstpic[x,y]
			pxb = copysecondpic[x,y]
		
			r2 = int(pxa[0])
			r1 = int(pxb[0])
			g2 = int(pxa[1])
			g1 = int(pxb[1])
			b2 = int(pxa[2])
			b1 = int(pxb[2])
			
			sum += math.sqrt(((r2-r1)**2)+((g2-g1)**2)+((b2-b1)**2)) # euclidian distance
	return sum

def newcompare(firstpic, secondpic):	
	imga_crop = firstpic[0:50, 0:50]
	imgb_crop = secondpic[0:50, 0:50]
	
	compare_a = imga_crop/tolerance
	compare_b = imgb_crop/tolerance
	
	#dist = np.linalg.norm(compare_b-compare_a)
	
	x = np.ndarray.flatten(compare_a)
	y = np.ndarray.flatten(compare_b)
	
	dist = (y-x)**2
	dist = math.sqrt(dist.sum())
	
	return dist

def compare(firstpic, secondpic):
	return oldcompare(
		firstpic,
		secondpic
	)	

if __name__ == "__main__":
	args = sys.argv
	
	if(len(args) <3):
		print("Usage: python " + args[0] + " (filea) (fileb)")
	else:
		a = cv2.imread(args[1])
		b = cv2.imread(args[2])
		#difference = compare(a, b)
		#print("The difference is " + str(difference))
		print("Oldcompare says " + str(oldcompare(a,b)))
		print("New compare says " + str(newcompare(a,b)))
