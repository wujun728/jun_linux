fig up -d && fig ps
kafka-topics.sh --create --zookeeper 192.168.59.103:2181 --replication-factor 1 --partitions 1 --topic storm-sentence
java -cp storm-kafka-0.8-plus-test-0.2.0-SNAPSHOT-jar-with-dependencies.jar storm.kafka.KafkaSpoutTestTopology 192.168.59.103:2181