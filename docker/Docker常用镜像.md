# [Docker常用镜像](https://www.cnblogs.com/leanfish/p/9938530.html)

　　Docker，具有快捷方便的特性，机器上不需要安装软件和进行各种配置，拉取镜像，一行命令即可启动服务，不使用时，一行命令关闭容器即可，快捷方便，干净、利索。建议将本地的redis、mysql、kafka等常见服务使用docker进行安装，使用时用命令行启动，不使用则关闭即可。

下面列出我本地常用的镜像。

一、本地docker添加https://registry.docker-cn.com镜像地址

在国内拉取镜像时经常出现超时现象，建议添加docker中国地址，例如

![img](https://img2018.cnblogs.com/blog/319088/201811/319088-20181110101127292-1992962732.png)

 二、我本地使用的docker清单：

1、postgres
2、mysql
3、redis
4、nginx
5、mongo
6、kafka
7、rabbitmq


三、镜像命令
-- 拉取镜像。tag不写的话，则拉取最新版的镜像

```
docker pull 镜像名称:tag
```

 -- 查看镜像

```
docker images
```

 -- 查找镜像仓库中镜像

```
docker search 镜像名
```

 -- 查找本地镜像

```
docker images | ``grep` `镜像名
```

 -- 移除镜像

```
docker rmi 镜像名称:tag
```

-- 进入容器，可以查看容器内部文件组

```
docker ``exec` `-it [CONTAINER ID] ``/bin/sh
```

 -- 查看正在运行的容器

```
docker ``ps` `-a ``# docker ps -a | grep <容器名>
```

 -- 停止正在运行的容器

```
docker stop [CONTAINER ID]
```

 -- 移除已经停止的容器

```
docker ``rm` `[CONTAINER ID]
```

 

四、各个镜像的使用

**1、postgres**
-- 拉取镜像

```
docker pull postgres:9.6
```

 -- 运行镜像

```
docker run --name mypostgre -e POSTGRES_PASSWORD=root -p 54321:5432 -d postgres:9.6
```

 

解释：
run，创建并运行一个容器；
--name，指定创建的容器的名字；
-e POSTGRES_PASSWORD=password，设置环境变量，指定数据库的登录口令为password(登录名：postgres)；
-p 54321:5432，端口映射将容器的5432端口映射到外部机器的54321端口；
-d postgres:9.6，指定使用postgres:9.6作为镜像。

在使用客户端连接数据库即可。

 

**2、mysql**
-- 拉取镜像

```
docker pull mysql:8
```

 -- 运行镜像

```
docker run --name mysqllocal -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:8
```

 -- 进入容器

-- 登录mysql

```
mysql -u root -p 解释： —登录名：root 密码：root
```

-- 修复navicat客户端登录

```
ALTER USER root IDENTIFIED WITH mysql_native_password BY root;
```

再使用客户端连接数据库即可。　　

 

**3、redis**
-- 拉取镜像

```
docker pull redis:3.2
```

-- 运行镜像

```
docker run --name myredis -p 6379:6379 -d redis:3.2 redis-server
```

-- 进入容器

-- 登录redis

```
redis-cli
```

 

有密码的，需要登录

docker exec -it 63519b779f2f redis-cli -a ‘密码’

常用命令：

先要选择库，select [0-15]

#### 1、查询键

keys * 查询所有的键，会遍历所有的键值，复杂度O(n)

#### 2、键总数

dbsize 查询键总数，直接获取redis内置的键总数变量，复杂度O(1)

#### 3、检查键是否存在

exists key 存在返回1，不存在返回0

#### 4、删除键O(k)

del key [key...] 返回结果为成功删除键的个数

　　

**4、nginx**
-- 拉取镜像

```
docker pull nginx
```

-- 运行镜像

```
docker run --name mynginx -d -p 8080:80 nginx:latest
```

　　

**5、mongo**
-- 拉取镜像

```
docker pull mongo
```

-- 运行镜像

```
docker run -p 27017:27017 -d mongo:latest
```

　　

**6、kafka**
-- 拉取镜像

```
zookeeker: docker pull zookeeper:latest``kafka: docker pull wurstmeister``/kafka``:latest
```

-- 运行镜像

-- 运行zookeeper

```
docker run -d --name myzookeeper --publish 2181:2181 --volume ``/etc/localtime``:``/etc/localtime` `zookeeper:latest
```

-- 运行kafka

```
docker run -d --name mykafka --publish 9092:9092 \``--link myzookeeper \``--``env` `KAFKA_ZOOKEEPER_CONNECT=myzookeeper:2181 \``--``env` `KAFKA_ADVERTISED_HOST_NAME=kafka所在宿主机的IP \``--``env` `KAFKA_ADVERTISED_PORT=9092 \``--volume ``/etc/localtime``:``/etc/localtime` `\``wurstmeister``/kafka``:latest
```

　　

**7、rabbitmq**

-- 拉取镜像

```
docker pull rabbitmq:management
```

*-- 运行镜像*

```
docker run -d --name rabbitmq --publish 5671:5671 \`` ``--publish 5672:5672 --publish 4369:4369 --publish 25672:25672 --publish 15671:15671 --publish 15672:15672 \``rabbitmq:management
```

*容器启动之后就可以访问web 管理端了 http://宿主机IP:15672，默认创建了一个 guest 用户，密码也是 guest。*