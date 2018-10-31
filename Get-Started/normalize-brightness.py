import cv2
import copy

"""
newBright = scaleBrightness (img, 40)
cv2.imshow ("hihihi", newBright)
cv2.imshow ("Agh", img_rgb)

img = cv2.imread('2.jpg', 1)
img_grey = cv2.imread('2.jpg', 0)
"""

######################################################################

def mask_by_rgb(img, r, g, b):
    """Mask an BGR image by RGB based on threshold tuples"""
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb_threshold = cv2.inRange(img_rgb,
                                        (r[0], g[0], b[0]),
                                        (r[1], g[1], b[1]))
    img_rgb_mask = cv2.bitwise_and(img_rgb, img_rgb, mask=img_rgb_threshold)
    return cv2.cvtColor(img_rgb_mask, cv2.COLOR_BGR2RGB)

def mask_by_hls(img, h, l, s):
    """Mask an BGR image by HLS based on threshold tuples"""
    img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    img_hls_threshold = cv2.inRange(img_hls,
                                        (h[0], l[0], s[0]),
                                        (h[1], l[1], s[1]))
    img_hls_mask = cv2.bitwise_and(img_hls, img_hls, mask=img_hls_threshold)

#lowest brightness w/o mask = 36.41217240632445
def avg_non_black (img):
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
 
def scale_brightness(img):
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

img = cv2.imread('2.jpg', 1)
print(avg_non_black(img))
cv2.imshow("bit", img)
cv2.waitKey(0)

img_change1 = mask_by_rgb(img, (0, 255), (10, 255), (0, 255))
print(avg_non_black(img_change1))
cv2.imshow("bit", img_change1)
cv2.waitKey(0)

"""
hue = [20, 180.0]
saturation = [0.0, 255.0]
luminance = [0.0, 255.0]
img_change2 = cv2.bitwise_and(img_change1, img_change1, mask=threshold_hsl)
"""
