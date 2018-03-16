import time
import ImageDetection

start = time.time()
control = ImageDetection.Detector()
#control.wait()           wait for arduino
control.find_plant()
control.find_weeds()
stop = time.time()
control.draw_weeds()
control.draw_plant()
control.display_drawings()
print("Algorithm runtime for program:", stop - start)
