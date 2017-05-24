import cv2
import sys
import math
from itertools import product

tolerance = 32

def euclidian_comparer(firstpic, secondpic):
	sum = 0
	
	copyfirstpic = firstpic/tolerance
	copysecondpic = secondpic/tolerance
	
	for x,y in product(range(50), range(50)):
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

def compare(firstpic, secondpic):
	return euclidian_comparer(
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
		print("Euclidian comparer says " + str(euclidian_comparer(a,b)))
