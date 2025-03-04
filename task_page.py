from PyQt5.QtWidgets import *
from datetime import datetime
import sqlite3

class TaskPage(QWidget):
    def __init__(self, home_page, tasks, stacked_layout):
        super().__init__()
        
        self.home_page = home_page  # to add tasks to the home page
        self.tasks = tasks  # to keep track of tasks
        self.stacked_layout = stacked_layout  # reference to stacked layout

        # stacked layout is responsible for switching pagesn and we can use setcurrentindex correctly

        # layout
        self.layout = QFormLayout()

        # input fields
        self.title_input = QLineEdit()
        self.deadline_input = QTimeEdit()
        self.deadline_calendar_widget = QCalendarWidget()
        self.deadline_calendar_widget.setMinimumDate(datetime.today())
        self.no_deadline_checkbox = QCheckBox("No deadline")
        self.details_input = QLineEdit()

        # button to save and cancel the task
        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.add_task)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_task)

        # add widgets to layout
        self.layout.addRow("Title", self.title_input)
        self.layout.addRow("Deadline", self.deadline_input)
        self.layout.addRow("Details", self.details_input)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def cancel_task(self):
        # clear input fields & return to home page
        self.title_input.clear()
        self.deadline_input.clear()
        self.details_input.clear()
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
        deadline = self.deadline_input.text()
        details = self.details_input.text()

        if title:
            # Combine details into one task string (optional for display purposes)
            task = f"Title: {title}, Deadline: {deadline}, Details: {details}"

            # Save the task to the database
            self.save_task_to_db(title, deadline, details)

            # Add the task to the home page task list (if needed)
            self.home_page.add_task(task)

            # Show success dialog
            self.task_success_dialog()

            # Clear input fields and return to home page
            self.title_input.clear()
            self.deadline_input.clear()
            self.details_input.clear()

            # Go back to the home page
            self.stacked_layout.setCurrentIndex(0)

    def save_task_to_db(self, title, deadline, details):
        """Save the task into the database."""
        db_name = "tasks.db"  # Your database name
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()

            # Insert new task into the Tasks table
            cursor.execute("""INSERT INTO Tasks (Title, Deadline, Details)
                            VALUES (?, ?, ?)""", (title, deadline, details))
            
            db.commit()
