import os
import sqlite3

dbcon = None
cursor = None
count = 0

def table_is_empty(table):
    cursor.execute("SELECT count(*) FROM " + table)
    return cursor.fetchall()[0][0] == 0


def tend_occupied_classrooms():
    done = []
    cursor.execute(
        "SELECT classrooms.*,courses.course_name FROM classrooms JOIN courses ON classrooms.current_course_id = courses.id WHERE current_course_id != 0")
    occupied_classes = cursor.fetchall()

    for classroom in occupied_classes:
        if classroom[3] == 1:
            cursor.execute("DELETE FROM courses WHERE id = ?", [classroom[2]])
            cursor.execute(
                "UPDATE classrooms SET current_course_id = 0 , current_course_time_left = 0 WHERE id = ?",
                [classroom[0]])
            done.append((classroom[0], classroom[4]))
        else:
            cursor.execute("UPDATE classrooms SET current_course_time_left = current_course_time_left - 1 WHERE id = ?", [classroom[0]])
    return done


def tend_students(grade, count):
    cursor.execute("UPDATE students SET count = count - ? WHERE grade = ?", (count, grade))


def tend_free_classrooms():
    cursor.execute("""SELECT * FROM courses JOIN 
                        classrooms ON classrooms.id = courses.class_id 
                        WHERE classrooms.current_course_id = 0 
                        ORDER BY classrooms.id, courses.id""")
    free_classes = cursor.fetchall()
    skip = None
    for classroom in free_classes:
        if classroom[4] == skip:
            continue
        skip = classroom[4]
        cursor.execute(
            "UPDATE classrooms SET current_course_id = ?, current_course_time_left = ? WHERE id = ?",
            [classroom[0], classroom[5], classroom[6]])
        tend_students(classroom[2], classroom[3])


def print_classes_spec(count, classrooms, done):
    for c in classrooms:
        for i, val in enumerate(done):
            if val[0] == c[0]:
                done_course = val[1]
                print("({}) {}: {} is done".format(count, c[1], done_course))
                break
        if c[4] is not None:
            if c[3] == c[9]:
                print("({}) {}: {} is schedule to start".format(count, c[1], c[5]))
            else:
                print("({}) {}: occupied by {}".format(count, c[1], c[5]))


def do_prints():
    for table in ["courses", "classrooms", "students"]:
        cursor.execute("SELECT * FROM " + table)
        print(table)
        for l in cursor.fetchall():
            print(l)


# create ‘myDB.db' file and connect to it
def main():
    count = 0
    while DBExist and not table_is_empty("courses"):
        cursor.execute("SELECT * FROM classrooms")
        done = tend_occupied_classrooms()
        tend_free_classrooms()
        cursor.execute(
            "SELECT * FROM classrooms LEFT JOIN courses ON classrooms.current_course_id = courses.id ORDER BY classrooms.id")
        classrooms = cursor.fetchall()

        print_classes_spec(count, classrooms, done)

        do_prints()
        count += 1

    if count == 0:
        do_prints()


if __name__ == "__main__":
    DBExist = os.path.isfile("schedule.db")
    if DBExist:
        dbcon = sqlite3.connect("schedule.db")
        cursor = dbcon.cursor()
        main()
        dbcon.commit()
        dbcon.close()
