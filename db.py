# db.py
import sqlite3
import os

# Get the directory of the current script and use it to construct a relative path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "rms.db")

def get_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn


