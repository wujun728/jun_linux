##使用说明：

### 安装docker和composer
[安装docker和composer请点我](http://git.oschina.net/ibenchu/docker-lnmp/wikis/docker%E5%AE%89%E8%A3%85)

### 下载
```
git clone http://git.oschina.net/ibenchu/docker-lnmp
```
### yml文件（可跳过）

ports 宿主机端口:容器端口
volumes 宿主机目录:容器目录
links 用于连接容器，容器别名:连接名

### 配置nginx文件

在config目录的conf目录下
新建主机请建在vhost目录下，可以参照demo

### 运行

第一次运行

```
docker-compose up
```

启动、重启、关闭： `docker-compose start`   `docker-compose retart`   `docker-compose stop`
 
**请一定在yml文件所在目录执行** 

### 使用说明

[查看使用说明（PHP\composer）](http://git.oschina.net/ibenchu/docker-lnmp/wikis/php%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)

[nginx使用说明](http://git.oschina.net/ibenchu/docker-lnmp/wikis/nginx(openresty)%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)