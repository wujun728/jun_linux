微云（可快速扩充）
====================

数据采集-介绍
---------------------

高可靠的，分布式的海量日志采集、聚合和传输的系统，Flume支持在日志系统中定制各类数据发送方，用于收集数据；同时，Flume提供对数据进行简
单处理，并写到各种数据接受方（可定制）的能力。

Flume提供对数据进行简单处理，并写到各种数据接受方（可定制）的能力 Flume提供了从console（控制台）、RPC（Thrift-RPC）、text（文件）、
tail（UNIX tail）、syslog（syslog日志系统，支持TCP和UDP等2种模式），exec（命令执行）等数据源上收集数据的能力。

支持采集的数据源：Avro Source、Thrift Source、Exec Source、JMS Source、Converter、Spooling Directory Source、
Twitter 1% firehose Source、Event Deserializers、LINE、BlobDeserializer、NetCat Source、Sequence Generator Source
Syslog Sources、Syslog TCP Source、Multiport Syslog TCP Source、Syslog UDP Source、HTTP Source、Legacy Sources、Scribe Source

Flume-og采用了多Master的方式。为了保证配置数据的一致性，Flume[1] 引入了ZooKeeper，用于保存配置数据，ZooKeeper本身可保证配置数据的
一致性和高可用，另外，在配置数据发生变化时，ZooKeeper可以通知Flume Master节点。Flume Master间使用gossip协议同步数据。
Flume-ng最明显的改动就是取消了集中管理配置的 Master 和 Zookeeper，变为一个纯粹的传输工具。Flume-ng另一个主要的不同点是读入数据和写
出数据现在由不同的工作线程处理（称为 Runner）。 在 Flume-og 中，读入线程同样做写出工作（除了故障重试）。如果写出慢的话（不是完全失败），
它将阻塞 Flume 接收数据的能力。这种异步的设计使读入线程可以顺畅的工作而无需关注下游的任何问题。

为了保证可扩展性，Flume采用了多Master的方式。为了保证配置数据的一致性，Flume引入了ZooKeeper，用于保存配置数据，ZooKeeper本身可保证配
置数据的一致性和高可用，另外，在配置数据发生变化时，ZooKeeper可以通知Flume Master节点。


Flume OG:Flume original generation 即Flume 0.9.x版本
Flume NG:Flume next generation ，即Flume 1.x版本
对于 Flume NG ，它摒弃了Master和zookeeper，collector也没有了，web配置台也没有了，只剩下source，sink和channel，此时一个Agent的概念包括source,channel和sink，完全由一个分布式系统变成了传输工具。


![alt text](resource/UserGuide_image00.png "Title")

(1) 可靠性

当节点出现故障时，日志能够被传送到其他节点上而不会丢失。Flume提供了三种级别的可靠性保障，从强到弱依次分别为：end-to-end（收到数据agent
首先将event写到磁盘上，当数据传送成功后，再删除；如果数据发送失败，可以重新发送。），Store on failure（这也是scribe采用的策略，当数据
接收方crash时，将数据写到本地，待恢复后，继续发送），Best effort（数据发送到接收方后，不会进行确认）。

(2) 可扩展性

Flume采用了三层架构，分别为agent，collector和storage，每一层均可以水平扩展。其中，所有agent和collector由master统一管理，这使得系统
容易监控和维护，且master允许有多个（使用ZooKeeper进行管理和负载均衡），这就避免了单点故障问题。

(3) 可管理性

所有agent和colletor由master统一管理，这使得系统便于维护。多master情况，Flume利用ZooKeeper和gossip，保证动态配置数据的一致性。用户可
以在master上查看各个数据源或者数据流执行情况，且可以对各个数据源配置和动态加载。Flume提供了web 和shell script command两种形式对数据流
进行管理。

(4) 功能可扩展性

用户可以根据需要添加自己的agent，collector或者storage。此外，Flume自带了很多组件，包括各种agent（file， syslog等），collector和
storage（file，HDFS等）。

### 常用场景1 netcat网络采集数据

> 采集网络获取数据.
>
> 存放到内存或者硬盘；硬盘顺序读写，确保高效；
>
> ## 日志输出到屏幕

### 常用场景2 exec日志采集数据

> 采集日志获取数据.
>
> 存放到内存或者硬盘；硬盘顺序读写，确保高效；
>
> ## 日志输出到屏幕

### 常用场景3 批量数据采集处理 详见mycloud(http://example.com/).

> 采集网络获取数据.
>
> 存放到内存或者硬盘；硬盘顺序读写，确保高效；
>
> ## 日志输出到kafka

### 常用场景4 实时数据采集处理 详见mykafka(http://example.com/).

> 采集网络获取数据.
>
> 存放到内存或者硬盘；硬盘顺序读写，确保高效；
>
> ## 日志输出到hbase

数据采集-运行示例
---------------------
### 构造镜像包
> 进入到当前目录
> ## fig build
### 运行
> 进入到当前目录
> ## fig up -d && fig ps
### 观察日志
> telnet 192.168.59.103 44445
>
> 输入abc
>
> fig logs base
>
> 显示abc
>
> 显示dokg.log日志信息
>
> fig logs base1
>
> ## 显示 cde

--------flume1.6增加的事项
·增加了apache kafka的sink和source两大组件
·增加了一个新的channel——kafka channel
·增加了hive的sink组件，需要hive streaming的支持
·端到端的认证
·简单的正则搜索和替换的拦截器
