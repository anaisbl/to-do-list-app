from PyQt5.QtWidgets import *

class HomePage(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        print("Tasks received by HomePage:", self.tasks)  # Debug statement
        self.layout = QVBoxLayout()

        # create a QTreeWidget for structured task display
        self.task_list = QTreeWidget()
        self.task_list.setColumnCount(3)  # Title, Deadline, Details
        self.task_list.setHeaderLabels(["Title", "Deadline", "Details"])

        self.layout.addWidget(self.task_list)
        self.setLayout(self.layout)

        # Populate the task list on initialization
        self.update_task_list()

    def update_task_list(self, new_task=None):
       """Updates the task list displayed on the HomePage."""
       self.task_list.clear()
       if new_task:
            self.tasks.append(new_task)

       for task in self.tasks:
            title, deadline, details = task  # Unpack the tuple
            item = QTreeWidgetItem([title, deadline, details])  # Create a new row
            self.task_list.addTopLevelItem(item)  # Add the row to the QTreeWidget