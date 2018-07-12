from . import Drawer as d
from . import Editor as e       # version 4 contains polygon detection
from . import GripEditor as g   # version 3 only

thresholdBrightness = .6
weedFactor = 1/64

drawer = d.Drawer()
editor = e.Editor(img=None)
grip = g.GripPipeline()

def sameImage(array1, array2):
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

def image_grab(imgName, cameraNum):
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

    thresh1 = grip_filter(img)
    editor.select_img(thresh1)
    drawer.select_img(img)
    drawer.select_thresh1(thresh1)

def grip_filter(img):
    grip.process(img)
    return grip.normalize_output

def find_plant():
    """Finds the largest object and designates as the plant.
        Currently the most inefficient code."""
    while True:
        editor.max_locations(drawer.thresholdBrightness)
        editor.get_all_regions()

        # Find the largest region. In the case of a tie, break the tie by
            # lowering the brightness threshold.
        largestRegion = editor.get_largest_region()
        if len(largestRegion) == 1:
            break
        else:
            drawer.thresholdBrightness -= .01

    drawer.plant = largestRegion[0]        # set the largest region as the plant

def find_weeds():
    """Determine if an object is a plant or a weed. Currently, the plant is removed, and everything
        else is designated as a weed."""
    plantFound = False
    plantIndex = None
    drawer.largeRegions = editor.get_large_regions(weedFactor)
    for index in range(len(drawer.largeRegions)):
        region = drawer.largeRegions[index]
        newLocation = editor.find_centroid(region)
        if not plantFound and sameImage(region, drawer.plant):
            print("Location of plant:", newLocation)
            plantFound = True
            plantIndex = index
        else:
            drawer.weeds.append(newLocation)
    drawer.largeRegions.pop(plantIndex)
    print("Locations of weeds:", drawer.weeds)

def detect_all():
    find_plant()
    find_weeds()

def draw_all():
    drawer.outline_weeds()
    drawer.outline_plant()
    drawer.add_original()
    drawer.add_outlines()
    drawer.add_first_threshold()

    drawer.thresh2 = editor.combine_regions()
    drawer.add_second_threshold()

    drawer.display_drawings()

