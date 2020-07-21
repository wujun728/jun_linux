# -*- coding: utf-8 -*-
'''
Created on 2015-4-14

@author: Nob
'''
import logging

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# 记录一条日志
logger.info('foorbar')