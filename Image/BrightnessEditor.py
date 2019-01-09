import cv2
from PIL import Image, ImageStat
import numpy as np
import math

DEFAULT_ALPHA = 1     # contrast, 1 is no change
DEFAULT_BETA = 0        # raw brightness, max of 255, 0 is no change
DEFAULT_GAMMA = 1     # saturation factor, keep under 5, 1 does nothing

TARGET_BRIGHTNESS = 50 / .015
TEST_INCREMENTAL = True

def perceived_brightness(img_name):
    img = Image.open(img_name)
    stat = ImageStat.Stat(img)
    r,g,b = stat.mean
    return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def brightness(img):
    avgSum = 0
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    width, height = img_grey.shape
    for i in range(width):
        for j in range(height):
            avgSum += img_grey[i][j]
    return avgSum / (width * height)

def basic_linear_transform(img, alpha, beta):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def gamma_correction(img, gamma):
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    img_gamma_corrected = cv2.LUT(img, lookUpTable)
    return img_gamma_corrected

def adjust_brightness(img_original, ratio):
    print(brightness(img_original))

    #img_corrected = np.empty((img_original.shape[0], img_original.shape[1], img_original.shape[2]), img_original.dtype)
    #img_gamma_corrected = np.empty((img_original.shape[0], img_original.shape[1], img_original.shape[2]), img_original.dtype)

    if TEST_INCREMENTAL:
        # beta adjustments first
        new_img = img_original
        beta = TARGET_BRIGHTNESS * ratio - brightness(new_img)
        print("Start beta and brightness:", beta, brightness(new_img))
        while abs(beta) > 1:
            if beta > 0:
                new_img = basic_linear_transform(new_img, 1 - abs(beta / 255), beta)
            else:
                new_img = basic_linear_transform(new_img, 1 - abs(beta / 255), 0)
            beta = TARGET_BRIGHTNESS * ratio - brightness(new_img)
            print(beta, brightness(new_img))
    else:
        beta = TARGET_BRIGHTNESS * ratio - brightness(img_original)
        if beta > 0:
            new_img = basic_linear_transform(img_original, 1 - abs(beta / 255), beta)
        else:
            new_img = basic_linear_transform(img_original, 1 - abs(beta / 255), 0)
        print(brightness(new_img))

    #cv2.imshow("Brightness and contrast adjustments", new_img)
    new_img2 = gamma_correction(new_img, DEFAULT_GAMMA)
    return new_img2


if __name__ == '__main__':
    IMG_FILE = '2.jpg'
    #IMG_FILE = '1521224317.jpg'
    img_first = cv2.imread(IMG_FILE)
    img_new = adjust_brightness(img_first, .015)
    
    cv2.imshow("Gamma correction", img_new)
    cv2.imshow("No correction", img_first)
    cv2.waitKey()
