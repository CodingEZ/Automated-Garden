# Weed-Detection

The following program detects weeds and plants, implementing OpenCV to threshold and find the edges of green objects.
As of right now, the largest object is considered a plant while any other object above a certain size is considered a weed.
One of the advantages of this program is that it performs under a range (albeit small) of lighting conditions.
However, one of the disadvantages of using this program is that it does not implement any kind of machine learning.
I aim to add in the future a neural network to identify plants regardless of size.

## Requirements
1. Python 3.x
2. OpenCV 3.4
3. matplotlib (if you would like to display results, mostly for testing)
4. serial (if you want to communicate with an Arduino, will add extension later)

## How to use this repo
control = Project()
The project overall has a class from which you call methods from other classes.

control.find_plant()
This function finds the plant, which is for now the object that has the largest size after thresholding and normalizing.

control.find_weeds()
This function labels all other regions as weeds.

control.draw_weeds()
Using matplot lib, one can draw the images created and outline the contour of all weeds.