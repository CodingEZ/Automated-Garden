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
        newButton.resize(app.bw, app.bh)
        newButton.move(app.sw * widthFactor - app.bw / 2,
                       app.sh * heightFactor - (len(buttonInfo) * app.bh) / 2
                                + index * app.bh)
        newButton.clicked.connect(buttonInfo[name][1])
        buttons.append(newButton)
        index += 1
    hideButtons(buttons)
    return buttons
