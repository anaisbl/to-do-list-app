from PyQt5.QtWidgets import *
from datetime import datetime
import sqlite3

class TaskPage(QWidget):
    def __init__(self, home_page, tasks, stacked_layout):
        super().__init__()
        
        self.home_page = home_page  # to add tasks to the home page
        self.tasks = tasks  # to keep track of tasks
        self.stacked_layout = stacked_layout  # reference to stacked layout

        # stacked layout is responsible for switching pages and we can use setcurrentindex correctly

        # layout
        self.layout = QFormLayout()

        # input fields
        self.title_input = QLineEdit()
        self.deadline_input = QCalendarWidget()
        self.deadline_input.setMinimumDate(datetime.today())
        self.no_deadline_checkbox = QCheckBox("No deadline")

        # group deadline input and checkbox in a horizontal layout
        deadline_layout = QHBoxLayout()
        deadline_layout.addWidget(self.deadline_input)
        deadline_layout.addWidget(self.no_deadline_checkbox)

        # buttons to save and cancel the task
        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.add_task)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_task)

        # add widgets to layout
        self.layout.addRow("Title", self.title_input)
        self.layout.addRow("Deadline", deadline_layout)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def cancel_task(self):
        # clear input fields & return to home page
        self.title_input.clear()
        self.deadline_input.setSelectedDate(self.deadline_input.minimumDate())
        self.stacked_layout.setCurrentIndex(0)   

    def task_success_dialog(self):
        # dialog box for user response
        dlg = QMessageBox(self)
        dlg.setWindowTitle("To List App")
        dlg.setText("Task created!")
        button = dlg.exec()
        if button == QMessageBox.Ok:
            print("OK!")

    def add_task(self):
        """Add task to home page, save to database, and clear fields."""
        title = self.title_input.text()

        # handle deadline
        if self.no_deadline_checkbox.isChecked():
            deadline = "No deadline"
        else:
            selected_date = self.deadline_input.selectedDate().toString("dd-MM-yy")
            deadline = f"{selected_date}"

        if title:
            # save the task to the database
            self.save_task(title, deadline)

            # add task to homepage
            self.tasks.append((title, deadline, "No", ""))

            # Refresh the HomePage display
            self.home_page.update_task_list()

            # Show success dialog
            self.task_success_dialog()

            # Clear input fields and return to the home page
            self.title_input.clear()
            self.deadline_input.setSelectedDate(self.deadline_input.minimumDate())
            self.stacked_layout.setCurrentIndex(0)

    def save_task(self, title, deadline):
        """Save the task into the database."""
        db_name = "tasks.db"
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            # Insert new task into the Tasks table with Status and Completed fields
            cursor.execute("""INSERT INTO Tasks (Title, Deadline, Status, Completed)
                            VALUES (?, ?, ?, ?)""", (title, deadline, "No", ""))
            db.commit()

