# Automated Garden

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

## Python Libraries

1. Python 3.x
2. OpenCV 3.0 or higher (currently using 3.4.1)
3. numpy (latest available version preferred)
4. pillow (image resizing)
5. PyQt5 (for the Raspberry Pi interface)
    For more specific directions: 
    https://raspberrypi.stackexchange.com/questions/62939/pyqt5-on-a-raspberry-pi. 
    PyQt4 is also possible, though the entire interface must be edited for that  
6. serial (for Arduino communication, currently working on extension)
7. (FUTURE) tensorflow (normally runs on a 64-bit operating system, have not implemented)

## Arduino

You can get the latest Arduino from here: https://www.arduino.cc/en/Main/Software.
However, the Raspberry Pi we currently have runs on Arduino 1.6+.

# Getting Started

## Github and Github Desktop

To get started with this project:
1. Make a Github account
2. Download and install Github Desktop (https://desktop.github.com/) on your computer. 
3. Sign into Github desktop with your Github account information. 
4. Select File -> Clone Repository to clone (make a copy of) this project onto your desktop. 

You can now make changes to the files on your local machine, then use 
Github Desktop to send those edits to the Github repository here.

To save changes to the shared repository on Github:
1. Open Github Dekstop on your computer and select the correct repository. You should see 
that change have been made if you made local changes.
2. A summary (name) for the edits is required, so name your edits, preferable with your 
name or username at the start
3. Commit edits with the "commit to master" button
4. Click the "Push to Origin" button in the top center of Github Desktop

Be very careful about pushing edits, as they will affect everyone who pulls in the 
repository. Pulling edits is done by pressing the "Fetch Origin" button.

## Library Installation

OpenCV, Pyserial, and PyQt5 can be installed by the 'pip install' or 'pip3 install' command. 
The commands should be input in terminal. If you have multiple versions of Python installed, 
make sure to use the correct version of pip.

```pip3 install opencv-python``` <br />
```pip3 install pyserial``` <br />
```pip3 install pyqt5``` <br />
```pip3 install pillow``` <br />

In the case that you don't have pip or the above commands produce the error "pip is not 
recognized", you can follow these steps:

1. Go to the Python packages library (https://pypi.org/)

2. Download the desired library (usually a wheel file)

3. If you don't have 7-zip or some kind of file extraction program that can deal with wheel 
files, you can download 7-zip at https://www.7-zip.org/download.html. Choose the distribution 
that fits your machine and install it.

4. Once you have 7-zip and have downloaded the library, extract the file with 7-zip. Right 
click the downloaded file, hover over "7-zip," and select "Extract Files." the following link 
provides a visual and might be helpful: https://www.newsgroupreviews.com/7-zip-extract-unrar.html.

5. Attempt to import the library on the command line in the Python IDLE shell, in Pyzo, and 
whatever Python editor you prefer. The commands are: <br /><br />
    a. opencv-python - ```import cv2``` <br />
    b. pyserial - ```import serial``` <br />
    c. pyqt5 - ```import PyQt5``` <br />
    d. pillow - ```import PIL``` <br /><br />
    
6. If step 5 fails for any particular library, place the library contents of that library in 
the site-packages directory of your Python distribution and attempt to import again. If you are
installing OpenCV on a Mac and you succeeded in pip installing but fail to import cv2, try the 
directions here: https://www.learnopencv.com/install-opencv3-on-macos/. If all fails, 
contact us.

Once the libraries are installed, attempt to run some of the test files in the 'Test' folder of 
this repository. If there are no errors, you are set to go!

## Running Some Tests

To make sure that you've followed instructions correctly, try to run some of the tests. The two 
tests are located within the "Tests" folder. The first test is called "Test-ImageGrab," which 
tests the reading capabilities of OpenCV. Play around and see if you can take a live picture 
with your laptop's built-in camera.

The second test is "Test-Threshold," which is an example of one way to threshold the image.
There are many ways to threshold, so don't be afraid to play around with the different thresholds.
A quick example is located here: https://medium.com/@ckyrkou/color-thresholding-in-opencv-91049607b06d.
You can also look into OpenCV masks and contours. The OpenCV docs are here: https://docs.opencv.org/3.4.1/.

# How to use this repo

## ImageControl.Controller Class

```from Image import ImageControl``` <br />
```imgControl = ImageControl.Controller()``` <br />

```imgControl.image_grab()``` <br />

Must be called in order to initialize the image. Can use a given image in the Camera
folder or can take an image with a given camera.

```imgControl.find_plants()``` <br />

Finds a plant and weeds based on default thresholds, including a scale for brightness. 
Future edits will allow for changes. Currently, the center-most object is identified as a plant, 
and all other objects identified as weeds. 

```imgControl.draw_all()``` <br />

Outlines the plant in green and the weeds in blue, and displays the result.

## ArduinoControl.Controller Class

```from Arduino import ArduinoControl``` <br />
```arduinoControl = ArduinoControl.Controller()``` <br />

Creating an instance of Controller opens up serial communication with an Arduino. The various
commands to be given to the Arduino can be found in the Arduino folder.

```arduinoControl.water_cycle()``` <br />

Commands such as watering are still being determined.

