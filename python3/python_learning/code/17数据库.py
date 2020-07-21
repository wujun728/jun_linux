'''
Created on 2018年10月10日

@author: Administrator
'''
import pymysql as pm
conn=pm.connect("localhost","root","123456","demo")

# 获取当前的游标对象
cursor=conn.cursor()

# 执行SQL语句
cursor.execute("select * from emp")

# 抓取到值
# emp=cursor.fetchone()
# print(emp)
# print(type(emp))
all=cursor.fetchall()
print(all)

#关闭连接
conn.close()