---
layout: post
title: FastDFS 集群 安装 配置
category: FastDFS
tags: [FastDFS]
---

这篇文章介绍如何搭建FastDFS 集群

FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包括：文件存储、文件同步、文件访问（文件上传、文件下载）等，解决了大容量存储和负载均衡的问题。特别适合以文件为载体的在线服务，如相册网站、视频网站等等。

FastDFS为互联网量身定制，充分考虑了冗余备份、负载均衡、线性扩容等机制，并注重高可用、高性能等指标，使用FastDFS很容易搭建一套高性能的文件服务器集群提供文件上传、下载等服务。

## 环境准备

系统系统 centos6.5        
六台服务器：192.168.53.85/86/90
            192.168.54.73/74/75  
安装包： 

``` sh
fastdfs-5.05.tar.gz
libfastcommon-1.0.36.zip
nginx-1.7.9.tar.gz
```

服务器规划

tracker服务器：192.168.53.85/86 
storage服务器：192.168.53.90
               192.168.54.73/74/75 

## 安装Fastdfs(全部)

安装依赖包

> 注意：FastDFS 5.x 取消了对 libevent 的依赖，添加了对 libfastcommon 的依赖。

- 在安装FastDFS和Nginx之前，需确保gcc、gcc-c++、 libstdc++-devel、make等依赖库和工具已经安装

``` sh
#安装依赖软件
yum -y install gcc gcc-c++ libstdc++-devel pcre-devel zlib-devel wget make
yum -y groupinstall 'Development Tools' 
```

安装libfastcommon类库

安装FastDFS必须先安装libfastcommon类库，否则会导致报错，安装直接根据如下几个步骤即可~

``` sh
unzip libfastcommon-1.0.36.zip  -d /usr/local

cd /usr/local/libfastcommon-1.0.36
./make.sh
./make.sh install
```

安装FastDFS

``` sh
tar -xvzf fastdfs-5.05.tar.gz -C /usr/local

cd /usr/local/fastdfs-5.05
./make.sh
./make.sh install
```

安装好之后，在/usr/bin目录下，可以看fdfs开头的命令工具

> FastDFS安装完成之后，所有配置文件在/etc/fdfs目录下，tracker需要tracker.conf配置文件，storage需要storage.conf配置文件。


## 安装tracker（85/86）

将tracker.conf.sample文件重命名为tracker.conf，然后修改配置文件/etc/fdfs/tracker.conf

``` sh
# 存储日志和数据的根目录
mkdir /root/fastdfs

cd /etc/fdfs
cp tracker.conf.sample tracker.conf
```

只需要修改 base_pash路径（文件存储路径）

``` sh
vi tracker.conf
base_path=/root/fastdfs
```

配置文件中有这几个参数需要注意：

``` sh
#启用配置文件
disabled=false
#设置tracker的端口号
port=22122
#设置tracker的数据文件和日志目录（需手动创建）
base_path=/root/fastdfs
#设置http端口号
http.server_port=9090
```

使用```/usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf start```尝试启动tracker

``` sh
[root@localhost ~]# fdfs_trackerd /etc/fdfs/tracker.conf restart
[root@localhost ~]# 
```

没有报错，查看端口22122是否开始监听，确认启动是否成功。

``` sh
[root@localhost ~]# ps -ef|grep fdfs
root      6078     1  0 11:59 ?        00:00:00 /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf start
root      6101  6054  0 12:01 pts/2    00:00:00 grep fdfs
[root@localhost ~]# netstat -unltp | grep fdfs
tcp        0      0 0.0.0.0:22122               0.0.0.0:*                   LISTEN      6078/fdfs_trackerd  
```

也可以查看tracker的日志是否启动成功

``` sh
[root@localhost ~]# cat /root/fastdfs/logs/trackerd.log 
[2017-10-09 11:59:12] INFO - FastDFS v5.05, base_path=/root/fastdfs, run_by ...
```

至此，一个简单的的tracker配置就完成了，Tracker也成功启动~， 接下来要做的就是完成Storage的配置~

## 安装storage（90/73/74/75）

将存储节点分为两个组，其中group1 （72、73）、group2 （74、75）。

创建存储目录和配置文件

``` sh
mkdir /root/fastdfs

cd /etc/fdfs
cp storage.conf.sample storage.conf
``` 

修改配置

storage主要完成base_path，store_path以及tracker的连接地址以及storage的http服务端口配置等。

主要有如下几个参数：

``` sh
vi /etc/fdfs/storage.conf
# 内容
group_name=group1                   # 组名（第一组为group1，第二组为group2，依次类推...）
base_path=/root/fastdfs             # 数据和日志文件存储根目录
store_path0=/root/fastdfs           #第一个存储目录，第二个存储目录起名为：store_path1=xxx，其它存储目录名依次类推...
store_path_count=1                  # 存储路径个数，需要和store_path个数匹配
tracker_server=192.168.53.85:22122          # tracker服务器IP和端口
tracker_server=192.168.53.86:22122          # tracker服务器IP和端口
```

启动Storage

>启动storage，会根据配置文件的设置自动创建多级存储目录，查看端口23000是否开始监听，确认启动是否成功。

``` sh
[root@localhost fdfs]# fdfs_storaged /etc/fdfs/storage.conf restart
[root@localhost fdfs]# netstat -unltp | grep fdfs
tcp        0      0 0.0.0.0:23000               0.0.0.0:*                   LISTEN      5551/fdfs_storaged  
```

也可以查看storage的日志是否启动成功。

``` sh
[root@localhost logs]# cat /root/fastdfs/logs/storaged.log 
[2017-10-09 15:39:12] INFO - FastDFS v5.05, base_path=/root/fastdfs, store_path_count=1 ...
```

验证storage是否登记到tracker服务器

使用```fdfs_monitor /etc/fdfs/storage.conf```，运行fdfs_monitor查看storage服务器是否已经登记到tracker服务器。

>可以在任一存储节点上使用如下命令查看集群的状态信息 

``` sh
fdfs_monitor /etc/fdfs/storage.conf
```

如果出现ip_addr = <IP> Active, 则表明storage服务器已经登记到tracker服务器，如下：

``` sh
Storage 1:
        id = 192.168.53.90
        ip_addr = 192.168.53.90 (localhost)  ACTIVE
```

至此，tracker、storage等配置都完成并成功启动

接下来，继续完成Nginx和fastdfs-nginx-module的安装和配置


## 在storage上安装nginx

> 注意：fastdfs-nginx-module模块只需要安装到storage上。

### 安装

解压安装包

``` sh
tar -xvzf fastdfs-nginx-module_v1.16.tar.gz -C /usr/local
tar -zvxf nginx-1.7.9.tar.gz  -C /usr/local
```

需要先配置软链接:

``` sh
ln -sv /usr/include/fastcommon /usr/local/include/fastcommon 
ln -sv /usr/include/fastdfs /usr/local/include/fastdfs 
ln -sv /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so
```

> 安装nginx的时候，添加 fastdfs-nginx-module-master模块，如：
> ```./configure --add-module=../fastdfs-nginx-module/src/```

``` sh
cd /usr/local/nginx-1.7.9
./configure --prefix=/usr/local/nginx --add-module=/usr/local/fastdfs-nginx-module/src
```

configure 成功输出结果：

``` sh
checking for OS
 + Linux 2.6.32-431.el6.x86_64 x86_64
checking for C compiler ... found
 + using GNU C compiler
 + gcc version: 4.4.7 20120313 (Red Hat 4.4.7-18) (GCC) 
checking for gcc -pipe switch ... found

......

nginx http access log file: "/usr/local/nginx/logs/access.log"
nginx http client request body temporary files: "client_body_temp"
nginx http proxy temporary files: "proxy_temp"
nginx http fastcgi temporary files: "fastcgi_temp"
nginx http uwsgi temporary files: "uwsgi_temp"
nginx http scgi temporary files: "scgi_temp" 
```
configure成功了

接下来执行make和make install 

``` sh
make
```

确定编译没有出错，再进行install

``` sh
make install 
```

安装成功，查看版本信息

``` sh
/usr/local/nginx/sbin/nginx -V
```

### 配置

**配置fastdfs-nginx-module**

进入fastdfs-nginx-module的src目录，将md_fastdfs.conf配置文件拷贝到/etc/fdfs/目录中

``` sh
cd /usr/local/fastdfs-nginx-module/src
cp mod_fastdfs.conf /etc/fdfs/
```

配置 mod_fastdfs.conf

``` sh
vim /etc/fdfs/mod_fastdfs.conf
```

``` sh
一般只需改动以下几个参数即可：
base_path=/root/fastdfs           #保存日志目录
tracker_server=192.168.53.85:22122
tracker_server=192.168.53.86:22122 
storage_server_port=23000         #storage服务器的端口号
group_name=group1                 #当前服务器的group名
url_have_group_name = true        #文件url中是否有group名
store_path_count=1                #存储路径个数，需要和store_path个数匹配
store_path0=/root/fastdfs         #存储路径
group_count = 2                   #设置组的个数
```

在末尾增加3个组的具体信息：

``` sh
[group1]
group_name=group1
storage_server_port=23000
store_path_count=1
store_path0=/root/fastdfs

[group2]
group_name=group2
storage_server_port=23000
store_path_count=1
store_path0=/root/fastdfs
```

建立M00至存储目录的符号连接。

``` sh
ln -s /root/fastdfs/data /root/fastdfs/data/M00
ll /root/fastdfs/data/M00
```

**配置nginx**

编辑```/usr/local/nginx/conf```配置文件目录下的nginx.conf，设置添加storage信息并保存。

``` sh
vim /usr/local/nginx/conf/nginx.conf
```

将server段中的listen端口号改为8080，启动用户使用root。

``` sh
user root
listen       8080;
```

在server段中添加：

``` sh
location ~/group[1-2]/M00 {
    root /root/fastdfs/data;
    ngx_fastdfs_module;
}
```

复制fastdfs中的http.conf、mime.types文件到/etc/fdfs

``` sh
cp /usr/local/fastdfs-5.05/conf/http.conf /usr/local/fastdfs-5.05/conf/mime.types  /etc/fdfs
```

至此，nginx以及FastDFS插件模块设置完成。

### 运行

运行nginx之前，先要把防火墙中对应的端口打开（本例中为8080）。

``` sh
iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT
/etc/init.d/iptables save
```

启动nginx，确认启动是否成功。（查看是否对应端口8080是否开始监听）

``` sh
[root@localhost ~]# /usr/local/nginx/sbin/nginx
ngx_http_fastdfs_set pid=12768
[root@localhost ~]# netstat -unltp | grep nginx
tcp        0      0 0.0.0.0:8080                0.0.0.0:*                   LISTEN      12769/nginx  
```

也可查看nginx的日志是否启动成功或是否有错误。

``` sh
cat /usr/local/nginx/logs/error.log
```

在error.log中没有错误，既启动成功。可以打开浏览器，直接访问http://192.168.53.90:8080，查看是否弹出nginx欢迎页面。

查看到欢迎页则说明，nginx运行成功。之后依次在其它storage上全部安装上nginx并确认运行正常。

将nginx设置为开机启动：

``` sh
vim /etc/rc.d/rc.local
```

将运行命令行添加进文件：```/usr/local/nginx/sbin/nginx```


## 在tracker上安装nginx

在tracker上安装的nginx主要为了提供http访问的反向代理、负载均衡以及缓存服务。

### 安装

解压

``` sh
tar -zvxf nginx-1.7.9.tar.gz  -C /usr/local
```

运行./configure进行安装前的设置，主要设置安装路径

``` sh
cd /usr/local/nginx-1.7.9
./configure --prefix=/usr/local/nginx
```

运行make进行编译，确保编译成功。

``` sh
make
```

运行make install进行安装。

``` sh
make install
```

### 配置

编辑/usr/local/nginx/conf配置文件目录下的nginx.conf，设置负载均衡

``` sh
vim /usr/local/nginx/conf/nginx.conf
```

配置信息

``` sh
worker_processes  4;                  #根据CPU核心数而定
events {
    worker_connections  65535;        #最大链接数
    use epoll;                        #新版本的Linux可使用epoll加快处理性能
}
http {
    #设置group1的服务器
    upstream fdfs_group1 {
        server 192.168.53.90:8080 weight=1 max_fails=2 fail_timeout=30s;
        server 192.168.54.229:8080 weight=1 max_fails=2 fail_timeout=30s;
    }
    #设置group2的服务器
    upstream fdfs_group2 {
        server 192.168.54.233:8080 weight=1 max_fails=2 fail_timeout=30s;
        server 192.168.54.234:8080 weight=1 max_fails=2 fail_timeout=30s;
    }

   server {
       #设置服务器端口
        listen       8080;
       #设置group1的负载均衡参数
        location /group1/M00 {
            proxy_pass http://fdfs_group1;
        }
        #设置group2的负载均衡参数
        location /group2/M00 {
            proxy_pass http://fdfs_group2;
        }
      }

    }
```

至此，nginx设置完成。

### 运行

运行nginx之前，先要把防火墙中对应的端口打开（本例中为8080）

``` sh
iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT
/etc/init.d/iptables save
```

启动nginx，确认启动是否成功。（查看是否对应端口8080是否开始监听）

``` sh
[root@localhost ~]# /usr/local/nginx/sbin/nginx
ngx_http_fastdfs_set pid=12768
[root@localhost ~]# netstat -unltp | grep nginx
tcp        0      0 0.0.0.0:8080                0.0.0.0:*                   LISTEN      12769/nginx  
```

也可查看nginx的日志是否启动成功或是否有错误。

``` sh
cat /usr/local/nginx/logs/error.log
```

尝试上传一个文件到FastDFS，然后访问试试。先配置client.conf文件。

``` sh
cp client.conf.sample  client.conf
vim /etc/fdfs/client.conf
```

修改以下参数：

``` sh
base_path=/root/fastdfs                   #日志存放路径
tracker_server=192.168.53.85:22122         
tracker_server=192.168.53.86:22122 
http.tracker_server_port=8080
```

使用/usr/local/bin/fdfs_upload_file上传一个文件，程序会自动返回文件的URL。

``` sh
[root@localhost fdfs]# fdfs_upload_file /etc/fdfs/client.conf /root/test.jpg
group2/M00/00/00/wKg26VncfamAEqZ0AAu-4Kcs3QI677.jpg
```

然后使用浏览器访问:

``` sh
http://192.168.53.85:8080/group2/M00/00/00/wKg26VncfamAEqZ0AAu-4Kcs3QI677.jpg
```

看有查看到图片,说明集群搭建成功！

![](http://www.itmind.net/assets/images/neo.jpg)

> 生产中可以将：```/root/fastdfs``` 替换为：```/fdfs/storage```


##  报错

### 编译nginx的时候报错

在nginx目录下，执行configure之后，进行make编译报错，报错内容如下：

``` sh
s -I src/mail \
                -o objs/addon/src/ngx_http_fastdfs_module.o \
                /usr/local/fastdfs-nginx-module/src/ngx_http_fastdfs_module.c
In file included from /usr/local/fastdfs-nginx-module/src/ngx_http_fastdfs_module.c:6:
/usr/local/fastdfs-nginx-module/src/common.c:21:25: error: fdfs_define.h: No such file or directory

......

/usr/local/fastdfs-nginx-module/src/ngx_http_fastdfs_module.c:933: error: ‘true’ undeclared (first use in this function)
make[1]: *** [objs/addon/src/ngx_http_fastdfs_module.o] Error 1
make[1]: Leaving directory `/usr/local/nginx-1.7.9'
make: *** [build] Error 2
```

做以下修改

``` sh
vim /usr/local/fastdfs-nginx-module/src/config
```

将、
``` sh
CORE_INCS="$CORE_INCS /usr/local/include/fastdfs /usr/local/include/fastcommon/"
```

修改为：

``` sh
CORE_INCS="$CORE_INCS /usr/include/fastdfs /usr/local/include/fastcommon/"
```

其实就是改动了fastdfs的路径，没改之前直接访问```cd /usr/local/include/fastdfs```为空目录。

或者设置对应的软连接也可以。

``` sh
ln -sv /usr/include/fastcommon /usr/local/include/fastcommon 
ln -sv /usr/include/fastdfs /usr/local/include/fastdfs 
ln -sv /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so
```

修改完成之后在nginx目录，重新configure和make就好了。

``` sh
./configure --prefix=/usr/local/nginx --add-module=/usr/local/fastdfs-nginx-module/src
make
```

### 启动nginx报错

在在storage上配置nginx相关信息后启动nginx，查看日志发现报错：

``` sh
cat /usr/local/nginx/logs/error.log
ngx_http_fastdfs_process_init pid=12770
[2017-10-10 13:41:44] ERROR - file: ini_file_reader.c, line: 631, include file "http.conf" not exists, line: "#include http.conf"
[2017-10-10 13:41:44] ERROR - file: /usr/local/fastdfs-nginx-module/src/common.c, line: 155, load conf file "/etc/fdfs/mod_fastdfs.conf" fail, ret code: 2
2017/10/10 13:41:44 [alert] 12769#0: worker process 12770 exited with fatal code 2 and cannot be respawned
```

解决方案：

复制fastdfs中的http.conf、mime.types文件到/etc/fdfs

``` sh
cp /usr/local/fastdfs-5.05/conf/http.conf /usr/local/fastdfs-5.05/conf/mime.types  /etc/fdfs
```

然后重启nginx

``` sh
killall nginx
/usr/local/nginx/sbin/nginx
```

查看日志，还报错：

``` sh
[root@localhost logs]# cat /usr/local/nginx/logs/error.log
ngx_http_fastdfs_process_init pid=12813
[2017-10-10 14:05:33] ERROR - file: /usr/local/fastdfs-nginx-module/src/common.c, line: 180, config file: /etc/fdfs/mod_fastdfs.conf, you must set url_have_group_name to true to support multi-group!
2017/10/10 14:05:33 [alert] 12812#0: worker process 12813 exited with fatal code 2 and cannot be respawned
```

解决方案：

``` sh
vim  /etc/fdfs/mod_fastdfs.conf
```

将

``` sh
url_have_group_name=false
```
改为

``` sh
url_have_group_name=true 
```

重启正常



### 测试图片无法访问

搭建完成之后，访问```http://192.168.53.85:8080/group2/M00/00/00/wKg26VncfamAEqZ0AAu-4Kcs3QI677.jpg```
地址图片总是报404无法找到，跟踪到storage服务器，查看nginx的error日志发现如下；

``` sh
ERROR - file: /usr/local/fastdfs-nginx-module/src/common.c, line: 877, stat file: /root/fastdfs/data/00/00/wKg1Wlnchn2AOo0kAAu-4Kcs3QI239.jpg fail, errno: 13, error info: Permission denied
```

原因是nginx启动的时候默认会以nobody用户来启动，这样的话就权限访问```/root/fastdfs/data```的权限

修改这个问题有两个版本，第一个方案设置nginx以root身份启动，或者设置nobody用户权限可以访问```/root/fastdfs/data```地址。这里只展示第一种方案的修改

``` sh
vim /usr/local/nginx/conf/nginx.conf
# 修改nobody为root
user root
```

重启nginx后问题解决

**这里有一个网友整理的word版本的安装配置文档，包括缓存各方面的内容比较全面，需要的朋友在公众号回复：“fastdfs”**

参考：

[CentOS上安装分布式文件系统FastDFS & 配置和问题](https://my.oschina.net/wangmengjun/blog/1142982)