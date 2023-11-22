import numpy as np
import cv2



img = cv2.imread('/home/pi/Desktop/fingerprint3.jpg', 0)
img = cv2.resize(img, (500, 500))
size = np.size(img)
skel = np.zeros(img.shape, np.uint8)

ret, img = cv2.threshold(img, 127, 255, 0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

done = False;

while( not done):
    eroded = cv2.erode(img, element)
    temp = cv2.dilate(eroded, element)
    temp = cv2.subtract(img, temp)
    skel = cv2.bitwise_or(skel, temp)
    img = eroded.copy()

    zeros = size - cv2.countNonZero(img)
    if zeros == size:
        done = True

cv2.imshow("skel", skel)

img2 = cv2.imwrite("thinnedImage.jpg",skel)

''' Finding the Harris Corner Points'''

img = cv2.imread("thinnedImage.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(skel, 2,3,0,0.04)
ret,dst = cv2.threshold(dst, 0.01*dst.max(), 255, 0)
dst = np.uint8(dst)

ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray, np.float32(centroids),(5,5),(-1,-1), criteria)



res = np.hstack((centroids, corners))
res = np.int0(res)
img[res[:,1],res[:,0]] = [0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]

cv2.imwrite('subpixelimg.jpg',img)
cv2.imshow('dst', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
