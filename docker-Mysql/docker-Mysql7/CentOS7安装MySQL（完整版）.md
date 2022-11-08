# [CentOS7安装MySQL（完整版）](https://www.cnblogs.com/yss818824/p/12349719.html)

在CentOS中默认安装有MariaDB，这个是MySQL的分支，但为了需要，还是要在系统中安装MySQL，而且安装完成之后可以直接覆盖掉MariaDB。

### 1 下载并安装MySQL官方的 Yum Repository,Mysql版本5.7.14

```
[root@localhost ~]# yum -y install mysql57-community-release-el7-10.noarch.rpm
```

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223121716019-249128534.png)

 

使用上面的命令就直接下载了安装用的Yum Repository，大概25KB的样子，然后就可以直接yum安装了。

```
[root@localhost ~]# yum -y install mysql57-community-release-el7-10.noarch.rpm
```

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223121910756-796254492.png)

 

 

 之后就开始安装MySQL服务器

```
[root@localhost ~]# yum -y install mysql-community-server
```

这步可能会花些时间，安装完成后就会覆盖掉之前的mariadb，具体多久根据个人网速决定。

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223135556321-206061203.png)

 

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223135634512-1182117406.png)

 

 

 ![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223135721838-1733161177.png)

 

 

 安装完成，接下来进行mysql的一些配置。

### 2 MySQL数据库设置

（1）首先启动MySQL

```
[root@localhost ~]# systemctl start  mysqld.service
```

（2）查看MySQL运行状态，运行状态如图：

```
[root@localhost ~]# systemctl status mysqld.service
```

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223135914965-841480391.png)

 

 

 （3）此时MySQL已经开始正常运行，不过要想进入MySQL还得先找出此时root用户的密码，通过如下命令可以在日志文件中找出密码：

```
[root@localhost ~]# grep "password" /var/log/mysqld.log
```

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223140024043-914316551.png)

 

 

 （4）如下命令登录数据库：

 

```
[root@localhost ~]# mysql -uroot -p
```

（5）此时不能做任何事情，因为MySQL默认必须修改密码之后才能操作数据库，如下命令修改密码：

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new password';
```

其中‘new password’替换成你要设置的密码，注意:密码设置必须要大小写字母数字和特殊符号（,/';:等）,不然不能配置成功。

如果出现如下错误：

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223140359672-390749921.png)

 

 是以为密码的复杂度不符合默认规定，如下命令查看mysql默认密码复杂度：

```
SHOW VARIABLES LIKE 'validate_password%';
```

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223140628401-1902345961.png)

 

 

 如需修改密码复杂度参考如下命令：

```
set global validate_password_policy=LOW;
```

 

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223140721583-1718649859.png)

 

 

 

```
set global validate_password_length=6;
```

 ![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223140843664-1138395293.png)

 

 

 

### 3 开启mysql的远程访问

执行以下命令开启远程访问限制（注意：下面命令开启的IP是 192.168.19.128，如要开启所有的，用%代替IP）：

```
grant all privileges on *.* to 'root'@'192.168.0.1' identified by 'password' with grant option;
```

**注：password--是你设置你的mysql远程登录密码。**

然后再输入下面两行命令

```
mysql> flush privileges;
```

此步操作，退出mysql也可以。具体参考：

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223141433774-1613386939.png)

 

 

 

### 4 、开启防火墙端口，CentOS为firewalld添加开放端口3306，具体是什么参考如下：

[　　　　https://i-beta.cnblogs.com/posts?cateId=1653053](https://i-beta.cnblogs.com/posts?cateId=1653053)

### 5 、更改mysql的语言

首先重新登录mysql，然后输入status：

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223141820442-26776716.png)

 



 可以看到，红色方框处不是utf-8，修改为utf8即可。

因此我们先退出mysql，然后再到/etc目录下的my.cnf文件下修改一下文件内容

```
cd /etc
```

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223142042765-727425898.png)

 

 进入文件后，新增四行代码：

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223142058134-390931034.png)

 



 保存更改后的my.cnf文件后，重启下mysql，然后输入status再次查看，你就会发现变化啦

![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223142143245-586519999.png)

 



 ![img](https://img2018.cnblogs.com/i-beta/1780831/202002/1780831-20200223142200190-1364319425.png)

 

 到此CentOS7安装Mysql5.7完毕。

set global validate_password_policy=LOW;