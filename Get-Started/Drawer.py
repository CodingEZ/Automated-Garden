import cv2


def outline(img, contours, color):
    for index in range(len(contours)):
        cv2.drawContours(img, contours, -1, color, 2)

def outline_plant(imgOutlined, plant):
    """Outlines the contour of the plant."""
    color = (0, 255, 0)
    outline(imgOutlined, [plant], color)

def outline_weeds(imgOutlined, weeds):
    """Outlines the contour of each weed."""
    color = (255, 0, 0)
    outline(imgOutlined, weeds, color)

def show_img(img):
    cv2.imshow('Img', img)



