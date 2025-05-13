import tkinter as tk
from tkinter import Menu, filedialog, ttk, messagebox
from VanPhuTung.DTO.sinhvienDTO import SinhVienDTO
from VanPhuTung.GUI.canhbaohocvuGUI import CanhBaoHocVuGUI
from VanPhuTung.BLL.sinhvienBLL import SinhVienBLL

def show_main_window():
    root = tk.Tk()
    root.title("Quản lý sinh viên")
    root.geometry("1200x760")
    root.configure(bg="#f7f7f7")

    SinhVienGUI(root)

    root.mainloop()

class SinhVienGUI:
    def __init__(self, root):
        self.root = root
        self.BLL = SinhVienBLL()
        self.sort_order = {}
        self.create_menu()
        self.create_student_form()
        self.create_view_main()

    def create_menu(self):
        menubar = Menu(self.root, bg="#4caf50", fg="white", activebackground="#81c784")
        self.root.config(menu=menubar)

        chucnang_menu = Menu(menubar, tearoff=0, bg="#ffffff", activebackground="#c8e6c9")
        menubar.add_cascade(label="Chức năng", menu=chucnang_menu)
        chucnang_menu.add_command(label="Cảnh báo học vụ", command=self.open_canhcao)

    def create_view_main(self):
        # Frame chính
        frame = tk.Frame(self.root, bg="#f7f7f7")
        frame.pack(fill=tk.BOTH, expand=True)

        # Nút chọn file
        def select_file():
            file_path = filedialog.askopenfilename(title="Chọn file excel", filetypes=[("Excel files", "*.xls;*.xlsx")])
            if file_path:
                self.BLL.sync_excel_toDAL(file_path, self.tree, self.refreshGUI)

        # Frame cho các nút
        button_frame = tk.Frame(frame, bg="#f7f7f7")
        button_frame.grid(row=0, column=0, columnspan=5, pady=10, sticky='ew')

        button_style = {"font": ("Arial", 12, "bold"), "bg": "#4caf50", "fg": "white", "relief": tk.RAISED,
                        "cursor": "hand2", "width": 15}

        # Button select file
        button_select_file = tk.Button(button_frame, text="📂 Nhập file", **button_style, command=select_file)
        button_select_file.grid(row=0, column=0, padx=5, pady=5)

        # Button update
        button_update = tk.Button(button_frame, text="✏️Sửa", **button_style, command=self.update_student)
        button_update.grid(row=0, column=1, padx=5, pady=5)

        # Button select student
        button_select = tk.Button(button_frame, text="👁️Chi tiết", **button_style, command=self.select_student)
        button_select.grid(row=0, column=2, padx=5, pady=5)

        # Button add
        button_add = tk.Button(button_frame, text="➕ Thêm", **button_style, command=self.add_student)
        button_add.grid(row=0, column=3, padx=5, pady=5)

        # Button delete
        button_delete = tk.Button(button_frame, text="❌ Xoá", **button_style, command=self.delete_student)
        button_delete.grid(row=0, column=4, padx=5, pady=5)

        # Button export
        button_export = tk.Button(button_frame, text="📄 Xuất file", **button_style, command=self.save_to_excel)
        button_export.grid(row=0, column=5, padx=5, pady=5)

        # Button refresh
        button_refresh = tk.Button(button_frame, text="🔄 Làm mới", **button_style, command=self.refreshGUI)
        button_refresh.grid(row=0, column=6, padx=5, pady=5)

        # Search Frame
        input_frame = tk.Frame(frame, bg="#f7f7f7")
        input_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky='ew')

        tk.Label(input_frame, text="Nhập thông tin:", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.search_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        search_button = tk.Button(input_frame, text="🔍 Tìm kiếm", **button_style, command=self.search_student)
        search_button.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # Tree
        tree_frame = tk.Frame(frame, bg="#ffffff", bd=1, relief=tk.SUNKEN)
        tree_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky='nsew')

        self.tree = ttk.Treeview(tree_frame, columns=(), show='headings', height=22, style="Custom.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.columns_sinhvien = ("Mã sinh viên", "Họ đệm", "Tên", "Tổng buổi vắng", "Lớp học", "Đợt", "Tên môn học")

        self.tree.config(columns=self.columns_sinhvien)
        for col in self.columns_sinhvien:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))
            self.tree.column(col, width=120 if col in ["Mã sinh viên", "Họ đệm", "Tên", "Lớp học", "Đợt", "Tên môn học"] else 100)

        self.BLL.load_sinhvienBLL_treeview(self.tree)

        # Cấu hình trọng số của các hàng và cột để Treeview mở rộng
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(0, weight=1)

    def create_student_form(self):
        form_frame = tk.LabelFrame(self.root, text="Thông tin sinh viên", padx=10, pady=10, bg="#f7f7f7", font=("Arial", 12, "bold"))
        form_frame.pack(fill="x", padx=10, pady=10)

        fields = ["Mã sinh viên", "Họ đệm", "Tên", "Giới tính", "Ngày sinh", "Vắng có phép", "Vắng không phép", "Tổng số tiết", "Phần trăm vắng", "Lớp học", "Đợt", "Mã lớp học phần", "Ngày vắng"]

        self.entries = {}
        for idx, field in enumerate(fields):
            column = (idx % 3) * 2
            row = idx // 3
            tk.Label(form_frame, text=field, bg="#f7f7f7", font=("Arial", 10, "bold")).grid(row=row, column=column, sticky='w', pady=5, padx=10)
            entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
            entry.grid(row=row, column=column + 1, pady=5, padx=10)
            self.entries[field] = entry

    def sort_column(self, col, reverse):
        if col == "Tổng buổi vắng":
            l = [(int(self.tree.set(k, col)), k) for k in self.tree.get_children('')]
        else:
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def refreshGUI(self):
        self.BLL.load_sinhvienBLL_treeview(self.tree)

    def on_view_change(self, event):
        self.BLL.load_sinhvienBLL_treeview(self.tree)

    def open_canhcao(self):
        self.root.withdraw()
        canhcao_window = tk.Toplevel()
        CanhBaoHocVuGUI(canhcao_window)
        canhcao_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_new_window(canhcao_window))

    def on_close_new_window(self, new_window):
        new_window.destroy()
        self.root.deiconify()

    def add_student(self):
        # Lấy thông tin từ các trường nhập liệu
        ma_sinh_vien = self.entries["Mã sinh viên"].get().strip()
        ho_dem = self.entries["Họ đệm"].get().strip()
        ten = self.entries["Tên"].get().strip()
        gioi_tinh = self.entries["Giới tính"].get().strip()
        ngay_sinh = self.entries["Ngày sinh"].get().strip()
        vang_co_phep = self.entries["Vắng có phép"].get().strip()
        vang_khong_phep = self.entries["Vắng không phép"].get().strip()
        tong_so_tiet = self.entries["Tổng số tiết"].get().strip()
        phan_tram_vang = self.entries["Phần trăm vắng"].get().strip()
        lop_hoc = self.entries["Lớp học"].get().strip()
        dot = self.entries["Đợt"].get().strip()
        ma_lop_hoc_phan = self.entries["Mã lớp học phần"].get().strip()
        ngay_vang = self.entries["Ngày vắng"].get().strip()

        # Kiểm tra xem các trường bắt buộc đã được nhập hay chưa
        if not ma_sinh_vien or not ho_dem or not ten:
            messagebox.showwarning("Thông báo", "Hãy nhập đầy đủ thông tin")
            return

        sinhvien = SinhVienDTO(
            maSinhVien=ma_sinh_vien,  # Use the correct parameter name
            hoDem=ho_dem,
            ten=ten,
            gioiTinh=gioi_tinh,
            ngaySinh=ngay_sinh,
            vangCoPhep=vang_co_phep,
            vangKhongPhep=vang_khong_phep,
            tongSoTiet=tong_so_tiet,
            phanTramVang=phan_tram_vang,
            lopHoc=lop_hoc,
            dot=dot,
            maLopHocPhan=ma_lop_hoc_phan,
            ngayVang=ngay_vang
        )

        self.BLL.add_sinhvien(sinhvien)
        self.refreshGUI()

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Lỗi: Chọn sinh viên để xóa")
            return
        maSinhVien = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Thông báo", f"Bạn có chắc muốn xóa sinh viên {maSinhVien} không?")
        if confirm:
            self.BLL.delete_sinhvien(maSinhVien)
            self.refreshGUI()

    def select_student(self):
        selected_item = self.tree.selection()  # Lấy mục được chọn từ bảng
        if not selected_item:
            messagebox.showwarning("Thông báo", "Lỗi: Chọn sinh viên để hiển thị chi tiết")
            return

        # Lấy dữ liệu sinh viên từ mục được chọn
        sinhvien_data = self.tree.item(selected_item)['values']

        # Bỏ ký tự 'S' ở đầu của mã lớp học phần nếu có
        maLopHocPhan = sinhvien_data[13]
        if maLopHocPhan.startswith("S"):
            maLopHocPhan = maLopHocPhan[1:]

        # Điền thông tin vào các trường dữ liệu trong form
        self.entries["Mã sinh viên"].delete(0, tk.END)
        self.entries["Mã sinh viên"].insert(0, sinhvien_data[0])

        self.entries["Họ đệm"].delete(0, tk.END)
        self.entries["Họ đệm"].insert(0, sinhvien_data[1])

        self.entries["Tên"].delete(0, tk.END)
        self.entries["Tên"].insert(0, sinhvien_data[2])

        self.entries["Giới tính"].delete(0, tk.END)
        self.entries["Giới tính"].insert(0, sinhvien_data[7])

        self.entries["Ngày sinh"].delete(0, tk.END)
        self.entries["Ngày sinh"].insert(0, sinhvien_data[8])

        self.entries["Vắng có phép"].delete(0, tk.END)
        self.entries["Vắng có phép"].insert(0, sinhvien_data[9])

        self.entries["Vắng không phép"].delete(0, tk.END)
        self.entries["Vắng không phép"].insert(0, sinhvien_data[10])

        self.entries["Tổng số tiết"].delete(0, tk.END)
        self.entries["Tổng số tiết"].insert(0, sinhvien_data[11])

        self.entries["Phần trăm vắng"].delete(0, tk.END)
        self.entries["Phần trăm vắng"].insert(0, sinhvien_data[12])

        self.entries["Lớp học"].delete(0, tk.END)
        self.entries["Lớp học"].insert(0, sinhvien_data[4])

        self.entries["Đợt"].delete(0, tk.END)
        self.entries["Đợt"].insert(0, sinhvien_data[5])

        # Điền mã lớp học phần đã sửa vào form
        self.entries["Mã lớp học phần"].delete(0, tk.END)
        self.entries["Mã lớp học phần"].insert(0, maLopHocPhan)

        self.entries["Ngày vắng"].delete(0, tk.END)
        self.entries["Ngày vắng"].insert(0, sinhvien_data[15])

    def update_student(self):
        selected_item = self.tree.selection()  # Get the selected item
        if not selected_item:
            messagebox.showwarning("Thông báo", "Lỗi: Chọn sinh viên để sửa")
            return

        msv = self.entries["Mã sinh viên"].get()
        ho_dem = self.entries["Họ đệm"].get()
        ten = self.entries["Tên"].get()
        gioi_tinh = self.entries["Giới tính"].get()
        ngay_sinh = self.entries["Ngày sinh"].get()
        vang_co_phep = self.entries["Vắng có phép"].get()
        vang_khong_phep = self.entries["Vắng không phép"].get()
        tong_tiet = self.entries["Tổng số tiết"].get()
        phan_tram_vang = self.entries["Phần trăm vắng"].get()
        lop_hoc = self.entries["Lớp học"].get()
        dot = self.entries["Đợt"].get()
        ma_lop_hoc_phan = self.entries["Mã lớp học phần"].get()
        ngay_vang = self.entries["Ngày vắng"].get()

        sinhvien = SinhVienDTO(
            maSinhVien=msv,
            hoDem=ho_dem,
            ten=ten,
            gioiTinh=gioi_tinh,
            ngaySinh=ngay_sinh,
            vangCoPhep=int(vang_co_phep),
            vangKhongPhep=int(vang_khong_phep),
            tongSoTiet=int(tong_tiet),
            phanTramVang=float(phan_tram_vang),
            lopHoc=lop_hoc,
            dot=dot,
            maLopHocPhan=ma_lop_hoc_phan,
            ngayVang=ngay_vang
        )

        self.BLL.update_sinhvien(sinhvien)
        self.refreshGUI()


    def search_student(self):
        ma_sinh_vien = self.search_entry.get()
        self.BLL.load_sinhvienBLL_treeview(self.tree, ma_sinh_vien)


    def save_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xls;*.xlsx")])
        if file_path:
            self.BLL.save_to_excel(file_path)