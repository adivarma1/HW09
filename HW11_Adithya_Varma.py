""" HW11 Creating a Student database and adding the database
    @uthor: Adithya Varma Created on:10-12-19"""

import sqlite3
from prettytable import PrettyTable
from HW08_Adithya_Varma import file_reading_gen
import os
from collections import defaultdict



class Student:
    """Class thats adds students to repository"""

    pt_table = ["CWID", "NAME", "Majors", "Courses Completed", "Required Courses", "Electives"]

    def __init__(self, cwid, name, major, mj): #mj is the instance of class major
        """ Initializing the field names"""
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = defaultdict(str)
        self._mj = mj


    def add_course(self, course, grade):
        """ Adding courses and grades"""
        self._courses[course] = grade

    def pt_summary(self):
        """ adding values to the pretty table"""
        return[self._cwid, self._name, self._major, sorted(self._mj.grades(self._courses)), self._mj.courses_required(self._courses), self._mj.courses_electives(self._courses)]

class Instructor:
    """Class thats adds instructor to repository"""

    pt_table = ["CWID", "NAME", "DEPT", "COURSE", "STUDENTS"]

    def __init__(self, cwid, name, dept):
        """ Initializing the field names"""
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int)

    def add_course(self, course):
        """ Adding courses """
        self._courses[course] += 1

    def pt_summary(self):
        """ Function adding to pretty table"""
        for course, students in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, students]

class Major:
    """Class that adds majors"""


    pt_table = ['Dept', 'Required', 'Elective']

    def __init__(self, major):
        """ initializing the field names """
        self._major = major
        self.required = set()
        self.elective = set()

    def update_major(self, flag, course):
        """ Checking if required or elective"""
        if flag == 'R':
            self.required.add(course)
        elif flag == 'E':
            self.elective.add(course)
        else:
            raise ValueError(' Unknown status of course')

    def pt_summary(self):
        """ return the values for prettytable"""
        return [self._major, sorted(self.required), sorted(self.elective)]

    def grades(self, courses):
        """ calculate the successfully completed courses, remaining required, elective courses"""
        passed_grades = ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C') # the grades needed to pass the course

        completed_courses = set()
        for course, grade in courses.items():
            if grade in passed_grades: # in case there is no grade for the course yet
                completed_courses.add(course)

        return completed_courses

    def courses_required(self, courses):
        """ function that returns remaining required courses """
        return self.required.difference(courses)

    def courses_electives(self, courses):
        """ function that returns remaining electives """
        if self.grades(courses).intersection(self.elective):
            return None
        else:
            return self.elective

class Repository:
    """Class contains details about both student and instructor"""


    def __init__(self, path):
        self._path = path
        self._students = dict()
        self._instructors = dict()
        self._majors = dict()
        self.read_majors(os.path.join(path, 'majors.txt'))
        self.read_students(os.path.join(path, 'students.txt'))
        self.read_instructors(os.path.join(path, 'instructors.txt'))
        self.read_grades(os.path.join(path, 'grades.txt'))
        self.student_prettytable()
        self.instructor_prettytable()
        self.major_prettytable()
        self.instructor_databbase(os.path.join(path, 'adi.db'))


    def read_students(self, path):
        """ Reads the values in the path"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep="\t", header = True):
                self._students[cwid] = Student(cwid, name, major, self._majors[major])
        except ValueError as err:
            print(err)

    def read_instructors(self, path):
        """ Reads the values in the path"""
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep = "\t", header = True):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as err:
            print(err)


    def read_grades(self, path):
        """ Reads the values in the path"""
        try:

            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep ='\t', header = True):
                if student_cwid in self._students:

                    self._students[student_cwid].add_course(course, grade)

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course(course)

        except ValueError as erf:

            print(erf)

    def read_majors(self, dir_path):
        """ Reads majors in the path"""
        for major, flag, course in file_reading_gen(dir_path, 3, sep='\t', header=True):

            if major not in self._majors:
                self._majors[major] = Major(major)

            self._majors[major].update_major(flag, course)

    def major_prettytable(self):
        """ Prettytable for major class"""
        pt1 = PrettyTable(field_names=Major.pt_table)
        for major in self._majors.values():
            pt1.add_row(major.pt_summary())
        print(pt1)


    def student_prettytable(self):
        """ Prettytable for student details"""
        pt = PrettyTable(field_names=Student.pt_table)
        for student in self._students.values():
            pt.add_row(student.pt_summary())
        print(pt)

    def instructor_prettytable(self):
        """ Prettytable for instructor details """
        pt = PrettyTable(field_names=Instructor.pt_table)
        for instructor in self._instructors.values():
            for row in instructor.pt_summary():
                pt.add_row(row)
        print(pt)
    
    def instructor_databbase(self, path):
        """ connects the database and displays it in a prettytable """
        try:
            con = sqlite3.connect(path)
        except sqlite3.DatabaseError:
            print('Error: Unable to open database')
        else:
            cursor = con.cursor()
            cursor.execute("""  select instructors.CWID, instructors.Name, instructors.Dept, grades.Course, count(grades.Course)
                                from instructors
                                JOIN grades on grades.InstructorCWID = instructors.CWID
                                group by grades.Course, instructors.Name """)
            final = cursor.fetchall()
            pt = PrettyTable(field_names=['CWID', 'Name', 'Department', 'Course', 'No of students'])
            for i in final:
                pt.add_row(i)
            print(pt)


def main():
    """ Takes the path to the repository """
    repo = Repository('/Users/adithyavarma/Desktop/SSW 810/pyp')


if __name__ == "__main__":
    main()