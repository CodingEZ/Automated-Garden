# interface modules
from PyQt5.QtCore import pyqtSlot  # for the buttons
from PyQt5.QtWidgets import QInputDialog, QLineEdit  # for input boxes
from PyQt5.QtWidgets import QWidget  # for creating the window
import Background as Background
import Button as Button
import Display as Display
import Label as Label

import sys
import time
from Image import ImageControl
from Arduino import ArduinoControl

imgControl = ImageControl.Controller()
arduinoControl = ArduinoControl.Controller()


class Window(QWidget):
    
    largeStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 14pt; }"
    mediumStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 11pt; }"
    smallStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 9pt; }"

    def __init__(self, application, width=1000, height=800):
        super().__init__()
        self.app = application

        self.title = 'Sustainable Earth Arduino Garden'
        self.left = 200
        self.top = 100
        self.width = self.left + width
        self.height = self.top + height
        self.background = 'Logos/back.jpg'

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        Background.load_background(self)
        self.show()

        self.aboutText = None
        try:
            file = open('Texts/About.txt', 'r')
            self.aboutText = file.read()
            file.close()
        except OSError:
            Display.displayWarning(self, 'Failed to load "Texts/About.txt" file. Was it corrupted?')

        self.logText = None
        try:
            file = open('Texts/Log.txt', 'r')
            self.logText = file.read()
            file.close()
        except OSError:
            Display.displayWarning(self, 'Failed to load "Texts/Log.txt" file. Was it corrupted?')

        if arduinoControl.arduino is None:
            Display.displayWarning(self, 'Careful! Arduino was unable to initialize.')

        self.labels = []
        self.labelDict = dict()
        self.initLabels()

        self.buttons = []
        self.buttonDict = dict()
        self.initButtons()

        self.initStartMenu()  # begin application in the start menu

    def initLabels(self):

        self.labelDict['startMenu'] = [Label.showText(self, 1 / 2, 1 / 4, 3 / 4, 1 / 8, 10,
                            __class__.largeStyle, 'Sustainable Earth Arduino Garden')
                       ]
        self.labelDict['commandsMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10,
                            __class__.largeStyle, 'Garden Command Center'),
                      Label.showText(self, 1 / 3, 1 / 2, 1 / 2, 14 / 25, 10,
                            __class__.smallStyle, self.logText)
                      ]
        self.labelDict['settingsMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10,
                            __class__.largeStyle, 'General Settings')
                      ]
        self.labelDict['aboutMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10,
                            __class__.largeStyle, 'About'),
                       Label.showText(self, 1 / 2, 1 / 2, 3 / 5, 1 / 3, 10,
                            __class__.smallStyle, self.aboutText)
                       ]
        self.labelDict['commandSettingsMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10,
                                __class__.largeStyle, 'Garden Water Settings'),
                         Label.showText(self, 1 / 3, 16 / 36, 1 / 3, 1 / 20, 10, __class__.smallStyle,
                                'Watering Interval: %d minutes' % arduinoControl.waterInterval),
                         Label.showText(self, 1 / 3, 18 / 36, 1 / 3, 1 / 20, 10, __class__.smallStyle,
                                'Threshold Brightness: %d out of 1' % imgControl.thresholdBrightness)
                         ]

    def initButtons(self):
        # BI stands for Button Information

        startMenuBI = {
            'Commands': ['Go to Commands Menu', self.initCommandsMenu],
            'Settings': ['Go to Settings Menu', self.initSettingsMenu],
            'About': ['Information about this software', self.initAboutMenu],
            'Quit': ['Exit the Application', self.onClickQuit]
        }

        commandsMenuBI = {
            'Water' : ['Begins watering', self.onClickWater],
            'Detect Weeds': ['Sends the command to detect weeds', self.onClickDetectWeeds],
            'Apply Pesticide': ['Sends the command to apply pesticide', self.onClickPesticide],
            'Change Settings': ['Change Settings', self.initCommandSettingsMenu],
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu]
        }

        settingsMenuBI = {
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu]
        }

        aboutMenuBI = {
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu],
        }

        commandSettingsMenuBI = {
            'Back': ['Return to the Commands Menu', self.initCommandsMenu]
        }

        intervalBI = {
            'Change Water Period': ['Change the interval at which \n' +
                                    'this device waters plants.',
                                    self.onClickChangeWaterInterval],
            'Change Threshold Brightness': ['Change the brightness at which \n' +
                                    'this device detects plants.',
                                    self.onClickChangeThresholdBrightness]
        }

        self.buttonDict['startMenu'] = Button.createButtons(self, startMenuBI, 1 / 2, 1 / 2)
        self.buttonDict['commandsMenu'] = Button.createButtons(self, commandsMenuBI, 13 / 16, 1 / 2)
        self.buttonDict['settingsMenu'] = Button.createButtons(self, settingsMenuBI, 1 / 2, 1 / 2)
        self.buttonDict['aboutMenu'] = Button.createButtons(self, aboutMenuBI, 1 / 2, 2 / 3)
        self.buttonDict['commandSettingsMenu'] = (Button.createButtons(self, commandSettingsMenuBI, 1 / 2, 1 / 4) +
                                                  Button.createButtons(self, intervalBI, 2 / 3, 15 / 32)
                                                  )

##############################################################
    # Menu Initializers
##############################################################

    def initStartMenu(self):
        # Labels first
        Label.hideLabels(self.labels)
        self.labels = self.labelDict['startMenu']
        Label.showLabels(self.labels)

        # Buttons second
        Button.hideButtons(self.buttons)
        self.buttons = self.buttonDict['startMenu']
        Button.showButtons(self.buttons)

    def initCommandsMenu(self):
        # Labels first
        Label.hideLabels(self.labels)
        self.labels = self.labelDict['commandsMenu']
        Label.showLabels(self.labels)

        # Buttons second
        Button.hideButtons(self.buttons)
        self.buttons = self.buttonDict['commandsMenu']
        Button.showButtons(self.buttons)

    def initSettingsMenu(self):
        # Labels first
        Label.hideLabels(self.labels)
        self.labels = self.labelDict['settingsMenu']
        Label.showLabels(self.labels)

        # Buttons second
        Button.hideButtons(self.buttons)
        self.buttons = self.buttonDict['settingsMenu']
        Button.showButtons(self.buttons)

    def initAboutMenu(self):
        # Labels first
        Label.hideLabels(self.labels)
        self.labels = self.labelDict['aboutMenu']
        Label.showLabels(self.labels)

        # Buttons second
        Button.hideButtons(self.buttons)
        self.buttons = self.buttonDict['aboutMenu']
        Button.showButtons(self.buttons)

    def initCommandSettingsMenu(self):
        # Labels first
        Label.hideLabels(self.labels)
        self.labels = self.labelDict['commandSettingsMenu']
        Label.showLabels(self.labels)

        # Buttons
        Button.hideButtons(self.buttons)
        self.buttons = self.buttonDict['commandSettingsMenu']
        Button.showButtons(self.buttons)

##############################################################
    # Clicking Functions
##############################################################

    @pyqtSlot()
    def onClickChangeWaterInterval(self):
        num, okPressed = QInputDialog.getInt(self, "Change Watering Interval",
                                    "Pick an interval (in minutes) at which the device \n" +
                                    " will water. The minimum interval is %d minutes, \n" % arduinoControl.minInterval +
                                    "and the maximum is %d minutes." % arduinoControl.maxInterval,
                                    QLineEdit.Normal, arduinoControl.waterInterval)
        if okPressed:
            if num < arduinoControl.minInterval:
                Display.displayWarning(self, 'You cannot water at intervals less than %d minutes!'
                                       % arduinoControl.minInterval)
                return
            elif num > arduinoControl.maxInterval:
                Display.displayWarning(self, 'You cannot water at intervals more than %d minutes!'
                                       % arduinoControl.maxInterval)
                return
            arduinoControl.waterInterval = num

    @pyqtSlot()
    def onClickChangeThresholdBrightness(self):
        num, okPressed = QInputDialog.getInt(self, "Change Threshold Brightness",
                                    "Pick an interval (in minutes) at which the device \n" +
                                    " will water. The minimum interval is %d minutes, \n" % imgControl.minBrightness +
                                    "and the maximum is %d minutes." % imgControl.maxBrightness,
                                    QLineEdit.Normal, imgControl.thresholdBrightness)
        if okPressed:
            if num < imgControl.minBrightness:
                Display.displayWarning(self, 'Threshold cannot be less than %d minutes!'
                                       % imgControl.minBrightness)
                return
            elif num > imgControl.maxBrightness:
                Display.displayWarning(self, 'Threshold cannot be more than %d minutes!'
                                       % imgControl.maxBrightness)
                return
            imgControl.thresholdBrightness = num

    @pyqtSlot()
    def onClickWater(self):
        arduinoControl.water_cycle()
        self.log('Water')

    @pyqtSlot()
    def onClickDetectWeeds(self):
        imgName = '1516378704.jpg'
        cameraNum = 0  # built-in cameraNum = 0, attached cameraNum = 1

        start = time.time()
        imgControl.drawer.change_default_settings(thresholdBrightness=.35, weedFactor=1 / 16)
        imgControl.image_grab(imgName, cameraNum)
        imgControl.find_plants()
        #imgControl.draw_all()     # currently thread error if run but not terminated in different thread
        stop = time.time()
        self.log('Weed Detection')
        print("Algorithm runtime for program:", stop - start)
            # add this to the log, along with start time

    @pyqtSlot()
    def onClickPesticide(self):
        self.log('Pesticide')

    @pyqtSlot()
    def onClickQuit(self):
        sys.exit(self.app.exec_())

##############################################################
    # Helper Functions
##############################################################

    def log(self, command):
        completionTime = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
        try:
            file = open('Texts/Log.txt', 'a')
            file.write(command + ' : ' + completionTime + '\n')
            file.close()
        except OSError:
            file = open('Texts/Temp.txt', 'a')
            file.write(command + ' : ' + completionTime + '\n')
            file.close()
            Display.displayWarning(self, "Unable to open 'Texts/Log.txt'. Logged to 'Texts/Temp.txt'")
        self.logText += command + ' : ' + completionTime + '\n'
        self.initLabels()
        self.initCommandsMenu()