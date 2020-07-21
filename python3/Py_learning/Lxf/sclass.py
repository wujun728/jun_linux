#!/usr/bin/python3
'Student Class'
class  Student(object):
	"""name,scorestring for  Student"""
	def __init__(self, name,score):
		self.__name =name
		self.__score=score

	def get_name(self):
		return self.__name

	def get_score(self):
		return self.__score

	def set_score(self,score):
		if 0<=score<=100:
			self.__score=score
		else:
			print('数据非法')

	def print_score(std):
		print('%s:%s'%(std.__name,std.__score))

	def get_grade(self):
		if self.__score>=90:
			return 'A'
		elif self.__score>=60:
			return 'B'
		else:
			return 'C'

