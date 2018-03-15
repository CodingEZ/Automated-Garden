import cv2
import numpy as np

def find_max(img):
    maxPixel = 0
    for x in range(width):
        for y in range(height):
            if img[y, x] > maxPixel:
                maxPixel = img[y, x]
    return maxPixel

def max_locations(img, maxPixel, thresholdBrightness=.6):
    locations = np.array( [[False] * width] * height )
    counter = 0
    for y in range(height):
        for x in range(width):
            if img[y, x] >= thresholdBrightness * maxPixel:
                # .6 is a threshold
                locations[y, x] = True
                counter += 1
    return locations

def find_next_location(locations):
    for y in range(height):
        for x in range(width):
            if locations[y, x]:
                return (y, x)
    return None

def get_connected_region(location, locations):
    checkLocations = [location]
    newCheckLocations = []
    checkedLocations = []
    region = np.array( [[False] * width] * height )
    locations[location[0], location[1]] = False  # first spot is already checked
    while len(checkLocations) > 0:
        for check in checkLocations:
            if check in checkedLocations:
                pass
            else:
                checkedLocations.append(check)
                if locations[check[0]-1, check[1]]:
                    newCheckLocations.append((check[0]-1, check[1]))
                    locations[check[0]-1, check[1]] = False
                if locations[check[0]+1, check[1]]:
                    newCheckLocations.append((check[0]+1, check[1]))
                    locations[check[0]+1, check[1]] = False
                if locations[check[0], check[1]-1]:
                    newCheckLocations.append((check[0], check[1]-1))
                    locations[check[0], check[1]-1] = False
                if locations[check[0], check[1]+1]:
                    newCheckLocations.append((check[0], check[1]+1))
                    locations[check[0], check[1]+1] = False
        for check2 in checkLocations:
            region[check2[0], check2[1]] = True
        checkLocations = newCheckLocations
        newCheckLocations = []
    return region

def get_all_regions(locations):
    regions = []
    start = find_next_location(locations)
    while start != None:
        region = get_connected_region(start, locations)
        regions.append(region)
        start = find_next_location(locations)
    return regions

def region_length(region):
    counter = 0
    for y in range(height):
        for x in range(width):
            if region[y][x]:
                counter += 1
    return counter

def keep_large_regions(regions, thresholdSize=100):
    for i in range(len(regions)-1, -1, -1):
        if region_length(regions[i]) < thresholdSize:
            regions.pop(i)
        else:
            pass
            #print(len(regions[i]))

def blacken_regions(regions, img):
    for region in regions2:
        for y in range(height):
            for x in range(width):
                if region[y, x]:
                    img[y, x] = 0

#img = cv2.imread('Rotated\\30.jpg', 0)
img = cv2.imread('EditedTestLeaves.jpg', 0)
cv2.imshow('Window', img)

(height, width) = img.shape
print('Height: ', height, ', Width: ', width)

maxPixel = find_max(img)
locations = max_locations(img, maxPixel, .6)    # .6 is default
regions = get_all_regions(locations)
keep_large_regions(regions, 100)                # 100 is default

locations2 = max_locations(img, maxPixel, .5)
regions2 = get_all_regions(locations2)
keep_large_regions(regions2)

blacken_regions(regions2, img)

print('Plant regions: ', len(regions), ', All regions: ', len(regions2))
print('Potential weeds: ', len(regions2)-len(regions))
cv2.imshow('Window1', img)

# try to make any image possible
# next step: detect if potential weeds are inside boundary of plant
#    if yes, not a weed
#    if no, probably a weed


