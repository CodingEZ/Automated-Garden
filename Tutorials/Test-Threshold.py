from Image import ImageControl

imgControl = ImageControl.Controller()

imgName = "2.jpg"
cameraNum = 0

imgControl.image_grab(imgName, cameraNum)
imgControl.find_plants()
imgControl.draw_all()
