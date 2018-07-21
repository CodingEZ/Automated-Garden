from matplotlib import pyplot as plt


class Drawer:

    def __init__(self, thresholdBrightness=.6, weedFactor=1/100):
        self.thresholdBrightness = thresholdBrightness
        self.weedFactor = weedFactor   # size of weeds in comparison to plant
        self.plant = None
        self.weeds = []
        self.largeRegions = None

        self.img = None
        self.thresh1 = None
        self.thresh2 = None
        self.finalImg = None

        self.drawImgs = []
        self.drawNames = []

    def change_default_settings(self, thresholdBrightness, weedFactor):
        self.thresholdBrightness = thresholdBrightness
        self.weedFactor = weedFactor

    def select_img(self, img):
        import copy
        self.img = img
        self.finalImg = copy.deepcopy(img)

    def select_thresh1(self, thresh):
        self.thresh1 = thresh

    @staticmethod
    def outline(img, largeRegions, color):
        import cv2

        for index in range(len(largeRegions)):
            contour = cv2.findContours(largeRegions[index], 1, 2)[1][0]
            cv2.drawContours(img, [contour], -1, color, 2)

    def outline_plant(self):
        """Outlines the contour of the plant."""
        color = (0, 255, 0)
        __class__.outline(self.finalImg, [self.plant], color)

    def outline_weeds(self):
        """Outlines the contour of each weed."""
        color = (255, 0, 255)
        __class__.outline(self.finalImg, self.largeRegions, color)

    def add_outlines(self):
        """Add the original image with outlines for the plant and weeds."""
        self.drawImgs.append(self.finalImg)
        self.drawNames.append('self.finalImg')

    def add_original(self):
        """Add the original image"""
        self.drawImgs.append(self.img)
        self.drawNames.append('self.img')

    def add_first_threshold(self):
        """Add the original image with outlines after it is filtered."""
        self.drawImgs.append(self.thresh1)
        self.drawNames.append('self.thresh1')

    def add_second_threshold(self):
        """Add the original image with outlines of all (separate) regions."""
        self.drawImgs.append(self.thresh2)
        self.drawNames.append('self.thresh2')

    def display_drawings(self):
        """Displays a grid of images using matplotlib."""

        numImgs = len(self.drawNames)
        # plt.figure(num=1, figsize=(4*numImgs, 4))
        if numImgs == 1:
            plt.figure(num=1, figsize=(4, 4))
            plt.subplot(1, 1, 1)
            plt.imshow(self.drawImgs[0], 'gray')
            plt.title(self.drawNames[0])
        else:
            plt.figure(num=1, figsize=(2 * numImgs, 4 * ((numImgs + 1) // 2)))
            for i in range(numImgs):
                # plt.subplot(1,numImgs,i+1)
                plt.subplot((numImgs + 1) // 2, 2, i + 1)
                plt.imshow(self.drawImgs[i], 'gray')
                plt.title(self.drawNames[i])
        plt.show()
