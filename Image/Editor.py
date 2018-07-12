import cv2
import numpy as np
import copy

class Editor:

    def __init__(self, img=None):
        self.img = img

        if img is None:
            self.height = None
            self.width = None
        else:
            (self.height, self.width) = img.shape

        self.black = 0
        self.white = 1
        self.blackImg = None

        self.maxPixel = self.find_max()
        self.maxLocations = None
        self.regions = None             # holds all regions that pass through the filter
        self.size = None                # size of plant

    def select_img(self, img):
        self.img = img
        (self.height, self.width) = img.shape
        self.maxPixel = self.find_max()
        self.blackImg = np.array([[self.black] * self.width for _ in range(self.height)], dtype='uint8')
        print('Height: ', self.height, ', Width: ', self.width)

    def find_max(self):
        """Finds the pixel of maximum brightness. This value is usually 255."""
        if self.img is None:
            return None

        maxPixel = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.img[y, x] > maxPixel:
                    maxPixel = self.img[y, x]
        return maxPixel

    def max_locations(self, thresholdBrightness=.6):
        """Finds all locations above a threshold brightness compared to the maximum
            brightness. The default is .6 (out of 1.0). No need to calculate the exact
            value of brightness."""
        lowestIntensity = thresholdBrightness * self.maxPixel
        ret, thresh = cv2.threshold(self.img, lowestIntensity, 255, cv2.THRESH_BINARY)
        self.maxLocations = copy.deepcopy(self.blackImg)

        for y in range(self.height):
            for x in range(self.width):
                if thresh[y, x] == 255:
                    self.maxLocations[y, x] = self.white

    def find_next_location(self, startY=0):
        """Goes through each ROW from LEFT TO RIGHT until it encounters the first
            true location. Skips every other column and row."""
        for y in range(startY, self.height, 2):
            for x in range(0, self.width, 2):
                if self.maxLocations[y, x]:
                    return y, x
        return None

    @staticmethod
    def find_centroid(region):
        contour = cv2.findContours(region, 1, 2)[1][0]
        M = cv2.moments(contour)
        if M is not None:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cY, cX
        else:
            return None

    def get_connected_region(self, start):
        """Obtains a single region. The format of the region is a numpy array that has
            the height and width of the original image. Be careful as this is a call by
            reference that directly edits the array of locations."""
        checkLocations = {start}
        newCheckLocations = set()
        checkedLocations = set()
        region = copy.deepcopy(self.blackImg)
        self.maxLocations[start[0], start[1]] = self.black  # first spot is already checked

        while len(checkLocations) > 0:
            for check in checkLocations:
                if check not in checkedLocations:
                    checkedLocations.add(check)
                    if check[0] != 0 and self.maxLocations[check[0]-1, check[1]] == 1:
                        newCheckLocations.add((check[0]-1, check[1]))
                        self.maxLocations[check[0]-1, check[1]] = self.black
                    if check[0]+1 != self.height and self.maxLocations[check[0]+1, check[1]] == 1:
                        newCheckLocations.add((check[0]+1, check[1]))
                        self.maxLocations[check[0]+1, check[1]] = self.black
                    if check[1] != 0 and self.maxLocations[check[0], check[1]-1] == 1:
                        newCheckLocations.add((check[0], check[1]-1))
                        self.maxLocations[check[0], check[1]-1] = self.black
                    if check[1]+1 != self.width and self.maxLocations[check[0], check[1]+1] == 1:
                        newCheckLocations.add((check[0], check[1]+1))
                        self.maxLocations[check[0], check[1]+1] = self.black
            for check2 in checkLocations:
                region[check2[0], check2[1]] = self.white
            checkLocations = newCheckLocations
            newCheckLocations = set()
        return region

    def get_all_regions(self):
        """Obtains each region. Returns a list of regions."""
        self.regions = []
        start = self.find_next_location()
        while start is not None:
            region = self.get_connected_region(start)
            self.regions.append(region)
            start = self.find_next_location(start[0])

    def get_large_regions(self, weedFactor=1):
        """Take the regions and filters those that are below threshold size."""
        largeRegions = copy.deepcopy(self.regions)
        for i in range(len(self.regions)-1, -1, -1):
            contour = cv2.findContours(self.regions[i], 1, 2)[1][0]
            if cv2.contourArea(contour) < self.size * weedFactor:
                largeRegions.pop(i)
        return largeRegions

    def get_largest_region(self):
        """Take the largest region with greatest circularity (best leaf shape).
            May result in a tie."""

        largestRegion = []
        self.size = self.img.size
        while len(largestRegion) == 0 and self.size > 0:
            self.size //= 2
            largestRegion = self.get_large_regions()
        while len(largestRegion) != 0:
            self.size += 100
            largestRegion = self.get_large_regions()
        while len(largestRegion) == 0:
            self.size -= 1
            largestRegion = self.get_large_regions()

        return largestRegion

    def combine_regions(self):
        newImage = copy.deepcopy(self.blackImg)
        for y in range(self.height):
            for x in range(self.width):
                for index in range(len(self.regions)):
                    if self.regions[index][y, x] == self.white:
                        newImage[y, x] = self.white
                        break
        return newImage

'''

    def mk_points_list(self, regions):
        """This creates an unedited list of points on a polygon."""
        pointsList = [None] * len(regions)
        counter = 0
        for region in regions:
            pointsList[counter] = __class__.find_centroid(region)
            counter += 1
        return pointsList

    def blacken_regions(self, regions):
        """This is just a check that the regions are correct. Be careful as this
            is a call by reference that directly edits the image."""
        for region in regions:
            for y in range(self.height):
                for x in range(self.width):
                    if region[y, x]:
                        self.img[y, x] = self.black
    
'''
