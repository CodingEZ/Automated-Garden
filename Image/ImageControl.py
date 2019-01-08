from . import BrightnessEditor as b
from . import GripEditor as g
import cv2


class Controller:
    
    def __init__(self):
        self.img = None
        self.imgOutlined = None
        self.center = None
        self.contours = []
        self.centroids = []
        self.plant = None
        self.weeds = []

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
        import cv2, time, copy
        if imgName is None:
            cap = cv2.VideoCapture(cameraNum)
            img = cap.read()[1]
            cv2.imwrite('Camera\\' + str(int(time.time())) + '.jpg', img)
            cap.release()  # When everything done, release the capture
        else:
            img = cv2.imread('Camera\\' + imgName, 1)

        self.contours = []
        self.centroids = []
        self.plant = None
        self.weeds = []

        self.img = img
        self.imgOutlined = copy.deepcopy(img)
        (height, width, channels) = img.shape
        self.center = (width/2, height/2)

    def get_contours(self):
        return g.GripPipeline().process(self.img)

    def sum_contour_areas(self):
        contour_sum = 0
        for contour in self.contours:
            contour_sum += cv2.contourArea(contour)
        return contour_sum

    @staticmethod
    def get_centroid(contour):
        M = cv2.moments(contour)
        if M is not None:
            # error in calculating centroid
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY
        else:
            return None

    def get_all_centroids(self):
        centroids = []
        for contour in self.contours:
            centroid = __class__.get_centroid(contour)
            if centroid is not None:
                centroids.append(centroid)
        return centroids

    def differentiate_plants(self):
        def distance(point1, point2):
            return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

        plant = None
        weeds = []
        minDistance = self.center[0]**2 + self.center[1]**2
        for (point, contour) in zip(self.centroids, self.contours):
            newDistance = distance(self.center, point)
            if newDistance < minDistance:
                if plant is not None:
                    weeds.append(plant)
                minDistance = newDistance
                plant = contour
            else:
                weeds.append(contour)
        return plant, weeds

    def find_plants(self):
        self.contours = self.get_contours()
        ratio = self.sum_contour_areas() / self.img.size
        print('Contour ratio: ', ratio)

        self.img = b.adjust_brightness(self.img, ratio)
        self.contours = self.get_contours()
        self.centroids = self.get_all_centroids()
        self.plant, self.weeds = self.differentiate_plants()

    def draw_all(self):
        cv2.drawContours(self.imgOutlined, self.weeds, -1, (255, 0, 0), 2)
        cv2.drawContours(self.imgOutlined, [self.plant], -1, (0, 255, 0), 2)
        cv2.imshow('Img', self.imgOutlined)

