from . import Drawer as d
from . import Pointer as p


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
            cv2.imwrite(str(int(time.time())) + '.jpg', img)
            cap.release()  # When everything done, release the capture
        else:
            img = cv2.imread(imgName, 1)

        self.contours = []
        self.centroids = []
        self.plant = None
        self.weeds = []

        self.img = img
        self.imgOutlined = copy.deepcopy(img)
        (height, width, channels) = img.shape
        self.center = (width/2, height/2)

    def find_plants(self):
        self.contours = p.get_contours(self.img)
        self.centroids = p.get_all_centroids(self.contours)
        self.plant, self.weeds = p.get_plants(self.contours, self.centroids, self.center)
    
    def draw_all(self):
        d.outline_weeds(self.imgOutlined, self.weeds)
        d.outline_plant(self.imgOutlined, self.plant)
        d.show_img(self.imgOutlined)

