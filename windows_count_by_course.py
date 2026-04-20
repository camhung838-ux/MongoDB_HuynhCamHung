from bson import ObjectId

import tkinter as tk
from tkinter import ttk, messagebox

from utils.db_connect import DbConnect
from utils.query_generator import QueryGenerator as QG
from utils.support_functions import show_default_error

import re

########### SUB WINDOWS 2 ###########
def loop(root, db_connect):
    
    # Sub window
    sub_window = tk.Toplevel(root)
    sub_window.title("Đếm số sinh viên theo môn")
    sub_window.geometry("430x400")
    sub_window.resizable(False, True) 
    
    # Show data
    tk.Label(sub_window).grid(row=0)

    total_rows = tk.StringVar(value="Tổng cộng: 0")
    lbl_total = tk.Label(sub_window, textvariable=total_rows).grid(row=1, sticky="w")

    # key: [column name, column width, add db data to column]
    headings = {
        "stt": ["No", 30, False],
        "_id": ["Mã môn học", 200, True],
        "name": ["Môn học", 100, True],
        "student_count": ["Số sinh viên", 100, True]
    }

    tree = ttk.Treeview(sub_window, columns=tuple(headings.keys()), show="headings")

    for key, value in headings.items():
        tree.heading(key, text=value[0])
        tree.column(key, width=value[1],stretch=tk.NO)

    tree.grid(row=2)

    # Query info from database
    query = [
                QG.generate_lookup("Enrollment", "_id", "courseId", "enrolls"),
                QG.generate_project({
                    "_id": 1,
                    "name": 1,
                    "student_count": { "$size": "$enrolls" }
                })
            ]

    try:
        cursor = db_connect.aggregate("Course", query)

        if not cursor:
            show_default_error(2, sub_window)
            return
        
        row_count = 0
        for db_row in cursor:

            treeview_row = [str(row_count + 1)]

            for key in headings.keys():
                add_data_to_column = headings[key][2]

                if not add_data_to_column:
                    continue

                if key in db_row:
                    treeview_row.append(db_row[key])
                else:
                    treeview_row.append("")

            tree.insert("", "end", values=tuple(treeview_row))
            row_count += 1

        total_rows.set(f"Tổng cộng: {row_count}")

    except Exception as e:
        print(e)
        show_default_error(3, sub_window)
        return