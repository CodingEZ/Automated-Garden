import time
import serial


class ArduinoControl():

    def __init__(self):
        '''Calibration and set-up'''
        self.plantLocations = [(), (), (), ()]
        self.numPlants = len(self.plantLocations)
        self.lastWater = None
        
        self.unit_x = 180              # 1 x-stepper motor turn = unit_x pixels
        self.unit_y = 180              # same for y
        #self.screen_x = ?            # stepper motor turn per 1 screen width
        #self.screen_y = ?            # vice versa

        self.arduino = serial.Serial('COM3', 9600, timeout=.1)       # set up the serial port
        time.sleep(3)                           # allow Arduino to reset

    def wait(self):
        try:
            byteNum = int((self.arduino.read()).decode())
        except:
            byteNum = -1

        while byteNum != 0:
            try:
                byteNum = int((self.arduino.read()).decode())
            except:
                byteNum = -1

    def arduino_move(self, right, down):
        self.arduino.write(b'0')         # haven't established yet, we need a list of commands and give each a number
        try:
            byteNum = int((self.arduino.read()).decode())
        except:
            byteNum = -1

        while byteNum != 1:
            try:
                byteNum = int((self.arduino.read()).decode())
            except:
                byteNum = -1

        right = str(right)
        down = str(down)
        for i in range(3-len(right)):
            right = '0' + right
        for j in range(3-len(down)):
            down = '0' + down
        
        for char in right:
            self.arduino.write(char.encode('utf-8'))    # need the bytes of the char
        for char2 in down:
            self.arduino.write(char2.encode('utf-8'))    # need the bytes of the char

        self.wait()

    def arduino_water(self, timeLength=10):
        '''Note: time length is in seconds.'''
        '''
        waterStart = time.time()
        while time.time() < waterStart + timeLength:
            self.arduino.write(b'2')
        '''
        # send water command
        self.wait()

    def water_cycle(self):
        '''Cycle through plant locations and water plants.'''
        for location in self.plantLocations:
            self.arduino_move(location)
            self.arduino_water()
        self.lastWater = time.time()

    def kill_weed(self, location):
        self.arduino_move(location)
