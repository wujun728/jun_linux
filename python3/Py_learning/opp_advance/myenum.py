#!/usr/bin/python3
from enum import Enum

Month=Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name,member in Month.__members__.items():
	print(name,'=>',member,',',member.value)


from enum import Enum,unique

@unique
class Weekday(Enum):
	"""docstring for Weekday"""
	Sun=0
	Mon=1
	Tue=2
	Wed=3
	Thu=4
	Fri=5
	Sat=6

for name,member in Weekday.__members__.items():
	print(name,'=>',member)
		