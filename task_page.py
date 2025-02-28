from PyQt5.QtWidgets import *

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
        """Add task to home page and clear fields."""
        title = self.title_input.text()
        deadline = self.deadline_input.text()
        details = self.details_input.text()

        if title:
            # Combine details into one task string
            task = f"Title: {title}, Deadline: {deadline}, Details: {details}"

            # Add the task to the home page task list
            self.home_page.add_task(task)

            # Show success dialog
            self.task_success_dialog()

            # Clear input fields and return to home page
            self.title_input.clear()
            self.deadline_input.clear()
            self.details_input.clear()

            # Go back to the home page
            self.stacked_layout.setCurrentIndex(0)