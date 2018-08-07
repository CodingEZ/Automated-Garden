import cv2
import numpy as np
import copy


class Pointer:

    def __init__(self, img=None):
        self.img = img

        if img is None:
            self.height = None
            self.width = None
        else:
            (self.height, self.width) = img.shape

        self.blackImg = None
        self.maxPixel = self.find_max()
        self.maxLocations = None
        self.centroids = []             # holds all regions that pass through the filter
        self.size = None                # size of plant

    def select_img(self, img):
        self.img = img
        (self.height, self.width) = img.shape
        self.maxPixel = self.find_max()
        self.blackImg = np.array([[0] * self.width for _ in range(self.height)], dtype='uint8')
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

        maxLocations = self.maxLocations    # improvement on runtime

        for y in range(self.height):
            for x in range(self.width):
                if thresh[y, x] == 255:
                    maxLocations[y, x] = 1

    def find_next_region(self, startY=0):
        """Goes through each ROW from LEFT TO RIGHT until it encounters the first
            true location. Skips every other column and row."""
        maxLocations = self.maxLocations        # improvement on runtime

        for y in range(startY, self.height, 2):
            for x in range(0, self.width, 2):
                if maxLocations[y, x]:
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

        maxLocations = self.maxLocations        # improvement on runtime

        maxLocations[start[0], start[1]] = 0  # first spot is already checked

        while len(checkLocations) > 0:
            for check in checkLocations:
                if check not in checkedLocations:
                    checkedLocations.add(check)
                    if check[0] != 0 and maxLocations[check[0]-1, check[1]] == 1:
                        newCheckLocations.add((check[0]-1, check[1]))
                        maxLocations[check[0]-1, check[1]] = 0
                    if check[0]+1 != self.height and maxLocations[check[0]+1, check[1]] == 1:
                        newCheckLocations.add((check[0]+1, check[1]))
                        maxLocations[check[0]+1, check[1]] = 0
                    if check[1] != 0 and maxLocations[check[0], check[1]-1] == 1:
                        newCheckLocations.add((check[0], check[1]-1))
                        maxLocations[check[0], check[1]-1] = 0
                    if check[1]+1 != self.width and maxLocations[check[0], check[1]+1] == 1:
                        newCheckLocations.add((check[0], check[1]+1))
                        maxLocations[check[0], check[1]+1] = 0
            for check2 in checkLocations:
                region[check2[0], check2[1]] = 1
            checkLocations = newCheckLocations
            newCheckLocations = set()

        return region

    def get_all_centroids(self):
        self.centroids = []
        start = self.find_next_region()
        while start is not None:
            region = self.get_connected_region(start)
            self.centroids.append(__class__.find_centroid(region))
            start = self.find_next_region(start[0])

    def get_crop(self):
        pass
        # under development

    def get_weeds(self):
        pass
        # under development
