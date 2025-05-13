# BLL/loginBLL.py
import sqlite3
from VanPhuTung.DAL.userDAL import create_connection, setup_databaseDAL
from VanPhuTung.DTO.userDTO import UserDTO
from tkinter import messagebox
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginBLL:
    def __init__(self):
        self.connection = create_connection()
        if self.connection:
            setup_databaseDAL(self.connection)  # Truyền đối số 'connection'

    def verify_login(self, username, password):
        if not self.connection:
            return None
        hashed_password = hash_password(password)
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE username=? AND password=?
        ''', (username, hashed_password))
        user = cursor.fetchone()
        return user

    def add_user(self, user: UserDTO):
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            hashed_password = hash_password(user.password)
            cursor.execute('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', (user.username, hashed_password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Thông báo", "Lỗi: Tên đăng nhập đã tồn tại")
            return False
        except Exception as e:
            messagebox.showerror("Thông báo", f"Lỗi: đã xảy ra lỗi: {e}")
            return False