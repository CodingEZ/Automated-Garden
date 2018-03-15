import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=.1)
time.sleep(5)

while True:
    data = arduino.read()
    if len(data.decode()) > 0:
        print(int( data.decode() ))
    arduino.write(b'1')
