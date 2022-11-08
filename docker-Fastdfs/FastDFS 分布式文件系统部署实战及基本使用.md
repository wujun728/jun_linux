　**FastDFS 分布式文件系统部署实战及基本使用**

　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　

 

　　**FastDFS是一个开源的高性能分布式文件系统。它的主要功能包括：文件存储，文件同步和文件访问（文件上传和文件下载），它可以解决高容量和负载平衡问题。FastDFS应满足基于照片共享站点和视频共享站点等文件服务的网站的要求。它的应用场景非常适合存储大于4k小于500M左右的音频，图片，APP安装包等二进制文件。FastDFS典型用户有UC，支付宝，京东，飞信，58同城，51CTO等等。GitHub地址为：https://github.com/happyfish100/fastdfs。**

 

 

**一.FastDFS基础知识**

**1>.什么是FastDFS**

　　FastDFS是一个开源的轻量级分布式文件系统。它解决了大数据量存储和负载均衡等问题。特别适合以中小文件（建议范围：4KB < file_size <500MB）为载体的在线服务，如相册网站、视频网站等等。在UC基于FastDFS开发向用户提供了：网盘，社区，广告和应用下载等业务的存储服务。

　　FastDFS是一款开源的轻量级分布式文件系统纯C实现，支持Linux、FreeBSD等UNIX系统类google FS，不是通用的文件系统，只能通过专有API访问，目前提供了C、Java和PHP API为互联网应用量身定做，解决大容量文件存储问题，追求高性能和高扩展性FastDFS可以看做是基于文件的key value pair存储系统，称作分布式文件存储服务更为合适。

**2>.FastDFS的特性**

　　2.1>.文件不分块存储，上传的文件和OS文件系统中的文件一一对应；

　　2.2>.支持相同内容的文件只保存一份，节约磁盘空间；

　　2.3>.下载文件支持HTTP协议，可以使用内置Web Server，也可以和其他Web Server配合使用；

　　2.4>.支持在线扩容；

　　2.5>.支持主从文件；

　　2.6>.存储服务器上可以保存文件属性（meta-data）V2.0网络通信采用libevent，支持大并发访问，整体性能更好；

**3>.FastDFS架构** 

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) FastDFS相关概念

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
FastDFS有两个角色：跟踪器和存储。
    跟踪服务器（Tracker）负责文件访问的调度和负载平衡。在内存中记录集群中group（同一个group的数据是相同的，和raid1原理很相似，group是支持在线添加的，各个group之间并不互相通信！它们只和追踪服务器通信！）和storage server的状态信息，是连接client和storage server的枢纽。因为相关信息全部在内存中，Tracker server的性能非常高，一个较大的集群（比如上百个group）中有3台就足够了。
    　　存储服务器（Storage）负责存储文件及其功能是文件管理，包括：文件存储，文件同步，提供文件访问接口。它还管理元数据（meta data），这些元数据表示为文件的键值对。例如：width = 1024，键为“width”，值为“1024”。


跟踪器和存储器包含一个或多个服务器。可以随时向集群中添加或删除跟踪器或存储集群中的服务器，而不会影响在线服务。跟踪器集群中的服务器是对等的。

由文件卷/组组织的storarge服务器以获得高容量。存储系统包含一个或多个卷，这些卷的文件在这些卷中是独立的。整个存储系统的容量等于所有容量的总和。文件卷包含一个或多个存储服务器，这些服务器的文件在这些服务器中相同。文件卷中的服务器相互备份，所有这些服务器都是负载平衡的。将存储服务器添加到卷时，此卷中已存在的文件会自动复制到此新服务器，完成此复制后，系统将在线将此服务器切换为提供存储服务。

当整个存储容量不足时，您可以添加一个或多个卷以扩展存储容量。为此，您需要添加一个或多个存储服务器。

文件的标识由两部分组成：卷名和文件名。Tracker相当于FastDFS的大脑，不论是上传还是下载都是通过tracker来分配资源；客户端一般可以使用ngnix等静态服务器来调用或者做一部分的缓存；存储服务器内部分为卷（或者叫做组），卷于卷之间是平行的关系，可以根据资源的使用情况随时增加，卷内服务器文件相互同步备份，以达到容灾的目的。
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 ![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219161409014-417276906.png)

**4>.FastDFS上传文件**

　　首先客户端请求Tracker服务获取到存储服务器的ip地址和端口，然后客户端根据返回的IP地址和端口号请求上传文件，存储服务器接收到请求后生产文件，并且将文件内容写入磁盘并返回给客户端file_id、路径信息、文件名等信息，客户端保存相关信息上传完毕。

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) FastDFS内部机制详解

 ![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219161430889-1913291329.png)

**5>.FastDFS下载文件**

 　客户端带上文件名信息请求Tracker服务获取到存储服务器的ip地址和端口，然后客户端根据返回的IP地址和端口号请求下载文件，存储服务器接收到请求后返回文件给客户端。

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) FastDFS下载内部机制详解 

![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219162420571-2043112855.png)

**6>.精巧的文件ID-FID**

　　说到下载就不得不提文件索引（又称：FID）的精巧设计了。文件索引结构如下图，是客户端上传文件后存储服务器返回给客户端，用于以后访问该文件的索引信息。文件索引信息包括：组名，虚拟磁盘路径，数据两级目录，文件名。

![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219163423078-127182914.png)

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
组名：文件上传后所在的存储组名称，在文件上传成功后有存储服务器返回，需要客户端自行保存。

虚拟磁盘路径：存储服务器配置的虚拟路径，与磁盘选项store_path*对应。

数据两级目录：存储服务器在每个虚拟磁盘路径下创建的两级目录，用于存储数据文件。

文件名：与文件上传时不同。是由存储服务器根据特定信息生成，文件名包含：源存储服务器IP地址、文件创建时间戳、文件大小、随机数和文件拓展名等信息。
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**7>.快速定位文件**

```
知道FastDFS FID的组成后，我们来看看FastDFS是如何通过这个精巧的FID定位到需要访问的文件。

1、通过组名tracker能够很快的定位到客户端需要访问的存储服务器组，并将选择合适的存储服务器提供客户端访问；

2、存储服务器根据“文件存储虚拟磁盘路径”和“数据文件两级目录”可以很快定位到文件所在目录，并根据文件名找到客户端需要访问的文件。
```

![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219163644456-291111123.png) 

　　以上信息引用自：https://www.cnblogs.com/ityouknow/p/8240976.html。

 

**二.安装libfastcommon类库（安装FastDFS必须先安装libfastcommon类库，否则会导致报错）**

**1>.查看**[happyfish100](https://github.com/happyfish100)/[libfastcommon](https://github.com/happyfish100/libfastcommon)**地址**

![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219172252302-234155779.png)

**2>.下载libfastcommon安装包** 

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# yum -y install gcc gcc-c++ libstdc++-devel pcre-devel zlib-devel wget make　　　　　　　　　　#安装依赖软件

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# wget https://github.com/happyfish100/libfastcommon/archive/V1.0.39.tar.gz 

 ![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219172814411-99597035.png)

**3>.** **安装libfastcommon（本实验使用的是CentOS 7.6，两台配置一样的虚拟机测试，因此2台虚拟机都需要做同的操作）**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# tar -zxf V1.0.39.tar.gz -C /yinzhengjie/softwares/
[root@node101 ~]# 
[root@node101 ~]# ll /yinzhengjie/softwares/libfastcommon-1.0.39/
total 40
drwxrwxr-x 2 root root 4096 Jul 31  2018 doc
-rw-rw-r-- 1 root root 9099 Jul 31  2018 HISTORY
-rw-rw-r-- 1 root root  566 Jul 31  2018 INSTALL
-rw-rw-r-- 1 root root 1607 Jul 31  2018 libfastcommon.spec
-rwxrwxr-x 1 root root 3248 Jul 31  2018 make.sh
drwxrwxr-x 2 root root 4096 Jul 31  2018 php-fastcommon
-rw-rw-r-- 1 root root 2763 Jul 31  2018 README
drwxrwxr-x 3 root root 4096 Jul 31  2018 src
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 libfastcommon-1.0.39]# ./make.sh

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 libfastcommon-1.0.39]# ./make.sh install

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# yum -y install gcc gcc-c++ libstdc++-devel pcre-devel zlib-devel wget make　　　　　　　　　　#安装依赖软件

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# wget https://github.com/happyfish100/libfastcommon/archive/V1.0.39.tar.gz

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 libfastcommon-1.0.39]# ./make.sh

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 libfastcommon-1.0.39]# ./make.sh install

 

**三.部署FastDFS**

**1>.查看[happyfish100](https://github.com/happyfish100)/[fastdfs](https://github.com/happyfish100/fastdfs)地址**

 ![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219175309946-2013860883.png)

**2>.选择[FastDFS的版本](https://github.com/happyfish100/fastdfs/archive/V5.11.tar.gz)**

 ![img](https://img2018.cnblogs.com/blog/795254/201902/795254-20190219175445724-97205745.png)

**3>.安装FastDFS**

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# wget https://github.com/happyfish100/fastdfs/archive/V5.11.tar.gz

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# tar -zxf V5.11.tar.gz -C /yinzhengjie/softwares/
[root@node101 ~]# 
[root@node101 ~]# ll /yinzhengjie/softwares/fastdfs-5.11/
total 136
drwxrwxr-x 3 root root  4096 Jun  3  2017 client
drwxrwxr-x 2 root root  4096 Jun  3  2017 common
drwxrwxr-x 2 root root  4096 Jun  3  2017 conf
-rw-rw-r-- 1 root root 35067 Jun  3  2017 COPYING-3_0.txt
-rw-rw-r-- 1 root root  3171 Jun  3  2017 fastdfs.spec
-rw-rw-r-- 1 root root 33100 Jun  3  2017 HISTORY
drwxrwxr-x 2 root root  4096 Jun  3  2017 init.d
-rw-rw-r-- 1 root root  7755 Jun  3  2017 INSTALL
-rwxrwxr-x 1 root root  5548 Jun  3  2017 make.sh
drwxrwxr-x 2 root root  4096 Jun  3  2017 php_client
-rw-rw-r-- 1 root root  2380 Jun  3  2017 README.md
-rwxrwxr-x 1 root root  1768 Jun  3  2017 restart.sh
-rwxrwxr-x 1 root root  1680 Jun  3  2017 stop.sh
drwxrwxr-x 4 root root  4096 Jun  3  2017 storage
drwxrwxr-x 2 root root  4096 Jun  3  2017 test
drwxrwxr-x 2 root root  4096 Jun  3  2017 tracker
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 fastdfs-5.11]# ./make.sh

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 fastdfs-5.11]# ./make.sh install

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# wget https://github.com/happyfish100/fastdfs/archive/V5.11.tar.gz

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 fastdfs-5.11]# ./make.sh

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 fastdfs-5.11]# ./make.sh install

**4>.FastDFS的文件存放说明** 

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# ll /etc/fdfs/  　　　　　　　　　　　　　　　　　　　　　　　　#配置文件存放路径
total 24
-rw-r--r-- 1 root root 1461 Feb 19 17:58 client.conf.sample
-rw-r--r-- 1 root root 7927 Feb 19 17:58 storage.conf.sample
-rw-r--r-- 1 root root  105 Feb 19 17:58 storage_ids.conf.sample
-rw-r--r-- 1 root root 7389 Feb 19 17:58 tracker.conf.sample
[root@node101 ~]# 
[root@node101 ~]#
[root@node101 ~]# ll /etc/init.d/fdfs_*　　　　　　　　　　　　　　　　　　　　#脚本存放路径
-rwxr-xr-x 1 root root 961 Feb 19 17:58 /etc/init.d/fdfs_storaged 　　　　#用于存储的脚本
-rwxr-xr-x 1 root root 963 Feb 19 17:58 /etc/init.d/fdfs_trackerd　　　　 #用于追踪的脚本
[root@node101 ~]# 　　　　
[root@node101 ~]#
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**5>.创建存储数据的路径**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# mkdir -p /home/yinzhengjie/
.bash_logout   .bash_profile  .bashrc        Desktop/       glusterfs/     
[root@node101 ~]# mkdir -p /home/yinzhengjie/fastdfs/data/fdfs_tracker
[root@node101 ~]# 
[root@node101 ~]# mkdir -p /home/yinzhengjie/fastdfs/data/fdfs_storage
[root@node101 ~]# 
[root@node101 ~]# ssh node102.yinzhengjie.org.cn
Last login: Tue Feb 19 12:50:49 2019 from node101.yinzhengjie.org.cn
[root@node102 ~]# 
[root@node102 ~]# mkdir -p /home/yinzhengjie/fastdfs/data/fdfs_tracker
[root@node102 ~]# 
[root@node102 ~]# mkdir -p /home/yinzhengjie/fastdfs/data/fdfs_storage
[root@node102 ~]# 
[root@node102 ~]# exit 
logout
Connection to node102.yinzhengjie.org.cn closed.
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**6>.修改配置文件（我这里的做法是在node101.yinzhengjie.org.cn上配置好后，将该配置文件拷贝到node102.yinzhengjie.org.cn节点上去！）**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# cd /etc/fdfs/
[root@node101 fdfs]# 
[root@node101 fdfs]# ll
total 24
-rw-r--r-- 1 root root 1461 Feb 19 17:58 client.conf.sample
-rw-r--r-- 1 root root 7927 Feb 19 17:58 storage.conf.sample
-rw-r--r-- 1 root root  105 Feb 19 17:58 storage_ids.conf.sample
-rw-r--r-- 1 root root 7389 Feb 19 17:58 tracker.conf.sample
[root@node101 fdfs]# 
[root@node101 fdfs]# cp storage.conf.sample storage.conf
[root@node101 fdfs]# 
[root@node101 fdfs]# cp tracker.conf.sample tracker.conf
[root@node101 fdfs]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# sed -i s'#base_path=/home/yuqing/fastdfs#base_path=/home/yinzhengjie/fastdfs/data/fdfs_tracker#' /etc/fdfs/tracker.conf

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# sed -i s'#base_path=/home/yuqing/fastdfs#base_path=/home/yinzhengjie/fastdfs/data/fdfs_storage#' /etc/fdfs/storage.conf

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# sed -i s'#store_path0=/home/yuqing/fastdfs#store_path0=/home/yinzhengjie/fastdfs/data/fdfs_storage/store#' /etc/fdfs/storage.conf

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# sed -i s'#tracker_server=192.168.209.121:22122#tracker_server=node101.yinzhengjie.org.cn:22122\ntracker_server=node102.yinzhengjie.org.cn:22122\n#' /etc/fdfs/storage.conf

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# scp /etc/fdfs/tracker.conf /etc/fdfs/storage.conf node102.yinzhengjie.org.cn:/etc/fdfs/　　　　　　　　　　　　　　#将node101.yinzhengjie.org.cn的配置同步到node102.yinzhengjie.org.cn上去！
tracker.conf                                                                                                                                                                     100% 7412     8.9MB/s   00:00    
storage.conf                                                                                                                                                                     100% 8039    13.1MB/s   00:00    
[root@node101 ~]# 
[root@node101 ~]# ssh node102.yinzhengjie.org.cn
Last login: Tue Feb 19 18:46:47 2019 from node101.yinzhengjie.org.cn
[root@node102 ~]# 
[root@node102 ~]# 
[root@node102 ~]# cat /etc/redhat-release 
CentOS Linux release 7.6.1810 (Core) 
[root@node102 ~]# 
[root@node102 ~]# hostname
node102.yinzhengjie.org.cn
[root@node102 ~]# 
[root@node102 ~]# 
[root@node102 ~]# grep base_path /etc/fdfs/tracker.conf
base_path=/home/yinzhengjie/fastdfs/data/fdfs_tracker
[root@node102 ~]# 
[root@node102 ~]# grep base_path /etc/fdfs/storage.conf | grep -v ^#
base_path=/home/yinzhengjie/fastdfs/data/fdfs_storage
[root@node102 ~]# 
[root@node102 ~]# grep store_path0 /etc/fdfs/storage.conf | grep -v ^#
store_path0=/home/yinzhengjie/fastdfs/data/fdfs_storage/store
[root@node102 ~]# 
[root@node102 ~]# grep tracker_server /etc/fdfs/storage.conf | grep -v ^# 
tracker_server=node101.yinzhengjie.org.cn:22122
tracker_server=node102.yinzhengjie.org.cn:22122
[root@node102 ~]#  
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# diff /etc/fdfs/storage.conf /etc/fdfs/storage.conf.sample 

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# diff /etc/fdfs/tracker.conf /etc/fdfs/tracker.conf.sample

**7>.在各个节点上启动FastDFS服务** 

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# yum -y install net-tools　　　　　　　　#安装网络工具

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# /etc/init.d/fdfs_trackerd start
Reloading systemd:                                         [  OK  ]
Starting fdfs_trackerd (via systemctl):                    [  OK  ]
[root@node101 ~]# 
[root@node101 ~]# mkdir -pv /home/yinzhengjie/fastdfs/data/fdfs_storage/store/data　　　　　　　　　　#这个目录需要我们手动创建一下，否则启动时日志会报错！
mkdir: created directory ‘/home/yinzhengjie/fastdfs/data/fdfs_storage/store’
mkdir: created directory ‘/home/yinzhengjie/fastdfs/data/fdfs_storage/store/data’
[root@node101 ~]#
[root@node101 ~]# /etc/init.d/fdfs_storaged start
Starting fdfs_storaged (via systemctl):                    [  OK  ]
[root@node101 ~]# 
[root@node101 ~]# 
[root@node101 ~]# netstat -untalp | grep fdfs
tcp        0      0 0.0.0.0:22122           0.0.0.0:*               LISTEN      11694/fdfs_trackerd 
tcp        0      0 0.0.0.0:23000           0.0.0.0:*               LISTEN      12189/fdfs_storaged 
tcp        0      0 172.30.1.101:49142      172.30.1.102:22122      ESTABLISHED 11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:51268      172.30.1.102:23000      ESTABLISHED 12189/fdfs_storaged 
tcp        0      0 172.30.1.101:54588      172.30.1.101:22122      ESTABLISHED 12189/fdfs_storaged 
tcp        0      0 172.30.1.101:23000      172.30.1.102:37686      ESTABLISHED 12189/fdfs_storaged 
tcp        0      0 172.30.1.101:22122      172.30.1.102:59616      ESTABLISHED 11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:22122      172.30.1.101:54588      ESTABLISHED 11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:49102      172.30.1.102:22122      ESTABLISHED 12189/fdfs_storaged 
[root@node101 ~]# 
[root@node101 ~]#
[root@node101 ~]# netstat -untalp | grep 23000
tcp        0      0 0.0.0.0:23000           0.0.0.0:*               LISTEN      12189/fdfs_storaged 
tcp        0      0 172.30.1.101:51268      172.30.1.102:23000      ESTABLISHED 12189/fdfs_storaged 
tcp        0      0 172.30.1.101:23000      172.30.1.102:37686      ESTABLISHED 12189/fdfs_storaged 
[root@node101 ~]# 
[root@node101 ~]# netstat -untalp | grep 22122
tcp        0      0 0.0.0.0:22122           0.0.0.0:*               LISTEN      11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:49142      172.30.1.102:22122      ESTABLISHED 11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:54588      172.30.1.101:22122      ESTABLISHED 12189/fdfs_storaged 
tcp        0      0 172.30.1.101:22122      172.30.1.102:59616      ESTABLISHED 11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:22122      172.30.1.101:54588      ESTABLISHED 11694/fdfs_trackerd 
tcp        0      0 172.30.1.101:49102      172.30.1.102:22122      ESTABLISHED 12189/fdfs_storaged 
[root@node101 ~]# 
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# /etc/init.d/fdfs_trackerd start

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# /etc/init.d/fdfs_storaged start 

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# tail -1000f /home/yinzhengjie/fastdfs/data/fdfs_tracker/logs/trackerd.log　　　　　　　　　　　　#查看trackerd进程日志

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node102 ~]# tail -1000f /home/yinzhengjie/fastdfs/data/fdfs_storage/logs/storaged.log　　　　　　　　　　　　#查看storaged进程日志

 

**四.FastDFS的基本使用**

**1>.配置FastDFS的client的配置文件**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf
[root@node101 ~]# 
[root@node101 ~]# grep base_path /etc/fdfs/client.conf
base_path=/home/yuqing/fastdfs
[root@node101 ~]# 
[root@node101 ~]# sed -i s'#base_path=/home/yuqing/fastdfs#base_path=/var/log/fastdfs_client#' /etc/fdfs/client.conf　　　　　　　　　　#配置日志的存放路径
[root@node101 ~]# 
[root@node101 ~]# grep base_path /etc/fdfs/client.conf                                                              
base_path=/var/log/fastdfs_client
[root@node101 ~]# 
[root@node101 ~]# grep tracker_server=  /etc/fdfs/client.conf | grep -v ^#
tracker_server=192.168.0.197:22122
[root@node101 ~]# 
[root@node101 ~]# 
[root@node101 ~]# sed -i s'#tracker_server=192.168.0.197:22122#tracker_server=node101.yinzhengjie.org.cn:22122\ntracker_server=node102.yinzhengjie.org.cn:22122#' /etc/fdfs/client.conf　　　　　　#配置Tracker地址
[root@node101 ~]# 
[root@node101 ~]# grep tracker_server=  /etc/fdfs/client.conf | grep -v ^#                                                                                                              
tracker_server=node101.yinzhengjie.org.cn:22122
tracker_server=node102.yinzhengjie.org.cn:22122
[root@node101 ~]# 
[root@node101 ~]# mkdir /var/log/fastdfs_client　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　#这一步骤必须做，如果该目录不存在的话，我们在下一步测试上传文件时会报错！
[root@node101 ~]#
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**2>.上传文件到FastDFS** 

```
[root@node101 ~]# fdfs_upload_file /etc/fdfs/client.conf /etc/passwd
group1/M00/00/00/rB4BZVxr8omAKBoWAAAEXu7xndU2260655　　　　　　　　　　#注意，这里返回的值就是fastDFS存储路径
[root@node101 ~]# 
[root@node101 ~]# 
```

**3>.下载文件到本地**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr8omAKBoWAAAEXu7xndU2260655
[root@node101 ~]# 
[root@node101 ~]# md5sum rB4BZVxr8omAKBoWAAAEXu7xndU2260655  　　　　　　　　　　　　
b8e310865d07d9d3a9eac16f6c5547ee  rB4BZVxr8omAKBoWAAAEXu7xndU2260655
[root@node101 ~]# 
[root@node101 ~]# md5sum /etc/passwd　　　　　　　　　　　　　　　　　　　　　　#我们会发现文件的内容并没有被修改！
b8e310865d07d9d3a9eac16f6c5547ee  /etc/passwd
[root@node101 ~]#  
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) [root@node101 ~]# md5sum /home/yinzhengjie/fastdfs/data/fdfs_storage/store/data/00/00/rB4BZVxr8omAKBoWAAAEXu7xndU2260655

**4>.查询文件信息** 

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# fdfs_file_info /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr8omAKBoWAAAEXu7xndU2260655
source storage id: 0
source ip address: 172.30.1.101
file create timestamp: 2019-02-19 20:11:53
file size: 1118
file crc32: 4008811989 (0xEEF19DD5)
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**5>.给某个文件追加内容**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# 
[root@node101 ~]# echo "尹正杰到此一游！" > 1.txt
[root@node101 ~]# 
[root@node101 ~]# echo "Jason Yin" > 2.txt   
[root@node101 ~]# 
[root@node101 ~]# cat 1.txt 
尹正杰到此一游！
[root@node101 ~]# 
[root@node101 ~]# cat 2.txt 
Jason Yin
[root@node101 ~]# 
[root@node101 ~]# fdfs_upload_appender /etc/fdfs/client.conf 1.txt 
group1/M00/00/00/rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt
[root@node101 ~]# 
[root@node101 ~]# fdfs_append_file  /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt 2.txt 　　　　　　　　#我们这里吧2.txt的内容追加到了1.txt中！
[root@node101 ~]# 　　　　　　　　　　
[root@node101 ~]# fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt
[root@node101 ~]# 
[root@node101 ~]# cat rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt
尹正杰到此一游！
Jason Yin
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**6>.删除文件** 

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# 
[root@node101 ~]# fdfs_file_info /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt　　　　　　　　　　#我们已经确认该文件已经存在，使用下面的命令删除该文件后就无法查看到该文件的信息啦！
source storage id: 0
source ip address: 172.30.1.101
file create timestamp: 2019-02-19 20:30:13
file size: 35
file crc32: 1128193532 (0x433EDDFC)
[root@node101 ~]# 
[root@node101 ~]# 
[root@node101 ~]# fdfs_delete_file /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt　　　　　　　　　　#删除FastDFS中已经存在的文件
[root@node101 ~]# 
[root@node101 ~]# 
[root@node101 ~]# fdfs_file_info /etc/fdfs/client.conf group1/M00/00/00/rB4BZVxr9pOEPLVbAAAAAEM-3fw595.txt  
[2019-02-19 20:34:42] ERROR - file: tracker_proto.c, line: 48, server: 172.30.1.101:23000, response status 2 != 0
[2019-02-19 20:34:42] ERROR - file: ../client/storage_client.c, line: 372, fdfs_recv_response fail, result: 2
query file info fail, error no: 2, error info: No such file or directory
[root@node101 ~]# 
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**7>.监控FastDFS集群信息**

![img](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@node101 ~]# fdfs_monitor /etc/fdfs/client.conf
[2019-02-19 20:35:52] DEBUG - base_path=/var/log/fastdfs_client, connect_timeout=30, network_timeout=60, tracker_server_count=2, anti_steal_token=0, anti_steal_secret_key length=0, use_connection_pool=0, g_connection_pool_max_idle_time=3600s, use_storage_id=0, storage server id count: 0

server_count=2, server_index=1

tracker server is 172.30.1.102:22122

group count: 1

Group 1:
group name = group1
disk total space = 11502 MB
disk free space = 10597 MB
trunk free space = 0 MB
storage server count = 2
active server count = 2
storage server port = 23000
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.30.1.101
                ip_addr = 172.30.1.101 (node101.yinzhengjie.org.cn)  ACTIVE
                http domain = 
                version = 5.11
                join time = 2019-02-19 19:30:39
                up time = 2019-02-19 19:43:21
                total storage = 11502 MB
                free storage = 10597 MB
                upload priority = 10
                store_path_count = 1
                subdir_count_per_path = 256
                storage_port = 23000
                storage_http_port = 8888
                current_write_path = 0
                source storage id = 
                if_trunk_server = 0
                connection.alloc_count = 256
                connection.current_count = 1
                connection.max_count = 2
                total_upload_count = 3
                success_upload_count = 3
                total_append_count = 1
                success_append_count = 1
                total_modify_count = 0
                success_modify_count = 0
                total_truncate_count = 0
                success_truncate_count = 0
                total_set_meta_count = 0
                success_set_meta_count = 0
                total_delete_count = 1
                success_delete_count = 1
                total_download_count = 2
                success_download_count = 2
                total_get_meta_count = 0
                success_get_meta_count = 0
                total_create_link_count = 0
                success_create_link_count = 0
                total_delete_link_count = 0
                success_delete_link_count = 0
                total_upload_bytes = 1153
                success_upload_bytes = 1153
                total_append_bytes = 10
                success_append_bytes = 10
                total_modify_bytes = 0
                success_modify_bytes = 0
                stotal_download_bytes = 1153
                success_download_bytes = 1153
                total_sync_in_bytes = 35
                success_sync_in_bytes = 35
                total_sync_out_bytes = 0
                success_sync_out_bytes = 0
                total_file_open_count = 8
                success_file_open_count = 8
                total_file_read_count = 2
                success_file_read_count = 2
                total_file_write_count = 6
                success_file_write_count = 6
                last_heart_beat_time = 2019-02-19 20:35:27
                last_source_update = 2019-02-19 20:34:38
                last_sync_update = 2019-02-19 20:27:10
                last_synced_timestamp = 2019-02-19 20:27:01 (0s delay)
        Storage 2:
                id = 172.30.1.102
                ip_addr = 172.30.1.102 (node102.yinzhengjie.org.cn)  ACTIVE
                http domain = 
                version = 5.11
                join time = 2019-02-19 19:30:15
                up time = 2019-02-19 19:50:48
                total storage = 11502 MB
                free storage = 10597 MB
                upload priority = 10
                store_path_count = 1
                subdir_count_per_path = 256
                storage_port = 23000
                storage_http_port = 8888
                current_write_path = 0
                source storage id = 172.30.1.101
                if_trunk_server = 0
                connection.alloc_count = 256
                connection.current_count = 1
                connection.max_count = 2
                total_upload_count = 2
                success_upload_count = 2
                total_append_count = 0
                success_append_count = 0
                total_modify_count = 0
                success_modify_count = 0
                total_truncate_count = 0
                success_truncate_count = 0
                total_set_meta_count = 0
                success_set_meta_count = 0
                total_delete_count = 0
                success_delete_count = 0
                total_download_count = 1
                success_download_count = 1
                total_get_meta_count = 0
                success_get_meta_count = 0
                total_create_link_count = 0
                success_create_link_count = 0
                total_delete_link_count = 0
                success_delete_link_count = 0
                total_upload_bytes = 35
                success_upload_bytes = 35
                total_append_bytes = 0
                success_append_bytes = 0
                total_modify_bytes = 0
                success_modify_bytes = 0
                stotal_download_bytes = 10
                success_download_bytes = 10
                total_sync_in_bytes = 1163
                success_sync_in_bytes = 1163
                total_sync_out_bytes = 0
                success_sync_out_bytes = 0
                total_file_open_count = 7
                success_file_open_count = 7
                total_file_read_count = 1
                success_file_read_count = 1
                total_file_write_count = 6
                success_file_write_count = 6
                last_heart_beat_time = 2019-02-19 20:35:30
                last_source_update = 2019-02-19 20:27:01
                last_sync_update = 2019-02-19 20:34:44
                last_synced_timestamp = 2019-02-19 20:34:38 (0s delay)
[root@node101 ~]# 
[root@node101 ~]# 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)