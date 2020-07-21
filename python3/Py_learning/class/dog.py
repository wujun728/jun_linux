#!/usr/bin/python3
from animal import Animal
class Dog(Animal):
	def run(self):
		print('Dog is running....')

if __name__=='__main__':
	dog=Dog()
	dog.run()