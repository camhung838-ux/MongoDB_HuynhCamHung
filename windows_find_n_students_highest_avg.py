import tkinter as tk
from tkinter import ttk, messagebox

from utils.support_functions import *

import re

########### SUB WINDOWS 4 ###########
def loop(root, db_connect):
    def clear_data():
         # remove existing table data in windows
        style.configure("Treeview", rowheight=20)
        total_rows.set(f"Tổng cộng: 0")
        tree.delete(*tree.get_children())

    def show_result(cursor):
        row_count = 0
        max_line_count = 1

        for db_row in cursor:
            
            treeview_row = [str(row_count + 1)]

            for key in headings.keys():
                add_data_to_column = headings[key][2]

                if not add_data_to_column:
                    continue
                
                value = ""

                if key in db_row:
                    value = db_row[key]

                    if value or value == 0:
                        if key == "dob":
                            value = value.strftime("%d/%m/%Y") if check_is_valid_date(value) else "NaN"
                            
                        elif key == "avg_score":
                            value = f"{value:.1f}" if check_is_valid_float(value) else "NaN"
                            
                        elif isinstance(value, str):
                            value, line_count = add_line_break_every_n_chars(value, int(headings[key][1] / 10))

                            if line_count > max_line_count:
                                max_line_count = line_count
                    else:
                        value = ""


                treeview_row.append(value)
                

            tree.insert("", "end", values=tuple(treeview_row))
            row_count += 1


        style.configure("Treeview", rowheight=max_line_count * 20)
        total_rows.set(f"Tổng cộng: {row_count}")

    def search():
        clear_data()

        query = []

        try:
            # generate query from n_students
            n_students = n_students_entry.get().strip()

            if not re.match("^[\\d\\s]*$", n_students):
                raise ValueError(f"'{n_students}' không phải là số hợp lệ!")
        
            query = generate_query_n_students_highest_avg(n_students)

        except Exception as e:
            total_rows.set(f"Tổng cộng: 0")
            messagebox.showerror("Dữ liệu sai!", e, parent=sub_window)
            return

        try:
            cursor = db_connect.aggregate("Student", query)
            
            if not cursor:
                show_default_error(2, sub_window)
                return
            
            show_result(cursor)
            
        except Exception as e:
            print(e)
            show_default_error(3, sub_window)
            return
    
    # Sub window
    width, height = 850, 600

    sub_window = tk.Toplevel(root)
    sub_window.title("Tìm kiếm n sinh viên có điểm trung bình cao nhất")
    sub_window.geometry(f"{width}x{height}")
    sub_window.resizable(False, True) 
    sub_window.grab_set()
    
    sub_window.columnconfigure(0, weight=1)
    sub_window.columnconfigure(1, weight=1)

    # Search control
    tk.Label(sub_window).grid(row=0)

    search_frame = tk.Frame(sub_window)
    search_frame.grid(row=1, column=0, sticky="w")
    
    n_students_lbl = tk.Label(search_frame, text="Số sinh viên: ")
    n_students_entry = tk.Entry(search_frame, width=20)

    n_students_lbl.grid(row=0,column=0)
    n_students_entry.grid(row=0,column=1)
    
    btn_search = tk.Button(sub_window, text="Tìm kiếm", command=search)
    btn_search.grid(row=1, column=1, sticky="e")

    tk.Label(sub_window).grid(row=2)

    # Widgets for showing data
    total_rows = tk.StringVar(value="Tổng cộng: 0")
    lbl_total = tk.Label(sub_window, textvariable=total_rows).grid(row=3, column=0, sticky="w")

    # key: [column name, column width, add db data to column]
    headings = {
        "stt": ["No", 30, False],
        "_id": ["Mã sinh viên", 180, True],
        "name": ["Họ tên", 170, True],
        "avg_score": ["Điểm AVG", 70, True],
        "address": ["Địa chỉ", 200, True],
        "phone": ["SĐT", 100, True],
        "dob": ["Ngày sinh", 100, True]
    }

    tree_view_frame = tk.Frame(sub_window, width=width, height=height - 200)
    tree_view_frame.pack_propagate(False)
    tree_view_frame.grid(row=4, columnspan=2)

    style = ttk.Style()
    style.configure("Treeview", rowheight=20)

    tree = ttk.Treeview(tree_view_frame, columns=tuple(headings.keys()), show="headings")

    for key, value in headings.items():
        tree.heading(key, text=value[0])
        tree.column(key, width=value[1],stretch=tk.NO)

    tree.pack(fill="both", expand=True)

    tree.bind("<Control-Key-c>", lambda x: copy_treeview_selection(tree, x))
