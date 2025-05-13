import sqlite3
from VanPhuTung.DAL.sinhvienDAL import create_connection
from VanPhuTung.DTO.sinhvienDTO import SinhVienDTO
from VanPhuTung.excel_data_processor import load_data
from tkinter import messagebox
import pandas as pd

class SinhVienBLL:
    def __init__(self):
        self.connection = create_connection()
        if self.connection:
            self.setup_databaseDAL()

    def setup_databaseDAL(self):
        from VanPhuTung.DAL.sinhvienDAL import setup_databaseDAL
        setup_databaseDAL(self.connection)

    def sync_excel_toDAL(self, file_path, tree, current_view_callback):
        df, hocphan_info = load_data(file_path)
        if not df.empty and hocphan_info:
            try:
                cursor = self.connection.cursor()
                # Bắt đầu giao dịch
                self.connection.execute('BEGIN')

                # Chèn hoặc cập nhật thông tin HocPhan
                cursor.execute("SELECT * FROM HocPhan WHERE maLopHocPhan = ?", (hocphan_info['maLopHocPhan'],))
                existing_hocphan = cursor.fetchone()
                if existing_hocphan:
                    # Cập nhật nếu đã tồn tại
                    cursor.execute(''' 
                        UPDATE HocPhan
                        SET tenMonHoc = ?, coSo = ?
                        WHERE maLopHocPhan = ?
                    ''', (hocphan_info['tenMonHoc'], hocphan_info['coSo'], hocphan_info['maLopHocPhan']))
                else:
                    # Chèn mới nếu chưa tồn tại
                    cursor.execute(''' 
                        INSERT INTO HocPhan (maLopHocPhan, tenMonHoc, coSo) 
                        VALUES (?, ?, ?)
                    ''', (hocphan_info['maLopHocPhan'], hocphan_info['tenMonHoc'], hocphan_info['coSo']))

                # Thêm dữ liệu vào bảng SinhVien
                for _, row in df.iterrows():
                    # Thay đổi định dạng ngày sinh từ YYYY-MM-DD thành dd/mm/yyyy
                    ngay_sinh_str = row['Ngày sinh'].strftime('%d/%m/%Y') if pd.notnull(row['Ngày sinh']) else None

                    # Tính tổng buổi vắng
                    tong_vang = int(row['Vắng có phép']) + int(row['Vắng không phép'])

                    # Thêm sinh viên mà không cập nhật
                    try:
                        cursor.execute(''' 
                            INSERT INTO SinhVien (
                                maSinhVien, hoDem, ten, gioiTinh, ngaySinh, 
                                vangCoPhep, vangKhongPhep, tongVang, tongSoTiet, phanTramVang,
                                lopHoc, dot, maLopHocPhan, ngayVang
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            row['Mã sinh viên'], row['Họ đệm'], row['Tên'],
                            row['Giới tính'], ngay_sinh_str,
                            row['Vắng có phép'], row['Vắng không phép'], tong_vang,
                            row['Tổng số tiết'], row['Phần trăm vắng'],
                            row['lopHoc'], row['dot'], row['maLopHocPhan'],
                            row['Ngày vắng']
                        ))
                    except sqlite3.IntegrityError:
                        # Nếu mã sinh viên đã tồn tại, thông báo cho người dùng
                        messagebox.showwarning("Cảnh báo",
                                               f"Mã sinh viên {row['Mã sinh viên']} đã tồn tại. Không thêm.")

                # Commit giao dịch
                self.connection.commit()
                current_view_callback()  # Tải dữ liệu mới vào Treeview
                messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")

            except sqlite3.IntegrityError as e:
                self.connection.rollback()
                messagebox.showerror("Lỗi", f"Ràng buộc khóa ngoại bị vi phạm: {e}")

            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def load_sinhvienBLL_treeview(self, tree, search_term=None):
        # Xóa tất cả các item hiện có trong treeview
        for item in tree.get_children():
            tree.delete(item)

        cursor = self.connection.cursor()

        # Kiểm tra nếu có từ khóa để tìm kiếm
        if search_term:
            cursor.execute(f"""
                SELECT sv.maSinhVien, sv.hoDem, sv.ten, sv.gioiTinh, sv.ngaySinh, 
                       sv.vangCoPhep, sv.vangKhongPhep, sv.tongVang, sv.tongSoTiet, sv.phanTramVang,
                       sv.lopHoc, sv.dot, sv.maLopHocPhan,
                       hp.tenMonHoc, hp.coSo, sv.ngayVang
                FROM SinhVien sv
                LEFT JOIN HocPhan hp ON sv.maLopHocPhan = hp.maLopHocPhan
                WHERE sv.maSinhVien LIKE ? 
                   OR sv.hoDem LIKE ? 
                   OR sv.ten LIKE ?
                   OR (sv.hoDem || ' ' || sv.ten) LIKE ?
            """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        else:
            # Truy vấn tất cả nếu không có từ khóa
            cursor.execute(f""" 
                SELECT sv.maSinhVien, sv.hoDem, sv.ten, sv.gioiTinh, sv.ngaySinh, 
                       sv.vangCoPhep, sv.vangKhongPhep, sv.tongVang, sv.tongSoTiet, sv.phanTramVang,
                       sv.lopHoc, sv.dot, sv.maLopHocPhan,
                       hp.tenMonHoc, hp.coSo, sv.ngayVang
                FROM SinhVien sv
                LEFT JOIN HocPhan hp ON sv.maLopHocPhan = hp.maLopHocPhan
            """)

        rows = cursor.fetchall()

        # Chèn thông tin vào treeview
        for row in rows:
            (
                maSinhVien, hoDem, ten, gioiTinh, ngaySinh,
                vangCoPhep, vangKhongPhep, tongVang, tongSoTiet, phanTramVang,
                lopHoc, dot, maLopHocPhan,
                tenMonHoc, coSo, ngayVang
            ) = row
            maLopHocPhan = f"S{str(maLopHocPhan)}"

            # Kiểm tra nếu ngaySinh không phải là None
            if ngaySinh:
                try:
                    ngaySinh_dt = pd.to_datetime(ngaySinh, format='%d/%m/%Y')
                    ngaySinh_display = ngaySinh_dt.strftime('%d/%m/%Y')
                except ValueError:
                    ngaySinh_display = ngaySinh
            else:
                ngaySinh_display = ''

            tree.insert('', 'end', values=(
                maSinhVien, hoDem, ten, tongVang, lopHoc, dot, tenMonHoc, gioiTinh, ngaySinh_display,
                vangCoPhep, vangKhongPhep, tongSoTiet, phanTramVang,
                maLopHocPhan, coSo, ngayVang
            ))

    def add_sinhvien(self, sinhvien: SinhVienDTO):
        try:
            cursor = self.connection.cursor()
            tongVang = int(sinhvien.vangCoPhep) + int(sinhvien.vangKhongPhep)
            # phanTramVang = float((int(tongVang) / int(sinhvien.tongSoTiet)) * 100)
            cursor.execute('''
                INSERT INTO SinhVien (
                    maSinhVien, hoDem, ten, gioiTinh, ngaySinh, 
                    vangCoPhep, vangKhongPhep, tongVang, tongSoTiet, phanTramVang,
                    lopHoc, dot, maLopHocPhan, ngayVang
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sinhvien.maSinhVien, sinhvien.hoDem, sinhvien.ten,
                sinhvien.gioiTinh, sinhvien.ngaySinh,
                sinhvien.vangCoPhep, sinhvien.vangKhongPhep,
                tongVang ,sinhvien.tongSoTiet, sinhvien.phanTramVang,
                sinhvien.lopHoc, sinhvien.dot, sinhvien.maLopHocPhan,
                sinhvien.ngayVang
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã sinh viên đã tồn tại!")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def update_sinhvien(self, sinhvien: SinhVienDTO):
        try:
            cursor = self.connection.cursor()
            tongVang = int(sinhvien.vangCoPhep) + int(sinhvien.vangKhongPhep)
            cursor.execute('''
                UPDATE SinhVien
                SET hoDem = ?, ten = ?, gioiTinh = ?, ngaySinh = ?,
                    vangCoPhep = ?, vangKhongPhep = ?, tongVang = ?, tongSoTiet = ?,
                    phanTramVang = ?, lopHoc = ?, dot = ?, maLopHocPhan = ?
                WHERE maSinhVien = ?
            ''', (
                sinhvien.hoDem, sinhvien.ten, sinhvien.gioiTinh, sinhvien.ngaySinh,
                sinhvien.vangCoPhep, sinhvien.vangKhongPhep, tongVang, sinhvien.tongSoTiet,
                sinhvien.phanTramVang, sinhvien.lopHoc, sinhvien.dot,
                sinhvien.maLopHocPhan, sinhvien.maSinhVien
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def delete_sinhvien(self, maSinhVien: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM SinhVien WHERE maSinhVien = ?', (maSinhVien,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def save_to_excel(self, file_path: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" 
                SELECT sv.maSinhVien, sv.hoDem, sv.ten, sv.gioiTinh, sv.ngaySinh, 
                       sv.vangCoPhep, sv.vangKhongPhep, sv.tongVang, sv.tongSoTiet, sv.phanTramVang,
                       sv.lopHoc, sv.dot, sv.maLopHocPhan,
                       hp.tenMonHoc, hp.coSo
                FROM SinhVien sv
                LEFT JOIN HocPhan hp ON sv.maLopHocPhan = hp.maLopHocPhan
            """)
            rows = cursor.fetchall()
            columns = [
                "Mã sinh viên", "Họ đệm", "Tên", "Giới tính",
                "Ngày sinh", "Vắng có phép", "Vắng không phép",
                "Tổng Vắng", "Tổng số tiết", "Phần trăm vắng",
                "Lớp Học", "Đợt", "Mã Lớp Học Phần", "Tên môn học", "Cơ sở"
            ]

            df = pd.DataFrame(rows, columns=columns)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", "Lưu dữ liệu vào Excel thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
