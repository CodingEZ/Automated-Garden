from PyQt5.QtWidgets import QWidget         # for creating the window
from PyQt5.QtWidgets import QInputDialog, QLineEdit     # for input boxes
from PyQt5.QtCore import pyqtSlot           # for the buttons
import sys
import time

from ImageDetection import Detector
import Interface_Background as Background
import Interface_Display as Display
import Interface_Label as Label
import Interface_Button as Button


class Window(QWidget):

    def __init__(self, application, width=1000, height=800):
        super().__init__()
        self.app = application

        self.title = 'Sustainable Earth Arduino Garden'
        self.left = 200
        self.top = 100
        self.width = self.left + width
        self.height = self.top + height
        self.background = 'Logos/back.jpg'
        self.largeStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 14pt; }"
        self.mediumStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 11pt; }"
        self.smallStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 9pt; }"

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        Background.showBackground(self)

        self.aboutText = None
        try:
            self.aboutText = open('Texts/About.txt', 'r').read()
        except OSError:
            Display.displayWarning(self, 'Failed to load "Texts/About.txt" file. Was it corrupted?')

        self.waterInterval = 10  # minutes
        self.minInterval = 10
        self.maxInterval = 20

        self.labels = []
        self.labelDict = dict()
        self.initLabels()

        self.buttons = []
        self.buttonDict = dict()
        self.initButtons()

        self.initStartMenu()  # begin application in the start menu
        self.show()

    def initLabels(self):

        self.labelDict['startMenu'] = [Label.showText(self, 1 / 2, 1 / 4, 3 / 4, 1 / 8, 10, self.largeStyle,
                                            'Sustainable Earth Arduino Garden')
                                        ]
        self.labelDict['commandsMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10, self.largeStyle,
                                                'Garden Command Center'),
                                          Label.showText(self, 1 / 3, 1 / 2, 1 / 2, 14 / 25, 10, self.smallStyle,
                                                'Nothing here yet.')
                                          ]
        self.labelDict['settingsMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10, self.largeStyle,
                                            'General Settings')
                                          ]
        self.labelDict['aboutMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10, self.largeStyle,
                                            'About'),
                                       Label.showText(self, 1 / 2, 1 / 2, 3 / 5, 1 / 3, 10, self.smallStyle,
                                            self.aboutText)
                                        ]
        self.labelDict['waterMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 10, self.largeStyle,
                                                      'Garden Water Settings'),
                                        Label.showText(self, 1 / 3, 1 / 2, 1 / 3, 1 / 16, 10, self.smallStyle,
                                                      'Watering Interval: %d minutes' % self.waterInterval)
                                        ]

    def initButtons(self):

        startMenuButtonInfo = {
            'Commands': ['Go to Commands Menu', self.initCommandsMenu],
            'Settings': ['Go to Settings Menu', self.initSettingsMenu],
            'About': ['Information about this software', self.initAboutMenu],
            'Quit': ['Exit the Application', self.onClickQuit]
        }

        commandsMenuButtonInfo = {
            'Water': ['Goes to the watering menu', self.initWaterMenu],
            'Detect Weeds': ['Sends the command to detect weeds', self.onClickDetectWeeds],
            'Pesticide': ['Sends the command to apply pesticide', self.onClickPesticide],
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu],
        }

        settingsMenuButtonInfo = {
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu]
        }

        aboutMenuButtonInfo = {
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu],
        }

        waterMenuButtonInfo = {
            'Start Watering': ['The default settings are tailored \n' +
                               'toward outdoor noontime lighting. \n' +
                               'Try out some thresholds.', self.initWaterMenu],
            'Cancel': ['Go to Commands Menu', self.initCommandsMenu]
        }

        intervalButtonInfo = {
            'Change Water Interval': ['Change the interval at which \n' +
                                      'this device waters plants.', self.onClickChangeWaterInterval]
        }

        self.buttonDict['startMenu'] = Button.createButtons(self, startMenuButtonInfo, 1 / 2, 1 / 2)
        self.buttonDict['commandsMenu'] = Button.createButtons(self, commandsMenuButtonInfo, 13 / 16, 1 / 2)
        self.buttonDict['settingsMenu'] = Button.createButtons(self, settingsMenuButtonInfo, 1 / 2, 1 / 2)
        self.buttonDict['aboutMenu'] = Button.createButtons(self, aboutMenuButtonInfo, 1 / 2, 2 / 3)
        self.buttonDict['waterMenu'] = (Button.createButtons(self, waterMenuButtonInfo, 1 / 2, 1 / 4) +
                                        Button.createButtons(self, intervalButtonInfo, 2 / 3, 1 / 2)
                                        )

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

    def initWaterMenu(self):
        # Labels first
        Label.hideLabels(self.labels)
        self.labels = self.labelDict['waterMenu']
        Label.showLabels(self.labels)

        # Buttons
        Button.hideButtons(self.buttons)
        self.buttons = self.buttonDict['waterMenu']
        Button.showButtons(self.buttons)

##############################################################
    # Clicking Functions
##############################################################

    @pyqtSlot()
    def onClickChangeWaterInterval(self):
        num, okPressed = QInputDialog.getInt(self, "Change Watering Interval",
                                    "Pick an interval (in minutes) at which the device \n" +
                                    " will water. The minimum interval is %d minutes, \n" % self.minInterval +
                                    "and the maximum is %d minutes." % self.maxInterval,
                                    QLineEdit.Normal, self.waterInterval)
        if okPressed:
            if num < self.minInterval:
                Display.displayWarning(self, 'You cannot water at intervals less than %d minutes!'
                                       % self.minInterval)
                return
            elif num > self.maxInterval:
                Display.displayWarning(self, 'You cannot water at intervals more than %d minutes!'
                                       % self.maxInterval)
                return
            self.waterInterval = num

    @pyqtSlot()
    def onClickDetectWeeds(self):
        imgName = '1516378704.jpg'
        cameraNum = 0  # built-in cameraNum = 0, attached cameraNum = 1

        start = time.time()
        detector = Detector(thresholdBrightness=.35, weedFactor=1 / 16)
        Detector.detect_all(detector, imgName, cameraNum)
        Detector.draw_all(detector)     # currently thread error if run but not terminated in different thread
        stop = time.time()
        print("Algorithm runtime for program:", stop - start)
            # add this to the log, along with start time

    @pyqtSlot()
    def onClickPesticide(self):
        pass

    @pyqtSlot()
    def onClickQuit(self):
        sys.exit(self.app.exec_())
