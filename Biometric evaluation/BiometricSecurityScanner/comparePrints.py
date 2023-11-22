#Brian Goldfarb

import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
from tempfile import TemporaryFile



def build_filters():
 filters = []
 ksize = 31
 for theta in np.arange(0, np.pi, np.pi / 20):
     kern = cv2.getGaborKernel((ksize, ksize), 3.8, theta, 13.0, 0.7, 0, ktype=cv2.CV_32F)
     kern /= 1.85*kern.sum()
     filters.append(kern)
 return filters

def process(img, filters):
 accum = np.zeros_like(img)
 for kern in filters:
     fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
     np.maximum(accum, fimg, accum)
 return accum




img_fn = sys.argv[1]
#img_fn = '/Users/briangoldfarb/Desktop/Fingerprints/fingerprint3.jpg'

name = ""
print("What is your Name?")
name = input()
print("Passing print through gabor filter for: ", name)
gabor_img = cv2.imread(img_fn)
gabor_img = cv2.resize(gabor_img, (500, 700))


filters = build_filters()

res1 = process(gabor_img, filters)
#cv2.imshow('Old Image', gabor_img)
#cv2.imshow('result', res1)
cv2.imwrite('/Users/briangoldfarb/Desktop/ProcessedPrints/gaborFilter-'+name+'.jpg',res1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#OTSU Filter
print("Passing print through ostu binarization filter...")
ostu_img = cv2.imread('/Users/briangoldfarb/Desktop/ProcessedPrints/gaborFilter-'+name+'.jpg',0)
# global thresholding
ret1,th1 = cv2.threshold(ostu_img,127,255,cv2.THRESH_BINARY)
# Otsu's thresholding
ret2,th2 = cv2.threshold(ostu_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(ostu_img,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# plot all the images and their histograms

#cv2.imshow("otsuBinarizedImage.jpg",th3)
cv2.imwrite("/Users/briangoldfarb/Desktop/ProcessedPrints/ostuBinarizationImage-"+name+'.jpg',th3)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



#Thin Image
print("Thinning image...")
thin_img = cv2.imread("/Users/briangoldfarb/Desktop/ProcessedPrints/ostuBinarizationImage-"+name+'.jpg',0)
size = np.size(thin_img)
skel = np.zeros(thin_img.shape,np.uint8)

ret,thin_img = cv2.threshold(thin_img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False

while( not done):
    eroded = cv2.erode(thin_img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(thin_img,temp)
    skel = cv2.bitwise_or(skel,temp)
    thin_img = eroded.copy()

    zeros = size - cv2.countNonZero(thin_img)
    if zeros==size:
        done = True

#cv2.imshow("skel",skel)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv2.imwrite("/Users/briangoldfarb/Desktop/ProcessedPrints/ThinnedImage-"+name+'.jpg', skel)

print("Determining fingerprint features...")
filename = "/Users/briangoldfarb/Desktop/ProcessedPrints/ThinnedImage-"+name+'.jpg'
edge_img = cv2.imread(filename)
gray = cv2.cvtColor(edge_img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,5,3,0.006)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
edge_img[dst>0.51*dst.max()]=[0,0,255]

coord = np.where(np.all(edge_img == (0, 0, 255), axis=-1))
#print(coord)
np.set_printoptions(threshold=np.nan)
print("**********************************")
for i in range(100):
    print((coord[0][i]), (coord[1][i]))
print("**********************************")




cv2.imwrite('/Users/briangoldfarb/Desktop/ProcessedPrints/edgeDetection'+name+'.jpg', edge_img)
cv2.imshow('dst',edge_img)


otherName = ""
print("Would you like to compare Images? Enter y to match")
if(input() != 'y'):
    print("Exiting...")
    sys.exit()
else:
    print("Which print would you like to match?")
    otherName = input()



otherImage = cv2.imread("/Users/briangoldfarb/Desktop/ProcessedPrints/ThinnedImage-"+otherName+'.jpg')


gray = cv2.cvtColor(otherImage,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,5,3,0.007)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
otherImage[dst>0.51*dst.max()]=[0,0,255]
coord2 = np.where(np.all(otherImage == (0, 0, 255), axis=-1))

print("**********************************")
for j in range(100):
    print((coord2[0][j]), (coord2[1][j]))
print("**********************************")


cv2.imshow('otherImage',otherImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

count = 0
total = 0


for i in range(250):
        if (coord2[0][i]) in coord[0] and coord2[1][i] in coord[1]:
            count += 1
            total += 1
        else:
            total += 1

print("Matching Minutaie:",count)
print("Total points calculated: ",total)
percent = (count/total)*100
print("Percent correct is: ", percent)

if(percent < 80):
    print("You are not authorized")
else:
    print("You are correctly identified")
    print("Welcome ",name)

print("Done")
