from VanPhuTung.DAL.sinhvienDAL import create_connection
from tkinter import messagebox
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from tkinter import filedialog

class CanhBaoHocVuBLL:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.username = '' # username gmail
        self.password = '' # password (key)

        self.connection = create_connection()
        if self.connection:
            self.setup_databaseDAL()

    def setup_databaseDAL(self):
        from VanPhuTung.DAL.sinhvienDAL import setup_databaseDAL
        setup_databaseDAL(self.connection)


    def load_canhbaoBLL_treeview(self, tree, table):
        for item in tree.get_children():
            tree.delete(item)

        cursor = self.connection.cursor()

        if table == 'Trên 20%':
            cursor.execute("""
                SELECT sv.maSinhVien, sv.hoDem, sv.ten, sv.tongSoTiet, sv.phanTramVang, 
                       sv.lopHoc, sv.dot, hp.tenMonHoc, sv.gioiTinh, sv.ngaySinh, 
                       sv.vangCoPhep, sv.vangKhongPhep, sv.maLopHocPhan, sv.ngayVang, hp.coSo
                FROM SinhVien sv
                LEFT JOIN HocPhan hp ON sv.maLopHocPhan = hp.maLopHocPhan
                WHERE CAST(sv.phanTramVang AS DECIMAL) >= 20 AND CAST(sv.phanTramVang AS DECIMAL) < 50 
            """)
            rows = cursor.fetchall()
            for row in rows:
                (
                    maSinhVien, hoDem, ten,tongSoTiet, phanTramVang,
                    lopHoc, dot, tenMonHoc, gioiTinh, ngaySinh,
                    vangCoPhep, vangKhongPhep, maLopHocPhan, ngayVang, coSo
                ) = row
                maLopHocPhan = f"S{str(maLopHocPhan)}"

                if ngaySinh:
                    try:
                        ngaySinh_dt = pd.to_datetime(ngaySinh, format='%Y-%m-%d', errors='coerce')
                        if pd.notnull(ngaySinh_dt):
                            ngaySinh_display = ngaySinh_dt.strftime('%d/%m/%Y')
                        else:
                            ngaySinh_display = ngaySinh  # Nếu định dạng không đúng, hiển thị nguyên dạng
                    except Exception:
                        ngaySinh_display = ngaySinh  # Hiển thị nguyên dạng nếu có lỗi
                else:
                    ngaySinh_display = ''

                tree.insert('', 'end', values=(
                    maSinhVien, hoDem, ten, tongSoTiet, phanTramVang,
                    lopHoc, dot, tenMonHoc, gioiTinh, ngaySinh_display,
                    vangCoPhep, vangKhongPhep, maLopHocPhan, ngayVang, coSo
                ))

        elif table == 'Trên 50%':
            cursor.execute("""
                SELECT sv.maSinhVien, sv.hoDem, sv.ten, sv.tongSoTiet, sv.phanTramVang, 
                       sv.lopHoc, sv.dot, hp.tenMonHoc, sv.gioiTinh, sv.ngaySinh, 
                       sv.vangCoPhep, sv.vangKhongPhep, sv.maLopHocPhan, sv.ngayVang,  hp.coSo
                FROM SinhVien sv
                LEFT JOIN HocPhan hp ON sv.maLopHocPhan = hp.maLopHocPhan
                WHERE CAST(sv.phanTramVang AS DECIMAL) >= 50 
            """)
            rows = cursor.fetchall()
            for row in rows:
                (
                    maSinhVien, hoDem, ten, tongSoTiet, phanTramVang,
                    lopHoc, dot, tenMonHoc, gioiTinh, ngaySinh,
                    vangCoPhep, vangKhongPhep, maLopHocPhan, ngayVang, coSo
                ) = row
                maLopHocPhan = f"S{str(maLopHocPhan)}"

                if ngaySinh:
                    try:
                        ngaySinh_dt = pd.to_datetime(ngaySinh, format='%Y-%m-%d', errors='coerce')
                        if pd.notnull(ngaySinh_dt):
                            ngaySinh_display = ngaySinh_dt.strftime('%d/%m/%Y')
                        else:
                            ngaySinh_display = ngaySinh  # Nếu định dạng không đúng, hiển thị nguyên dạng
                    except Exception:
                        ngaySinh_display = ngaySinh  # Hiển thị nguyên dạng nếu có lỗi
                else:
                    ngaySinh_display = ''

                tree.insert('', 'end', values=(
                    maSinhVien, hoDem, ten, tongSoTiet, phanTramVang,
                    lopHoc, dot, tenMonHoc, gioiTinh, ngaySinh_display,
                    vangCoPhep, vangKhongPhep, maLopHocPhan, ngayVang, coSo
                ))
        else:
            messagebox.showerror("Lỗi", f"Bảng không hợp lệ: {table}")

    def send_warning_email(self, email, student):
        subject = "Cảnh báo học vụ"
        body = f"""
        Xin chào sinh viên {student.hoDem} {student.ten},

        Thông báo: Sinh viên vắng mặt {student.phanTramVang}% số tiết học tại lớp {student.lopHoc}, môn học {student.maLopHocPhan}.
        
        Sinh viên lưu ý đi học đầy đủ hơn.
        """

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            print(f"Email đã được gửi tới {email}")
        except Exception as e:
            raise Exception(f"Không thể gửi email: {str(e)}")

    def generate_excel_file(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM SinhVien
            Where CAST(phanTramVang AS DECIMAL) >= 20
        """)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(rows, columns=columns)
        file_path = "database_sinhvien.xlsx"
        df.to_excel(file_path, index=False)

        return file_path

    def send_email_to_employee(self, email, window):
        if not email:
            messagebox.showerror("Lỗi", "Vui lòng nhập email nhân viên!")
            return

        try:
            # Tạo file Excel từ dữ liệu
            file_path = self.generate_excel_file()

            # Gửi email
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = email
            msg['Subject'] = "Tổng hợp các lớp vắng"

            body = "Tổng hợp thông tin sv các lớp vắng nhiều thành một file excel riêng"
            msg.attach(MIMEText(body, 'plain'))

            # Đính kèm file Excel
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
            msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, email, text)
            server.quit()

            messagebox.showinfo("Thông báo", "Đã gửi email thành công!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Gửi email không thành công. Lỗi: {str(e)}")

    def save_to_excel(self):
        try:
            # Mở hộp thoại để người dùng chọn đường dẫn lưu file
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
            if not file_path:  # Nếu người dùng hủy hộp thoại
                return "Không có tệp được chọn"

            cursor = self.connection.cursor()
            cursor.execute("""
                 SELECT * FROM SinhVien
                 Where CAST(phanTramVang AS DECIMAL) >= 20
            """)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Lấy tên cột từ mô tả con trỏ

            df = pd.DataFrame(rows, columns=columns)
            df.to_excel(file_path, index=False)

            return "Lưu thành công"
        except Exception as e:
            raise Exception(f"Bị lỗi: {e}")