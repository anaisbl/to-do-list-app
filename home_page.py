from PyQt5.QtWidgets import *
import sqlite3

class HomePage(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.layout = QVBoxLayout()

        # create a QTreeWidget for structured task display
        self.task_list = QTreeWidget()
        self.task_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.task_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_list.setColumnCount(3)
        self.task_list.setHeaderLabels(["Title", "Deadline", "Details"])

        # add task list to layout
        self.layout.addWidget(self.task_list)

        # add delete and modify buttons for tasks
        self.modify_button = QPushButton("Modify task")
        self.modify_button.clicked.connect(self.modify_task)
        self.layout.addWidget(self.modify_button)
        self.delete_button = QPushButton("Delete task")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        # set widget layout
        self.setLayout(self.layout)

        # populate the task list on initialization
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

    def modify_task(self):
        """Modify the selected task."""
        selected_item = self.task_list.currentItem()  # Get the currently selected row
        if selected_item:
            # Get current task details
            old_title = selected_item.text(0)
            old_deadline = selected_item.text(1)
            old_details = selected_item.text(2)

            # Open input dialogs for each field
            new_title, ok1 = QInputDialog.getText(self, "Modify Title", "Enter new title:", QLineEdit.Normal, old_title)
            new_deadline, ok2 = QInputDialog.getText(self, "Modify Deadline", "Enter new deadline:", QLineEdit.Normal, old_deadline)
            new_details, ok3 = QInputDialog.getText(self, "Modify Details", "Enter new details:", QLineEdit.Normal, old_details)

            if ok1 and ok2 and ok3:  # Ensure all inputs are confirmed
                # Update task in self.tasks
                self.tasks = [
                    (new_title, new_deadline, new_details) if task == (old_title, old_deadline, old_details) else task
                    for task in self.tasks
                ]

                # Update task in the database
                db_name = "tasks.db"
                with sqlite3.connect(db_name) as db:
                    cursor = db.cursor()
                    cursor.execute(
                        """UPDATE Tasks 
                        SET Title = ?, Deadline = ?, Details = ? 
                        WHERE Title = ? AND Deadline = ? AND Details = ?""",
                        (new_title, new_deadline, new_details, old_title, old_deadline, old_details)
                    )
                    db.commit()

                # Refresh the task list
                self.update_task_list()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a task to modify.")

    def delete_task(self):
        """Delete the selected task from the list and the database."""
        selected_item = self.task_list.currentItem()  # Get the currently selected row
        if selected_item:
            title = selected_item.text(0)  # Title is in the first column
            deadline = selected_item.text(1)  # Deadline is in the second column
            details = selected_item.text(2)  # Details are in the third column

            # Confirm before deletion
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete '{title}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Remove task from self.tasks
                self.tasks = [task for task in self.tasks if task != (title, deadline, details)]

                # Remove task from the database
                db_name = "tasks.db"
                with sqlite3.connect(db_name) as db:
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM Tasks WHERE Title = ? AND Deadline = ? AND Details = ?", (title, deadline, details))
                    db.commit()

                # Refresh the task list
                self.update_task_list()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a task to delete.")
