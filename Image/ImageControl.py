from . import Drawer as d
from . import Editor as e       # version 4 contains polygon detection
from . import GripEditor as g   # version 3 only

class Controller:
    
    def __init__(self):

        self.thresholdBrightness = .6
        self.weedFactor = 1/64
        
        self.drawer = d.Drawer()
        self.editor = e.Editor(img=None)
        self.grip = g.GripPipeline()

    @staticmethod
    def same_image(array1, array2):
        """Use if guaranteed non-empty deep arrays."""
        if len(array1) != len(array2):
            return False
        for i in range(len(array1)):
            if len(array1[i]) != len(array2[i]):
                return False
            for j in range(len(array1[i])):
                if array1[i][j] != array2[i][j]:
                    return False
        return True
    
    def image_grab(self, imgName, cameraNum):
        """Grabs an image. Uses an existing image if name is given. Otherwise takes an
            image using a given camera."""
        import cv2
        import time
        if imgName is None:
            cap = cv2.VideoCapture(cameraNum)
            img = cap.read()[1]
            cv2.imwrite('Camera\\' + str(int(time.time())) + '.jpg', img)
            cap.release()  # When everything done, release the capture
        else:
            img = cv2.imread('Camera\\' + imgName, 1)
    
        thresh1 = self.grip_filter(img)
        self.editor.select_img(thresh1)
        self.drawer.select_img(img)
        self.drawer.select_thresh1(thresh1)
    
    def grip_filter(self, img):
        self.grip.process(img)
        return self.grip.normalize_output
    
    def find_plant(self):
        """Finds the largest object and designates as the plant.
            Currently the most inefficient code."""
        while True:
            self.editor.max_locations(self.drawer.thresholdBrightness)
            self.editor.get_all_regions()
    
            # Find the largest region. In the case of a tie, break the tie by
                # lowering the brightness threshold.
            largestRegion = self.editor.get_largest_region()
            if len(largestRegion) == 1:
                break
            else:
                self.drawer.thresholdBrightness -= .01
    
        self.drawer.plant = largestRegion[0]        # set the largest region as the plant
    
    def find_weeds(self):
        """Determine if an object is a plant or a weed. Currently, the plant is removed, and everything
            else is designated as a weed."""
        plantFound = False
        plantIndex = None
        self.drawer.largeRegions = self.editor.get_large_regions(self.weedFactor)
        for index in range(len(self.drawer.largeRegions)):
            region = self.drawer.largeRegions[index]
            newLocation = self.editor.find_centroid(region)
            if not plantFound and __class__.same_image(region, self.drawer.plant):
                print("Location of plant:", newLocation)
                plantFound = True
                plantIndex = index
            else:
                self.drawer.weeds.append(newLocation)
        self.drawer.largeRegions.pop(plantIndex)
        print("Locations of weeds:", self.drawer.weeds)
    
    def detect_all(self):
        self.find_plant()
        self.find_weeds()
    
    def draw_all(self):
        self.drawer.outline_weeds()
        self.drawer.outline_plant()
        self.drawer.add_original()
        self.drawer.add_outlines()
        self.drawer.add_first_threshold()
    
        self.drawer.thresh2 = self.editor.combine_regions()
        self.drawer.add_second_threshold()
    
        self.drawer.display_drawings()

