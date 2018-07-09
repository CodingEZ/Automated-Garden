from PyQt5.QtWidgets import QApplication
from Interface_Window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)    # initialize the entire application
    ex = Window(app, width=1000, height=800)
    sys.exit(app.exec_())
