from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image

def showBackground(app):
    """Takes the background file name in the __init__ function."""
    labelBack = QLabel(app)
    name = resize_image(app.background, (app.width, app.height))
    pixmap = QPixmap(name)
    labelBack.setPixmap(pixmap)


def getExtensionIndex(name):
    index = -1
    while name[index] != '.' and index > -len(name) + 1:
        index -= 1
    return index


def resize_image(name, windowSize, imgFormat='JPEG'):
    img = Image.open(name)
    index = getExtensionIndex(name)
    extension = name[index:]

    if img.size[0] > windowSize[0]:
        width = windowSize[0]
    else:
        width = img.size[0]

    if img.size[1] > windowSize[1]:
        height = windowSize[1]
    else:
        height = img.size[1]

    img = img.resize((width, height), Image.ANTIALIAS)  # image resize filter
    img.save(name[:index] + 'COPY' + extension, imgFormat)

    return name[:index] + 'COPY' + extension
