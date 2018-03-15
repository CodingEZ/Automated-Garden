import cv2

def find_max(img):
    maxPixel = 0
    for x in range(width):
        for y in range(height):
            if img[y, x] > maxPixel:
                maxPixel = img[y, x]
    return maxPixel

def max_locations(img, maxPixel, thresholdBrightness=.6):
    locations = []
    for x in range(width):
        for y in range(height):
            if img[y, x] >= thresholdBrightness * maxPixel:
                # .6 is a threshold
                locations.append((y, x))
    return locations

def get_connected_region(location, locations):
    checkLocations = [location]
    newCheckLocations = []
    checkedLocations = []
    region = []
    locations.remove(location)  # first spot is already checked
    while len(checkLocations) > 0:
        for check in checkLocations:
            if check in checkedLocations:
                pass
            else:
                checkedLocations.append(check)
                if (check[0]-1, check[1]) in locations:
                    newCheckLocations.append((check[0]-1, check[1]))
                    locations.remove((check[0]-1, check[1]))
                if (check[0]+1, check[1]) in locations:
                    newCheckLocations.append((check[0]+1, check[1]))
                    locations.remove((check[0]+1, check[1]))
                if (check[0], check[1]-1) in locations:
                    newCheckLocations.append((check[0], check[1]-1))
                    locations.remove((check[0], check[1]-1))
                if (check[0], check[1]+1) in locations:
                    newCheckLocations.append((check[0], check[1]+1))
                    locations.remove((check[0], check[1]+1))
        region += checkLocations
        checkLocations = newCheckLocations
        newCheckLocations = []
    return region

def get_all_regions(locations, img):
    regions = []
    while len(locations) > 0:
        region = get_connected_region(locations[0], locations)
        '''
        for location in region:
            img[location[0], location[1]] = 0
        '''
        regions.append(region)
    return regions

def keep_large_regions(regions, thresholdSize=100):
    for i in range(len(regions)-1, -1, -1):
        print(len(regions[i]))
        if len(regions[i]) < thresholdSize:
            regions.pop(i)
        else:
            pass

#img = cv2.imread('Rotated\\30.jpg', 0)
img = cv2.imread('EditedTestLeaves.jpg', 0)
cv2.imshow('Window', img)

(height, width) = img.shape
#print(height, width)

maxPixel = find_max(img)    
locations = max_locations(img, maxPixel, .6)    # .6 is default
regions = get_all_regions(locations, img)
keep_large_regions(regions, 100)                # 100 is default

locations2 = max_locations(img, maxPixel, .4)
regions2 = get_all_regions(locations2, img)
keep_large_regions(regions2)

for region in regions:
    for location in region:
        img[location[0], location[1]] = 0

print(len(regions))
print(len(regions2))
print('Potential weeds: ', len(regions2)-len(regions))
#print(maxPixel, locations)
cv2.imshow('Window1', img)

# try to make any image possible
# next step: detect if potential weeds are inside boundary of plant
#    if yes, not a weed
#    if no, probably a weed


