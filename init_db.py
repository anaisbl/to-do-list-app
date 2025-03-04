import sqlite3

def create_new_db(db_name):
    """Sets up tables for new database"""
    
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        # Create Tasks table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Deadline TEXT,        Details TEXT, Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Completed TIMESTAMP                         
        );""")
        
        db.commit()

