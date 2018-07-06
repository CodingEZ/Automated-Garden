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
4. (Optional) matplotlib (if you would like to display results, mostly for 
testing)
5. (Future) serial (if you want to communicate with an Arduino, will add 
extension later)

## How to use this repo
detect = ImageDetection()
The project overall has a class from which you call methods from other classes.

detect.image_grab()
This function must be called in order to initialize the image. Can use a given
image in the folder Capture or can take an image with a given camera.

detect.find_plant()
This function finds the plant, which is (for now) the object that has the 
largest size after thresholding and normalizing. Some of the thresholds have 
defaults, but others are currently fixed.

detect.find_weeds()
This function labels all other regions as weeds.

detect.outline_weeds()
One can outline the contour of all weeds. 
The color is currently fixed to magenta.

detect.outline_plant()
One can outline the contour of the plant detected. 
The color is currently fixed to green.

detect.draw_outlines()
Adds the original image with added outlines to images to be drawn. It currently 
produces an error if no outlines are made.

detect.draw_first_threshold()
Adds the first threshold to images that should be drawn. The first threshold is
only an HSV threshold.

detect.draw_second_threshold()
Adds the second threshold to images that should be drawn. The second threshold is
based on size and brightness after normalization.

detect.display_drawings()
Using matplotlib, this displays the original image along with any drawn images
(based on draw_x calls).

## Future Edits
I will later add arduino communication capabilities to allow one to implement 
the weed detection in an Arduino garden.

I am currently working on an interface for use on a Raspberry Pi.
