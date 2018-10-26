import cv2

## Threshold Example
red = (0.0, 255.0)
green = (75.0, 255.0)
blue = (0.0, 255.0)

img = cv2.imread('2.jpg', 1)

"""
Function name: cvtColor
Purpose: convert between different image types

"""
img_converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
threshold = cv2.inRange(img_converted,
                        (red[0], green[0], blue[0]),
                        (red[1], green[1], blue[1]))
cv2.imshow('threshold', threshold)


external_only = True        # for retreiving only extrenal contours
if (external_only):
    mode = cv2.RETR_EXTERNAL
else:
    mode = cv2.RETR_LIST
method = cv2.CHAIN_APPROX_SIMPLE
im2, contours, hierarchy = cv2.findContours(threshold, mode=mode, method=method)
