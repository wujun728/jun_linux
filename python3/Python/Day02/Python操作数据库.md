## 简介

- pymysql：纯Python实现的一个驱动。因为是纯Python编写的，因此执行效率不如MySQL-python。并且也因为是纯Python编写的，因此可以和Python代码无缝衔接。

- MySQL Connector/Python：MySQL官方推出的使用纯Python连接MySQL的驱动。因为是纯Python开发的，效率不高。


- MySQL-python：也就是MySQLdb。是对C语言操作MySQL数据库的一个简单封装。遵循了Python DB API v2。但是只支持Python2，目前还不支持Python3。

- mysqlclient：是MySQL-python的另外一个分支。支持Python3并且修复了一些bug。


## PyMySQL

Python3 MySQL 数据库连接 - PyMySQL 驱动

PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库，Python2中则使用mysqldb。


```
pip3 install PyMySQL
```

### 案例

这里以查询秒杀商品数据为例：

```
#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "seckill")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * FROM seckill")

# 使用 fetchall() 方法获取s所有数据.
data = cursor.fetchall()

print(data)

# 关闭数据库连接
db.close()
```

----------------------------------------------------------------------------------

## mysql-connector

mysql-connector 是 MySQL 官方提供的驱动器。

我们可以使用 pip 命令来安装 mysql-connector：


```
pip3 install  mysql-connector
```

### 案例

这里以查询秒杀商品数据为例：

```
#!/usr/bin/python3

import mysql.connector

# 打开数据库连接
# db = pymysql.connect("localhost", "root", "123456", "seckill")

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123456",
  database="seckill"
)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * FROM seckill")

# 使用 fetchall() 方法获取s所有数据.
data = cursor.fetchall()

print(data)

# 关闭数据库连接
db.close()
```
