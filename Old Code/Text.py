from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

def showText(app, xFactor, yFactor, widthFactor, heightFactor, width, styleBound, styleText, text, textCenter=True):
    labelIn = QLabel(app)  # inside label, with text
    labelIn.resize(app.width * widthFactor, app.height * heightFactor)
    labelIn.move(app.width * xFactor - labelIn.width() / 2, app.height * yFactor - labelIn.height() / 2)
    labelIn.setStyleSheet(styleText)
    if textCenter:
        labelIn.setAlignment(Qt.AlignCenter)
    else:
        labelIn.setAlignment(Qt.AlignLeft)
    labelIn.setText(text)
    return [labelIn]
