import sqlite3
from tkinter import messagebox
from pathlib import Path

# Đường dẫn đến cơ sở dữ liệu
DAL_PATH = Path(__file__).parent.parent / 'student.db'

def create_connection():
    """Tạo kết nối đến cơ sở dữ liệu SQLite và kích hoạt khóa ngoại."""
    try:
        connection = sqlite3.connect(DAL_PATH)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')    # Kích hoạt khóa ngoại
        cursor.execute('PRAGMA foreign_keys')
        return connection
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", str(e))
        return None

def setup_databaseDAL(connection):
    """Khởi tạo cơ sở dữ liệu với các bảng nếu chưa tồn tại."""
    cursor = connection.cursor()
    #Tạo bảng HocPhan nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HocPhan (
            maLopHocPhan TEXT PRIMARY KEY,
            tenMonHoc TEXT,
            coSo TEXT	
        )
    ''')
    # Tạo bảng SinhVien nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SinhVien (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            maSinhVien TEXT NOT NULL,   
            hoDem TEXT NOT NULL,  
            ten TEXT NOT NULL,
            gioiTinh TEXT,
            ngaySinh DATE,
            lopHoc TEXT,
            dot TEXT,
            vangCoPhep INT,
            vangKhongPhep INT,
            tongSoTiet INT,
            phanTramVang INT,
            maLopHocPhan TEXT,
            tongVang INT,
            ngayVang TEXT,
            FOREIGN KEY (maLopHocPhan) REFERENCES HocPhan (maLopHocPhan) ON DELETE CASCADE
        )
    ''')
    connection.commit()
