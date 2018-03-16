import cv2
import numpy as np
import time

def equalArray(array1, array2):
    '''Use if guaranteed non-empty deep arrays.'''
    if len(array1) != len(array2):
        return False
    elif isinstance(array1[0], int) or isinstance(array1[0], np.uint8):
        for index in range(len(array1)):
            if array1[index] != array2[index]:
                return False
        return True
    else:
        for index in range(len(array1)):
            if not equalArray(array1[index], array2[index]):
                return False
        return True

def grab(cameraNumber):
    cap = cv2.VideoCapture(cameraNumber)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    # name, fourcc code, frame rate, frame size, isColor tag
    output = cv2.VideoWriter('output.avi', fourcc, 10.0, (640,480), isColor=False)

    frame = cap.read()[1]
    cv2.imwrite('Capture\\' + str(int(time.time())) + '.jpg', frame)
                
    # When everything done, release the capture
    cap.release()
    output.release()
    cv2.destroyAllWindows()
    return frame
