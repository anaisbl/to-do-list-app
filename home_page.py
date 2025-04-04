from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
import sqlite3

class HomePage(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.layout = QVBoxLayout()

        # Create a QTableWidget for structured task display
        self.task_table = QTableWidget()
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Task", "Deadline", "Status", ""])

        # Add table to layout
        self.layout.addWidget(self.task_table)

        # Set widget layout
        self.setLayout(self.layout)

        # Populate the task list on initialization
        self.update_task_list()

    def update_task_list(self):
        """Updates the task table, excluding completed tasks."""
        self.task_table.setRowCount(0)  # Clear the table
        row_counter = 0
        for task in self.tasks:
            title, deadline, status, completed = task

            # Only show tasks where the status is not completed
            if status == "No":
                # Add new row with title & deadline
                self.task_table.insertRow(row_counter)
                self.task_table.setItem(row_counter, 0, QTableWidgetItem(title))
                self.task_table.setItem(row_counter, 1, QTableWidgetItem(deadline))

                # Add "Modify" button
                modify_button = QPushButton()
                modify_button.setIcon(QIcon("assets/icons8-edit-64.png"))
                modify_button.clicked.connect(lambda _, row=row_counter: self.modify_task(row))

                # Add "Delete" button
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
        """Update task status and refresh the table to hide completed tasks."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # Determine new status and completed timestamp
        if state == Qt.Checked:
            status = "Yes"
            completed = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm")
            self.task_complete_dialog()
        else:
            status = "No"
            completed = ""

        # Update the task in self.tasks
        for i, task in enumerate(self.tasks):
            if task[0] == title and task[1] == deadline:
                self.tasks[i] = (title, deadline, status, completed)
                break

        # Update the database
        db_name = "tasks.db"
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute(
                """UPDATE Tasks 
                SET Status = ?, Completed = ? 
                WHERE Title = ? AND Deadline = ?""",
                (status, completed, title, deadline)
            )
            db.commit()

        # Refresh the task table to hide completed tasks
        self.update_task_list()
    
    def task_complete_dialog(self):
        # dialog box for user response
        dlg = QMessageBox(self)
        dlg.setWindowTitle("To List App")
        dlg.setText("Task completed!")
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

        if ok1 and ok2:  # check both inputs are confirmed
            self.tasks[row] = (new_title, new_deadline, self.tasks[row][2])  # update locally

            # update database
            db_name = "tasks.db"
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute(
                    """UPDATE Tasks 
                    SET Title = ?, Deadline = ? 
                    WHERE Title = ? AND Deadline = ?""",
                    (new_title, new_deadline, title, deadline)
                )
                db.commit()

            # refresh task table
            self.update_task_list()

    def delete_task(self, row):
        """Delete the task for the given row."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # Confirm before deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{title}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Remove from self.tasks
            self.tasks.pop(row)

            # Remove from database
            db_name = "tasks.db"
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM Tasks WHERE Title = ? AND Deadline = ?", (title, deadline))
                db.commit()

            # Refresh task table
            self.update_task_list()