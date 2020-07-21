#!/usr/bin/python3
class Student(object):
	"""docstring for Student"""
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "Student object(name:%s)"%self.name

	__repr__=__str__
print(Student('Michael'))
s=Student('Mike')
s