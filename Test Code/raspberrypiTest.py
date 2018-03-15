import serial
import RPi.GPIO as GPIO
import time
import cv2

## https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

ser = serial.Serial("/dev/ttyACM0", 9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate = 9600         # baudrate is bits per second that can be transferred

def blink(pin):    
    GPIO.output(pin, GPIO.HIGH)     # light up
    time.sleep(1)  
    GPIO.output(pin, GPIO.LOW)      # light down
    time.sleep(1)  
    return

pinNumber = 11
#mode = GPIO.getmode()
#if mode == None:
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinNumber, GPIO.OUT)     # set up as an output

# read from Arduino
'''
while True:    
    read_ser = ser.readline()
    # maybe use ser.read() ?
    print(read_ser)
    if (read_ser=="Hello From Arduino!"):
        blink(11)
        
    asciiChar = cv2.waitKey(25) & 0xFF
    if asciiChar == ord('q'):
        break
'''

# write to serial, from which arduino reads
'''
time.sleep(5)       # allow time for arduino to reset
while True:
    ser.write(info)

    asciiChar = cv2.waitKey(25) & 0xFF
    if asciiChar == ord('q'):
        break
'''

GPIO.cleanup()
