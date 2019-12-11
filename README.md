# Schedule-manager
## General Description
An sqlite3 database that holds courses, students, and classrooms tables, and assigning classrooms to courses using Python and SQLite.
## Method and Technical Description
### The Database Structure
The database classes.db has three tables.
 1. courses: This table holds information of the courses. The columns are: id, course_name, student, number_of_students, class_id, classrooms, course_length.
 2. students: This table holds the number of students per grade. The columns are: grade, count.
 3. classrooms: This table holds the location and the status of each class room. The columns are: id, location, current_course_id, current_course_time_left.
## schedule.py
This module is in charge of orchestrating the schedule of the courses.
It will run in a loop until one of the following conditions hold:
1. The database file schedule.db does not exist.
2. All courses are done (The courses table is empty)
At each iteration of the loop it will print the tables, the name of the table followed by the tuples (each in a row).
At the beginning all classrooms are free and available.
At each iteration, many courses as possible need to be assigned to their classrooms (by the
input file order). A classroom is available if “current_course_time_left” is zero. When a course is
assigned to a classroom the amount of students allowed to take that course should be deducted
from the total amount of available students since each student is allowed to participate only in
a single course.

## create_ db.py
This module is the module that builds the database and inputs the initial data from the
configuration file. When run, it will be given an argument of the path for the config file. For
example, "python3 create_db.py config".
If it is the first time the module runs, i.e. the database file does not yet exist, then it should
create the database and the tables as specified, parse the config file, and store the data
given in the config file in the database.

## Configuration Files
Each line in the configuration file represents either a course(C), students(S), or a
classroom(R).
For example:
“C, 1, SPL 191, cs_ungrd, 80, 3, 2” represents a course id is 1, named “SPL 191” requires 80
computer science undergraduate students, located at classroom with id 3 and needs 2 iterations to 
complete , and.
“S, cs_grad, 150” represents there are 150 computer science graduate students
“R, 1, 90/233” represents the classroom 90/ 233 whose id is 1.
