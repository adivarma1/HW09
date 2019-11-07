""" HW09 Test Cases for Student repository
    @uthor: Adithya Varma   Created on: 10-30-19"""

from HW09_Adithya_Varma import Repository, Student, Instructor
import unittest

class StudentTest(unittest.TestCase):
        """ Class for Student test """
        def test_student(self):
                """ Function that tests class Student """
                student = Student("", "Badri", "Software Engineering")
                self.assertEqual(student._name, "Badri")  
                self.assertEqual(student._major, "Software Engineering")  
        
class InstructorTest(unittest.TestCase):
        """ Class for instructor test"""
        def test_instructor(self):
                """ Function that tests class Instructor """
                instructor = Instructor("", "Newton", "Software Engineering")
                self.assertEqual(instructor._name, "Newton")  
                self.assertEqual(instructor._dept, "Software Engineering")

class TestRepository(unittest.TestCase):
        """ Testing the Repsitory from HW09"""
        def test_Repository(self):
                """test for student pretty table"""
                wdir = "/Users/adithyavarma/Desktop/SSW 810/pyp"
                stevens = Repository(wdir)

                expected_students = ['10115', '10172', '10175', '10183', '11399', '11461', '11658', '11714', '11788']
                expected_instructors = ['98764', '98763', '98762', '98761', '98760']

                self.assertEqual(list(stevens._students), expected_students)
                self.assertEqual(list(stevens._instructors), expected_instructors)             


if __name__ == "__main__":
	unittest.main(exit=False, verbosity=2)
