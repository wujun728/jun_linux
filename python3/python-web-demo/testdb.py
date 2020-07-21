#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector

conn = mysql.connector.connect(user='root',password='',database='test',use_unicode=True)

cursor = conn.cursor()

#sql = 'create table user (id varchar(20) primary key, name varchar(20))'

#create a user table

#cursor.execute(sql)

sql = "insert into user (id, name) values('%s', '%s')" % ('1','Hejing')
print sql

#cursor.execute('insert table user (id, name) values(%s, %s)',['1','Hejing'])
#sql = "INSERT INTO user (id, name) VALUES ('3', 'hejing')"
cursor.execute(sql)

#cursor.rowcount

conn.commit()

#cursor.close()

sql = "select * from user where id ='%s'" %('1',)
cursor.execute(sql)



values = cursor.fetchall()

print values

cursor.close()


