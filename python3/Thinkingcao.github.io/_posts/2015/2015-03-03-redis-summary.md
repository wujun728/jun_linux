---
layout: post
title: redis使用总结
category: redis
tags: [redis]
---

Redis是目前业界使用最广泛的内存数据存储。相比memcached，Redis支持更丰富的数据结构，例如hashes, lists, sets等，同时支持数据持久化。除此之外，Redis还提供一些类数据库的特性，比如事务，HA，主从库。可以说Redis兼具了缓存系统和数据库的一些特性，因此有着丰富的应用场景。本文介绍Redis在Spring Boot中两个典型的应用场景。


## 运营命令

1、启动redis
> src/redis-server &

2、关闭redis
> src/redis-cli shutdown

3、连接
> telnet localhost 6379


## 诊断命令

1、查看基本信息
>  INFO

2、查看缓存键 
> keys '*'

3、查看key的类型
> type yourkey

## 操作命令
1、插入命令
> set key yy

2、获取命令
> get key

2、清空所有数据
> FLUSHALL 

## 配置命令

1、添加日志
> vim redis.conf
> logfile /data/redis_cache/logs/redis.log #日志路径
