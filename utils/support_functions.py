from tkinter import messagebox
from bson import ObjectId
from datetime import date, datetime
from textwrap import wrap

def show_default_error(option, parent):
        match option:
            case 1:
                messagebox.showerror("Dữ liệu sai!", "Dữ liệu bạn nhập không hợp lệ!", parent=parent)
            case 2:
                messagebox.showerror("Không có dữ liệu", "Dữ liệu bạn muốn tìm kiếm không tồn tại", parent=parent)
            case 3:
                messagebox.showerror("Lỗi!", "Gặp sự cố không mong muốn!", parent=parent)

def add_line_break_every_n_chars(text: str, n_chars: int):

    if isinstance(text, str):
        text_arr = wrap(text, n_chars)
        return "\n".join(text_arr), len(text_arr)
    else:
        return text, 0
    
def check_is_valid_float(number_str):
    try:
        float(number_str)
    except:
        return False
    
    return True

def check_is_valid_date(input_date):
    
    return isinstance(input_date, (datetime, date))


def generate_min_max_year_query(field, gte, lte):
    and_ = []
     
    if gte:
        expr = {
            "$expr": {
            "$gte": [{ "$year": f"${field}" }, float(gte)],
            },
        }
            
        and_.append(expr)
     
    if lte:
        expr = {
            "$expr": {
            "$lte": [{ "$year": f"${field}" }, float(lte)],
            },
        }
            
        and_.append(expr)

    if and_:
        return {
            "$and": and_
        }
    else:
        return {}
    
def generate_query_count_by_course():
    
    return [
        {
            "$lookup": {
            "from": "Enrollment",
            "localField": "_id",
            "foreignField": "courseId",
            "as": "enrolls",
            },
        },
        {
            "$project": {
            "_id": 1,
            "name": 1,
            "student_count": { "$size": "$enrolls" },
            },
        },
    ]

def generate_query_n_students_highest_avg(n_students):

    query = [
        {
            "$lookup": {
            "from": "Enrollment",
            "localField": "_id",
            "foreignField": "studentId",
            "as": "enrolls",
            },
        },
        {
            "$project": {
            "_id": 1,
            "name": 1,
            "address": 1,
            "phone": 1,
            "dob": 1,
            "avg_score": {
                "$avg": "$enrolls.score",
            },
            },
        },
        {
            "$sort": {
            "avg_score": -1,
            },
        }
    ]

    if n_students:
        query.append(
             {
                "$limit": int(n_students),
            }
        )

    return query

def generate_query_find_with_score(field, gte, lte):
    query = [
        {
            "$lookup": {
            "from": "Course",
            "localField": "courseId",
            "foreignField": "_id",
            "as": "course",
            },
        },
        {
            "$lookup": {
            "from": "Student",
            "localField": "studentId",
            "foreignField": "_id",
            "as": "student",
            },
        },
        {
            "$unwind": "$course",
        },
        {
            "$unwind": "$student",
        },
        {
            "$project": {
            "_id": 0,
            "student_id": "$studentId",
            "student_name": "$student.name",
            "address": "$student.address",
            "course_name": "$course.name",
            "score": 1,
            "enrollDate": 1,
            },
        },
    ]

    match_ = {}
     
    if gte:
        match_["$gte"] = float(gte)
     
    if lte:
        match_["$lte"] = float(lte)

    if match_:
        query.insert(0,
            {
                "$match": {
                    "score": match_,
                },
            }
        )

    return query

def generate_query_find_with_student_id_and_list_courses_join(search_id):
    query = [
        {
            "$match": {
                "_id": ObjectId(search_id),
            },
        },
        {
            "$lookup": {
                "from": "Enrollment",
                "let": { "master_student_id": "$_id" },
                "pipeline": [
                    { "$match": { "$expr": { "$eq": ["$studentId", "$$master_student_id"] } } },
                    {
                    "$lookup": {
                        "from": "Course",
                        "let": { "foreign_course_id": "$courseId" },
                        "pipeline": [
                        {
                            "$match": {
                            "$expr": { "$eq": ["$_id", "$$foreign_course_id"] },
                            },
                        },
                        ],
                        "as": "course",
                    },
                    },
                    { "$unwind": "$course" },
                    {
                        "$addFields": {
                            "courseName": "$course.name",
                        },
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "courseId": 1,
                            "courseName": 1,
                            "score": 1,
                            "enrollDate": 1,
                        },
                    }
                ],
                "as": "enrolls",
            },
        },
        {
            "$project": {
            "_id": 1,
            "name": 1,
            "avg_score": {
                "$avg": { "$map": { "input": "$enrolls", "as": "e", "in": "$$e.score" } },
            },
            "address": 1,
            "phone": 1,
            "dob": 1,
            "enrolls": 1,
            },
        },
        {
            "$addFields": {
                "grade": {
                    "$switch": {
                    "branches": [
                        { "case": { "$gte": ["$avg_score", 8] }, "then": "Giỏi" },
                        { "case": { "$gte": ["$avg_score", 6] }, "then": "Khá" },
                        { "case": { "$gte": ["$avg_score", 4] }, "then": "Trung Bình" },
                        { "case": { "$gte": ["$avg_score", 2] }, "then": "Yếu" },
                    ],
                    "default": "Chưa Đạt",
                    },
                },
            },
        },
    ]
    
    return query
