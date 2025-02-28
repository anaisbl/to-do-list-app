import sys
from PyQt5.QtWidgets import *
from home_page import HomePage
from task_page import TaskPage

# core of every Qt app is the QApplication class
# every app needs one QApplication object to function
# this object holds the event loop -- the core loop that governs all UI with the GUI
# each interaction generates an event that is placed on the event queue
# the event handler deals with the event then passes the control back to the event loop

# good approach is to subclass the main window and self contain its behavior

class toDoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # window size and title
        self.setWindowTitle("To do list")
        self.setGeometry(100,100,400,300)

        # list to store tasks
        self.tasks = []

        # create stacked layout and pass to task page
        self.stackedLayout = QStackedLayout()


        # create homepage and task page and pass necessary things
        self.home_page = HomePage(self.tasks)
        self.task_page = TaskPage(self.home_page, self.tasks, self.stackedLayout)
        self.stackedLayout.addWidget(self.home_page)
        self.stackedLayout.addWidget(self.task_page)

        # create and initialize nav buttons
        self.home_button = QPushButton("Home")
        self.add_task_button = QPushButton("Add task")

        # connect buttons to switch pages
        self.home_button.clicked.connect(self.switchHome)
        self.add_task_button.clicked.connect(self.switchTask)

        # Layout for main window
        layout = QVBoxLayout()
        layout.addWidget(self.home_button)
        layout.addWidget(self.add_task_button)
        layout.addLayout(self.stackedLayout)

        # set up the main window layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def switchHome(self):
        self.stackedLayout.setCurrentIndex(0)

    def switchTask(self):
        self.stackedLayout.setCurrentIndex(1)  
    


# Qapplication instance
# passing sys.argv argument to allow CL arguments for the app
app = QApplication(sys.argv)

# create Qtwidget which is our window
window = toDoApp()
window.show()   # because windows are hidden by default

# start event loop
app.exec()