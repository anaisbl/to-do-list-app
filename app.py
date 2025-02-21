import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

# core of every Qt app is the QApplication class
# every app needs one QApplication object to function
# this object holds the event loop -- the core loop that governs all UI with the GUI
# each interaction generates an event that is placed on the event queue
# the event handler deals with the event then passes the control back to the event loop

# good approach is to subclass the main window and self contain its behavior

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To do list")
        button = QPushButton("Idk what this does")

        # set central widget of the window
        self.setCentralWidget(button)

# Qapplication instance
# passing sys.argv argument to allow CL arguments for the app
app = QApplication(sys.argv)

# create Qtwidget which is our window
window = MainWindow()
window.show()   # because windows are hidden by default

# start event loop
app.exec()