import tkinter as tk
from tkinter import ttk, messagebox, font, scrolledtext

from utils.support_functions import *

import re

########### SUB WINDOWS 3 ###########
def loop(root, db_connect):

    def clear_data():
        # remove existing data in windows
        for txt in student_data_txts.values():
            txt.config(state='normal')
            txt.delete("1.0", "end")
            txt.config(state='disabled')

        style.configure("Treeview", rowheight=20)
        total_rows.set(f"Số môn học tham gia: 0")
        tree.delete(*tree.get_children())

    def show_student_data(student_data):
        for field, txt in student_data_txts.items():
            if field in student_data:
                value = student_data[field]

                if not isinstance(txt, scrolledtext.ScrolledText) and not isinstance(value, ObjectId):

                    if value or value == 0:
                        if field == "dob" and check_is_valid_date(value):
                            value = value.strftime("%d/%m/%Y")

                        elif field == "avg_score" and check_is_valid_float(value):
                            value = f"{value:.1f}"

                        elif isinstance(value, str):
                            value = re.sub("[\\r\\n]+", "", value)

                            max_length_each_line = 40
                            n_dot = 3

                            value_length = len(value)
                            if value_length > max_length_each_line:
                                value = value[0: max_length_each_line] + "..." * n_dot
                        else:
                            value = "NaN"
                    else:
                        value = ""

  
                txt.config(state='normal')
                txt.insert("1.0", str(value))
                txt.config(state='disabled')
    
    def show_enrolls_data(enrolls):
        row_count = 0
        max_line_count = 1

        for db_row in enrolls:
            treeview_row = [str(row_count + 1)]
            
            for key in headings.keys():
                add_data_to_column = headings[key][2]

                if not add_data_to_column:
                    continue
                
                value = ""

                if key in db_row:
                    value = db_row[key]

                    if value or value == 0:
                        if key == "enrollDate":
                            value = value.strftime("%d/%m/%Y") if check_is_valid_date(value) else "NaN"

                        elif key == "score":
                            value = f"{value:.1f}" if check_is_valid_float(value) else "NaN"
                        else:
                            value, line_count = add_line_break_every_n_chars(value, int(headings[key][1] / 10))

                            if line_count > max_line_count:
                                max_line_count = line_count
                    else:
                        value = ""


                treeview_row.append(value)
            

            tree.insert("", "end", values=tuple(treeview_row))
            row_count += 1

        style.configure("Treeview", rowheight=max_line_count * 20)
        total_rows.set(f"Số môn học tham gia: {row_count}")

    def search():
        clear_data()

        query = []

        try:
            search_id = id_entry.get().strip()

            if not re.match("^ *[A-z\\d]{24} *$", search_id):
                raise ValueError(f"'{search_id}' không phải là mã sinh viên hợp lệ! Mã sinh viên gồm 24 ký tự [A-z0-9].")
        
            if search_id:
                query = generate_query_find_with_student_id_and_list_courses_join(search_id)

        except Exception as e:
            messagebox.showerror("Dữ liệu sai!", e, parent=sub_window)
            return  
        
        try:
            cursor = db_connect.aggregate("Student", query)
            
            if not cursor:
                show_default_error(2, sub_window)
                return
            
            show_student_data(cursor[0])

            show_enrolls_data(cursor[0]["enrolls"])

        except Exception as e:
            print(e)
            show_default_error(3, sub_window)
            return
    
    # Sub window
    width, height = 500, 720

    sub_window = tk.Toplevel(root)
    sub_window.title("Tìm kiếm sinh viên bằng mã và liệt kê môn học")
    sub_window.geometry(f"{width}x{height}")
    sub_window.resizable(False, True) 
    sub_window.grab_set()
    
    sub_window.columnconfigure(0, weight=1)
    sub_window.columnconfigure(1, weight=1)

    # Search control
    tk.Label(sub_window).grid(row=0)

    search_frame = tk.Frame(sub_window)
    search_frame.grid(row=1, column=0, sticky="w")
    
    id_lbl = tk.Label(search_frame, text="Mã sinh viên: ")
    id_entry = tk.Entry(search_frame, width=25)

    id_lbl.grid(row=0,column=0)
    id_entry.grid(row=0,column=1)
    
    btn_search = tk.Button(sub_window, text="Tìm kiếm", command=search)
    btn_search.grid(row=1, column=1, sticky="e")

    # Show student data
    student_data_structure = {
        "_id": ["Mã sinh viên:", True],
        "name": ["Họ tên:", True],
        "phone": ["Điện thoại:", True],
        "dob": ["Ngày sinh:", True],
        "avg_score": ["Điểm AVG:", True],
        "grade": ["Xếp loại:", False],
        "address": ["Địa chỉ:", True],
    }

    # max_student_label_length = max(len(v[0]) for v in student_data_structure.values())

    tk.Label(sub_window).grid(row=2)

    windows_row_for_student = 3
    txt_width = 50
    student_data_txts = {}
    for field, structures in student_data_structure.items():
        frame = tk.Frame(sub_window)
        frame.grid(row=windows_row_for_student, columnspan=2, sticky="w")

        tk.Label(frame, width=10, anchor="w", text=structures[0]).grid(row=0, column=0, sticky="nw")

        txt = None

        if field == "address":
            txt = scrolledtext.ScrolledText(frame, width=txt_width - 10, height=1)
        else:
            txt = tk.Text(frame, height=1, width=txt_width, borderwidth=0, highlightthickness=0, bg=root.cget("bg"), font=font.nametofont("TkDefaultFont"))
        
        txt.configure(state="disabled", cursor="arrow")
        txt.grid(row=0, column=1)

        student_data_txts[field] = txt
        windows_row_for_student += 1

    tk.Label(sub_window).grid(row=windows_row_for_student+1)

    total_rows = tk.StringVar(value="Số môn học tham gia: 0")
    lbl_total = tk.Label(sub_window, textvariable=total_rows).grid(row=windows_row_for_student+2, column=0, sticky="w")

    # key: [column name, column width, add db data to column]
    headings = {
        "stt": ["No", 30, False],
        "courseId": ["Mã môn học", 150, True],
        "courseName": ["Tên môn học", 150, True],
        "score": ["Điểm số", 70, True],
        "enrollDate": ["Ngày enroll", 100, True]
    }

    tree_view_frame = tk.Frame(sub_window, width=width, height=height - 300)
    tree_view_frame.pack_propagate(False)
    tree_view_frame.grid(row=windows_row_for_student+3, columnspan=2)

    style = ttk.Style()
    style.configure("Treeview", rowheight=20)

    tree = ttk.Treeview(tree_view_frame, columns=tuple(headings.keys()), show="headings")

    for key, value in headings.items():
        tree.heading(key, text=value[0])
        tree.column(key, width=value[1],stretch=tk.NO)

    tree.pack(fill="both", expand=True)
    tree.bind("<Control-Key-c>", lambda x: copy_treeview_selection(tree, x))