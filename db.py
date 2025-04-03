import sqlite3

def create_table():
    """Sets up tables for new database"""

    db = sqlite3.connect('tasks.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Deadline TEXT, Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status TEXT, Completed TIMESTAMP                         
        );""")
    
    db.close()

