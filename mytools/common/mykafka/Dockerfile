FROM    supermy/docker-jre:7

MAINTAINER supermy

RUN apt-get update && apt-get install -y unzip

RUN wget  http://apache.fayea.com/kafka/0.9.0.0/kafka_2.11-0.9.0.0.tgz -O /tmp/kafka_2.11-0.9.0.0.tgz


RUN tar xfz /tmp/kafka_2.11-0.9.0.0.tgz -C /opt

RUN rm /tmp/kafka_2.11-0.9.0.0.tgz

VOLUME ["/kafka"]

ENV KAFKA_HOME /opt/kafka_2.11-0.9.0.0

ADD shell/start-kafka.sh /usr/bin/start-kafka.sh
ADD shell/broker-list.sh /usr/bin/broker-list.sh

RUN chmod a+x /usr/bin/start-kafka.sh
RUN chmod a+x /usr/bin/broker-list.sh


CMD start-kafka.sh