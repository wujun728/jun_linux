import sqlite3 as sq

# 使用SQLite数据库（通过Python内置的sqlite3驱动器）

# 定义建表语句
query = """CREATE TABLE test (a varchar(20), b varchar(20), c real, d integer);"""

# 创建连接
con = sq.connect("mydata.sqlite");

# 执行操作
con.execute(query);

# 提交
con.commit();

# 数据部分
data = [('Atlanta', 'Georgia', 1.25, 6),('Tallahassee', 'Florida', 2.6, 3),('Sacramento', 'California', 1.7, 5)]

# 插入语句
stmt = "INSERT INTO test VALUES(?,?,?,?)"

# 提交插入数据
con.executemany(stmt, data);


###########  查询数据 #############

cursor = con.execute('select * from test');

# fetchone()  返回单个的元组，也就是一条记录(row)，如果没有结果 , 则返回 None
# fetchall()  返回多个元组，即返回多条记录(rows),如果没有结果,则返回()
rows = cursor.fetchall();
print(rows);




