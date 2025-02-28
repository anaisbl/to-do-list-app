import sys
from PyQt5.QtWidgets import *

class HomePage(QWidget):
    def __init__(self, tasks):
        super().__init__()

        self.tasks = tasks

        self.layout = QVBoxLayout()

        # Task list display
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        self.setLayout(self.layout)

        self.update_task_list()
    
    def add_task(self, task):
        """Adds a task to the home page task list."""
        self.tasks.append(task)  # Add to the shared task list
        self.update_task_list()

    def update_task_list(self):
        """Updates the task list displayed on the HomePage."""
        self.task_list.clear()  # Clear the list first
        self.task_list.addItems(self.tasks)  # Add all tasks