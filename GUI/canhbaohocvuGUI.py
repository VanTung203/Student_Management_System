import tkinter as tk
from tkinter import ttk, messagebox
from VanPhuTung.BLL.canhbaohocvuBLL import CanhBaoHocVuBLL
from VanPhuTung.DTO.sinhvienDTO import SinhVienDTO
import threading
import time  # Chỉ sử dụng để mô phỏng quá trình xử lý

class CanhBaoHocVuGUI:
    def __init__(self, root):
        self.root = root
        self.BLL = CanhBaoHocVuBLL()
        self.selected_student = None
        self.createGUI()

    def createGUI(self):
        self.root.title("Cảnh báo học vụ")
        self.root.geometry("1200x600")
        self.root.configure(bg="#f2f2f2")

        frame = tk.Frame(self.root, bg="#f2f2f2")
        frame.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(frame, bg="#f2f2f2")
        button_frame.grid(row=1, column=0, columnspan=5, pady=5, sticky='ew')

        # Button cảnh báo
        button_canhcao = tk.Button(
            button_frame,
            text="📧 Gửi email cảnh báo",  # Thêm biểu tượng icon
            font=("Arial", 12, "bold"),  # Chữ đậm
            bg="#4CAF50",  # Màu nền xanh lá
            fg="white",  # Màu chữ trắng
            activebackground="#45a049",  # Hiệu ứng khi nhấn nút
            activeforeground="white",  # Màu chữ khi nhấn
            bd=1,
            relief=tk.RAISED,  # Hiệu ứng nút hiện đại
            width=20,
            command=self.open_warning_form
        )
        button_canhcao.grid(row=1, column=0, padx=10, pady=5)

        # Gửi mail cho nhân viên
        button_mailToEmp = tk.Button(
            button_frame,
            text="📄 Gửi file excel riêng",  # Thêm biểu tượng icon
            font=("Arial", 12, "bold"),
            bg="#2196F3",  # Màu nền xanh dương
            fg="white",
            activebackground="#1E88E5",
            activeforeground="white",
            bd=1,
            relief=tk.RAISED,
            width=25,
            command=self.open_email_form_to_employee
        )
        button_mailToEmp.grid(row=1, column=1, padx=10, pady=5)

        # Export excel
        button_export_excel = tk.Button(
            button_frame,
            text="📂 Xuất file",  # Thêm biểu tượng icon
            font=("Arial", 12, "bold"),
            bg="#FF5722",  # Màu nền cam
            fg="white",
            activebackground="#E64A19",
            activeforeground="white",
            bd=1,
            relief=tk.RAISED,
            width=15,
            command=self.export_to_excel
        )
        button_export_excel.grid(row=1, column=2, padx=10, pady=5)

        view_frame = tk.Frame(frame, bg="#f2f2f2")
        view_frame.grid(row=1, column=1, columnspan=5, pady=10, sticky='w')

        view_label = tk.Label(view_frame, text="Trường hợp:", font=("Arial", 12), bg="#f2f2f2")
        view_label.pack(side=tk.LEFT, padx=5)

        self.current_view = tk.StringVar()
        self.current_view.set("Trên 20%")

        view_combobox = ttk.Combobox(view_frame, textvariable=self.current_view, values=["Trên 20%", "Trên 50%"],
                                     state="readonly", width=20)
        view_combobox.pack(side=tk.LEFT, padx=5)
        view_combobox.bind("<<ComboboxSelected>>", self.on_view_change)

        tree_frame = tk.Frame(frame, bg="#f2f2f2")
        tree_frame.grid(row=2, column=0, columnspan=5, pady=5, sticky='nsew')

        self.tree = ttk.Treeview(tree_frame, columns=(), show='headings', height=23)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.columns_sinhvien = ("Mã sinh viên", "Họ đệm", "Tên", "Tổng số tiết", "Phần trăm vắng (%)", "Lớp Học", "Đợt", "Tên môn học")
        self.tree.config(columns=self.columns_sinhvien)
        for col in self.columns_sinhvien:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Bind the selection event to on_student_select
        self.tree.bind("<<TreeviewSelect>>", self.on_student_select)

        # Load initial data
        self.BLL.load_canhbaoBLL_treeview(self.tree, self.current_view.get())

        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

    def on_view_change(self, event):
        self.BLL.load_canhbaoBLL_treeview(self.tree, self.current_view.get())

    def on_student_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Hãy chọn một sinh viên")
            return

        sinhvien_data = self.tree.item(selected_item)['values']
        maLopHocPhan = sinhvien_data[12]
        if maLopHocPhan.startswith("S"):
            maLopHocPhan = maLopHocPhan[1:]

        self.selected_student = SinhVienDTO(
            maSinhVien=sinhvien_data[0],
            hoDem=sinhvien_data[1],
            ten=sinhvien_data[2],
            gioiTinh=sinhvien_data[8],
            ngaySinh=sinhvien_data[9],
            vangCoPhep=sinhvien_data[10],
            vangKhongPhep=sinhvien_data[11],
            tongSoTiet=sinhvien_data[3],
            phanTramVang=sinhvien_data[4],
            lopHoc=sinhvien_data[5],
            dot=sinhvien_data[6],
            maLopHocPhan=maLopHocPhan,
            ngayVang=sinhvien_data[13]
        )

    def open_warning_form(self):
        if not self.selected_student:
            messagebox.showwarning("Thông báo", "Lỗi: Hãy chọn một sinh viên")
            return

        warning_window = tk.Toplevel(self.root)
        warning_window.title("Gửi email cảnh báo")
        warning_window.geometry("400x400")
        warning_window.configure(bg="#f2f2f2")

        email_label = tk.Label(warning_window, text="Nhập email sinh viên:", font=("Arial", 12), bg="#f2f2f2")
        email_label.pack(pady=10)

        email_entry = tk.Entry(warning_window, font=("Arial", 12), width=30)
        email_entry.pack(pady=5)

        # Thêm ô hiển thị nội dung email
        email_content_label = tk.Label(warning_window, text="Nội dung email:", font=("Arial", 12), bg="#f2f2f2")
        email_content_label.pack(pady=10)

        email_content = tk.Text(warning_window, font=("Arial", 12), height=10, wrap=tk.WORD)
        email_content.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Nội dung mẫu email
        email_body = f"""
        Xin chào sinh viên {self.selected_student.hoDem} {self.selected_student.ten},

        Thông báo: Sinh viên vắng mặt {self.selected_student.phanTramVang}% số tiết học tại lớp {self.selected_student.lopHoc}, môn học {self.selected_student.maLopHocPhan}.

        Sinh viên lưu ý đi học đầy đủ hơn.
        """
        email_content.insert("1.0", email_body)  # Thêm nội dung email vào ô Text
        # email_content.config(state="disabled")  # Vô hiệu hóa chỉnh sửa nội dung

        send_button = tk.Button(warning_window, text="Gửi", font=("Arial", 12), bg="#D3D3D3", fg="black",
                                command=lambda: self.send_warning(email_entry.get(), self.selected_student,
                                                                  warning_window))
        send_button.pack(pady=20)

    def send_warning(self, email, student, warning_window):
        if not email:
            messagebox.showerror("Thông báo", "Lỗi: Hãy nhập email sinh viên")
            return

        # Tạo cửa sổ loading
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Đang gửi email...")
        loading_window.geometry("300x100")
        loading_window.configure(bg="#f2f2f2")
        loading_window.resizable(False, False)

        label = tk.Label(loading_window, text="Đang gửi email, vui lòng chờ...", font=("Arial", 12), bg="#f2f2f2")
        label.pack(pady=10)

        progress = ttk.Progressbar(loading_window, mode='indeterminate', length=250)
        progress.pack(pady=5)
        progress.start(10)

        def send_email_task():
            try:
                time.sleep(3)  # Mô phỏng thời gian gửi email
                self.BLL.send_warning_email(email, student)  # Gửi email thực tế
                messagebox.showinfo("Thông báo", "Gửi cảnh báo sinh viên thành công")
            except Exception as e:
                messagebox.showerror("Thông báo", f"Gửi cảnh báo sinh viên không thành công. Lỗi: {str(e)}")
            finally:
                loading_window.destroy()  # Đóng cửa sổ loading
                warning_window.destroy()  # Đóng cửa sổ cảnh báo

        # Thực thi gửi email trong luồng riêng
        threading.Thread(target=send_email_task).start()

    def open_email_form_to_employee(self):
        email_window = tk.Toplevel(self.root)
        email_window.title("Gửi file excel riêng")
        email_window.geometry("400x300")
        email_window.configure(bg="#f2f2f2")

        email_label = tk.Label(email_window, text="Nhập email nhân viên:", font=("Arial", 12), bg="#f2f2f2")
        email_label.pack(pady=10)

        email_entry = tk.Entry(email_window, font=("Arial", 12), width=30)
        email_entry.pack(pady=5)

        # def send_email_to_employee():
        #     email = email_entry.get()
        #     if not email:
        #         messagebox.showerror("Lỗi", "Vui lòng nhập email nhân viên!")
        #         return
        #
        #     # Tạo cửa sổ loading
        #     loading_window = tk.Toplevel(self.root)
        #     loading_window.title("Đang gửi email...")
        #     loading_window.geometry("300x100")
        #     loading_window.configure(bg="#f2f2f2")
        #     loading_window.resizable(False, False)
        #
        #     label = tk.Label(loading_window, text="Đang gửi email, vui lòng chờ...", font=("Arial", 12), bg="#f2f2f2")
        #     label.pack(pady=10)
        #
        #     progress = ttk.Progressbar(loading_window, mode='indeterminate', length=250)
        #     progress.pack(pady=5)
        #     progress.start(10)
        #
        #     def send_email_task():
        #         try:
        #             time.sleep(3)  # Mô phỏng thời gian gửi email
        #             self.BLL.send_email_to_employee(email, email_window)  # Gửi email thực tế
        #         except Exception as e:
        #             messagebox.showerror("Lỗi", f"Gửi email không thành công. Lỗi: {str(e)}")
        #         finally:
        #             loading_window.destroy()  # Đóng cửa sổ loading
        #
        #     # Thực thi gửi email trong luồng riêng
        #     threading.Thread(target=send_email_task).start()

        send_button = tk.Button(email_window, text="Gửi", font=("Arial", 12), bg="#D3D3D3", fg="black",
                                command=lambda: self.BLL.send_email_to_employee(email_entry.get(), email_window))
        send_button.pack(pady=20)

    def export_to_excel(self):
        try:
            message = self.BLL.save_to_excel()
            messagebox.showinfo("Thành công", message)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))


