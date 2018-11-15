import copy
import cv2

## Threshold Example
red = (0.0, 255.0)
green = (75.0, 255.0)
blue = (0.0, 255.0)

hue = [21.582734842094585, 180.0]
saturation = [0.0, 255.0]
luminance = [0.0, 255.0]

img = cv2.imread('2.jpg', 1)

"""
Function name: cvtColor
Purpose: convert between different image types

Parameters:
    cv2 image
    cv2 color conversion types (search up cv2.COLOR_BGR2RGB for more info)
"""
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
threshold_rgb = cv2.inRange(img_rgb,
                            (red[0], green[0], blue[0]),
                            (red[1], green[1], blue[1]))

img_hsl = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
threshold_hsl = cv2.inRange(img_hsl,
                            (hue[0], luminance[0], saturation[0]),
                            (hue[1], luminance[1], saturation[1]))
'''
cv2.imshow('threshold_rgb', threshold_rgb)
cv2.imshow('threshold_hsl', threshold_hsl)
cv2.waitKey(100)
'''

img_grey = cv2.imread('2.jpg', 0)

def maskByThreshold (img, thresh):
    """take an img and mask it based off thresh (tuple of green) return an img"""
    red = (0.0, 255.0)
    green = thresh
    blue = (0.0, 255.0)
    threshold_rgb = cv2.inRange (img,
                                (red[0], green[0], blue[0]),
                                (red[1], green[1], blue[1]))
    return cv2.bitwise_and (img, img, mask=threshold_rgb)
    

#lowest brightness w/o mask = 36.41217240632445
def avgOfNoneBlack (img):
    avgSum = 0
    totPix = 0
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    width, height = img_grey.shape
    for i in range (width):
        for j in range (height):
            if img_grey [i][j] != 0:
                avgSum += (img_grey[i][j])
                totPix += 1
    return avgSum/totPix
    
def avg (img):
    avgSum = 0
    totPix = 0
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # possible error here
    width, height = img_grey.shape
    for i in range (width):
        for j in range (height):
            #if img_grey [i][j] != 0:
                avgSum += (img_grey[i][j])
                totPix += 1
    return avgSum/totPix
 
def scalar (goal, curr):
    return goal/curr
 
def scaleBrightness(img, goalBright):
    imgc = copy.deepcopy (img)
    height,width, channels = imgc.shape
    #currBright = avg (imgc)
    #c = scalar(goalBright, currBright)
    c=1.5
    for w in range (width):
        for h in range (height):
            imgc [h][w][0] = imgc [h][w][0] * c
            imgc [h][w][1] = imgc [h][w][1] * c
            imgc [h][w][2] = imgc [h][w][2] * c
            if imgc[h][w][0] > 255:     imgc[h][w][0] = 255
            if imgc[h][w][1] > 255:     imgc[h][w][1] = 255
            if imgc[h][w][2] > 255:     imgc[h][w][2] = 255
    return imgc

newBright = scaleBrightness (img, 40)
cv2.imshow ("hihihi", newBright)
cv2.imshow ("Agh", img_rgb)


print(avgOfNoneBlack (maskByThreshold(img_rgb, (10,255))))

urmum = cv2.bitwise_and(img, img, mask=threshold_rgb)
urdad = cv2.bitwise_and(urmum, urmum, mask=threshold_hsl)
cv2.imshow("bit", urmum)
cv2.waitKey(0)
cv2.imshow("bitwise", urdad)
cv2.waitKey(0)




"""
self.__mask_1_input = source0
self.__mask_1_mask = self.hsl_threshold_output
(self.mask_1_output) = self.__mask(self.__mask_1_input, self.__mask_1_mask)
"""
