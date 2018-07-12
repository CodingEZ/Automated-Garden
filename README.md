# Weed-Detection

The following program detects weeds and plants, implementing OpenCV 
to threshold and find the edges of green objects. As of right now, 
the largest object is considered a plant while any other object above 
a certain size is considered a weed. One of the advantages of this 
program is that it performs under a range (albeit small) of lighting 
conditions. However, one of the disadvantages of using this program is 
that it does not implement any kind of machine learning. I aim to add 
in the future a neural network to identify plants regardless of size.

## Requirements
The project was run on a Windows computer, on which OpenCV 3.4 was easy to 
install. However, as long as one could install OpenCV, this project can be 
run on other operating systems.

1. Python 3.x
2. OpenCV 3.4
3. numpy (latest available version preferred)
4. PyQt5 (for the interface)
5. matplotlib (if you would like to display results, mostly for testing)
6. (Future) serial (if you want to communicate with an Arduino, will add 
extension later)

## How to use this repo
import Image
Importing the module Image will immediately create three objects, a Drawer, an 
Editor, and a GripPipeline. The Drawer handles all drawing and outline functions 
with matplotlib. The Editor creates different thresholds for image processing, 
and calls the Grippipeline object for filtering.

Image.Controller.image_grab()
This function must be called in order to initialize the image. Can use a given
image in the folder Capture or can take an image with a given camera.

Image.Controller.find_plant()
This function finds the plant, which is (for now) the object that has the 
largest size after thresholding and normalizing. Some of the thresholds have 
defaults, but others are currently fixed.

Image.Controller.find_weeds()
This function labels all other regions as weeds.

Image.Controller.detect_all()
This function calls find_plant() and find_weed().

Image.Controller.drawer.outline_weeds()
One can outline the contour of all weeds. 
The color is currently fixed to magenta.

Image.Controller.drawer.outline_plant()
One can outline the contour of the plant detected. 
The color is currently fixed to green.

Image.Controller.drawer.add_outlines()
Adds the original image with added outlines to images to be drawn. It currently 
produces an error if no outlines are made.

Image.Controller.drawer.add_first_threshold()
Adds the first threshold to images that should be drawn. The first threshold is
only an HSV threshold.

Image.Controller.drawer.add_second_threshold()
Adds the second threshold to images that should be drawn. The second threshold is
based on size and brightness after normalization.

Image.Controller.drawer.display_drawings()
Using matplotlib, this displays the original image along with any drawn images.

Image.Controller.drawer.draw_all()
A convenient function that draws all of the possible thresholds.

## Future Edits
I will later add arduino communication capabilities to allow one to implement 
the weed detection in an Arduino garden.

I am currently working on an interface for use on a Raspberry Pi.
