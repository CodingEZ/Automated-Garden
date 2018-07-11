from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

def showLabels(labels):
    for label in labels:
        label.show()

def hideLabels(labels):
    for label in labels:
        label.hide()

def showText(app, xFactor, yFactor, widthFactor, heightFactor, width, styleText, text, textCenter=True):
    label = QLabel(app)  # inside label, with text
    label.resize(app.width * widthFactor, app.height * heightFactor)
    label.move(app.width * xFactor - label.width() / 2, app.height * yFactor - label.height() / 2)
    label.setStyleSheet(styleText)
    if textCenter:
        label.setAlignment(Qt.AlignCenter)
    else:
        label.setAlignment(Qt.AlignLeft)
    label.setText(text)
    label.hide()
    return label
