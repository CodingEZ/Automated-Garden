from PyQt5.QtWidgets import QApplication
from Window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)    # initialize the entire application
    ex = Window(width=800, height=800)
    app.exec_()

    print("Done!")
