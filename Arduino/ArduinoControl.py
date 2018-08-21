import time
import serial

# keep everything consistent (seconds?, centimeters?)

# command list:
#   0 : move
#       char: direction
#           u : up
#           d : down
#           l : left
#           r : right
#       number : ?
#           time (seconds) to move
#           could also use distance
#   1 : water
#       number : time (seconds) to water


class Controller:

    def __init__(self):
        """Calibration and set-up of all variables. Only one instance of the
            controller should be maintained."""
        self.lastWater = None
        self.waterInterval = 10  # minutes, should change to seconds
        self.minInterval = 10
        self.maxInterval = 20

        self.gridSize = (4, 4)
        self.squareDimensions = (15, 15)        # in centimeters
        self.curX = 0           # starting coordinate x
        self.curY = 0           # starting coordinate y
        self.unitX = 180        # 1 x-stepper motor turn = unit_x pixels
        self.unitY = 180        # same for y
        self.turnSpeed = 00     # cm per second, CURRENTLY UNKNOWN

        self.ser = None

    def make_connection(self):
        """Pick the connection with the right port."""
        try:
            #self.ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 1.0)
            #self.ser = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout = 1.0)
            self.ser = serial.Serial('\\.\COM3', baudrate = 9600, timeout = 1.0)
            print("Serial connection opened.")
        except:
            self.ser = None

    def no_connection(self):
        if self.ser is None:
            print('No Arduino was initialized')
            return True
        return False

    def close_connection(self):
        """Closes an existing connection."""
        if self.no_connection():    return
        
        self.ser.close()
        print("Serial connection closed.")

    def wait(self, period):
        """Waits until message is available to read in the serial connection.
            Need to create a timeout to avoid infinite wait."""
        if self.no_connection():    return
        
        print("Waiting ... ", end="")
        if float(serial.__version__) >= 3.0:
            while self.ser.in_waiting == 0:
                print("\nWaiting ... ", end="")
                time.sleep(period)
        else:
            while self.ser.inWaiting() == 0:
                print("\nWaiting ... ", end="")
                time.sleep(period)
        print("Finished")

    def flush_read(self):
        """Flushes everything that remains to be read."""
        print("Entered flushing ... ", end="")
        char = self.ser.read().decode()
        while char != "":
            print(char, end="")
            char = self.ser.read().decode()
        print(" Exited flushing.")

    def send_command(self, command):
        """Writes a message to an existing serial connection.
            Accepts both strings and character arrays."""
        print("Sent command ... ", end="")
        self.ser.write(str(len(command)).encode('utf-8'))
        for char in command:
            self.ser.write(char.encode('utf-8'))
        time.sleep(1.0)
        print("Finished.")

    def read_message(self):
        """Reads a message from an existing serial connection."""
        print("Read attempt ... ", end="")
        message = ""
        char = self.ser.read().decode()
            
        if char != "":
            for _ in range(int(char)):
                #print(self.ser.read())
                message += self.ser.read().decode()
            print("Message: ", message)
            return message
        print("Nothing")
        return None

    def move(self, direction, period):
        """Sends command to move in direction for given period."""
        if self.no_connection(): return

        command = '0' + direction + str(period)
        self.send_command(command)

    def water(self, period=10):
        """Sends command to water for a given period."""
        if self.no_connection(): return

        command = '1' + str(period)
        self.send_command(command)

    ##############################################################
    '''End of tested code'''
    ##############################################################

    def move_to_plant(self, cx, cy):
        if self.no_connection(): return

        dx = cx - self.curX
        dy = cy - self.curY
        if dx > 0:
            self.move('r', dx / self.turnSpeed)
        else:
            self.move('l', dx * (-1) / self.turnSpeed)
        if dy > 0:
            self.move('d', dy / self.turnSpeed)
        else:
            self.move('u', dy * (-1) / self.turnSpeed)

    def water_cycle(self):
        """Cycle through plant locations and water plants. Does not water if last water was less than
            one hour ago."""
        if self.no_connection(): return

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
        if self.no_connection(): return
        
        # self.move()
