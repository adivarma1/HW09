""" HW09 Creating a Student database
    @uthor: Adithya Varma Created on:10-28-19"""


from prettytable import PrettyTable         
from HW08_Adithya_Varma import file_reading_gen
import os
from collections import defaultdict



class Student:
    """Class thats adds students to repository"""

    pt_table = ["CWID", "NAME", "Courses Completed"]            

    def __init__(self, cwid, name, major):
        """ Initializing the field names"""
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = defaultdict(str)
        

    def add_course(self, course, grade):
        """ Adding courses and grades"""
        self._courses[course] = grade       

    def pt_summary(self):
        """ adding values to the pretty table"""
        return[self._cwid, self._name, sorted(self._courses.keys())]   

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

class Repository:
    """Class contains details about both student and instructor"""
    _students = dict()
    _instructors = dict()

    def __init__(self, path):
        self._path = path
        self.read_students(os.path.join(path, 'students.txt'))          
        self.read_instructors(os.path.join(path, 'instructors.txt'))
        self.read_grades(os.path.join(path, 'grades.txt'))
        self.student_prettytable()
        self.instructor_prettytable()


    def read_students(self, path):
        """ Reads the values in the path"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep = "\t", header = False):
                self._students[cwid] = Student(cwid, name, major)           
        except ValueError as err:
            print(err)

    def read_instructors(self, path):
        """ Reads the values in the path"""
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep = "\t", header = False):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as err:
            print(err)


    def read_grades(self, path):
        """ Reads the values in the path"""
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep ='\t', header = False):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade)      
                
                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course(course) 
                    
        except ValueError as erf:
            print(erf)

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

def main():
    """ Takes the path to the repository """
    repo = Repository('/Users/adithyavarma/Desktop/SSW 810/pyp')

        
if __name__ == "__main__":
    main()                      
