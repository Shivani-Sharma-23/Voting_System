import cv2
import numpy as np
import RPi.GPIO as GPIO



image1 = cv2.imread("colorprint.jpg",cv2.IMREAD_GRAYSCALE )
image2 = cv2.imread("nextprint2.jpg",cv2.IMREAD_GRAYSCALE)
print(image1)


def showFirstImage(img):
	cv2.imshow('newimg', img)
	cv2.waitKey(0)
	'''cv2.destroyAllWindows()'''

def showSecondImage(img):
	cv2.imshow('nxtimg', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
def showDiffImage(img):
	print("Showing image displaying differences between images")
	cv2.imshow('nxtimg', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def compareImages(img1, img2):
	diff = cv2.subtract(img1, img2)
	result = not np.any(diff)
	if result:
		print("images are the same")
		
	else:
		cv2.imwrite("result.jpg", diff)
		print("Images are different")
	return diff
	


showFirstImage(image1)
showSecondImage(image2)
diff = compareImages(image1, image2)
showDiffImage(diff)

