---
layout: post
title: mongodb 3.4 集群搭建：分片+副本集
category: mongodb
tags: [mongodb]
---

mongodb是最常用的nosql数据库，在数据库排名中已经上升到了前六。这篇文章介绍如何搭建高可用的mongodb（分片+副本）集群。

在搭建集群之前，需要首先了解几个概念：路由，分片、副本集、配置服务器等。

## 相关概念

先来看一张图：

 
![](http://www.itmind.net/assets/images/2017/bigdata/sharded-cluster-production-architecture.bakedsvg.svg)

从图中可以看到有四个组件：mongos、config server、shard、replica set。

mongos，数据库集群请求的入口，所有的请求都通过mongos进行协调，不需要在应用程序添加一个路由选择器，mongos自己就是一个请求分发中心，它负责把对应的数据请求请求转发到对应的shard服务器上。在生产环境通常有多mongos作为请求的入口，防止其中一个挂掉所有的mongodb请求都没有办法操作。

config server，顾名思义为配置服务器，存储所有数据库元信息（路由、分片）的配置。mongos本身没有物理存储分片服务器和数据路由信息，只是缓存在内存里，配置服务器则实际存储这些数据。mongos第一次启动或者关掉重启就会从 config server 加载配置信息，以后如果配置服务器信息变化会通知到所有的 mongos 更新自己的状态，这样 mongos 就能继续准确路由。在生产环境通常有多个 config server 配置服务器，因为它存储了分片路由的元数据，防止数据丢失！

shard，分片（sharding）是指将数据库拆分，将其分散在不同的机器上的过程。将数据分散到不同的机器上，不需要功能强大的服务器就可以存储更多的数据和处理更大的负载。基本思想就是将集合切成小块，这些块分散到若干片里，每个片只负责总数据的一部分，最后通过一个均衡器来对各个分片进行均衡（数据迁移）。

replica set，中文翻译副本集，其实就是shard的备份，防止shard挂掉之后数据丢失。复制提供了数据的冗余备份，并在多个服务器上存储数据副本，提高了数据的可用性， 并可以保证数据的安全性。

仲裁者（Arbiter），是复制集中的一个MongoDB实例，它并不保存数据。仲裁节点使用最小的资源并且不要求硬件设备，不能将Arbiter部署在同一个数据集节点中，可以部署在其他应用服务器或者监视服务器中，也可部署在单独的虚拟机中。为了确保复制集中有奇数的投票成员（包括primary），需要添加仲裁节点做为投票，否则primary不能运行时不会自动切换primary。

简单了解之后，我们可以这样总结一下，应用请求mongos来操作mongodb的增删改查，配置服务器存储数据库元信息，并且和mongos做同步，数据最终存入在shard（分片）上，为了防止数据丢失同步在副本集中存储了一份，仲裁在数据存储到分片的时候决定存储到哪个节点。


## 环境准备

系统系统 centos6.5        
三台服务器：192.168.0.75/84/86   
安装包： mongodb-linux-x86_64-3.4.6.tgz  

服务器规划

服务器75	| 服务器84	| 服务器86
---     |---        |---
mongos | mongos |  mongos  
config server|config server|config server
shard server1 主节点 |shard server1 副节点|  shard server1 仲裁
shard server2 仲裁 |shard server2 主节点|  shard server2 副节点
shard server3 副节点  |shard server3 仲裁 |  shard server3 主节点

端口分配：

``` properties
mongos：20000
config：21000
shard1：27001
shard2：27002
shard3：27003
```

## 集群搭建

### 1、安装mongodb

``` sh
#解压
tar -xzvf mongodb-linux-x86_64-3.4.6.tgz -C /usr/local/
#改名
mv mongodb-linux-x86_64-3.4.6 mongodb
```

分别在每台机器建立conf、mongos、config、shard1、shard2、shard3六个目录，因为mongos不存储数据，只需要建立日志文件目录即可。

``` sh
mkdir -p /usr/local/mongodb/conf
mkdir -p /usr/local/mongodb/mongos/log
mkdir -p /usr/local/mongodb/config/data
mkdir -p /usr/local/mongodb/config/log
mkdir -p /usr/local/mongodb/shard1/data
mkdir -p /usr/local/mongodb/shard1/log
mkdir -p /usr/local/mongodb/shard2/data
mkdir -p /usr/local/mongodb/shard2/log
mkdir -p /usr/local/mongodb/shard3/data
mkdir -p /usr/local/mongodb/shard3/log
```

配置环境变量

``` sh
vim /etc/profile
# 内容
export MONGODB_HOME=/usr/local/mongodb
export PATH=$MONGODB_HOME/bin:$PATH
# 使立即生效
source /etc/profile
```

### 2、config server配置服务器

mongodb3.4以后要求配置服务器也创建副本集，不然集群搭建不成功。

添加配置文件

``` sh
vi /usr/local/mongodb/conf/config.conf

## 配置文件内容
pidfilepath = /usr/local/mongodb/config/log/configsrv.pid
dbpath = /usr/local/mongodb/config/data
logpath = /usr/local/mongodb/config/log/congigsrv.log
logappend = true
 
bind_ip = 0.0.0.0
port = 21000
fork = true
 
#declare this is a config db of a cluster;
configsvr = true

#副本集名称
replSet=configs
 
#设置最大连接数
maxConns=20000
```

启动三台服务器的config server

``` sh
mongod -f /usr/local/mongodb/conf/config.conf
```

登录任意一台配置服务器，初始化配置副本集

``` sh
#连接
mongo --port 21000
#config变量
config = {
...    _id : "configs",
...     members : [
...         {_id : 0, host : "192.168.0.75:21000" },
...         {_id : 1, host : "192.168.0.84:21000" },
...         {_id : 2, host : "192.168.0.86:21000" }
...     ]
... }

#初始化副本集
rs.initiate(config)
```

其中，"_id" : "configs"应与配置文件中配置的 replicaction.replSetName 一致，"members" 中的 "host" 为三个节点的 ip 和 port

### 3、配置分片副本集(三台机器)

**设置第一个分片副本集**

配置文件

``` sh
vi /usr/local/mongodb/conf/shard1.conf

#配置文件内容
#——————————————–
pidfilepath = /usr/local/mongodb/shard1/log/shard1.pid
dbpath = /usr/local/mongodb/shard1/data
logpath = /usr/local/mongodb/shard1/log/shard1.log
logappend = true

bind_ip = 0.0.0.0
port = 27001
fork = true
 
#打开web监控
httpinterface=true
rest=true
 
#副本集名称
replSet=shard1
 
#declare this is a shard db of a cluster;
shardsvr = true
 
#设置最大连接数
maxConns=20000
```

启动三台服务器的shard1 server

``` sh
mongod -f /usr/local/mongodb/conf/shard1.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo --port 27001
#使用admin数据库
use admin
#定义副本集配置，第三个节点的 "arbiterOnly":true 代表其为仲裁节点。
config = {
...    _id : "shard1",
...     members : [
...         {_id : 0, host : "192.168.0.75:27001" },
...         {_id : 1, host : "192.168.0.84:27001" },
...         {_id : 2, host : "192.168.0.86:27001” , arbiterOnly: true }
...     ]
... }
#初始化副本集配置
rs.initiate(config);
```

**设置第二个分片副本集**

配置文件

``` sh
vi /usr/local/mongodb/conf/shard2.conf

#配置文件内容
#——————————————–
pidfilepath = /usr/local/mongodb/shard2/log/shard2.pid
dbpath = /usr/local/mongodb/shard2/data
logpath = /usr/local/mongodb/shard2/log/shard2.log
logappend = true

bind_ip = 0.0.0.0
port = 27002
fork = true
 
#打开web监控
httpinterface=true
rest=true
 
#副本集名称
replSet=shard2
 
#declare this is a shard db of a cluster;
shardsvr = true
 
#设置最大连接数
maxConns=20000
```

启动三台服务器的shard2 server

``` sh
mongod -f /usr/local/mongodb/conf/shard2.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo --port 27002
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard2",
...     members : [
...         {_id : 0, host : "192.168.0.75:27002"  , arbiterOnly: true },
...         {_id : 1, host : "192.168.0.84:27002" },
...         {_id : 2, host : "192.168.0.86:27002" }
...     ]
... }

#初始化副本集配置
rs.initiate(config);
```

**设置第三个分片副本集**

配置文件

``` sh
vi /usr/local/mongodb/conf/shard3.conf

#配置文件内容
#——————————————–
pidfilepath = /usr/local/mongodb/shard3/log/shard3.pid
dbpath = /usr/local/mongodb/shard3/data
logpath = /usr/local/mongodb/shard3/log/shard3.log
logappend = true

bind_ip = 0.0.0.0
port = 27003
fork = true
 
#打开web监控
httpinterface=true
rest=true
 
#副本集名称
replSet=shard3
 
#declare this is a shard db of a cluster;
shardsvr = true
 
#设置最大连接数
maxConns=20000
```

启动三台服务器的shard3 server

``` sh
mongod -f /usr/local/mongodb/conf/shard3.conf
```

登陆任意一台服务器，初始化副本集

``` sh
mongo --port 27003
#使用admin数据库
use admin
#定义副本集配置
config = {
...    _id : "shard3",
...     members : [
...         {_id : 0, host : "192.168.0.75:27003" },
...         {_id : 1, host : "192.168.0.84:27003" , arbiterOnly: true},
...         {_id : 2, host : "192.168.0.86:27003" }
...     ]
... }

#初始化副本集配置
rs.initiate(config);
```

### 4、配置路由服务器 mongos

先启动配置服务器和分片服务器,后启动路由实例:（三台机器）

``` sh
vi /usr/local/mongodb/conf/mongos.conf

#内容
pidfilepath = /usr/local/mongodb/mongos/log/mongos.pid
logpath = /usr/local/mongodb/mongos/log/mongos.log
logappend = true

bind_ip = 0.0.0.0
port = 20000
fork = true

#监听的配置服务器,只能有1个或者3个 configs为配置服务器的副本集名字
configdb = configs/192.168.0.75:21000,192.168.0.84:21000,192.168.0.86:21000
 
#设置最大连接数
maxConns=20000
```

启动三台服务器的mongos server

``` sh
mongos -f /usr/local/mongodb/conf/mongos.conf
```

### 5、启用分片

目前搭建了mongodb配置服务器、路由服务器，各个分片服务器，不过应用程序连接到mongos路由服务器并不能使用分片机制，还需要在程序里设置分片配置，让分片生效。

登陆任意一台mongos

``` sh
mongo --port 20000
#使用admin数据库
use  admin
#串联路由服务器与分配副本集
sh.addShard("shard1/192.168.0.75:27001,192.168.0.84:27001,192.168.0.86:27001")
sh.addShard("shard2/192.168.0.75:27002,192.168.0.84:27002,192.168.0.86:27002")
sh.addShard("shard3/192.168.0.75:27003,192.168.0.84:27003,192.168.0.86:27003")
#查看集群状态
sh.status()
```

### 6、测试

目前配置服务、路由服务、分片服务、副本集服务都已经串联起来了，但我们的目的是希望插入数据，数据能够自动分片。连接在mongos上，准备让指定的数据库、指定的集合分片生效。

``` sh
#指定testdb分片生效
db.runCommand( { enablesharding :"testdb"});
#指定数据库里需要分片的集合和片键
db.runCommand( { shardcollection : "testdb.table1",key : {id: 1} } )
```
我们设置testdb的 table1 表需要分片，根据 id 自动分片到 shard1 ，shard2，shard3 上面去。要这样设置是因为不是所有mongodb 的数据库和表 都需要分片！

测试分片配置结果

``` sh
mongo  127.0.0.1:20000
#使用testdb
use  testdb;
#插入测试数据
for (var i = 1; i <= 100000; i++)
db.table1.save({id:i,"test1":"testval1"});
#查看分片情况如下，部分无关信息省掉了
db.table1.stats();

{
        "sharded" : true,
        "ns" : "testdb.table1",
        "count" : 100000,
        "numExtents" : 13,
        "size" : 5600000,
        "storageSize" : 22372352,
        "totalIndexSize" : 6213760,
        "indexSizes" : {
                "_id_" : 3335808,
                "id_1" : 2877952
        },
        "avgObjSize" : 56,
        "nindexes" : 2,
        "nchunks" : 3,
        "shards" : {
                "shard1" : {
                        "ns" : "testdb.table1",
                        "count" : 42183,
                        "size" : 0,
                        ...
                        "ok" : 1
                },
                "shard2" : {
                        "ns" : "testdb.table1",
                        "count" : 38937,
                        "size" : 2180472,
                        ...
                        "ok" : 1
                },
                "shard3" : {
                        "ns" : "testdb.table1",
                        "count" :18880,
                        "size" : 3419528,
                        ...
                        "ok" : 1
                }
        },
        "ok" : 1
}
```

可以看到数据分到3个分片，各自分片数量为： shard1 “count” : 42183，shard2 “count” : 38937，shard3 “count” : 18880。已经成功了！


## 后期运维

### 启动关闭

mongodb的启动顺序是，先启动配置服务器，在启动分片，最后启动mongos.

``` sh
mongod -f /usr/local/mongodb/conf/config.conf
mongod -f /usr/local/mongodb/conf/shard1.conf
mongod -f /usr/local/mongodb/conf/shard2.conf
mongod -f /usr/local/mongodb/conf/shard3.conf
mongod -f /usr/local/mongodb/conf/mongos.conf
```

关闭时，直接killall杀掉所有进程

``` sh
killall mongod
killall mongos
```

参考：

[搭建高可用mongodb集群（四）—— 分片](http://www.lanceyan.com/category/tech/mongodb)  
[MongoDB3.4副本集分片集群搭建](https://zhuanlan.zhihu.com/p/25594963)  
[Mongodb高可用集群（四）——分片](http://www.xiamujun.cn/forum.php?mod=viewthread&tid=373)



