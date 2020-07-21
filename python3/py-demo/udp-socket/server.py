# -*- coding: utf-8 -*-
'''
from http://www.pythondoc.com/python-cookbook/cookbook_12.html
@author: Nob
'''


import socket
port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print "waiting on port:", port
while 1:
    data, addr = s.recvfrom(1024)
    print data