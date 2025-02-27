import sys
from PyQt5.QtWidgets import *

# core of every Qt app is the QApplication class
# every app needs one QApplication object to function
# this object holds the event loop -- the core loop that governs all UI with the GUI
# each interaction generates an event that is placed on the event queue
# the event handler deals with the event then passes the control back to the event loop

# good approach is to subclass the main window and self contain its behavior

class toDoApp(QWidget):
    def __init__(self):
        super().__init__()

        # window size and title
        self.setWindowTitle("To do list")
        self.setGeometry(100,100,400,300)

        # list to store tasks
        self.tasks = []

        # top level layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # button to switch to another page
        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Home", "Add Task"])
        self.pageCombo.activated.connect(self.switchPage)

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()

        # add home page
        self.home_page = QWidget()
        self.home_pageLayout = QVBoxLayout()
        self.task_list = QListWidget()  # List to display tasks
        self.home_pageLayout.addWidget(self.task_list)
        self.home_page.setLayout(self.home_pageLayout)
        self.stackedLayout.addWidget(self.home_page)

        # add task page
        self.task_page = QWidget()
        self.task_pageLayout = QFormLayout()

        # input fields
        self.title_input = QLineEdit()
        self.deadline_input = QLineEdit()
        self.details_input = QLineEdit()

        # Add a button to save the task
        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.add_task)

        self.task_pageLayout.addRow("Title", self.title_input)
        self.task_pageLayout.addRow("Deadline", self.deadline_input)
        self.task_pageLayout.addRow("Details", self.details_input)
        self.task_pageLayout.addWidget(self.save_button)

        self.task_page.setLayout(self.task_pageLayout)
        self.stackedLayout.addWidget(self.task_page)

        # combo box & stacked layout to main layout
        layout.addWidget(self.pageCombo)
        layout.addLayout(self.stackedLayout)


    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())

    def add_task(self):
        title = self.title_input.text()
        deadline = self.deadline_input.text()
        details = self.details_input.text()

        if title:
            task = f"Title: {title}, Deadline: {deadline}, Details: {details}"
            self.tasks.append(task)

            # add task to task list on home page
            self.task_list.addItem(task)

            # clear input fields & return to home page
            self.title_input.clear()
            self.deadline_input.clear()
            self.details_input.clear()
            self.pageCombo.setCurrentIndex(0)  # Switch to Home page
            self.stackedLayout.setCurrentIndex(0)        
    


# Qapplication instance
# passing sys.argv argument to allow CL arguments for the app
app = QApplication(sys.argv)

# create Qtwidget which is our window
window = toDoApp()
window.show()   # because windows are hidden by default

# start event loop
app.exec()