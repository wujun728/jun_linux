# [Nginx Linux详细安装部署教程](https://www.cnblogs.com/taiyonghai/p/6728707.html)

**一、Nginx简介**

Nginx是一个web服务器也可以用来做负载均衡及反向代理使用，目前使用最多的就是负载均衡，具体简介我就不介绍了百度一下有很多，下面直接进入安装步骤

**二、Nginx安装**

**1、下载Nginx及相关组件**

Linux系统是Centos 6.5 64位，我直接切换到root用户下安装

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418152744852-939208787.png)

进入用户目录下载程序

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418153003446-820207739.png)

下载相关组件

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@localhost src]# wget http://nginx.org/download/nginx-1.10.2.tar.gz
省略安装内容...
[root@localhost src]# wget http://www.openssl.org/source/openssl-fips-2.0.10.tar.gz
省略安装内容...
[root@localhost src]# wget http://zlib.net/zlib-1.2.11.tar.gz
省略安装内容...
[root@localhost src]# wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.40.tar.gz
省略安装内容...
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

安装c++编译环境，如已安装可略过

```
[root@localhost src]# yum install gcc-c++
省略安装内容...
期间会有确认提示输入y回车
Is this ok [y/N]:y
省略安装内容...
```

**2、安装Nginx及相关组件**

openssl安装

```
[root@localhost src]# tar zxvf openssl-fips-2.0.10.tar.gz省略安装内容...
[root@localhost src]# cd openssl-fips-2.0.10
[root@localhost openssl-fips-2.0.10]# ./config && make && make install省略安装内容...
```

pcre安装

```
[root@localhost src]# tar zxvf pcre-8.40.tar.gz省略安装内容...
[root@localhost src]# cd pcre-8.40
[root@localhost pcre-8.40]# ./configure && make && make install省略安装内容...
```

zlib安装

```
[root@localhost src]# tar zxvf zlib-1.2.11.tar.gz省略安装内容...
[root@localhost src]# cd zlib-1.2.11
[root@localhost zlib-1.2.11]# ./configure && make && make install省略安装内容...
```

nginx安装

```
[root@localhost src]# tar zxvf nginx-1.10.2.tar.gz省略安装内容...
[root@localhost src]# cd nginx-1.10.2
[root@localhost nginx-1.10.2]# ./configure && make && make install省略安装内容...
```

**3、启动Nginx**

先找一下nginx安装到什么位置上了

 ![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418154742915-713647057.png)

进入nginx目录并启动

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418154804759-1842869219.png)

报错了，error while loading shared libraries: libpcre.so.1: cannot open shared object file: No such file or directory，按照下面方式解决

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
1.用whereis libpcre.so.1命令找到libpcre.so.1在哪里
2.用ln -s /usr/local/lib/libpcre.so.1 /lib64命令做个软连接就可以了
3.用sbin/nginx启动Nginx
4.用ps -aux | grep nginx查看状态
[root@localhost nginx]# whereis libpcre.so.1
[root@localhost nginx]# ln -s /usr/local/lib/libpcre.so.1 /lib64
[root@localhost nginx]# sbin/nginx
[root@localhost nginx]# ps -aux | grep nginx 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418162004024-2058687645.png)

进入Linux系统的图形界面，打开浏览器输入localhost会看到下图，说明nginx启动成功

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418162145790-461736932.png)

nginx的基本操作

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
启动
[root@localhost ~]# /usr/local/nginx/sbin/nginx
停止/重启
[root@localhost ~]# /usr/local/nginx/sbin/nginx -s stop(quit、reload)
命令帮助
[root@localhost ~]# /usr/local/nginx/sbin/nginx -h
验证配置文件
[root@localhost ~]# /usr/local/nginx/sbin/nginx -t
配置文件
[root@localhost ~]# vim /usr/local/nginx/conf/nginx.conf
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

**4、简单配置Nginx**

打开nginx配置文件位于nginx目录下的conf文件夹下

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418164812196-1164065507.png)

简单介绍一下vim的语法

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
默认vim打开后是不能录入的，需要按键才能操作，具体如下：
开启编辑：按“i”或者“Insert”键
退出编辑：“Esc”键
退出vim：“:q”
保存vim：“:w”
保存退出vim：“:wq”
不保存退出vim：“:q!”
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

"#"代表注释，最重要的是server{}块这部分就代表每一个web站点，详细的配置介绍可以查阅我的另一片配置文章，此处我们先暂时设置三个站点

 ![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418173628696-1685332558.png)

分别使用不同的端口80、81、82保存退出并且重启nginx

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418174444118-588824024.png)

**5、开启外网访问**

在Linux系统中默认有防火墙Iptables管理者所有的端口，只启用默认远程连接22端口其他都关闭，咱们上面设置的80等等也是关闭的，所以我们需要先把应用的端口开启

**方法一**直接关闭防火墙，这样性能较好，但安全性较差，如果有前置防火墙可以采取这种方式

```
关闭防火墙
[root@localhost ~]# service iptables stop
关闭开机自启动防火墙
[root@localhost ~]# chkconfig iptables off
[root@localhost ~]# chkconfig --list|grep ipt
```

下面是防火墙的其他操作命令

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418175910868-1921833075.png)

**方法二**将开启的端口加入防火墙白名单中，这种方式较安全但性能也相对较差

```
编辑防火墙白名单
[root@localhost ~]# vim /etc/sysconfig/iptables
增加下面一行代码
-A INPUT -p tcp -m state -- state NEW -m tcp --dport 80 -j ACCEPT
保存退出，重启防火墙
[root@localhost ~]# service iptables restart
```

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418180736931-1955851185.png)

 

Linux配置完毕了，使用另一台电脑而非安装nginx的电脑，我是用的windows系统，配置一下host在“C:\Windows\System32\drivers\etc”下的hosts中配置一下域名重定向

```
10.11.13.22 nginx.test.com nginx.test1.com nginx.test2.com
```

然后cmd再ping一下这个域名是否正确指向了这个IP上

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418174908977-27238342.png)

正确指向后在telnet一下80端口看一下是否可以与端口通信（如果telnet提示没有此命令是没有安装客户端，在启用或禁用windows功能处安装后再操作即可）

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418175445712-2089843604.png)

得到以下界面及代表通信成功

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418175512790-352719306.png)

打开这台Windows系统内的浏览器，输入nginx.test.com会得到以下结果，就说明外网访问成功

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418181546415-521855633.png)

如果防火墙你依然启用，只是设置了启用端口，那我们访问81那个端口会发现无法访问，因为我并没有加入白名单

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170418181649259-174579881.png)

到此Nginx服务器雏形部署完成。

**6、Nginx负载均衡配置**

 Nginx集反向代理和负载均衡于一身，在配置文件中修改配就可以实现

首先我们打开配置文件

```
[root@localhost nginx]# vim conf/nginx.conf
```

 每一个server就是一个虚拟主机，我们有一个当作web服务器来使用

```
listen 80;代表监听80端口
server_name xxx.com;代表外网访问的域名
location / {};代表一个过滤器，/匹配所有请求，我们还可以根据自己的情况定义不同的过滤，比如对静态文件js、css、image制定专属过滤
root html;代表站点根目录
index index.html;代表默认主页
```

 ![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170419164359634-2043724986.png)

这样配置完毕我们输入域名就可以访问到该站点了。

负载均衡功能往往在接收到某个请求后分配到后端的多台服务器上，那我们就需要upstream{}块来配合使用

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
upstream xxx{};upstream模块是命名一个后端服务器组，组名必须为后端服务器站点域名，内部可以写多台服务器ip和port，还可以设置跳转规则及权重等等
ip_hash;代表使用ip地址方式分配跳转后端服务器，同一ip请求每次都会访问同一台后端服务器
server;代表后端服务器地址

server{};server模块依然是接收外部请求的部分
server_name;代表外网访问域名
location / {};同样代表过滤器，用于制定不同请求的不同操作
proxy_pass;代表后端服务器组名，此组名必须为后端服务器站点域名

server_name和upstream{}的组名可以不一致，server_name是外网访问接收请求的域名，upstream{}的组名是跳转后端服务器时站点访问的域名
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 ![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170419165116649-972950787.png)

配置一下Windows的host将我们要访问的域名aaa.test.com指向Linux

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170419170949509-1331178335.png)

因为硬件有限，我是将Windows中的IIS作为Nginx的后端服务器，所以配置一下IIS的站点域名

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170419171121993-488143433.png)

打开cmd再ping一下aaa.test.com确实指向Linux系统了，再打开浏览器输入aaa.test.com会显示bbb这个站点就代表负载成功了。

![img](https://images2015.cnblogs.com/blog/172889/201704/172889-20170419171408649-130031505.png)

Nginx的负载功能就配置完成了，这只是简单设置了一下，生产环境中还有很多详细的调整，后续再逐渐增加，本人水平有限，如有不对之处还望指导谢谢。

 