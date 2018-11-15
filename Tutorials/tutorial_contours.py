import cv2

img = cv2.imread('2.jpg', 1)

r = (0.0, 255.0)
g = (70.0, 255.0)
b = (0.0, 255.0)
img_rgb_threshold = cv2.inRange(img, 
	(r[0], g[0], b[0]),
	(r[1], g[1], b[1])
)

"""
Function name: cv2.findContours
Inputs:
	image: cv2 binary image
	mode: cv2 contour mode
	method: cv2 contour method
Outputs:
	image: cv2 image
	contours: cv2 contours
	hierarchy: ?, look it up for more information
"""

#######################################################################

mode = cv2.RETR_EXTERNAL
method = cv2.CHAIN_APPROX_SIMPLE
## Different contour modes will pick up different contours

im2, contours, hierarchy = cv2.findContours(img_rgb_threshold, mode=mode, method=method)

#######################################################################

"""
Function name: cv2.boundingRect
Inputs:
	contour
Outputs:
	x, y, w, h
	w is width of smallest rectangle containing the contour
	h is height of smallest rectangle containing the contour

Useful for getting bounds of a region, could apply mask
"""

"""
Function name: cv2.contourArea
Inputs:
	contour
Outputs:
	area: int (the area contained within the contour)

Useful for getting the size of a region, used in filtering noise
"""

"""
Function name: cv2.arcLength
Inputs:
	contour
Outputs:
	length: int (the perimeter of the area contained within the contour)

Useful for getting the perimeter of a region, used in filtering noise
"""

min_area = 100.0
max_area = 40000.0
min_perimeter = 0.0
min_width = 10.0
max_width = 500.0
min_height = 10.0
max_height = 500.0

output_contours = []
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    if (w < min_width or w > max_width):
        continue
    if (h < min_height or h > max_height):
        continue
    area = cv2.contourArea(contour)
    if (area < min_area or area > max_area):
        continue
    if (cv2.arcLength(contour, True) < min_perimeter):
        continue
    output_contours.append(contour)

"""
Function name: cv2.drawContours

Inputs:
	cv2 image
	contour list
	mode: integer
	color: (0 < int < 255, int, int)
	option parameters: (thickness is the first)

Outputs:
	cv2 image with contours drawn on the input image
"""

img_drawn = cv2.drawContours(img, output_contours, -1, (255.0, 0.0, 0.0), 2)
cv2.imshow('img_drawn', img_drawn)
cv2.waitKey(0)

"""
Function name: cv2.moments
Inputs:
	contour: cv2 contour
Output:
	moment dictionary, which contains many different values
	The important ones to know are "m10" and "m01", which are
	the x value and y value on the image, essentially, a pixel location
"""

for contour in output_contours:
	M = cv2.moments(contour)
	print(M)
	if M["m00"] == 0:
		continue
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	print(cX, cY)
