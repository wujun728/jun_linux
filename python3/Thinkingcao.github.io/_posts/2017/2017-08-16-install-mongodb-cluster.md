---
layout: post
title: mongodb 3.4 集群搭建升级版 五台集群
category: mongodb
tags: [mongodb]
---

最新版mongodb推荐使用yaml语法来做配置，另外一些旧的配置在最新版本中已经不在生效，所以我们在生产实际搭建mongodb集群的时候做了一些改进。如果大家不熟悉什么是分片、副本集、仲裁者的话请先移步查看上一篇文章：[mongodb 3.4 集群搭建：分片+副本集](http://www.ityouknow.com/mongodb/2017/08/05/mongodb-cluster-setup.html)

和前一个版本相比，改动点有：

- 配置文件采用yaml方式来配置  
- 生产中取消了仲裁者的角色，因为仲裁者也不会存储数据，只是起到选举的作用，线上为了保证数据安全，每份数据都会配置两个副本集，也就是每份数据存储了三份。  
- 优化配置，采用五台集群  
- 使用非root账户搭建mongodb集群。

## 环境准备

系统系统 centos6.9        
五台服务器：192.168.0.31/32/33/34/35   
安装包： mongodb-linux-x86_64-3.4.6.tgz  

服务器规划

服务器31      |服务器32	      |服务器33       |服务器34      |服务器35
---           |---            |---            |---           |---
mongos server |mongos server  |config server  |config server |config server
shard1 server |shard2 server  |shard3 server  |shard4 server |shard5 server
shard5 server |shard1 server  |shard2 server  |shard3 server |shard4 server
shard4 server |shard5 server  |shard1 server  |shard2 server |shard3 server


端口分配：

``` properties
mongos：20000
config：21000
shard1：27001
shard2：27002
shard3：27003
shard4：27004
shard5：27005
```

权限分配：

登录root账户，将安装目录和数据目录权限分配给日常操作（youknow）账户

``` properties
chown -R youknow:youknow /usr/local/
chown -R youknow:youknow /data
```

## mongodb安装


### 1、下载

下载 mongodb 3.4.6 安装包

``` sh
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.6.tgz
```

``` sh
#解压
tar -xzvf mongodb-linux-x86_64-3.4.6.tgz -C /usr/local/
#改名
mv mongodb-linux-x86_64-3.4.6 mongodb
```

### 2、创建相关目录

根据服务器的规范，分别在对应的服务器上建立conf、mongos、config、shard1、shard2、shard3、shard4、shard5等目录，因为mongos不存储数据，只需要建立日志文件目录即可。

``` sh
mkdir -p /usr/local/mongodb/conf
mkdir -p /data/mongos/log
mkdir -p /data/config/data
mkdir -p /data/config/log
mkdir -p /data/shard1/data
mkdir -p /data/shard1/log
mkdir -p /data/shard2/data
mkdir -p /data/shard2/log
mkdir -p /data/shard3/data
mkdir -p /data/shard3/log
mkdir -p /data/shard4/data
mkdir -p /data/shard4/log
mkdir -p /data/shard5/data
mkdir -p /data/shard5/log
```


### 3、环境变量

为了后续方便操作，配置mongodb的环境变量，需要切到root用户下面

``` sh
vim /etc/profile
# 内容
export MONGODB_HOME=/usr/local/mongodb
export PATH=$MONGODB_HOME/bin:$PATH
# 使立即生效，在安装用户下（youknow）执行
source /etc/profile
```

查看mongodb版本信息```mongod -v``` 输出版本信息表明配置环境变量成功


## 集群配置

### 1、config server配置服务器

在服务器33、34、35上配置以下内容：

添加配置文件：

添加配置文件

``` sh
vi /usr/local/mongodb/conf/config.conf

## content
systemLog:
  destination: file
  logAppend: true
  path: /data/config/log/config.log
 
# Where and how to store data.
storage:
  dbPath: /data/config/data
  journal:
    enabled: true
# how the process runs
processManagement:
  fork: true
  pidFilePath: /data/config/log/configsrv.pid
 
# network interfaces
net:
  port: 21000
  bindIp: 192.168.0.33
 
#operationProfiling:
replication:
    replSetName: config        

sharding:
    clusterRole: configsvr
```

启动三台服务器的config server

``` sh
numactl --interleave=all mongod --config /usr/local/mongodb/conf/config.conf
```

登录任意一台配置服务器，初始化配置副本集

``` sh
#连接
mongo 192.168.0.33:21000
#config变量
config = {
...    _id : "config",
...     members : [
...         {_id : 0, host : "192.168.0.33:21000" },
...         {_id : 1, host : "192.168.0.34:21000" },
...         {_id : 2, host : "192.168.0.35:21000" }
...     ]
... }

#初始化副本集
rs.initiate(config)

#查看分区状态
rs.status();
```

其中，"_id" : "configs"应与配置文件中配置的 replicaction.replSetName 一致，"members" 中的 "host" 为三个节点的ip和port

*这样配置服务器就配置好了*


### 2、配置分片、副本集

#### 配置第一个分片副本集

在服务器 31、32、33上面做以下配置

配置文件

``` sh
vi /usr/local/mongodb/conf/shard1.conf

#配置文件内容
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/shard1/log/shard1.log
 
# Where and how to store data.
storage:
  dbPath: /data/shard1/data
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
       cacheSizeGB: 20

# how the process runs
processManagement:
  fork: true 
  pidFilePath: /data/shard1/log/shard1.pid
 
# network interfaces
net:
  port: 27001
  bindIp: 192.168.0.33

#operationProfiling:
replication:
    replSetName: shard1
sharding:
    clusterRole: shardsvr
```

启动三台服务器的shard1 server

``` sh
numactl --interleave=all mongod  --config  /usr/local/mongodb/conf/shard1.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo 192.168.0.31:27001
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard1",
...     members : [
...         {_id : 0, host : "192.168.0.31:27001" },
...         {_id : 1, host : "192.168.0.32:27001" },
...         {_id : 2, host : "192.168.0.33:27001" }
...     ]
... }


#初始化副本集配置
rs.initiate(config);


#查看分区状态
rs.status();
```


#### 配置第二个分片副本集

在服务器32、33、34上面做以下配置

配置文件

``` sh
vi /usr/local/mongodb/conf/shard2.conf

#配置文件内容
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/shard2/log/shard2.log
 
# Where and how to store data.
storage:
  dbPath: /data/shard2/data
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
       cacheSizeGB: 20
 
# how the process runs
processManagement:
  fork: true 
  pidFilePath: /data/shard2/log/shard2.pid
 
# network interfaces
net:
  port: 27002
  bindIp: 192.168.0.33

 
#operationProfiling:
replication:
    replSetName: shard2
sharding:
    clusterRole: shardsvr
```

启动三台服务器的shard2 server

``` sh
numactl --interleave=all mongod  --config /usr/local/mongodb/conf/shard2.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo 192.168.0.32:27002
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard2",
...     members : [
...         {_id : 0, host : "192.168.0.32:27002" },
...         {_id : 1, host : "192.168.0.33:27002" },
...         {_id : 2, host : "192.168.0.34:27002" }
...     ]
... }


#初始化副本集配置
rs.initiate(config);

#查看分区状态
rs.status();
```

#### 配置第三个分片副本集

在服务器33、34、35上面做以下配置

配置文件

``` sh
vi /usr/local/mongodb/conf/shard3.conf

#配置文件内容
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/shard3/log/shard3.log
 
# Where and how to store data.
storage:
  dbPath: /data/shard3/data
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
       cacheSizeGB: 20
# how the process runs
processManagement:
  fork: true 
  pidFilePath: /data/shard3/log/shard3.pid
 
# network interfaces
net:
  port: 27003
  bindIp: 192.168.0.33

 
#operationProfiling:
replication:
    replSetName: shard3
sharding:
    clusterRole: shardsvr
```

启动三台服务器的shard3 server

``` sh
numactl --interleave=all mongod  --config  /usr/local/mongodb/conf/shard3.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo 192.168.0.33:27003
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard3",
...     members : [
...         {_id : 0, host : "192.168.0.33:27003" },
...         {_id : 1, host : "192.168.0.34:27003" },
...         {_id : 2, host : "192.168.0.35:27003" }
...     ]
... }


#初始化副本集配置
rs.initiate(config);

#查看分区状态
rs.status();
```


#### 配置第四个分片副本集

在服务器34、35、31上面做以下配置

配置文件

``` sh
vi /usr/local/mongodb/conf/shard4.conf

#配置文件内容
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/shard4/log/shard4.log
 
# Where and how to store data.
storage:
  dbPath: /data/shard4/data
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
       cacheSizeGB: 20

# how the process runs
processManagement:
  fork: true 
  pidFilePath: /data/shard4/log/shard4.pid
 
# network interfaces
net:
  port: 27004
  bindIp: 192.168.0.35

 
#operationProfiling:
replication:
    replSetName: shard4
sharding:
    clusterRole: shardsvr
```

启动三台服务器的shard4 server

``` sh
numactl --interleave=all mongod  --config /usr/local/mongodb/conf/shard4.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo 192.168.0.34:27004
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard4",
...     members : [
...         {_id : 0, host : "192.168.0.34:27004" },
...         {_id : 1, host : "192.168.0.35:27004" },
...         {_id : 2, host : "192.168.0.31:27004" }
...     ]
... }


#初始化副本集配置
rs.initiate(config);

#查看分区状态
rs.status();
```


#### 配置第五个分片副本集

在服务器35、31、32上面做以下配置

配置文件

``` sh
vi /usr/local/mongodb/conf/shard5.conf

#配置文件内容
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /data/shard5/log/shard5.log
 
# Where and how to store data.
storage:
  dbPath: /data/shard5/data
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
       cacheSizeGB: 20

# how the process runs
processManagement:
  fork: true 
  pidFilePath: /data/shard5/log/shard5.pid
 
# network interfaces
net:
  port: 27005
  bindIp: 192.168.0.35

 
#operationProfiling:
replication:
    replSetName: shard5
sharding:
    clusterRole: shardsvr
```

启动三台服务器的shard5 server

``` sh
numactl --interleave=all mongod  --config  /usr/local/mongodb/conf/shard5.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo 192.168.0.35:27005
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard5",
...     members : [
...         {_id : 0, host : "192.168.0.35:27005" },
...         {_id : 1, host : "192.168.0.31:27005" },
...         {_id : 2, host : "192.168.0.32:27005" }
...     ]
... }


#初始化副本集配置
rs.initiate(config);

#查看分区状态
rs.status();
```

*至此，五个分片和副本集搭建完毕*


### 3、配置路由服务器 mongos


以下配置在服务器31、32上执行

> 注意：先启动配置服务器和分片服务器,后启动路由实例

``` sh
vi /usr/local/mongodb/conf/mongos.conf

systemLog:
  destination: file
  logAppend: true
  path: /data/mongos/log/mongos.log
processManagement:
  fork: true
#  pidFilePath: /usr/local/mongodb/mongos.pid
 
# network interfaces
net:
  port: 20000
  bindIp: 192.168.0.31
#监听的配置服务器,只能有1个或者3个 configs为配置服务器的副本集名字
sharding:
   configDB: configs/192.168.0.33:21000,192.168.0.34:21000,192.168.0.35:21000
```

启动二台服务器的mongos server

``` sh
mongos  --config  /usr/local/mongodb/conf/mongos.conf
```


### 4、启用分片


目前搭建了mongodb配置服务器、路由服务器，各个分片服务器，不过应用程序连接到mongos路由服务器并不能使用分片机制，还需要在程序里设置分片配置，让分片生效。

登陆任意一台mongos

``` sh
mongo 192.168.0.31:20000
#使用admin数据库
use  admin
#串联路由服务器与分配副本集
sh.addShard("shard1/192.168.0.31:27001,192.168.0.32:27001,192.168.0.33:27001")
sh.addShard("shard2/192.168.0.32:27002,192.168.0.33:27002,192.168.0.34:27002")
sh.addShard("shard3/192.168.0.33:27003,192.168.0.34:27003,192.168.0.35:27003")
sh.addShard("shard4/192.168.0.34:27004,192.168.0.35:27004,192.168.0.31:27004")
sh.addShard("shard5/192.168.0.35:27005,192.168.0.31:27005,192.168.0.32:27005")
#查看集群状态
sh.status()
```

这样mongodb的五台集群搭建就已经完成了，后期如何优化和运营请查看下一篇文章。


## 错误

### rs.initiate报错

执行 rs.initiate(config); 报错：

``` sh
rs.initiate(config);
{
        "ok" : 0,
        "errmsg" : "No host described in new configuration 1 for replica set shard1 maps to this node",
        "code" : 93,
        "codeName" : "InvalidReplicaSetConfig"
}
```

最后发现是自己的一个端口号写错了。


###  启动mongos报错

启动mongos的时候报错：

``` sh
about to fork child process, waiting until server is ready for connections.
forked process: 1436
ERROR: child process failed, exited with error number 1
```

这个问题卡了我们半天，找了很多的资料，不是说清理lock文件，就是说清理log文件总无解，最后看到这个网站的提示

[ERROR: child process failed, exited with error number 1](http://www.kriblog.com/bigdata/NoSQL/MongoDb/error-child-process-failed-exited-with-error-number-1.html)

去掉了配置文件中  --fork，才将真正的错误日志打印了出来，是我们的配置文件中的路径写错了，本来是log写成了logs

原来：```path: /data/logs/mongos.log```

改为：```path: /data/log/mongos.log```

成功


> 为了方便大家拿取配置文件，我在github上面放置了一份:[mongodb-five-cluster-conf](https://github.com/ityouknow/hadoop-ecosystem-examples/tree/master/mongodb/mongodb-five-cluster-conf)