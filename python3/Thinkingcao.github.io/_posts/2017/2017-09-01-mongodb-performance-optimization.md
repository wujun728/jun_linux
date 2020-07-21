---
layout: post
title: mongodb集群性能优化
category: mongodb
tags: [mongodb]
---

在前面两篇文章，我们介绍了如何去搭建mongodb集群，这篇文章我们将介绍如何去优化mongodb的各项配置，以达到最优的效果。

## 警告

不做任何的优化，集群搭建完成之后，使用命令连接mongodb终端，一般会遇到以下的警告信息：  
>如何你是用的是我最新一版集群搭建的脚本，估计警告会少几个，因为里面已经做了一些优化

``` sh
2017-08-16T18:33:42.985+0800 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2017-08-16T18:33:42.985+0800 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2017-08-16T18:33:43.024+0800 I CONTROL  [initandlisten] 
2017-08-16T18:33:43.024+0800 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2017-08-16T18:33:43.024+0800 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2017-08-16T18:33:43.024+0800 I CONTROL  [initandlisten] 
2017-08-16T18:33:43.025+0800 I CONTROL  [initandlisten] 
2017-08-16T18:33:43.025+0800 I CONTROL  [initandlisten] ** WARNING: You are running on a NUMA machine.
2017-08-16T18:33:43.025+0800 I CONTROL  [initandlisten] **          We suggest launching mongod like this to avoid performance problems:
2017-08-16T18:33:43.025+0800 I CONTROL  [initandlisten] **              numactl --interleave=all mongod [other options]
2017-08-16T18:33:43.026+0800 I CONTROL  [initandlisten] 
2017-08-16T18:33:43.026+0800 I CONTROL  [initandlisten] ** WARNING: /proc/sys/vm/zone_reclaim_mode is 1
2017-08-16T18:33:43.026+0800 I CONTROL  [initandlisten] **          We suggest setting it to 0
2017-08-16T18:33:43.026+0800 I CONTROL  [initandlisten] **          http://www.kernel.org/doc/Documentation/sysctl/vm.txt
2017-08-16T18:33:43.026+0800 I CONTROL  [initandlisten] 
2017-08-16T18:33:43.027+0800 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/enabled is 'always'.
2017-08-16T18:33:43.027+0800 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2017-08-16T18:33:43.027+0800 I CONTROL  [initandlisten] 
2017-08-16T18:33:43.027+0800 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/defrag is 'always'.
2017-08-16T18:33:43.027+0800 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2017-08-16T18:33:43.027+0800 I CONTROL  [initandlisten] 
```

这其实是六条建议，下来我们分别来进行解读；

第一条，“Using the XFS filesystem is strongly recommended with the WiredTiger storage engine” ，意思就是强烈建议启用XFS文件系统，启用XFS文件系统会对性能有比较好的提升，我们使用的系统是centos6.9，重新格式化磁盘就可以。

具体如何格式成XFS文件系统，请参考这篇文章：[centos6构建XFS文件系统](http://blog.csdn.net/xiegh2014/article/details/52687734)

第二条，“Access control is not enabled for the database. Read and write access to data and configuration is unrestricted.”，就是说数据安全很重要，该配置管理员账户、密码、权限的就赶紧配上。

如何去配置呢，参考官方文档吧：[Re-start the MongoDB instance with access control.](https://docs.mongodb.com/master/tutorial/enable-authentication/#re-start-the-mongodb-instance-with-access-controls)

第三条，“ You are running on a NUMA machine.We suggest launching mongod like this to avoid，numactl --interleave=all mongod [other options]”，我们运行的服务器CPU架构是MUMA，因此建议启动的时候加一些参数，可以提高性能，怎么加呢，看下面的命令，想多了解一些可以参考这篇文章：[Mongodb NUMA 导致的性能问题](http://zhangliyong.github.io/posts/2014/04/09/mongodb-numa-dao-zhi-de-xing-neng-wen-ti.html)

``` sh
numactl --interleave=all mongod [other options]
```

第四条，“/proc/sys/vm/zone_reclaim_mode is 1，We suggest setting it to 0”，就是系统的这个值现在是1，请修改为0

``` sh
echo 0 > /proc/sys/vm/zone_reclaim_mode
```

第五条，"sys/kernel/mm/transparent_hugepage/enabled is，We suggest setting it to 'never'"，建议修改将配置I为”never“

``` sh
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

第六条，”/sys/kernel/mm/transparent_hugepage/defrag is，We suggest setting it to 'never'“，和上面基本相似。

``` sh
echo never > /sys/kernel/mm/transparent_hugepage/defrag
```


##  写测试


生产使用了5台服务器，五个分片，每个分片两个副本集，服务器内存128G，CPU 20核，硬盘3T 做完raid10之后，数据目录data大概是2.1T的空间。

搭建完成时候迫不及待的进行了压测，启动了10个线程每个线程1万数据，没有启动分片的勤快下，大概用了8分钟。启用分片之后，进行测试启动了100个线程，每个线程插入100万的时候，平均每秒插入速度8000。第二天过来的时候发现分片5节点挂了，报错如下：


项目报错：

``` sh
Caused by: com.mongodb.WriteConcernException: Write failed with error code 83 and error message 'write results unavailable from 192.168.0.35:27005 :: caused by :: Location11002: socket exception [CONNECT_ERROR] for 192.168.0.35:27005'
```

mongos错误信息：

``` sh
 Failed to connect to 192.168.0.35:27005, in(checking socket for error after poll), reason: Connection refused

 No primary detected for set shard5
```

 congfig 报错：

``` sh
 No primary detected for set shard5
2017-08-21T11:08:22.709+0800 W NETWORK  [Balancer] Failed to connect to 192.168.0.31:27005, in(checking socket for error after poll), reason: Connection refused
2017-08-21T11:08:22.710+0800 W NETWORK  [Balancer] Failed to connect to 192.168.0.35:27005, in(checking socket for error after poll), reason: Connection refused
2017-08-21T11:08:22.710+0800 W NETWORK  [Balancer] No primary detected for set shard5
2017-08-21T11:08:22.710+0800 I SHARDING [Balancer] caught exception while doing balance: could not find host matching read preference { mode: "primary" } for set shard5
2017-08-21T11:08:22.710+0800 I SHARDING [Balancer] about to log metadata event into actionlog: { _id: "mongodb34.hkrt.cn-2017-08-21T11:08:22.710+0800-599a4ea698ec442a0836e2d5", server: "mongodb34.hkrt.cn", clientAddr: "", time: new Date(1503284902710), what: "balancer.round", ns: "", details: { executionTimeMillis: 20051, errorOccured: true, errmsg: "could not find host matching read preference { mode: "primary" } for set shard5" } }
```

剩余分片（192.168.0.32）报错：

``` sh
not master and slaveOk=false
could not find host matching read preference { mode: "primary" } for set shard5
```


同时查看五台服务器内存，全部被使用完了，重新启动分片5之后，查看数据只插入了3000万条，就崩了；启动万之后，在进行了10万数据的压测，结果分片三又蹦了。

看了mongodb的官方文档，猜测大概是内存配置的问题。找到这一句：


``` sh
storage.wiredTiger.engineConfig.cacheSizeGB

Type: float

The maximum size of the internal cache that WiredTiger will use for all data.

Changed in version 3.4: Values can range from 256MB to 10TB and can be a float. In addition, the default value has also changed.

Starting in 3.4, the WiredTiger internal cache, by default, will use the larger of either:

50% of RAM minus 1 GB, or
256 MB.
Avoid increasing the WiredTiger internal cache size above its default value.

With WiredTiger, MongoDB utilizes both the WiredTiger internal cache and the filesystem cache.

Via the filesystem cache, MongoDB automatically uses all free memory that is not used by the WiredTiger cache or by other processes. Data in the filesystem cache is compressed.

*NOTE*
*The storage.wiredTiger.engineConfig.cacheSizeGB limits the size of the WiredTiger internal cache. The operating system will use the available free memory for filesystem cache, which allows the compressed MongoDB data files to stay in memory. In addition, the operating system will use any free RAM to buffer file system blocks and file system cache.*

*To accommodate the additional consumers of RAM, you may have to decrease WiredTiger internal cache size.*


The default WiredTiger internal cache size value assumes that there is a single mongod instance per machine. If a single machine contains multiple MongoDB instances, then you should decrease the setting to accommodate the other mongod instances.

If you run mongod in a container (e.g. lxc, cgroups, Docker, etc.) that does not have access to all of the RAM available in a system, you must set storage.wiredTiger.engineConfig.cacheSizeGB to a value less than the amount of RAM available in the container. The exact amount depends on the other processes running in the container.
```

[原文地址](https://docs.mongodb.com/manual/reference/configuration-options/index.html)


大概意思就是，分配的缓存默认会使用内存的一半减去1G,如果部署多个实例的时候应该相应的减少缓存大小的配置。

如果不设置的话，128G的内存，每个分片的实例使用内存的大小是63G,三个分片的使用的大小是189G远远超出内存128G，导致内存使用过量分片down掉。


看到这块的时候，感觉mongodb还是不够智能，为什么不会根据实例的多少动态平衡呢非要把内容打满down掉，随后我们调整了每天实例使用内存的大小，设置如下：

分片的启动参数中添加以下配置：

``` sh
storage:
  wiredTiger:
    engineConfig:
       cacheSizeGB: 20
```

每台实例的大小设置为20G。

可以使用mongostat命令来查看每个分片使用内存的大小。

第二天再次进行了压测，100个线程每个线程插入100万，1亿数据入库，正常，插入的速度，8000/s,高峰期间可以达到2万/s。


## 查询测试


以下为我在生产中的测试记录

100万数据 分页查询list count 秒出 ， agg聚合 3秒

1000万数据  分页查询 list  count 秒出 ，  agg 聚合 14秒

6000万数据  分页查询  list秒出  count 1秒时间  agg聚合时间  第一次 4分钟 第二次 1分钟24秒

6000万数据  条件分页查询  list秒出  count 40秒时间  agg聚合时间 2分11秒

1亿 分页查询  list  count 10秒时间  agg聚合时间 3分

1亿4000万数据  分页查询  list秒出  count 秒出  agg聚合时间 2分11秒

3亿数据  分页查询  list 1  count 1秒  agg聚合时间 30分

3亿数据  条件分页查询  list 1  count 3分钟  agg聚合时间 18分钟


插入测试：13:35分开始 1亿条 每秒插入速度2000-3000 预计12-13小时左右，实际用时30小时。



4亿数据  分页查询  list 1  count 1秒     agg聚合时间 45分

4亿数据  条件分页查询  list 1秒  count 6分钟  agg聚合时间 48分钟
