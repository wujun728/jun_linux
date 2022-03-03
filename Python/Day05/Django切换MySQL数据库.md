## 准备

| 软件 | 版本  | 
| ---- | ----- |
|   Django   | 2.1.3 |   
|   Python   |  3.7.1 |    


默认使用的是sqlite3

```
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
}
```
切换为MySql：

```
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'book',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'POST': '3306',
    }
}
```



## 实现步骤：

我们使用Django 来操作MySQL，实际上底层还是通过Python来操作的。因此我们想要用Django来操作MySQL，首先还是需要安装一个驱动程序。在Python3中，驱动程序有多种选择。比如有pymysql以及mysqlclient等。 

常见的Mysql驱动介绍：


- MySQL-python：也就是MySQLdb。是对C语言操作MySQL数据库的一个简单封装。遵循了Python DB API v2。但是只支持Python2，目前还不支持Python3。
- mysqlclient：是MySQL-python的另外一个分支。支持Python3并且修复了一些bug。
- pymysql：纯Python实现的一个驱动。因为是纯Python编写的，因此执行效率不如MySQL-python。并且也因为是纯Python编写的，因此可以和Python代码无缝衔接。
- MySQL Connector/Python：MySQL官方推出的使用纯Python连接MySQL的驱动。因为是纯Python开发的。效率不高。

### mysqlclient安装

基于目前的环境以及版本来说，直接运行 pip install mysqlclient 是会报错的，具体错误，自己执行以下就知道了。

解决办法：

去 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient 下载指定文件，我用的是python3.7，win环境是64位，所以下载了mysqlclient-1.3.13-cp37-cp37m-win_amd64.whl。

然后执行：


```
pip3 install mysqlclient-1.3.13-cp37-cp37m-win_amd64.whl
```

如果出现以下说明安装成功：


```
Installing collected packages: mysqlclient
Successfully installed mysqlclient-1.3.13
```

### 迁移数据库

Django中通过以下命令来迁移数据库，在每次创建Model时，执行该命令，在数据库中生成对应的表：


```
python manage.py makemigrations
python manage.py migrate
```
