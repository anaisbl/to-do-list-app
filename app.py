import sys
import getpass
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFontDatabase, QBrush, QColor
from PyQt5.QtCore import Qt, QDateTime, QTimer, QSize
from db import DbInteraction

###_________ NOTES ___________###
# core of every Qt app is the QApplication class
# every app needs one QApplication object to function
# this object holds the event loop -- the core loop that governs all UI with the GUI
# each interaction generates an event that is placed on the event queue
# the event handler deals with the event then passes the control back to the event loop

# good approach is to subclass the main window and self contain its behavior
###_________ END NOTES __________###

class toDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")

        # Initialize the database
        DbInteraction.create_table()
        
        # stylesheet
        self.load_stylesheet("style.qss")

        # add font to font db
        font_path = "assets/font/IndieFlower-Regular.ttf"
        QFontDatabase.addApplicationFont(font_path)

        # window size + title
        self.setWindowTitle("Cute To-do list")
        self.setGeometry(80, 80, 700, 600)

        # create homepage
        self.home_page = HomePage()

        # layout for main window
        layout = QVBoxLayout()
        layout.addWidget(self.home_page)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # load stylesheet
    def load_stylesheet(self, filename):
        with open(filename, "r") as file:
            QApplication.instance().setStyleSheet(file.read())

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setObjectName("Homepage")

        # header section
        self.header_section()

        # create task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Task", "Deadline", "Status", ""])
        self.layout.addWidget(self.task_table)

        self.setLayout(self.layout)

        # Store reference to the task creation window
        self.task_creation_window = None
        self.history_window = None

        # Initial population of the task list
        self.refresh_task_list()

    def header_section(self):
        """Create a greeting section with the username and current date+time and (wip) weather."""
        username = getpass.getuser()  # get current user's name
        current_date = datetime.now().strftime("%A, %d %B %Y") 
        current_time = datetime.now().strftime("%H : %M : %S")

        # greeting label
        greeting_label = QLabel(f"Hey, {username}!")
        greeting_label.setStyleSheet("font-family: Indie Flower; font-size: 40px; font-weight: 800; color: rgb(93, 28, 90);")

        # current date & time label
        date_label = QLabel(f"Today is {current_date}.")
        self.time_label = QLabel(f"The time is {current_time} ")
        date_label.setStyleSheet("font-family: Indie Flower; font-weight: 400; font-size: 28px; color: rgb(90, 53, 88);")
        self.time_label.setStyleSheet("font-family: Indie Flower; font-weight: 400; font-size: 28px; color: rgb(90, 53, 88);")
        self.update_time()

        # current weather (initially empty) -- wip
        # self.weather_label = QPushButton("Click here to set your city for weather info!")
        # self.weather_label.setProperty("button", True)
        # self.weather_label.mousePressEvent = self.prompt_city_input  # attach click event
        
        # history button
        self.hist_button = QPushButton()
        self.hist_button.setIcon(QIcon("assets/icons8-history-folder-64.png"))
        self.hist_button.setIconSize(QSize(40, 40))
        self.hist_button.setProperty("button", False)
        self.hist_button.setToolTip("History")
        self.hist_button.clicked.connect(self.open_history_window)

        # new task button
        self.add_task_button = QPushButton()
        self.add_task_button.setIcon(QIcon("assets/icons8-plus-sign-50.png"))
        self.add_task_button.setIconSize(QSize(40, 40))
        self.add_task_button.setProperty("button", False)
        self.add_task_button.setToolTip("Add task")
        self.add_task_button.clicked.connect(self.open_task_creation_window)

        # group history & add task button
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.hist_button, alignment=Qt.AlignRight)
        button_layout.addWidget(self.add_task_button, alignment=Qt.AlignRight)

        # horizontal layout for top-row alignment
        top_layout = QHBoxLayout()
        top_layout.addWidget(greeting_label, alignment=Qt.AlignLeft)
        top_layout.addLayout(button_layout)

        # vertical layout for the whole section
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(date_label, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.time_label, alignment=Qt.AlignLeft)
        # main_layout.addWidget(self.weather_label, alignment=Qt.AlignLeft)

        # wrap in a QWidget and add to main layout
        greeting_widget = QWidget()
        greeting_widget.setLayout(main_layout)
        self.layout.addWidget(greeting_widget)

        # create a timer to update the time every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)  # connect timer to update_time method
        timer.start(1000)  # update every 1000 milliseconds 
    
    def update_time(self):
        """Update the time label with the current time."""
        current_time = datetime.now().strftime("%H : %M : %S")  # get the current time
        self.time_label.setText(f"The time is {current_time}")

    def open_history_window(self):
        """Open the history window."""
        if not self.history_window or not self.history_window.isVisible():
            self.history_window = HistoryWindow(self)
            self.history_window.show()

    def open_task_creation_window(self):
        """Open the task creation window."""
        if not self.task_creation_window or not self.task_creation_window.isVisible():
            self.task_creation_window = TaskCreationWindow(self)
            self.task_creation_window.show()

    def refresh_task_list(self):
        """Refresh the task table, handle status changes, and exclude completed tasks."""
        self.task_table.setRowCount(0)  # clear the table to avoid dups
        row_counter = 0

        #word wrap
        self.task_table.setWordWrap(True)

        # retrieve tasks
        tasks = DbInteraction.fetch_tasks()

        for task in tasks:
            title, deadline, status, completed = task

            # only show tasks where the status is "Pending"
            if status == "Pending":
                # add the task title with word wrap
                task_item = QTableWidgetItem(title)
                task_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.task_table.insertRow(row_counter)
                self.task_table.setItem(row_counter, 0, task_item)

                # add deadline
                deadline_item = QTableWidgetItem(deadline)
                deadline_item.setTextAlignment(Qt.AlignCenter)
                self.task_table.setItem(row_counter, 1, deadline_item)

                # add a checkbox for task completion
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                checkbox.setToolTip("Mark complete")
                checkbox.stateChanged.connect(lambda state, row=row_counter: self.handle_status_change(state, row))
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                self.task_table.setCellWidget(row_counter, 2, checkbox_widget)

                # add modify + delete buttons
                modify_button = QPushButton()
                modify_button.setIcon(QIcon("assets/icons8-edit-64.png"))
                modify_button.clicked.connect(lambda _, row=row_counter: self.modify_task(row))
                modify_button.setProperty("button", False)
                modify_button.setToolTip("Edit task")

                delete_button = QPushButton()
                delete_button.setIcon(QIcon("assets/icons8-trash-can-64.png"))
                delete_button.clicked.connect(lambda _, row=row_counter: self.delete_task(row))
                delete_button.setProperty("button", False)
                delete_button.setToolTip("Delete task")

                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.addWidget(modify_button)
                button_layout.addWidget(delete_button)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_layout.setAlignment(Qt.AlignCenter)
                self.task_table.setCellWidget(row_counter, 3, button_widget)

                # apply overdue styling
                self.apply_overdue_styling(row_counter, deadline)

                # increment the visible row index
                row_counter += 1
            
            # resize rows to fit wrapped text
            self.task_table.resizeRowsToContents()
    
    def handle_status_change(self, state, row):
        """Update task status, hide completed tasks, and update the database."""
        title = self.task_table.item(row, 0).text()
        deadline = self.task_table.item(row, 1).text()

        # Determine new status and completed timestamp
        if state == Qt.Checked:
            status = "Done"
            completed = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm")
            self.success_dialog("Task completed!")
        else:
            status = "Pending"
            completed = ""

        # Update the task in the database
        DbInteraction.update_task_status(title, deadline, status, completed)

        # Refresh the task table
        self.refresh_task_list()

    def apply_overdue_styling(self, row_index, deadline):
        """Apply styling to a task row if the deadline is overdue."""
        try:
            # parse the deadline
            task_deadline = datetime.strptime(deadline, "%d-%m-%y")
            
            # check if the task is overdue & apply styling
            if task_deadline < datetime.now():
                for col in range(2):
                    task_item = self.task_table.item(row_index, col)
                    print(task_item)
                    if task_item:
                        font = task_item.font()
                        font.setBold(True)
                        task_item.setFont(font)
                        task_item.setForeground(QBrush(QColor(255, 0, 0)))
        except ValueError:
            pass  # ignore invalid date formats
    
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
        self.home_page = home_page  # reference to refresh task list after creation
        self.setWindowTitle("Add new task")
        self.setGeometry(150, 80, 400, 300)
        self.setObjectName("TaskCreationWindow")

        # layout
        self.layout = QFormLayout()

        # labels
        task_label = QLabel("Task: ")
        deadline_label = QLabel("Deadline: ")

        task_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 800;
            font-family: 'Indie Flower';
            color: rgb(93, 28, 90);
        """)
        deadline_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 800;
            font-family: 'Indie Flower';
            color: rgb(93, 28, 90);
        """)

        # inputs
        self.title_input = QTextEdit()
        self.title_input.setFixedWidth(400)
        self.title_input.setFixedHeight(80)
        self.deadline_input = QCalendarWidget()
        self.deadline_input.setFixedSize(400, 300)
        self.no_deadline_checkbox = QCheckBox("No deadline")

        # group deadline input and checkbox
        deadline_layout = QVBoxLayout()
        deadline_layout.addWidget(self.deadline_input)
        deadline_layout.addWidget(self.no_deadline_checkbox)
        deadline_layout.setAlignment(Qt.AlignCenter)

        # save + cancel buttons grouped as well
        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.save_task)
        self.save_button.setProperty("button", True)
        self.save_button.setFixedWidth(180)
        self.save_button.setFixedHeight(40)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setProperty("button", True)
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setFixedWidth(180)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.setAlignment(Qt.AlignRight)

        # Add widgets to layout
        self.layout.addRow(task_label, self.title_input)
        self.layout.addRow(deadline_label, deadline_layout)
        self.layout.addRow(button_layout)

        self.setLayout(self.layout)

    def save_task(self):
        """Save the task to the database and refresh the homepage."""
        title = self.title_input.toPlainText()
        deadline = "No deadline" if self.no_deadline_checkbox.isChecked() else self.deadline_input.selectedDate().toString("dd-MM-yy")

        if title:
            DbInteraction.save_task(title, deadline)
            self.home_page.refresh_task_list()
            self.close()

            # show success message
            QMessageBox.information(self, "Success","Task created successfully!")
        else:
            QMessageBox.information(self, "Error", "Missing inputs!")

class HistoryWindow(QWidget):
    def __init__(self, home_page):
        super().__init__()
        self.layout = QVBoxLayout()
        self.home_page = home_page  # reference to refresh task list after creation
        self.setWindowTitle("Task history")
        self.setGeometry(150, 80, 900, 600)
        self.setObjectName("HistoryWindow")

        # header section
        self.top_filter_section()

        # table of tasks
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Task", "Created on", "Due", "Status", "Complete on"])
        self.layout.addWidget(self.history_table)
        self.setLayout(self.layout)

        # populate table
        self.display_all_tasks()

    def top_filter_section(self):
        """Create a top section with filters to rowse through all tasks ever created."""

        # intro
        intro_label = QLabel(f"Here is a history of all your tasks.")
        intro_label.setStyleSheet("font-family: Indie Flower; font-size: 30px; font-weight: 800; color: rgb(93, 28, 90);")

        # filters
        self.all_tasks_button = QPushButton("View all tasks")
        self.all_tasks_button.setProperty("button", True)
        self.all_tasks_button.setToolTip("Sort pending tasks")
        self.all_tasks_button.clicked.connect(self.display_all_tasks)

        self.pending_task_button = QPushButton("View pending tasks")
        self.pending_task_button.setProperty("button", True)
        self.pending_task_button.setToolTip("Sort pending tasks")
        self.pending_task_button.clicked.connect(self.pending_task_filter)

        self.date_asc_button = QPushButton("Sort by date due (asc)")
        self.date_asc_button.setProperty("button", True)
        self.date_asc_button.setToolTip("Sort ealiest to latest due")
        self.date_asc_button.clicked.connect(self.date_asc_filter)

        filter_button_layout = QHBoxLayout()
        filter_button_layout.addWidget(self.all_tasks_button, alignment=Qt.AlignLeft)
        filter_button_layout.addWidget(self.pending_task_button, alignment=Qt.AlignLeft)
        filter_button_layout.addWidget(self.date_asc_button, alignment=Qt.AlignLeft)

        # add to layout
        self.layout.addWidget(intro_label)
        self.layout.addLayout(filter_button_layout)
    
    def display_all_tasks(self):
        """Display all tasks in the history task table"""
        self.history_table.setRowCount(0)  # clear the table to avoid dups
        row_counter = 0
        all_tasks = False #flag to check for tasks

        #word wrap
        self.history_table.setWordWrap(True)

        # retrieve tasks
        tasks = DbInteraction.grab_all_history()

        for task in tasks:
            all_tasks = True
            title, creation, deadline, status, completed = task

            # add task title
            task_item = QTableWidgetItem(title)
            task_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.history_table.insertRow(row_counter)
            self.history_table.setItem(row_counter, 0, task_item)

            # add task creation
            task_creation_item = QTableWidgetItem(creation)
            task_creation_item.setTextAlignment(Qt.AlignVCenter)
            self.history_table.setItem(row_counter, 1, task_creation_item)

            # add deadline
            deadline_item = QTableWidgetItem(deadline)
            deadline_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row_counter, 2, deadline_item)

            # add status
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row_counter, 3, status_item)

            # add completion date
            completion_item = QTableWidgetItem(completed)
            completion_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row_counter, 4, completion_item)

            # Increment the visible row index
            row_counter += 1
            
        # Resize rows to fit wrapped text
        self.history_table.resizeRowsToContents()

        if not all_tasks:
            self.no_task_dialog("No tasks in history!")
    
    def pending_task_filter(self):
        """Filter out tasks that are pending in the history task table"""
        self.history_table.setRowCount(0)  # clear the table to avoid dups
        row_counter = 0
        pending_tasks = False # flag to check for pending tasks

        #word wrap
        self.history_table.setWordWrap(True)

        # retrieve tasks
        tasks = DbInteraction.grab_all_history()

        for task in tasks:
            title, creation, deadline, status, completed = task

            if status == "Pending":
                pending_tasks = True

                # add task title
                task_item = QTableWidgetItem(title)
                task_item.setTextAlignment(Qt.AlignLeft | Qt.AlignCenter)
                self.history_table.insertRow(row_counter)
                self.history_table.setItem(row_counter, 0, task_item)

                # add task creation
                task_creation_item = QTableWidgetItem(creation)
                task_creation_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 1, task_creation_item)

                # add deadline
                deadline_item = QTableWidgetItem(deadline)
                deadline_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 2, deadline_item)

                # add status
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 3, status_item)

                # add completion date
                completion_item = QTableWidgetItem(completed)
                completion_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 4, completion_item)

                # increment the visible row index
                row_counter += 1
                
        # resize rows to fit wrapped text
        self.history_table.resizeRowsToContents()
        
        if not pending_tasks:
            self.no_task_dialog("No pending tasks!")
    
    def date_asc_filter(self):
        """Sort tasks ascending by status, earliest due date on top in the history task table"""
        self.history_table.setRowCount(0)  # clear the table to avoid dups
        row_counter = 0
        all_tasks = False # flag to check for pending tasks

        #word wrap
        self.history_table.setWordWrap(True)

        # retrieve tasks
        tasks = DbInteraction.grab_all_history()

        # convert deadline to datetime objects for sorting
        sorted_tasks = []
        for task in tasks:
            title, creation, deadline, status, completed = task
            try:
                deadline_date = datetime.strptime(deadline, "%d-%m-%y")
            except ValueError:
                # account for "no deadline"
                deadline_date = None

            sorted_tasks.append((deadline_date, title, creation, deadline, status, completed))

        # sort tasks by the parsed datetime object (earliest first)
        sorted_tasks.sort(key=lambda task: (task[0] is None, task[0] or datetime.max))
        for deadline_date, title, creation, deadline, status, completed in sorted_tasks:

            if deadline_date != None:
                all_tasks = True

                # add task title
                task_item = QTableWidgetItem(title)
                task_item.setTextAlignment(Qt.AlignLeft | Qt.AlignCenter)
                self.history_table.insertRow(row_counter)
                self.history_table.setItem(row_counter, 0, task_item)

                # add task creation
                task_creation_item = QTableWidgetItem(creation)
                task_creation_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 1, task_creation_item)

                # add deadline
                if deadline_date is not None:
                    formatted_deadline = deadline_date.strftime("%d-%m-%y") # back into string
                else:
                    formatted_deadline = deadline
                deadline_item = QTableWidgetItem(formatted_deadline)
                deadline_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 2, deadline_item)

                # add status
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 3, status_item)

                # add completion date
                completion_item = QTableWidgetItem(completed)
                completion_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_counter, 4, completion_item)

                # increment the visible row index
                row_counter += 1

        # resize rows to fit wrapped text
        self.history_table.resizeRowsToContents()
        
        if not all_tasks:
            self.no_task_dialog("No tasks in history!")
    
    def no_task_dialog(self, message):
        """Dialog box for when the filter buttons return nothing"""
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Task History")
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec()
        if button == QMessageBox.Ok:
            print("OK!")


# Qapplication instance
# passing sys.argv argument to allow CL arguments for the app
app = QApplication(sys.argv)

# create Qtwidget which is our window
window = toDoApp()
window.show()   # because windows are hidden by default

# start event loop
app.exec()