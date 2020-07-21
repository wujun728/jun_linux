#!/usr/bin/python3
class Screen(object):
	"""docstring for Screen"""
	@property
	def width(self):
	    return self._width

	@property
	def height(self):
	    return self._height

	@width.setter
	def width(self,value):
		if not isinstance(value,int):
			raise ValueError('必须是整数输入')
		self._width=value

	@height.setter
	def height(self,value):
		if not isinstance(value,int):
			raise ValueError('必须是整数输入')
		self._height=value


	@property
	def resolution(self):
	    return self._width*self._height
	

#######################################
#下面测试
#######################################
s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution

