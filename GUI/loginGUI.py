import tkinter as tk
from tkinter import messagebox
from VanPhuTung.BLL.loginBLL import LoginBLL
from VanPhuTung.GUI.registerGUI import RegisterGUI
from VanPhuTung.GUI.sinhvienGUI import show_main_window

class LoginGUI:
    def __init__(self, master):
        self.master = master
        self.BLL = LoginBLL()
        self.create_widgets()

    def create_widgets(self):
        # Cài đặt cơ bản cho cửa sổ
        self.master.title("Đăng nhập")
        self.master.geometry("400x500")
        self.master.configure(bg="#f9f9f9")
        self.master.resizable(False, False)

        # Khung chứa chính
        main_frame = tk.Frame(self.master, bg="#f9f9f9", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Tiêu đề
        title_label = tk.Label(main_frame, text="Đăng Nhập", font=("Arial", 20, "bold"), bg="#f9f9f9", fg="#333")
        title_label.pack(pady=(10, 30))

        # Tên đăng nhập
        username_label = tk.Label(main_frame, text="Tài khoản:", font=("Arial", 12), bg="#f9f9f9", fg="#555")
        username_label.pack(anchor="w", padx=10)
        self.username_entry = tk.Entry(main_frame, font=("Arial", 12), width=30, bd=1, relief="solid")
        self.username_entry.pack(pady=5, padx=10)

        # Mật khẩu
        password_label = tk.Label(main_frame, text="Mật khẩu:", font=("Arial", 12), bg="#f9f9f9", fg="#555")
        password_label.pack(anchor="w", padx=10)
        self.password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12), width=30, bd=1, relief="solid")
        self.password_entry.pack(pady=5, padx=10)

        # Nút đăng nhập và đăng ký
        button_frame = tk.Frame(main_frame, bg="#f9f9f9")
        button_frame.pack(pady=30)

        login_button = tk.Button(
            button_frame,
            text="Đăng Nhập",
            command=self.attempt_login,
            font=("Arial", 12),
            width=15,
            bg="#4CAF50",
            fg="white",
            bd=1,
            relief=tk.RAISED,
            activebackground="#45a049"
        )
        login_button.pack(side="left", padx=10)

        register_button = tk.Button(
            button_frame,
            text="Đăng Ký",
            command=self.go_to_register,
            font=("Arial", 12),
            width=15,
            bg="#2196F3",
            fg="white",
            bd=1,
            relief=tk.RAISED,
            activebackground="#1976D2"
        )
        register_button.pack(side="right", padx=10)

        # # Chú thích
        # footer_label = tk.Label(main_frame, text="Quên mật khẩu? Liên hệ quản trị viên.",
        #                         font=("Arial", 10), bg="#f9f9f9", fg="#777")
        # footer_label.pack(pady=(30, 0))

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and password:
            user = self.BLL.verify_login(username, password)
            if user:
                messagebox.showinfo("Thông báo", "Đăng nhập thành công")
                self.master.destroy()
                show_main_window()
            else:
                messagebox.showerror("Thông báo", "Lỗi: Tên đăng nhập hoặc mật khẩu không đúng")
        else:
            messagebox.showerror("Thông báo", "Lỗi: Vui lòng điền đầy đủ")

    def go_to_register(self):
        self.master.destroy()
        RegisterGUI(tk.Tk())
