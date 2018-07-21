# Weed-Detection

The following program detects weeds and plants, implementing OpenCV 
to threshold and find the edges of green objects. As of right now, 
the largest object is considered a plant while any other object above 
a certain size is considered a weed. One of the advantages of this 
program is that it performs under a range (albeit small) of lighting 
conditions. However, one of the disadvantages of using this program is 
that it does not implement any kind of machine learning. I aim to add 
in the future a neural network to identify plants regardless of size.

# About

This was a project inspired by Farmbot and a group called Sustainable Earth 
at Carnegie Mellon University. Overall, it has been a rewarding experience 
to understand to program such a large project in pieces, put everything 
together, and ultimately see some promising results.

# Requirements

The project was run on a Windows computer, on which OpenCV 3.4 was easy to 
install. However, as long as one could install OpenCV, this project can be 
run on other operating systems.

1. Python 3.x, preferably 64-bit
2. OpenCV 3.0 or higher (possibly will be replaced by tensorflow, TBD)
3. numpy (latest available version preferred)
4. pillow (image resizing)
4. PyQt5 (for the Raspberry Pi interface)
5. matplotlib (for displaying results, mostly for testing purposes)
6. serial (if you want to communicate with an Arduino ,working on extension)
7. tensorflow (naturally runs on a 64-bit operating system)

# How to use this repo

## Image

```from Image import ImageControl```
```imgControl = ImageControl.Controller()```
Creating a new instance of the Controller will immediately create three objects, 
a Drawer, an Editor, and a GripPipeline. The Drawer handles all drawing and outline 
functions with matplotlib. The Editor creates different thresholds for image 
processing, and calls the Grip pipeline object for filtering.

```imgControl.image_grab()```
This function must be called in order to initialize the image. Can use a given
image in the folder Camera or can take an image with a given camera.

```imgControl.find_plant()```

This function finds the plant, which is (for now) the object that has the 
largest size after thresholding and normalizing. Some of the thresholds have 
defaults, but others are currently fixed.

```imgControl.find_weeds()```
This function labels all other regions as weeds.

```imgControl.detect_all()```
This function calls find_plant() and find_weed().

```imgControl.drawer.outline_weeds()```
One can outline the contour of all weeds. The color is currently fixed to magenta.

```imgControl.drawer.outline_plant()```
One can outline the contour of the plant detected. The color is currently fixed to green.

```imgControl.drawer.add_outlines()```
Adds the original image with added outlines to images to be drawn. It currently 
produces an error if no outlines are made.

```imgControl.drawer.add_first_threshold()```
Adds the first threshold to images that should be drawn. The first threshold is
only an HSV threshold.

```imgControl.drawer.add_second_threshold()```
Adds the second threshold to images that should be drawn. The second threshold is
based on size and brightness after normalization.

```imgControl.drawer.display_drawings()```
Using matplotlib, this displays the original image along with any drawn images.

```imgControl.drawer.draw_all()```
A convenient function that draws all of the possible thresholds.

## Arduino

```from Arduino import ArduinoControl```
```arduinoControl = ArduinoControl.Controller()```

Creating an instance of Controller opens up serial communication with an Arduino

```arduinoControl.water_cycle()```

Waters in an order still to be determined.

# Future Edits
I am continuing to add arduino communication capabilities to allow one to implement 
the weed detection in an Arduino garden.

I am currently working on an interface for use on a Raspberry Pi.
