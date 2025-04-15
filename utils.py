import sys
import os

# function to access datas resource path to avoid errors when packaging
def get_resource_path(filename):
    """Get the absolute path to a resource."""
    if getattr(sys, '_MEIPASS', False):  # PyInstaller temp directory
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# function to create db in app data for persistent memory
def get_db_path():
    """Ensure the database is stored in a persistent location."""
    if getattr(sys, 'frozen', False):  
        base_path = os.path.expanduser("~\\AppData\\Local\\MyApp")  # Windows AppData
        os.makedirs(base_path, exist_ok=True)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "database.db")