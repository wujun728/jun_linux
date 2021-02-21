#!/usr/bin/env bash
kafka-topics.sh --create --zookeeper 192.168.99.101:2181 --replication-factor 1 --partitions 3 --topic debugo01
kafka-topics.sh --create --zookeeper 192.168.99.101:2181 --replication-factor 3 --partitions 1 --topic debugo02
kafka-topics.sh --create --zookeeper 192.168.99.101:2181 --replication-factor 2 --partitions 3 --topic debugo03

kafka-topics.sh --list --zookeeper 192.168.99.101:2181

kafka-topics.sh --describe --zookeeper 192.168.99.101:2181 --topic debugo01
kafka-topics.sh --describe --zookeeper 192.168.99.101:2181 --topic debugo02
kafka-topics.sh --describe --zookeeper 192.168.99.101:2181 --topic debugo03

# 生产者
kafka-console-producer.sh --broker-list 192.168.99.101:9092,192.168.99.101:9093,192.168.99.101:9094  --topic debugo03
# 消费者
kafka-console-consumer.sh --zookeeper 192.168.99.101:2181 --from-beginning --topic debugo03

###kafka redis 性能相当
#下面使用perf命令来测试几个topic的性能，需要先下载kafka-perf_2.10-0.8.1.1.jar，并拷贝到kafka/libs下面。
#50W条消息，每条1000字节，batch大小1000，topic为debugo01，4个线程（message size设置太大需要调整相关参数，否则容易OOM）。只用了18秒完成，kafka在多分区支持下吞吐量是非常给力的。
kafka-producer-perf-test.sh --messages 500000 --message-size 1000  --batch-size 1000 --topics debugo01 --threads 4 --broker-list 192.168.99.101:9092,192.168.99.101:9093,192.168.99.101:9094
##2015-11-20 23:07:07:576, 2015-11-20 23:07:25:781, 0, 1000, 1000, 476.84, 26.1926, 500000, 27464.9821


#同样的参数测试debugo02, 由于但分区加复制（replicas-factor=3），用时29秒。所以，适当加大partition数量和broker相关线程数量会极大的提高性能。
kafka-producer-perf-test.sh --messages 500000 --message-size 1000  --batch-size 1000 --topics debugo02 --threads 4 --broker-list 192.168.99.101:9092,192.168.99.101:9093,192.168.99.101:9094
#测试有错误
##2015-11-20 23:00:40:044, 2015-11-20 23:01:09:510, 0, 1000, 1000, 476.84, 16.1826, 500000, 16968.7097

#同样的参数测试debugo03，用时26秒。
kafka-producer-perf-test.sh --messages 500000 --message-size 1000  --batch-size 1000 --topics debugo03 --threads 4 --broker-list 192.168.99.101:9092,192.168.99.101:9093,192.168.99.101:9094
# 消息复制出现错误
##2015-11-20 23:04:52:655, 2015-11-20 23:05:18:417, 0, 1000, 1000, 476.84, 18.5093, 500000, 19408.4310


#测试comsumer的性能。17/20/19
kafka-consumer-perf-test.sh --zookeeper 192.168.99.101:2181 --messages 500000 --topic debugo01 --threads 3
#2015-11-20 23:08:51:074, 2015-11-20 23:09:08:370, 1048576, 476.8372, 38.7799, 500000, 40663.6304

kafka-consumer-perf-test.sh --zookeeper 192.168.99.101:2181 --messages 500000 --topic debugo02 --threads 3
#2015-11-20 23:09:29:018, 2015-11-20 23:09:49:459, 1048576, 476.8372, 30.8812, 500000, 32381.3225

kafka-consumer-perf-test.sh --zookeeper 192.168.99.101:2181 --messages 500000 --topic debugo03 --threads 3
#2015-11-20 23:11:48:033, 2015-11-20 23:12:07:603, 1048576, 476.8372, 32.7273, 500000, 34317.0899

