from PyQt5.QtWidgets import QMessageBox

def displayMessage(app, message):
    QMessageBox.information(app, 'Message Display', message, QMessageBox.Ok)

def displayWarning(app, message):
    QMessageBox.warning(app, 'Warning Display', message, QMessageBox.Ok)

def displayQuestion(app, message):
    return QMessageBox.question(app, 'Question Display', message,
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)