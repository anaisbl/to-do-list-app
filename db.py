import sqlite3

class DbInteraction:
    # static methods don't rely on instance attr, they only interact with the db
    @staticmethod
    def create_table():
        """Sets up tables for new database"""
        db = sqlite3.connect('tasks.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Tasks (
                TaskID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Deadline TEXT, Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status TEXT, Completed TIMESTAMP                         
            );""")
        
        db.close()
    
    @staticmethod
    def save_task(title, deadline, status="Pending", completed=""):
        """Save a task into the database."""
        with sqlite3.connect('tasks.db') as db:
            cur = db.cursor()
            cur.execute(
                """INSERT INTO Tasks (Title, Deadline, Status, Completed) 
                VALUES (?, ?, ?, ?)""",
                (title, deadline, status, completed)
            )
            db.commit()
        
    @staticmethod
    def fetch_tasks():
        """Fetch all tasks, 4 cols from the database."""
        with sqlite3.connect('tasks.db') as db:
            cur = db.cursor()
            cur.execute("SELECT Title, Deadline, Status, Completed FROM Tasks")
            return cur.fetchall()
    
    @staticmethod
    def grab_all_history():
         """"Fetch all tasks, all cols from db for the history view"""
         with sqlite3.connect('tasks.db') as db:
            cur = db.cursor()
            cur.execute("SELECT Title, Deadline, Created, Status, Completed FROM Tasks")
            return cur.fetchall()

    @staticmethod
    def delete_task(title, deadline):
        """Delete a task from the database."""
        with sqlite3.connect('tasks.db') as db:
            cur = db.cursor()
            cur.execute("DELETE FROM Tasks WHERE Title = ? AND Deadline = ?", (title, deadline))
            db.commit()
    
    @staticmethod
    def update_task_status(title, deadline, status, completed):
        """Update completion status of task"""
        with sqlite3.connect('tasks.db') as db:
            cursor = db.cursor()
            cursor.execute(
                """UPDATE Tasks 
                SET Status = ?, Completed = ? 
                WHERE Title = ? AND Deadline = ?""",
                (status, completed, title, deadline)
            )
            db.commit()
    @staticmethod
    def update_task(new_title, new_deadline, title, deadline):
        with sqlite3.connect('tasks.db') as db:
                cursor = db.cursor()
                cursor.execute(
                    """UPDATE Tasks 
                    SET Title = ?, Deadline = ? 
                    WHERE Title = ? AND Deadline = ?""",
                    (new_title, new_deadline, title, deadline)
                )
                db.commit()
    @staticmethod
    def delete_task(title, deadline):
        with sqlite3.connect('tasks.db') as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM Tasks WHERE Title = ? AND Deadline = ?", (title, deadline))
                db.commit()

