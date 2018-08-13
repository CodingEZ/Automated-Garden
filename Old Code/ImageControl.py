# EDIT WHAT TO SEND TO THE DRAWER

from Image import Drawer as d
from Image import GripEditor as g  # version 3 only
from Image import Pointer as p  # version 4 contains polygon detection


class Controller:
    
    def __init__(self):

        self.thresholdBrightness = .6
        self.minBrightness = .01
        self.maxBrightness = 1
        
        self.drawer = d.Drawer()
        self.pointer = p.Pointer(img=None)
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
        cv2.imshow('name', thresh1)
        self.pointer.select_img(thresh1)
        self.drawer.select_img(img)
        self.drawer.select_thresh1(thresh1)
    
    def grip_filter(self, img):
        self.grip.process(img)
        return self.grip.normalize_output
    
    def find_plants(self):
        self.pointer.max_locations()
        try:
            self.pointer.get_all_centroids()
            self.pointer.get_plants()
            self.drawer.plant = self.pointer.plant
            self.drawer.weeds = self.pointer.weeds
        except Exception as e:
            print(e)
    
    def draw_all(self):
        self.drawer.outline_weeds()
        self.drawer.outline_plant()
        self.drawer.add_original()
        self.drawer.add_outlines()
        self.drawer.add_first_threshold()
        self.drawer.display_drawings()

