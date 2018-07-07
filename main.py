import time
import ImageDetection
import ArduinoControl

imgName = '1521224317.jpg'
#imgName = '1516378704.jpg'
#imgName = '1520808085.jpg'
#imgName = '1.jpg'
cameraNum = 0    # built-in cameraNum = 0, attached cameraNum = 1

#control = ArduinoControl.ArduinoControl()
#control.wait()           wait for arduino

start = time.time()
detect = ImageDetection.Detector(thresholdBrightness=.35,
                                 weedFactor=1/16)
detect.image_grab(imgName, cameraNum)
detect.find_plant()
detect.find_weeds()
stop = time.time()
print("Algorithm runtime for program:", stop - start)

detect.outline_weeds()
detect.outline_plant()
detect.draw_outlines()
detect.draw_first_threshold()
detect.draw_second_threshold()
detect.display_drawings()

'''
while True:
    if (control.lastWater == None) or (time.time() - control.lastWater > 300):
        control.water_cycle()
    detect = ImageDetection.Detector(thresholdBrightness=.4)
    detect.image_grab(imgName, cameraNum)
    detect.find_plant()
    detect.find_weeds()
    for location in detect.weeds:
        control.kill_weed(location)

if time.time() - control.lastWater < 300:
'''
