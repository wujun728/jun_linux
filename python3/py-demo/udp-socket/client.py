# -*- coding: utf-8 -*-
'''

@author: Nob
'''
import socket
port = 8081
host = "localhost"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 0))
s.sendto("Holy Guido! It's working.", (host, port))