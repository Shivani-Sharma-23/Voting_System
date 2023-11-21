import numpy as np
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('/home/pi/Desktop/fingerPrintImages/fingerprint1.jpg',0)
img2 = cv2.imread('/home/pi/Desktop/fingerPrintImages/fingerprint3.jpg',0)
ret, img1 = cv2.threshold(img1, 127, 255, 0)
'''ret, img2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY_INV)'''

size1 = np.size(img1)
size2 = np.size(img2)

skel1 = np.zeros(img1.shape, np.uint8)
skel2 = np.zeros(img2.shape, np.uint8)

element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))


while 1:
    eroded = cv2.erode(img1, element)
    temp = cv2.dilate(eroded, element)
    temp = cv2.subtract(img1, temp)
    skel1 = cv2.bitwise_or(skel1, temp)
    img1 = eroded.copy()

    zeros = size1 - cv2.countNonZero(img1)
    if zeros==size1:
        break

cv2.imshow("skel", skel1)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:15], None, flags=2)
plt.imshow(img3)
plt.show()'''
