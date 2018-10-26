import numpy as np
import cv2

# Load an color image in grayscale
"""
function name: imread
purpose: reads in existing image file into a pixel array
parameters:
    string (name of file)
    int (image read mode, 0 is grayscale, 1 is color)
"""

img_grey = cv2.imread('2.jpg', 0)
img_color = cv2.imread('2.jpg', 1)

"""
function name: imshow
purpose: shows an image, may have issues on Macs
parameters:
    string (name of image)
    cv2 image
"""
cv2.imshow('image_grey', img_grey)
cv2.waitKey(0)
# positive number is milliseconds the img is shown
# 0 waits for any key to be pressed

cv2.inshow('image_color', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
function name: imwrite
purpose: writes an image to specified file name
parameters:
    string (name of new image)
    cv2 image
"""
cv2.imwrite('new_name.jpg', img_grey)
