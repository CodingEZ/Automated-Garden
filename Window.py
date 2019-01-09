# interface modules
import sys
import time

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import pyqtSlot  # for the buttons
from PyQt5.QtWidgets import QInputDialog, QLineEdit  # for input boxes
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QImage, QPalette, QBrush

import Resize
import Display
from Image import ImageControl
from Arduino import ArduinoControl

imgControl = ImageControl.Controller()
arduinoControl = ArduinoControl.Controller()


class Window(QMainWindow):

    def __init__(self, width=500, height=400):
        super().__init__()

        self.left = 200
        self.top = 100
        self.sw = self.left + width     # screen width
        self.sh = self.top + height     # screen height
        self.bw = 200                   # button width
        self.bh = 50                    # button height

        self.setGeometry(self.left, self.top, self.sw, self.sh)

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

        # load all menus here
        menus = []
        menus.append(self.loadMainMenu())
        menus.append(self.loadCommandsMenu())
        menus.append(self.loadSettingsMenu())
        menus.append(self.loadAboutMenu())
        menus.append(self.loadControlsMenu())

        # this layout holds widgets for the application
        self.stacked_layout = QStackedLayout()

        # add widgets
        for menu in menus:
            self.stacked_layout.addWidget(menu)

        # initialize the central widget
        self.widget_central = QWidget()
        self.widget_central.setLayout(self.stacked_layout)
        self.setCentralWidget(self.widget_central)

        # Start with the main menu
        self.switch_main()

        # load background
        #self.background = 'Logos/back.jpg'
        #label_background = QLabel(self.widget_central)
        #name = Resize.resize_image(self.background, (self.sw, self.sh))
        #pixmap = QPixmap(name)
        #label_background.setPixmap(pixmap)

        #background = QImage('Logos/back.jpg').scaled(QSize(self.sw, self.sh))
        #palette = QPalette()
        #palette.setBrush(10, QBrush(background))                     # 10 = Windowrole
        #self.setPalette(palette)

        # Show the window
        self.show()


#------------------------------------------------------------------------------------------------------------------
# Menu Transitions

    def switch_main(self):
        # Give window proper title
        self.setWindowTitle('Main Menu')
        self.stacked_layout.setCurrentIndex(0)

    def switch_commands(self):
        # Give window proper title
        self.setWindowTitle('Commands Menu')
        self.stacked_layout.setCurrentIndex(1)

    def switch_settings(self):
        # Give window proper title
        self.setWindowTitle('Settings Menu')
        self.stacked_layout.setCurrentIndex(2)

    def switch_about(self):
        # Give window proper title
        self.setWindowTitle('About Menu')
        self.stacked_layout.setCurrentIndex(3)

    def switch_controls(self):
        # Give window proper title
        self.setWindowTitle('Controls Menu')
        self.stacked_layout.setCurrentIndex(4)

#------------------------------------------------------------------------------------------------------------------
# Load Functions

    def loadMainMenu(self):
        # ---- Initialize smallest components ---------------------------------------------------------------------
        button_list = []
        button_list.append(self.make_button('Commands', self.switch_commands, 'Go to Commands Menu'))
        button_list.append(self.make_button('Settings', self.switch_settings, 'Go to Settings Menu'))
        button_list.append(self.make_button('About', self.switch_about, 'Information about this software'))
        button_list.append(self.make_button('Quit', self.onClickQuit, 'Exit the Application'))

        # ---- Button Container -----------------------------------------------------------------------------------
        
        # setup layout for the buttons
        layout_buttons = QVBoxLayout()
        layout_buttons.setAlignment(Qt.AlignTop)
        layout_buttons.setSpacing(0)
        layout_buttons.setContentsMargins(0, 0, 0, 0)
        for button in button_list:
            layout_buttons.addWidget(button)

        container_buttons = QWidget()
        container_buttons.setFixedWidth(self.bw)
        container_buttons.setLayout(layout_buttons)

        # ---- Main Container -----------------------------------------------------------------------------------
        
        # add components to main layout
        layout_main = QHBoxLayout()
        layout_main.setAlignment(Qt.AlignLeft)
        layout_main.addWidget(container_buttons)

        # widget to be returned
        container_main = QWidget()
        container_main.setLayout(layout_main)
        return container_main

    def loadCommandsMenu(self):
        # ---- Initialize smallest components ---------------------------------------------------------------------
        button_list = []
        button_list.append(self.make_button('Water', self.onClickWater, 'Begins watering'))
        button_list.append(self.make_button('Detect Weeds', self.onClickDetectWeeds, 'Sends the command to detect weeds'))
        button_list.append(self.make_button('Apply Pesticide', self.onClickPesticide, 'Sends the command to apply pesticide'))
        button_list.append(self.make_button('Change Controls', self.switch_controls, 'Change Controls'))
        button_list.append(self.make_button('Back to Main Menu', self.switch_main, 'Returns to the Main Menu'))

        # currently does not update itself
        label_list = []
        label_list.append(self.make_label(self.logText))

        # ---- Label Container -------------------------------------------------------------------------------------

        layout_labels = QVBoxLayout()
        layout_labels.setAlignment(Qt.AlignTop)
        layout_labels.setSpacing(0)
        layout_labels.setContentsMargins(0, 0, 0, 0)
        for label in label_list:
            layout_labels.addWidget(label)

        container_labels = QWidget()
        container_labels.setFixedWidth(self.bw)
        container_labels.setLayout(layout_labels)

        # ---- Button Container -----------------------------------------------------------------------------------

        # setup layout for the buttons
        layout_buttons = QVBoxLayout()
        layout_buttons.setAlignment(Qt.AlignTop)
        layout_buttons.setSpacing(0)
        layout_buttons.setContentsMargins(0, 0, 0, 0)
        for button in button_list:
            layout_buttons.addWidget(button)

        container_buttons = QWidget()
        container_buttons.setFixedWidth(self.bw)
        container_buttons.setLayout(layout_buttons)

        # ---- Main Container -----------------------------------------------------------------------------------

        # add components to main layout
        layout_main = QHBoxLayout()
        layout_main.setAlignment(Qt.AlignLeft)
        layout_main.addWidget(container_labels)
        layout_main.addWidget(container_buttons)

        # widget to be returned
        container_main = QWidget()
        container_main.setLayout(layout_main)
        return container_main

    def loadSettingsMenu(self):
        # ---- Initialize smallest components ---------------------------------------------------------------------
        button_list = []
        button_list.append(self.make_button('Back to Main Menu', self.switch_main, 'Returns to the Main Menu'))

        # ---- Main Container -----------------------------------------------------------------------------------

        # add components to main layout
        layout_main = QHBoxLayout()
        layout_main.setAlignment(Qt.AlignLeft)
        for button in button_list:
            layout_main.addWidget(button)

        # widget to be returned
        container_main = QWidget()
        container_main.setLayout(layout_main)
        return container_main

    def loadAboutMenu(self):
        # ---- Initialize smallest components ---------------------------------------------------------------------
        button_list = []
        button_list.append(self.make_button('Back to Main Menu', self.switch_main, 'Returns to the Main Menu'))

        label_list = []
        label_list.append(self.make_label(self.aboutText))

        # ---- Main Container -----------------------------------------------------------------------------------

        # add components to main layout
        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignCenter)
        for label in label_list:
            layout_main.addWidget(label)
        for button in button_list:
            layout_main.addWidget(button)

        # widget to be returned
        container_main = QWidget()
        container_main.setLayout(layout_main)
        return container_main

    def loadControlsMenu(self):
        # ---- Initialize smallest components ---------------------------------------------------------------------
        button_list = []
        button_list.append(self.make_button('Back to Commands', self.switch_commands, 'Returns to the Commands Menu'))

        # currently does not update itself
        label1 = self.make_label('Watering Interval: %d minutes' % arduinoControl.waterInterval)

        button1 = self.make_button('Change Water Period', self.onClickChangeWaterInterval,
                                   'Change the interval at which \nthis device waters plants.')

        # ---- Return Container ---------------------------------------------------------------------------------

        # setup layout for the buttons
        layout_buttons = QVBoxLayout()
        layout_buttons.setAlignment(Qt.AlignCenter)
        layout_buttons.setSpacing(0)
        layout_buttons.setContentsMargins(0, 0, 0, 0)
        for button in button_list:
            layout_buttons.addWidget(button)

        container_buttons = QWidget()
        container_buttons.setFixedWidth(self.bw)
        container_buttons.setLayout(layout_buttons)

        # ---- Action Container ---------------------------------------------------------------------------------

        # setup layout for actions
        layout_actions = QGridLayout()
        layout_actions.setSpacing(0)
        layout_actions.setContentsMargins(0, 0, 0, 0)

        # add videos
        layout_actions.addWidget(label1, 0, 0)
        layout_actions.addWidget(button1, 0, 1)

        # container for all video information
        container_actions = QWidget()
        container_actions.setLayout(layout_actions)

        # ---- Main Container -----------------------------------------------------------------------------------

        # add components to main layout
        layout_main = QHBoxLayout()
        layout_main.setAlignment(Qt.AlignLeft)
        layout_main.addWidget(container_buttons)
        layout_main.addWidget(container_actions)

        # widget to be returned
        container_main = QWidget()
        container_main.setLayout(layout_main)
        return container_main
        

#------------------------------------------------------------------------------------------------------------------
# Button Specific Functions

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
    def onClickWater(self):
        arduinoControl.make_connection()
        arduinoControl.ser.flushInput()
        arduinoControl.flush_read()
        #arduinoControl.water_cycle()
        arduinoControl.water()
        if not arduinoControl.is_connected():
            Display.displayWarning(self, 'Arduino was unable to initialize.')
            return
        arduinoControl.wait(1)
        start = time.time()
        while time.time() - start < 2:
            message = arduinoControl.read_message()
        self.log('Water')
        arduinoControl.close_connection()

    @pyqtSlot()
    def onClickDetectWeeds(self):
        try:
            imgName = '2.jpg'
            cameraNum = 0  # built-in cameraNum = 0, attached cameraNum = 1

            imgControl.image_grab(imgName, cameraNum)
            imgControl.find_plants()
            imgControl.draw_all()
            self.log('Weed Detection')
        except Exception as e:
            print(e)

    @pyqtSlot()
    def onClickPesticide(self):
        arduinoControl.make_connection()
        #arduinoControl.kill_weeds()
        if not arduinoControl.is_connected():
            Display.displayWarning(self, 'Arduino was unable to initialize.')
            return
        self.log('Pesticide')
        arduinoControl.close_connection()

    @pyqtSlot()
    def onClickQuit(self):
        super().close()

#------------------------------------------------------------------------------------------------------------------
# Helper Functions

    def make_button(self, name, f, tip):
        button = QPushButton(name, self)
        button.resize(self.bw, self.bh)
        button.clicked.connect(f)
        button.setToolTip(tip)
        return button

    def make_label(self, text):
        largeStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 14pt; }"
        mediumStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 11pt; }"
        smallStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 9pt; }"
        label = QLabel(self)
        label.setText(text)
        label.setStyleSheet(smallStyle)
        return label
    
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


if __name__ == '__main__':
    app = QApplication(sys.argv)    # initialize the entire application
    ex = Window()
    app.exec_()

    print("Done!")
