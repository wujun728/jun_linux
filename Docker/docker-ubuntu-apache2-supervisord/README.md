# 基于Docker的PHP服务搭建

## 一.使用方法
### 1.使用docker build -t 镜像名:版本号 路径
#### 例子：docker build -t lamp:latest .
#### 表示使用当前路径的Dockerfile文件生成镜像
## 二.安装的软件
#### 1.apache2 用于HTTP服务
#### 2.php7.0 用于处理PHP脚本
#### 3.php7.0-mysql 用于PHP连接mysql
#### 4.libapache2-mod-php7.0 使apache能处理PHP脚本
#### 5.php7.0-json 为PHP脚本提供json的处理
#### 6.php7.0-gd 为PHP提供图片的处理能力
#### 7.supervisord 用于对其它软件的监控，主要实现对进程的启动以及进程意外停止的自动开启（在docker容器中默认不能使用systemctl或service等命令，所以需要supervisor对进程进行管理）
## 三.文件介绍
### 1.apache/apache2.conf
#### apache配置文件
### 2.apache/sites-enabled/000-default.conf
#### apache监听的端口号，以及虚拟主机路径的配置
### 3.apt/sources.list
#### ubuntu16.04的网易源配置文件(主要用于国内构建镜像，国内使用默认源会非常慢甚至构建失败。)
### 4.supervisor/conf.d/supervisord.conf
#### supervisord的配置文件（包含supervisord需要监听的进程）
## 四.注意事项
### 1.运行镜像时默认配置的网站跟目录为/data/wwwroot/default
#### 运行容器时需要使用-v /data:/data为容器挂载卷，并把网站代码放在主机的/data/wwwroot/default下，并且网站入口文件为index.php或index.html
### 2.需要注意目录权限问题，要给容器足够的权限
#### 发生其它奇怪的问题可以在运行容器时加--privileged给容器特权
### 3.当然还要端口映射了
#### -p 端口号:端口号 将主机的 端口与容器的端口进行映射
### 4.如何使用mysql
#### 容器默认未提供mysql服务，需要先pull一个mysql容器，并运行，然后再运行lamp容器并添加--link mysql:mysql PHP如何调用数据库,其实调用数据库时只需要将连接数据库的主机名填写为mysql就能够直接连接,必须先启动mysql容器再启动lamp容器，因为lamp容器会依赖mysql容器。
### 5.完整运行命令例子
```
docker run --privileged --name lamp -d -v /data:/data -p 80:80 -p 443:443 lamp:latest
```
### 6.个性化
#### 可以更改项目中对应软件的配置文件实现其它的个性化设置，然后再构建容器镜像
### 7.演示
![](https://git.oschina.net/lebar/docker-ubuntu-apache2-supervisord/raw/master/thumbnail.png)