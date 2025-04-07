import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDateTime
from db import DbInteraction
# core of every Qt app is the QApplication class
# every app needs one QApplication object to function
# this object holds the event loop -- the core loop that governs all UI with the GUI
# each interaction generates an event that is placed on the event queue
# the event handler deals with the event then passes the control back to the event loop

# good approach is to subclass the main window and self contain its behavior

class toDoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the database
        DbInteraction.create_table()

        # Window size and title
        self.setWindowTitle("To-Do List")
        self.setGeometry(80, 80, 700, 400)

        # stylesheet
        self.load_stylesheet("style.qss")

        # Create homepage
        self.home_page = HomePage()

        # Add Task button to open TaskCreationWindow
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.open_task_creation_window)

        # Layout for main window
        layout = QVBoxLayout()
        layout.addWidget(self.add_task_button)
        layout.addWidget(self.home_page)

        # Set main window layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Store reference to the task creation window
        self.task_creation_window = None

    def open_task_creation_window(self):
        """Open the task creation window."""
        if not self.task_creation_window or not self.task_creation_window.isVisible():
            self.task_creation_window = TaskCreationWindow(self.home_page)
            self.task_creation_window.show()

    # load stylesheet
    def load_stylesheet(app, filename):
        with open(filename, "r") as file:
            app.setStyleSheet(file.read())

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Create task table
        self.task_table = QTableWidget()
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Task", "Deadline", "Status", ""])
        self.layout.addWidget(self.task_table)

        self.setLayout(self.layout)

        # Initial population of the task list
        self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the task table, handle status changes, and exclude completed tasks."""
        self.task_table.setRowCount(0)  # Clear the table
        row_counter = 0
        tasks = DbInteraction.fetch_tasks()

        for task in tasks:
            title, deadline, status, completed = task

            # Only show tasks where the status is "No" (not completed)
            if status == "No":
                # Add new row with title & deadline
                self.task_table.insertRow(row_counter)
                self.task_table.setItem(row_counter, 0, QTableWidgetItem(title))
                self.task_table.setItem(row_counter, 1, QTableWidgetItem(deadline))

                # Add a checkbox for task completion
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                checkbox.stateChanged.connect(lambda state, row=row_counter: self.handle_status_change(state, row))
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                self.task_table.setCellWidget(row_counter, 2, checkbox_widget)

                # Add "Modify" and "Delete" buttons
                modify_button = QPushButton()
                modify_button.setIcon(QIcon("assets/icons8-edit-64.png"))
                modify_button.clicked.connect(lambda _, row=row_counter: self.modify_task(row))

                delete_button = QPushButton()
                delete_button.setIcon(QIcon("assets/icons8-trash-can-64.png"))
                delete_button.clicked.connect(lambda _, row=row_counter: self.delete_task(row))

                # Create a widget to hold the buttons
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.addWidget(modify_button)
                button_layout.addWidget(delete_button)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_layout.setAlignment(Qt.AlignCenter)
                self.task_table.setCellWidget(row_counter, 3, button_widget)  # Add buttons to column 3

                # Increment the visible row index
                row_counter += 1
    
    def handle_status_change(self, state, row):
        """Update task status, hide completed tasks, and update the database."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # Determine new status and completed timestamp
        if state == Qt.Checked:
            status = "Yes"
            completed = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm")
            self.success_dialog("Task completed!")
        else:
            status = "No"
            completed = ""

        # Update the task in the database
        DbInteraction.update_task_status(title, deadline, status, completed)

        # Refresh the task table
        self.refresh_task_list()
    
    def success_dialog(self, message):
        # dialog box for user response
        dlg = QMessageBox(self)
        dlg.setWindowTitle("To List App")
        dlg.setText(message)
        button = dlg.exec()
        if button == QMessageBox.Ok:
            print("OK!")
    
    def modify_task(self, row):
        """Modify the task for the given row."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # input dialogs for modification
        new_title, ok1 = QInputDialog.getText(self, "Modify Title", "Enter new title:", QLineEdit.Normal, title)
        new_deadline, ok2 = QInputDialog.getText(self, "Modify Deadline", "Enter new deadline:", QLineEdit.Normal, deadline)

        # fetch db 
        tasks = DbInteraction.fetch_tasks()

        if ok1 and ok2:  # check both inputs are confirmed
            tasks[row] = (new_title, new_deadline, tasks[row][2])  # update locally

            # update database
            DbInteraction.update_task(new_title, new_deadline, title, deadline)

            # success msg
            self.success_dialog("Task modified!")

            # refresh task table
            self.refresh_task_list()
    
    def delete_task(self, row):
        """Delete the task for the given row."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # fetch db 
        tasks = DbInteraction.fetch_tasks()

        # Confirm before deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{title}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Remove from self.tasks
            tasks.pop(row)

            # Remove from database
            DbInteraction.delete_task(title, deadline)

            # success msg
            self.success_dialog("Task deleted!")

            # refresh task table
            self.refresh_task_list()



class TaskCreationWindow(QWidget):
    def __init__(self, home_page):
        super().__init__()
        self.home_page = home_page  # Reference to refresh task list after creation

        # Layout for task creation
        self.layout = QFormLayout()

        # Inputs for task title and deadline
        self.title_input = QLineEdit()
        self.deadline_input = QCalendarWidget()
        self.no_deadline_checkbox = QCheckBox("No deadline")

        # Group deadline input and checkbox
        deadline_layout = QHBoxLayout()
        deadline_layout.addWidget(self.deadline_input)
        deadline_layout.addWidget(self.no_deadline_checkbox)

        # Buttons for saving and canceling
        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.save_task)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        # Add widgets to layout
        self.layout.addRow("Title", self.title_input)
        self.layout.addRow("Deadline", deadline_layout)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def save_task(self):
        """Save the task to the database and refresh the homepage."""
        title = self.title_input.text()
        deadline = "No deadline" if self.no_deadline_checkbox.isChecked() else self.deadline_input.selectedDate().toString("dd-MM-yy")

        if title:
            DbInteraction.save_task(title, deadline)  # Save to the database
            self.home_page.refresh_task_list()       # Refresh tasks on the homepage
            self.close()                             # Close the creation window

            # Show success message
            QMessageBox.information(self, "Success", "Task created successfully!")

# Qapplication instance
# passing sys.argv argument to allow CL arguments for the app
app = QApplication(sys.argv)

# create Qtwidget which is our window
window = toDoApp()
window.show()   # because windows are hidden by default

# start event loop
app.exec()