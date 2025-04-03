from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime
import sqlite3

class HomePage(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.layout = QVBoxLayout()

        # Create a QTableWidget for structured task display
        self.task_table = QTableWidget()
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(["Title", "Deadline", "Status"])

        # Add table to layout
        self.layout.addWidget(self.task_table)

        # Add buttons for task modification and deletion
        self.modify_button = QPushButton("Modify Task")
        self.modify_button.clicked.connect(self.modify_task)
        self.layout.addWidget(self.modify_button)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        # Set widget layout
        self.setLayout(self.layout)

        # Populate the task list on initialization
        self.update_task_list()

    def update_task_list(self):
        """Updates the task table with current tasks."""
        self.task_table.setRowCount(0)  # Clear the table
        for row_index, task in enumerate(self.tasks):
            # Ensure the task has all 4 fields; use default values if missing
            if len(task) == 3:
                title, deadline, status = task
                completed = ""  # Default to empty string if 'completed' is missing
            else:
                title, deadline, status, completed = task

            self.task_table.insertRow(row_index)

            # Add title
            self.task_table.setItem(row_index, 0, QTableWidgetItem(title))

            # Add deadline
            self.task_table.setItem(row_index, 1, QTableWidgetItem(deadline))

            # Add checkbox for completion status
            checkbox = QCheckBox()
            checkbox.setChecked(status == "Yes")  # Mark as completed if status is "Yes"
            checkbox.stateChanged.connect(lambda state, row=row_index: self.handle_status_change(state, row))
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)  # Center-align checkbox
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.task_table.setCellWidget(row_index, 2, checkbox_widget)

            # Add completed timestamp
            timestamp_item = QTableWidgetItem(completed)
            self.task_table.setItem(row_index, 3, timestamp_item)



    def handle_status_change(self, state, row):
        """Update task status and completion timestamp."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # Determine new status and completed timestamp
        if state == Qt.Checked:
            status = "Yes"
            completed = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm")
        else:
            status = "No"
            completed = ""

        # Update self.tasks
        for i, task in enumerate(self.tasks):
            if task[0] == title and task[1] == deadline:
                self.tasks[i] = (title, deadline, status, completed)
                break

        # Update database
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

        # Refresh task table
        self.update_task_list()

    def modify_task(self):
        """Modify the selected task."""
        selected_row = self.task_table.currentRow()  # Get the selected row index
        if selected_row != -1:
            old_title = self.task_table.item(selected_row, 0).text()
            old_deadline = self.task_table.item(selected_row, 1).text()

            # Open input dialogs for modification
            new_title, ok1 = QInputDialog.getText(self, "Modify Title", "Enter new title:", QLineEdit.Normal, old_title)
            new_deadline, ok2 = QInputDialog.getText(self, "Modify Deadline", "Enter new deadline:", QLineEdit.Normal, old_deadline)

            if ok1 and ok2:  # Ensure both inputs are confirmed
                self.tasks[selected_row] = (new_title, new_deadline, self.tasks[selected_row][2])  # Update locally

                # Update database
                db_name = "tasks.db"
                with sqlite3.connect(db_name) as db:
                    cursor = db.cursor()
                    cursor.execute(
                        """UPDATE Tasks 
                        SET Title = ?, Deadline = ? 
                        WHERE Title = ? AND Deadline = ?""",
                        (new_title, new_deadline, old_title, old_deadline)
                    )
                    db.commit()

                # Refresh task table
                self.update_task_list()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a task to modify.")

    def delete_task(self):
        """Delete the selected task."""
        selected_row = self.task_table.currentRow()  # Get the selected row index
        if selected_row != -1:
            title = self.task_table.item(selected_row, 0).text()
            deadline = self.task_table.item(selected_row, 1).text()

            # Confirm before deletion
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete '{title}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Remove from self.tasks
                self.tasks.pop(selected_row)

                # Remove from database
                db_name = "tasks.db"
                with sqlite3.connect(db_name) as db:
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM Tasks WHERE Title = ? AND Deadline = ?", (title, deadline))
                    db.commit()

                # Refresh task table
                self.update_task_list()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a task to delete.")
