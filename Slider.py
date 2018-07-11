from PyQt5.QtWidgets import QSlider, QGroupBox, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt

def createSliderBox(window):
    sliderGrid = QGridLayout()
    sliderGrid.addWidget(createSlider())
    sliderGrid.addWidget(createSlider())
    window.setLayout(sliderGrid)
    window.sliderGrid = sliderGrid

def createSlider():
    groupBox = QGroupBox("Slider Example")
    slider = QSlider(Qt.Horizontal)
    slider.setFocusPolicy(Qt.StrongFocus)
    slider.setTickPosition(QSlider.TicksBothSides)
    slider.setTickInterval(10)
    slider.setSingleStep(1)

    vbox = QVBoxLayout()
    vbox.addWidget(slider)
    vbox.addStretch(1)
    groupBox.setLayout(vbox)

    return groupBox