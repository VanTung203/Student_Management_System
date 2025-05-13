import sqlite3
from tkinter import messagebox
from pathlib import Path

# Đường dẫn đến tệp cơ sở dữ liệu
DAL_PATH = Path(__file__).parent.parent / 'user.db'

def create_connection():
    """Tạo và trả về kết nối đến cơ sở dữ liệu SQLite."""
    try:
        connection = sqlite3.connect(DAL_PATH)
        return connection
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", str(e))
        return None

def setup_databaseDAL(connection):
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
    ''')
    connection.commit()
