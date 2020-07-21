#!/usr/bin/python3
try:
	print('try....')
	r=10/2
	print('result:',r)
except ValueError as e:
	print('ValueError:',e)
except ZeroDivisionError as  e:
	print('except:',e)
else:
	print('no error')
finally:
	print('finally....')
print('END')