from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QInputDialog, QLineEdit     # for input boxes
from PyQt5.QtCore import pyqtSlot
import sys

import Background
import Display
import Label
import Button


class Window(QWidget):

    def __init__(self, width=1000, height=800):
        super().__init__()
        self.title = 'Speech Practice and Transcription'
        self.left = 100
        self.top = 100
        self.width = self.left + width
        self.height = self.top + height
        self.background = 'Images/back.jpg'
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
        except:
            Display.displayWarning(self, 'Unexpected error.')

        self.waterInterval = 10  # minutes
        self.minInterval = 10
        self.maxInterval = 20

        self.buttons = []
        self.buttonDict = dict()
        self.initButtons()

        self.labels = []
        self.labelDict = dict()
        self.initLabels()

        self.initStartMenu()  # begin application in the start menu
        self.show()
        
    def initButtons(self):
        
        startMenuButtonInfo = {
            'Commands': ['Go to Commands Menu', self.initCommandsMenu],
            'Settings': ['Go to Settings Menu', self.onClickSettings],
            'About': ['Information about this software', self.initAboutMenu],
            'Quit': ['Exit the Application', onClickQuit]
        }
        commandsMenuButtonInfo = {
            'Water': ['Goes to the watering menu', self.initWaterMenu],
            'Detect Weeds': ['Sends the command to detect weeds', self.onClickDetectWeeds],
            'Pesticide': ['Sends the command to apply pesticide', self.onClickPesticide],
            'Back to Start': ['Returns to the Start Menu', self.initStartMenu],
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
        self.buttonDict['settingsMenu'] = None
        self.buttonDict['aboutMenu'] = Button.createButtons(self, aboutMenuButtonInfo, 1 / 2, 2 / 3)
        self.buttonDict['waterMenu'] = (Button.createButtons(self, waterMenuButtonInfo, 1 / 2, 1 / 4) +
                                            Button.createButtons(self, intervalButtonInfo, 2 / 3, 1 / 2)
                                        )

    def initLabels(self):

        self.labelDict['startMenu'] = [Label.showText(self, 1 / 2, 1 / 4, 3 / 4, 1 / 8, 25, self.largeStyle,
                                            'Sustainable Earth Arduino Garden')
                                        ]
        self.labelDict['commandsMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 25, self.largeStyle,
                                                'Garden Command Center'),
                                          Label.showText(self, 1 / 3, 1 / 2, 1 / 2, 14 / 25, 25, self.smallStyle,
                                                'Nothing here yet.')
                                          ]
        self.labelDict['settingsMenu'] = None
        self.labelDict['aboutMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 25, self.largeStyle,
                                            'About'),
                                       Label.showText(self, 1 / 2, 1 / 2, 3 / 5, 1 / 3, 25, self.smallStyle,
                                            self.aboutText)
                                        ]
        self.labelDict['waterMenu'] = [Label.showText(self, 1 / 2, 1 / 8, 1 / 2, 1 / 12, 25, self.largeStyle,
                                                      'Garden Water Settings'),
                                        Label.showText(self, 1 / 3, 1 / 2, 1 / 3, 1 / 16, 25, self.smallStyle,
                                                      'Watering Interval: %d minutes' % self.waterInterval)
                                        ]

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
        pass

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
    def onClickSettings(self):
        self.initSettingsMenu()

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
        pass

    @pyqtSlot()
    def onClickPesticide(self):
        pass

def onClickQuit():
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window(1000, 800)
    onClickQuit()