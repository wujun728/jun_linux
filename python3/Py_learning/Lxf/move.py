#!/usr/bin/python3
import math
def move(x,y,step,angle=0):
	'''给出坐标，位移和角度，就可以计算出新的坐标'''
	nx=x+step*math.cos(angle)
	ny=y-step*math.sin(angle)
	return nx,ny
