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

cv2.imshow('threshold_rgb', threshold_rgb)
cv2.imshow('threshold_hsl', threshold_hsl)
cv2.waitKey(100)

"""
self.__mask_1_input = source0
self.__mask_1_mask = self.hsl_threshold_output
(self.mask_1_output) = self.__mask(self.__mask_1_input, self.__mask_1_mask)

cv2.bitwise_and(img, img, mask=threshold_rgb)
"""
