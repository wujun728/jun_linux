# docker方式搭建zookeeper集群

 docker方式搭建zookeeper集群，主要包括docker方式搭建zookeeper集群使用实例、应用技巧、基本知识点总结和需要注意事项，具有一定的参考价值，需要的朋友可以参考一下。



方式一：单台服务器搭建zookeeper集群

一、取镜像，本篇以3.4.10为例

```
docker pull zookeeper #拉取最新的镜像
docker pull zookeeper:3.4.10 # 拉取指定版本
```

二、创建镜像，启动服务

```
docker run -d --name zk01 -p 2181:2181 --ip 10.88.0.19 zookeeper:3.4.10
docker run -d --name zk02 -p 2182:2181 --ip 10.88.0.20 zookeeper:3.4.10
docker run -d --name zk03 -p 2183:2181 --ip 10.88.0.21 zookeeper:3.4.10
```

注意：

1. 宿主机要用不同的端口去映射zookeeper的2181端口，否则从第二个容器开始会启动失败
2. 还有就是ip地址要指定设置成静态，否则后面容器停了之后再次启动ip地址可能会有改变，这样导致集群搭建失败
3. 如果失败请看第三部网络配置问题

三、指定容器IP的注意事项

Docker创建容器时默认采用bridge网络，自行分配ip，不允许自己指定。在实际部署中，我们需要指定容器ip，不允许其自行分配ip，尤其是搭建集群时，固定ip是必须的。我们可以创建自己的bridge网络 ： mynet，创建容器的时候指定网络为mynet并指定ip即可。

1.查看网络模式

```
[root@k8s-node-1 ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
3dfc7f4e8674        bridge              bridge              local
459fab2289a4        host                host                local
aeaff244696b        none                null                local
```

2.创建一个新的bridge网络

```
docker network create --driver bridge --subnet=172.18.12.0/16 --gateway=172.18.1.1 mynet
```

3.查看网络信息

```
docker network inspect mynet
```

4.创建容器并指定容器ip

```
// 建议用此命令运行容器
docker run -e TZ="Asia/Shanghai" --privileged -itd -h zookeeper01.com --name zk01.com --network=mynet -p 2181:2181 --ip 172.18.12.1 zookeeper:3.4.10 
docker run -e TZ="Asia/Shanghai" --privileged -itd -h zookeeper01.com --name zk01.com --network=mynet -p 2182:2181 --ip 172.18.12.2 zookeeper:3.4.10 
docker run -e TZ="Asia/Shanghai" --privileged -itd -h zookeeper01.com --name zk01.com --network=mynet -p 2183:2181 --ip 172.18.12.3 zookeeper:3.4.10 
```

解释说明:

- --privileged 可以有很多权限
- -e TZ="Asia/Shanghai" 时区
- -h zk01.com 主机名
- --name zk01 容器名字
- -i ：开启标准输入
- -it :合起来实现和容器交互的作用，运行一个交互式会话 shell
- -d : 后台运行
- -p 宿主机与容器映射端口

5.查看容器ip

```
docker inspect 容器id
```

四、 修改zookeeper配置

1、修改zoo.cfg

```
[root@k8s-node-1 ~]# docker exec -it zk01 /bin/bash
bash-4.3# vi /conf/zoo.cfg
```

将如下配置内容写入zoo.cfg的最后

```
server.1=172.18.12.1:2888:3888
server.2=172.18.12.2:2888:3888
server.3=172.18.12.3:2888:3888
```

注意：

- 每一行后面都不能有空格，ip或端口都不能有错误。任意一个节点异常，都会导致整个集群的异常
- server.1 此处的1或2或3，是每个zookeeper节点的myid的值

注意：
请注意，如果你是在Linux环境下直接搭建zookeeper，请修改本机所在节点的ip为0.0.0.0
例如我当前节点是server.1，则ip修改为0.0.0.0（非docker环境），如下配置：

```
server.1=0.0.0.0:2888:3888;2181
server.2=10.88.0.20:2888:3888;2181
server.3=10.88.0.21:2888:3888;2181
```

2、修改myid

```
bash-4.3# vi /data/myid
```

注意：

- 前面已经说了，myid里面写的是数字，每个节点的数字不要重复
- zk01的myid是1，zk02的myid是2，zk03的myid是3

所有zookeeper节点的上述两个配置都配置完毕，接下来就是重启docker容器。

五、重启docker容器

使用exit命令退出容器后，重启三个docker服务

```
bash-4.3# exit
exit
[root@k8s-node-1 ~]# docker restart zk01 zk02 zk03
```

六、检查集群状态

分别进入三个容器

```
[root@k8s-node-1 ~]# docker exec -it zk01 /bin/bash
bash-4.3# /zookeeper-3.4.10/bin/zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /conf/zoo.cfg
Mode: leader
[root@k8s-node-1 ~]# docker exec -it zk02 /bin/bash
bash-4.3# /zookeeper-3.4.10/bin/zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /conf/zoo.cfg
Mode: follower
[root@k8s-node-1 ~]# docker exec -it zk03 /bin/bash
bash-4.3# /zookeeper-3.4.10/bin/zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /conf/zoo.cfg
Mode: follower
```

可以看到zk01是leader，zk02和zk03是follower

结束！



原文地址：https://www.cnblogs.com/aaronthon/p/16178227.html