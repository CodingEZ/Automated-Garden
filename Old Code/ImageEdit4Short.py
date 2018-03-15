import cv2
import numpy as np
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
        '''Finds all locations above a threshold brightness compared to the maximum brightness.
            The default is .6 (out of 1.0). No need to calculate the exact value of brightness.'''
        locations = copy.deepcopy(self.blackImg)
        for y in range(self.height):
            for x in range(self.width):
                if self.img[y, x] >= thresholdBrightness * maxPixel:
                    # .6 is a threshold
                    locations[y, x] = self.white
        return locations

    def find_next_location(self, locations):
        '''Goes through each ROW from LEFT TO RIGHT until it encounters the first true location.'''
        for y in range(self.height):
            for x in range(self.width):
                if locations[y, x]:
                    return (y, x)
        return None

    def get_connected_region(self, location, locations):
        '''Obtains a single. The format of the region is a numpy array that has the
            height and width of the original image. Be careful as this is a call by
            reference that directly edits the array of locations.'''
        checkLocations = [location]
        newCheckLocations = []
        checkedLocations = []
        region = copy.deepcopy(self.blackImg)
        locations[location[0], location[1]] = self.black  # first spot is already checked
        while len(checkLocations) > 0:
            for check in checkLocations:
                if check in checkedLocations:
                    pass
                else:
                    checkedLocations.append(check)
                    if check[0] != 0:
                        if locations[check[0]-1, check[1]] == 1:
                            newCheckLocations.append((check[0]-1, check[1]))
                            locations[check[0]-1, check[1]] = self.black
                    if check[0]+1 != self.height:
                        if locations[check[0]+1, check[1]] == 1:
                            newCheckLocations.append((check[0]+1, check[1]))
                            locations[check[0]+1, check[1]] = self.black
                    if check[1] != 0:
                        if locations[check[0], check[1]-1] == 1:
                            newCheckLocations.append((check[0], check[1]-1))
                            locations[check[0], check[1]-1] = self.black
                    if check[1]+1 != self.width:
                        if locations[check[0], check[1]+1] == 1:
                            newCheckLocations.append((check[0], check[1]+1))
                            locations[check[0], check[1]+1] = self.black
            for check2 in checkLocations:
                region[check2[0], check2[1]] = self.white
            checkLocations = newCheckLocations
            newCheckLocations = []
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

    def region_length(self, region):
        '''Finds the size of a region in pixels.'''
        counter = 0
        for y in range(self.height):
            for x in range(self.width):
                if region[y][x]:
                    counter += 1
        return counter

    def keep_large_regions(self, regions, thresholdSize=100):
        '''Take the regions and filters those that are below threshold size. Default threshold size
            is 100 pixels. Be careful as this is a call by reference that directly edits the list
            of regions.'''
        for i in range(len(regions)-1, -1, -1):
            if self.region_length(regions[i]) < thresholdSize:
                regions.pop(i)
            else:
                pass

    def combine_regions(self, regions):
        newImage = copy.deepcopy(self.blackImg)
        for y in range(self.height):
            for x in range(self.width):
                boolArray = [None] * len(regions)
                for index in range(len(regions)):
                    boolArray[index] = regions[index][y, x]
                if self.white in boolArray:
                    newImage[y, x] = self.white
        return newImage

    def blacken_regions(self, regions):
        '''This is just a check that the regions are correct. Be careful as this is a call by
            reference that directly edits the image.'''
        for region in regions:
            for y in range(self.height):
                for x in range(self.width):
                    if region[y, x]:
                        self.img[y, x] = self.black

