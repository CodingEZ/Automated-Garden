import time
import ImageDetection
import ArduinoControl

imgName = None
cameraNum = 0    # built-in cameraNum = 0
                    # attached cameraNum = 1

#control = ArduinoControl.ArduinoControl()
#control.wait()           wait for arduino

start = time.time()
detect = ImageDetection.Detector(thresholdBrightness=.4)
detect.image_grab(imgName, cameraNum)
detect.find_plant()
detect.find_weeds()
stop = time.time()
print("Algorithm runtime for program:", stop - start)

detect.draw_weeds()
detect.draw_plant()
detect.display_drawings()

