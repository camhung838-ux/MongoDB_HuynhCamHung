use("DT2507L-NK_huynhcamhung_StudentDB");

function insert_test_students() {
  db.createCollection("Student");

  resp = db.Student.insertMany([
    {
      name: "Student 1",
      address: "TPHCM",
      phone: "111",
      dob: ISODate("2000-01-01"),
    },
    {
      name: "Student 2",
      address: "TPHCM",
      phone: "222",
      dob: ISODate("2000-01-02"),
    },
    {
      name: "Student 3",
      address: "Ha Noi",
      phone: "333",
      dob: ISODate("2000-01-03"),
    },
    {
      name: "Student 4",
      address: "Ha Noi",
      phone: "444",
      dob: ISODate("2001-01-01"),
    },
    {
      name: "Student 5",
      address: "Da Nang",
      phone: "555",
      dob: ISODate("2001-02-01"),
    },
    {
      name: "Student 6",
      address: "Da Nang",
      phone: "666",
      dob: ISODate("2001-03-01"),
    },
    {
      name: "Student 7",
      address: "Hue",
      phone: "777",
      dob: ISODate("2002-12-01"),
    },
    {
      name: "Student 8",
      address: "Hue",
      phone: "888",
      dob: ISODate("2002-11-01"),
    },
    {
      name: "Student 9",
      address: "Hue",
      phone: "999",
      dob: ISODate("2003-01-01"),
    },
    {
      name: "Student 10",
      address: "Hue",
      phone: "101010",
      dob: ISODate("2003-01-01"),
    },
  ]);

  console.log(resp);
}

function insert_test_courses() {
  db.createCollection("Course");

  resp = db.Course.insertMany([
    {
      name: "Toan",
      description: "Hoc toan",
    },
    {
      name: "Ly",
      description: "Hoc ly",
    },
    {
      name: "Hoa",
      description: "Hoc hoa",
    },
    {
      name: "Van",
      description: "Hoc van",
    },
    {
      name: "Lich su",
      description: "Hoc lich su",
    },
    {
      name: "Anh van",
      description: "Hoc anh van",
    },
    {
      name: "Sinh hoc",
      description: "Hoc sinh hoc",
    },
    {
      name: "Dao duc",
      description: "Hoc dao duc",
    },
    {
      name: "Am nhac",
      description: "Hoc am nhac",
    },
    {
      name: "Dia ly",
      description: "Hoc dia ly",
    },
  ]);

  console.log(resp);
}

function insert_test_enrollments() {
  ////// Auto assign all students to different n course

  //Support fucntions
  function convert_mongo_to_array(mongo_object) {
    let return_array = [];

    mongo_object.forEach((document) => {
      return_array.push(document);
    });

    return return_array;
  }

  function get_random_subset(original_array, size) {
    if (size > original_array.length) {
      console.log("Input subset size bigger than orginal array");
      return;
    }
    clone_array = [...original_array];

    for (var i = clone_array.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = clone_array[i];
      clone_array[i] = clone_array[j];
      clone_array[j] = temp;
    }

    return clone_array.slice(0, size);
  }

  // Auto assign logic
  n_courses = 3;
  max_score = 10;

  enrollment_list = [];

  students = db.Student.find({});
  courses = convert_mongo_to_array(db.Course.find({}));

  students.forEach((student) => {
    random_courses = get_random_subset(courses, n_courses);

    random_courses.forEach((course) => {
      random_score = Math.floor(Math.random() * max_score);
      enrollment = {
        studentId: ObjectId(student["_id"]),
        courseId: ObjectId(course["_id"]),
        courseName: course["name"],
        score: random_score,
        enrollDate: ISODate(),
      };

      enrollment_list.push(enrollment);
    });
  });

  //Add data to Enrollment
  db.createCollection("Enrollment");
  resp = db.Enrollment.insertMany(enrollment_list);
  console.log(resp);
}

// insert_test_students();
// insert_test_courses();
// insert_test_enrollments();
