import cv2
img = cv2.imread("testmask.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

params = cv2.SimpleBlobDetector_Params()
params.blobColor = 255
params.filterByColor = True
params.minArea = 16
params.filterByArea = True
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(255 - img)

cv2.imwrite(img, detector)
