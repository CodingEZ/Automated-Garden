import cv2
import time

def grab(cameraNumber):
    cap = cv2.VideoCapture(cameraNumber)
    frame = cap.read()[1]
    cv2.imwrite('Capture\\' + str(int(time.time())) + '.jpg', frame)
                
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return frame
