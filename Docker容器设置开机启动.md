# [docker容器怎么设置开机启动](https://www.cnblogs.com/gcgc/p/10494615.html)



**目录**

- 一、docker服务设置自动启动
  - [查看已启动的服务](https://www.cnblogs.com/gcgc/p/10494615.html#_label0_0)
  - [查看是否设置开机启动](https://www.cnblogs.com/gcgc/p/10494615.html#_label0_1)
  - [设置开机启动](https://www.cnblogs.com/gcgc/p/10494615.html#_label0_2)
  - [关闭开机启动](https://www.cnblogs.com/gcgc/p/10494615.html#_label0_3)
- 二、docker容器设置自动启动
  - [启动时加--restart=always](https://www.cnblogs.com/gcgc/p/10494615.html#_label1_0)
  - [如果已经过运行的项目](https://www.cnblogs.com/gcgc/p/10494615.html#_label1_1)

 

------

https://my.oschina.net/lwenhao/blog/1923003

# docker服务器、以及容器设置自动启动

[回到顶部](https://www.cnblogs.com/gcgc/p/10494615.html#_labelTop)

## 一、docker服务设置自动启动

说明：适用于yum安装的各种服务



### 查看已启动的服务

```
systemctl list-units --type=service
```



### 查看是否设置开机启动

```
systemctl list-unit-files | grep enable
```



### 设置开机启动

```
systemctl enable docker.service
```



### 关闭开机启动

```
systemctl disable docker.service
```

[回到顶部](https://www.cnblogs.com/gcgc/p/10494615.html#_labelTop)

## 二、docker容器设置自动启动



### 启动时加--restart=always

```
docker run -tid --name isaler_v0.0.11 -p 8081:8080 --restart=always -v /alidata/iDocker/run/projectImages/isaler/v0.0.11/log:/usr/local/tomcat/logs isaler_v0.0.11


Flag	Description
no		不自动重启容器. (默认value)
on-failure 	容器发生error而退出(容器退出状态不为0)重启容器
unless-stopped 	在容器已经stop掉或Docker stoped/restarted的时候才重启容器
always 	在容器已经stop掉或Docker stoped/restarted的时候才重启容器
```



### 如果已经过运行的项目

```
如果已经启动的项目，则使用update更新：
docker update --restart=always isaler_v0.0.11
```