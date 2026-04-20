import tkinter as tk
from tkinter import ttk, messagebox

from utils.db_connect import DbConnect
from utils.query_generator import QueryGenerator as QG
from utils.support_functions import show_default_error

import windows_find_with_year, windows_count_by_course, windows_find_student_with_id_and_list_courses, windows_find_n_students_highest_avg, windows_find_with_score

from functools import partial

class StudentManagementApp:
    def __init__(self, db_connect):

        self.db_connect = db_connect
        
        self.sub_windows = [
            [windows_find_with_year, "Tìm kiếm theo năm sinh"],
            [windows_count_by_course, "Đếm sinh viên từng môn"],
            [windows_find_student_with_id_and_list_courses, "Thông tin sinh viên"],
            [windows_find_n_students_highest_avg, "Sinh viên điểm avg lớn nhất"],
            [windows_find_with_score, "Liệt kê sinh viên dựa trên điểm"]
        ]

        windows_width = 60 * (len(self.sub_windows) + 2)
        windows_height = 400

        self.root = tk.Tk()
        self.root.title("Quản lý sinh viên")
        self.root.geometry(f"{windows_width}x{windows_height}")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        button_width = 30
        button_height = 2
        button_font = ("Arial", 8, "bold")

        row_count = 0
        self.root.rowconfigure(row_count, weight=1)
        

        for index, sub in enumerate(self.sub_windows):
            row_count += 1
            self.root.rowconfigure(row_count, weight=1)
            menu_btn = tk.Button(self.root ,text=sub[1], width=button_width, height=button_height, font=button_font, command=partial(self.run_subwindows, index))
            menu_btn.grid(row=row_count, column=1)
            
        row_count += 1  
        self.root.rowconfigure(row_count, weight=1)


    def mainloop(self):
        self.root.mainloop()

    def run_subwindows(self, index):
        self.sub_windows[index][0].loop(self.root, self.db_connect)

    
db_connect = DbConnect()
app = StudentManagementApp(db_connect)
app.mainloop()

