import cv2
import numpy as np

class Editor():

    def __init__(self, img):
        self.img = img
        (self.height, self.width) = img.shape
        print('Height: ', self.height, ', Width: ', self.width)

    def find_max(self):
        '''Finds the pixel of maximum brightness. This value is usually 255.'''
        maxPixel = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.img[y, x] > maxPixel:
                    maxPixel = self.img[y, x]
        return maxPixel

    def max_locations(self, maxPixel, thresholdBrightness=.6):
        '''Finds all locations above a threshold brightness compared to the maximum brightness.
            The default is .6 (out of 1.0). No need to calculate the exact value of brightness.'''
        locations = np.array( [[False] * self.width for _ in range(self.height)] )
        counter = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.img[y, x] >= thresholdBrightness * maxPixel:
                    # .6 is a threshold
                    locations[y, x] = True
                    counter += 1
        return locations

    def find_next_location(self, locations):
        '''Goes through each ROW from LEFT TO RIGHT until it encounters the first true location.'''
        for y in range(self.height):
            for x in range(self.width):
                if locations[y, x]:
                    return (y, x)
        return None

    def get_connected_region(self, location, locations):
        '''Obtains a single. The format of the region is a numpy array that has the
            height and width of the original image. Be careful as this is a call by
            reference that directly edits the array of locations.'''
        checkLocations = [location]
        newCheckLocations = []
        checkedLocations = []
        region = np.array( [[False] * self.width for _ in range(self.height)] )
        locations[location[0], location[1]] = False  # first spot is already checked
        while len(checkLocations) > 0:
            for check in checkLocations:
                if check in checkedLocations:
                    pass
                else:
                    checkedLocations.append(check)
                    if check[0] != 0:
                        if locations[check[0]-1, check[1]]:
                            newCheckLocations.append((check[0]-1, check[1]))
                            locations[check[0]-1, check[1]] = False
                    if check[0]+1 != self.height:
                        if locations[check[0]+1, check[1]]:
                            newCheckLocations.append((check[0]+1, check[1]))
                            locations[check[0]+1, check[1]] = False
                    if check[1] != 0:
                        if locations[check[0], check[1]-1]:
                            newCheckLocations.append((check[0], check[1]-1))
                            locations[check[0], check[1]-1] = False
                    if check[1]+1 != self.width:
                        if locations[check[0], check[1]+1]:
                            newCheckLocations.append((check[0], check[1]+1))
                            locations[check[0], check[1]+1] = False
            for check2 in checkLocations:
                region[check2[0], check2[1]] = True
            checkLocations = newCheckLocations
            newCheckLocations = []
        return region

    def get_all_regions(self, locations):
        '''Obtains each region. Returns a list of regions.'''
        regions = []
        start = self.find_next_location(locations)
        while start != None:
            region = self.get_connected_region(start, locations)
            regions.append(region)
            start = self.find_next_location(locations)
        return regions

    def region_length(self, region):
        '''Finds the size of a region in pixels.'''
        counter = 0
        for y in range(self.height):
            for x in range(self.width):
                if region[y][x]:
                    counter += 1
        return counter

    def keep_large_regions(self, regions, thresholdSize=100):
        '''Take the regions and filters those that are below threshold size. Default threshold size
            is 100 pixels. Be careful as this is a call by reference that directly edits the list
            of regions.'''
        for i in range(len(regions)-1, -1, -1):
            if self.region_length(regions[i]) < thresholdSize:
                regions.pop(i)
            else:
                pass
                #print(len(regions[i]))

    def combine_regions(self, regions):
        newImage = np.array( [[False] * self.width] for _ in range(self.height) )
        for y in range(self.height):
            for x in range(self.width):
                boolArray = []
                for region in regions:
                    boolArray.append(region[y, x])
                if True in boolArray:
                    newImage[y, x] = True
        return newImage

    def blacken_regions(self, regions):
        '''This is just a check that the regions are correct. Be careful as this is a call by
            reference that directly edits the image.'''
        for region in regions:
            for y in range(self.height):
                for x in range(self.width):
                    if region[y, x]:
                        self.img[y, x] = 0

    def mk_points_list(self, regions):
        '''This creates an unedited list of points on a polygon.'''
        pointsList = [None] * len(regions)
        counter = 0
        for region in regions:
            pointsList[counter] = self.find_next_location(region)
            counter += 1
        return pointsList

    def cartesian_edit(self, points):
        '''The purpose of this function is to ensure that no points have the same height or
            the same width. This way, we can show that a point lies on a certain side of a
            line with an inequality. This is a call by reference.'''
        heights = []
        widths = []
        for point in points:
            counter = 0
            while (point[0]+counter) in heights:
                counter += 1                    # if height is taken, move down
            heights.append(point[0]+counter)

            counter = 0
            while (point[1]+counter) in widths:
                counter += 1                    # if width is taken, move right
            widths.append(point[1]+counter)

        for index in range(len(points)):
            points[index] = (heights[index], widths[index])

    def colinearity_edit(self, points):
        '''Makes sure that no lines are actually the same line. May cause error with Cartesian
            edit, rare chance for this kind of error. Remember, first coordinate is in y direction!'''
        for index1 in range(len(points)):
            slopes = []
            point1 = points[index1]
            for index2 in range(index1+1, len(points)):
                point2 = points[index2]
                slope = (point2[0] - point1[0]) / (point2[1] - point1[1])
                if slope in slopes:
                    points[index2][0] += 1
                    slope = (point2[0] - point1[0]) / (point2[1] - point1[1])
                slopes.append(slope)

    def point_inside(self, point, lines, directions):
        '''Checks to make sure a point is inside a list of lines.'''
        for index in range(len(lines)):
            if directions[index]:
                if point[1]*lines[index][0] + lines[index][1] < point[0]:
                    return False
            else:
                if point[1]*lines[index][0] + lines[index][1] > point[0]:
                    return False
        return True

    def get_point_inside_triangle(self, pointsList):
        '''Takes the first three points and finds a point in the triangle formed by the first three points.
            If no point exists inside the figure, returns None.'''
        points = pointsList[:3]     # take only the first three points
        lines = []
        directions = []
        
        for i in range(len(points)):
            point1 = points[i%3]
            point2 = points[(i+1)%3]
            point3 = points[(i+2)%3]
            slope = (point2[0] - point1[0]) / (point2[1] - point1[1])
            intercept = ((point2[1]*point1[0] - point1[1]*point2[0])) / (point2[1] - point1[1])     # y-intercept
            lines.append((slope, intercept))

            if point3[0] * slope + intercept > point3[1]:
                directions.append(True)         # True means the point is 'above' the line
            else:
                directions.append(False)

        for y in range(height):
            for x in range(width):
                if point_inside((y, x), lines, directions):
                    return (y, x)
        return None

    def mk_lines_and_directions(self, points, insidePoint):
        length = len(points)
        lines= []
        directions = []
        
        for i in range(length):
            point1 = points[i%length]
            point2 = points[(i+1)%length]
            slope = (point2[0] - point1[0]) / (point2[1] - point1[1])
            intercept = ((point2[1]*point1[0] - point1[1]*point2[0])) / (point2[1] - point1[1])     # y-intercept
            lines.append((slope, intercept))

            if insidePoint[1] * slope + intercept > insidePoint[0]:
                directions.append(True)         # True means the point is 'above' the line
            else:
                directions.append(False)
        return (lines, directions)
                
    def mk_polygon(self, points):
        '''This function makes a polygon, which represents the area that the plant of interest occupies.'''
        insidePoint = self.get_point_inside_triangle(points)
        points = pointsList[:3]     # take only the first three points
        
        info = self.mk_lines_and_directions(points, insidePoint)
        lines = info[0]
        directions = info[1]

        consideredPoints = 3
        while consideredPoints != len(points):
            violatedLines = 0
            lastViolated = None
            for index in range(len(lines)):
                if not self.point_inside(pointsList[consideredPoints], [lines[index]], [directions[index]]):
                    violatedLines += 1
                    lastViolated = index        # remember that the index represents the first point

            if violatedLines == 0:
                pass        # ignore point
            else:
                for _ in range(violatedLines - 1):
                    points.pop( (lastViolated-violatedLines) % len(points) )
                points.insert(lastViolated-violatedLines, pointsList[consideredPoints])

                # following algorithm needs editing
                '''
                if violatedLines == 1:
                    points.insert(index+1, pointsList[consideredPoints])
                    [lines, directions] = mk_lines_and_directions(points, insidePoint)
                elif violatedLines == 2:
                    points.pop(index)
                    points.insert(index, pointsList[consideredPoints])
                elif violatedLines == 3:
                    pass        
                '''

                info = self.mk_lines_and_directions(points, insidePoint)
                lines = info[0]
                directions = info[1]
                
            consideredPoints += 1

        return points

"""
img = cv2.imread('EditedTestLeaves.jpg', 0)
cv2.imshow('Window', img)

(height, width) = img.shape
print('Height: ', height, ', Width: ', width)

maxPixel = find_max(img)
locations = max_locations(img, maxPixel, .6)    # .6 is default
regions = get_all_regions(locations)
keep_large_regions(regions, 100)                # 100 is default
pointsList = mk_points_list(regions)
cartesian_edit(pointsList)
colinearity_edit(pointsList)
print(pointsList)
mk_polygon(pointsList)


'''
locations2 = max_locations(img, maxPixel, .5)
regions2 = get_all_regions(locations2)
keep_large_regions(regions2)
'''

blacken_regions(regions, img)

print('Plant regions: ', len(regions))
#print('Plant regions: ', len(regions), ', All regions: ', len(regions2))
#print('Potential weeds: ', len(regions2)-len(regions))
cv2.imshow('Window1', img)

# try to make any image possible
# next step: detect if potential weeds are inside boundary of plant
#    if yes, not a weed
#    if no, probably a weed
"""

