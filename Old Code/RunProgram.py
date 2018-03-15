####do experiment:
####put a green dot at bottom right edge
####move stpper motor (trial & error) to make it to exactly the top left corner
####find the pixel size and stepper motor turn length ratio.

from enum import Enum
import time
import serial
import cv2
import ImageEdit5 as ImageEdit          # version 4 contains polygon detection
import ImageGrab
import GripEdit3 as GripEdit            # version 3 only
import PolygonDetect2 as PolygonDetect  # currently has errors

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
        self.thresholdBrightness = .5
        self.weeds = []
        self.weedFactor = 1/100   # size of weeds in comparison to plant

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
        #img = ImageGrab.grab(0)     # built-in camera number = 0
                                    # attached camera number = 1
        img = cv2.imread('Capture\\1520992405.jpg', 1)
        return img

    def find_weeds(self):
        start = time.time()

        # Threshold above a certain brightness, which represents area
        maxPixel = self.editor.find_max()
        while True:
            locations = self.editor.max_locations(maxPixel, self.thresholdBrightness)
                # .6 is the default value for thresholdBrightness
            regions = self.editor.get_all_regions(locations)

            # Find the largest region. In the case of a tie, lower the brightness threshold.
            (largestRegion, startSize) = self.editor.obtain_largest_region(regions)
            if len(largestRegion) == 1:
                break
            else:
                self.thresholdBrightness -= .01
        plant = largestRegion[0]        # set the largest region as the plant

        # Determine if plant or weed
        largeRegions = self.editor.keep_large_regions(regions, startSize * self.weedFactor)
        for region in largeRegions:
            newLocation = self.editor.find_next_location(region)
            if ImageGrab.equalArray(region, plant):
                print("Location of plant:", newLocation)
            else:
                self.weeds.append(newLocation)
        print("Locations of weeds:", self.weeds)

        # Use polygons only when plant has multiple leaves
        '''
        pointsList = editor.mk_points_list(largeRegions)
        if len(pointsList) > 2:
            constructor = PolygonDetect.PolygonConstruct(self.img, pointsList)
            constructor.mk_polygon()
            print("Constructed polygon:", constructor.polygon)
        else:
            print("Error! Not enough points to make a polygon:", pointsList)
        '''
        
        stop = time.time()
        print("Algorithm runtime for program:", stop - start)

        finalImg = self.editor.circle(self.img, self.weeds)
        cv2.imshow('window', self.imgEdit)
        #cv2.imshow('window', finalImg)

x = Project()
#x.wait()           wait for arduino
x.find_weeds()
print(x.weeds)

'''
while True:
    if (lastWater == None) or (time.time() - lastWater > 300):
        x.water_cycle()
    x.find_weeds()
    x.kill_weeds()

if time.time() - x.lastWater < 300:
'''


###############################################################################3



"""
img = cv2.imread('EditedTestLeaves.jpg', 0)
cv2.imshow('Window', img)

blacken_regions(regions, img)

# try to make any image possible
# next step: detect if potential weeds are inside boundary of plant
#    if yes, not a weed
#    if no, probably a weed
"""

