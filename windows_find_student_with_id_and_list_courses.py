from bson import ObjectId

import tkinter as tk
from tkinter import ttk, messagebox

from utils.db_connect import DbConnect
from utils.query_generator import QueryGenerator as QG
from utils.support_functions import show_default_error

import re

########### SUB WINDOWS 3 ###########
def loop(root, db_connect):

    def clear_student_data():
        for field, str_var in student_variables.items():
            prefix = student_data_structure[field][0] 
            str_var.set(prefix)

        total_rows.set(f"Số môn học tham gia: 0")

    def show_student_data(student_data):
        for field, str_var in student_variables.items():
            if field in student_data:
                value = student_data[field]
                
                if field == "dob":
                    value = value.strftime("%d/%m/%Y")
                elif field == "avg_score":
                    value = f"{value:.1f}"

                prefix = student_data_structure[field][0] 
                str_var.set(prefix + f"{value}")

    def search():
        # remove existing data in windows
        clear_student_data()
        tree.delete(*tree.get_children())

        nested_lookup = QG.generate_lookup_with_pipeline("Course", "courseId", "_id", "course")
        switch_grade_logic = QG.generate_simple_switch("avg_score", "gte", {8: "Giỏi", 6: "Khá", 4: "Trung Bình", 2: "Yếu"}, "Chưa Đạt")

        query = [
            QG.generate_lookup_with_pipeline("Enrollment", "_id", "studentId", "enrolls", nested_lookup, "course"),
            QG.generate_project({
                "_id": 1,
                "name": 1,
                "avg_score": {"$avg": QG.generate_map("enrolls", "e", "score")},
                "address": 1,
                "phone": 1,
                "dob": 1,
                "enrolls": 1
                }),
            QG.generate_add_fields({"grade": switch_grade_logic})
        ]

        try:
            search_id = id_entry.get().strip()

            if not re.match("^ *[A-z\\d]{24} *$", search_id):
                raise ValueError(f"'{search_id}' không phải là mã sinh viên hợp lệ! Mã sinh viên gồm 24 ký tự [A-z0-9].")
        
            if search_id:
                query.insert(0, QG.generate_match( {"_id": ObjectId(search_id)} ))

        except Exception as e:
            messagebox.showerror("Dữ liệu sai!", e, parent=sub_window)
            return  
        
        try:
            cursor = db_connect.aggregate("Student", query)
            
            if not cursor:
                show_default_error(2, sub_window)
                return
            
            show_student_data(cursor[0])

            enrolls = cursor[0]["enrolls"]

            row_count = 0
            for db_row in enrolls:
                treeview_row = [str(row_count + 1)]

                for key in headings.keys():
                    add_data_to_column = headings[key][2]

                    if not add_data_to_column:
                        continue

                    if key in db_row:
                        value = db_row[key]

                        if key == "enrollDate":
                            value = value.strftime("%d/%m/%Y")
                        elif key == "score":
                            value = f"{value:.1f}"
                        elif key == "course":
                            value = value["name"]

                        treeview_row.append(value)
                    else:
                        treeview_row.append("")

                tree.insert("", "end", values=tuple(treeview_row))
                row_count += 1

            total_rows.set(f"Số môn học tham gia: {row_count}")

        except Exception as e:
            print(e)
            show_default_error(3, sub_window)
            return
    
    # Sub window
    sub_window = tk.Toplevel(root)
    sub_window.title("Tìm kiếm sinh viên bằng mã và liệt kê môn học")
    sub_window.geometry("500x600")
    sub_window.resizable(False, True) 

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
        "_id": ["Mã sinh viên: ", True],
        "name": ["Họ tên sinh viên: ", True],
        "address": ["Địa chỉ: ", True],
        "phone": ["Điện thoại: ", True],
        "dob": ["Ngày sinh: ", True],
        "avg_score": ["Điểm Trung Bình: ", True],
        "grade": ["Xếp loại: ", False]
    }

    tk.Label(sub_window).grid(row=2)

    windows_row_for_student = 3

    student_variables = {}
    for field, structures in student_data_structure.items():
        student_variables[field] = tk.StringVar(value=structures[0])
        tk.Label(sub_window, textvariable=student_variables[field]).grid(row=windows_row_for_student, sticky="w")
        windows_row_for_student += 1

    tk.Label(sub_window).grid(row=windows_row_for_student+1)

    total_rows = tk.StringVar(value="Số môn học tham gia: 0")
    lbl_total = tk.Label(sub_window, textvariable=total_rows).grid(row=windows_row_for_student+2, column=0, sticky="w")

    # key: [column name, column width, add db data to column]
    headings = {
        "stt": ["No", 30, False],
        "courseId": ["Mã môn học", 150, True],
        "course": ["Tên môn học", 150, True],
        "score": ["Điểm số", 70, True],
        "enrollDate": ["Ngày enroll", 100, True]
    }

    tree = ttk.Treeview(sub_window, columns=tuple(headings.keys()), show="headings")

    for key, value in headings.items():
        tree.heading(key, text=value[0])
        tree.column(key, width=value[1],stretch=tk.NO)

    tree.grid(row=windows_row_for_student+3, columnspan=2)