from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import Background
import Text
import ButtonClick
import sys

class Window(QWidget):

    def __init__(self, width=1000, height=800):
        super().__init__()
        self.title = 'Speech Practice and Transcription'
        self.left = 100
        self.top = 100
        self.width = self.left + width
        self.height = self.top + height
        self.background = 'Images/back.jpg'
        self.boundStyle = "QLabel { background-color : #FFFFFF; }"
        self.titleStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 14pt; }"
        self.normalStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 11pt; }"
        self.logStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 9pt; }"

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        Background.showBackground(self)

        self.buttons = []
        self.labels = []

        self.initStart()  # begin application in the start menu
        self.show()

    def initStart(self):
        self.buttons = []
        buttonInfo = {'Commands' : ['Go to Commands Menu', self.onClickCommands],
                      'Settings' : ['Go to Settings Menu', self.onClickSettings],
                      'Quit' : ['Exit the Application', onClickQuit]}

        self.labels = []
        self.labels += Text.showText(self, 1 / 2, 1 / 3, 3 / 4, 1 / 8, 50, self.boundStyle, self.titleStyle,
                                     'Sustainable Earth Arduino Garden')

        index = 0
        for name in buttonInfo:
            newButton = QPushButton(name, self)
            newButton.setObjectName(name)
            newButton.setToolTip(buttonInfo[name][0])
            newButton.move(self.width / 2 - newButton.width() / 2 - 5,
                           self.height / 2 - (len(buttonInfo) * newButton.height()) / 2
                           + index * newButton.height())
            newButton.clicked.connect(buttonInfo[name][1])
            self.buttons.append(newButton)
            index += 1

    def initCommandsMenu(self):
        self.buttons = []
        buttonInfo = {'Instructions' : ['Gives an explanation of what goes on in this menu', onClickQuit],
                      'Transcribe' : ['Makes a full transcription of audio', onClickQuit],
                      'Choose File' : ['Choose a video from your computer to transcribe', onClickQuit],
                      'Choose URL' : ['Choose a video from Youtube to transcribe', onClickQuit],
                      'Download' : ['Downloads a video from a given Youtube url', onClickQuit],
                      'Back to Start' : ['Returns to the Start Menu', onClickQuit],
                      'Quit' : ['Exit the Application', onClickQuit]}

        self.labels = []

        index = 0
        for name in buttonInfo:
            newButton = QPushButton(name, self)
            newButton.setObjectName(name)
            newButton.setToolTip(buttonInfo[name][0])
            newButton.move(self.width * (3 / 4) - newButton.width() / 2 - 5,
                           self.height * (3 / 4) - (
                           len(buttonInfo) * newButton.height()) / 2 + index * newButton.height())
            newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)
            index += 1

    @pyqtSlot()
    def onClickCommands(self):
        ButtonClick.hideButtons(self.buttons)
        ButtonClick.hideLabels(self.labels)
        self.initCommandsMenu()
        ButtonClick.showLabels(self.labels)
        ButtonClick.showButtons(self.buttons)

    @pyqtSlot()
    def onClickSettings(self):
        pass

def onClickQuit():
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window(1000, 800)
    onClickQuit()