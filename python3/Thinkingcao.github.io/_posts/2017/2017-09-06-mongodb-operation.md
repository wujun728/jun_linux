---
layout: post
title: mongodb集群监控和运维
category: mongodb
tags: [mongodb]
---

这篇文件介绍如何动态的添加、下架mongod分片和副本集，以及如何监控和运维mongodb。

## 添加节点

### 副本集 改为仲裁节点

[convert-secondary-into-arbiter](https://docs.mongodb.com/manual/tutorial/convert-secondary-into-arbiter/)

登录

``` sh
mongo 192.168.0.35:27005
#使用admin数据库
use admin
```

``` sh
#查看分区状态
rs.status();
```

移除副本集

``` sh
rs.remove("192.168.0.35:27005")
```

查看配置

``` sh
rs.conf()
```

删除shard5的数据目录，重启shard5

重新添加仲裁节点

``` sh
rs.addArb("192.168.0.35:27005")
```

查看配置

``` sh
rs.conf()
```


### 仲裁节点改成副本集

[Add Members to a Replica Set](https://docs.mongodb.com/manual/tutorial/expand-replica-set/)

移除仲裁节点

``` sh
rs.remove("192.168.0.35:27005")
```

删除总裁节点的数据，并重启


在 primary 添加副本节点

``` sh
rs.add("192.168.0.35:27005")
```

``` sh
rs.conf()
rs.status();
```

刚添加的副本集状态为：STARTUP2

``` sh
"stateStr" : "STARTUP2",
```

## 集群中添加分片


``` sh
mongo 192.168.0.31:20000
#使用admin数据库
use  admin
#添加分片
sh.addShard("shard5/192.168.0.35:27005,192.168.0.31:27005,192.168.0.32:27005")
#查看集群状态
sh.status()
```


## 监控

###  mongostat 

mongostat是mongdb自带的状态检测工具，在命令行下使用。它会间隔固定时间获取mongodb的当前运行状态，并输出。如果你发现数据库突然变慢或者有其他问题的话，你第一手的操作就考虑采用mongostat来查看mongo的状态。


它的输出有以下几列：

- inserts/s 每秒插入次数
- query/s 每秒查询次数
- update/s 每秒更新次数
- delete/s 每秒删除次数
- getmore/s 每秒执行getmore次数
- command/s 每秒的命令数，比以上插入、查找、更新、删除的综合还多，还统计了别的命令
- flushs/s 每秒执行fsync将数据写入硬盘的次数。
- mapped/s 所有的被mmap的数据量，单位是MB，
- vsize 虚拟内存使用量，单位MB
- res 物理内存使用量，单位MB
- faults/s 每秒访问失败数（只有Linux有），数据被交换出物理内存，放到swap。不要超过100，否则就是机器内存太小，造成频繁swap写入。此时要升级内存或者扩展
- locked % 被锁的时间百分比，尽量控制在50%以下吧
- idx miss % 索引不命中所占百分比。如果太高的话就要考虑索引是不是少了
- ```q t|r|w``` 当Mongodb接收到太多的命令而数据库被锁住无法执行完成，它会将命令加入队列。这一栏显示了总共、读、写3个队列的长度，都为0的话表示mongo毫无压力。高并发时，一般队列值会升高。
- conn 当前连接数
- time 时间戳

示例：

``` sh
mongostat -h 192.168.0.31:27001
##返回结果
insert query update delete getmore command dirty  used flushes vsize   res qrw arw net_in net_out conn    set repl                time
   576    *0     *0     *0     455  1370|0  2.7% 64.0%       0 15.8G 13.9G 0|1 0|0  1.82m   1.44m   77 shard1  PRI Aug 23 17:05:25.495
   514    *0     *0     *0     446  1336|0  2.7% 64.0%       0 15.8G 13.9G 0|1 0|0  1.71m   1.29m   77 shard1  PRI Aug 23 17:05:26.495
   499    *0     *0     *0     461  1310|0  2.7% 64.0%       0 15.8G 13.9G 0|0 1|0  1.68m   1.27m   77 shard1  PRI Aug 23 17:05:27.495
   485    *0     *0     *0     442  1285|0  2.7% 64.0%       0 15.8G 13.9G 0|0 0|1  1.64m   1.24m   77 shard1  PRI Aug 23 17:05:28.496
   498    *0     *0     *0     444  1317|0  2.7% 64.0%       0 15.8G 13.9G 0|0 0|0  1.68m   1.26m   77 shard1  PRI Aug 23 17:05:29.494
   477    *0     *0     *0     445  1272|0  2.7% 64.0%       0 15.8G 13.9G 0|0 0|0  1.61m   1.22m   77 shard1  PRI Aug 23 17:05:30.494
```

mongostat间隔时间刷新mongodb分片的各项操作。

## mongotop

mongotop用来跟踪MongoDB的实例， 提供每个集合的统计数据。默认情况下，mongotop每一秒刷新一次。
mongotop用法：

``` sh
mongotop -h 192.168.0.31:27001 10
```

后面的10是<sleeptime>参数 ，可以不使用，等待的时间长度，以秒为单位，mongotop等待调用之间。通过的默认mongotop返回数据的每一秒。


mongotop --locks
报告每个数据库的锁的使用中，使用mongotop - 锁，这将产生以下输出：

结果字段介绍：
ns：包含数据库命名空间，后者结合了数据库名称和集合。
db：包含数据库的名称。名为 . 的数据库针对全局锁定，而非特定数据库。
total：mongod花费的时间工作在这个命名空间提供总额。
read：提供了大量的时间，这mongod花费在执行读操作，在此命名空间。
write：提供这个命名空间进行写操作，这mongod花了大量的时间。



### profiler

类似于MySQL的slow log, MongoDB可以监控所有慢的以及不慢的查询。

Profiler默认是关闭的，你可以选择全部开启，或者有慢查询的时候开启。

``` sh
> use test
switched to db test
> db.setProfilingLevel(2);
{"was" : 0 , "slowms" : 100, "ok" : 1} // "was" is the old setting
> db.getProfilingLevel()
```

查看Profile日志

``` sh
> db.system.profile.find().sort({$natural:-1})
{"ts" : "Thu Jan 29 2009 15:19:32 GMT-0500 (EST)" , "info" :
"query test.$cmd ntoreturn:1 reslen:66 nscanned:0 query: { profile: 2 } nreturned:1 bytes:50" ,
"millis" : 0} ...
```

``` sh
#查看系统中的慢查询数量
db.system.profile.count();
```

3个字段的意义

- ts：时间戳
- info：具体的操作
- millis：操作所花时间，毫秒

参考：[Database Profiler](https://docs.mongodb.com/manual/tutorial/manage-the-database-profiler/)

注意，造成满查询可能是索引的问题，也可能是数据不在内存造成因此磁盘读入造成。


### db.serverStatus()

db.serverStatus()

获取服务器的状态

``` sh
{
        "host" : "mongodb31.hkrt.cn:20000",
        "version" : "3.4.6",
        "process" : "mongos",
        "pid" : NumberLong(1940),
        "uptime" : 67854,
        "uptimeMillis" : NumberLong(67853593),
        "uptimeEstimate" : NumberLong(67853),
        "localTime" : ISODate("2017-08-23T09:39:55.400Z"),
        "asserts" : {
                "regular" : 0,
                "warning" : 0,
                "msg" : 0,
                "user" : 7048,
                "rollovers" : 0
        },
        "connections" : {
                "current" : 56,
                "available" : 52372,
                "totalCreated" : 523
        },
        "extra_info" : {
                "note" : "fields vary by platform",
                "page_faults" : 3
        },
        "network" : {
                "bytesIn" : NumberLong("102972729600"),
                "bytesOut" : NumberLong("7551683898"),
                "physicalBytesIn" : NumberLong("102972729600"),
                "physicalBytesOut" : NumberLong("7551683898"),
                "numRequests" : NumberLong(210803831)
        },
        "opcounters" : {
                "insert" : 79028505,
                "query" : 26334341,
                "update" : 0,
                "delete" : 4,
                "getmore" : 0,
                "command" : 79067537
        },
        "sharding" : {
                "configsvrConnectionString" : "config/192.168.0.33:21000,192.168.0.34:21000,192.168.0.35:21000",
                "lastSeenConfigServerOpTime" : {
                        "ts" : Timestamp(1503481193, 1),
                        "t" : NumberLong(1)
                }
        },
        "tcmalloc" : {
                "generic" : {
                        "current_allocated_bytes" : 3643648,
                        "heap_size" : 40898560
                },
                "tcmalloc" : {
                        "pageheap_free_bytes" : 36864,
                        "pageheap_unmapped_bytes" : 24522752,
                        "max_total_thread_cache_bytes" : NumberLong(1073741824),
                        "current_total_thread_cache_bytes" : 4660344,
                        "total_free_bytes" : 12695296,
                        "central_cache_free_bytes" : 2833608,
                        "transfer_cache_free_bytes" : 5201344,
                        "thread_cache_free_bytes" : 4660344,
                        "aggressive_memory_decommit" : 0,
                        "formattedString" : "------------------------------------------------\nMALLOC:        3643648 (    3.5 MiB) Bytes in use by application\nMALLOC: +        36864 (    0.0 MiB) Bytes in page heap freelist\nMALLOC: +      2833608 (    2.7 MiB) Bytes in central cache freelist\nMALLOC: +      5201344 (    5.0 MiB) Bytes in transfer cache freelist\nMALLOC: +      4660344 (    4.4 MiB) Bytes in thread cache freelists\nMALLOC: +      1401024 (    1.3 MiB) Bytes in malloc metadata\nMALLOC:   ------------\nMALLOC: =     17776832 (   17.0 MiB) Actual memory used (physical + swap)\nMALLOC: +     24522752 (   23.4 MiB) Bytes released to OS (aka unmapped)\nMALLOC:   ------------\nMALLOC: =     42299584 (   40.3 MiB) Virtual address space used\nMALLOC:\nMALLOC:           1936              Spans in use\nMALLOC:            109              Thread heaps in use\nMALLOC:           4096              Tcmalloc page size\n------------------------------------------------\nCall ReleaseFreeMemory() to release freelist memory to the OS (via madvise()).\nBytes released to the OS take up virtual address space but no physical memory.\n"
                }
        },
        "mem" : {
                "bits" : 64,
                "resident" : 24,
                "virtual" : 689,
                "supported" : true
        },
        "metrics" : {
                "cursor" : {
                        "timedOut" : NumberLong(21),
                        "open" : {
                                "multiTarget" : NumberLong(0),
                                "singleTarget" : NumberLong(0),
                                "pinned" : NumberLong(0),
                                "total" : NumberLong(0)
                        }
                },
                "commands" : {
                        "aggregate" : {
                                "failed" : NumberLong(1),
                                "total" : NumberLong(16)
                        },
                        "balancerStatus" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(2)
                        },
                        "buildInfo" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(519)
                        },
                        "collStats" : {
                                "failed" : NumberLong(1),
                                "total" : NumberLong(97)
                        },
                        "count" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(12)
                        },
                        "createIndexes" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(4)
                        },
                        "currentOp" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(2)
                        },
                        "dbStats" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(4)
                        },
                        "delete" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(4)
                        },
                        "drop" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(7)
                        },
                        "dropDatabase" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(2)
                        },
                        "find" : {
                                "failed" : NumberLong(2),
                                "total" : NumberLong(26334294)
                        },
                        "getLastError" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(252)
                        },
                        "getLog" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(6)
                        },
                        "insert" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(79028505)
                        },
                        "isMaster" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(24048)
                        },
                        "listCollections" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(44)
                        },
                        "listDatabases" : {
                                "failed" : NumberLong(1),
                                "total" : NumberLong(135)
                        },
                        "ping" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(13575)
                        },
                        "profile" : {
                                "failed" : NumberLong(3),
                                "total" : NumberLong(3)
                        },
                        "replSetGetStatus" : {
                                "failed" : NumberLong(34),
                                "total" : NumberLong(34)
                        },
                        "serverStatus" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(131)
                        },
                        "whatsmyuri" : {
                                "failed" : NumberLong(0),
                                "total" : NumberLong(135)
                        }
                }
        },
        "ok" : 1
}
```

需要关心的地方：

- connections 当前连接和可用连接数，听过一个同行介绍过，mongodb最大处理到2000个连接就不行了（要根据你的机器性能和业务来设定），所以设大了没意义。设个合理值的话，到达这个值mongodb就拒绝新的连接请求，避免被太多的连接拖垮。
- indexCounters:btree:misses 索引的不命中数，和hits的比例高就要考虑索引是否正确建立。你看我的”missRatio”3.543930204420982e-7，很健康吧。所以miss率在mongostat里面也可以看
- 其他的都能自解释，也不是查看mongo健康状况的关键，就不说明了。

详细的解释参考这里：[serverStatus](https://docs.mongodb.com/manual/reference/command/serverStatus/#dbcmd.serverStatus)


### db.currentOp()

Mongodb 的命令一般很快就完成，但是在一台繁忙的机器或者有比较慢的命令时，你可以通过db.currentOp()获取当前正在执行的操作。

在没有负载的机器上，该命令基本上都是返回空的

``` sh
>  db.currentOp()
{ "inprog" : [ ] }
```

以下是一个有负载的机器上得到的返回值样例：

``` sh
{ "opid" : "shard3:466404288", "active" : false, "waitingForLock" : false, "op" : "query", "ns" : "sd.usersEmails", "query" : { }, "client_s" : "10.121.13.8:34473", "desc" : "conn" },
```

字段名字都能自解释。如果你发现一个操作太长，把数据库卡死的话，可以用这个命令杀死他

``` sh
> db.killOp("shard3:466404288")
```

[db.currentOp()](https://docs.mongodb.com/manual/reference/method/db.currentOp/index.html)

