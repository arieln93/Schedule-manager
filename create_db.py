import sqlite3  
import sys
import os  
import atexit 

cursor = None
dbcon = None


def create_tables():
    # Note that DBExist and cursor are global variables and need to be set prior to calling this function
    cursor.execute(""" CREATE TABLE courses ( id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    student TEXT NOT NULL,
    number_of_students INTEGER NOT NULL,
    class_id INTEGER REFERENCES classrooms(id),
    course_length INTEGER NOT NULL)  """)
    cursor.execute(""" CREATE TABLE students ( grade TEXT PRIMARY KEY,
    count INTEGER NOT NULL)""")
    cursor.execute(""" CREATE TABLE classrooms ( id INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            current_course_id INTEGER NOT NULL,
            current_course_time_left INTEGER NOT NULL)  """)


def insert_course(id, name, student, num, classId, length):
    cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?)", [id, name, student, num, classId, length])


# insert a record into students table
def insert_student(grade, count):
    cursor.execute("INSERT INTO students VALUES (?, ?)", [grade, count])


# insert a record into students table
def insert_classroom(id, location):
    cursor.execute("INSERT INTO classrooms VALUES (?, ?, ?, ?)", [id, location, 0, 0])


# print table as table
def printTable(table):
    print(table)
    cursor.execute('SELECT * FROM ' + table);
    list = cursor.fetchall()
    for item in list:
        print(item)


def read_from_file():
    file1 = open(sys.argv[1], "r")
    for line in file1:
        list1 = line.split(",")
        list1 = [x.strip() for x in list1]
        if len(list1) > 0:
            if list1[0] == 'S':
                insert_student(list1[1], list1[2])
            if list1[0] == "R":
                insert_classroom(list1[1], list1[2])
            if list1[0] == "C":
                insert_course(list1[1], list1[2], list1[3], list1[4], list1[5], list1[6])
    file1.close()
    printTable("courses")
    printTable("classrooms")
    printTable("students")


# define a function to be called when program terminates
def close_db():
    dbcon.commit()  # if you want to save changes into database file
    cursor.close()
    dbcon.close()


def main(argv):
    global dbcon, cursor
    DBExist = os.path.isfile("schedule.db")
    if DBExist:
        sys.exit()

    dbcon = sqlite3.connect("schedule.db")
    cursor = dbcon.cursor()
    create_tables()
    read_from_file()
    atexit.register(close_db)


if __name__ == '__main__':
    main(sys.argv)
