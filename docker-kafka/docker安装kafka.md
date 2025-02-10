docker安装kafka

 
目录
1.前置条件：先按zookeeper
2.正题：安装kafka
3.参数意义
4.验证kafka是否可以使用
4.1 进入容器
4.2 进入路径
4.3运行kafka生产者发送消息
4.4 发送消息
1.前置条件：先按zookeeper
docker run -d --name zookeeper -p 2181:2181 -v /etc/localtime:/etc/localtime wurstmeister/zookeeper
1


2.正题：安装kafka
docker run  -d --name kafka -p 9092:9092 -e KAFKA_BROKER_ID=0 -e KAFKA_ZOOKEEPER_CONNECT=10.9.44.11:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://10.9.44.11:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -t wurstmeister/kafka

1
2
3.参数意义
-e KAFKA_BROKER_ID=0 在kafka集群中，每个kafka都有一个BROKER_ID来区分自己

-e KAFKA_ZOOKEEPER_CONNECT=10.9.44.11:2181/kafka 配置zookeeper管理kafka的路径10.9.44.11:2181/kafka

-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://10.9.44.11:9092 把kafka的地址端口注册给zookeeper

-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 配置kafka的监听端口

-v /etc/localtime:/etc/localtime 容器时间同步虚拟机的时间



4.验证kafka是否可以使用
4.1 进入容器
docker exec -it kafka /bin/sh
1
4.2 进入路径
cd /opt/kafka_2.11-2.0.0/bin

4.3运行kafka生产者发送消息
./kafka-console-producer.sh --broker-list localhost:9092 --topic sun

4.4 发送消息
{“datas”:[{“channel”:"",“metric”:“temperature”,“producer”:“ijinus”,“sn”:“IJA0101-00002245”,“time”:“1543207156000”,“value”:“80”}],“ver”:“1.0”}

https://www.cnblogs.com/vipsoft/p/13233045.html
————————————————
版权声明：本文为CSDN博主「方方园园」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_22041375/article/details/106180415