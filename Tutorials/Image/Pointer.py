import cv2
from . import GripEditor as g

def distance(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

def get_contours(img):
    return g.GripPipeline().process(img)

def get_all_centroids(contours):
    centroids = []
    for contour in contours:
        centroid = get_centroid(contour)
        if centroid is not None:
            centroids.append(centroid)
    return centroids

def get_centroid(contour):
    M = cv2.moments(contour)
    if M is not None:
        # error in calculating centroid
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    else:
        return None

def get_plants(contours, centroids, center):
    plant = None
    weeds = []
    minDistance = center[0]**2 + center[1]**2
    for (point, contour) in zip(centroids, contours):
        newDistance = distance(center, point)
        if newDistance < minDistance:
            if plant is not None:
                weeds.append(plant)
            minDistance = newDistance
            plant = contour
        else:
            weeds.append(contour)
    return plant, weeds
