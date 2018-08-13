class PolygonConstruct():

    def __init__(self, image, pointsList):
        self.pointsList = pointsList
        self.numPoints = len(self.pointsList)
        self.cartesian_edit()
        self.colinearity_edit()

        self.height = image.shape[0]
        self.width = image.shape[1]

        self.polygon = None

    def cartesian_edit(self):
        '''The purpose of this function is to ensure that no points have the same height or
            the same width. This way, we can show that a point lies on a certain side of a
            line with an inequality. This is a call by reference.'''
        heights = [0] * self.numPoints
        widths = [0] * self.numPoints
        for index in range(self.numPoints):
            counter = 0
            while (self.pointsList[index][0] + counter) in heights:
                counter += 1                # if height is taken, move down
            heights[index] = self.pointsList[index][0] + counter

            counter = 0
            while (self.pointsList[index][1] + counter) in widths:
                counter += 1                # if width is taken, move right
            widths[index] = self.pointsList[index][1] + counter

        for index in range(self.numPoints):
            self.pointsList[index] = (heights[index], widths[index])

    def colinearity_edit(self):
        '''Makes sure that no lines are actually the same line. May cause error with Cartesian
            edit, rare chance for this kind of error. Remember, first coordinate is in y direction!'''
        for index1 in range(self.numPoints):
            slopes = []
            point1 = self.pointsList[index1]
            for index2 in range(index1+1, self.numPoints):
                point2 = self.pointsList[index2]
                slope = (point2[0] - point1[0]) / (point2[1] - point1[1])
                if slope in slopes:
                    self.pointsList[index2] = (self.pointsList[index2][0] + 1, self.pointsList[index2][1])
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

    def get_point_inside_triangle(self):
        '''Takes the first three points and finds a point in the triangle formed by the first three points.
            If no point exists inside the figure, returns None.'''
        points = self.pointsList[:3]     # take only the first three points
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

        for y in range(self.height):
            for x in range(self.width):
                if self.point_inside((y, x), lines, directions):
                    return (y, x)
        return None

    @staticmethod
    def mk_lines_and_directions(points, insidePoint):
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

    def mk_polygon(self):
        '''This function makes a polygon, which represents the area that the plant of interest occupies.'''
        insidePoint = self.get_point_inside_triangle()
        points = self.pointsList[:3]     # take only the first three points        
        (lines, directions) = __class__.mk_lines_and_directions(points, insidePoint)

        # ERROR HERE!!!!!!!!!!!!!!!!!!!!!!!11
        consideredPoints = 3
        while consideredPoints != len(points):
            violatedLines = 0
            lastViolated = None
            for index in range(len(lines)):
                if not self.point_inside(self.pointsList[consideredPoints], [lines[index]], [directions[index]]):
                    violatedLines += 1
                    lastViolated = index        # remember that the index represents the first point

            if violatedLines != 0:
                for _ in range(violatedLines - 1):
                    points.pop( (lastViolated-violatedLines) % len(points) )
                points.insert(lastViolated-violatedLines, self.pointsList[consideredPoints])

                (lines, directions) = __class__.mk_lines_and_directions(points, insidePoint)
                
            consideredPoints += 1

        self.polygon = points
