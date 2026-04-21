use("DT2507L-NK_huynhcamhung_StudentDB");

//Câu 1: Nhập vào 2 năm sinh là 2 số nguyên min và max.
//Liệt kê các sinh viên có năm sinh nằm trong khoảng từ min đến max (4d)

/*
db.Student.find({
  $and: [
    {
      $expr: {
        $gte: [{ $year: "$dob" }, 2002],
      },
    },
    {
      $expr: {
        $lte: [{ $year: "$dob" }, 2003],
      },
    },
  ],
});
*/

// Câu 2: Đếm số sinh viên tham gia từng môn học (2d)
/*
db.Course.aggregate([
  {
    $lookup: {
      from: "Enrollment",
      localField: "_id",
      foreignField: "courseId",
      as: "enrolls",
    },
  },
  {
    $project: {
      _id: 1,
      name: 1,
      student_count: { $size: "$enrolls" },
    },
  },
]);
*/

// Câu 3: Nhập vào 1 mã sinh viên. Liệt kê các thông tin:
// a. Mã môn học, tên môn học, điểm số, ngày tham gia mà sinh viên đó tham gia (2d)
// b. Điểm trung bình (2d)
// c. Xếp loại sinh viên (2d)

let _id = "69e3d4f2f275f6f08af4002d";

db.Student.aggregate([
  {
    $match: {
      _id: ObjectId(_id),
    },
  },
  {
    $lookup: {
      from: "Enrollment",
      let: { master_student_id: "$_id" },
      pipeline: [
        { $match: { $expr: { $eq: ["$studentId", "$$master_student_id"] } } },
        {
          $lookup: {
            from: "Course",
            let: { foreign_course_id: "$courseId" },
            pipeline: [
              {
                $match: {
                  $expr: { $eq: ["$_id", "$$foreign_course_id"] },
                },
              },
            ],
            as: "course",
          },
        },
        { $unwind: "$course" },
        {
          $addFields: {
            courseName: "$course.name",
          },
        },
        {
          $project: {
            _id: 0,
            courseId: 1,
            courseName: 1,
            score: 1,
            enrollDate: 1,
          },
        },
      ],
      as: "enrolls",
    },
  },
  {
    $project: {
      _id: 1,
      name: 1,
      avg_score: {
        $avg: { $map: { input: "$enrolls", as: "e", in: "$$e.score" } },
      },
      address: 1,
      phone: 1,
      dob: 1,
      enrolls: 1,
    },
  },
  {
    $addFields: {
      rank: {
        $switch: {
          branches: [
            { case: { $gte: ["$avg_score", 8] }, then: "Giỏi" },
            { case: { $gte: ["$avg_score", 6] }, then: "Khá" },
            { case: { $gte: ["$avg_score", 4] }, then: "Trung Bình" },
            { case: { $gte: ["$avg_score", 2] }, then: "Yếu" },
          ],
          default: "Chưa Đạt",
        },
      },
    },
  },
]);

// câu 4: Nhập vào số nguyên n.
// Liệt kê n sinh viên có điểm trung bình lớn nhất (4d)

/*
db.Student.aggregate([
  {
    $lookup: {
      from: "Enrollment",
      localField: "_id",
      foreignField: "studentId",
      as: "enrolls",
    },
  },
  {
    $project: {
      _id: 1,
      name: 1,
      address: 1,
      phone: 1,
      dob: 1,
      avg_score: {
        $avg: "$enrolls.score",
      },
    },
  },
  {
    $sort: {
      avg_score: -1,
    },
  },
  {
    $limit: 3,
  },
]);
*/

// Câu 5: Nhập vào 2 số thực min và max. iệt kê thông tin các điểm số có giá trị nằm trong khoảng từ min đến max.
// Gồm các field sau: Mã sinh viên, họ tên, địa chỉ, Mã môn học, tên môn học, điểm số, ngày tham gia(4d)

/*
db.Enrollment.aggregate([
  {
    $match: {
      score: {
        $gte: 7,
        $lte: 9,
      },
    },
  },

  {
    $lookup: {
      from: "Course",
      localField: "courseId",
      foreignField: "_id",
      as: "course",
    },
  },
  {
    $lookup: {
      from: "Student",
      localField: "studentId",
      foreignField: "_id",
      as: "student",
    },
  },
  {
    $unwind: "$course",
  },
  {
    $unwind: "$student",
  },
  {
    $project: {
      _id: 0,
      student_id: "$studentId",
      student_name: "$student.name",
      address: "$student.address",
      course_name: "$course.name",
      score: 1,
      enrollDate: 1,
    },
  },
]);
*/
