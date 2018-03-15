# import the necessary packages
import numpy
import imutils
import cv2
import os

# load the image from disk
image = cv2.imread('Edited Leaf.jpg')

if not os.path.exists('Rotated'):
    os.mkdir('Rotated')

# loop over the rotation angles again, this time ensuring
# no part of the image is cut off
for angle in numpy.arange(0, 360, 15):
    rotated = imutils.rotate_bound(image, angle)
    cv2.imshow("Rotated (Correct)", rotated)
    cv2.imwrite('Rotated\\' + str(angle) + '.jpg', rotated)
    cv2.waitKey(100)

