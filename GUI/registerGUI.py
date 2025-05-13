import tkinter as tk
from tkinter import messagebox
from VanPhuTung.BLL.registerBLL import RegisterBLL


class RegisterGUI:
    def __init__(self, master):
        self.master = master
        self.BLL = RegisterBLL()
        self.create_widgets()

    def create_widgets(self):
        # Thiết lập cơ bản cho cửa sổ
        self.master.title("Đăng ký")
        self.master.geometry("400x500")
        self.master.configure(bg="#f9f9f9")
        self.master.resizable(False, False)

        # Khung chính chứa các thành phần giao diện
        main_frame = tk.Frame(self.master, bg="#f9f9f9", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Tiêu đề
        title_label = tk.Label(main_frame, text="Đăng ký", font=("Arial", 20, "bold"), bg="#f9f9f9", fg="#333")
        title_label.pack(pady=(10, 30))

        # Trường Tên người dùng
        username_label = tk.Label(main_frame, text="Tài khoản:", font=("Arial", 12), bg="#f9f9f9", fg="#555")
        username_label.pack(anchor="w", padx=5)
        self.username_entry = tk.Entry(main_frame, font=("Arial", 12), width=30, bd=1, relief="solid")
        self.username_entry.pack(pady=5, padx=5)

        # Trường Mật khẩu
        password_label = tk.Label(main_frame, text="Mật khẩu:", font=("Arial", 12), bg="#f9f9f9", fg="#555")
        password_label.pack(anchor="w", padx=5)
        self.password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12), width=30, bd=1, relief="solid")
        self.password_entry.pack(pady=5, padx=5)

        # Trường Xác nhận mật khẩu
        confirm_password_label = tk.Label(main_frame, text="Xác nhận mật khẩu:", font=("Arial", 12), bg="#f9f9f9",
                                          fg="#555")
        confirm_password_label.pack(anchor="w", padx=5)
        self.confirm_password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12), width=30, bd=1, relief="solid")
        self.confirm_password_entry.pack(pady=5, padx=5)

        # Nút Đăng ký và Quay lại Đăng nhập
        button_frame = tk.Frame(main_frame, bg="#f9f9f9")
        button_frame.pack(pady=(30, 10))

        register_button = tk.Button(
            button_frame,
            text="Đăng Ký",
            command=self.attempt_register,
            font=("Arial", 12),
            width=15,
            bg="#4CAF50",
            fg="white",
            bd=1,
            relief=tk.RAISED,
            activebackground="#45a049"
        )
        register_button.pack(side="left", padx=10)

        back_button = tk.Button(
            button_frame,
            text="Quay lại",
            command=self.go_back_to_login,
            font=("Arial", 12),
            width=15,
            bg="#2196F3",
            fg="white",
            bd=1,
            relief=tk.RAISED,
            activebackground="#1976D2"
        )
        back_button.pack(side="right", padx=10)

        # Hướng dẫn ở cuối
        footer_label = tk.Label(main_frame, text="Đã có tài khoản? Quay lại để đăng nhập.",
                                font=("Arial", 10), bg="#f9f9f9", fg="#777")
        footer_label.pack(pady=(30, 0))

    def attempt_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        # Kiểm tra điều kiện nhập liệu
        if not username or not password or not confirm_password:
            messagebox.showerror("Thông báo", "Lỗi: Hãy điền đầy đủ thông tin.")
            return

        if password != confirm_password:
            messagebox.showerror("Thông báo", "Lỗi: Mật khẩu và xác nhận mật khẩu không khớp.")
            return

        # Thực hiện đăng ký
        if self.BLL.register_user(username, password):
            messagebox.showinfo("Thông báo", "Đăng ký thành công!")
            self.master.destroy()
            from VanPhuTung.GUI.loginGUI import LoginGUI
            LoginGUI(tk.Tk())
        else:
            messagebox.showerror("Thông báo", "Lỗi: Tên tài khoản đã tồn tại.")

    def go_back_to_login(self):
        self.master.destroy()
        from VanPhuTung.GUI.loginGUI import LoginGUI
        LoginGUI(tk.Tk())
