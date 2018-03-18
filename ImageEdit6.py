import cv2
import numpy as np
import math
import copy

class Editor():

    def __init__(self, img):
        self.img = img
        (self.height, self.width) = img.shape
        self.black = 0
        self.white = 1
        self.blackImg = np.array( [[self.black] * self.width for _ in range(self.height)], dtype='uint8' )
        print('Height: ', self.height, ', Width: ', self.width)

    def find_max(self):
        '''Finds the pixel of maximum brightness. This value is usually 255.'''
        maxPixel = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.img[y, x] > maxPixel:
                    maxPixel = self.img[y, x]
        return maxPixel

    def max_locations(self, maxPixel, thresholdBrightness=.6):
        '''Finds all locations above a threshold brightness compared to the maximum
            brightness. The default is .6 (out of 1.0). No need to calculate the exact
            value of brightness.'''
        lowestIntensity = thresholdBrightness * maxPixel
        ret, thresh = cv2.threshold(self.img, lowestIntensity, 255, cv2.THRESH_BINARY)
        locations = copy.deepcopy(self.blackImg)
        for y in range(self.height):
            for x in range(self.width):
                if thresh[y, x] == 255:
                    locations[y, x] = self.white
        return locations

    def find_next_location(self, locations):
        '''Goes through each ROW from LEFT TO RIGHT until it encounters the first
            true location. Skips every other column and row.'''
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):
                if locations[y, x]:
                    return (y, x)
        return None

    def find_centroid(self, region):
        contour = cv2.findContours(region, 1, 2)[1][0]
        M = cv2.moments(contour)
        if M != None:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return (cY, cX)
        else:
            return None

    def get_connected_region(self, location, locations):
        '''Obtains a single. The format of the region is a numpy array that has the
            height and width of the original image. Be careful as this is a call by
            reference that directly edits the array of locations.'''
        checkLocations = set([location])
        newCheckLocations = set()
        checkedLocations = set()
        region = copy.deepcopy(self.blackImg)
        locations[location[0], location[1]] = self.black  # first spot is already checked
        while len(checkLocations) > 0:
            for check in checkLocations:
                if check not in checkedLocations:
                    checkedLocations.add(check)
                    if check[0] != 0 and locations[check[0]-1, check[1]] == 1:
                        newCheckLocations.add((check[0]-1, check[1]))
                        locations[check[0]-1, check[1]] = self.black
                    if check[0]+1 != self.height and locations[check[0]+1, check[1]] == 1:
                        newCheckLocations.add((check[0]+1, check[1]))
                        locations[check[0]+1, check[1]] = self.black
                    if check[1] != 0 and locations[check[0], check[1]-1] == 1:
                        newCheckLocations.add((check[0], check[1]-1))
                        locations[check[0], check[1]-1] = self.black
                    if check[1]+1 != self.width and locations[check[0], check[1]+1] == 1:
                        newCheckLocations.add((check[0], check[1]+1))
                        locations[check[0], check[1]+1] = self.black
            for check2 in checkLocations:
                region[check2[0], check2[1]] = self.white
            checkLocations = newCheckLocations
            newCheckLocations = set()
        return region

    def get_all_regions(self, locations):
        '''Obtains each region. Returns a list of regions.'''
        regions = []
        start = self.find_next_location(locations)
        while start != None:
            region = self.get_connected_region(start, locations)
            regions.append(region)
            start = self.find_next_location(locations)
        return regions

    def keep_large_regions(self, regions, thresholdSize=100):
        '''Take the regions and filters those that are below threshold size. Default
            threshold size is 100 pixels. This function uses copies.'''
        largeRegions = copy.deepcopy(regions)
        for i in range(len(regions)-1, -1, -1):
            contour = cv2.findContours(regions[i], 1, 2)[1][0]
            if cv2.contourArea(contour) < thresholdSize:
                largeRegions.pop(i)
        return largeRegions

    def obtain_largest_region(self, regions):
        '''Take the largest region with greatest circularity (best leaf shape).
            May result in a tie.'''
        largestRegion = []
        startSize = self.img.size
        while len(largestRegion) == 0 and startSize > 0:
            startSize //= 2
            largestRegion = self.keep_large_regions(regions, startSize)
        while len(largestRegion) != 0:
            startSize += 100
            largestRegion = self.keep_large_regions(regions, startSize)
        while len(largestRegion) == 0:
            startSize -= 1
            largestRegion = self.keep_large_regions(regions, startSize)
        return (largestRegion, startSize)

    def mk_points_list(self, regions):
        '''This creates an unedited list of points on a polygon.'''
        pointsList = [None] * len(regions)
        counter = 0
        for region in regions:
            pointsList[counter] = self.find_centroid(region)
            counter += 1
        return pointsList

    def combine_regions(self, regions):
        newImage = copy.deepcopy(self.blackImg)
        for y in range(self.height):
            for x in range(self.width):
                for index in range(len(regions)):
                    if regions[index][y, x] == self.white:
                        newImage[y, x] = self.white
                        break
        return newImage

    def blacken_regions(self, regions):
        '''This is just a check that the regions are correct. Be careful as this
            is a call by reference that directly edits the image.'''
        for region in regions:
            for y in range(self.height):
                for x in range(self.width):
                    if region[y, x]:
                        self.img[y, x] = self.black

    def outline(self, img, largeRegions, color, needToCopy=False):
        if needToCopy:
            img = copy.deepcopy(img)
            
        radius = 10
        for index in range(len(largeRegions)):
            contour = cv2.findContours(largeRegions[index], 1, 2)[1][0]
            cv2.drawContours(img, [contour], -1, color, 2)
            
        if needToCopy:
            return img
    
