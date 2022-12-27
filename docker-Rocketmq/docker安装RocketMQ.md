### docker安装RocketMQ

 目录
1.创建namesrv服务
拉取镜像
创建namesrv数据存储路径
构建namesrv容器
2.创建broker节点
创建broker数据存储路径
创建配置文件
构建broker容器
3.创建rockermq-console服务
拉取镜像
构建rockermq-console容器
需要关闭防火墙或者开放namesrv和broker端口
关闭防火墙
开放指定端口
访问控制台
1.创建namesrv服务
拉取镜像
docker pull rocketmqinc/rocketmq
1
创建namesrv数据存储路径
mkdir -p  /docker/rocketmq/data/namesrv/logs   /docker/rocketmq/data/namesrv/store
1
构建namesrv容器
docker run -d \
--restart=always \
--name rmqnamesrv \
-p 9876:9876 \
-v /docker/rocketmq/data/namesrv/logs:/root/logs \
-v /docker/rocketmq/data/namesrv/store:/root/store \
-e "MAX_POSSIBLE_HEAP=100000000" \
rocketmqinc/rocketmq \
sh mqnamesrv 
1
2
3
4
5
6
7
8
9
参数	说明
-d	以守护进程的方式启动
- -restart=always	docker重启时候容器自动重启
- -name rmqnamesrv	把容器的名字设置为rmqnamesrv
-p 9876:9876	把容器内的端口9876挂载到宿主机9876上面
-v /docker/rocketmq/data/namesrv/logs:/root/logs	把容器内的/root/logs日志目录挂载到宿主机的 /docker/rocketmq/data/namesrv/logs目录
-v /docker/rocketmq/data/namesrv/store:/root/store	把容器内的/root/store数据存储目录挂载到宿主机的 /docker/rocketmq/data/namesrv目录
rmqnamesrv	容器的名字
-e “MAX_POSSIBLE_HEAP=100000000”	设置容器的最大堆内存为100000000
rocketmqinc/rocketmq	使用的镜像名称
sh mqnamesrv	启动namesrv服务
2.创建broker节点
创建broker数据存储路径
mkdir -p  /docker/rocketmq/data/broker/logs   /docker/rocketmq/data/broker/store /docker/rocketmq/conf
1
创建配置文件
vi /docker/rocketmq/conf/broker.conf
# 所属集群名称，如果节点较多可以配置多个
brokerClusterName = DefaultCluster
#broker名称，master和slave使用相同的名称，表明他们的主从关系
brokerName = broker-a
#0表示Master，大于0表示不同的slave
brokerId = 0
#表示几点做消息删除动作，默认是凌晨4点
deleteWhen = 04
#在磁盘上保留消息的时长，单位是小时
fileReservedTime = 48
#有三个值：SYNC_MASTER，ASYNC_MASTER，SLAVE；同步和异步表示Master和Slave之间同步数据的机制；
brokerRole = ASYNC_MASTER
#刷盘策略，取值为：ASYNC_FLUSH，SYNC_FLUSH表示同步刷盘和异步刷盘；SYNC_FLUSH消息写入磁盘后才返回成功状态，ASYNC_FLUSH不需要；
flushDiskType = ASYNC_FLUSH
# 设置broker节点所在服务器的ip地址
brokerIP1 = 192.168.52.136
# 磁盘使用达到95%之后,生产者再写入消息会报错 CODE: 14 DESC: service not available now, maybe disk full
diskMaxUsedSpaceRatio=95

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
构建broker容器
docker run -d  \
--restart=always \
--name rmqbroker \
--link rmqnamesrv:namesrv \
-p 10911:10911 \
-p 10909:10909 \
-v  /docker/rocketmq/data/broker/logs:/root/logs \
-v  /docker/rocketmq/data/broker/store:/root/store \
-v /docker/rocketmq/conf/broker.conf:/opt/rocketmq-4.4.0/conf/broker.conf \
-e "NAMESRV_ADDR=namesrv:9876" \
-e "MAX_POSSIBLE_HEAP=200000000" \
rocketmqinc/rocketmq \
sh mqbroker -c /opt/rocketmq-4.4.0/conf/broker.conf 
1
2
3
4
5
6
7
8
9
10
11
12
13
参数	说明
-d	以守护进程的方式启动
–restart=always	docker重启时候镜像自动重启
- -name rmqbroker	把容器的名字设置为rmqbroker
- --link rmqnamesrv:namesrv	和rmqnamesrv容器通信
-p 10911:10911	把容器的非vip通道端口挂载到宿主机
-p 10909:10909	把容器的vip通道端口挂载到宿主机
-e “NAMESRV_ADDR=namesrv:9876”	指定namesrv的地址为本机namesrv的ip地址:9876
-e “MAX_POSSIBLE_HEAP=200000000” rocketmqinc/rocketmq sh mqbroker	指定broker服务的最大堆内存
rocketmqinc/rocketmq	使用的镜像名称
sh mqbroker -c /opt/rocketmq-4.4.0/conf/broker.conf	指定配置文件启动broker节点
3.创建rockermq-console服务
拉取镜像
docker pull pangliang/rocketmq-console-ng
1
构建rockermq-console容器
需要把192.168.52.136换成部署namesrv机器地址

docker run -d \
--restart=always \
--name rmqadmin \
-e "JAVA_OPTS=-Drocketmq.namesrv.addr=192.168.52.136:9876 \
-Dcom.rocketmq.sendMessageWithVIPChannel=false" \
-p 9999:8080 \
pangliang/rocketmq-console-ng
1
2
3
4
5
6
7
参数	说明
-d	以守护进程的方式启动
- -restart=always	docker重启时候镜像自动重启
- -name rmqadmin	把容器的名字设置为rmqadmin
-e "JAVA_OPTS=-Drocketmq.namesrv.addr=192.168.52.136:9876	设置namesrv服务的ip地址
-Dcom.rocketmq.sendMessageWithVIPChannel=false"	不使用vip通道发送消息
–p 9999:8080	把容器内的端口8080挂载到宿主机上的9999端口
需要关闭防火墙或者开放namesrv和broker端口
如果不设置,控制台服务将无法访问namesrv服务
异常信息如下
org.apache.rocketmq.remoting.exception.RemotingConnectException: connect to failed



关闭防火墙
systemctl stop firewalld.service
1
开放指定端口
firewall-cmd --permanent --zone=public --add-port=9876/tcp
firewall-cmd --permanent --zone=public --add-port=10911/tcp
# 立即生效
firewall-cmd --reload
1
2
3
4
访问控制台
网页访问http://192.168.52.136:9999/查看控制台信息

 