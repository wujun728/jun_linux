#!/usr/bin/python3
'Run twice'

__author__='Zhjy'

from animal import Animal
def run_twice(animal):
	animal.run()
	animal.run()

if __name__=='__main__':
	run_twice(Animal())
