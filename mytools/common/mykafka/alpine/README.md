image is 187Mb
Usage
make a kafka data dir and and the directory zookeeper.
docker run -d -p 9092:9092 -p 2181:2181 -v /kafka/data:/tmp --name kafka --hostname kafka danielguerra/alpine-kafka
The server listens to 9092 and 2181

kafka shell
docker run -ti --link kafka:kafka --name kafka-shell --hostname kafka-shell danielguerra/alpine-kafka /bin/bash