from PyQt5.QtWidgets import QApplication
from Window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)    # initialize the entire application
    ex = Window(app, width=800, height=800)
    sys.exit(app.exec_())
