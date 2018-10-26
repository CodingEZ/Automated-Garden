import cv2

img = cv2.imread('2.jpg', 1)
img_grey = cv2.imread('2.jpg', 0)

#######################################################################

mode = cv2.RETR_EXTERNAL
method = cv2.CHAIN_APPROX_SIMPLE
im2, contours, hierarchy = cv2.findContours(img_grey, mode=mode, method=method)

#######################################################################

min_area = 0.0
min_perimeter = 0.0
min_width = 0.0
max_width = 50.0
min_height = 0.0
max_height = 50.0

output = []
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    if (w < min_width or w > max_width):
        continue
    if (h < min_height or h > max_height):
        continue
    area = cv2.contourArea(contour)
    if (area < min_area):
        continue
    if (cv2.arcLength(contour, True) < min_perimeter):
        continue
    output.append(contour)

img_drawn = cv2.drawContours(img, contours, -1, (255.0, 0.0, 0.0), 2)
cv2.imshow('img_drawn', img_drawn)
cv2.waitKey(0)
