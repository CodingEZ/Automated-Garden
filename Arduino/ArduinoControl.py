import time
import serial


# command list:
#   0 : move
#       direction
#           u : up
#           d : down
#           l : left
#           r : right
#       number
#           time (seconds) to move
#           could also use distance
#   1 : water
#       number
#           time (seconds) to water


class Controller:

    def __init__(self):
        """Calibration and set-up"""
        self.lastWater = None
        self.waterInterval = 10  # minutes
        self.minInterval = 10
        self.maxInterval = 20

        self.gridSize = (4, 4)
        self.squareDimensions = (15, 15)        # in centimeters
        self.curX = 0           # starting coordinate x
        self.curY = 0           # starting coordinate y
        self.unitX = 180        # 1 x-stepper motor turn = unit_x pixels
        self.unitY = 180        # same for y
        self.turnSpeed = 00     # cm per second, CURRENTLY UNKNOWN

        try:
            self.arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=2)  # set up the serial port
            time.sleep(5)          # allow Arduino to reset
        except:
            self.arduino = None

    def is_busy(self):
        if self.arduino == None:    return

        arduinoMessage = self.arduino.read().decode()
        # more work to be done here

    def move(self, direction, period):
        if self.arduino == None:
            print('No Arduino was initialized')
            return

        message = '0' + direction + str(period)
        self.arduino.write(message.encode('utf-8'))    # need the bytes of the char

    def move_to_plant(self, cx, cy):
        if self.arduino == None:
            print('No Arduino was initialized')
            return

        dx = cx - self.curX
        dy = cy - self.curY
        if dx > 0:
            self.move('r', dx / self.turnSpeed)
        elif dx < 0:
            self.move('l', dx * (-1) / self.turnSpeed)
        if dy > 0:
            self.move('d', dy / self.turnSpeed)
        elif dy < 0:
            self.move('u', dy * (-1) / self.turnSpeed)

    def water(self, period=10):
        if self.arduino == None:
            print('No Arduino was initialized')
            return

        message = '0' + str(period)
        self.arduino.write(message.encode('utf-8'))

    def water_cycle(self):
        """Cycle through plant locations and water plants. Does not water if last water was less than
            one hour ago."""
        if self.arduino == None:
            print('No Arduino was initialized')
            return

        if isinstance(self.lastWater, int) and time.time() - self.lastWater < 3600:
            return      # 3600 seconds = 1 hour

        self.move_to_plant(0, 0)        # start at the top left and work down
        for row in range(self.gridSize[0]):
            for col in range(self.gridSize[1]):
                self.move_to_plant(col, row)       # x relates to column number, y relates to row number
                self.water()
        self.lastWater = time.time()
        self.move_to_plant(0, 0)        # return to top left

    def kill_weed(self, pixelLocation):
        if self.arduino == None:
            print('No Arduino was initialized')
            return

        # self.move()
