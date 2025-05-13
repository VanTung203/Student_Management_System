from GUI.loginGUI import LoginGUI
from DAL.userDAL import create_connection, setup_databaseDAL
import tkinter as tk

def main():
    # Tạo kết nối đến cơ sở dữ liệu và khởi tạo cấu trúc
    connection = create_connection()
    if connection:
        setup_databaseDAL(connection)
        connection.close()

    # Khởi tạo giao diện
    root = tk.Tk()
    LoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
