class Student:
    def __init__(self, _id, name, address, phone, dob):
        self._id = _id
        self.name = name
        self.address = address
        self.phone = phone
        self.dob = dob

class Course:
    def __init__(self, _id, name, description):
        self._id = _id
        self.name = name
        self.description = description
    
class Enrollment:
    def __init__(self, studentId, courseId, score, enrollDate):
        self.studentId = studentId
        self.courseId = courseId
        self.score = score
        self.enrollDate = enrollDate

   

    