import pandas as pd
from tkinter import messagebox
import re

def load_data(file_path):
    try:
        # Đọc dữ liệu từ file excel
        df_all = pd.read_excel(file_path, header=None)

        # Lấy thông tin các ô C6, C7, C8, C9, C10
        dot = df_all.iloc[5, 2]
        coSo = df_all.iloc[6, 2]
        maLopHocPhan = df_all.iloc[7, 2]
        tenMonHoc = df_all.iloc[8, 2]
        lopHoc = df_all.iloc[9, 2]

        # Đọc dữ liệu từ hàng 12 và các cột B -> W
        df = pd.read_excel(file_path, header=None, skiprows=11)
        df = df.iloc[:, 1:28]

        # Đọc tên cột từ hàng 12
        original_headers = df_all.iloc[11, 1:27].tolist()

        # Đặt tên cột dataframe
        df.columns = [
            'Mã sinh viên', 'Họ đệm', 'Tên', 'Giới tính', 'Ngày sinh',
            'date_1', 'STLD1', 'STLD2',
            'date_2', 'STLD3', 'STLD4',
            'date_3', 'STLD5', 'STLD6',
            'date_4', 'STLD7', 'STLD8',
            'date_5', 'STLD9', 'STLD10',
            'date_6', 'STLD11', 'STLD12',
            'Vắng có phép', 'Vắng không phép',
            'Tổng số tiết', 'Phần trăm vắng'
        ]
        df.columns = [col.strip() for col in df.columns]

        # Lấy các cột có ngày vắng
        date_col_indices = [5, 8, 11, 14, 17, 20]  # Zero-based indices trong DataFrame
        date_list = []
        date_columns = ['date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6']

        for i in range(len(date_col_indices)):
            col_idx = date_col_indices[i]
            col_name = original_headers[col_idx]
            # Sử dụng regex để trích xuất ngày trong định dạng dd/mm/yyyy
            match = re.search(r'(\d{2}/\d{2}/\d{4})', str(col_name))
            if match:
                date_str = match.group(1)
                date_obj = pd.to_datetime(date_str, dayfirst=True)
                date_list.append(date_obj)
            else:
                date_list.append(None)

        # Thêm các cột thông tin cố định vào DataFrame
        df['lopHoc'] = lopHoc
        df['dot'] = dot
        df['maLopHocPhan'] = str(maLopHocPhan)

        # Chuyển đổi kiểu dữ liệu cho các cột
        df['Mã sinh viên'] = df['Mã sinh viên'].astype(str)
        df['Họ đệm'] = df['Họ đệm'].astype(str)
        df['Tên'] = df['Tên'].astype(str)
        df['Giới tính'] = df['Giới tính'].astype(str)

        # Đảm bảo ngày sinh đúng định dạng
        df['Ngày sinh'] = pd.to_datetime(df['Ngày sinh'], dayfirst=True, errors='coerce')

        # Loại bỏ các giá trị bị thiếu
        df.dropna(subset=['Mã sinh viên', 'Họ đệm', 'Tên', 'Giới tính', 'Ngày sinh'], inplace=True)

        required_columns = [
            'Mã sinh viên', 'Họ đệm', 'Tên', 'Giới tính',
            'Ngày sinh', 'Vắng có phép', 'Vắng không phép',
            'Tổng số tiết', 'Phần trăm vắng', 'lopHoc', 'dot', 'maLopHocPhan'
        ]

        # Xử lý các hàng để ghi ngày vắng
        def process_row(row):
            result = []
            for idx, date_col in enumerate(date_columns):
                if row[date_col] in ['P', 'K']:
                    date = date_list[idx]
                    if pd.notnull(date):
                        date_str = date.strftime('%d/%m/%Y')
                        result.append(date_str)
            return ', '.join(result) if result else None

        df['Ngày vắng'] = df.apply(process_row, axis=1)

        # Xóa các cột không cần thiết
        df.drop(columns=date_columns + ['STLD1', 'STLD2', 'STLD3', 'STLD4', 'STLD5', 'STLD6',
                                        'STLD7', 'STLD8', 'STLD9', 'STLD10', 'STLD11', 'STLD12'], inplace=True)

        # Thêm thông tin về HocPhan vào DataFrame
        hocphan_info = {
            'maLopHocPhan': maLopHocPhan,
            'tenMonHoc': tenMonHoc,
            'coSo': coSo
        }

        return df, hocphan_info

    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy tệp Excel.")
        return pd.DataFrame(columns=required_columns), {}
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))
        return pd.DataFrame(columns=required_columns), {}
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        return pd.DataFrame(columns=required_columns), {}