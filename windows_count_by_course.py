import tkinter as tk
from tkinter import ttk, messagebox

from utils.support_functions import *

########### SUB WINDOWS 2 ###########
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
                        if isinstance(value, str):
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

    
    def refresh():
        clear_data()

        # Query info from database
        query = generate_query_count_by_course()

        try:
            cursor = db_connect.aggregate("Course", query)

            if not cursor:
                show_default_error(2, sub_window)
                return
            
            show_result(cursor)

        except Exception as e:
            print(e)
            show_default_error(3, sub_window)
            return

    # Sub window
    width, height = 430, 600

    sub_window = tk.Toplevel(root)
    sub_window.title("Đếm số sinh viên theo môn")
    sub_window.geometry(f"{width}x{height}")
    sub_window.resizable(False, True) 
    sub_window.grab_set()
    
    
    tk.Label(sub_window).grid(row=0)

    btn_refresh = tk.Button(sub_window, text="Refresh", command=refresh)
    btn_refresh.grid(row=1, column=1, sticky="e")

    tk.Label(sub_window).grid(row=2)
    # Widgets for showing data
    total_rows = tk.StringVar(value="Tổng cộng: 0")
    lbl_total = tk.Label(sub_window, textvariable=total_rows).grid(row=3, sticky="w")

    # key: [column name, column width, add db data to column]
    headings = {
        "stt": ["No", 30, False],
        "_id": ["Mã môn học", 200, True],
        "name": ["Môn học", 100, True],
        "student_count": ["Số sinh viên", 100, True]
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

    refresh()

    tree.bind("<Control-Key-c>", lambda x: copy_treeview_selection(tree, x))

    