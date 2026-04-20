from tkinter import messagebox

def show_default_error(option, parent):
        match option:
            case 1:
                messagebox.showerror("Dữ liệu sai!", "Dữ liệu bạn nhập không hợp lệ!", parent=parent)
            case 2:
                messagebox.showerror("Không có dữ liệu", "Dữ liệu bạn muốn tìm kiếm không tồn tại", parent=parent)
            case 3:
                messagebox.showerror("Lỗi!", "Gặp sự cố không mong muốn!", parent=parent)