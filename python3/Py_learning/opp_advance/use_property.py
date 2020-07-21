#!/usr/bin/python3
class Student(object):
	"""docstring for Student"""
	@property
	def score(self):
		return self._score
	
	@score.setter
	def score(self,value):
		if not isinstance(value,int):
			raise  ValueError('成绩必须是整数')
		if value<0 or value>100:
			raise ValueError('成绩必须处于0~100之间!')
		self._score=value		