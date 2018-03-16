####do experiment:
####put a green dot at bottom right edge
####move stpper motor (trial & error) to make it to exactly the top left corner
####find the pixel size and stepper motor turn length ratio.

import time
#import serial
import cv2
import ImageEdit5 as ImageEdit          # version 4 contains polygon detection
import ImageGrab2 as ImageGrab
import GripEdit3 as GripEdit            # version 3 only
from matplotlib import pyplot as plt

class Project():

    def __init__(self):
        '''Calibration and set-up'''
        
        #self.unit_x = 180              # 1 x-stepper motor turn = unit_x pixels
        #self.unit_y = 180              # same for y
        #self.screen_x = ?            # stepper motor turn per 1 screen width
        #self.screen_y = ?            # vice versa

        #self.arduino = serial.Serial('COM3', 9600, timeout=.1)       # set up the serial port
        #time.sleep(3)                           # allow Arduino to reset
        
        self.plantLocations = [(), (), (), ()]
        self.numPlants = len(self.plantLocations)
        self.lastWater = None
        self.img = self.image_grab()
        self.imgEdit = GripEdit.filter(self.img)
        self.editor = ImageEdit.Editor(self.imgEdit)
        self.thresholdBrightness = .4       # .6 is the default value
        self.weeds = []
        self.weedFactor = 1/100   # size of weeds in comparison to plant

        # Initialized later
        self.regions = None
        self.plant = None
        self.startSize = None
        self.finalImg = None
        self.largeRegions = None

    def wait(self):
        try:
            byteNum = int((self.arduino.read()).decode())
        except:
            byteNum = -1

        while byteNum != 0:
            try:
                byteNum = int((self.arduino.read()).decode())
            except:
                byteNum = -1

    def arduino_move(self, right, down):
        self.arduino.write(b'0')         # haven't established yet, we need a list of commands and give each a number
        try:
            byteNum = int((self.arduino.read()).decode())
        except:
            byteNum = -1

        while byteNum != 1:
            try:
                byteNum = int((self.arduino.read()).decode())
            except:
                byteNum = -1

        right = str(right)
        down = str(down)
        for i in range(3-len(right)):
            right = '0' + right
        for j in range(3-len(down)):
            down = '0' + down
        
        for char in right:
            self.arduino.write(char.encode('utf-8'))    # need the bytes of the char
        for char2 in down:
            self.arduino.write(char2.encode('utf-8'))    # need the bytes of the char

        self.wait()

    def arduino_water(self, timeLength=10):
        '''Note: time length is in seconds.'''
        waterStart = time.time()
        while time.time() < waterStart + timeLength:
            self.arduino.write(b'2')
        self.wait()

    def water_cycle(self):
        '''Cycle through plant locations and water plants.'''
        for location in self.plantLocations:
            self.arduino_move(location)
            self.arduino_water()
        self.lastWater = time.time()

    def image_grab(self):
        img = ImageGrab.grab(0)     # built-in camera number = 0
                                    # attached camera number = 1
        #img = cv2.imread('Capture\\1521224317.jpg', 1)
        return img

    def image_plot(self, imgNames):
        num = len(imgNames)
        plt.figure(num=1, figsize=(4*num, 4))
        for i in range(num):
            plt.subplot(1,num,i+1)
            plt.imshow(eval(imgNames[i]),'gray')
            plt.title(imgNames[i])
        plt.show()

    def find_plant(self):
        '''Finds the largest object and designates as the plant.
            Currently the most inefficient code.'''
        maxPixel = self.editor.find_max()
        while True:
            locations = self.editor.max_locations(maxPixel, self.thresholdBrightness)
            self.regions = self.editor.get_all_regions(locations)

            # Find the largest region. In the case of a tie, lower the brightness threshold.
            (largestRegion, self.startSize) = self.editor.obtain_largest_region(self.regions)
            if len(largestRegion) == 1:
                break
            else:
                self.thresholdBrightness -= .01
        self.plant = largestRegion[0]        # set the largest region as the plant

    def find_weeds(self):
        '''Determine if an object is a plant or a weed. Currently, the plant is removed, and everything
            else is designated as a weed.'''
        plantFound = False
        plantIndex = None
        self.largeRegions = self.editor.keep_large_regions(self.regions, self.startSize * self.weedFactor)
        for index in range(len(self.largeRegions)):
            region = self.largeRegions[index]
            newLocation = self.editor.find_centroid(region)
            if not plantFound and ImageGrab.equalArray(region, self.plant):
                print("Location of plant:", newLocation)
                plantFound = True
                plantIndex = index
            else:
                self.weeds.append(newLocation)
        self.largeRegions.pop(plantIndex)
        print("Locations of weeds:", self.weeds)

    def draw_weeds(self):
        '''Outlines the contour of each weed.'''
        self.finalImg = self.editor.outline(self.img, self.largeRegions)
        thresh = ['self.img', 'self.imgEdit', 'self.finalImg']
        self.image_plot(thresh)

start = time.time()
control = Project()
#control.wait()           wait for arduino
control.find_plant()
control.find_weeds()
stop = time.time()
control.draw_weeds()
print("Algorithm runtime for program:", stop - start)

'''
while True:
    if (control.lastWater == None) or (time.time() - control.lastWater > 300):
        control.water_cycle()
    control.find_weeds()
    control.kill_weeds()

if time.time() - control.lastWater < 300:
'''
