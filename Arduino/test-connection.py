import serial
import time

class Controller():

    def __init__(self):
        self.ser = None
        self.make_connection()

    def make_connection(self):
        """Pick the connection with the right port."""
        try:
            self.ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 1.0)
            #self.ser = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout = 1.0)
            print("Serial connection opened!")

            # Flush everything before proceeding
            self.ser.flushInput()
            self.flush_read()
        except:
            self.ser = None

    def is_connected(self):
        return self.ser is not None

    # internal check, refrain from using this beyond internal programming
    def _check_connection(self):
        if self.ser is None:
            raise Exception("Arduino not connected or already closed!")

    def close_connection(self):
        """Closes an existing connection."""
        self._check_connection()
        
        self.ser.close()
        print("Serial connection closed.")

    def _wait(self, period):
        """Waits until message is available to read in the serial connection."""
        print("In waiting ... ", end="")
        self._check_connection()
        
        if float(serial.__version__) >= 3.0:
            while self.ser.in_waiting == 0:
                time.sleep(period)
                print(" ... ", end="")
        else:
            while self.ser.inWaiting() == 0:
                time.sleep(period)
                print(" ... ", end="")

    def flush_read(self):
        """Flushes everything that remains to be read."""
        print("Entering flushing ... ", end="")
        self._check_connection()
        
        char = self.ser.read().decode()
        while char != "":
            print(char, end="")
            char = self.ser.read().decode()
        print(" Exited flushing.")

    def send_command(self, command):
        """Writes a message to an existing serial connection.
            Accepts both strings and character arrays."""
        print("Sending command ... ", end="")
        self._check_connection()
        
        print(len(command), command, end=" ... ")
        self.ser.write(str(len(command)).encode('utf-8'))
        for char in command:
            self.ser.write(char.encode('utf-8'))
        time.sleep(1.0)

        self._wait(1)
        print("Finished")

    def read_message(self):
        """Reads a message from an existing serial connection."""
        print("Read attempt ... ", end="")
        self._check_connection()
        
        message = ""
        char = self.ser.read().decode()
            
        if char != "":
            for _ in range(int(char)):
                #print(self.ser.read())
                message += self.ser.read().decode()
        else:
            message = None
        
        print("Finished")
        return message

# Functions that send specific commands --------------------------------

    def move(self, direction, period):
        """Function that will move the garden tools"""
        self._check_connection()

        command = '0' + direction + str(period)
        self.send_command(command)

    def water(self, period=10):
        """Function to water."""
        self._check_connection()

        command = '1' + str(period)
        self.send_command(command)


if __name__ == '__main__':
    def test_response(command, timeout=2):
        print("Start of serial communication test!")
        control = Controller()

        if control.is_connected():
            control.send_command(command)
            message = control.read_message()
            print("Message: ", message)
            
            control.close_connection()
        print("End of serial communication test!\n")


    # no error if serial port is closed and opened again,
    # error if serial port kept open

    command1 = ['0', 'r', '2']
    test_response(command1)

    command2 = ['1', 'r', '2']
    test_response(command2)

