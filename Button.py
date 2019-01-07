from PyQt5.QtWidgets import QPushButton

def showButtons(buttons):
    for button in buttons:
        button.show()

def hideButtons(buttons):
    for button in buttons:
        button.hide()

def createButtons(app, buttonInfo, widthFactor, heightFactor):
    buttons = []
    index = 0
    for name in buttonInfo:
        newButton = QPushButton(name, app)
        newButton.setObjectName(name)
        newButton.setToolTip(buttonInfo[name][0])
        newButton.resize(250, 50)
        newButton.move(app.width * widthFactor - newButton.width() / 2,
                       app.height * heightFactor - (len(buttonInfo) * newButton.height()) / 2
                                + index * newButton.height())
        newButton.clicked.connect(buttonInfo[name][1])
        buttons.append(newButton)
        index += 1
    hideButtons(buttons)
    return buttons
