---
layout: post
title: 分布式文件系统FastDFS详解
category: FastDFS
tags: [FastDFS]
excerpt: 分布式文件系统FastDFS快速入门、设计、原理、实践
keywords: FastDFS, 分布式文件系统、图片服务器
---

上一篇文章《[一次FastDFS并发问题的排查经历](http://mp.weixin.qq.com/s/EFsK3yOtb7maDNqgaHjQow)》介绍了一次生产排查并发问题的经历，可能有些人对FastDFS不是特别的了解，因此计划写几篇文章完整的介绍一下这个软件。

## 为什么要使用分布式文件系统呢？

嗯，这个问题问的好，使用了它对我们有哪些好处？带着这个问题我们来往下看：

### 单机时代

初创时期由于时间紧迫，在各种资源有限的情况下，通常就直接在项目目录下建立静态文件夹，用于用户存放项目中的文件资源。如果按不同类型再细分，可以在项目目录下再建立不同的子目录来区分。例如：```resources\static\file```、```resources\static\img```等。
    
**优点**：这样做比较便利，项目直接引用就行，实现起来也简单，无需任何复杂技术，保存数据库记录和访问起来也很方便。

**缺点**：如果只是后台系统的使用一般也不会有什么问题，但是作为一个前端网站使用的话就会存在弊端。一方面，文件和代码耦合在一起，文件越多存放越混乱；另一方面，如果流量比较大，静态文件访问会占据一定的资源，影响正常业务进行，不利于网站快速发展。

### 独立文件服务器

随着公司业务不断发展，将代码和文件放在同一服务器的弊端就会越来越明显。为了解决上面的问题引入独立图片服务器，工作流程如下：项目上传文件时，首先通过ftp或者ssh将文件上传到图片服务器的某个目录下，再通过ngnix或者apache来访问此目录下的文件，返回一个独立域名的图片URL地址，前端使用文件时就通过这个URL地址读取。

**优点**：图片访问是很消耗服务器资源的（因为会涉及到操作系统的上下文切换和磁盘I/O操作），分离出来后，Web/App服务器可以更专注发挥动态处理的能力；独立存储，更方便做扩容、容灾和数据迁移；方便做图片访问请求的负载均衡，方便应用各种缓存策略（HTTP Header、Proxy Cache等），也更加方便迁移到CDN。

**缺点**：单机存在性能瓶颈，容灾、垂直扩展性稍差

### 分布式文件系统

通过独立文件服务器可以解决一些问题，如果某天存储文件的那台服务突然down了怎么办？可能你会说，定时将文件系统备份，这台down机的时候，迅速切换到另一台就OK了，但是这样处理需要人工来干预。另外，当存储的文件超过100T的时候怎么办？单台服务器的性能问题？这个时候我们就应该考虑分布式文件系统了。

业务继续发展，单台服务器存储和响应也很快到达了瓶颈，新的业务需要文件访问具有高响应性、高可用性来支持系统。分布式文件系统，一般分为三块内容来配合，服务的存储、访问的仲裁系统，文件存储系统，文件的容灾系统来构成，仲裁系统相当于文件服务器的大脑，根据一定的算法来决定文件存储的位置，文件存储系统负责保存文件，容灾系统负责文件系统和自己的相互备份。

**优点**：扩展能力: 毫无疑问，扩展能力是一个分布式文件系统最重要的特点；高可用性: 在分布式文件系统中，高可用性包含两层，一是整个文件系统的可用性，二是数据的完整和一致性；弹性存储: 可以根据业务需要灵活地增加或缩减数据存储以及增删存储池中的资源，而不需要中断系统运行

**缺点**：系统复杂度稍高，需要更多服务器


## FastDFS

毫无疑问FastDFS就属于我们上面介绍的分布式文件系统，下面我们来详细了解一下：

### 什么是FastDFS

FastDFS是一个开源的轻量级分布式文件系统。它解决了大数据量存储和负载均衡等问题。特别适合以中小文件（建议范围：4KB < file_size <500MB）为载体的在线服务，如相册网站、视频网站等等。在UC基于FastDFS开发向用户提供了：网盘，社区，广告和应用下载等业务的存储服务。

FastDFS是一款开源的轻量级分布式文件系统纯C实现，支持Linux、FreeBSD等UNIX系统类google FS，不是通用的文件系统，只能通过专有API访问，目前提供了C、Java和PHP API为互联网应用量身定做，解决大容量文件存储问题，追求高性能和高扩展性FastDFS可以看做是基于文件的key value pair存储系统，称作分布式文件存储服务更为合适。

**FastDFS特性**：

- 文件不分块存储，上传的文件和OS文件系统中的文件一一对应
- 支持相同内容的文件只保存一份，节约磁盘空间
- 下载文件支持HTTP协议，可以使用内置Web Server，也可以和其他Web Server配合使用
- 支持在线扩容
- 支持主从文件
- 存储服务器上可以保存文件属性（meta-data）V2.0网络通信采用libevent，支持大并发访问，整体性能更好

### FastDFS相关概念

FastDFS服务端有三个角色：跟踪服务器（tracker server）、存储服务器（storage server）和客户端（client）。

**tracker server**：跟踪服务器，主要做调度工作，起负载均衡的作用。在内存中记录集群中所有存储组和存储服务器的状态信息，是客户端和数据服务器交互的枢纽。相比GFS中的master更为精简，不记录文件索引信息，占用的内存量很少。

Tracker是FastDFS的协调者，负责管理所有的storage server和group，每个storage在启动后会连接Tracker，告知自己所属的group等信息，并保持周期性的心跳，tracker根据storage的心跳信息，建立group==>[storage server list]的映射表。

Tracker需要管理的元信息很少，会全部存储在内存中；另外tracker上的元信息都是由storage汇报的信息生成的，本身不需要持久化任何数据，这样使得tracker非常容易扩展，直接增加tracker机器即可扩展为tracker cluster来服务，cluster里每个tracker之间是完全对等的，所有的tracker都接受stroage的心跳信息，生成元数据信息来提供读写服务。

**storage server**：存储服务器（又称：存储节点或数据服务器），文件和文件属性（meta data）都保存到存储服务器上。Storage server直接利用OS的文件系统调用管理文件。

Storage server（后简称storage）以组（卷，group或volume）为单位组织，一个group内包含多台storage机器，数据互为备份，存储空间以group内容量最小的storage为准，所以建议group内的多个storage尽量配置相同，以免造成存储空间的浪费。

以group为单位组织存储能方便的进行应用隔离、负载均衡、副本数定制（group内storage server数量即为该group的副本数），比如将不同应用数据存到不同的group就能隔离应用数据，同时还可根据应用的访问特性来将应用分配到不同的group来做负载均衡；缺点是group的容量受单机存储容量的限制，同时当group内有机器坏掉时，数据恢复只能依赖group内地其他机器，使得恢复时间会很长。

group内每个storage的存储依赖于本地文件系统，storage可配置多个数据存储目录，比如有10块磁盘，分别挂载在```/data/disk1-/data/disk10```，则可将这10个目录都配置为storage的数据存储目录。

storage接受到写文件请求时，会根据配置好的规则（后面会介绍），选择其中一个存储目录来存储文件。为了避免单个目录下的文件数太多，在storage第一次启动时，会在每个数据存储目录里创建2级子目录，每级256个，总共65536个文件，新写的文件会以hash的方式被路由到其中某个子目录下，然后将文件数据直接作为一个本地文件存储到该目录中。

**client**：客户端，作为业务请求的发起方，通过专有接口，使用TCP/IP协议与跟踪器服务器或存储节点进行数据交互。FastDFS向使用者提供基本文件访问接口，比如upload、download、append、delete等，以客户端库的方式提供给用户使用。

另外两个概念：

**group** ：组， 也可称为卷。 同组内服务器上的文件是完全相同的 ，同一组内的storage server之间是对等的， 文件上传、 删除等操作可以在任意一台storage server上进行 。

**meta data** ：文件相关属性，键值对（ Key Value Pair） 方式，如：width=1024,heigth=768 。


![](http://www.itmind.net/assets/images/2018/fastdfs/fastdfs_arch.png)

Tracker相当于FastDFS的大脑，不论是上传还是下载都是通过tracker来分配资源；客户端一般可以使用ngnix等静态服务器来调用或者做一部分的缓存；存储服务器内部分为卷（或者叫做组），卷于卷之间是平行的关系，可以根据资源的使用情况随时增加，卷内服务器文件相互同步备份，以达到容灾的目的。

### 上传机制

首先客户端请求Tracker服务获取到存储服务器的ip地址和端口，然后客户端根据返回的IP地址和端口号请求上传文件，存储服务器接收到请求后生产文件，并且将文件内容写入磁盘并返回给客户端file_id、路径信息、文件名等信息，客户端保存相关信息上传完毕。

![](http://www.itmind.net/assets/images/2018/fastdfs/upload.png)

内部机制如下：

**1、选择tracker server**

当集群中不止一个tracker server时，由于tracker之间是完全对等的关系，客户端在upload文件时可以任意选择一个trakcer。
选择存储的group
当tracker接收到upload file的请求时，会为该文件分配一个可以存储该文件的group，支持如下选择group的规则：

- 1、Round robin，所有的group间轮询 
- 2、Specified group，指定某一个确定的group 
- 3、Load balance，剩余存储空间多多group优先

**2、选择storage server**

当选定group后，tracker会在group内选择一个storage server给客户端，支持如下选择storage的规则： 

- 1、Round robin，在group内的所有storage间轮询 
- 2、First server ordered by ip，按ip排序 
- 3、First server ordered by priority，按优先级排序（优先级在storage上配置）

**3、选择storage path**

当分配好storage server后，客户端将向storage发送写文件请求，storage将会为文件分配一个数据存储目录，支持如下规则： 

- 1、Round robin，多个存储目录间轮询 
- 2、剩余存储空间最多的优先

**4、生成Fileid**

选定存储目录之后，storage会为文件生一个Fileid，由storage server ip、文件创建时间、文件大小、文件crc32和一个随机数拼接而成，然后将这个二进制串进行base64编码，转换为可打印的字符串。
选择两级目录
当选定存储目录之后，storage会为文件分配一个fileid，每个存储目录下有两级256*256的子目录，storage会按文件fileid进行两次hash（猜测），路由到其中一个子目录，然后将文件以fileid为文件名存储到该子目录下。

**5、生成文件名**

当文件存储到某个子目录后，即认为该文件存储成功，接下来会为该文件生成一个文件名，文件名由group、存储目录、两级子目录、fileid、文件后缀名（由客户端指定，主要用于区分文件类型）拼接而成。


### 下载机制

客户端带上文件名信息请求Tracker服务获取到存储服务器的ip地址和端口，然后客户端根据返回的IP地址和端口号请求下载文件，存储服务器接收到请求后返回文件给客户端。

![](http://www.itmind.net/assets/images/2018/fastdfs/download.png)

跟upload file一样，在download file时客户端可以选择任意tracker server。tracker发送download请求给某个tracker，必须带上文件名信息，tracke从文件名中解析出文件的group、大小、创建时间等信息，然后为该请求选择一个storage用来服务读请求。由于group内的文件同步时在后台异步进行的，所以有可能出现在读到时候，文件还没有同步到某些storage server上，为了尽量避免访问到这样的storage，tracker按照如下规则选择group内可读的storage。

- 1、该文件上传到的源头storage - 源头storage只要存活着，肯定包含这个文件，源头的地址被编码在文件名中。
- 2、文件创建时间戳==storage被同步到的时间戳 且(当前时间-文件创建时间戳) > 文件同步最大时间（如5分钟) - 文件创建后，认为经过最大同步时间后，肯定已经同步到其他storage了。 
- 3、文件创建时间戳 < storage被同步到的时间戳。 - 同步时间戳之前的文件确定已经同步了 
- 4、(当前时间-文件创建时间戳) > 同步延迟阀值（如一天）。 - 经过同步延迟阈值时间，认为文件肯定已经同步了。


### 同步时间管理

当一个文件上传成功后，客户端马上发起对该文件下载请求（或删除请求）时，tracker是如何选定一个适用的存储服务器呢？
其实每个存储服务器都需要定时将自身的信息上报给tracker，这些信息就包括了本地同步时间（即，同步到的最新文件的时间戳）。而tracker根据各个存储服务器的上报情况，就能够知道刚刚上传的文件，在该存储组中是否已完成了同步。同步信息上报如下图：

![](http://www.itmind.net/assets/images/2018/fastdfs/sync.png)

写文件时，客户端将文件写至group内一个storage server即认为写文件成功，storage server写完文件后，会由后台线程将文件同步至同group内其他的storage server。

每个storage写文件后，同时会写一份binlog，binlog里不包含文件数据，只包含文件名等元信息，这份binlog用于后台同步，storage会记录向group内其他storage同步的进度，以便重启后能接上次的进度继续同步；进度以时间戳的方式进行记录，所以最好能保证集群内所有server的时钟保持同步。

storage的同步进度会作为元数据的一部分汇报到tracker上，tracke在选择读storage的时候会以同步进度作为参考。
比如一个group内有A、B、C三个storage server，A向C同步到进度为T1 (T1以前写的文件都已经同步到B上了），B向C同步到时间戳为T2（T2 > T1)，tracker接收到这些同步进度信息时，就会进行整理，将最小的那个做为C的同步时间戳，本例中T1即为C的同步时间戳为T1（即所有T1以前写的数据都已经同步到C上了）；同理，根据上述规则，tracker会为A、B生成一个同步时间戳。


### 精巧的文件ID-FID

说到下载就不得不提文件索引（又称：FID）的精巧设计了。文件索引结构如下图，是客户端上传文件后存储服务器返回给客户端，用于以后访问该文件的索引信息。文件索引信息包括：组名，虚拟磁盘路径，数据两级目录，文件名。

![](http://www.itmind.net/assets/images/2018/fastdfs/id.png)

- 组名：文件上传后所在的存储组名称，在文件上传成功后有存储服务器返回，需要客户端自行保存。
- 虚拟磁盘路径：存储服务器配置的虚拟路径，与磁盘选项store_path*对应。
- 数据两级目录：存储服务器在每个虚拟磁盘路径下创建的两级目录，用于存储数据文件。
- 文件名：与文件上传时不同。是由存储服务器根据特定信息生成，文件名包含：源存储服务器IP地址、文件创建时间戳、文件大小、随机数和文件拓展名等信息。

**快速定位文件**

知道FastDFS FID的组成后，我们来看看FastDFS是如何通过这个精巧的FID定位到需要访问的文件。

- 1、通过组名tracker能够很快的定位到客户端需要访问的存储服务器组，并将选择合适的存储服务器提供客户端访问；
- 2、存储服务器根据“文件存储虚拟磁盘路径”和“数据文件两级目录”可以很快定位到文件所在目录，并根据文件名找到客户端需要访问的文件。

![](http://www.itmind.net/assets/images/2018/fastdfs/find.jpg)


**如何搭建FastDFS？参考我博客的这篇文章[FastDFS 集群 安装 配置
](http://www.ityouknow.com/fastdfs/2017/10/10/cluster-building-fastdfs.html)**，下图为某用户搭建的架构示意图

![](http://www.itmind.net/assets/images/2018/fastdfs/install.png)

> 文中图片均来源于网络

## 参考

[官方网站](https://github.com/happyfish100/)  
[配置文档](https://github.com/happyfish100/fastdfs/wiki/)  
[Java客户端](https://github.com/happyfish100/fastdfs-client-java)  
[分布式文件系统FastDFS设计原理](http://blog.chinaunix.net/uid-20196318-id-4058561.html)  
[FASTDFS](https://www.jianshu.com/p/1c71ae024e5e)  