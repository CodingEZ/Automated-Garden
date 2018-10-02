import cv2, time, copy

def image_grab(imgName, cameraNum):
    """Grabs an image. Uses an existing image if name is given. Otherwise takes
        an image using a given camera."""
    if imgName is None:
        cap = cv2.VideoCapture(cameraNum)
        img = cap.read()[1]
        cv2.imwrite(str(int(time.time())) + '.jpg', img)
        cap.release()  # When everything done, release the capture
    else:
        img = cv2.imread(imgName)
        
    cv2.imshow("img", img)

image_grab("2.jpg", None)
#image_grab(None, 0)
#image_grab(None, 1)
