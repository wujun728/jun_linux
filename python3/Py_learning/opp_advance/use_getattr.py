#!/usr/bin/python3
class Chain(object):
	"""docstring for Chain"""
	def __init__(self, path=''):
		self.path=path

	def __getattr__(self,path):
		return Chain('%s%s'%(self.path,path))

	def __str__(self):
		return self._path


	__repr__=__str__

